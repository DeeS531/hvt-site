# -*- coding: utf-8 -*-
"""Генератор страниц группы 3 — ограничители перенапряжения ОПН-П и регистраторы JCQF2/JCQF3.
Данные: tools/opn_data.py (его делает tools/extract_opn.py). Шапка/подвал/head берутся из site/lkc70.html, как в gen_osk.py.
Запуск: cd tools && python3 gen_opn.py"""
import os, re, sys
from html import escape
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import opn_data as D
import site_nav

SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
src = open(f'{SITE}/lkc70.html', encoding='utf-8').read()
head_part = src.split('<body>')[0]
head_part = re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+', '', head_part, flags=re.I)
header = re.search(r'<header class="site-header".*?</header>', src, re.S).group(0)
footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
tail = ('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
        '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')

ASK = 'уточняйте'
def br(t): return re.sub(r'\n+', '<br>', escape(t))
def cell(t): return br(t) if t and t != '—' else '<span class="text-muted">—</span>'
def img(name, alt, cls='opn-drawing'):
    return f'<img class="{cls}" src="images/opn/{escape(name)}" alt="{escape(alt)}" loading="lazy">'

PAGE_BY_ID = {p['id']: p for p in D.PAGES}
ORDER = ['022', '3', '33', '6', '10', '15', '20', '27', '35', '110', '150', '220', '330']
def chip_label(i):
    return {'022': '0,22–0,4 кВ', '33': '3,3 кВ', '27': '27,5 кВ'}.get(i, f'{i} кВ')
def volt_nav(cur):
    items = ''.join(f'<a class="volt-chip{" active" if i == cur else ""}" href="{PAGE_BY_ID[i]["file"]}">{chip_label(i)}</a>' for i in ORDER)
    items += ''.join(f'<a class="volt-chip{" active" if r["id"] == cur else ""}" href="{r["file"]}">{r["title"]}</a>' for r in D.REGS)
    items += '<a class="volt-chip" href="opn.html">Все ОПН</a>'
    return f'<div class="volt-nav">{items}</div>'

def cta(text='Подберём ограничитель под ваши параметры: класс напряжения, наибольшее рабочее напряжение, пропускную способность и климатическое исполнение. Доставка по Украине любым удобным перевозчиком.'):
    return f'''<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен подбор ограничителя?</h2>
  <p class="section-lead mx-auto">{escape(text)}</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''

def page(title, desc, body):
    h = head_part
    h = re.sub(r'<title>.*?</title>', f'<title>{escape(title)} — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(desc)}">', h, count=1)
    hdr = header.replace('href="#', 'href="index.html#').replace('nav-link active', 'nav-link')
    return '<!DOCTYPE html>\n<html lang="ru">\n' + h + '<body>\n\n' + hdr + '\n\n<main>' + body + '\n</main>\n\n' + footer + '\n\n' + tail

def hero(crumbs_tail, h1, lead, cur):
    return f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / {crumbs_tail}</nav>
  <h1>{escape(h1)}</h1>
  <p class="section-lead">{escape(lead)}</p>
  {volt_nav(cur)}
  <div class="d-flex flex-wrap gap-3 mt-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>'''

def crumbs(last): return f'<a href="opn.html">Ограничители перенапряжения ОПН</a> / {last}'

# ---------- фото (с них убраны водяные знаки старого сайта: tools/unwatermark.js) ----------
PHOTOS = {'3': ['OPN3_4.png'], '6': ['OPN6.png'], '10': ['OPN10.png', 'OPN10version2.png', 'OPN10version3.png', 'OPN10version4.png', 'OPN10schem.png'],
          '20': ['OPN20_4.png'], '35': ['OPN35.png', 'OPN35-02.png', 'OPN35-04.png', 'OPN-35-4.png']}
def photos_section(kv, label):
    ph = PHOTOS.get(kv)
    if not ph: return ''
    figs = ''.join(f'<figure class="m-0">{img("photo/" + n, ("Устройство ОПН-П (в разрезе)" if "schem" in n else f"Ограничитель перенапряжения ОПН-П {label} кВ"))}</figure>' for n in ph)
    return f'<section><div class="container"><span class="eyebrow">Фото</span><h2 class="section-title">ОПН-П {escape(label)} кВ</h2><div class="opn-drawings">{figs}</div></div></section>'

