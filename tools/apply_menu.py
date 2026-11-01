# -*- coding: utf-8 -*-
"""Вставляет/обновляет выпадающее меню «Продукция» в шапке всех страниц site/*.html. Запуск: python3 tools/apply_menu.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import site_nav
SITE = os.path.normpath(os.path.join(HERE, '..', 'site'))
n = 0
for f in sorted(os.listdir(SITE)):
    if f.endswith('.html'):
        p = os.path.join(SITE, f); s = open(p, encoding='utf-8').read(); t = site_nav.add_banner(site_nav.add_sidebar(site_nav.patch_footer(site_nav.patch_header(s)), f), f)
        if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
print('меню обновлено на страницах:', n)
