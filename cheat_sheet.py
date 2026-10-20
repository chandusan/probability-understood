"""Publish the exam reference and its original one-page printable PDF."""
import html
import json

PDF_NAME = 'probability-statistics-exam-cheat-sheet.pdf'


def load_cheat_sheet(root):
    pdf = root / 'assets/downloads' / PDF_NAME
    if not pdf.is_file() or pdf.read_bytes()[:5] != b'%PDF-':
        raise ValueError('Missing or invalid exam cheat-sheet PDF')
    columns = json.loads((root / 'content/cheat-sheet.json').read_text())
    if not isinstance(columns, list) or not columns:
        raise ValueError('Exam cheat sheet needs content columns')
    for column in columns:
        if not isinstance(column, list) or not column or column[0][0] != 'h':
            raise ValueError('Each cheat-sheet column must begin with a heading')
        for item in column:
            if (not isinstance(item, list) or len(item) != 2
                    or item[0] not in ('h', 'p', 's', 'b', 'e')
                    or not isinstance(item[1], str) or not item[1].strip()):
                raise ValueError('Invalid cheat-sheet content block')
    return columns


def download_panel(prefix, on_cheat_sheet=False):
    pdf = f'{prefix}assets/downloads/{PDF_NAME}'
    secondary = (f'<a class="cheat-sheet-secondary" href="{pdf}" target="_blank" rel="noopener">Open PDF to print ↗</a>'
                 if on_cheat_sheet else
                 f'<a class="cheat-sheet-secondary" href="{prefix}cheat-sheet/index.html">Read the cheat sheet →</a>')
    title = 'Print the one-page sheet' if on_cheat_sheet else 'Exam cheat sheet · Lessons 01–10'
    return f'''<section class="cheat-sheet-download" id="download" aria-labelledby="download-title">
<h2 id="download-title">{title}</h2>
<p>Key formulas, methods and common traps, prioritized using the 2024 and 2025 midterms.</p>
<div class="cheat-sheet-actions"><a class="cheat-sheet-button" href="{pdf}" download="{PDF_NAME}">Download PDF</a>{secondary}</div>
<p class="cheat-sheet-print-note">1 page · A4 landscape · Print at 100% / actual size</p>
</section>'''


def build_cheat_sheet(out, columns, chapter_navigation):
    sections, toc = [], []
    for column in columns:
        for kind, value in column:
            if kind == 'h':
                if sections:
                    sections.append('</section>')
                anchor = f'topic-{len(toc) + 1}'
                label = html.escape(value)
                toc.append(f'<a href="#{anchor}">{label}</a>')
                sections.append(f'<section class="cheat-sheet-topic" aria-labelledby="{anchor}"><h2 id="{anchor}">{label}</h2>')
            elif kind == 'e':
                sections.append('<div class="cheat-sheet-equation">\\[' + html.escape(value) + '\\]</div>')
            else:
                # These trusted source fragments also feed the printable sheet.
                value = value.replace('<super>', '<sup>').replace('</super>', '</sup>')
                sections.append(f'<h3>{value}</h3>' if kind == 'b' else f'<p>{value}</p>')
    sections.append('</section>')
    navigation = '<a href="#download">Download &amp; print</a>' + ''.join(toc)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="An exam-focused cheat sheet for all ten STAT 5701 lessons, with a one-page A4 PDF to download and print."><title>Exam cheat sheet — Probability, understood</title><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/cheat-sheet.css"><link rel="stylesheet" href="../assets/vendor/katex/katex.min.css"><script defer src="../assets/vendor/katex/katex.min.js"></script><script defer src="../assets/vendor/katex/contrib/auto-render.min.js"></script><script defer src="../assets/site.js"></script></head>
<body class="cheat-sheet-page"><a class="skip" href="#lesson">Skip to the cheat sheet</a>
<aside class="sidebar" aria-label="Cheat sheet navigation"><a class="brand" href="../index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Probability,<br>understood.</span></a><button class="nav-close" data-close-nav aria-label="Close navigation">×</button><p class="course-label">Your study companion</p>{chapter_navigation('../')}<p class="course-title">Exam cheat sheet</p><nav class="slide-nav reference-nav" aria-label="Cheat sheet topics">{navigation}</nav><div class="nav-footer"><a class="appendix-link" href="../exercises/index.html">Lesson exercises</a><a class="appendix-link" href="../midterms/index.html">Midterms · questions &amp; solutions</a><a class="appendix-link" href="../appendix/calculus.html">Calculus appendix</a></div></aside>
<button class="scrim" data-close-nav aria-label="Close navigation"></button><div class="site-body"><header class="topbar"><button class="menu-button" aria-expanded="false" aria-label="Open cheat sheet navigation">☰ Menu</button><div class="breadcrumb"><strong>Exam cheat sheet</strong></div><div class="top-tools"><a href="../assets/downloads/{PDF_NAME}" download="{PDF_NAME}">Download PDF ↓</a></div></header><div class="reading-progress" aria-hidden="true"><i data-reading-progress></i></div>
<div class="page-layout"><main class="lesson" id="lesson"><p class="eyebrow">Exam reference · Lessons 01–10</p><h1>Your exam cheat sheet</h1><p class="lead">The essentials from all ten PDFs, brought together for revision. Read the formulas here or keep the single-page version beside you while you practise.</p>{download_panel('../', on_cheat_sheet=True)}<p class="cheat-sheet-workflow"><strong>Before calculating:</strong> state the support → normalize → choose sums or integrals → condition correctly → check totals and endpoints.</p><article class="prose cheat-sheet-content">{''.join(sections)}</article><footer class="footer"><p>Based on STAT 5701 · Dobrin Marchev · Lessons 01–10 and the Fall 2024 and Fall 2025 midterms. Sources reviewed 20 October 2026.</p><p>A personal study reference. The downloadable PDF is the same one-page sheet presented here.</p></footer></main><aside class="page-toc" aria-label="On this sheet"><p class="toc-label">On this sheet</p>{navigation}<a href="#lesson">Back to the top ↑</a></aside></div></div></body></html>'''
    folder = out / 'cheat-sheet'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(page)
