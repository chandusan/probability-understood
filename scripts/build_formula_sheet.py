"""Compile audited, unchanged source-formula regions onto one A4 page."""
from pathlib import Path
import argparse
import sys

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cheat_sheet import load_cheat_sheet


def read_regions():
    content = load_cheat_sheet(ROOT, check_pdf=False)
    sources, entries = [], []
    for lesson in content['lessons']:
        sources.append({'lesson': lesson['number'], 'pdf': ROOT / 'assets/source' / lesson['source_pdf']})
        for page in lesson['pages']:
            entries.append({'lesson': lesson['number'], 'page': page['number'], 'rects': page['rects']})
    return sources, entries


def place(groups, columns, scale, width, height):
    """Keep every slide's crops together and preserve strict reading order."""
    gap = 5.0
    cw = (width - gap * (columns - 1)) / columns
    col, y = 0, 0
    result = []
    for group in groups:
        rects = group['rects']
        header = 4.2 if group['first'] else 2.7
        gh = header + sum(r.height * scale for r in rects) + max(0, len(rects) - 1) * .65 + 1.2
        if max(r.width * scale for r in rects) > cw or gh > height:
            return None
        if y + gh > height:
            col += 1
            y = 0
        if col >= columns:
            return None
        result.append({'group': group, 'column': col, 'x': col * (cw + gap), 'y': y, 'height': gh, 'header': header})
        y += gh
    return result


def build(output):
    sources, entries = read_regions()
    documents = {s['lesson']: fitz.open(s['pdf']) for s in sources}
    groups, seen = [], set()
    for entry in entries:
        lesson, number = entry['lesson'], entry['page']
        source_page = documents[lesson][number - 1]
        rects = []
        for raw in entry['rects']:
            r = fitz.Rect(raw)
            assert r.width > 0 and r.height > 0 and source_page.rect.contains(r), entry
            rects.append(r)
        if rects:
            groups.append({'lesson': lesson, 'page': number, 'rects': rects, 'first': lesson not in seen})
            seen.add(lesson)
    assert groups, 'No source formulas selected'
    page_rect = fitz.paper_rect('a4-l')
    margin, top, bottom = 12.0, 29.0, 15.0
    width, height = page_rect.width - 2 * margin, page_rect.height - top - bottom
    candidates = []
    for columns in range(4, 19):
        lo, hi = .001, 1.0
        for _ in range(35):
            scale = (lo + hi) / 2
            if place(groups, columns, scale, width, height) is None:
                hi = scale
            else:
                lo = scale
        candidates.append((lo, columns))
    scale, columns = max(candidates)
    layout = place(groups, columns, scale, width, height)
    assert layout is not None
    pdf = fitz.open()
    page = pdf.new_page(width=page_rect.width, height=page_rect.height)
    page.insert_text((margin, 14), 'FORMULAS FROM PDFs 01-09', fontsize=9, fontname='hebo')
    page.insert_text((margin, 23), 'Original slide notation and calculations | Read down each column, then continue to the next', fontsize=5)
    page.draw_line((margin, top - 3), (page_rect.width - margin, top - 3), color=(.25, .25, .25), width=.3)
    cw = (width - 5 * (columns - 1)) / columns
    for c in range(1, columns):
        x = margin + c * (cw + 5) - 2.5
        page.draw_line((x, top), (x, page_rect.height - bottom), color=(.75, .75, .75), width=.15)
    region_count = 0
    for block in layout:
        g = block['group']
        x, y = margin + block['x'], top + block['y']
        label = f"PDF {g['lesson']:02} / slide {g['page']:02}"
        page.insert_text((x, y + block['header'] - .8), label, fontsize=2.7 if g['first'] else 1.9, fontname='hebo')
        y += block['header']
        for crop in g['rects']:
            target = fitz.Rect(x, y, x + crop.width * scale, y + crop.height * scale)
            page.show_pdf_page(target, documents[g['lesson']], g['page'] - 1, clip=crop, keep_proportion=True)
            y += crop.height * scale + .65
            region_count += 1
    page.insert_text((margin, page_rect.height - 6), 'STAT 5701 - Dobrin Marchev | Source formulas reproduced unchanged; PDFs 01-09 only | One A4 landscape page', fontsize=4.4)
    pdf.set_metadata({'title': 'Formulas from PDFs 01-09 - original slide order', 'subject': 'Every audited formula region, reproduced directly from the original slides', 'author': 'Source slides: Dobrin Marchev, STAT 5701'})
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(output, garbage=4, deflate=True)
    check = fitz.open(output)
    assert len(check) == 1
    meta = {'audited_slides': len(entries), 'formula_slides': len(groups), 'regions': region_count, 'columns': columns, 'source_scale': scale, 'page_size': list(page_rect), 'bytes': output.stat().st_size}
    print(meta)
    print(output)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, default=ROOT / 'assets/downloads/probability-statistics-exam-cheat-sheet.pdf')
    build(p.parse_args().output)
