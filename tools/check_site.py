# -*- coding: utf-8 -*-
"""Проверка сайта: python3 tools/check_site.py
Ищет: двойной doctype/html, дубли id, битые локальные ссылки, ссылки на PDF без файла,
ссылки на старый домен и старые контакты."""
import os, re, sys, collections, urllib.parse
SITE=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
BAD=['sep.ho.ua','slavsep@gmail.com','761-20-09','Славэнергосистем','Славэнергопром','Slavenergosistem']
problems=0; missing_pdf=set(); have_pdf=0
for root,_,files in os.walk(SITE):
    if os.sep+'vendor' in root: continue
    for f in files:
        if not f.endswith('.html'): continue
        path=os.path.join(root,f); rel=os.path.relpath(path,SITE)
        s=open(path,encoding='utf-8').read()
        errs=[]
        if len(re.findall(r'<!DOCTYPE',s,re.I))!=1: errs.append('doctype != 1')
        if len(re.findall(r'<html[\s>]',s))!=1: errs.append('<html> != 1')
        ids=re.findall(r'\bid="([^"]+)"',s)
        d=[k for k,v in collections.Counter(ids).items() if v>1]
        if d: errs.append('дубли id: '+', '.join(d[:5]))
        for ref in set(re.findall(r'(?:href|src)="([^"]+)"',s)):
            if ref.startswith(('http','mailto:','tel:','data:','javascript:')): continue
            if ref.startswith('#'):
                if ref[1:] and ref[1:] not in ids and ref[1:] not in ('top',): errs.append('нет якоря '+ref)
                continue
            target=urllib.parse.unquote(ref.split('#')[0].split('?')[0])
            if not target: continue
            full=os.path.normpath(os.path.join(os.path.dirname(path),target))
            if target.lower().endswith('.pdf'):
                if os.path.exists(full): have_pdf+=1
                else: missing_pdf.add(target)
            elif not os.path.exists(full): errs.append('нет файла '+ref)
        for b in BAD:
            if b in s: errs.append('старые данные: '+b)
        if errs:
            problems+=1; print(f'[!] {rel}:'); [print('     -',e) for e in errs]
print(f'\nPDF: найдено {have_pdf} ссылок на существующие файлы, НЕТ файла у {len(missing_pdf)} уникальных ссылок')
if missing_pdf and '--pdf' in sys.argv:
    for m in sorted(missing_pdf): print('   ',m)
print('Страниц с проблемами:',problems)
sys.exit(1 if problems else 0)
