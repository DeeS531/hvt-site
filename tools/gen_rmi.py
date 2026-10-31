# -*- coding: utf-8 -*-
"""Группа 8 — распорки междуфазные РМИ-35/110/220/330: rmi.html.
Страница features-grid.html на старом сайте сейчас отдаёт 404, поэтому данные — из таблицы чертежа chertejy/104.pdf (site/pdf/104.pdf), перенесены вручную с проверкой по увеличенному изображению.
Запуск: cd tools && python3 gen_rmi.py"""
import os, re, sys
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', src.split('<body>')[0], flags=re.I)
T = 'Распорки междуфазные изолирующие полимерные РМИ-35, РМИ-110, РМИ-220, РМИ-330'
DESC = 'Междуфазные изолирующие полимерные распорки РМИ для линий электропередачи 35, 110, 220 и 330 кВ: характеристики, длина пути утечки, строительная высота, масса, чертёж. Поставки по Украине.'
head = re.sub(r'<title>.*?</title>', f'<title>{escape(T)} — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(DESC)}">', head, count=1)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0).replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')
COLS = ['РМИ-35', 'РМИ-110', 'РМИ-220', 'РМИ-330']
ROWS = [
 ('Номинальное напряжение, кВ', ['35', '110', '220', '330']),
 ('Нормированная разрушающая механическая сила при растяжении, не менее, кН', ['120', '120', '120', '120']),
 ('Степень загрязнения (СЗ) по СОУ МПЕ 40.1.51.301', ['5', '5', '5', '5']),
 ('Степень загрязнённости атмосферы (СЗА) по ГОСТ 28856', ['VII', 'VII', 'VII', 'VII']),
 ('Длина пути утечки, мм', ['2000', '5200', '11600', '14200']),
 ('Строительная высота, Нстр, мм', ['2500', '4200-5000', '6200-7000', '7500-8300']),
 ('Масса, не более, кг', ['15,0', '25,0', '29,0', '40,0']),
 ('Рисунок №', ['1', '2', '3', '4']),
]
th = ''.join(f'<th>{c}</th>' for c in COLS)
tr = ''.join('<tr><td>' + escape(l) + '</td>' + ''.join(f'<td class="fw-semibold">{escape(v)}</td>' for v in vs) + '</tr>' for l, vs in ROWS)
body = f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / Распорки межфазные РМИ</nav>
  <h1>Распорки междуфазные изолирующие полимерные РМИ</h1>
  <p class="section-lead">Распорки для линий электропередачи на напряжение 35, 110, 220 и 330 кВ (класс нагрузки 120 кН, район СЗА 5 по СОУ МПЕ 40.1.51.301).</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section><div class="container"><div class="row g-4 mx-0 align-items-start">
  <div class="col-12"><span class="eyebrow">Характеристики</span><h2 class="section-title">Основные показатели распорок</h2>
    <div class="table-wrap"><table class="spec-table matrix-table"><thead><tr><th>Показатель</th>{th}</tr></thead><tbody>{tr}</tbody></table></div>
    <p class="note">«Рисунок №» — номер рисунка на чертеже (РМИ-35 — рис. 1, РМИ-110 — рис. 2, РМИ-220 — рис. 3, РМИ-330 — рис. 4).</p>
    <p class="mt-3"><a class="btn-main" href="pdf/104.pdf" target="_blank" rel="noopener"><i class="fa fa-file-pdf-o"></i> Чертёж 104.pdf</a></p></div>
  <div class="col-lg-7"><img class="opn-drawing" src="images/rmi104.png" alt="Чертёж распорок междуфазных РМИ-35, РМИ-110, РМИ-220, РМИ-330 (рисунки 1–4)" loading="lazy"></div>
</div></div></section>
<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен подбор распорки?</h2>
  <p class="section-lead mx-auto">Подберём междуфазную распорку по классу напряжения и условиям линии. Доставка по Украине любым удобным перевозчиком.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''
open(f'{SITE}/rmi.html', 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html lang="ru">\n' + head + '<body>\n\n' + header + '\n\n<main>' + body + '\n</main>\n\n' + footer + '\n\n' + tail)
print('rmi.html done')
