"""Publish original formula regions from PDFs 01–09 and their one-page PDF."""
import html
import json
import math
import hashlib
from pathlib import Path

PDF_NAME = 'probability-statistics-exam-cheat-sheet.pdf'
SOURCE_SLIDES = ['', 'probability-part1', 'counting', 'probability-part2',
                 'probability-part3', 'random-variables', 'random-variables-part2',
                 'random-variables-part3', 'expectation']
PAGE_COUNTS = [31, 43, 53, 36, 44, 36, 36, 49, 49]


def slide_image(lesson, page):
    folder = SOURCE_SLIDES[lesson - 1]
    return f'assets/slides/{folder + "/" if folder else ""}{page:02}.webp'


def load_cheat_sheet(root, check_pdf=True):
    pdf = root / 'assets/downloads' / PDF_NAME
    if check_pdf and (not pdf.is_file() or pdf.read_bytes()[:5] != b'%PDF-'):
        raise ValueError('Missing or invalid exam cheat-sheet PDF')
    content = json.loads((root / 'content/cheat-sheet.json').read_text())
    if content.get('version') != 2 or [l['number'] for l in content['lessons']] != list(range(1, 10)):
        raise ValueError('Formula sheet must contain PDFs 01–09 in order')
    for lesson in content['lessons']:
        number = lesson['number']
        if [p['number'] for p in lesson['pages']] != list(range(1, PAGE_COUNTS[number - 1] + 1)):
            raise ValueError(f'Incomplete slide audit for PDF {number:02}')
        if not (root / 'assets/source' / lesson['source_pdf']).is_file():
            raise ValueError('Missing original source PDF')
        for page in lesson['pages']:
            width, height = page['width'], page['height']
            for rect in page['rects']:
                if (len(rect) != 4 or not all(math.isfinite(v) for v in rect)
                        or not 0 <= rect[0] < rect[2] <= width
                        or not 0 <= rect[1] < rect[3] <= height):
                    raise ValueError('Invalid source formula region')
            if page['rects'] and not (root / slide_image(number, page['number'])).is_file():
                raise ValueError('Missing original slide image')
    return content


def pdf_url(prefix):
    pdf = Path(__file__).resolve().parent / 'assets/downloads' / PDF_NAME
    version = hashlib.sha256(pdf.read_bytes()).hexdigest()[:12]
    return f'{prefix}assets/downloads/{PDF_NAME}?v={version}'


def download_panel(prefix, on_cheat_sheet=False):
    pdf = pdf_url(prefix)
    secondary = (f'<a class="cheat-sheet-secondary" href="{pdf}" target="_blank" rel="noopener">Open PDF to print ↗</a>'
                 if on_cheat_sheet else
                 f'<a class="cheat-sheet-secondary" href="{prefix}cheat-sheet/index.html">Read the cheat sheet →</a>')
    title = 'Print the one-page sheet' if on_cheat_sheet else 'Formula sheet · PDFs 01–09'
    return f'''<section class="cheat-sheet-download" id="download" aria-labelledby="download-title">
<h2 id="download-title">{title}</h2>
<p>Original formulas from PDFs 01–09, in the order they appear in the slides.</p>
<div class="cheat-sheet-actions"><a class="cheat-sheet-button" href="{pdf}" download="{PDF_NAME}">Download PDF</a>{secondary}</div>
<p class="cheat-sheet-print-note">1 page · A4 landscape · Very small text · Print at 100% / actual size</p>
</section>'''


