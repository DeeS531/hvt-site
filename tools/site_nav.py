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
        items.append(f'<li{" class=\"has-sub\"" if subs else ""}><a href="{href}">{escape(title)}</a>{sub}</li>')
    return ('<li class="nav-item nav-mega"><a class="nav-link" href="index.html#catalog" data-i18n="nav_products">Продукция</a>'
            '<ul class="mega-menu">' + ''.join(items) + '</ul></li><!--/nav-mega-->')

def patch_header(html):
    new = nav_li()
    if '<!--/nav-mega-->' in html:
        return re.sub(r'<li class="nav-item nav-mega">.*?<!--/nav-mega-->', lambda m: new, html, flags=re.S)
    return re.sub(r'<li class="nav-item"><a class="nav-link" href="(?:index\.html)?#catalog" data-i18n="nav_products">Продукция</a></li>', lambda m: new, html)

def side_nav(group_href, current=None):
    """боковой список подгрупп группы (как на старом сайте)"""
    for title, href, subs in MENU:
        if href == group_href:
            lis = ''.join(f'<li><a class="{"active" if h == current else ""}" href="{h}">{escape(t)}</a></li>' for t, h in subs)
            return (f'<aside class="side-nav"><div class="side-title">{escape(title)}</div><ul>{lis}</ul>'
                    f'<a class="side-all" href="index.html#catalog"><i class="fa fa-th-large"></i> Вся продукция</a></aside>')
    raise KeyError(group_href)