# ---------- общие куски ----------
def is_title_line(p):
    return len(p) < 230 and p.startswith(('Ограничитель перенапряжения ОПН', 'Ограничители перенапряжения ОПН', '(', 'Ограничители перенапряжения не линейные'))

def lead_of(pg):
    ps = [p for p in pg.get('intro', []) if is_title_line(p) and not p.startswith('Ограничители перенапряжения не линейные')]
    t = ' '.join(ps[:2]) if ps else ''
    t = re.sub(r'\s+,', ',', re.sub(r'\s+', ' ', t)).replace('( ', '(').replace(' )', ')').strip()
    return t

def spec_rows(spec):
    out = []
    for l, u, v in spec:
        vv = f'<span class="text-muted">{ASK}</span>' if v == ASK else br(v)
        out.append(f'<tr><td>{br(l)}</td><td>{escape(u) or "—"}</td><td class="fw-semibold">{vv}</td></tr>')
    return ''.join(out)

def matrix_table(mx, with_header_group=False):
    """mx: строки; [0] — «Норма для ограничителя», [1] — шапка с типами, далее параметры"""
    head = mx[1]
    th = ''.join(f'<th>{br(c)}</th>' for c in head)
    body = []
    for r in mx[2:]:
        lab = re.sub(r'^\d+\s+', '', r[0])
        lab = lab[:1].upper() + lab[1:]
        lab = lab.replace('UНР', 'Uнр')
        body.append('<tr><td>' + br(lab) + '</td>' + f'<td>{escape(r[1]) or "—"}</td>' + ''.join(f'<td class="fw-semibold">{br(c)}</td>' for c in r[2:]) + '</tr>')
    return f'<div class="table-wrap"><table class="spec-table matrix-table"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'

def notes_block(lines):
    ls = [l.strip() for l in lines if l.strip()]
    if not ls: return ''
    return '<p class="note">' + '<br>'.join(escape(l) for l in ls) + '</p>'

def alias_block(text, title='Варианты обозначения'):
    return f'<section><div class="container"><span class="eyebrow">Обозначения других производителей</span><h2 class="section-title">{escape(title)}</h2><p class="section-lead">Так эти ограничители могут быть обозначены в других каталогах и спецификациях. Если не нашли нужный аналог, свяжитесь с нами, мы подберём его.</p><div class="alias-text">{escape(text)}</div></div></section>'

def reg_link_note():
    return '<p class="note">К ограничителям поставляются регистраторы срабатывания: <a href="jcqf2.html">JCQF2</a>, <a href="jcqf3.html">JCQF3</a>.</p>'

CATCH = ('Полимерные ограничители перенапряжения (разрядники) ОПН-П, ОПНп')

# ---------- страница с моделями ----------
def inter_ru(t): return t.replace('вентильних розрядників', 'вентильных разрядников').replace('колонки', 'колонки')

