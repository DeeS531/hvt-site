# -*- coding: utf-8 -*-
"""Разбор сохранённых страниц старого сайта (группа 3, ОПН) в блоки.
Исходные HTML лежат в data/opn_raw.tar.gz (имена: ru_*.html / ua_*.html, подстраницы: ru_sub_*, ua_sub_*).
Блок: ('p', текст) | ('table', [[ячейка,...],...]) | ('img', src, alt) ; ячейка = {'t': текст с \\n, 'a': [href,...]}"""
import re, tarfile, os
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'data', 'opn_raw.tar.gz')

def load_raw():
    out = {}
    with tarfile.open(RAW) as t:
        for m in t.getmembers():
            if m.isfile():
                out[os.path.basename(m.name)] = t.extractfile(m).read().decode('utf-8-sig')
    return out

def norm(s):
    s = s.replace('\xa0', ' ')
    s = re.sub(r'[ \t\r]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)
    return s.strip()

class P(HTMLParser):
    def __init__(s, alt=False):
        super().__init__(convert_charrefs=True); s.alt = alt
        s.blocks = []; s.skip = 0; s.buf = []; s.in_content = False; s.links = []; s.open_a = None
        s.tables = []   # стек таблиц: {'rows':[], 'row':None, 'cell':None}
    # --- текстовый буфер текущего «абзаца»
    def flush(s):
        t = norm(''.join(s.buf)); s.buf = []
        lk = s.links; s.links = []
        if t and s.in_content and not s.tables: s.blocks.append(('p', t, lk))
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag in ('script', 'style'): s.skip += 1; return
        if s.skip: return
        if tag == 'a' and 'carousel-control' in (a.get('class') or '') and 'right' in (a.get('class') or ''):
            s.in_content = True; return
        if tag == 'div' and ('opn-hero' in (a.get('class') or '') or (s.alt and 'col-md-9' in (a.get('class') or ''))) and not s.in_content:
            s.in_content = True
        if not s.in_content: return
        if tag == 'table':
            s.flush(); s.tables.append({'rows': [], 'row': None, 'cell': None}); return
        if s.tables:
            T = s.tables[-1]
            if tag == 'tr': T['row'] = []; return
            if tag in ('td', 'th'):
                T['cell'] = {'buf': [], 'a': [], 'rs': int(a.get('rowspan', 1) or 1), 'cs': int(a.get('colspan', 1) or 1)}; return
            if T['cell'] is not None:
                if tag in ('br', 'p', 'div', 'li'): T['cell']['buf'].append('\n')
                if tag == 'a' and a.get('href'): T['cell']['a'].append(a['href'])
                if tag == 'img' and a.get('src'): T['cell']['a'].append('IMG:' + a['src'])
            return
        if tag in ('p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol'): s.flush()
        if tag == 'img' and a.get('src'): s.flush(); s.blocks.append(('img', a['src'], a.get('alt', ''), s.open_a))
        if tag == 'a' and a.get('href') and not a['href'].startswith('#'):
            s.open_a = a['href']; s.links.append(a['href'])
    def handle_endtag(s, tag):
        if tag in ('script', 'style'): s.skip -= 1; return
        if s.skip or not s.in_content: return
        if s.tables:
            T = s.tables[-1]
            if tag in ('td', 'th') and T['cell'] is not None:
                c = T['cell']; T['cell'] = None
                T['row'].append({'t': norm(''.join(c['buf'])), 'a': c['a'], 'rs': c['rs'], 'cs': c['cs']})
            elif tag == 'tr' and T['row'] is not None:
                T['rows'].append(T['row']); T['row'] = None
            elif tag == 'table':
                s.tables.pop()
                grid = expand(T['rows'])
                if s.tables:   # вложенная таблица: вливаем текстом в ячейку родителя
                    par = s.tables[-1]
                    if par['cell'] is not None:
                        par['cell']['buf'].append('\n'.join(' | '.join(c['t'] for c in r) for r in grid))
                else:
                    s.blocks.append(('table', grid))
            return
        if tag == 'a': s.open_a = None
        if tag in ('p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol'): s.flush()
    def handle_data(s, d):
        if s.skip or not s.in_content: return
        if s.tables:
            T = s.tables[-1]
            if T['cell'] is not None: T['cell']['buf'].append(d)
        else: s.buf.append(d)

def expand(rows):
    """раскрывает rowspan/colspan в прямоугольную сетку"""
    grid = []; pend = {}
    for r in rows:
        out = []; col = 0; cells = list(r)
        while cells or any(k >= col for k in pend):
            if col in pend:
                cell, left = pend[col]; out.append(cell)
                if left > 1: pend[col] = (cell, left - 1)
                else: del pend[col]
                col += 1; continue
            if not cells: break
            c = cells.pop(0)
            for k in range(c['cs']):
                cc = {'t': c['t'], 'a': c['a']}
                out.append(cc)
                if c['rs'] > 1: pend[col] = (cc, c['rs'] - 1)
                col += 1
        grid.append(out)
    return grid

def parse(html, alt=False):
    p = P(alt); p.feed(html); p.flush(); return p.blocks

def cut_footer(blocks):
    """обрезает всё с блока «Контакты» (подвал старого сайта)"""
    out = []
    for b in blocks:
        if b[0] == 'p' and b[1].startswith('Контакты'): break
        out.append(b)
    return out
