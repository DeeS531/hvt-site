# -*- coding: utf-8 -*-
"""Переводы страниц продукции: site/*.html (русские) -> site/ua/*.html, site/en/*.html.
Тексты и атрибуты разбиваются на шаблоны: обозначения моделей/числа заменяются на {0},{1}… (не переводятся), остальное переводится
по словарям tools/tr/ua.json и tools/tr/en.json (ключ — русский шаблон).
  python3 tools/i18n_build.py extract   -> tools/tr/templates.json (что нужно перевести), tools/tr/todo_*.json (чего не хватает)
  python3 tools/i18n_build.py build     -> собрать site/ua и site/en"""
import os, re, sys, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
TR = os.path.join(HERE, 'tr')
SKIP = {'index.html', 'form.html'}          # главная и форма переводятся через js/i18n.js
CYR = re.compile(r'[А-Яа-яЁё]')
W = r'(?:[^\s,;:()«»]|(?<=\d),(?=\d))'
ATOM = rf'(?:{W}*\d{W}*|[А-ЯA-ZЁ]{{2,}}{W}*)'
TOKEN = re.compile(rf'(?<![\w{{]){ATOM}(?:\s{ATOM})*')
def templ(text):
    params = []
    def rep(m):
        t = m.group(0); tail = ''
        if re.search(r'УХЛ\d[а-я]$', t): t, tail = t[:-1], t[-1]          # «УХЛ1с изолирующим» — буква приклеена к обозначению
        params.append(t); return '{%d}' % (len(params) - 1) + tail
    return TOKEN.sub(rep, text), params
UNITS = {'кВ', 'кА', 'кН', 'мм', 'кг', 'А', 'мкСм', 'мкс', 'мА', 'Ом', 'м', 'кДж/кВ', 'пКл', 'кН·м', 'кВА'}
def translatable(sk):
    r = re.sub(r'\{\d+\}', ' ', sk)
    return bool(re.search(r'[А-Яа-яЁёІіЇїЄє]{2,}', r)) or any(w in UNITS for w in re.findall(r'[А-Яа-яЁёA-Za-z/·]+', r))
WORDMAP = {
 'en': [('и аналогичные написания', 'and similar spellings'), ('Изолятор опорный', 'Post insulator'), ('Ізолятор опорний', 'Post insulator'), ('Разядник', 'Arrester'), ('Разрядник', 'Arrester'), ('Ізолятор Полімерний', 'Polymer insulator'), ('Изолятор полимерный', 'Polymer insulator')],
 'ua': [('и аналогичные написания', 'та аналогічні написання'), ('Изолятор опорный', 'Ізолятор опорний'), ('Разядник', 'Розрядник'), ('Разрядник', 'Розрядник'), ('Изолятор полимерный', 'Ізолятор полімерний'), ('Изолятор', 'Ізолятор')],
}
def wordmap(t, lang):
    for a, b in WORDMAP[lang]: t = t.replace(a, b)
    return t
def fill(tr, params, lat=False):
    for i, p in enumerate(params): tr = tr.replace('{%d}' % i, translit(p) if lat else p)
    return tr
