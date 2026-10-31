# -*- coding: utf-8 -*-
"""Минимальный читатель PDF (stdlib): xref-таблицы и xref-потоки, объектные потоки, Flate. Только чтение/разбор."""
import re, zlib

class PDF:
    def __init__(self, data):
        self.d = data
        self.xref = {}      # num -> ('off', offset) | ('stm', stmnum, idx)
        self.trailer = {}
        self._objstm = {}
        self._read_xref()

    # --- токены словарей (упрощённый разбор) ---
    def _read_xref(self):
        d = self.d
        pos = int(re.search(rb'startxref\s+(\d+)\s*%%EOF\s*$', d[-200:], re.S).group(1))
        seen = set(); first = True
        while pos is not None and pos not in seen:
            seen.add(pos)
            if d[pos:pos+4] == b'xref':
                tr = d.index(b'trailer', pos)
                body = d[pos+4:tr]
                lines = body.split()
                i = 0
                while i < len(lines):
                    start, cnt = int(lines[i]), int(lines[i+1]); i += 2
                    for k in range(cnt):
                        off, gen, t = lines[i], lines[i+1], lines[i+2]; i += 3
                        if t == b'n' and (start+k) not in self.xref: self.xref[start+k] = ('off', int(off))
                tdict = self.parse_dict(d, tr + 7)[0]
                if first: self.trailer = tdict
                if b'XRefStm' in tdict:
                    self._xrefstm(int(tdict[b'XRefStm']))
                pos = int(tdict[b'Prev']) if b'Prev' in tdict else None
            else:
                tdict = self._xrefstm(pos)
                if first: self.trailer = tdict
                pos = int(tdict[b'Prev']) if b'Prev' in tdict else None
            first = False

    def _xrefstm(self, pos):
        num, dic, raw = self.read_obj_at(pos)
        data = self.decode_stream(dic, raw)
        w = [int(x) for x in re.findall(rb'\d+', dic[b'W'])]
        size = int(dic[b'Size'])
        idx = [int(x) for x in re.findall(rb'\d+', dic[b'Index'])] if b'Index' in dic else [0, size]
        rl = sum(w); p = 0
        for a in range(0, len(idx), 2):
            for n in range(idx[a], idx[a] + idx[a+1]):
                row = data[p:p+rl]; p += rl
                f = [int.from_bytes(row[sum(w[:j]):sum(w[:j+1])], 'big') if w[j] else (1 if j == 0 else 0) for j in range(3)]
                if n in self.xref: continue
                if f[0] == 1: self.xref[n] = ('off', f[1])
                elif f[0] == 2: self.xref[n] = ('stm', f[1], f[2])
        return dic

    # --- разбор словаря: значения хранятся «сырыми» байтами ---
    @staticmethod
    def parse_dict(d, pos):
        i = d.index(b'<<', pos) + 2; depth = 1; out = {}
        # простой токенайзер верхнего уровня
        def skip_ws(i):
            while d[i:i+1] in b' \t\r\n\x00\x0c': i += 1
            return i
        def read_val(i):
            i = skip_ws(i)
            c = d[i:i+1]
            if d[i:i+2] == b'<<':
                j = i + 2; dep = 1
                while dep:
                    if d[j:j+2] == b'<<': dep += 1; j += 2
                    elif d[j:j+2] == b'>>': dep -= 1; j += 2
                    else: j += 1
                return d[i:j], j
            if c == b'[':
                j = i + 1; dep = 1
                while dep:
                    ch = d[j:j+1]
                    if ch == b'[': dep += 1
                    elif ch == b']': dep -= 1
                    elif ch == b'(':
                        k = j + 1; lv = 1
                        while lv:
                            if d[k:k+1] == b'\\': k += 1
                            elif d[k:k+1] == b'(': lv += 1
                            elif d[k:k+1] == b')': lv -= 1
                            k += 1
                        j = k - 1
                    j += 1
                return d[i:j], j
            if c == b'(':
                k = i + 1; lv = 1
                while lv:
                    if d[k:k+1] == b'\\': k += 1
                    elif d[k:k+1] == b'(': lv += 1
                    elif d[k:k+1] == b')': lv -= 1
                    k += 1
                return d[i:k], k
            if c == b'<':
                j = d.index(b'>', i) + 1; return d[i:j], j
            m = re.compile(rb'/?[^\s/<>\[\]()%]+').match(d, i)
            val = m.group(0); j = m.end()
            m2 = re.compile(rb'\s+(\d+)\s+R(?![A-Za-z])').match(d, j)
            if m2 and re.fullmatch(rb'\d+', val): return val + b' ' + m2.group(1) + b' R', m2.end()
            return val, j
        while True:
            i = skip_ws(i)
            if d[i:i+2] == b'>>': return out, i + 2
            k, i = read_val(i)
            v, i = read_val(i)
            out[k[1:]] = v

    def read_obj_at(self, off):
        d = self.d
        m = re.compile(rb'(\d+)\s+(\d+)\s+obj\s*').match(d, off)
        num = int(m.group(1)); p = m.end()
        if d[p:p+2] != b'<<':
            end = d.index(b'endobj', p); return num, d[p:end].strip(), None
        dic, q = self.parse_dict(d, p)
        m2 = re.compile(rb'\s*stream\r?\n').match(d, q)
        if not m2: return num, dic, None
        s = m2.end()
        ln = dic.get(b'Length', b'0')
        if re.fullmatch(rb'\d+ \d+ R', ln): ln = self.get(int(ln.split()[0]))[1] if False else self._len(ln)
        n = int(ln)
        return num, dic, d[s:s+n]

    def _len(self, ref):
        o = self.xref[int(ref.split()[0])]
        return self.read_obj_at(o[1])[1]

    @staticmethod
    def decode_stream(dic, raw):
        f = dic.get(b'Filter', b'')
        if b'FlateDecode' in f:
            data = zlib.decompress(raw)
            dp = dic.get(b'DecodeParms', b'')
            m = re.search(rb'/Predictor\s+(\d+)', dp)
            if m and int(m.group(1)) >= 10:
                cols = int(re.search(rb'/Columns\s+(\d+)', dp).group(1))
                prev = bytearray(cols); out = bytearray()
                for r in range(0, len(data), cols + 1):
                    ft = data[r]; row = bytearray(data[r+1:r+1+cols])
                    if ft == 2:
                        for j in range(cols): row[j] = (row[j] + prev[j]) & 255
                    elif ft == 1:
                        for j in range(1, cols): row[j] = (row[j] + row[j-1]) & 255
                    out += row; prev = row
                return bytes(out)
            return data
        return raw

    def get(self, num):
        """-> (словарь или байты, поток-или-None)"""
        e = self.xref[num]
        if e[0] == 'off':
            n, dic, raw = self.read_obj_at(e[1])
            return dic, raw
        stmnum, idx = e[1], e[2]
        if stmnum not in self._objstm:
            _, sd, sraw = self.read_obj_at(self.xref[stmnum][1])
            data = self.decode_stream(sd, sraw)
            n = int(sd[b'N']); first = int(sd[b'First'])
            hdr = [int(x) for x in re.findall(rb'\d+', data[:first])]
            self._objstm[stmnum] = (data, first, hdr[:2*n])
        data, first, hdr = self._objstm[stmnum]
        for k in range(0, len(hdr), 2):
            if hdr[k] == num:
                start = first + hdr[k+1]
                if data[start:start+2] == b'<<': return self.parse_dict(data, start)[0], None
                end = first + hdr[k+3] if k + 3 < len(hdr) else len(data)
                return data[start:end].strip(), None
        raise KeyError(num)

    def pages(self):
        root = int(self.trailer[b'Root'].split()[0])
        pages = int(self.get(root)[0][b'Pages'].split()[0])
        out = []
        def walk(n):
            dic, _ = self.get(n)
            if dic.get(b'Type') == b'/Pages':
                for r in re.findall(rb'(\d+) \d+ R', dic[b'Kids']): walk(int(r))
            else: out.append(n)
        walk(pages)
        return out
