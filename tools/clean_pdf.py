# -*- coding: utf-8 -*-
"""Убирает из PDF-чертежей шапку старой компании (логотип + строки «Україна / Тел. / e-mail / сайт») и ставит наш логотип.
Вход: data/pdf_orig/*.pdf (скачано «как есть» tools/fetch_pdf.py). Выход: site/pdf/*.pdf.
PDF пересобирается заново из достижимых объектов (старые логотип, текст шапки, Info и XMP-метаданные в файл не попадают).
Запуск: python3 tools/clean_pdf.py [имя.pdf ...]"""
import os, re, sys, zlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from pdf_min import PDF
ROOT = os.path.normpath(os.path.join(HERE, '..'))
ORIG = os.path.join(ROOT, 'data', 'pdf_orig')
OUT = os.path.join(ROOT, 'site', 'pdf')
LOGO = open(os.path.join(ROOT, 'data', 'logo_211.jpg'), 'rb').read()
LW, LH = 1132, 522
BAD = [b'slavsep', b'sep.ho', b'761 20', b'761-20', 'Славен'.encode('utf-8'), b'Slaven']
NUM = rb'[\d.\-]+'

def ser(dic):
    return b'<<' + b''.join(b'/' + k + b' ' + v + b'\n' for k, v in dic.items()) + b'>>'

def strip_header(s):
    """-> (новый поток, что удалено)"""
    removed = []
    # картинки в верхней части страницы (логотип): убираем оператор Do, если перед ним cm с y >= 700
    def img(m):
        if float(m.group(6)) >= 700: removed.append('img ' + m.group(7).decode()); return b''
        return m.group(0)
    s = re.sub(rb'(?:(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+cm\s*/(Im\d+)\s+Do)',
               lambda m: img(m) if False else _img(m, removed), s)
    # строки контактов: после Tm с x>=480, y>=735 — все строки текста до следующего Tm
    out = []; pos = 0
    for m in re.finditer(rb'(' + NUM + rb') (' + NUM + rb') (' + NUM + rb') (' + NUM + rb') (' + NUM + rb') (' + NUM + rb') Tm', s):
        pass
    tms = list(re.finditer(rb'(' + NUM + rb') (' + NUM + rb') (' + NUM + rb') (' + NUM + rb') (' + NUM + rb') (' + NUM + rb') Tm', s))
    res = bytearray(s); edits = []
    for i, m in enumerate(tms):
        x, y = float(m.group(5)), float(m.group(6))
        if x >= 480 and y >= 735:
            end = tms[i + 1].start() if i + 1 < len(tms) else len(s)
            seg = s[m.end():end]
            et = seg.find(b'ET'); seg_end = m.end() + (et if et >= 0 else len(seg))
            edits.append((m.end(), seg_end))
    for a, b in reversed(edits):
        seg = bytes(res[a:b])
        new = re.sub(rb'<[0-9A-Fa-f]+>\s*Tj', b'<>Tj', seg)
        new = re.sub(rb'\[(?:[^\]]*)\]\s*TJ', b'[]TJ', new)
        new = re.sub(rb'\((?:\\.|[^\\)])*\)\s*Tj', b'()Tj', new)
        if new != seg: removed.append('text'); res[a:b] = new
    return bytes(res), removed

def _img(m, removed):
    if float(m.group(6)) >= 700:
        removed.append('img ' + m.group(7).decode()); return b''
    return m.group(0)

