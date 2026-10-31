# -*- coding: utf-8 -*-
import os, re, sys, urllib.parse
from html import escape
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import osk_data as D
import site_nav

SITE=os.path.normpath(os.path.join(HERE,'..','site'))
src=open(f'{SITE}/lkc70.html',encoding='utf-8').read()
head_part=src.split('<body>')[0]
head_part=re.sub(r'^\s*(<!DOCTYPE html>\s*<html[^>]*>\s*)+','',head_part,flags=re.I)
header=re.search(r'<header class="site-header".*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="site-footer">.*?</footer>',src,re.S).group(0)
tail=('<button class="to-top" id="toTop" aria-label="Наверх"><i class="fa fa-angle-up fa-lg"></i></button>\n\n'
      '<script src="js/vendor/bootstrap.bundle.min.js"></script>\n<script src="js/i18n.js"></script>\n<script src="js/main.js"></script>\n</body>\n</html>\n')

def pdf_href(n): return 'pdf/'+urllib.parse.quote(n)
def pdf_links(lst):
    if not lst: return '<span class="text-muted">—</span>'
    return '<br>'.join(f'<a href="{pdf_href(p)}" target="_blank" rel="noopener"><i class="fa fa-file-pdf-o"></i> {escape(p)}</a>' for p in lst)
def cell(t): return escape(t) if t and t!='—' else '<span class="text-muted">—</span>'
def slug(m):
    base=re.sub(r'[^0-9A-Za-z_]+','-',m.replace('ОСК','osk').replace(',','_').replace('/','-')).strip('-').lower()
    return base
def dedupe_alias(s):
    items=re.split(r'\s(?=(?:И?ОСК|Изолятор опорный)\s)',s.strip())
    seen=[];out=[]
    for i in items:
        i=i.strip()
        if i and i not in seen: seen.append(i);out.append(i)
    return ', '.join(out)

LEGEND='''<div class="code-block">
  <div class="mb-2 fw-bold" style="color:var(--navy)">Как читается обозначение</div>
  <div><b>О</b> — опорный</div>
  <div><b>С</b> — стержневой</div>
  <div><b>К</b> — кремнийорганическая резина (материал оболочки)</div>
  <div><b>4 … 30</b> — минимальная разрушающая сила при изгибе, кН</div>
  <div><b>10 … 220</b> — номинальное напряжение, кВ</div>
  <div><b>80 … 950</b> — выдерживаемое напряжение грозового импульса, кВ</div>
  <div><b>1 … 3</b> — район по степени загрязнённости атмосферы (СЗА)</div>
  <div><b>01, 02 …</b> — конструктивное исполнение</div>
</div>
<div class="example-box mt-3"><div class="small text-muted mb-1">Пример</div>
ОСК 8-35/195-3-01: разрушающая сила на изгиб 8 кН, напряжение 35 кВ, грозовой импульс 195 кВ, район СЗА 3, исполнение 01.</div>'''

def table(rows, with_note=False):
    out=['<div class="table-wrap"><table class="spec-table osk-table"><thead><tr><th>Модель</th><th>Строит. высота, мм</th><th>Фарфоровый аналог</th><th>Варианты обозначения</th><th>Чертёж</th></tr></thead><tbody>']
    for r in rows:
        m,h,f,p,pdfs=r[:5]; note=r[5] if len(r)>5 else ''
        has=m in D.S
        name=escape(m)
        rid=slug(m)+('-b' if 'второе' in m else '')
        if has: name=f'<a href="#d-{slug(m)}">{name}</a>'
        if note: name+=f'<div class="small text-muted mt-1">{escape(note)}</div>'
        out.append(f'<tr id="r-{rid}"><td class="code">{name}</td><td>{cell(h)}</td><td>{cell(f)}</td><td>{cell(p)}</td><td>{pdf_links(pdfs)}</td></tr>')
    out.append('</tbody></table></div>')
    return '\n'.join(out)