def build_cheat_sheet(out, content, chapter_navigation):
    sections, toc = [], []
    pdf = pdf_url('../')
    for lesson in content['lessons']:
        number = lesson['number']
        anchor, label = f'pdf-{number:02}', f'PDF {number:02}'
        source = html.escape(lesson['source_pdf'], quote=True)
        toc.append(f'<a href="#{anchor}">{label}</a>')
        sections.append(f'<section class="cheat-sheet-topic" aria-labelledby="{anchor}"><h2 id="{anchor}">{label}</h2>')
        for page in lesson['pages']:
            if not page['rects']:
                continue
            p, w, h = page['number'], page['width'], page['height']
            sections.append(f'<section class="formula-source-slide" id="pdf-{number:02}-slide-{p:02}"><h3>Slide {p:02}<a href="../assets/source/{source}#page={p}" target="_blank" rel="noopener" aria-label="Open PDF {number:02}, slide {p:02}">Original slide ↗</a></h3>')
            for i, (x0, y0, x1, y1) in enumerate(page['rects'], 1):
                rw, rh = x1 - x0, y1 - y0
                # Display the exact audited crop; the full source image is cached once per slide.
                crop_style = f'width:{rw / w * 100:.6f}%;aspect-ratio:{rw:.6f}/{rh:.6f}'
                image_style = f'width:{w / rw * 100:.6f}%;left:{-x0 / rw * 100:.6f}%;top:{-y0 / rh * 100:.6f}%'
                image = slide_image(number, p)
                sections.append(f'<div class="formula-source-crop" style="{crop_style}"><img src="../{image}" style="{image_style}" loading="lazy" decoding="async" alt="Original formula region {i}, PDF {number:02}, slide {p:02}"></div>')
            sections.append('</section>')
        sections.append('</section>')
    navigation = '<a href="#download">Download &amp; print</a>' + ''.join(toc)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Original formulas from STAT 5701 PDFs 01–09, in slide order, with a one-page A4 PDF to download and print."><title>Exam cheat sheet — Probability, understood</title><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/cheat-sheet.css?v=source-formulas-2"><link rel="stylesheet" href="../assets/vendor/katex/katex.min.css"><script defer src="../assets/vendor/katex/katex.min.js"></script><script defer src="../assets/vendor/katex/contrib/auto-render.min.js"></script><script defer src="../assets/site.js"></script></head>
<body class="cheat-sheet-page"><a class="skip" href="#lesson">Skip to the cheat sheet</a>
<aside class="sidebar" aria-label="Cheat sheet navigation"><a class="brand" href="../index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Probability,<br>understood.</span></a><button class="nav-close" data-close-nav aria-label="Close navigation">×</button><p class="course-label">Your study companion</p>{chapter_navigation('../')}<p class="course-title">Exam cheat sheet</p><nav class="slide-nav reference-nav" aria-label="Cheat sheet topics">{navigation}</nav><div class="nav-footer"><a class="appendix-link" href="../exercises/index.html">Lesson exercises</a><a class="appendix-link" href="../midterms/index.html">Midterms · questions &amp; solutions</a><a class="appendix-link" href="../appendix/calculus.html">Calculus appendix</a></div></aside>
<button class="scrim" data-close-nav aria-label="Close navigation"></button><div class="site-body"><header class="topbar"><button class="menu-button" aria-expanded="false" aria-label="Open cheat sheet navigation">☰ Menu</button><div class="breadcrumb"><strong>Exam cheat sheet</strong></div><div class="top-tools"><a href="{pdf}" download="{PDF_NAME}">Download PDF ↓</a></div></header><div class="reading-progress" aria-hidden="true"><i data-reading-progress></i></div>
<div class="page-layout"><main class="lesson" id="lesson"><p class="eyebrow">Original slide formulas · PDFs 01–09</p><h1>Your formula sheet</h1><p class="lead">Formulas reproduced directly from the original slides, in teaching order. Read them at a larger size below, or download the single-page printable sheet.</p>{download_panel('../', on_cheat_sheet=True)}<article class="prose cheat-sheet-content">{''.join(sections)}</article><footer class="footer"><p>STAT 5701 · Dobrin Marchev · PDFs 01–09 · All 377 source slides reviewed.</p><p>Original notation, conditions and calculations are preserved. The download contains the same formula regions on one A4 landscape page.</p></footer></main><aside class="page-toc" aria-label="On this sheet"><p class="toc-label">On this sheet</p>{navigation}<a href="#lesson">Back to the top ↑</a></aside></div></div></body></html>'''
    folder = out / 'cheat-sheet'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(page)
