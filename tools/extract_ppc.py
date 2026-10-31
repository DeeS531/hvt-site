# -*- coding: utf-8 -*-
"""Группа 6 — проходные изоляторы ППЦ/ИППУ и ввод 110 кВ: data/ppc_raw.tar.gz -> tools/ppc_data.py (+ нестыковки: -q)."""
import os, re, sys, tarfile, pprint
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import opn_parse as P
RAW = {}
with tarfile.open(os.path.join(HERE, '..', 'data', 'ppc_raw.tar.gz')) as t:
    for m in t.getmembers():
        if m.isfile() and m.name.endswith('.html'): RAW[os.path.basename(m.name)] = t.extractfile(m).read().decode('utf-8-sig')
Q = []
def quirk(w, t): Q.append((w, t))
ASK = 'уточняйте'
# ссылки на PDF, которые на старом сайте отдают 404 (проверено curl 2026-10-31)
BROKEN_PDF = {'PPC-20-2000-12,5 УХЛ1.pdf', 'ППЦ-10-1000-8 УХЛ1.pdf', 'PPC-10-4000-30 УХЛ1.pdf', 'PPC-10-4000-12.5 УХЛ1.pdf'}
UKR = re.compile(r'[іїєґІЇЄҐ]')
def blocks(k, alt=True): return P.cut_footer(P.parse(RAW[k], alt))
def one(t): return re.sub(r'\s*\n\s*', ' ', t).strip()
def fnum(s):
    m = re.search(r'\d+(?:[.,]\d+)?', s or ''); return float(m.group(0).replace(',', '.')) if m else None

# ---- подписи (украинские -> русские) ----
LAB = [
 (r'^Номінальна напруга', ('Номинальное напряжение', 'кВ')), (r'^Номинальное напряжение', ('Номинальное напряжение', None)),
 (r'^Номінальний струм', ('Номинальный ток', 'А')),
 (r'^Нормована (руйнуюча|руйнівна)', ('Нормированная разрушающая механическая сила при изгибе, не менее', 'кН')),
 (r'^Нормированная разрушающая', ('Нормированная разрушающая механическая сила при изгибе, не менее', 'кН')),
 (r'^Витримувальна напруга грозового', ('Выдерживаемое напряжение грозового импульса «1,2/50»', 'кВ')),
 (r'^Напряжение выдерживаемого грозового', ('Выдерживаемое напряжение грозового импульса «1,2/50»', 'кВ')),
 (r'^Витримувальна напруга промислової частоти у сухому', ('Выдерживаемое напряжение промышленной частоты в сухом состоянии', 'кВ')),
 (r'^Выдерживаемое напряжение промышленной частоты в сухом', ('Выдерживаемое напряжение промышленной частоты в сухом состоянии', 'кВ')),
 (r'^Довжина шляху витоку зовнішньої ізоляції', ('Длина пути утечки внешней изоляции, не менее', 'мм')),
 (r'^Довжина шляху витоку внутрішньої ізоляції', ('Длина пути утечки внутренней изоляции, не менее', 'мм')),
 (r'^Довжина шляху витоку зовнішньої/внутрішньої', ('Длина пути утечки внешней/внутренней изоляции, не менее', 'мм')),
 (r'^Длина пути утечки, внешней/внутренней', ('Длина пути утечки внешней/внутренней изоляции, не менее', 'мм')),
 (r'^Ізоляційна відстань', ('Изоляционное расстояние внешней/внутренней изоляции, не менее', 'мм')),
 (r'^Изоляционное расстояние', ('Изоляционное расстояние внешней/внутренней изоляции, не менее', 'мм')),
 (r'^Висота встановлення|^Высота установки', ('Высота установки над уровнем моря, не более', 'м')),
 (r'^Кут встановлення|^Угол установки', ('Угол установки', '°')),
 (r'^Тангенс (кута|угла)', ('Тангенс угла диэлектрических потерь', '%')),
 (r'^Пропускна здатність|^Пропускная способность', ('Пропускная способность', 'А')),
 (r'^Клас напруги мережі|^Класс напряжения сети', ('Класс напряжения сети', 'кВ')),
 (r'^Маса, ?(кг, )?не більше|^Масса', ('Масса, не более', 'кг')),
 (r'^Товщина перешкоди', ('Толщина преграды (указывается при заказе)', 'мм')),
 (r'^Материал шин', ('Материал шин и токопровода', '')),
 (r'^Стандарт', ('Стандарт', '')),
 (r'^Необходимая длинна проходной|^Длинна проходной', ('Необходимая длина проходной части H', 'мм')),
]
VALTR = {'Мідь': 'Медь', 'зависит от конфигурации': 'зависит от конфигурации'}
def rows_from(tab):
    out = []
    for r in tab[1:]:
        lab = re.sub(r'^\d+\s+', '', r[0]['t'].strip())
        flat = one(lab)
        if flat.startswith('Напруга, грозового імпульсу'):
            vals = [v.strip() for v in re.split(r'\n+', r[-1]['t']) if v.strip()]
            if len(vals) != 3: raise ValueError('грозовой/пром. частота: ' + repr(vals))
            out += [('Выдерживаемое напряжение грозового импульса «1,2/50»', 'кВ', vals[0]),
                    ('Выдерживаемое напряжение промышленной частоты в сухом состоянии', 'кВ', vals[1]),
                    ('Выдерживаемое напряжение промышленной частоты под дождём', 'кВ', vals[2])]; continue
        m = re.match(r'Витримувальна напруга промислової частоти, кВ, в забрудненому.*?\(([^)]*)\) ?мкСм', flat)
        if m:
            out.append((f'Выдерживаемое напряжение промышленной частоты в загрязнённом и увлажнённом состоянии при удельной поверхностной проводимости загрязнённого слоя ({m.group(1)}) мкСм, не менее', 'кВ', r[-1]['t'].strip())); continue
        for rx, (ru, u) in LAB:
            if re.match(rx, flat):
                unit = u if u is not None else (r[1]['t'].strip() if len(r) == 3 else '')
                if len(r) == 3 and r[1]['t'].strip() and ru in ('Стандарт',): unit = ''
                val = VALTR.get(r[-1]['t'].strip(), r[-1]['t'].strip())
                out.append((ru, unit, val)); break
        else: raise ValueError('неизвестная подпись: ' + flat)
    return out

