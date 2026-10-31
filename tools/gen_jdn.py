# -*- coding: utf-8 -*-
"""Страница группы 5: jdn.html — изоляторы полимерные для контактной сети ж/д. Данные: jdn_data.py. Запуск: cd tools && python3 gen_jdn.py"""
import os, re, sys, urllib.parse
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import jdn_data as D
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', src.split('<body>')[0], flags=re.I)
T = 'Изоляторы полимерные для контактной сети железных дорог ПСКЦ, НСКЦ, ФСКЦ, КСКЦ, КФСКЦ'
DESC = 'Полимерные стержневые изоляторы для контактной сети электрифицированных железных дорог: подвесные ПСКЦ, натяжные НСКЦ, фиксаторные ФСКЦ, консольные КСКЦ, консольно-фиксаторные КФСКЦ на 3,3 и 27,5 кВ. 14 моделей, чертежи. Поставки по Украине.'
head = re.sub(r'<title>.*?</title>', f'<title>{escape(T)} — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(DESC)}">', head, count=1)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0).replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')
rows = ''.join(f'<tr id="r-{i["pdf"][:-4]}"><td>{escape(i["type"])}</td><td class="code">{escape(i["model"])}</td><td>{escape(i["kv"])}</td>'
               f'<td><a href="pdf/{urllib.parse.quote(i["pdf"])}" target="_blank" rel="noopener"><i class="fa fa-file-pdf-o"></i> {escape(i["pdf"])}</a></td></tr>' for i in D.ITEMS)
paras = ''.join(f'<p>{escape(p)}</p>' for p in D.PARAS)
body = f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / Изоляторы для контактной сети</nav>
  <h1>Изоляторы полимерные для контактной сети железных дорог</h1>
  <p class="section-lead">Подвесные ПСКЦ, натяжные НСКЦ, фиксаторные ФСКЦ, консольные КСКЦ и консольно-фиксаторные КФСКЦ на 3,3 и 27,5 кВ. Моделей: {len(D.ITEMS)}.</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section><div class="container"><div class="row g-4 mx-0"><div class="col-lg-9"><span class="eyebrow">Описание</span><h2 class="section-title">Изоляторы ПСКЦ, НСКЦ, ФСКЦ, КСКЦ, КФСКЦ</h2>{paras}</div></div></div></section>
<section class="section-soft"><div class="container">
  <span class="eyebrow">Модели</span><h2 class="section-title">Модели и чертежи</h2>
  <p class="section-lead">Габаритные чертежи изоляторов — в PDF (откроются в новой вкладке).</p>
  <div class="table-wrap"><table class="spec-table"><thead><tr><th>Тип</th><th>Модель</th><th>Напряжение, кВ</th><th>Чертёж</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note">Если нужной модели нет в списке, свяжитесь с нами — подберём изолятор.</p>
</div></section>
<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен подбор изолятора?</h2>
  <p class="section-lead mx-auto">Подберём изолятор для контактной сети по типу и напряжению. Доставка по Украине любым удобным перевозчиком.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''
open(f'{SITE}/jdn.html', 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html lang="ru">\n' + head + '<body>\n\n' + header + '\n\n<main>' + body + '\n</main>\n\n' + footer + '\n\n' + tail)
print('jdn.html done')