def models_page(pg):
    kv = pg['id']; ms = pg['models']; n = len(ms)
    title = f'Ограничители перенапряжения ОПН-П {pg["label"]} кВ (ОПНп, разрядники)'
    desc = f'ОПН-П (ОПНп, разрядники) на напряжение {pg["label"]} кВ: {n} моделей, наибольшее рабочее напряжение, пропускная способность, характеристики, варианты обозначения и аналоги, чертежи. Поставки по Украине.'
    flagged = False
    rows = []
    for m in ms:
        bad = m['flags'].get('unr') or m['flags'].get('cap') or any(v == ASK for l, u, v in m['spec'])
        flagged = flagged or bad
        star = ' <span class="text-muted" title="есть расхождения в исходных данных">*</span>' if bad else ''
        extra = []
        if m.get('aliases'): extra.append(escape(m['aliases']))
        if m.get('other_names'): extra.append('Также: ' + escape(', '.join(m['other_names'])))
        if m.get('foreign'): extra.append('Аналоги: ' + escape(', '.join(m['foreign'])))
        if m.get('interchange'): extra.append('Взаимозаменяем с: ' + escape(inter_ru(m['interchange'])))
        alias = '<br>'.join(extra) if extra else '<span class="text-muted">—</span>'
        cap = f'{m["cap"]}' if m.get('cap') else '—'
        rows.append(f'<tr id="r-{m["id"]}"><td class="code"><a href="#d-{m["id"]}">{escape(m["name"])}</a>{star}</td><td>{escape(m["unr"] or "—")}</td><td>{cap}</td><td>{alias}</td></tr>')
    table = ('<div class="table-wrap"><table class="spec-table opn-table"><thead><tr><th>Модель</th><th>Uнр, кВ</th><th>Пропускная способность, А</th>'
             '<th>Варианты обозначения и аналоги</th></tr></thead><tbody>' + '\n'.join(rows) + '</tbody></table></div>')
    cards = []
    for m in ms:
        body = []
        if m.get('aliases'): body.append(f'<p class="mb-2"><b>Варианты обозначения:</b> {escape(m["aliases"])}</p>')
        if m.get('other_names'): body.append(f'<p class="mb-2"><b>Также обозначается:</b> {escape(", ".join(m["other_names"]))}</p>')
        if m.get('foreign'): body.append(f'<p class="mb-2"><b>Аналоги других производителей:</b> {escape(", ".join(m["foreign"]))}</p>')
        if m.get('interchange'): body.append(f'<p class="mb-2"><b>Взаимозаменяем с:</b> {escape(inter_ru(m["interchange"]))}</p>')
        body.append(f'<div class="table-wrap"><table class="spec-table"><thead><tr><th>Показатель</th><th>Ед. изм.</th><th>{escape(m["name"])}</th></tr></thead><tbody>{spec_rows(m["spec"])}</tbody></table></div>')
        if m['images']:
            body.append('<div class="opn-drawings mt-3">' + ''.join(img(i, f'Чертёж {m["name"]}') for i in m['images']) + '</div>')
        cards.append(f'''<details class="spec-details" id="d-{m["id"]}">
  <summary><span class="code">{escape(m["name"])}</span><span class="small text-muted ms-2">характеристики</span></summary>
  <div class="spec-body">
    {"".join(body)}
  </div>
</details>''')
    # вводный текст
    intro = [p for p in pg.get('intro', []) if not is_title_line(p) and not p.startswith(('Наиболее', 'Наимолее'))]
    legend = ''
    for i, p in enumerate(intro):
        if p.endswith('означают:'):
            items = intro[i + 1:]; intro = intro[:i]
            lines = ''.join('<div><b>' + escape(x.split(' — ')[0].strip()) + '</b> — ' + escape(x.split(' — ', 1)[1].rstrip(';. ')) + '</div>' for x in items if ' — ' in x)
            legend = f'<div class="code-block"><div class="mb-2 fw-bold" style="color:var(--navy)">Как читается обозначение</div>{lines}</div>'
            break
    intro_html = ''.join(f'<p>{escape(p)}</p>' for p in intro)
    fig = ''
    if pg.get('hero'): fig = ''.join(img(h, f'Чертёж ОПН-П {pg["label"]} кВ') for h in pg['hero'])
    left = intro_html or '<p>Ограничители перенапряжения ОПН-П (ОПНп) предназначены для защиты электрооборудования от грозовых и коммутационных перенапряжений.</p>'
    side = legend + fig
    top = (f'<section><div class="container"><div class="row g-4 mx-0"><div class="col-lg-7"><span class="eyebrow">Описание</span><h2 class="section-title">ОПН-П {escape(pg["label"])} кВ</h2>{left}</div>'
           f'<div class="col-lg-5">{side}</div></div></div></section>') if (intro_html or side) else ''
    # уникальные примечания про регистраторы
    seen = []
    for m in ms:
        for t in m['notes']:
            if t not in seen: seen.append(t)
    notes = ''.join(f'<p class="note">{escape(t)}</p>' for t in seen)
    custom = ''
    if pg.get('custom_matrix'):
        cm = pg['custom_matrix']
        custom = ('<section><div class="container"><span class="eyebrow">Под требования заказчика</span><h2 class="section-title">Исполнения по заказу</h2>'
                  '<p class="section-lead">Возможно изготовление ограничителей под определённые требования заказчика. «А» — наибольшее длительно допустимое рабочее напряжение; Х1…Х4 — числовые значения, зависящие от А.</p>'
                  + matrix_table(cm) + '</div></section>')
    var = alias_block(pg['variants_text']) if pg.get('variants_text') else ''
    fl = '<p class="note">* По этой модели в исходных данных есть расхождения; спорные значения в карточке отмечены «уточняйте». Свяжитесь с нами для точных данных.</p>' if flagged else ''
    body = hero(crumbs(f'{pg["label"]} кВ'), f'Ограничители перенапряжения ОПН-П {pg["label"]} кВ', lead_of(pg) or f'{CATCH} на напряжение {pg["label"]} кВ.', kv) + f'''
{top}
{photos_section(kv, pg["label"])}
<section class="section-soft"><div class="container">
  <span class="eyebrow">Модели</span><h2 class="section-title">Модели ОПН-П на {escape(pg["label"])} кВ</h2>
  <p class="section-lead">Моделей: {n}. Название модели — ссылка на технические характеристики и чертёж. Uнр — наибольшее длительно допустимое рабочее напряжение.</p>
  {table}
  {fl}{notes}{reg_link_note()}
</div></section>
<section class="section-soft"><div class="container"><span class="eyebrow">Характеристики</span><h2 class="section-title">Технические характеристики моделей</h2><p class="section-lead">Раскройте нужную модель, чтобы увидеть параметры.</p>
{chr(10).join(cards)}
</div></section>
{custom}{var}
{cta()}'''
    return page(title, desc, body)

