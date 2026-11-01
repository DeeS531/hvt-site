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
# контакты справа от логотипа (шрифт Helvetica без встраивания, ширины символов — по AFM)
PHONE = '+380 50 947 35 49'; EMAIL = 'highvoltagetechnologies.ua@gmail.com'
_W = dict(zip(range(32, 127), [278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278] + [556]*10 + [278,278,584,584,584,556,1015] +
    [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611] + [278,278,278,469,556,333] +
    [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,500,333,500,278,556,500,722,500,500,500] + [334,260,334,584]))
def tw(t, size): return sum(_W[ord(c)] for c in t) * size / 1000.0
def contacts_ops(right=548.0):
    ops = b'q 0.07 0.16 0.29 rg BT '
    for txt, y in ((PHONE, 772.0), (EMAIL, 756.0)):
        ops += b'/FHvt 10 Tf 1 0 0 1 %.2f %.2f Tm (%s) Tj ' % (right - tw(txt, 10), y, txt.encode())
    return ops + b'ET Q\n'

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
    font_n = maxn; maxn += 1
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
            stream += b'\nq %.2f 0 0 %.2f 47 733 cm /ImNewLogo Do Q\n' % (130.0, 130.0 * LH / LW) + contacts_ops()
            m = re.search(rb'/XObject\s*<<', res); m2 = re.search(rb'/XObject\s+(\d+) \d+ R', res)
            if m: res = res[:m.end()] + b'/ImNewLogo %d 0 R' % logo_n + res[m.end():]
            elif m2:
                inner = p.get(int(m2.group(1)))[0]
                res = res[:m2.start()] + b'/XObject<<' + inner[2:-2] + b'/ImNewLogo %d 0 R>>' % logo_n + res[m2.end():]
            else: res = res[:-2] + b'/XObject<</ImNewLogo %d 0 R>>>>' % logo_n
            mf = re.search(rb'/Font\s*<<', res); mf2 = re.search(rb'/Font\s+(\d+) \d+ R', res)
            if mf: res = res[:mf.end()] + b'/FHvt %d 0 R' % font_n + res[mf.end():]
            elif mf2:
                inner = p.get(int(mf2.group(1)))[0]
                res = res[:mf2.start()] + b'/Font<<' + inner[2:-2] + b'/FHvt %d 0 R>>' % font_n + res[mf2.end():]
            else: res = res[:-2] + b'/Font<</FHvt %d 0 R>>>>' % font_n
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
        if n in seen or n in new_content or n in (logo_n, font_n): continue
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
    if use_logo:
        put(font_n, {b'Type': b'/Font', b'Subtype': b'/Type1', b'BaseFont': b'/Helvetica', b'Encoding': b'/WinAnsiEncoding'}, None)
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