# ---- главная таблица ----
main = blocks('ru_index-2-PPC.html', False)
tab = next(x[1] for x in main if x[0] == 'table')
items = []
for r in tab[1:]:
    c = [x['t'] for x in r]
    lines = [l.strip() for l in c[0].split('\n') if l.strip()]
    name, note = lines[0].strip(), ', '.join(lines[1:])
    links = [a for x in r for a in x['a']]
    page = next((a for a in links if a.endswith('.html')), None)
    pdf = next((a for a in links if a.endswith('.pdf')), None)
    mm = re.match(r'(?:ППЦ|ИППУ)-(\d+)/(\d+)', name)
    kv = mm.group(1) if mm else re.sub(r'\D', '', c[1])
    amp = mm.group(2) if mm else re.sub(r'[^\d\-]', '', c[2])
    cat_amp = re.sub(r'\D', '', c[2])
    if mm and cat_amp != amp:
        quirk(name, f'в таблице каталога пропускная способность {c[2].strip()}, а в обозначении {amp} А; выведено значение из обозначения')
    items.append({'id': None, 'name': re.sub(r'\s+', ' ', name).replace('УХЛ 1', 'УХЛ1'), 'note': note, 'kv': kv, 'amp': amp, 'page': page, 'pdf_main': pdf,
                  'porcelain': one(c[3]).strip(), 'polymer': one(c[4]).strip() if len(c) > 4 else ''})

