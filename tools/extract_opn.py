# -*- coding: utf-8 -*-
"""Группа 3 (ОПН + регистраторы JCQF): разбор сохранённых страниц sep.ho.ua -> tools/opn_data.py.
Запуск: python3 tools/extract_opn.py   (читает data/opn_raw.tar.gz, пишет tools/opn_data.py и список нестыковок).
Ничего не округляет и не домысливает; расхождения исходника складываются в QUIRKS."""
import os, re, sys, pprint
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import opn_parse as P

RAW = P.load_raw()
QUIRKS = []          # (страница/модель, текст)
def quirk(where, text): QUIRKS.append((where, text))

# ---------- подписи строк (единые, по-русски) ----------
LBL = [
 (r'^Клас+ напр',              'Класс напряжения сети'),
 (r'^(Найбільша|Наибольшее)',                       'Наибольшее длительно допустимое рабочее напряжение Uнр (действующее значение)'),
 (r'^(Номінальна напруга|Номинальное напряжение)',  'Номинальное напряжение ограничителя'),
 (r'^(Номінальний розрядний|Номинальный разрядный)', 'Номинальный разрядный ток с формой волны 8/20 мкс (амплитудное значение)'),
 (r'^(Імпульс|Импульс)',                            'Импульс большого выдерживаемого тока 4/10 мкс'),
 (r'^(Пропускна|Пропускная)',                       'Пропускная способность ограничителя (амплитуда прямоугольного импульса 2000 мкс)'),
 (r'^(Залишкова напруга при дії|Остающееся напряжение при действии)', 'Остающееся напряжение при действии номинального разрядного тока с формой волны 8/20 мкс с амплитудой, не более:'),
 (r'^(Залишкова напруга при струмі|Остающееся напряжение при токе)',  'Остающееся напряжение при токе коммутационных перенапряжений на волне 30/60 мкс с амплитудой, не более:'),
 (r'^(Залишкова напруга при імпульсі|Остающееся напряжение при импульсе)', 'Остающееся напряжение при импульсе тока с крутым фронтом 1/10 мкс с амплитудой 10000 А, не более:'),
 (r'^(Довжина|Длина)',                              'Длина пути утечки, не менее'),
 (r'^(Удільна|Удельная)',                           'Удельная энергоёмкость ограничителя, не менее'),
 (r'^(Клас розр|Класс разр)',                       'Класс разряда линии'),
 (r'^(Маса|Масса)',                                 'Масса ограничителя, не более'),
 (r'^(Класифікаційна|Классификационное)',           'Классификационное напряжение ограничителя при активной составляющей переменного тока 1 мА ампл. (действующее значение), не менее'),
]
def canon_label(raw_label):
    t = re.sub(r'^\d+\s+', '', raw_label.strip())
    first = t.split('\n')[0]
    for rx, ru in LBL:
        if re.match(rx, re.sub(r'\s+', ' ', first)):
            subs = [l.strip() for l in t.split('\n')[1:] if l.strip() and l.strip().startswith(('–', '-'))]
            return ru + (('\n' + '\n'.join(subs)) if subs else '')
    raise ValueError('неизвестная подпись: ' + raw_label)

UNIT = {'Класс напряжения': 'кВ', 'Наибольшее': 'кВ', 'Номинальное напряжение': 'кВ', 'Номинальный разрядный': 'А', 'Импульс': 'кА',
        'Пропускная': 'А', 'Остающееся': 'кВ', 'Длина': 'мм', 'Удельная': 'кДж/кВ', 'Масса': 'кг', 'Классификационное': 'кВ'}
def unit_of(label, unit):
    if unit.strip(): return unit.strip()
    for k, u in UNIT.items():
        if label.startswith(k): return u
    return ''

def fnum(s):
    m = re.search(r'\d+(?:[.,]\d+)?', s or '')
    return float(m.group(0).replace(',', '.')) if m else None

# ---------- имя модели -> параметры ----------
def parse_name(name):
    m = re.search(r'ОПН[^\d]*?(\d+(?:,\d+)?)/(\d+(?:[.,]\d+)?)/(\d+)/(\d+)(?:/IV)?', name)
    if not m: return None
    kv, unr, i, g4 = m.groups()
    cap = int(g4)
    if cap in (1, 2) and '/IV' in name: cap = {1: 400, 2: 550}[cap]
    return {'kv': kv, 'unr': unr.replace('.', ','), 'I': i, 'cap': cap}

