# -*- coding: utf-8 -*-
"""Меню «Продукция» (выпадающее, два уровня) и боковой список подгрупп. Единый источник для всех страниц.
Группы 4–8 пока ведут на каталог на главной; когда страницы группы будут готовы — поменять href здесь и запустить `python3 tools/apply_menu.py`."""
import os, re
from html import escape

CAT = 'index.html#catalog'
MENU = [
 ('Линейные изоляторы', 'lkc.html', [('Линейные изоляторы ЛКЦ 70 кН', 'lkc70.html'), ('Линейные изоляторы ЛКЦ 120 кН', 'lkc120.html'), ('Линейные изоляторы ЛКЦ 160 кН', 'lkc160.html')]),
 ('Опорные изоляторы', 'osk.html', [(f'Изоляторы опорные {v} кВ', f'osk{v}.html') for v in (10, 20, 35, 110, 150, 220)]),
 ('Ограничители перенапряжения', 'opn.html',
   [('ОПНп, ОПН-П 0,22–0,4 кВ', 'opn022.html'), ('ОПНп, ОПН-П 3 кВ', 'opn3.html'), ('ОПНп, ОПН-П 3,3 кВ', 'opn33.html'), ('ОПНп, ОПН-П 6 кВ', 'opn6.html'),
    ('ОПНп, ОПН-П 10 кВ', 'opn10.html'), ('ОПНп, ОПН-П 15 кВ', 'opn15.html'), ('ОПНп, ОПН-П 20 кВ', 'opn20.html'), ('ОПНп, ОПН-П 27,5 кВ', 'opn27.html'),
    ('ОПНп, ОПН-П 35 кВ', 'opn35.html'), ('ОПНп, ОПН-П 110 кВ', 'opn110.html'), ('ОПНп, ОПН-П 150 кВ', 'opn150.html'), ('ОПНп, ОПН-П 220 кВ', 'opn220.html'),
    ('ОПНп, ОПН-П 330 кВ', 'opn330.html'), ('Регистратор срабатывания JCQF2', 'jcqf2.html'), ('Регистратор срабатывания JCQF3', 'jcqf3.html')]),
 ('Вводы высоковольтные для выключателей 35 кВ', 'vk35.html', [('Вводы ВК-35', 'vk35.html'), ('Вводы ГКВПШ с усиленной изоляцией', 'vk35u.html')]),
 ('Изоляторы полимерные для контактной сети железных дорог', 'jdn.html', []),
 ('Проходные изоляторы', 'ppc.html', []),
 ('Шинные опоры ШО, ШОП', 'shop.html', [(f'Шинные опоры на напряжение {v} кВ', f'shop{v}.html') for v in (10, 20, 35, 110, 150, 220, 330)]),
 ('Распорки межфазные РМИ', 'rmi.html', []),
 ('Взаимозаменяемость изоляторов ОСК', 'zamena.html', []),
 ('Документы и стандарты', 'docs.html', []),
]

def nav_li():
    items = []
    for title, href, subs in MENU:
        sub = ''
        if subs:
            sub = '<ul class="mega-sub">' + ''.join(f'<li><a href="{h}">{escape(t)}</a></li>' for t, h in subs) + '</ul>'
        tg = '<button type="button" class="mega-toggle sub-toggle" aria-label="Раскрыть" aria-expanded="false"><i class="fa fa-angle-down"></i></button>' if subs else ''
        items.append(f'<li{" class=\"has-sub\"" if subs else ""}><a href="{href}">{escape(title)}</a>{tg}{sub}</li>')
    return ('<li class="nav-item nav-mega"><a class="nav-link" href="index.html#catalog" data-i18n="nav_products">Продукция</a>'
            '<button type="button" class="mega-toggle" aria-label="Раскрыть" aria-expanded="false"><i class="fa fa-angle-down"></i></button>'
            '<ul class="mega-menu">' + ''.join(items) + '</ul></li><!--/nav-mega-->')

LANG_DD = ('<div class="lang-dd d-lg-none ms-auto me-2"><button type="button" class="lang-dd-btn" aria-haspopup="true" aria-expanded="false" aria-label="Language">'
           '<i class="fa fa-globe"></i><span data-lang-current>RU</span><i class="fa fa-angle-down lang-caret"></i></button>'
           '<ul class="lang-dd-list" hidden><li><button type="button" data-lang-btn="ru">RU</button></li><li><button type="button" data-lang-btn="uk">UA</button></li>'
           '<li><button type="button" data-lang-btn="en">EN</button></li></ul></div>')

def patch_header(html):
    new = nav_li()
    if '<!--/nav-mega-->' in html:
        html = re.sub(r'<li class="nav-item nav-mega">.*?<!--/nav-mega-->', lambda m: new, html, flags=re.S)
    else:
        html = re.sub(r'<li class="nav-item"><a class="nav-link" href="(?:index\.html)?#catalog" data-i18n="nav_products">Продукция</a></li>', lambda m: new, html)
    # выбор языка на мобильных: выпадающий список вместо трёх кнопок
    html = re.sub(r'<span class="lang-switch lang-switch-mobile d-lg-none ms-auto me-2".*?</span>', lambda m: LANG_DD, html, flags=re.S)
    # меню-шторкой управляет js/main.js, а не Bootstrap collapse
    html = html.replace(' data-bs-toggle="collapse" data-bs-target="#mainMenu"', '')
    # длинный e-mail в верхней полосе: на узких экранах — коротко «Email»
    html = html.replace('<i class="fa fa-envelope me-1"></i> highvoltagetechnologies.ua@gmail.com</a>', '<i class="fa fa-envelope me-1"></i> <span class="c-full">highvoltagetechnologies.ua@gmail.com</span><span class="c-short">Email</span></a>')
    return html