# ---------- матричная страница ----------
def matrix_page(pg):
    kv = pg['id']
    title = f'Ограничители перенапряжения ОПН-П {kv} кВ (ОПНп, разрядники)'
    desc = f'ОПН-П (ОПНп, разрядники) {kv} кВ: технические характеристики, типы по пропускной способности, варианты обозначения. Поставки по Украине.'
    fig = ''.join(img(h, f'Чертёж ОПН-П {kv} кВ') for h in pg.get('hero', []))
    note = notes_block(pg.get('matrix_note', []))
    var = alias_block(pg['variants_text']) if pg.get('variants_text') else ''
    body = hero(crumbs(f'{kv} кВ'), f'Ограничители перенапряжения ОПН-П {kv} кВ', lead_of(pg) or f'{CATCH} на напряжение {kv} кВ.', kv) + f'''
<section><div class="container"><div class="row g-4 mx-0 align-items-start">
  <div class="col-lg-8"><span class="eyebrow">Описание</span><h2 class="section-title">ОПН-П {kv} кВ</h2>
  <p>Ограничители ОПН-П {kv} кВ выпускаются в нескольких исполнениях по наибольшему длительно допустимому рабочему напряжению и пропускной способности. В таблице ниже приведены типовые исполнения; значения «А» и Х1…Х4 определяются по требованию заказчика.</p></div>
  <div class="col-lg-4">{fig}</div>
</div></div></section>
{photos_section(kv, kv)}
<section class="section-soft"><div class="container">
  <span class="eyebrow">Характеристики</span><h2 class="section-title">Технические характеристики</h2>
  {matrix_table(pg['matrix'])}
  {note}{reg_link_note()}
</div></section>
{var}
{cta()}'''
    return page(title, desc, body)

# ---------- 0,22 / 0,4 кВ ----------
def raw_page(pg):
    t1, t2, t3 = pg['tables']
    def tbl(g, first_col_code=True):
        head = ''.join(f'<th>{br(c)}</th>' for c in g[0])
        rows = ''.join('<tr>' + ''.join((f'<td class="code">{br(c)}</td>' if (i == 0 and first_col_code) else f'<td>{br(c)}</td>') for i, c in enumerate(r)) + '</tr>' for r in g[1:])
        return f'<div class="table-wrap"><table class="spec-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    t3 = [[c.replace('Длинна', 'Длина') for c in r] for r in t3]
    varp = next((p for p in pg['paras'] if p.startswith('Варианты обозначения')), '')
    var = alias_block(re.sub(r'^Варианты обозначения[^:]*:\s*', '', varp)) if varp else ''
    title = 'Ограничители перенапряжения ОПН-П 0,22–0,4 кВ (ОПНп, разрядники)'
    desc = 'ОПН-П на напряжение 0,22, 0,38 и 0,4 кВ, а также ОПН-П-0,28 и 0,44 кВ с прокалывающим зажимом: таблицы характеристик, варианты обозначения, чертежи. Поставки по Украине.'
    body = hero(crumbs('0,22–0,4 кВ'), 'Ограничители перенапряжения ОПН-П 0,22 / 0,38 / 0,4 кВ', 'Ограничители перенапряжения ОПН-П-0,22 кВ, ОПН-П-0,38 кВ, ОПН-П-0,4 кВ (ОПНп, ОПН) для сетей переменного тока.', '022') + f'''
<section><div class="container"><div class="row g-4 mx-0 align-items-start">
  <div class="col-lg-8"><span class="eyebrow">Характеристики</span><h2 class="section-title">ОПН-П 0,22 кВ и 0,38 / 0,4 кВ</h2>
  <h3 class="h5 mt-3">ОПН-П-0,22 кВ</h3>{tbl(t1)}
  <h3 class="h5 mt-4">ОПН-П-0,38 кВ / 0,4 кВ</h3>{tbl(t2)}</div>
  <div class="col-lg-4">{img(pg['hero'][0], 'Габаритный чертёж ОПН-П 0,22 кВ')}</div>
</div></div></section>
<section class="section-soft"><div class="container"><div class="row g-4 mx-0 align-items-start">
  <div class="col-lg-8"><span class="eyebrow">С прокалывающим зажимом</span><h2 class="section-title">ОПН-П-0,28 кВ и ОПН-П-0,44 кВ</h2>
  <p>Ограничители перенапряжения с прокалывающим зажимом ОПН-П-0,28 кВ, ОПН-П-0,44 кВ (ОПНп, ОПН) для сетей переменного тока.</p>{tbl(t3, first_col_code=False)}</div>
  <div class="col-lg-4">{img(pg['hero'][1], 'Схема установки ОПН-П-0,28 / 0,44 кВ с прокалывающим зажимом на СИП')}</div>
</div></div></section>
{var}
{cta()}'''
    return page(title, desc, body)