# ---------- подстраницы ----------
def spec_table(blocks):
    for x in blocks:
        if x[0] == 'table':
            g = x[1]
            if len(g[0]) == 3 and 'арактеристик' in g[0][0]['t']:
                return [(canon_label(r[0]['t']), unit_of(canon_label(r[0]['t']), r[1]['t']), r[2]['t']) for r in g[1:]], g[0][2]['t'].replace('\n', ' ')
            if len(g[0]) == 2 and 'араметр' in g[0][0]['t']:
                return [(canon_label(r[0]['t']), unit_of(canon_label(r[0]['t']), ''), r[1]['t']) for r in g[1:]], g[0][1]['t']
    return None, None

def variants_of(blocks):
    """(варианты обозначения, взаимозаменяемость, примечания)"""
    var = None; inter = None; notes = []
    for x in blocks:
        if x[0] != 'p': continue
        for line in x[1].split('\n'):
            pass
        t = x[1]
        flat = re.sub(r'\s*\n\s*', ' ', t)
        m = re.search(r'(Варианты обозначения[^:]*|Варіанти позначення[^:]*):\s*(.+)$', flat)
        if m and var is None:
            var = re.split(r'\s*(?:Купити ОПН|Купить ОПН)', m.group(2))[0].strip().rstrip('.')
        m = re.search(r'є взаємозамінними з (.+)$', flat)
        if m: inter = m.group(1).strip().rstrip('.')
        if re.search(r'комплектоваться регистратором|укомплектованы регистратором', flat): notes.append(flat)
    return var, inter, notes

DRAW = lambda n: n   # фильтр картинок ниже

WM = {  # фото с «вшитыми» водяными знаками старого сайта: в модельные карточки не берём; обработанные копии — tools/unwatermark.js -> images/opn/photo
 'OPN10.png','OPN10schem.PNG','OPN10version2.PNG','OPN10version3.PNG','OPN10version4.PNG','OPN6.png',
 'OPN35.png','OPN35-02.png','OPN35-04.png','OPN-35-1.png','OPN-35-2.png','OPN-35-3.png','OPN-35-4.png',
 'OPN35_4.png','opnp-6-IV.jpg','OPN3_4.png','OPN6_4.png','OPN10_4.png','OPN20_4.png'}
SKIP_IMG = re.compile(r'(slideshow|logo)')

def images_of(blocks):
    out = []
    for x in blocks:
        if x[0] == 'img' and not SKIP_IMG.search(x[1]):
            b = os.path.basename(x[1])
            if b not in WM and b not in out: out.append(b)
    for x in blocks:   # картинки внутри таблиц
        if x[0] == 'table':
            for r in x[1]:
                for c in r:
                    for a in c['a']:
                        if a.startswith('IMG:'):
                            b = os.path.basename(a[4:])
                            if b not in WM and b not in out: out.append(b)
    return out

def load_sub(key):
    html = RAW[key]
    bl = P.cut_footer(P.parse(html))
    spec, hdr = spec_table(bl)
    var, inter, notes = variants_of(bl)
    return {'file': key, 'spec': spec, 'hdr': hdr, 'var': var, 'inter': inter, 'notes': notes,
            'images': images_of(bl), 'blocks': bl}

SUBS = {}
for k in sorted(RAW):
    if re.match(r'(ru|ua)_(OPN_|opn-p|opnp)', k): SUBS[k] = load_sub(k)

def sv(sub, key):
    for l, u, v in sub['spec']:
        if l.startswith(key): return v
    return None

# ---------- категории ----------
def blocks_of(key): return P.cut_footer(P.parse(RAW[key]))
def ru_rows(key):
    out = []
    for x in blocks_of(key):
        if x[0] == 'table':
            hdr = x[1][0]
            for r in x[1][1:]:
                if r and r[0]['a'] and r[0]['a'][0].split('/')[-1].endswith('.html'):
                    out.append({'name': re.sub(r'\s+', ' ', r[0]['t'].replace('\n', ' ')).strip(), 'href': r[0]['a'][0].split('/')[-1],
                                'cells': [c['t'] for c in r]})
    return out
