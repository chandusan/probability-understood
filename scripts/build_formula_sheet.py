"""Typeset formula text with LaTeX and compose one printable A4 page.

Requires Tectonic and PyMuPDF. No slide images or source-PDF regions are used.
"""
from pathlib import Path
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cheat_sheet import load_cheat_sheet

PREAMBLE = r'''\documentclass[10pt]{article}
\usepackage{amsmath,amssymb,mathtools}
\usepackage[active,tightpage]{preview}
\setlength\PreviewBorder{0.6pt}
\setlength\arraycolsep{3pt}
\renewcommand\arraystretch{1.06}
\begin{document}
'''
UNSAFE = re.compile(r'\\(?:input|include|write|openout|read|usepackage|documentclass|special|directlua|catcode|csname|newcommand|def|href|url|includegraphics)\b')


def formulas_from(content):
    groups, formulas = [], []
    for lesson in content['lessons']:
        for page in lesson['pages']:
            if not page['formulas']:
                continue
            indices = []
            for formula in page['formulas']:
                tex = formula['tex'].strip()
                if UNSAFE.search(tex):
                    raise ValueError('Unsupported non-mathematical TeX command')
                indices.append(len(formulas))
                formulas.append({'tex': tex, 'lesson': lesson['number'], 'slide': page['number']})
            groups.append({'lesson': lesson['number'], 'slide': page['number'], 'indices': indices})
    return groups, formulas


