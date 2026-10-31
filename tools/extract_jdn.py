# -*- coding: utf-8 -*-
"""Группа 5 — изоляторы контактной сети: data/jdn_raw.tar.gz -> tools/jdn_data.py (+ нестыковки: -q)."""
import os, re, sys, tarfile, pprint
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import opn_parse as P
RAW = {}
with tarfile.open(os.path.join(HERE, '..', 'data', 'jdn_raw.tar.gz')) as t:
    for m in t.getmembers(): RAW[m.name] = t.extractfile(m).read().decode('utf-8-sig')
Q = []
def quirk(w, t): Q.append((w, t))
html = RAW['index-2-jdn.html']
# 14 чертежей — из выпадающего меню сайта
items = []
for href, name in re.findall(r'<a href="chertejy/(\d+\.pdf)"[^>]*>\s*([^<]+?)\s*</a>', html):
    m = re.match(r'(.+?) изолятор ([А-ЯЁ]+) (\d+)-([\d,]+)-(\d+)$', name.strip().replace('\xa0', ' '))
    typ, series, force, kv, n = m.groups()
    items.append({'pdf': href, 'type': typ + ' изолятор', 'model': f'{series} {force}-{kv}-{n}', 'series': series, 'kv': kv})
ORDER = ['ПСКЦ', 'НСКЦ', 'ФСКЦ', 'КСКЦ', 'КФСКЦ']
items.sort(key=lambda x: (ORDER.index(x['series']), float(x['kv'].replace(',', '.')), x['model']))
bl = P.cut_footer(P.parse(html))
raw_paras = [x[1] for x in bl if x[0] == 'p' and len(x[1]) > 80]
paras = []
for t in raw_paras:
    t = t.replace('СЛАВЭНЕРГОСИСТЕМ', '').replace('Главным Управленипромем', 'Главным Управлением')
    t = re.sub(r'продукция, предлагаемая\s*,', 'продукция', t)
    paras.append(re.sub(r'\s+', ' ', t).strip())
lead = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
quirk('jdn', 'в тексте убрано название старой компании («продукция, предлагаемая СЛАВЭНЕРГОСИСТЕМ» → «продукция»); исправлена опечатка «Управленипромем» → «Управлением»')
quirk('jdn', 'утверждения «разработаны в сотрудничестве с Главным Управлением электрификации Укрзализници», «сертификаты соответствия УкрСЕПРО», «более 18 лет опыта эксплуатации» — перенесены, требуют подтверждения клиентом')
quirk('jdn', 'на странице нет таблиц характеристик: только описание и 14 PDF-чертежей; расшифровка «-5»/«-7» в обозначениях на сайте не дана (не переносилась)')
quirk('jdn', 'украинская страница (UA/index-2-jdn.html) на русском; ссылки на чертежи UA/chertejy/*.pdf — те же имена, что и chertejy/*.pdf (проверяется по md5 при скачивании)')
with open(os.path.join(HERE, 'jdn_data.py'), 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n# СГЕНЕРИРОВАНО tools/extract_jdn.py\nITEMS = ' + pprint.pformat(items, width=150, sort_dicts=False) + '\n\nPARAS = ' + pprint.pformat(paras, width=150) + '\n\nQUIRKS = ' + pprint.pformat(Q, width=150) + '\n')
print('записано; чертежей', len(items), '| абзацев', len(paras))
if '-q' in sys.argv:
    for w, t in Q: print(f'  [{w}] {t}')
