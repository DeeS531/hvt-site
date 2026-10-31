# -*- coding: utf-8 -*-
"""Скачивает недостающие PDF-чертежи, на которые ссылаются страницы сайта (pdf/<имя>), со старого сайта в data/pdf_orig.
После скачивания: python3 tools/clean_pdf.py (убирает шапку старой компании, ставит наш логотип, пишет в site/pdf).
Читает только https://sep.ho.ua/chertejy/<имя>, пауза 0,6 с, 3 попытки, проверка заголовка %PDF.
Запуск: python3 tools/fetch_pdf.py            (все недостающие)
        python3 tools/fetch_pdf.py имя.pdf ...  (только указанные)"""
import os, re, sys, time, subprocess, urllib.parse
SITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
PDF = os.path.join(SITE, '..', 'data', 'pdf_orig')   # оригиналы «как есть»; чистые копии делает tools/clean_pdf.py -> site/pdf
BASE = 'https://sep.ho.ua/chertejy/'

def wanted():
    names = set()
    for root, _, files in os.walk(SITE):
        if os.sep + 'vendor' in root: continue
        for f in files:
            if f.endswith('.html'):
                s = open(os.path.join(root, f), encoding='utf-8').read()
                for ref in re.findall(r'href="(pdf/[^"]+\.pdf)"', s):
                    names.add(urllib.parse.unquote(ref)[4:])
    return sorted(names)

def fetch(name):
    """качает через curl (у системного python нет корневых сертификатов); проверка кода 200 и заголовка %PDF"""
    url = BASE + urllib.parse.quote(name)
    tmp = os.path.join(PDF, '.tmp_download')
    last = None
    for attempt in range(3):
        r = subprocess.run(['curl', '-sS', '-L', '-m', '60', '-o', tmp, '-w', '%{http_code}', url], capture_output=True, text=True)
        code = r.stdout.strip()
        if r.returncode == 0 and code == '200' and os.path.getsize(tmp) > 0:
            with open(tmp, 'rb') as f: head = f.read(4)
            if head == b'%PDF':
                size = os.path.getsize(tmp); os.replace(tmp, os.path.join(PDF, name)); return True, size
            last = 'ответ 200, но это не PDF'
        else: last = f'код {code} {r.stderr.strip()[:80]}'
        time.sleep(1.0)
    if os.path.exists(tmp): os.remove(tmp)
    return False, last

if __name__ == '__main__':
    names = sys.argv[1:] or [n for n in wanted() if not os.path.exists(os.path.join(PDF, n))]
    os.makedirs(PDF, exist_ok=True)
    ok = bad = 0
    for n in names:
        res, info = fetch(n)
        print(('OK  ' if res else 'ERR ') + n, info, flush=True)
        ok += res; bad += (not res)
        time.sleep(0.6)
    print(f'готово: скачано {ok}, ошибок {bad}')