# ---- подстраницы ----
IMG_OK = lambda s: not s.endswith('.webp') and 'slide' not in s and 'logo' not in s
def sub(item):
    key = 'ru_' + item['page'].replace(',', '_')
    bl = blocks(key)
    d = {'paras': [], 'spec': None, 'pdf': None, 'image': None, 'variants': None, 'replaces': None, 'extra': [], 'legend': [], 'notes': []}
    ps = [x for x in bl if x[0] == 'p']
    title = ps[0][1]
    d['title'] = one(title)
    for l in re.findall(r'href="chertejy/([^"]*\.pdf)"', RAW[key]):
        if l in BROKEN_PDF: d.setdefault('broken', set()).add(l)
        elif not d['pdf']: d['pdf'] = l
    for x in bl:
        if x[0] == 'img' and IMG_OK(x[1]) and not d['image']: d['image'] = os.path.basename(x[1])
        if x[0] == 'table' and d['spec'] is None:
            d['spec'] = rows_from(x[1]); d['spec_head'] = one(x[1][0][-1]['t'])
    for p in ps:
        t = p[1]; ft = one(t)
        for l in (p[2] if len(p) > 2 else []):
            pass
        m = re.match(r'(Варианты обозначения полимерных аналогов|Варіанти позначення полімерних аналогів|Возможные варианты обозначения)\s*:\s*(.+)', ft)
        if m: d['variants'] = m.group(2).strip().rstrip('.')
        m = re.match(r'(Заменяют фарфоровый проходной изолятор[^:]*|Замінюють порцеляновий прохідний ізолятор[^:]*)\s*:\s*(.+)', ft)
        if m: d['replaces'] = m.group(2).strip()
        if re.search(r'аналог (керамического|керамічного)', ft) and len(ft) > 100: d['paras'].append(ft)
        if re.match(r'(Изолятор ППЦ|Ізолятор ІППУ).*(применяется|застосовується)', ft): d['paras'].append(ft)
        if re.match(r'(Район эксплуатации со степенью|Код УКТ ВЭД)', ft): d['extra'].append(ft.rstrip(':'))
    # значения «лейбл/значение» новых страниц
    flat = [x[1] for x in bl if x[0] == 'p']
    for i, t in enumerate(flat[:-1]):
        if re.match(r'(Район эксплуатации со степенью|Код УКТ ВЭД)', one(t)):
            lab = one(t).rstrip(':').strip()
            lab = 'Район по степени загрязнённости атмосферы (СЗА)' if lab.startswith('Район') else 'Код УКТ ВЭД'
            d['extra'] = [e for e in d['extra'] if not e.startswith(('Район эксплуатации', 'Код УКТ'))]
            d.setdefault('extra_rows', []).append((lab, one(flat[i + 1])))
    d['extra'] = []
    # расшифровка обозначения (новые страницы)
    for i, t in enumerate(flat):
        if one(t).startswith('В условном обозначении проходных изоляторов'):
            for u in flat[i + 1:]:
                if one(u).startswith('Комплект поставки'): break
                d['legend'].append(one(u).rstrip(';. '))
    for t in flat:
        ft = one(t)
        if re.match(r'(H стандартно|\* зависит|По требованию заказчика имеется)', ft): d['notes'].append(ft)
    for b in sorted(d.get('broken', ())):
        quirk(item['name'], f'ссылка на чертёж «{b}» на старом сайте даёт 404 (файла нет)'+('' if d['pdf'] else '; PDF для этой модели нет'))
    d['broken'] = sorted(d.get('broken', ()))
    if any(UKR.search(p) for p in d['paras']):
        quirk(item['name'], 'описание на странице написано по-украински (в русской версии) — не перенесено; таблица характеристик переведена'); d['paras'] = []
    return d

for it in items:
    if not it['page']: continue
    it['sub'] = sub(it)
    it['id'] = re.sub(r'\.html$', '', it['page']).lower().replace(',', '').replace('_', '-')
for it in items:
    if it['id'] is None: it['id'] = re.sub(r'[^0-9a-z]+', '-', (it['name'] + ' ' + it['kv']).lower().replace('ппц', 'ppc')).strip('-') + '-nopage'

