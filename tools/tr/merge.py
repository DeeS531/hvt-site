# -*- coding: utf-8 -*-
"""Склеивает tools/tr/b*.txt (индекс ||| укр ||| англ) с keys_order.json в tools/tr/ua.json и en.json. «=» — оставить как есть."""
import json, os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
keys = json.load(open(os.path.join(HERE, 'keys_order.json'), encoding='utf-8'))
ua = {}; en = {}
for f in sorted(glob.glob(os.path.join(HERE, 'b*.txt'))):
    for ln in open(f, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip(): continue
        i, u, e = [x.strip() for x in ln.split(' ||| ')]
        k = keys[int(i)]
        ua[k] = k if u == '=' else u; en[k] = k if e == '=' else e
for fn, d in (('ua.json', ua), ('en.json', en)):
    old = {}
    p = os.path.join(HERE, fn)
    if os.path.exists(p): old = json.load(open(p, encoding='utf-8'))
    old.update(d)
    json.dump(old, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('ua', len(ua), 'en', len(en), 'из', len(keys), '| не покрыто:', len(set(keys) - set(ua)))