def details(rows):
    cards=[]
    for r in rows:
        m=r[0]
        if m not in D.S: continue
        s=D.S[m]
        trs=[('Номинальное напряжение, кВ',s['kv']),
             ('Мин. разрушающая сила при изгибе, кН',s['force'])]
        if s.get('sza'): trs.append(('Степень загрязнения атмосферы (ГОСТ 9920)',s['sza']))
        trs.append(('Грозовой импульс 1,2/50, кВ',s['light']))
        trs.append(('Промышленная частота, кВ: в сухом состоянии',s['dry']))
        trs.append(('Промышленная частота, кВ: под дождём',s['wet']))
        if s.get('mean_dry'): trs.append(('Среднее разрядное напряжение пром. частоты в сухом состоянии, кВ',s['mean_dry']))
        if s.get('light50'): trs.append(('50%-е разрядное напряжение полного грозового импульса, кВ',s['light50']))
        trs.append(('50%-е разрядное напряжение в загрязнённом и увлажнённом состоянии, кВ (уд. проводимость)',s['poll']))
        if s.get('torque'): trs.append(('Мин. разрушающий крутящий момент, кН·м',s['torque']))
        trs.append(('Длина пути утечки, мм',s['creep']))
        trs.append(('Уровень частичных разрядов, пКл','≤ 2'))
        if s.get('mass'): trs.append(('Масса, кг, не более',s['mass']))
        trs.append(('Климатическое исполнение (ГОСТ 15150)',s['climate']))
        rows_html=''.join(f'<tr><td>{escape(a)}</td><td class="fw-semibold">{escape(b)}</td></tr>' for a,b in trs)
        fa=r[2]; po=r[3]
        extra=''
        if fa and fa!='—': extra+=f'<p class="mb-2"><b>Заменяет фарфоровые:</b> {escape(fa)}</p>'
        if po and po!='—': extra+=f'<p class="mb-2"><b>Варианты обозначения полимерных аналогов:</b> {escape(po)}</p>'
        cards.append(f'''<details class="spec-details" id="d-{slug(m)}">
  <summary><span class="code">{escape(m)} УХЛ{escape(s['climate'][-1])}</span><span class="small text-muted ms-2">характеристики</span></summary>
  <div class="spec-body">
    <p class="mb-2">Опорный стержневой полимерный изолятор для изоляции и крепления токоведущих частей в электрических аппаратах, распределительных устройствах электростанций и подстанций переменного тока. Рабочий диапазон температур от −60 до +50 °C, высота установки не более 1000 м над уровнем моря. Соответствует СОУ МПЕ 40.1.51.302:2006.</p>
    {extra}
    <div class="table-wrap"><table class="spec-table"><thead><tr><th>Показатель</th><th>{escape(m)}</th></tr></thead><tbody>{rows_html}</tbody></table></div>
    <p class="mt-3 mb-0">{pdf_links(r[4])}</p>
  </div>
</details>''')
    if not cards: return ''
    return '<section class="section-soft"><div class="container"><span class="eyebrow">Характеристики</span><h2 class="section-title">Технические характеристики моделей</h2><p class="section-lead">Раскройте нужную модель, чтобы увидеть параметры.</p>'+'\n'.join(cards)+'</div></section>'

def alias_block(s):
    return f'<section><div class="container"><span class="eyebrow">Обозначения других производителей</span><h2 class="section-title">Альтернативные названия</h2><p class="section-lead">Так эти изоляторы могут быть обозначены в других каталогах и спецификациях. Если не нашли нужный аналог, свяжитесь с нами, мы подберём его.</p><div class="alias-text">{escape(dedupe_alias(s))}</div></div></section>'

def cta():
    return '''<section class="section-dark"><div class="container text-center">
  <h2 class="section-title">Нужен подбор или цена завода?</h2>
  <p class="section-lead mx-auto">Минимальный заказ — от 1 штуки. Доставка любым удобным перевозчиком. Подберём изолятор под вашу замену фарфоровых.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost" href="https://t.me/High_Voltage_Technologies" target="_blank" rel="noopener"><i class="fa fa-telegram"></i> Telegram</a>
  </div></div></section>'''

def page(title, desc, body):
    h=head_part
    h=re.sub(r'<title>.*?</title>',f'<title>{escape(title)} — ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ</title>',h,count=1)
    h=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{escape(desc)}">',h,count=1)
    hdr=header.replace('href="#','href="index.html#').replace('nav-link active','nav-link')
    return '<!DOCTYPE html>\n<html lang="ru">\n'+h+'<body>\n\n'+hdr+'\n\n<main>'+body+'\n</main>\n\n'+footer+'\n\n'+tail

