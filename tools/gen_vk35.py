# -*- coding: utf-8 -*-
"""Страницы группы 4: vk35.html (ВК-35) и vk35u.html (ГКВПШ, усиленная изоляция). Данные: vk35_data.py. Запуск: cd tools && python3 gen_vk35.py"""
import os, re, sys
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import site_nav, vk35_data as D
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head0 = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', src.split('<body>')[0], flags=re.I)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0).replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')
def br(t): return re.sub(r'\n+', '<br>', escape(t))
ASK = 'уточняйте'
META = {
 'vk35': ('Вводы высоковольтные ВК-35 для баковых выключателей 35 кВ', 'Высоковольтные вводы ВК-35 (ВК-35-01…ВК-35-09) для баковых выключателей 35 кВ С-35, ВВС-35, ВТ-35, ВМ-35, МКП-35, ВБЄТ-35 на токи 630–1600 А: размеры h, L, d1, d2, электрические характеристики, чертёж. Поставки по Украине.', 'Вводы ВК-35'),
 'vk35u': ('Вводы высоковольтные ГКВПШ с усиленной изоляцией для выключателей 35 кВ', 'Высоковольтные вводы ГКВПШ-90-40,5/1000 с усиленной изоляцией для баковых выключателей 35 кВ: типы, размеры h, L, d1, d2, электрические характеристики, чертёж. Поставки по Украине.', 'Вводы ГКВПШ с усиленной изоляцией'),
}
def build(pg):
    h1, desc, label = META[pg['id']]
    head = re.sub(r'<title>.*?</title>', f'<title>{escape(h1)} — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>', head0, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(desc)}">', head, count=1)
    th = ''.join(f'<th>{escape(c)}</th>' for c in pg['head'])
    rows = ''.join('<tr>' + ''.join(f'<td class="code">{escape(c)}</td>' if i == 1 else f'<td>{escape(c)}</td>' for i, c in enumerate(r)) + '</tr>' for r in pg['rows'])
    el_name = 'ВК-35' if pg['id'] == 'vk35' else 'ГКВПШ-90-40,5/1000'
    el = ''.join(f'<tr><td>{br(l)}</td><td class="fw-semibold">{"<span class=\"text-muted\">" + ASK + "</span>" if v == ASK else br(v)}</td></tr>' for l, v in pg['electric'])
    extra = ''
    if pg['id'] == 'vk35':
        extra = '<p>Вводы высоковольтные для масляных выключателей 35 кВ конденсаторного типа с RIP изоляцией.</p>'
    body = f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / <a href="vk35.html">Вводы высоковольтные 35 кВ</a> / {escape(label)}</nav>
  <h1>{escape(h1)}</h1>
  <p class="section-lead">{escape(pg['intro'])}</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section><div class="container"><div class="row g-4"><div class="col-lg-3">{site_nav.side_nav('vk35.html', pg['id'] + '.html')}</div><div class="col-lg-9">
  <span class="eyebrow">Модели</span><h2 class="section-title">Типы вводов по выключателям</h2>
  {extra}
  <div class="table-wrap"><table class="spec-table"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note">* {escape(pg['note'])}.</p>
  <div class="row g-4 mt-4 align-items-start">
    <div class="col-xl-5"><span class="eyebrow">Чертёж</span><h2 class="section-title">Габариты</h2><img class="opn-drawing" src="images/vk35.jpg" alt="Габаритный чертёж ввода: размеры h, L, d1, d2" loading="lazy"></div>
    <div class="col-xl-7"><span class="eyebrow">Характеристики</span><h2 class="section-title">Электрические характеристики</h2>
      <div class="table-wrap"><table class="spec-table"><thead><tr><th>Параметр</th><th>{escape(el_name)}</th></tr></thead><tbody>{el}</tbody></table></div>
      <p class="note">Спорные значения отмечены «{ASK}» — свяжитесь с нами для точных данных.</p></div>
  </div>
</div></div></div></section>
<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен ввод для вашего выключателя?</h2>
  <p class="section-lead mx-auto">Подберём ввод по типу выключателя и присоединительным размерам. Доставка по Украине любым удобным перевозчиком.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''
    open(f'{SITE}/{pg["id"]}.html', 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html lang="ru">\n' + head + '<body>\n\n' + header + '\n\n<main>' + body + '\n</main>\n\n' + footer + '\n\n' + tail)
for pg in D.PAGES: build(pg)
print('vk35 pages done')
