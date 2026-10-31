# -*- coding: utf-8 -*-
"""Группа 7 — шинные опоры ШОП/ШО: data/shop_raw.tar.gz -> tools/shop_data.py (+ нестыковки: -q)."""
import os, re, sys, tarfile, pprint
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import opn_parse as P
RAW = {}
with tarfile.open(os.path.join(HERE, '..', 'data', 'shop_raw.tar.gz')) as t:
    for m in t.getmembers():
        if m.isfile() and m.name.endswith('.html'): RAW[os.path.basename(m.name)] = t.extractfile(m).read().decode('utf-8-sig')
Q = []
def quirk(w, t): Q.append((w, t))
def one(t): return re.sub(r'\s*\n\s*', ' ', t).strip()
def bl(k): return P.cut_footer(P.parse(RAW[k]))
def clean_name(t):
    t = re.sub(r'\s*цена от.*$', '', one(t))
    t = re.sub(r'^Шинная опора( подвесного исполнения)?\s+', '', t)
    return t.strip()
SPECL = ('Класс напряжения сети', 'Испытательное напряжение', 'Район эксплуатации', 'Длина пути утечки', 'Минимальная разрушающая сила', 'Тип зажимаемого провода', 'Код УКТ ВЭД')
def spec_of(ps):
    out = []
    for i, t in enumerate(ps[:-1]):
        t1 = one(t)
        if t1.startswith(SPECL):
            out.append((t1.rstrip(':').strip(), one(ps[i + 1])))
    return out

def parse_sub(key):
    b = bl(key); ps = [x[1] for x in b if x[0] == 'p']
    d = {'title': one(ps[0]), 'spec': spec_of(ps), 'models': None, 'paras': [], 'wires': None, 'legend': [], 'variants': None, 'table': None, 'table_title': None, 'notes': [], 'images': [], 'drawing': None}
    seen_table = False
    for x in b:
        if x[0] == 'img' and 'slide' not in x[1]:
            n = os.path.basename(x[1])
            if seen_table: d['drawing'] = n
            elif n not in d['images']: d['images'].append(n)
        if x[0] == 'table' and not seen_table:
            g = x[1]; d['table'] = [[c['t'] for c in r] for r in g]; seen_table = True
    for i, t in enumerate(ps):
        f = one(t)
        if f.startswith('Шинные опоры ШОП') and 'с полимерной изоляцией' in f and not d['models']: d['models'] = f
        if f.startswith('Тип провода:'): d['wires'] = f[len('Тип провода:'):].strip()
        if f.startswith('Возможные варианты обозначения'): d['variants'] = re.sub(r'^[^:]*:\s*', '', f)
        if f.startswith('В условном обозначении шинных опор'):
            for u in ps[i + 1:]:
                if one(u).startswith('Комплект поставки'): break
                if ' — ' in one(u) or ' - ' in one(u): d['legend'].append(one(u).rstrip(';. '))
        if re.match(r'Шинные опоры .* (предназначены|применяются)', f) and 'преимущества' not in f: d['paras'].append(f)
        if f.startswith('По требованию заказчика'): d['notes'].append(f)
        if re.match(r'^ШОП-\d+', f) and d['table'] and not d['table_title'] and len(f) < 40: d['table_title'] = f
    return d

def parse_voltage(kv):
    key = f'ru_shinnyye-opory-{kv}-kV.html'
    b = bl(key); ps = [x for x in b if x[0] == 'p']
    pg = {'kv': kv, 'title': one(ps[0][1]), 'spec': spec_of([x[1] for x in ps]), 'legend': [], 'groups': [], 'src': key[3:]}
    allp = [x[1] for x in ps]
    for i, t in enumerate(allp):
        if one(t).startswith('В условном обозначении шинных опор'):
            for u in allp[i + 1:]:
                if one(u).startswith(('Шинные опоры ШОП-', 'Шинная')): break
                if ' — ' in one(u) or ' - ' in one(u): pg['legend'].append(one(u).rstrip(';. '))
    cur = None; img = None
    for x in b:
        if x[0] == 'img': img = os.path.basename(x[1])
        if x[0] != 'p': continue
        f = one(x[1])
        m = re.match(r'Шинные опоры ШОП-\d+\.([IV]+) УХЛ1\s*$', f)
        if m: cur = {'sza': m.group(1), 'heading': f, 'count_declared': None, 'items': []}; pg['groups'].append(cur); continue
        m = re.match(r'(\d+) исполн', f)
        if m and cur: cur['count_declared'] = int(m.group(1)); continue
        if cur and f.startswith('Шинная опора') and 'цена' in f and len(x) > 2 and x[2]:
            slug = x[2][0]
            cur['items'].append({'name': clean_name(f), 'img': img, 'sub': slug, 'desc': None})
        elif cur and cur['items'] and cur['items'][-1]['desc'] is None and len(x) > 2 and x[2] and 'Описание и характеристики' in f:
            cur['items'][-1]['desc'] = f.split('. Шинная опора')[0].rstrip('.')
    for g in pg['groups']:
        if g['count_declared'] and g['count_declared'] != len(g['items']):
            quirk(f'shop{kv}', f'в заголовке группы «{g["heading"]}» указано {g["count_declared"]} исполнений, а на странице их {len(g["items"])}')
    return pg