# ---- проверки ----
for it in items:
    s = it.get('sub')
    if not s or not s['spec']: continue
    cur = next((v for l, u, v in s['spec'] if l.startswith(('Номинальный ток', 'Пропускная способность'))), None)
    kvv = next((v for l, u, v in s['spec'] if l.startswith('Номинальное напряжение')), None)
    if cur and fnum(cur) and it['amp'].isdigit() and fnum(cur) != float(it['amp']):
        quirk(it['name'], f'ток в таблице характеристик {cur} А не совпадает с обозначением ({it["amp"]} А)')
    t = s['title']
    mm = re.search(r'(?:ППЦ|ИППУ|ІППУ)-(\d+)/(\d+)', t)
    if mm and it['name'].startswith(('ППЦ', 'ИППУ')) and (mm.group(1), mm.group(2)) != (it['kv'], it['amp']):
        quirk(it['name'], f'заголовок страницы «{t}» не совпадает с названием в каталоге «{it["name"]}»')
    h = s.get('spec_head', '')
    mh = re.search(r'(?:ППЦ|ИППУ|ІППУ)-(\d+)/(\d+)', h)
    if mh and (mh.group(1), mh.group(2)) != (it['kv'], it['amp']):
        quirk(it['name'], f'заголовок столбца таблицы характеристик «{h}» не совпадает с названием «{it["name"]}»')
# конкретные расхождения
for it in items:
    s = it.get('sub')
    if it['page'] == 'izolyator-prohidniy-polimerniy-20-3150-ukhl1.html':
        quirk(it['name'], 'заголовок над таблицей: «Технические характеристики изоляторов ИППУ-20/3150-30 УХЛ1» (сила 30 вместо 12,5); сила в таблице «8, 12,5, 20»')
        quirk(it['name'], 'в верхнем блоке длина пути утечки внешней изоляции 720 мм, в таблице 750/570 мм (внешняя/внутренняя)')
    if it['page'] and it['page'].startswith('izolyator-prohidniy-polimerniy-110'):
        quirk(it['name'], 'в названии 800-2000 А (адрес страницы …800-4000), в таблице 630-2000 А; тангенс угла потерь «>0,7 %» — вероятно «не более»; единица у «Стандарт» указана «мм»; перенесено как в источнике')
    if it['name'].startswith('ППЦ-10/630-12,5'): quirk(it['name'], 'в каталоге ссылка ведёт только на PDF (81.pdf), отдельной страницы нет')
    if it['name'].startswith('ППЦ-20/630-12,5'): quirk(it['name'], 'строка без ссылок и без страницы характеристик')
quirk('ППЦ/ИППУ-10/4000', 'в каталоге «ИППУ-10/4000-30-А4 УХЛ1», на странице и в таблице — «ИППУ-10/4000-12,5 УХЛ1» (сила 12,5 кН); PDF называется «PPC-10-4000-12.5»; перенесено как в источнике')
quirk('ppc', 'у «ИППУ-35/3150», «ИППУ-35/4000», «ИППУ-20/3150» и «110 кВ» на страницах есть фото-галерея (webp) с чужими стоковыми/заводскими фото неясного происхождения — не использованы; использованы только чертежи')
quirk('ppc', 'чертёж PPC-35-3150.jpg / PPC-35-4000.jpg содержал водяные знаки старого сайта — убраны tools/unwatermark.js (WHITE=205)')
quirk('ppc', 'с сайта не перенесены цены (110000 грн, 250000 грн), SEO-тексты и преимущества с формулировками про «боевые действия»; украинская страница 110 кВ (UA/…) использована как контроль')
quirk('ppc', 'в таблицах характеристик русских страниц подписи по-украински — переведены; значения не менялись')

with open(os.path.join(HERE, 'ppc_data.py'), 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n# СГЕНЕРИРОВАНО tools/extract_ppc.py (группа 6: проходные изоляторы)\n\nITEMS = ' + pprint.pformat(items, width=150, sort_dicts=False) + '\n\nQUIRKS = ' + pprint.pformat(Q, width=150) + '\n')
print('записано; позиций', len(items), '| со страницей', sum(1 for i in items if i.get('sub')), '| нестыковок', len(Q))
if '-q' in sys.argv:
    for w, t in Q: print(f'  [{w}] {t}')
