"""Lesson-specific practice, with solutions closed until the reader asks for them."""
import html
import json
import re

from midterms import render_fragment


def load_exercises(root, chapters):
    collections = {}
    for chapter in chapters:
        path = root / 'content/exercises' / f'{chapter["id"]}.json'
        paper = json.loads(path.read_text())
        if paper.get('chapter_id') != chapter['id']:
            raise ValueError(f'{path}: chapter_id must match its chapter')
        entries = paper.get('exercises')
        if not isinstance(entries, list) or not entries:
            raise ValueError(f'{path}: expected at least one source exercise')
        ids = set()
        for entry in entries:
            anchor = entry.get('id', '')
            if not re.fullmatch(r'slide-[a-z0-9-]+', anchor) or anchor in ids:
                raise ValueError(f'{path}: exercise ids must be unique and start with slide-')
            ids.add(anchor)
            for field in ('title', 'question', 'solution'):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    raise ValueError(f'{path}, {anchor}: missing {field}')
            pages = entry.get('source_pages')
            if not isinstance(pages, list) or not pages or any(type(n) is not int or not 1 <= n <= len(chapter['titles']) for n in pages):
                raise ValueError(f'{path}, {anchor}: invalid source pages')
            if pages != sorted(set(pages)):
                raise ValueError(f'{path}, {anchor}: source pages must be sorted and unique')
            if not isinstance(entry.get('parts'), list) or not all(isinstance(p, str) and p for p in entry['parts']):
                raise ValueError(f'{path}, {anchor}: missing question parts')
        collections[chapter['id']] = paper
    return collections


def exercise_count_label(count):
    return f'{count} exercise' + ('' if count == 1 else 's')


def exercise_anchor(entry):
    return 'exercise-' + entry['id']


def render_cards(paper, chapter, render_md, prefix):
    cards = []
    for n, entry in enumerate(paper['exercises'], 1):
        anchor = exercise_anchor(entry)
        question = render_fragment(entry['question'], anchor + '-question', render_md)
        solution = render_fragment(entry['solution'], anchor + '-solution', render_md)
        # Figure references remain identical in the end-of-lesson and collection views.
        question = question.replace('src="@assets/', f'src="{prefix}assets/')
        solution = solution.replace('src="@assets/', f'src="{prefix}assets/')
        pages = ', '.join(str(p) for p in entry['source_pages'])
        label = 'Slide' if len(entry['source_pages']) == 1 else 'Slides'
        source_links = ' · '.join(f'<a href="{prefix}{chapter["folder"]}/{p:02}.html">Slide {p}</a>' for p in entry['source_pages'])
        cards.append(f'''<section class="exercise-card" id="{anchor}" aria-labelledby="{anchor}-title">
<p class="exercise-meta">Exercise {n:02} <span aria-hidden="true">/</span> {label} {pages}</p>
<h3 id="{anchor}-title">{html.escape(entry['title'])}</h3><div class="prose exercise-question">{question}</div>
<details class="exercise-solution" data-exercise-solution><summary><span class="solution-closed-label">Show solution</span><span class="solution-open-label">Hide solution</span><span class="sr-only">: {html.escape(entry['title'])}</span></summary>
<div class="prose exercise-solution-body">{solution}</div><p class="exercise-source">Return to the explanation: {source_links}. <a href="{prefix}assets/source/{chapter['pdf']}#page={entry['source_pages'][0]}" target="_blank" rel="noopener">Original PDF ↗</a></p></details></section>''')
    return ''.join(cards)


def lesson_exercise_section(paper, chapter, render_md, prefix):
    count = len(paper['exercises'])
    return f'''<section class="lesson-exercises" id="lesson-exercises" aria-labelledby="lesson-exercises-title"><p class="eyebrow">Try it yourself</p><h2 id="lesson-exercises-title">Lesson {chapter['number']} exercises</h2><p class="exercise-intro">{exercise_count_label(count)} from this lesson. Try each question first, then open its solution for a step-by-step explanation.</p><p class="exercise-collection-link"><a href="{prefix}exercises/{chapter['id']}.html">Open this lesson’s exercise collection →</a> <span>·</span> <a href="{prefix}exercises/index.html">All lessons</a></p>{render_cards(paper, chapter, render_md, prefix)}</section>'''


def collection_links(chapters, collections, current=None):
    return ''.join(f'<a href="{c["id"]}.html"'+(' aria-current="page"' if current == c['id'] else '')+f'><span>{c["number"]}</span><span>{html.escape(c["title"])}<small>{exercise_count_label(len(collections[c["id"]]["exercises"]))}</small></span></a>' for c in chapters)