PAGES = []
for kv in ('10', '35', '110', '150'):
    PAGES.append(parse_voltage(kv))
SUBS = {}
for pg in PAGES:
    for g in pg['groups']:
        for it in g['items']:
            SUBS[it['sub']] = parse_sub('ru_' + it['sub'])
# проверки: СЗА страницы vs СЗА исполнения; число проводов; ссылки с разным регистром
for pg in PAGES:
    for g in pg['groups']:
        for it in g['items']:
            s = SUBS[it['sub']]
            za = next((v for l, v in s['spec'] if l.startswith('Район')), None)
            if za and g['sza'] not in re.split(r'[,\s]+', za):
                quirk(it['name'], f'исполнение в группе СЗА {g["sza"]}, а на странице указан СЗА «{za}»')
            if re.search(r'[a-z]I[a-z]', it['sub']) or 'iIi' in it['sub']:
                pass
mixed = sorted({it['sub'] for pg in PAGES for g in pg['groups'] for it in g['items'] if 'iIi' in it['sub']})
quirk('shop', f'на старом сайте {len(mixed)} ссылок вида «…-iIi-…» (смешанный регистр в адресе страницы); на новом сайте не имеет значения')
quirk('shop20/220/330', 'страницы шинных опор 20, 220 и 330 кВ в меню/каталоге старого сайта есть, но дают 404 (данных нет) — на новом сайте страницы «по запросу»')
quirk('shop', 'с сайта не перенесены цены (например «цена от 3900,00грн», 12500, 13100, 15500 грн), SEO-блоки «преимущества» (в т.ч. про «боевые действия») и «купить»-тексты')
quirk('shop', 'все 80 картинок шинных опор (рендеры и чертежи) содержали водяные знаки старого сайта — обработаны tools/unwatermark.js (SHOP_PHOTO=1 WHITE=205), на рендерах возможны едва заметные следы')
# страница группы
gb = P.cut_footer(P.parse(RAW['ru_shinnyye-opory.html'], True)); gp = [one(x[1]) for x in gb if x[0] == 'p']
GROUP = {'title': gp[0], 'paras': gp[1:4], 'cards': []}
for x in gb:
    if x[0] == 'p' and re.match(r'^Шинные опоры ШОП-\d+ УХЛ1, ШО-\d+ УХЛ1$', one(x[1])):
        GROUP['cards'].append({'name': one(x[1]), 'kv': re.search(r'ШОП-(\d+)', x[1]).group(1)})
for i, t in enumerate(gp):
    for c in GROUP['cards']:
        if t == c['name'] and i + 1 < len(gp) and not gp[i + 1].startswith(('Подробнее', 'Купить')): c['text'] = gp[i + 1]
with open(os.path.join(HERE, 'shop_data.py'), 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n# СГЕНЕРИРОВАНО tools/extract_shop.py (группа 7: шинные опоры)\n\nGROUP = ' + pprint.pformat(GROUP, width=150, sort_dicts=False) + '\n\nPAGES = ' + pprint.pformat(PAGES, width=150, sort_dicts=False) + '\n\nSUBS = ' + pprint.pformat(SUBS, width=150, sort_dicts=False) + '\n\nQUIRKS = ' + pprint.pformat(Q, width=150) + '\n')
print('записано; страниц', len(PAGES), '| исполнений', sum(len(g['items']) for p in PAGES for g in p['groups']), '| нестыковок', len(Q))
if '-q' in sys.argv:
    for w, t in Q: print(f'  [{w}] {t}')