def ua_cards(key):
    out = []
    for x in blocks_of(key):
        if x[0] == 'p' and len(x) > 2 and x[2] and '\n' not in x[1] and re.match(r'^(ОПН|MWK|3EK)', x[1]) and x[2][0].endswith('.html'):
            out.append({'name': re.sub(r'\s+', ' ', x[1]).strip(), 'href': x[2][0].split('/')[-1]})
    return out

def ua_slug_candidates(href):
    """RU 'OPN_10_11_5_400_1.html' -> кандидаты UA-слагов того же изделия"""
    m = re.match(r'^OPN_(\d+)_([\d_]+?)_(400|550)_([12])\.html$', href)
    if not m: return []
    kv, unr, cap, v = m.groups(); u = unr.replace('_', '-')
    c = [f'opn-p-{kv}kv-{kv}-{u}-{cap}-ukhl{v}.html']
    if '-' not in u: c.append(f'opn-p-{kv}kv-{kv}-{u}-0-{cap}-ukhl{v}.html')
    return c

# ---------- сборка моделей напряжения ----------
def build_models(kv, ru_key, ua_key):
    rrows = ru_rows(ru_key) if ru_key else []
    ucards = ua_cards(ua_key) if ua_key else []
    models = {}   # ключ: UA-слаг или RU-слаг
    def sub_for(href, lang):
        for pre in (lang + '_',):
            if pre + href in SUBS: return SUBS[pre + href]
    for r in rrows:
        href = r['href']
        if href.startswith(('opn-p', 'opnp')):    # RU-таблица ссылается прямо на UA-слаг
            key = href
        else:
            cands = [c for c in ua_slug_candidates(href) if 'ua_' + c in SUBS]
            key = cands[0] if cands else href
        m = models.setdefault(key, {'key': key, 'names': [], 'ru_href': None, 'ua_href': None, 'cat_cells': None})
        m['names'].append(('ru', r['name'])); m['cat_cells'] = r['cells']
        if href.startswith('OPN_') and key != href: m['ru_href'] = href
        elif href.startswith('OPN_'): m['ru_href'] = href
        else: m['ru_href'] = href if ('ru_' + href) in SUBS else None
        if ('ua_' + key) in SUBS: m['ua_href'] = key
    for c in ucards:
        key = c['href']
        m = models.setdefault(key, {'key': key, 'names': [], 'ru_href': None, 'ua_href': None, 'cat_cells': None})
        m['names'].append(('ua', c['name']))
        if ('ua_' + key) in SUBS: m['ua_href'] = key
        if ('ru_' + key) in SUBS and not m['ru_href']: m['ru_href'] = key
    return list(models.values())

def ru_sub_of(m):
    return SUBS.get('ru_' + m['ru_href']) if m['ru_href'] else None
def ua_sub_of(m):
    return SUBS.get('ua_' + m['ua_href']) if m['ua_href'] else None

def clean_name(n):
    n = re.sub(r'\s+', ' ', n).strip()
    n = re.sub(r'(?<=\d)(УХЛ)', r' \1', n)
    n = n.replace('виконання', 'исполнение')
    return n

