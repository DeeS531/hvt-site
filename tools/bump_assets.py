# -*- coding: utf-8 -*-
"""Добавляет версию к ссылкам на css/js во всех страницах (style.css?v=abc123): после заливки браузеры не держат старые стили.
Запускать ПОСЛЕДНИМ (после i18n_build.py). Версия = хэш содержимого css/js, меняется только при изменении файлов."""
import os, re, hashlib
SITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
h = hashlib.md5()
for f in ('css/style.css', 'js/main.js', 'js/i18n.js'): h.update(open(os.path.join(SITE, f), 'rb').read())
V = h.hexdigest()[:8]
pat = re.compile(r'((?:\.\./)?(?:css/style\.css|js/main\.js|js/i18n\.js))(?:\?v=\w+)?(")')
n = 0
for root, _, files in os.walk(SITE):
    if os.sep + 'vendor' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f); s = open(p, encoding='utf-8').read()
            t = pat.sub(lambda m: f'{m.group(1)}?v={V}{m.group(2)}', s)
            if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
print(f'версия ассетов {V}; страниц обновлено: {n}')
