# -*- coding: utf-8 -*-
"""Страница группы «Линейные изоляторы» (lkc.html): боковой список подгрупп + карточки 70/120/160 кН.
Описание берётся из lkc70.html (то же, что уже одобрено). Запуск: cd tools && python3 gen_lkc.py"""
import os, re, sys
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import site_nav
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', src.split('<body>')[0], flags=re.I)
head = re.sub(r'<title>.*?</title>', '<title>Линейные изоляторы ЛКЦ (ЛК) 70, 120, 160 кН — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>', head, count=1)
desc = 'Линейные подвесные стержневые полимерные изоляторы ЛКЦ (ЛК) на классы нагрузки 70, 120 и 160 кН, номинальное напряжение от 10 до 500 кВ. Модели, чертежи, варианты обозначения.'
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head, count=1)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0).replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
desc_html = re.search(r'<span class="eyebrow">Описание</span>.*?(?=</div>\s*<div class="col-lg-5">)', src, re.S).group(0)
legend = re.search(r'<div class="col-lg-5">(.*?)</div>\s*</div>\s*</div>\s*</section>', src, re.S).group(1)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')
cards = ''.join(f'<div class="col-6 col-md-4"><a class="volt-card" href="{h}"><span class="volt-num">{n}</span><span class="volt-unit">кН</span><span class="volt-cnt">{c}</span></a></div>'
                for n, h, c in [(70, 'lkc70.html', '10–500 кВ'), (120, 'lkc120.html', '35–330 кВ'), (160, 'lkc160.html', '110–500 кВ')])
body = f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / Линейные изоляторы</nav>
  <h1>Линейные изоляторы ЛКЦ (ЛК)</h1>
  <p class="section-lead">Подвесные стержневые полимерные изоляторы на класс нагрузки 70, 120 и 160 кН, номинальное напряжение от 10 до 500 кВ.</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section><div class="container"><div class="row g-4"><div class="col-lg-3">{site_nav.side_nav('lkc.html')}</div><div class="col-lg-9">
  <span class="eyebrow">Выберите класс нагрузки</span><h2 class="section-title">Каталог по классам нагрузки</h2>
  <div class="row g-3 mb-5">{cards}</div>
  <div class="row g-4 mx-0">
    <div class="col-xl-7">{desc_html}</div>
    <div class="col-xl-5">{legend}</div>
  </div>
</div></div></div></section>
<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен подбор или цена завода?</h2>
  <p class="section-lead mx-auto">Минимальный заказ — от 1 штуки. Доставка любым удобным перевозчиком.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''
open(f'{SITE}/lkc.html', 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html lang="ru">\n' + head + '<body>\n\n' + header + '\n\n<main>' + body + '\n</main>\n\n' + footer + '\n\n' + tail)
print('lkc.html done')