# ---------- 3,3 и 27,5 кВ: данных на старом сайте нет ----------
def stub_page(pg):
    kv = pg['label']
    title = f'Ограничители перенапряжения ОПН-П {kv} кВ'
    desc = f'ОПН-П (ОПНп) на напряжение {kv} кВ: технические данные и цена по запросу. Поставки по Украине.'
    body = hero(crumbs(f'{kv} кВ'), f'Ограничители перенапряжения ОПН-П {kv} кВ', f'{CATCH} на напряжение {kv} кВ.', pg['id']) + f'''
<section><div class="container"><div class="row g-4 mx-0"><div class="col-lg-8">
  <span class="eyebrow">Информация</span><h2 class="section-title">Технические данные — по запросу</h2>
  <p>Характеристики и исполнения ОПН-П на {escape(kv)} кВ предоставляются по запросу. Оставьте заявку или свяжитесь с нами — подберём ограничитель под ваши параметры и вышлем технические данные.</p>
  <p>Типовые исполнения других классов напряжения смотрите в <a href="opn.html">каталоге ОПН</a>.</p>
</div></div></div></section>
{cta()}'''
    return page(title, desc, body)

# ---------- регистраторы ----------
def reg_page(r):
    t = r['title']
    title = f'Регистратор срабатывания ограничителей перенапряжения {t}'
    desc = f'Регистратор срабатывания {t} для ОПН на класс напряжения 6–330 кВ: назначение, условия эксплуатации, технические характеристики, чертёж, схема монтажа. Поставки по Украине.'
    ps = list(r['paras'])
    html = []; i = 0
    while i < len(ps):
        p = ps[i]
        if p.startswith('- '):
            items = []
            while i < len(ps) and ps[i].startswith('- '): items.append(ps[i][2:].strip()); i += 1
            html.append('<ul>' + ''.join(f'<li>{escape(x)}</li>' for x in items) + '</ul>'); continue
        if p.endswith(':') and i + 1 < len(ps) and len(ps[i + 1]) < 130 and ps[i + 1].rstrip().endswith((';', '.')) and not ps[i + 1].startswith('- '):
            html.append(f'<h3 class="h5 mt-4">{escape(p.rstrip(":"))}</h3>'); i += 1
            items = []
            while i < len(ps) and len(ps[i]) < 130 and ps[i].rstrip().endswith((';', '.')) and not ps[i].startswith('- '):
                items.append(ps[i].rstrip(';. ')); i += 1
                if not ps[i - 1].rstrip().endswith(';'): break
            html.append('<ul>' + ''.join(f'<li>{escape(x)}</li>' for x in items) + '</ul>'); continue
        if p.startswith(('ОПН JCQF', 'Схема монтажа', 'Ограничители перенапряжений 35кВ могут')):
            html.append(f'<p class="note">{escape(p)}</p>'); i += 1; continue
        html.append(f'<p>{escape(p)}</p>'); i += 1
    imgs = ''.join(f'<figure class="mb-3">{img(n, f"{t}: чертёж и схема")}</figure>' for n in r['images'])
    body = hero(crumbs(t), f'Регистратор срабатывания {t}', f'Регистратор срабатывания ограничителей перенапряжения {t}: индикация тока проводимости и счёт срабатываний ОПН на класс напряжения 6–330 кВ.', r['id']) + f'''
<section><div class="container"><div class="row g-4 mx-0 align-items-start">
  <div class="col-lg-7"><span class="eyebrow">Описание</span><h2 class="section-title">{escape(t)}</h2>{"".join(html)}</div>
  <div class="col-lg-5">{imgs}</div>
</div></div></section>
{cta('Регистратор поставляется отдельно или в комплекте с ограничителем перенапряжения. Подберём исполнение под ваш класс напряжения.')}'''
    return page(title, desc, body)

