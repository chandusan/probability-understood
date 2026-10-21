"""Publish the combined study sheet and the earlier typed-formula reference."""
import html
import json
import hashlib
import struct
from pathlib import Path

PDF_NAME = 'probability-statistics-exam-cheat-sheet.pdf'
COMBINED_NAME = 'all-lessons-and-calculus.png'
PREVIEW_NAME = 'all-lessons-and-calculus-preview.jpg'
PAGE_COUNTS = [31, 43, 53, 36, 44, 36, 36, 49, 49]


def load_cheat_sheet(root, check_pdf=True):
    combined = root / 'assets/downloads' / COMBINED_NAME
    if not combined.is_file() or combined.read_bytes()[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Missing or invalid combined cheat-sheet PNG')
    if not (root / 'assets/downloads' / PREVIEW_NAME).is_file():
        raise ValueError('Missing combined cheat-sheet preview')
    pdf = root / 'assets/downloads' / PDF_NAME
    if check_pdf and (not pdf.is_file() or pdf.read_bytes()[:5] != b'%PDF-'):
        raise ValueError('Missing or invalid exam cheat-sheet PDF')
    content = json.loads((root / 'content/cheat-sheet.json').read_text())
    if content.get('version') != 3 or [l['number'] for l in content['lessons']] != list(range(1, 10)):
        raise ValueError('Formula sheet must contain PDFs 01–09 in order')
    for lesson in content['lessons']:
        number = lesson['number']
        if [p['number'] for p in lesson['pages']] != list(range(1, PAGE_COUNTS[number - 1] + 1)):
            raise ValueError(f'Incomplete slide audit for PDF {number:02}')
        if not (root / 'assets/source' / lesson['source_pdf']).is_file():
            raise ValueError('Missing original source PDF')
        for page in lesson['pages']:
            if not isinstance(page.get('formulas'), list):
                raise ValueError('Missing typed formulas')
            region_count = page.get('source_region_count')
            if not isinstance(region_count, int) or region_count < 0:
                raise ValueError('Missing source-slide coverage audit')
            covered = set()
            for formula in page['formulas']:
                tex = formula.get('tex')
                if not isinstance(tex, str) or not tex.strip():
                    raise ValueError('Empty typed formula')
                if not isinstance(formula.get('regions'), list):
                    raise ValueError('Missing source formula provenance')
                covered.update(formula['regions'])
            for exclusion in page.get('exclusions', []):
                if not exclusion.get('reason'):
                    raise ValueError('Unexplained source-region exclusion')
                covered.add(exclusion['region'])
            if covered != set(range(1, region_count + 1)):
                raise ValueError(f'Incomplete formula coverage: PDF {number:02}, slide {page["number"]}')
    if not any(p['formulas'] for l in content['lessons'] for p in l['pages']):
        raise ValueError('The formula sheet is empty')
    return content


def pdf_url(prefix):
    return download_url(prefix, PDF_NAME)


def download_url(prefix, name):
    asset = Path(__file__).resolve().parent / 'assets/downloads' / name
    version = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
    return f'{prefix}assets/downloads/{name}?v={version}'


def download_panel(prefix, on_cheat_sheet=False):
    pdf = pdf_url(prefix)
    combined = download_url(prefix, COMBINED_NAME)
    preview = download_url(prefix, PREVIEW_NAME)
    image = Path(__file__).resolve().parent / 'assets/downloads' / COMBINED_NAME
    with image.open('rb') as stream:
        width, height = struct.unpack('>II', stream.read(24)[16:24])
    size_mb = image.stat().st_size / 1_000_000
    secondary = (f'<a class="cheat-sheet-secondary" href="{combined}" target="_blank" rel="noopener">Open full-size image ↗</a>'
                 if on_cheat_sheet else
                 f'<a class="cheat-sheet-secondary" href="{prefix}cheat-sheet/index.html">View the cheat sheets →</a>')
    preview_html = (f'<a class="cheat-sheet-preview" href="{combined}" target="_blank" rel="noopener" aria-label="Open the combined cheat sheet at full resolution"><img src="{preview}" width="{width}" height="{height}" alt="Overview of the combined lessons 01–10 and calculus cheat sheet, arranged in eight columns." loading="lazy" decoding="async"></a>'
                    if on_cheat_sheet else '')
    return f'''<section class="cheat-sheet-download" id="download" aria-labelledby="download-title">
<h2 id="download-title">Combined cheat sheet · Lessons 01–10 + calculus</h2>
<p>Lessons 01–10 and calculus in one compact image. Definitions, formulas and conditions are grouped by topic, with repeated material consolidated and worked examples removed.</p>
<div class="cheat-sheet-actions"><a class="cheat-sheet-button" href="{combined}" download="{COMBINED_NAME}">Download combined sheet (PNG)</a>{secondary}</div>
<p class="cheat-sheet-print-note">{width:,} × {height:,} pixels · {size_mb:.1f} MB · Read down each column, then continue right. Open the full-size image to zoom into the formulas.</p>
{preview_html}
<p class="cheat-sheet-legacy">Earlier reference: <a href="{pdf}" download="{PDF_NAME}">original slide formulas, PDFs 01–09 (one-page PDF)</a>.</p>
</section>'''


def build_cheat_sheet(out, content, chapter_navigation):
    sections, toc = [], []
    pdf = pdf_url('../')
    combined = download_url('../', COMBINED_NAME)
    for lesson in content['lessons']:
        number = lesson['number']
        anchor, label = f'pdf-{number:02}', f'PDF {number:02}'
        source = html.escape(lesson['source_pdf'], quote=True)
        toc.append(f'<a href="#{anchor}">{label}</a>')
        sections.append(f'<section class="cheat-sheet-topic" aria-labelledby="{anchor}"><h2 id="{anchor}">{label}</h2>')
        for page in lesson['pages']:
            if not page['formulas']:
                continue
            p = page['number']
            sections.append(f'<section class="formula-source-slide" id="pdf-{number:02}-slide-{p:02}"><h3>Slide {p:02}<a href="../assets/source/{source}#page={p}" target="_blank" rel="noopener" aria-label="Open PDF {number:02}, slide {p:02}">Original slide ↗</a></h3>')
            for i, formula in enumerate(page['formulas'], 1):
                tex = html.escape(formula['tex'])
                sections.append(f'<div class="formula-equation" data-formula-id="{number:02}-{p:02}-{i:03}">\\[{tex}\\]</div>')
            sections.append('</section>')
        sections.append('</section>')
    navigation = '<a href="#download">Download combined sheet</a><a href="#source-formulas">Earlier formula reference</a>' + ''.join(toc)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Download the compact STAT 5701 cheat sheet: lessons 01–10 plus differentiation and integration, with definitions, formulas and key conditions."><title>Exam cheat sheets — Probability, understood</title><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/cheat-sheet.css?v=combined-sheet-1"><link rel="stylesheet" href="../assets/vendor/katex/katex.min.css"><script defer src="../assets/vendor/katex/katex.min.js"></script><script defer src="../assets/vendor/katex/contrib/auto-render.min.js"></script><script defer src="../assets/site.js"></script></head>
<body class="cheat-sheet-page"><a class="skip" href="#lesson">Skip to the cheat sheet</a>
<aside class="sidebar" aria-label="Cheat sheet navigation"><a class="brand" href="../index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Probability,<br>understood.</span></a><button class="nav-close" data-close-nav aria-label="Close navigation">×</button><p class="course-label">Your study companion</p>{chapter_navigation('../')}<p class="course-title">Exam cheat sheet</p><nav class="slide-nav reference-nav" aria-label="Cheat sheet topics">{navigation}</nav><div class="nav-footer"><a class="appendix-link" href="../exercises/index.html">Lesson exercises</a><a class="appendix-link" href="../midterms/index.html">Midterms · questions &amp; solutions</a><a class="appendix-link" href="../appendix/calculus.html">Calculus appendix</a></div></aside>
<button class="scrim" data-close-nav aria-label="Close navigation"></button><div class="site-body"><header class="topbar"><button class="menu-button" aria-expanded="false" aria-label="Open cheat sheet navigation">☰ Menu</button><div class="breadcrumb"><strong>Exam cheat sheets</strong></div><div class="top-tools"><a href="{combined}" download="{COMBINED_NAME}">Download PNG ↓</a></div></header><div class="reading-progress" aria-hidden="true"><i data-reading-progress></i></div>
<div class="page-layout"><main class="lesson" id="lesson"><p class="eyebrow">Lessons 01–10 · Calculus toolkit</p><h1>Your exam cheat sheets</h1><p class="lead">A compact reference with clear definitions, essential properties and formula tables. Download all ten lessons and the calculus toolkit together in one high-resolution image.</p>{download_panel('../', on_cheat_sheet=True)}<article class="prose cheat-sheet-content"><h2 id="source-formulas">Earlier reference · original slide formulas</h2><p>The archive below covers PDFs 01–09 in slide order. It matches the earlier one-page PDF, available above.</p>{''.join(sections)}</article><footer class="footer"><p>STAT 5701 · Dobrin Marchev · Personal study companion.</p><p>The original-formula archive covers all 377 source slides in PDFs 01–09 and preserves their notation and calculations.</p></footer></main><aside class="page-toc" aria-label="On this sheet"><p class="toc-label">On this sheet</p>{navigation}<a href="#lesson">Back to the top ↑</a></aside></div></div></body></html>'''
    folder = out / 'cheat-sheet'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(page)