def finish_model(kv, m):
    rs, us = ru_sub_of(m), ua_sub_of(m)
    where = m['key']
    ours = [(l, clean_name(n)) for l, n in m['names'] if n.startswith('ОПН')]
    foreign = []
    for l, n in m['names']:
        if not n.startswith('ОПН') and n not in foreign: foreign.append(n)
    ordered = [n for l, n in ours if l == 'ru'] + [n for l, n in ours if l != 'ru']
    name = next((n for n in ordered if 'УХЛ' in n), ordered[0] if ordered else None)
    sub = rs or us
    if sub is None:
        quirk(where, 'нет подстраницы с характеристиками (ссылка из каталога ведёт на несуществующую или недоступную страницу)')
    # сравнение RU и UA характеристик одного изделия (по числам; форматирование «12»/«12,0»/«10 000» не считается расхождением)
    conflict_rows = set()
    def nums(v): return [float(x.replace(',', '.')) for x in re.findall(r'\d+(?:,\d+)?', v.replace(' ', ''))]
    if rs and us and rs['spec'] and us['spec'] and m['ru_href'] != m['ua_href']:
        a = {l: v for l, u, v in rs['spec']}; b = {l: v for l, u, v in us['spec']}
        for l in a:
            if l in b and nums(a[l]) != nums(b[l]):
                conflict_rows.add(l)
                quirk(where, f'русская ({m["ru_href"]}) и украинская ({m["ua_href"]}) страницы расходятся: «{l.split(chr(10))[0][:48]}»: {a[l]!r} против {b[l]!r}; выведено «уточняйте»')
    spec = sub['spec'] if sub else []
    hdr = sub['hdr'] if sub else None
    # параметры из имени
    p = parse_name(name or '') or {}
    unr_s = next((v for l, u, v in spec if l.startswith('Наибольшее')), None)
    cap_s = next((v for l, u, v in spec if l.startswith('Пропускная')), None)
    cls_s = next((v for l, u, v in spec if l.startswith('Класс напряжения')), None)
    flags = {}
    if p:
        if unr_s and fnum(unr_s) != fnum(p['unr']):
            quirk(where, f'в названии «{name}» Uнр = {p["unr"]} кВ, а в таблице характеристик (стр. {sub["file"][3:]}) = {unr_s} кВ; в таблице выведено «уточняйте»'); flags['unr'] = True
        if cap_s and int(fnum(cap_s)) != p['cap']:
            quirk(where, f'в названии «{name}» пропускная способность {p["cap"]} А, а в таблице характеристик (стр. {sub["file"][3:]}) = {cap_s} А; в таблице выведено «уточняйте»'); flags['cap'] = True
        if cls_s and fnum(cls_s) != fnum(p['kv']):
            quirk(where, f'в названии «{name}» класс {p["kv"]} кВ, в таблице {cls_s} кВ'); flags['cls'] = True
    # заголовок столбца таблицы и заголовок страницы
    if hdr and p and hdr != 'Значення':
        hp = parse_name(hdr + ' ')
        if hp and (fnum(hp['unr']) != fnum(p['unr']) or hp['kv'] != p['kv']):
            quirk(where, f'заголовок столбца таблицы на странице «{hdr}» не совпадает с названием «{name}» (Uнр {hp["unr"]} против {p["unr"]})')
    ASK = 'уточняйте'
    def mark(prefixes):
        nonlocal spec
        spec = [(l, u, ASK if l.startswith(prefixes) else v) for l, u, v in spec]
    if flags.get('unr'): mark(('Наибольшее', 'Номинальное напряжение'))
    if flags.get('cap'): mark(('Пропускная',))
    if conflict_rows:
        spec = [(l, u, ASK if l in conflict_rows else v) for l, u, v in spec]
    # заголовок над таблицей на самой странице («Технические характеристики ограничителя … X»)
    for s_ in (rs, us):
        if not s_: continue
        for x in s_['blocks']:
            if x[0] == 'p' and re.match(r'Технические характеристики огр|Технічні характеристики обм', x[1]):
                tp = parse_name(x[1])
                if tp and p and (fnum(tp['unr']) != fnum(p['unr']) or tp['cap'] != p['cap']) and 'хлоп' not in x[1]:
                    quirk(where, f'заголовок над таблицей на странице {s_["file"][3:]}: «{x[1][:100]}» не совпадает с названием «{name}»')
                break
    # варианты обозначений и взаимозаменяемость
    var = None
    if kv in ('6', '10') and m['cat_cells'] and len(m['cat_cells']) >= 4 and m['cat_cells'][3].strip():
        var = re.sub(r'\s*\n\s*', ' ', m['cat_cells'][3]).strip().rstrip(',')
    for s in (rs, us):
        if not var and s and s['var']: var = s['var']
    inter = (rs or {}).get('inter') or (us or {}).get('inter')
    notes = []
    for s in (rs, us):
        if s:
            for n in s['notes']:
                if n not in notes and not re.search(r'[іїєґ]', n): notes.append(n)
    # картинки: чертежи
    imgs = []
    for s in (rs, us):
        if s:
            for i in s['images']:
                if i not in imgs: imgs.append(i)
    out = {'id': re.sub(r'\.html$', '', m['key']).lower().replace('_', '-'),
           'name': name, 'kv': kv, 'unr': p.get('unr'), 'cap': p.get('cap'),
           'aliases': var, 'interchange': inter, 'spec': spec, 'flags': flags,
           'images': imgs, 'notes': notes,
           'src': [x for x in (m['ru_href'], 'UA/' + m['ua_href'] if m['ua_href'] else None) if x]}
    core = lambda n: re.sub(r'(УХЛ\d|-04|\s)', '', n)
    alt = []
    for l, n in ours:
        if n != name and core(n) != core(name) and n not in alt: alt.append(n)
    if alt: out['other_names'] = alt
    if foreign: out['foreign'] = foreign
    return out