def typeset(formulas, work, tectonic):
    source = work / 'formulas.tex'
    source.write_text(PREAMBLE + '\n'.join(
        '%% Formula %d: PDF %02d, slide %02d\n\\begin{preview}\\(\\displaystyle %s\\)\\end{preview}'
        % (i + 1, f['lesson'], f['slide'], f['tex']) for i, f in enumerate(formulas)
    ) + '\n\\end{document}\n')
    result = subprocess.run([tectonic, '--untrusted', '--keep-logs', '--reruns', '0', str(source)],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (work / 'compiler-output.txt').write_text(result.stdout)
    if result.returncode:
        raise RuntimeError(result.stdout[-8000:])
    doc = fitz.open(work / 'formulas.pdf')
    if len(doc) != len(formulas):
        raise ValueError(f'Expected {len(formulas)} typed formulas; LaTeX produced {len(doc)} pages')
    if any(page.get_images() for page in doc):
        raise ValueError('Formula pages must contain typed math, not raster images')
    return doc


def pack_group(group, dimensions, width, scale):
    """Place consecutive formulas left-to-right, then continue on the next row."""
    header, row_gap, item_gap, end_gap = 4.7, 1.2, 4.0, 2.4
    x, y, row_height = 0.0, header, 0.0
    placements = []
    for i in group['indices']:
        w, h = dimensions[i]
        effective = min(scale, width / w)
        w, h = w * effective, h * effective
        if x and x + w > width + 1e-7:
            x, y, row_height = 0.0, y + row_height + row_gap, 0.0
        placements.append({'index': i, 'x': x, 'y': y, 'width': w, 'height': h, 'scale': effective})
        x += w + item_gap
        row_height = max(row_height, h)
    return placements, y + row_height + end_gap


def layout(groups, dimensions, columns, scale, width, height):
    gap = 6.0
    column_width = (width - gap * (columns - 1)) / columns
    col, y, blocks = 0, 0.0, []
    for group in groups:
        placements, block_height = pack_group(group, dimensions, column_width, scale)
        if block_height > height:
            return None
        if y + block_height > height:
            col, y = col + 1, 0.0
        if col >= columns:
            return None
        blocks.append({'group': group, 'x': col * (column_width + gap), 'y': y,
                       'height': block_height, 'placements': placements})
        y += block_height
    return blocks


def compose(content, output, work, tectonic):
    groups, formulas = formulas_from(content)
    if not formulas:
        raise ValueError('No formulas to typeset')
    doc = typeset(formulas, work, tectonic)
    dimensions = [(p.rect.width, p.rect.height) for p in doc]
    page_rect = fitz.Rect(0, 0, 842, 595)
    margin, top, bottom = 12.0, 29.0, 14.0
    width, height = page_rect.width - margin * 2, page_rect.height - top - bottom
    candidates = []
    for columns in range(4, 15):
        lo, hi = .02, 1.0
        if layout(groups, dimensions, columns, lo, width, height) is None:
            continue
        for _ in range(28):
            mid = (lo + hi) / 2
            if layout(groups, dimensions, columns, mid, width, height) is None:
                hi = mid
            else:
                lo = mid
        blocks = layout(groups, dimensions, columns, lo, width, height)
        scales = [p['scale'] for b in blocks for p in b['placements']]
        score = math.exp(sum(math.log(s) for s in scales) / len(scales))
        candidates.append((score, lo, columns, blocks))
    if not candidates:
        raise ValueError('All formulas could not fit on one page')
    _, scale, columns, blocks = max(candidates, key=lambda c: c[:3])
    pdf = fitz.open()
    page = pdf.new_page(width=page_rect.width, height=page_rect.height)
    page.insert_text((margin, 14), 'FORMULAS FROM PDFs 01-09', fontsize=9, fontname='hebo')
    page.insert_text((margin, 23), 'Original notation and teaching order | Read down each column; read each row from left to right', fontsize=5)
    page.draw_line((margin, 26), (page_rect.width - margin, 26), color=(.25, .25, .25), width=.3)
    column_width = (width - 6 * (columns - 1)) / columns
    for col in range(1, columns):
        x = margin + col * (column_width + 6) - 3
        page.draw_line((x, top), (x, page_rect.height - bottom), color=(.78, .78, .78), width=.15)
    placed = []
    for block in blocks:
        group = block['group']
        x, y = margin + block['x'], top + block['y']
        page.insert_text((x, y + 3.2), f"PDF {group['lesson']:02} / slide {group['slide']:02}", fontsize=3.1, fontname='hebo')
        for p in block['placements']:
            rect = fitz.Rect(x + p['x'], y + p['y'], x + p['x'] + p['width'], y + p['y'] + p['height'])
            assert page_rect.contains(rect)
            # The complete page is freshly typeset formula text, never a slide crop.
            page.show_pdf_page(rect, doc, p['index'])
            placed.append({'index': p['index'], 'rect': list(rect), 'font_size': 10 * p['scale']})
    assert [p['index'] for p in placed] == list(range(len(formulas)))
    page.insert_text((margin, page_rect.height - 6), 'STAT 5701 - Dobrin Marchev | PDFs 01-09 only | One A4 landscape page', fontsize=4.4)
    pdf.set_metadata({'title': 'Typed formulas from PDFs 01-09', 'subject': 'Original notation and teaching order; all formulas typeset from text', 'author': 'Source slides: Dobrin Marchev, STAT 5701'})
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(output, garbage=3, deflate=True)
    checked = fitz.open(output)
    assert len(checked) == 1 and not checked[0].get_images()
    meta = {'pages': 1, 'audited_slides': sum(len(l['pages']) for l in content['lessons']),
            'formula_slides': len(groups), 'formulas': len(formulas), 'columns': columns,
            'base_font_size': 10 * scale, 'minimum_font_size': min(p['font_size'] for p in placed),
            'images': len(checked[0].get_images()), 'bytes': output.stat().st_size}
    (work / 'layout.json').write_text(json.dumps({'summary': meta, 'placements': placed, 'formulas': formulas}, indent=2))
    print(json.dumps(meta, indent=2))
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tectonic', default=os.environ.get('TECTONIC', shutil.which('tectonic')))
    parser.add_argument('--work-dir', type=Path, default=ROOT / 'tmp/formula-sheet')
    parser.add_argument('--output', type=Path, default=ROOT / 'assets/downloads/probability-statistics-exam-cheat-sheet.pdf')
    parser.add_argument('--draft-content', type=Path, help='Optional draft input; never used by the website build')
    args = parser.parse_args()
    if not args.tectonic:
        parser.error('Install Tectonic or pass --tectonic /path/to/tectonic')
    content = json.loads(args.draft_content.read_text()) if args.draft_content else load_cheat_sheet(ROOT, check_pdf=False)
    args.work_dir.mkdir(parents=True, exist_ok=True)
    compose(content, args.output, args.work_dir.resolve(), str(Path(args.tectonic).resolve()))