DESC_TXT='''<p>Изоляторы опорные стержневые полимерные ОСК (альтернативные названия ИОСК, ИОС, ИО, ОНШ) с цельнолитой защитной оболочкой пришли на смену устаревшим фарфоровым изоляторам ИОС, УСТ, ОНШ, ИШТ, ОНС, АКО более 12 лет назад. Они отличаются более высокими качественно-эксплуатационными характеристиками, надёжностью, лёгкостью монтажа и обслуживания.</p>
<p>Изоляторы ОСК не нуждаются в очистке изоляционной оболочки. За счёт малого веса по сравнению с фарфоровыми аналогами их можно монтировать без крановой техники. Они стойки к вандализму и к механическим воздействиям (дробь, осколки и т. п.).</p>
<p>ОСК полностью взаимозаменяемы с фарфоровыми аналогами, поэтому замену можно выполнять без изменения конструкции оборудования. Малый вес позволяет экономить на металлоконструкциях при производстве разъединителей и при строительстве фундаментов подстанционного оборудования.</p>
<p>Опорные стержневые изоляторы ОСК на напряжение от 10 до 220 кВ более 20 лет эксплуатируются на объектах ДТЭК Энерго, Укрэнерго, Укрзализныци, а также в ведущих облэнерго Украины. Гарантийный срок эксплуатации — от 5 до 10 лет.</p>
<p>Производственная база располагает собственной электромеханической лабораторией: каждый изолятор проходит механические и электрические испытания. Партнёрами предприятия являются ведущие в Украине производители арматуры, поэтому возможна комплексная поставка необходимых материалов (зажимы, контакторы и т. д.).</p>'''

VOLTS=[('10','osk10.html'),('20','osk20.html'),('35','osk35.html'),('110','osk110.html'),('150','osk150.html'),('220','osk220.html')]
def volt_nav(cur):
    items=''.join(f'<a class="volt-chip{" active" if v==cur else ""}" href="{u}">{v} кВ</a>' for v,u in VOLTS)
    return f'<div class="volt-nav">{items}<a class="volt-chip" href="osk.html">Все ОСК</a></div>'

def volt_page(kv, rows, alias=None, lead_extra=''):
    n=len(rows); wd=sum(1 for r in rows if r[0] in D.S)
    title=f'Опорные изоляторы ОСК (ИОСК) {kv} кВ'
    desc=f'Опорные стержневые полимерные изоляторы ОСК (ИОСК, ИОС, ИО, ОНШ) на напряжение {kv} кВ: модели, строительная высота, фарфоровые аналоги, варианты обозначения, чертежи. Поставки по Украине, цена завода.'
    body=f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / <a href="osk.html">Опорные изоляторы ОСК</a> / {kv} кВ</nav>
  <h1>Опорные изоляторы ОСК {kv} кВ</h1>
  <p class="section-lead">Изоляторы опорные стержневые полимерные ОСК (альтернативные названия ИОСК, ИОС, ИО, ОНШ) на напряжение {kv} кВ. {lead_extra}</p>
  {volt_nav(kv)}
  <div class="d-flex flex-wrap gap-3 mt-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section><div class="container"><div class="row g-4 mx-0">
  <div class="col-lg-7"><span class="eyebrow">Описание</span><h2 class="section-title">Изоляторы ОСК</h2>{DESC_TXT}</div>
  <div class="col-lg-5">{LEGEND}</div>
</div></div></section>
<section class="section-soft"><div class="container">
  <span class="eyebrow">Модели</span><h2 class="section-title">Модели ОСК на {kv} кВ</h2>
  <p class="section-lead">Моделей: {n}. Для {wd} из них доступны подробные технические характеристики (название модели — ссылка).</p>
  {table(rows)}
  <p class="note">Строительная высота и другие размеры могут уточняться по чертежу. Если нужной модели нет в списке, свяжитесь с нами — подберём аналог.</p>
