# -*- coding: utf-8 -*-
"""Группа 6 — страница ppc.html (проходные изоляторы ППЦ/ИППУ 10–35 кВ и ввод 110 кВ). Данные: ppc_data.py. Запуск: cd tools && python3 gen_ppc.py"""
import os, re, sys, urllib.parse
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ppc_data as D
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', src.split('<body>')[0], flags=re.I)
T = 'Проходные изоляторы ППЦ, ИППУ 10, 20, 35 кВ и линейные вводы 110 кВ'
n_det = sum(1 for i in D.ITEMS if i.get('sub'))
DESC = f'Полимерные проходные изоляторы ППЦ и ИППУ на 10, 20 и 35 кВ (630–4000 А) и линейные вводы 110 кВ: {len(D.ITEMS)} позиций, характеристики, аналоги фарфоровых ИП, ИПУ, чертежи. Поставки по Украине.'
head = re.sub(r'<title>.*?</title>', f'<title>{escape(T)} — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(DESC)}">', head, count=1)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0).replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')
ASK = 'уточняйте'
def br(t): return re.sub(r'\n+', '<br>', escape(t))
def cell(t): return escape(t) if t else '<span class="text-muted">—</span>'
def pdf_name(i):
    s = i.get('sub') or {}
    n = s.get('pdf') or (os.path.basename(i['pdf_main']) if i.get('pdf_main') else None)
    return n
def pdf_link(n):
    return f'<a href="pdf/{urllib.parse.quote(n)}" target="_blank" rel="noopener"><i class="fa fa-file-pdf-o"></i> {escape(n)}</a>' if n else '<span class="text-muted">—</span>'
IMGFIX = {'A9R69D5.pdf.png': 'PPC-10-630-01.png', 'PPC-20-2000-12,5.jpg': 'PPC-20-2000-12_5.jpg', 'PPC-35-3150.jpg': 'PPC-35-3150.png', 'PPC-35-4000.jpg': 'PPC-35-4000.png'}
def imgpath(n):
    n = IMGFIX.get(n, n)
    return 'images/ppc/' + urllib.parse.quote(n)

rows = []; cards = []
for it in D.ITEMS:
    s = it.get('sub')
    nm = escape(it['name']) if not s else f'<a href="#d-{it["id"]}">{escape(it["name"])}</a>'
    if it['note']: nm += f'<div class="small text-muted mt-1">{escape(it["note"])}</div>'
    amp = it['amp'] + ' А'
    rows.append(f'<tr id="r-{it["id"]}"><td class="code">{nm}</td><td>{escape(it["kv"])} кВ</td><td>{escape(amp)}</td><td>{cell(it["porcelain"])}</td><td>{cell(it["polymer"])}</td><td>{pdf_link(pdf_name(it))}</td></tr>')
    if not s: continue
    body = []
    for pp in s['paras']: body.append(f'<p class="mb-2">{escape(pp)}</p>')
    if s.get('variants'): body.append(f'<p class="mb-2"><b>Варианты обозначения полимерных аналогов:</b> {escape(re.sub(r"\s*/\s*", " ", s["variants"]))}</p>')
    rep = s.get('replaces')
    if rep: body.append(f'<p class="mb-2"><b>Заменяют фарфоровый проходной изолятор:</b> {escape(re.sub(r"\s*/\s*", " ", rep))}</p>')
    spec = list(s['spec']) + list(s.get('extra_rows', []))
    trip = [(x + ('',))[:3] if len(x) == 3 else (x[0], '', x[1]) for x in spec]
    sr = ''.join(f'<tr><td>{br(l)}</td><td>{escape(u) or "—"}</td><td class="fw-semibold">{br(v)}</td></tr>' for l, u, v in trip)
    body.append(f'<div class="table-wrap"><table class="spec-table"><thead><tr><th>Показатель</th><th>Ед. изм.</th><th>{escape(it["name"])}</th></tr></thead><tbody>{sr}</tbody></table></div>')
    for nt in s['notes']: body.append(f'<p class="note mb-1">{escape(nt)}</p>')
    if s['legend']:
        lg = ''.join('<div>' + (f'<b>{escape(x.split(" — ")[0].split("—")[0].strip())}</b> — {escape(x.split("—", 1)[1].strip())}' if '—' in x else escape(x)) + '</div>' for x in s['legend'][1:] if x)
        body.append(f'<div class="code-block mt-3">{lg}</div>')
    if s['image']: body.append(f'<div class="opn-drawings mt-3"><img class="opn-drawing" src="{imgpath(s["image"])}" alt="Чертёж {escape(it["name"])}" loading="lazy"></div>')
    body.append(f'<p class="mt-3 mb-0">{pdf_link(pdf_name(it))}</p>')
    cards.append(f'<details class="spec-details" id="d-{it["id"]}"><summary><span class="code">{escape(it["name"])}</span><span class="small text-muted ms-2">{escape(it["kv"])} кВ, {escape(amp)}{", " + escape(it["note"]) if it["note"] else ""}</span></summary><div class="spec-body">{"".join(body)}</div></details>')
body = f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / Проходные изоляторы</nav>
  <h1>Проходные изоляторы ППЦ, ИППУ</h1>
  <p class="section-lead">Полимерные проходные изоляторы на 10, 20 и 35 кВ (630–4000 А) и линейные вводы 110 кВ. Для ввода и изоляции токоведущих частей закрытых распределительных устройств электрических станций и подстанций. Позиций: {len(D.ITEMS)}.</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section class="section-soft"><div class="container">
  <span class="eyebrow">Модели</span><h2 class="section-title">Проходные изоляторы и вводы</h2>
  <p class="section-lead">Название модели — ссылка на характеристики и чертёж. Показаны фарфоровые изоляторы, которые заменяют полимерные, и варианты обозначения полимерных аналогов.</p>
  <div class="table-wrap"><table class="spec-table ppc-table"><thead><tr><th>Модель</th><th>Напряжение</th><th>Ток</th><th>Фарфоровый аналог (варианты обозначения)</th><th>Варианты обозначения полимерного аналога</th><th>Чертёж</th></tr></thead><tbody>{chr(10).join(rows)}</tbody></table></div>
  <p class="note">Присоединительные размеры могут изменяться по требованию заказчика. Если нужной модели нет в списке, свяжитесь с нами — подберём изолятор.</p>
</div></section>
<section><div class="container"><span class="eyebrow">Характеристики</span><h2 class="section-title">Технические характеристики</h2><p class="section-lead">Раскройте нужную модель, чтобы увидеть параметры.</p>
{chr(10).join(cards)}
</div></section>
<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен подбор изолятора?</h2>
  <p class="section-lead mx-auto">Подберём проходной изолятор вместо фарфорового. Доставка по Украине любым удобным перевозчиком.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''
open(f'{SITE}/ppc.html', 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html lang="ru">\n' + head + '<body>\n\n' + header + '\n\n<main>' + body + '\n</main>\n\n' + footer + '\n\n' + tail)
print('ppc.html done; used images:', sorted({(i.get('sub') or {}).get('image') for i in D.ITEMS} - {None}))