def process(name):
    data = open(os.path.join(ORIG, name), 'rb').read()
    p = PDF(data)
    pages = p.pages()
    maxn = max(p.xref) + 1
    new_content = {}; new_page = {}
    logo_n = maxn; maxn += 1
    use_logo = False
    for pn in pages:
        dic, _ = p.get(pn)
        refs = [int(x) for x in re.findall(rb'(\d+) \d+ R', dic[b'Contents'])] if b'R' in dic[b'Contents'] else []
        stream = b'\n'.join(PDF.decode_stream(*p.get(r)) for r in refs)
        stream, rem = strip_header(stream)
        res = dic[b'Resources']
        if re.fullmatch(rb'\d+ \d+ R', res.strip()): res = ser(p.get(int(res.split()[0]))[0])
        if rem:
            use_logo = True
            stream += b'\nq %.2f 0 0 %.2f 47 733 cm /ImNewLogo Do Q\n' % (130.0, 130.0 * LH / LW)
            m = re.search(rb'/XObject\s*<<', res); m2 = re.search(rb'/XObject\s+(\d+) \d+ R', res)
            if m: res = res[:m.end()] + b'/ImNewLogo %d 0 R' % logo_n + res[m.end():]
            elif m2:
                inner = p.get(int(m2.group(1)))[0]
                res = res[:m2.start()] + b'/XObject<<' + inner[2:-2] + b'/ImNewLogo %d 0 R>>' % logo_n + res[m2.end():]
            else: res = res[:-2] + b'/XObject<</ImNewLogo %d 0 R>>>>' % logo_n
        nc = maxn; maxn += 1
        new_content[nc] = zlib.compress(stream, 9)
        d2 = dict(dic); d2[b'Contents'] = b'%d 0 R' % nc; d2[b'Resources'] = res
        new_page[pn] = d2
    # достижимые объекты
    root = int(p.trailer[b'Root'].split()[0])
    rd, _ = p.get(root); rd = dict(rd); rd.pop(b'Metadata', None)
    objs = {}; todo = [root]; override = {root: (rd, None)}
    for pn, d2 in new_page.items(): override[pn] = (d2, None)
    seen = set()
    while todo:
        n = todo.pop()
        if n in seen or n in new_content or n == logo_n: continue
        seen.add(n)
        d, raw = override[n] if n in override else p.get(n)
        objs[n] = (d, raw)
        blob = ser(d) if isinstance(d, dict) else d
        for r in re.findall(rb'(\d+) 0 R', blob):
            todo.append(int(r))
    out = bytearray(b'%PDF-1.5\n%\xe2\xe3\xcf\xd3\n'); offs = {}
    def put(n, d, raw):
        offs[n] = len(out)
        out.extend(b'%d 0 obj\n' % n)
        if isinstance(d, dict):
            d = dict(d)
            if raw is not None: d[b'Length'] = b'%d' % len(raw)
            out.extend(ser(d))
        else: out.extend(d)
        if raw is not None: out.extend(b'\nstream\n' + raw + b'\nendstream')
        out.extend(b'\nendobj\n')
    for n in sorted(objs):
        d, raw = objs[n]
        put(n, d, raw)
    for n, c in new_content.items(): put(n, {b'Filter': b'/FlateDecode'}, c)
    if use_logo:
        put(logo_n, {b'Type': b'/XObject', b'Subtype': b'/Image', b'Width': b'%d' % LW, b'Height': b'%d' % LH,
                     b'ColorSpace': b'/DeviceRGB', b'BitsPerComponent': b'8', b'Filter': b'/DCTDecode'}, LOGO)
    size = max(offs) + 1
    xr = len(out)
    out.extend(b'xref\n0 %d\n' % size)
    for n in range(size):
        out.extend(b'%010d 00000 n \n' % offs[n] if n in offs else (b'0000000000 65535 f \n' if n == 0 else b'0000000000 00000 f \n'))
    out.extend(b'trailer\n<</Size %d/Root %d 0 R>>\nstartxref\n%d\n%%%%EOF\n' % (size, root, xr))
    return bytes(out), use_logo

def verify(out, name):
    p = PDF(out); assert p.pages()
    blob = out
    for n in p.xref:
        try:
            d, raw = p.get(n)
            if raw is not None:
                try: blob += PDF.decode_stream(d, raw)
                except Exception: pass
        except Exception: pass
    return [b.decode('utf-8', 'ignore') for b in BAD if b in blob]

if __name__ == '__main__':
    names = sys.argv[1:] or sorted(f for f in os.listdir(ORIG) if f.lower().endswith('.pdf'))
    ok = bad = 0
    for nm in names:
        try:
            out, logo = process(nm)
            left = verify(out, nm)
            if not out.startswith(b'%PDF') or left or not logo:
                print('WARN', nm, 'логотип' if not logo else '', 'остатки:' + ','.join(left) if left else '')
            open(os.path.join(OUT, nm), 'wb').write(out); ok += 1
        except Exception as e:
            print('ERR ', nm, repr(e)); bad += 1
    print(f'готово: обработано {ok}, ошибок {bad}')