def model_sort(m):
    u = fnum(m['unr']) if m.get('unr') else 9999
    return (u, m.get('cap') or 0, m['name'] or '')

# ---------- параграфы страницы ----------
BRAND = [  # нейтральные замены старого названия
 (r'ОПН Славэнергосистем', 'ОПН'),
]
def strip_brand(t):
    for a, b in BRAND: t = re.sub(a, b, t)
    return t

def intro_of(key, stop_at_table=True):
    out = []
    for x in blocks_of(key):
        if x[0] == 'table': break
        if x[0] == 'p':
            t = x[1].strip()
            if t and not t.startswith(('Купить ОПН', 'Українська версія', 'Технические характеристики')): out.append(strip_brand(t))
    return out

def table_rows(g):
    return [[c['t'] for c in r] for r in g]

# ---------- сборка страниц ----------
PAGES = []
UA_KEY = {'022': 'ua_opn-0-22.html', '3': 'ua_opn-3.html', '6': 'ua_opn-6.html', '10': 'ua_opn-10.html', '15': 'ua_opn-15.html',
          '20': None, '35': 'ua_opn-35.html', '110': 'ua_opn-110.html', '150': 'ua_opn-150.html', '220': 'ua_opn-220.html', '330': 'ua_opn-330.html'}
for kv, label, fname in [('022', '0,22 / 0,38 / 0,4', 'opn022'), ('3', '3', 'opn3'), ('33', '3,3', 'opn33'), ('6', '6', 'opn6'),
                         ('10', '10', 'opn10'), ('15', '15', 'opn15'), ('20', '20', 'opn20'), ('27', '27,5', 'opn27'),
                         ('35', '35', 'opn35'), ('110', '110', 'opn110'), ('150', '150', 'opn150'), ('220', '220', 'opn220'), ('330', '330', 'opn330')]:
    rk = f'ru_index-2-opnn{kv}.html'
    bl = blocks_of(rk)
    page = {'id': kv, 'label': label, 'file': fname + '.html', 'src': rk[3:]}
    if not any(x[0] == 'table' for x in bl):
        page['kind'] = 'stub'; page['intro'] = []
        PAGES.append(page); continue
    page['intro'] = intro_of(rk)
    page['hero'] = [os.path.basename(x[1]) for x in bl if x[0] == 'img' and not SKIP_IMG.search(x[1])]
    tables = [x[1] for x in bl if x[0] == 'table']
    after = [x[1] for x in bl if x[0] == 'p']
    if kv in ('6', '10', '20', '35', '110'):
        page['kind'] = 'models'
        ms = build_models(kv, rk, UA_KEY.get(kv))
        fm = [finish_model(kv, m) for m in ms]
        uniq = []
        numsig = lambda v: tuple(float(y.replace(',', '.')) for y in re.findall(r'\d+(?:,\d+)?', v.replace(' ', '')))
        for x in sorted(fm, key=lambda z: -len(z['spec'])):
            dup = None
            for y in uniq:
                if y['name'] == x['name'] and y['kv'] == x['kv']:
                    ys = {l: numsig(v) for l, u, v in y['spec']}
                    if all(l in ys and ys[l] == numsig(v) for l, u, v in x['spec'] if v != 'уточняйте'):
                        dup = y; break
            if dup:
                dup['src'] += [z for z in x['src'] if z not in dup['src']]
                dup['images'] += [z for z in x['images'] if z not in dup['images']]
                quirk(x['id'], f'дубль: страница совпадает с {dup["id"]} (то же название, те же значения); показана одна запись')
            else: uniq.append(x)
        page['models'] = sorted(uniq, key=model_sort)
        # общий текст «Варианты обозначения ...»
        for t in after:
            if t.startswith('Варианты обозначения') and len(t) > 100: page['variants_text'] = re.sub(r'^Варианты обозначения[^:]*:\s*', '', re.sub(r'\s*\n\s*', ' ', t))
        for g in tables:
            if len(g[0]) >= 3 and 'арактеристик' in g[0][0]['t']:
                page['custom_matrix'] = table_rows(g)
            if len(g) == 1 and len(g[0]) == 1 and 'Варианты' in g[0][0]['t']:
                page['variants_text'] = re.sub(r'^Варианты обозначения[^:]*:\s*', '', re.sub(r'\s*\n\s*', ' ', g[0][0]['t']))
    elif kv in ('3', '15', '150', '220', '330'):
        page['kind'] = 'matrix'
        g = [t for t in tables if len(t) >= 15][0]
        page['matrix'] = table_rows(g)
        for t in after:
            if t.startswith('Варианты обозначения') and len(t) > 30: page['variants_text'] = re.sub(r'\s*\n\s*', ' ', t)
    else:   # 022
        page['kind'] = 'raw'
        page['tables'] = [table_rows(t) for t in tables]
        page['paras'] = [t for t in after]
    PAGES.append(page)