</div></section>
{details(rows)}
{alias_block(alias) if alias else ''}
{cta()}'''
    return page(title,desc,body)

open(f'{SITE}/osk10.html','w',encoding='utf-8').write(volt_page('10',D.R10,lead_extra='Фарфоровые аналоги: ИОС-10, ИО-10, ИОР-10, ОНШ, С4-80, С6-80 и др.'))
open(f'{SITE}/osk20.html','w',encoding='utf-8').write(volt_page('20',D.R20,lead_extra='Фарфоровые аналоги: ИОР-20, ОФР-20, ОНШ, ИОС-20.'))
open(f'{SITE}/osk35.html','w',encoding='utf-8').write(volt_page('35',D.R35,alias=D.ALIAS35,lead_extra='Фарфоровые аналоги: ИОР-35, ИОС-35, ОНШ-35, ОНС-35, ИШД-35, С4-195, С16-200.'))
open(f'{SITE}/osk110.html','w',encoding='utf-8').write(volt_page('110',D.R110,alias=D.ALIAS110,lead_extra='Фарфоровые аналоги: ИОС-110, УСТ-110, АКО-110, ОНС-110, С4-450, С4-550, С6-480.'))
open(f'{SITE}/osk150.html','w',encoding='utf-8').write(volt_page('150',D.R150,alias=D.ALIAS150,lead_extra='Изоляторы 150 кВ взаимозаменяемы с колонками фарфоровых ИОС-35 + ИОС-110.'))
open(f'{SITE}/osk220.html','w',encoding='utf-8').write(volt_page('220',D.R220,lead_extra='Изоляторы 220 кВ взаимозаменяемы с колонками фарфоровых ОНШ 35-20 и ИШТ 35.'))

# Общая страница группы
cards=''.join(f'''<div class="col-6 col-md-4"><a class="volt-card" href="{u}"><span class="volt-num">{v}</span><span class="volt-unit">кВ</span><span class="volt-cnt">{len(rows)} моделей</span></a></div>'''
    for (v,u),rows in zip(VOLTS,[D.R10,D.R20,D.R35,D.R110,D.R150,D.R220]))
total=sum(len(x) for x in (D.R10,D.R20,D.R35,D.R110,D.R150,D.R220))
body=f'''
<section class="page-hero"><div class="container">
  <nav class="crumbs"><a href="index.html#catalog">Продукция</a> / Опорные изоляторы ОСК</nav>
  <h1>Изоляторы опорные стержневые полимерные ОСК</h1>
  <p class="section-lead">Альтернативные названия: ИОСК, ИОС, ИО, ОНШ. Напряжение от 10 до 220 кВ. Всего в каталоге {total} моделей.</p>
  <div class="d-flex flex-wrap gap-3">
    <a class="btn-main" href="form.html"><i class="fa fa-paper-plane"></i> Оставить заявку</a>
    <a class="btn-ghost-dark" href="tel:+380509473549"><i class="fa fa-phone"></i> +380 50 947 35 49</a>
  </div>
</div></section>
<section><div class="container"><div class="row g-4"><div class="col-lg-3">{site_nav.side_nav('osk.html')}</div><div class="col-lg-9">
  <span class="eyebrow">Выберите напряжение</span><h2 class="section-title">Каталог по классам напряжения</h2>
  <div class="row g-3 mb-5">{cards}</div>
  <div class="row g-4 mx-0">
    <div class="col-xl-7"><span class="eyebrow">Описание</span><h2 class="section-title">Изоляторы ОСК</h2>{DESC_TXT}</div>
    <div class="col-xl-5">{LEGEND}</div>
  </div>
</div></div></div></section>
{cta()}'''
open(f'{SITE}/osk.html','w',encoding='utf-8').write(page('Опорные изоляторы ОСК (ИОСК), аналог ИОС, ОНШ 10–220 кВ','Опорные стержневые полимерные изоляторы ОСК (ИОСК, ИОС, ИО, ОНШ) на напряжение от 10 до 220 кВ. Замена фарфоровых изоляторов ИОС, УСТ, ОНШ, ИШТ, ОНС, АКО. Цена завода, поставки по Украине.',body))
print('pages done; total models',total)