# ---------- общая страница группы ----------
def main_page():
    total = sum(len(p.get('models', [])) for p in D.PAGES)
    cards = []
    for i in ORDER:
        pg = PAGE_BY_ID[i]
        cnt = {'models': f'{len(pg.get("models", []))} моделей', 'matrix': 'типовые исполнения', 'raw': 'типовые исполнения', 'stub': 'по запросу'}[pg['kind']]
        cards.append(f'<div class="col-6 col-md-4"><a class="volt-card" href="{pg["file"]}"><span class="volt-num">{escape(chip_label(i).replace(" кВ", ""))}</span><span class="volt-unit">кВ</span><span class="volt-cnt">{cnt}</span></a></div>')
    for r in D.REGS:
        cards.append(f'<div class="col-6 col-md-4"><a class="volt-card" href="{r["file"]}"><span class="volt-num" style="font-size:1.5rem">{r["title"]}</span><span class="volt-unit">регистратор</span><span class="volt-cnt">срабатывания ОПН</span></a></div>')
    paras = ''.join(f'<p>{escape(p)}</p>' for p in D.CATEGORY['paras'])
    adv = ''.join(f'<li>{escape(a)}</li>' for a in D.CATEGORY['adv'])
    vid = D.CATEGORY.get('video')
    video = (f'<div class="mt-5"><span class="eyebrow">Видео</span><h2 class="section-title">Испытание ОПН-П-150 кВ на взрывобезопасность</h2>'
             f'<div class="ratio ratio-16x9" style="max-width:760px"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="Испытание ОПН-П-150 кВ на взрывобезопасность" loading="lazy" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div></div>') if vid else ''
    title = 'Ограничители перенапряжения ОПН-П (ОПНп, разрядники) 0,22–330 кВ'
    desc = f'Полимерные ограничители перенапряжения ОПН-П (ОПНп, разрядники) на напряжение от 0,22 до 330 кВ: каталог по классам напряжения ({total} моделей с характеристиками), регистраторы срабатывания JCQF2 и JCQF3. Поставки по Украине.'
    body = f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / Ограничители перенапряжения ОПН</nav>
  <h1>Ограничители перенапряжения ОПН-П (ОПНп, разрядники)</h1>
  <p class="section-lead">Напряжение от 0,22 до 330 кВ. В каталоге {total} моделей с техническими характеристиками, а также регистраторы срабатывания JCQF2 и JCQF3.</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section><div class="container"><div class="row g-4"><div class="col-lg-3">{site_nav.side_nav('opn.html')}</div><div class="col-lg-9">
  <span class="eyebrow">Выберите напряжение</span><h2 class="section-title">Каталог по классам напряжения</h2>
  <div class="row g-3 mb-5">{"".join(cards)}</div>
  <div class="row g-4 mx-0">
    <div class="col-xl-7"><span class="eyebrow">Описание</span><h2 class="section-title">Ограничители ОПН-П</h2>{paras}</div>
    <div class="col-xl-5"><div class="code-block"><div class="mb-2 fw-bold" style="color:var(--navy)">Преимущества ОПНп</div><ul class="mb-0 ps-3">{adv}</ul></div></div>
  </div>
  {video}
</div></div></div></section>
{cta()}'''
    return page(title, desc, body)

# ---------- запись ----------
KIND = {'models': models_page, 'matrix': matrix_page, 'raw': raw_page, 'stub': stub_page}
for pg in D.PAGES:
    open(f'{SITE}/{pg["file"]}', 'w', encoding='utf-8').write(KIND[pg['kind']](pg))
for r in D.REGS:
    open(f'{SITE}/{r["file"]}', 'w', encoding='utf-8').write(reg_page(r))
open(f'{SITE}/opn.html', 'w', encoding='utf-8').write(main_page())
print('pages done:', len(D.PAGES) + len(D.REGS) + 1, '| models', sum(len(p.get('models', [])) for p in D.PAGES))