_TL = {'А':'A','Б':'B','В':'V','Г':'G','Ґ':'G','Д':'D','Е':'E','Є':'YE','Ж':'ZH','З':'Z','И':'I','І':'I','Ї':'YI','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'KH','Ц':'C','Ч':'CH','Ш':'SH','Щ':'SHCH','Ы':'Y','Э':'E','Ю':'YU','Я':'YA','Ь':'','Ъ':'','Ё':'YO'}
def translit(t):
    """Кириллические обозначения моделей -> латиница (как в адресах страниц старого сайта: OSK, LKC, OPN, PPC, SHOP, UKHL)"""
    t = t.replace('°С', '°C')
    out = []
    for ch in t:
        up = ch.upper()
        if up in _TL:
            lat = _TL[up]
            out.append(lat if ch.isupper() else lat.lower())
        else: out.append(ch)
    return ''.join(out)
def load(lang):
    p = os.path.join(TR, f'{lang}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}

SEG = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->)|(<[^>]+>)|([^<]+)', re.S)
ATTR = re.compile(r'\b(alt|title|aria-label|placeholder)="([^"]*)"')
META = re.compile(r'(<meta name="(?:description|keywords)" content=")([^"]*)(")')
TITLE = re.compile(r'(<title>)(.*?)(</title>)', re.S)

def tr_text(raw, dic, lang, miss, attr=False):
    """raw — текст как в HTML (с сущностями)."""
    s = html.unescape(raw); lead = re.match(r'\s*', s).group(0); trail = re.search(r'\s*$', s).group(0)
    core = re.sub(r'\s+', ' ', s).strip()
    if not core or not CYR.search(core): return raw
    sk, params = templ(core)
    if not translatable(sk):
        if lang == 'en':
            o = translit(core)
            return html.escape(o, quote=attr) if attr else lead + html.escape(o, quote=False) + trail
        return raw
    t = dic.get(sk)
    if t is None:
        miss.setdefault(sk, core); return raw
    out = fill(t, params, lang == 'en')
    if t == sk: out = wordmap(out, 'en' if lang == 'en' else 'ua')
    if lang == 'en' and CYR.search(out): out = translit(out)
    esc = html.escape(out, quote=attr)
    return (lead if not attr else '') + esc + (trail if not attr else '')

def convert_page(src, dic, lang, pages, miss):
    folder = {'uk': 'ua', 'en': 'en'}[lang]
    def fix_url(u):
        if re.match(r'^(https?:|mailto:|tel:|#|data:|javascript:)', u) or not u: return u
        path, _, frag = u.partition('#')
        if path in pages: return u
        return '../' + u
    src = src.replace('ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ', {'uk': 'ТЕХНОЛОГІЇ ВИСОКОЇ НАПРУГИ', 'en': 'HIGH VOLTAGE TECHNOLOGIES'}[lang])
    src = src.replace('alt="Логотип ТВН"', {'uk': 'alt="Логотип ТВН"', 'en': 'alt="HVT logo"'}[lang])
    out = []
    for m in SEG.finditer(src):
        if m.group(1):
            blk = m.group(1)
            if blk.startswith('<script'): blk = re.sub(r'\bsrc="([^"]*)"', lambda a: f'src="{fix_url(a.group(1))}"', blk, count=1)
            out.append(blk)
        elif m.group(2):
            tag = m.group(2)
            tag = ATTR.sub(lambda a: f'{a.group(1)}="{tr_text(a.group(2), dic, lang, miss, True)}"', tag)
            tag = re.sub(r'\b(href|src|data-bs-target)="([^"]*)"', lambda a: a.group(0) if a.group(1) == 'data-bs-target' else f'{a.group(1)}="{fix_url(a.group(2))}"', tag)
            out.append(tag)
        else: out.append(tr_text(m.group(3), dic, lang, miss))
    res = ''.join(out)
    res = META.sub(lambda m: m.group(1) + tr_text(m.group(2), dic, lang, miss, True) + m.group(3), res)
    res = res.replace('ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ', {'uk': 'ТЕХНОЛОГІЇ ВИСОКОЇ НАПРУГИ', 'en': 'HIGH VOLTAGE TECHNOLOGIES'}[lang])
    res = res.replace('alt="Логотип ТВН"', {'uk': 'alt="Логотип ТВН"', 'en': 'alt="HVT logo"'}[lang])
    res = res.replace('<html lang="ru">', f'<html lang="{lang}" data-page-lang="{lang}">', 1)
    return res

def pages_list(): return sorted(f for f in os.listdir(SITE) if f.endswith('.html') and f not in SKIP)

def run(mode):
    pages = set(pages_list()); allmiss = {}
    stats = {}
    for lang, folder in (('uk', 'ua'), ('en', 'en')):
        dic = load(folder); miss = {}
        if mode == 'build': os.makedirs(os.path.join(SITE, folder), exist_ok=True)
        for f in sorted(pages):
            src = open(os.path.join(SITE, f), encoding='utf-8').read()
            res = convert_page(src, dic, lang, pages, miss)
            if mode == 'build': open(os.path.join(SITE, folder, f), 'w', encoding='utf-8').write(res)
        allmiss[folder] = miss; stats[folder] = (len(dic), len(miss))
    return allmiss, stats

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'extract'
    miss, st = run('extract' if mode == 'extract' else 'build')
    if mode == 'extract':
        os.makedirs(TR, exist_ok=True)
        ex = {}
        for folder in miss:
            for k, v in miss[folder].items(): ex.setdefault(k, v)
        # все шаблоны (в т.ч. уже переведённые) — берём по русским страницам без словаря
        miss0, _ = (lambda: ({}, None))()
        json.dump(ex, open(os.path.join(TR, 'todo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print('нужно перевести шаблонов:', len(ex))
    else:
        for folder, (d, m) in st.items(): print(f'{folder}: в словаре {d}, не хватает {m}')
        for folder in miss:
            if miss[folder]:
                json.dump(miss[folder], open(os.path.join(TR, f'missing_{folder}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