# ---------- матрицы: единые подписи, класс напряжения ----------
REF = None
for pg in PAGES:
    if pg['id'] == '3': REF = [r[0] for r in pg['matrix'][2:15]]
for pg in PAGES:
    if pg['kind'] != 'matrix': continue
    mx = pg['matrix']
    mx[0] = ['Наименование характеристики', 'Ед. изм.'] + mx[0][2:]
    mx[1] = ['Наименование характеристики', 'Ед. изм.'] + mx[1][2:]
    for i in range(2, 15):
        raw_l = mx[i][0]
        canon = re.sub(r'^\d+\s+', '', raw_l)
        if pg['id'] in ('150', '220', '330'):
            mx[i][0] = REF[i - 2]
        mx[i][1] = mx[i][1].replace('Единица изменения', 'Ед. изм.')
    # класс напряжения
    row = mx[2]
    if pg['id'] in ('150', '220', '330'):
        vals = set(c for c in row[2:])
        quirk('opn' + pg['id'], f'в таблице характеристик ОПН {pg["id"]} кВ строка «Класс напряжения сети» = {", ".join(sorted(vals))} кВ (скопировано со страницы 110 кВ); выведено {pg["id"]} кВ')
        mx[2] = [row[0], row[1]] + [pg['id']] * (len(row) - 2)
    # убрать строки «Примечание» и «Варианты обозначения» из матрицы (они вынесены отдельно)
    pg['matrix_note'] = mx[15][0].replace('Примечание\n', '').split('\n') if len(mx) > 15 else []
    pg['matrix'] = mx[:15]
    extra = mx[16][0] if len(mx) > 16 else ''
    if extra.startswith('Варианты обозначения:') and len(extra) > 25:
        pg['variants_text'] = re.sub(r'\s*\n\s*', ' ', extra.replace('Варианты обозначения:', '').strip())
    elif 'variants_text' in pg:
        pg['variants_text'] = re.sub(r'^Варианты обозначения:\s*', '', pg['variants_text'])

