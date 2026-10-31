# -*- coding: utf-8 -*-
"""Группа 4 — вводы ВК-35 и ГКВПШ: data/vk35_raw.tar.gz -> tools/vk35_data.py (+ нестыковки: -q)."""
import os, re, sys, tarfile, pprint
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import opn_parse as P
RAW = {}
with tarfile.open(os.path.join(HERE, '..', 'data', 'vk35_raw.tar.gz')) as t:
    for m in t.getmembers(): RAW[m.name] = t.extractfile(m).read().decode('utf-8-sig')
Q = []
def quirk(w, t): Q.append((w, t))
ASK = 'уточняйте'

def page(key, ident):
    bl = P.cut_footer(P.parse(RAW[key]))
    paras = [x[1] for x in bl if x[0] == 'p' and not x[1].startswith(('Купить', 'Электрические', '*'))]
    tabs = [x[1] for x in bl if x[0] == 'table']
    types = [[c['t'] for c in r] for r in tabs[0]]
    el = [[c['t'] for c in r] for r in tabs[1]]
    note = next(x[1] for x in bl if x[0] == 'p' and x[1].startswith('*'))
    rows = []
    for r in el[1:]:
        lab = re.sub(r'^\d+\s+', '', r[0]).replace('плд дождем', 'под дождём').replace('Длинна', 'Длина').replace('дождем', 'дождём')
        rows.append((lab, r[1]))
    return {'id': ident, 'intro': paras[0], 'head': types[0], 'rows': types[1:], 'note': note.lstrip('*'), 'electric': rows, 'electric_head': el[0][1]}

vk = page('index-2-vk35.html', 'vk35'); vu = page('index-2-vk35u.html', 'vk35u')
for pg, label in ((vk, 'ВК-35'), (vu, 'ГКВПШ')):
    out = []
    for lab, v in pg['electric']:
        if lab.startswith('Номинальное напряжение'):
            quirk(pg['id'], f'в таблице электрических характеристик «{label}» номинальное напряжение = {v} кВ (ввод на 35 кВ, импульс 190 кВ); выведено «{ASK}»'); v = ASK
        out.append((lab, v))
    pg['electric'] = out
quirk('vk35u', 'таблица «Электрические характеристики» ГКВПШ скопирована с ВК-35 (заголовок столбца «ВК-35», ток 630-1600 А при обозначении «/1000»); отличается только тангенс угла потерь: 0,02 против 0,005 у ВК-35')
quirk('vk35u', 'исполнение «ГКВПШ-90-40,5/1000-010» — вероятно, опечатка (ряд -01…-09, затем -010); перенесено как в источнике')
quirk('vk35', 'в тексте исправлены опечатки: «плд дождем» → «под дождём», «Длинна» → «Длина»')
quirk('vk35/vk35u', 'украинские страницы (UA/index-2-vk35.html, …vk35u.html) полностью на русском, как русские; украинского перевода на старом сайте нет')
quirk('vk35', 'на странице нет PDF-чертежей; чертёж — картинка vk35.jpg (без водяных знаков)')
def write():
    with open(os.path.join(HERE, 'vk35_data.py'), 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n# СГЕНЕРИРОВАНО tools/extract_vk35.py (данные группы 4: ВК-35 и ГКВПШ)\n\n')
        f.write('PAGES = ' + pprint.pformat([vk, vu], width=150, sort_dicts=False) + '\n\nQUIRKS = ' + pprint.pformat(Q, width=150) + '\n')
if __name__ == '__main__':
    write(); print('записано; нестыковок', len(Q))
    if '-q' in sys.argv:
        for w, t in Q: print(f'  [{w}] {t}')
