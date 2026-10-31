# -*- coding: utf-8 -*-
"""«Прочее»: zamena.html (таблицы взаимозаменяемости ОСК, из index-10.html и index-10_p.html) и docs.html (документы).
Сырые страницы: data/misc_raw.tar.gz. Запуск: cd tools && python3 gen_misc.py"""
import os, re, sys, tarfile, urllib.parse
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import opn_parse as P
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
RAW = {}
with tarfile.open(os.path.join(HERE, '..', 'data', 'misc_raw.tar.gz')) as t:
    for m in t.getmembers(): RAW[m.name] = t.extractfile(m).read().decode('utf-8-sig')
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head0 = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', src.split('<body>')[0], flags=re.I)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0).replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')
def page(file, title, desc, body):
    h = re.sub(r'<title>.*?</title>', f'<title>{escape(title)} — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>', head0, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(desc)}">', h, count=1)
    open(f'{SITE}/{file}', 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html lang="ru">\n' + h + '<body>\n\n' + header + '\n\n<main>' + body + '\n</main>\n\n' + footer + '\n\n' + tail)
def hero(crumb, h1, lead):
    return f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / {crumb}</nav>
  <h1>{escape(h1)}</h1>
  <p class="section-lead">{escape(lead)}</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>'''
CTA = '''<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Не нашли нужный аналог?</h2>
  <p class="section-lead mx-auto">Свяжитесь с нами — подберём полимерный изолятор вместо фарфорового.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''
def slug(m): return re.sub(r'[^0-9A-Za-z_]+', '-', m.replace('ОСК', 'osk').replace(',', '_').replace('/', '-')).strip('-').lower()
osk_ids = {}
for kv in (10, 20, 35, 110, 150, 220):
    osk_ids[kv] = set(re.findall(r'id="r-([^"]+)"', open(f'{SITE}/osk{kv}.html', encoding='utf-8').read()))
def link_model(name):
    m = re.match(r'ОСК\s*[\d,]+-(\d+)/', name)
    if m and int(m.group(1)) in osk_ids:
        kv = int(m.group(1)); sl = slug(name)
        if sl in osk_ids[kv]: return f'<a href="osk{kv}.html#r-{sl}">{escape(name)}</a>'
    return escape(name)
def table(key, head):
    bl = P.cut_footer(P.parse(RAW[key], True)); g = next(x[1] for x in bl if x[0] == 'table')
    rows = []
    for r in g[1:]:
        c0 = [l.strip() for l in r[0]['t'].split('\n') if l.strip()]
        mm = re.search(r'(И?ОСК\s*[\d,]+-\d+/\S+)', ' '.join(c0))
        if not mm: continue
        name = mm.group(1)
        items = [l.strip().rstrip(',').strip() for l in r[1]['t'].split('\n') if l.strip()]
        items = [i for i in items if i and i not in ('Изолятор', 'Ізолятор', 'Ізолятор порцеляновий', 'Изолятор фарфоровый')]
        rows.append((name, ', '.join(items)))
    tr = ''.join(f'<tr><td class="code">{link_model(n)}</td><td>{escape(v) if v else "—"}</td></tr>' for n, v in rows)
    return rows, f'<div class="table-wrap"><table class="spec-table"><thead><tr><th>Полимерный изолятор</th><th>{head}</th></tr></thead><tbody>{tr}</tbody></table></div>'
r1, t1 = table('index-10.html', 'Фарфоровый аналог (варианты обозначения)')
r2, t2 = table('index-10_p.html', 'Варианты обозначения полимерного изолятора')
body = hero('Взаимозаменяемость изоляторов ОСК', 'Взаимозаменяемость опорных изоляторов ОСК', 'Полимерные опорные изоляторы ОСК и фарфоровые изоляторы ИОС, ИОР, ИО, ОНШ, УСТ, ОНС, АКО, которые они заменяют, а также варианты обозначения полимерных изоляторов.') + f'''
<section><div class="container"><span class="eyebrow">Фарфоровые аналоги</span><h2 class="section-title">Полимерные аналоги фарфоровых изоляторов</h2>
  <p class="section-lead">Моделей: {len(r1)}. Название модели ОСК — ссылка на страницу с подробными характеристиками.</p>{t1}</div></section>
<section class="section-soft"><div class="container"><span class="eyebrow">Варианты обозначения</span><h2 class="section-title">Варианты обозначения полимерных изоляторов ОСК</h2>
  <p class="section-lead">Моделей: {len(r2)}.</p>{t2}
  <p class="note">Данные соответствуют таблицам на страницах каталога опорных изоляторов <a href="osk.html">ОСК</a>.</p></div></section>
{CTA}'''
page('zamena.html', 'Взаимозаменяемость опорных изоляторов ОСК и фарфоровых ИОС, ИОР, ИО, ОНШ', 'Таблицы взаимозаменяемости: полимерные опорные изоляторы ОСК и фарфоровые аналоги ИОС, ИОР, ИО, ОНШ, УСТ, ОНС, АКО; варианты обозначения. Поставки по Украине.', body)
DOCS = [('Podveski.pdf', 'ЭСС.001 ТМ', 'Каталог линейной арматуры: зажимы натяжные клиновые, протекторы защитные спиральные и др. (128 стр., 16 МБ)'),
        ('GOST 28856.pdf', 'ГОСТ 28856-90', 'Изоляторы линейные подвесные стержневые полимерные. Общие технические условия'),
        ('SOY LK.pdf', 'СОУ МПЕ 40.1.51.301:2004', 'Изоляторы линейные подвесные стержневые полимерные. Общие технические условия (Минтопэнерго Украины, 2005; скан)')]
dl = ''.join(f'<tr><td class="code">{escape(n)}</td><td>{escape(d)}</td><td><a href="files/{urllib.parse.quote(f)}" target="_blank" rel="noopener"><i class="fa fa-file-pdf-o"></i> {escape(f)}</a></td></tr>' for f, n, d in DOCS)
body = hero('Документы', 'Документы и стандарты', 'Нормативные документы, на соответствие которым выпускаются полимерные изоляторы.') + f'''
<section><div class="container"><span class="eyebrow">Документы</span><h2 class="section-title">Стандарты</h2>
  <div class="table-wrap"><table class="spec-table"><thead><tr><th>Документ</th><th>Название</th><th>Файл</th></tr></thead><tbody>{dl}</tbody></table></div>
  <p class="note">Для линейных изоляторов <a href="lkc.html">ЛКЦ</a>.</p></div></section>
{CTA}'''
page('docs.html', 'Документы и стандарты: ГОСТ 28856-90, СОУ МПЕ 40.1.51.301', 'ГОСТ 28856-90 и СОУ МПЕ 40.1.51.301:2004 на линейные подвесные стержневые полимерные изоляторы — файлы для скачивания.', body)
print('zamena rows', len(r1), len(r2), '| docs', len(DOCS))