# ---------- регистраторы ----------
REGS = []
for key, fname, title in [('ru_JCQF2.html', 'jcqf2', 'JCQF2'), ('ru_JCQF3.html', 'jcqf3', 'JCQF3')]:
    bl = blocks_of(key)
    paras = []
    for x in bl:
        if x[0] == 'p':
            t = x[1].strip()
            if t.startswith('Купить ОПН'): break
            if t and not re.search(r'[іїєґ]', t): paras.append(t)
            elif re.search(r'[іїєґ]', t): quirk(fname, f'на русской странице есть украинская фраза, не перенесена: «{t[:90]}»')
    imgs = [os.path.basename(x[1]) for x in bl if x[0] == 'img' and not SKIP_IMG.search(x[1])]
    for x in bl:
        if x[0] == 'table':
            for r in x[1]:
                for c in r:
                    for a in c['a']:
                        if a.startswith('IMG:'): imgs.append(os.path.basename(a[4:]))
    REGS.append({'id': fname, 'file': fname + '.html', 'title': title, 'paras': paras, 'images': imgs})
quirk('jcqf3', 'страница называется JCQF3, а в тексте и в подписях регистратор назван «JCQ3» (и «аналогом JCQF3-С1»)')

# ---------- общая страница категории ----------
CATEGORY = {'paras': [], 'adv': [], 'video': None}
_bl = blocks_of('ru_index-2-opnn.html')
_lines = [l.strip() for x in _bl if x[0] == 'p' for l in x[1].split('\n') if l.strip()]
_adv = False
for l in _lines:
    if l.startswith('Преимущества'): _adv = True; continue
    if l.startswith('Испытание ОПН'): continue
    (CATEGORY['adv'] if _adv else CATEGORY['paras']).append(strip_brand(l.rstrip(';').strip()) if _adv else strip_brand(l))
_m = re.search(r'youtube\.com/embed/([\w-]+)', RAW['ru_index-2-opnn.html'])
CATEGORY['video'] = _m.group(1) if _m else None
quirk('opn', 'на странице категории есть встроенное видео YouTube «Испытание ОПН-П-150 кВ на взрывобезопасность» — по решению клиента встроено на opn.html')
quirk('opn', 'в тексте категории: «ОПН … на протяжении многих лет поставляются в адрес предприятий ДТЭК, Укрзализници, Укрэнерго…» (в оригинале с названием старой компании; название убрано) — требует подтверждения клиентом')
quirk('opn022', 'в таблице 0,4 кВ строка «ОПН-П-0,4/0,45/150» (обозначение, по-видимому, обрезано) и строка «ОПН-П-0,4/0,45/5/300-УХЛ1» с обозначением по ГОСТ «…/5/400 УХЛ1» (300 против 400) — перенесено как в источнике')
quirk('opn022', 'в таблице прокалывающего зажима: «Длинна пути утечки» (орфография исправлена на «Длина»)')

# ---------- общие нестыковки по страницам ----------
quirk('opn15', 'на странице ОПН 15 кВ использован файл рисунка 6.jpg (имя файла как у страницы 6 кВ); на рисунке габарит обозначен «Нстр» без числовых значений')
quirk('opn33', 'страница ОПН 3,3 кВ на старом сайте «в стадии разработки, техническая информация по запросу» (данных нет)')
quirk('opn27', 'страница ОПН 27,5 кВ на старом сайте «в стадии разработки, техническая информация по запросу» (данных нет)')

def write():
    path = os.path.join(HERE, 'opn_data.py')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n# Данные группы 3 — ограничители перенапряжения ОПН и регистраторы JCQF2/JCQF3.\n')
        f.write('# СГЕНЕРИРОВАНО tools/extract_opn.py из страниц sep.ho.ua (data/opn_raw.tar.gz). Руками не править — править экстрактор.\n\n')
        f.write('PAGES = ' + pprint.pformat(PAGES, width=150, sort_dicts=False) + '\n\n')
        f.write('REGS = ' + pprint.pformat(REGS, width=150, sort_dicts=False) + '\n\n')
        f.write('CATEGORY = ' + pprint.pformat(CATEGORY, width=150, sort_dicts=False) + '\n\n')
        f.write('QUIRKS = ' + pprint.pformat(QUIRKS, width=150) + '\n')
    return path

if __name__ == '__main__':
    pth = write()
    n = sum(len(p.get('models', [])) for p in PAGES)
    print('записано', pth, '| страниц', len(PAGES), '| моделей', n, '| регистраторов', len(REGS), '| нестыковок', len(QUIRKS))
    if '-q' in sys.argv:
        for w, t in QUIRKS: print(f'  [{w}] {t}')
