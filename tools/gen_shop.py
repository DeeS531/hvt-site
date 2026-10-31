# -*- coding: utf-8 -*-
"""Группа 7 — шинные опоры ШОП/ШО: shop.html (группа), shop{10,35,110,150}.html, заглушки shop{20,220,330}.html. Данные: shop_data.py.
Запуск: cd tools && python3 gen_shop.py"""
import os, re, sys
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import site_nav, shop_data as D
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head0 = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', src.split('<body>')[0], flags=re.I)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0).replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')
BADIMG = set()     # исходные картинки (с водяными знаками старого сайта) возвращены по решению клиента
def br(t): return re.sub(r'\n+', '<br>', escape(t))
def img(n, alt): return f'<img class="opn-drawing" src="images/shop/{escape(n)}" alt="{escape(alt)}" loading="lazy">'
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
def cta(t='Подберём шинную опору по классу напряжения, степени загрязнённости, диаметру и марке провода, установочным размерам. Доставка по Украине любым удобным перевозчиком.'):
    return f'''<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен подбор шинной опоры?</h2>
  <p class="section-lead mx-auto">{escape(t)}</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''
def side(cur): return site_nav.side_nav('shop.html', cur)
def spec_tbl(spec, head=('Параметр', 'Значение')):
    rows = ''.join(f'<tr><td>{escape(l)}</td><td class="fw-semibold">{br(v)}</td></tr>' for l, v in spec)
    return f'<div class="table-wrap"><table class="spec-table"><thead><tr><th>{head[0]}</th><th>{head[1]}</th></tr></thead><tbody>{rows}</tbody></table></div>'
def legend(lines):
    lg = ''.join(f'<div><b>{escape(re.split(r" [—-] ", x, 1)[0].strip())}</b> — {escape(re.split(r" [—-] ", x, 1)[1].strip())}</div>' for x in lines if re.search(r' [—-] ', x))
    return f'<div class="code-block"><div class="mb-2 fw-bold" style="color:var(--navy)">Как читается обозначение</div>{lg}</div>' if lg else ''

def vol_page(pg):
    kv = pg['kv']
    n = sum(len(g['items']) for g in pg['groups'])
    title = f'Шинные опоры ШОП-{kv}, ШО-{kv} УХЛ1'
    desc = f'Шинные опоры ШОП-{kv} с полимерной изоляцией и ШО-{kv} на напряжение {kv} кВ: ' + (f'{n} исполнений, ' if n else '') + 'технические характеристики, расшифровка обозначения, диаметр и марка провода, чертежи. Поставки по Украине.'
    drawings = sorted({s['drawing'] for g in pg['groups'] for it in g['items'] for s in [D.SUBS[it['sub']]] if s['drawing']})
    renders = []
    for g in pg['groups']:
        for it in g['items']:
            for im in D.SUBS[it['sub']]['images']:
                if im not in renders and not re.search(r'-5', im) and im not in BADIMG: renders.append(im)
    photos = ''.join(f'<figure class="m-0">{img(i, f"Шинная опора ШОП-{kv}")}</figure>' for i in renders)
    groups = []; cards = []
    for g in pg['groups']:
        rows = ''
        for it in g['items']:
            d = it['desc'] or ''
            typ = 'Подвесное' if d.startswith('Подвесное') else ('Опорное' if d.startswith('Опорное') else '—')
            wires = (re.search(r'(\d) провод', d) or [None, '—'])[1]
            fl = (re.search(r'фланец (\d+)', d) or [None, '—'])[1]
            rows += f'<tr><td class="code"><a href="#d-{escape(it["sub"][:-5])}">{escape(it["name"])}</a></td><td>{typ}</td><td>{wires}</td><td>{fl}</td></tr>'
            s = D.SUBS[it['sub']]
            body = [spec_tbl(s['spec'])]
            for ptxt in s['paras'][:1] + s['paras'][2:3]: body.insert(0, f'<p class="mb-2">{escape(ptxt)}</p>') if False else None
            intro = ''.join(f'<p class="mb-2">{escape(x)}</p>' for x in (s['paras'][:1] + s['paras'][2:3]))
            if s['models']: intro += f'<p class="mb-2"><b>Типы:</b> {escape(s["models"].split("изоляцией", 1)[-1].strip())}</p>'
            tb = ''
            if s['table']:
                th = ''.join(f'<th>{escape(c)}</th>' for c in s['table'][0])
                tr = ''.join('<tr>' + ''.join(f'<td>{br(c)}</td>' for c in r) + '</tr>' for r in s['table'][1:])
                tb = f'<h3 class="h6 mt-4">Исполнения и провода</h3><div class="table-wrap"><table class="spec-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
            wires_t = f'<p class="mt-3 mb-2"><b>Типы проводов:</b> {escape(s["wires"])}</p>' if s['wires'] else ''
            var = f'<p class="mb-2"><b>Возможные варианты обозначения:</b> {escape(s["variants"])}</p>' if s['variants'] else ''
            nt = ''.join(f'<p class="note mb-1">{escape(x)}</p>' for x in s['notes'])
            dr = f'<div class="opn-drawings mt-3">{img(s["drawing"], "Чертёж " + it["name"])}</div>' if s['drawing'] else ''
            cards.append(f'<details class="spec-details" id="d-{escape(it["sub"][:-5])}"><summary><span class="code">{escape(it["name"])}</span><span class="small text-muted ms-2">{escape(d)}, СЗА {g["sza"]}</span></summary><div class="spec-body">{intro}{body[0]}{tb}{wires_t}{var}{nt}{dr}</div></details>')
        groups.append(f'<h3 class="h5 mt-4">СЗА {g["sza"]} — {len(g["items"])} исполнений</h3><div class="table-wrap"><table class="spec-table"><thead><tr><th>Исполнение</th><th>Тип</th><th>Проводов</th><th>Фланец</th></tr></thead><tbody>{rows}</tbody></table></div>')
    models = ('<span class="eyebrow">Модели</span><h2 class="section-title">Исполнения шинных опор</h2><p class="section-lead">Название исполнения — ссылка на характеристики и чертёж. СЗА — степень загрязнённости атмосферы.</p>' + ''.join(groups)) if groups else ''
    det = f'<section class="section-soft"><div class="container"><span class="eyebrow">Характеристики</span><h2 class="section-title">Технические характеристики исполнений</h2><p class="section-lead">Раскройте нужное исполнение, чтобы увидеть параметры.</p>{"".join(cards)}</div></section>' if cards else ''
    body = hero(f'<a href="shop.html">Шинные опоры</a> / {kv} кВ', f'Шинные опоры ШОП-{kv}, ШО-{kv} УХЛ1', f'Шинные опоры на напряжение {kv} кВ для крепления, фиксации и электрической изоляции токоведущих шин и проводов в распределительных устройствах.') + f'''