def frame(title, content, sidebar, toc, chapter_navigation, current=None):
    label = html.escape(title)
    print_tools = ('<button class="plain-button print-button" data-print>Print questions</button><button class="plain-button print-button" data-print-solutions>Print with solutions</button>' if current else '<button class="plain-button print-button" data-print>Print lesson list</button>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Exercises from the lesson PDFs, with complete questions and clearly explained solutions you can reveal when ready."><title>{label} — Probability, understood</title><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/exercises.css"><link rel="stylesheet" href="../assets/vendor/katex/katex.min.css"><script defer src="../assets/vendor/katex/katex.min.js"></script><script defer src="../assets/vendor/katex/contrib/auto-render.min.js"></script><script defer src="../assets/site.js"></script></head>
<body class="exercises-page"><a class="skip" href="#lesson">Skip to the exercises</a><aside class="sidebar" aria-label="Exercise navigation"><a class="brand" href="../index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Probability,<br>understood.</span></a><button class="nav-close" data-close-nav aria-label="Close navigation">×</button><p class="course-label">Your study companion</p>{chapter_navigation('../',current)}<p class="course-title">Lesson exercises</p><nav class="slide-nav exercise-nav" aria-label="Exercises by lesson">{sidebar}</nav><div class="nav-footer"><a class="appendix-link" href="index.html">All lesson exercises</a><a class="appendix-link" href="../midterms/index.html">Midterms · questions &amp; solutions</a><a class="appendix-link" href="../cheat-sheet/index.html">Exam cheat sheet · PDF</a><a class="appendix-link" href="../appendix/calculus.html">Calculus appendix</a><span>Try the question. Reveal the reasoning.</span></div></aside><button class="scrim" data-close-nav aria-label="Close navigation"></button><div class="site-body"><header class="topbar"><button class="menu-button" aria-expanded="false" aria-label="Open exercise navigation">☰ Menu</button><div class="breadcrumb"><strong>{label}</strong></div><div class="top-tools">{print_tools}</div></header><div class="reading-progress" aria-hidden="true"><i data-reading-progress></i></div><div class="page-layout"><main class="lesson" id="lesson">{content}<footer class="footer"><p>Original exercises: Dobrin Marchev · STAT 5701. Explanations are an independent study companion.</p></footer></main><aside class="page-toc" aria-label="On this page"><p class="toc-label">On this page</p>{toc}<a href="#lesson">Back to the top ↑</a></aside></div></div></body></html>'''


def build_exercises(out, chapters, collections, render_md, chapter_navigation):
    folder = out / 'exercises'
    folder.mkdir(parents=True, exist_ok=True)
    total = sum(len(p['exercises']) for p in collections.values())
    cards = []
    for chapter in chapters:
        paper = collections[chapter['id']]
        count = len(paper['exercises'])
        cards.append(f'''<a class="exercise-lesson-card" href="{chapter['id']}.html" id="lesson-{chapter['number']}"><span class="exercise-lesson-number">{chapter['number']}</span><span><h2>{html.escape(chapter['title'])}</h2><span>{exercise_count_label(count)} · solutions closed until you open them</span></span><span aria-hidden="true">→</span></a>''')
        toc = ''.join(f'<a href="#{exercise_anchor(e)}">{i:02} · {html.escape(e["title"])}</a>' for i, e in enumerate(paper['exercises'],1))
        content = f'''<p class="eyebrow">Practice · Lesson {chapter['number']}</p><h1>{html.escape(chapter['title'])}</h1><p class="lead">Exercises</p><p class="exercise-intro">Work through the questions independently. Each solution starts closed; open it when you are ready for the reasoning and calculations.</p><div class="lesson-meta"><span>{exercise_count_label(count)}</span><span class="meta-sep">/</span><a href="../{chapter['folder']}/01.html">Read the lesson</a><span class="meta-sep">/</span><a href="index.html">All lesson exercises</a></div><div class="exercise-list"><h2 class="sr-only">Questions and solutions</h2>{render_cards(paper, chapter, render_md, '../')}</div>'''
        (folder / f'{chapter["id"]}.html').write_text(frame(f'Lesson {chapter["number"]} exercises',content,collection_links(chapters,collections,chapter['id']),toc,chapter_navigation,chapter['id']))
    toc = ''.join(f'<a href="#lesson-{c["number"]}">{c["number"]} · {html.escape(c["title"])}</a>' for c in chapters)
    content = f'''<p class="eyebrow">Try it yourself</p><h1>Lesson exercises</h1><p class="lead">Questions from each lesson PDF, collected in one place. Try them first, then reveal a solution whenever you need it.</p><div class="lesson-meta"><span>{len(chapters)} lessons</span><span class="meta-sep">/</span><span>{total} exercises</span></div><div class="exercise-lesson-list">{''.join(cards)}</div><p class="exercise-intro exercise-scope">These collections gather the PDFs’ exercises and standalone practice questions. Related subparts stay together, with their original slide numbers. Worked examples remain in the lessons.</p>'''
    (folder / 'index.html').write_text(frame('Lesson exercises',content,collection_links(chapters,collections),toc,chapter_navigation))
    return total