FOOTER = ('<footer class="site-footer">\n  <div class="container text-center">\n'
          '    <span>© 2026 ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ. <span data-i18n="footer_rights">Все права защищены.</span></span>\n  </div>\n</footer>')

def patch_footer(html):
    html = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: FOOTER, html, flags=re.S)
    return html

def side_nav(group_href, current=None):
    """боковой список подгрупп группы (как на старом сайте)"""
    for title, href, subs in MENU:
        if href == group_href:
            lis = ''.join(f'<li><a class="{"active" if h == current else ""}" href="{h}">{escape(t)}</a></li>' for t, h in subs)
            return (f'<details class="side-nav" open><summary class="side-title">{escape(title)}</summary><ul>{lis}</ul>'
                    f'<a class="side-all" href="index.html#catalog"><i class="fa fa-th-large"></i> Вся продукция</a></details>')
    raise KeyError(group_href)


def add_sidebar(html, fname):
    """боковое меню группы: на страницах подгрупп/изделий, где его нет, ставит в первый блок после шапки страницы;
    на уже готовых страницах приводит старую разметку <aside> к <details> (сворачивается на телефоне)"""
    html = re.sub(r'<aside class="side-nav"><div class="side-title">(.*?)</div>', r'<details class="side-nav" open><summary class="side-title">\1</summary>', html)
    html = html.replace('</a></aside>', '</a></details>')
    if 'class="side-nav"' in html:
        return html
    group = next((g for t, g, subs in MENU if any(h == fname for _, h in subs)), None)
    if not group:
        return html
    m = re.search(r'(class="page-hero".*?</section>\s*)(<section[^>]*>)(\s*<div class="container">)(.*?)(</div>)(\s*</section>)', html, flags=re.S)
    if not m:
        return html
    inner = m.group(4).replace('col-lg-7', 'col-xl-7').replace('col-lg-5', 'col-xl-5')
    new = (m.group(1) + m.group(2) + '<div class="container"><div class="row g-4"><div class="col-lg-3">' + side_nav(group, fname) +
           '</div><div class="col-lg-9">' + inner + '</div></div></div>' + m.group(6))
    return html[:m.start()] + new + html[m.end():]


# фото-баннеры на страницах групп (автопрокрутка, если фото несколько); наборы взяты со старого сайта
BANNERS = {
 'lkc.html': ['lk1', 'lk2', 'lk3', 'lk4', 'lk5'],
 'osk.html': ['osk1', 'osk2', 'osk3', 'osk4', 'osk5'],
 'opn.html': ['opn1', 'opn2', 'opn3', 'opn4', 'opn5'],
 'vk35.html': ['vk2'],
 'jdn.html': ['home3', 'lk1', 'lk2', 'lk3', 'lk5'],
 'ppc.html': ['osk1', 'osk2', 'osk3', 'osk4', 'osk5'],
 'shop.html': ['home4', 'home2', 'osk4', 'osk5'],
 'rmi.html': ['lk1', 'lk2', 'lk3', 'lk4'],
}

def add_banner(html, fname):
    """вставляет карусель фото между шапкой страницы и первым блоком контента"""
    names = BANNERS.get(fname) or BANNERS.get(next((g for t, g, subs in MENU if any(h == fname for _, h in subs)), None))
    if not names or 'banner-carousel' in html:
        return html
    m = re.search(r'(class="page-hero".*?</section>\s*)(<section)', html, flags=re.S)
    if not m:
        return html
    imgs = [f'<img src="images/banners/{n}.jpg" alt="" width="1080" height="300"{"" if i == 0 else " loading=\"lazy\""}>' for i, n in enumerate(names)]
    if len(imgs) == 1:
        inner = f'<div class="banner-carousel">{imgs[0]}</div>'
    else:
        ind = ''.join(f'<button type="button" data-bs-target="#groupBanner" data-bs-slide-to="{i}"{" class=\"active\" aria-current=\"true\"" if i == 0 else ""} aria-label="{i + 1}"></button>' for i in range(len(imgs)))
        items = ''.join(f'<div class="carousel-item{" active" if i == 0 else ""}">{im}</div>' for i, im in enumerate(imgs))
        inner = (f'<div id="groupBanner" class="carousel slide banner-carousel" data-bs-ride="carousel" data-bs-interval="3000">'
                 f'<div class="carousel-indicators">{ind}</div><div class="carousel-inner">{items}</div>'
                 '<button class="carousel-control-prev" type="button" data-bs-target="#groupBanner" data-bs-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span></button>'
                 '<button class="carousel-control-next" type="button" data-bs-target="#groupBanner" data-bs-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span></button></div>')
    sec = f'<section class="banner-sec"><div class="container">{inner}</div></section>\n'
    return html[:m.start(2)] + sec + html[m.start(2):]