<section><div class="container"><div class="row g-4"><div class="col-lg-3">{side(f"shop{kv}.html")}</div><div class="col-lg-9">
  <span class="eyebrow">Общие данные</span><h2 class="section-title">ШОП-{kv}, ШО-{kv} УХЛ1</h2>
  <div class="row g-4 mx-0 align-items-start"><div class="col-xl-7">{spec_tbl(pg["spec"])}<p class="note">Тип зажимаемого провода и другие параметры зависят от конфигурации шинной опоры.</p></div><div class="col-xl-5">{legend(pg["legend"])}</div></div>
  {('<div class="opn-drawings mt-4">' + photos + '</div>') if photos else ''}
  <div class="mt-5">{models}</div>
</div></div></div></section>
{det}
{cta()}'''
    page(f'shop{kv}.html', title, desc, body)

def stub_page(kv, text):
    title = f'Шинные опоры ШОП-{kv}, ШО-{kv} УХЛ1'
    body = hero(f'<a href="shop.html">Шинные опоры</a> / {kv} кВ', title, f'Шинные опоры на напряжение {kv} кВ.') + f'''
<section><div class="container"><div class="row g-4"><div class="col-lg-3">{side(f"shop{kv}.html")}</div><div class="col-lg-9">
  <span class="eyebrow">Информация</span><h2 class="section-title">Технические данные — по запросу</h2>
  <p>{escape(text)}</p><p>Характеристики и исполнения шинных опор {kv} кВ предоставляются по запросу. Оставьте заявку или свяжитесь с нами — подберём шинную опору под ваши параметры. Другие классы напряжения смотрите в <a href="shop.html">каталоге шинных опор</a>.</p>
</div></div></div></section>
{cta()}'''
    page(f'shop{kv}.html', title, f'Шинные опоры ШОП-{kv}, ШО-{kv} на напряжение {kv} кВ: технические данные и цена по запросу. Поставки по Украине.', body)

def group_page():
    cards = ''
    ex = {p['kv']: sum(len(g['items']) for g in p['groups']) for p in D.PAGES}
    for c in D.GROUP['cards']:
        kv = c['kv']; cnt = f'{ex[kv]} исполнений' if ex.get(kv) else ('характеристики' if kv in ex else 'по запросу')
        cards += f'<div class="col-6 col-md-4"><a class="volt-card" href="shop{kv}.html"><span class="volt-num">{kv}</span><span class="volt-unit">кВ</span><span class="volt-cnt">{cnt}</span></a></div>'
    paras = ''.join(f'<p>{escape(p)}</p>' for p in D.GROUP['paras'])
    body = hero('Шинные опоры', 'Шинные опоры ШОП и ШО 10–330 кВ', 'Шинные опоры ШОП с полимерной изоляцией и ШО с фарфоровой изоляцией для крепления, фиксации и электрической изоляции токоведущих шин и проводов.') + f'''
<section><div class="container"><div class="row g-4"><div class="col-lg-3">{side(None)}</div><div class="col-lg-9">
  <span class="eyebrow">Выберите напряжение</span><h2 class="section-title">Каталог по классам напряжения</h2>
  <div class="row g-3 mb-5">{cards}</div>
  <span class="eyebrow">Описание</span><h2 class="section-title">Шинные опоры ШОП и ШО</h2>{paras}
</div></div></div></section>
{cta()}'''
    page('shop.html', 'Шинные опоры ШОП и ШО 10–330 кВ', 'Шинные опоры ШОП (полимерная изоляция) и ШО (фарфоровая изоляция) на напряжение 10, 20, 35, 110, 150, 220, 330 кВ: каталог, характеристики, расшифровка обозначения. Поставки по Украине.', body)

for pg in D.PAGES: vol_page(pg)
done = {p['kv'] for p in D.PAGES}
for c in D.GROUP['cards']:
    if c['kv'] not in done: stub_page(c['kv'], c.get('text', ''))
group_page()
print('shop pages done:', len(D.PAGES), '+ заглушки', len(D.GROUP['cards']) - len(done), '+ группа')
