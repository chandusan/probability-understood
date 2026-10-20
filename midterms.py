"""Build independent midterm practice and worked-solution pages."""
import html
from cheat_sheet import download_panel
import json
import re
from pathlib import Path


def load_midterms(root):
    """Validate every paper and source PDF before the main build replaces docs/."""
    papers = []
    for path in sorted((root / 'content/midterms').glob('*.json')):
        paper = json.loads(path.read_text())
        label = f'{path}: '
        year = paper.get('year')
        if isinstance(year, bool) or not isinstance(year, (str, int)) or not re.fullmatch(r'\d{4}', str(year)) or str(year) != path.stem:
            raise ValueError(label + 'year must be a four-digit year matching the JSON filename')
        paper['year'] = int(year)
        for key in ('title', 'subtitle', 'intro', 'solution_pdf'):
            if not isinstance(paper.get(key), str) or not paper[key].strip():
                raise ValueError(label + f'missing {key}')
        if not isinstance(paper.get('notes'), list) or not all(isinstance(n, str) for n in paper['notes']):
            raise ValueError(label + 'notes must be a list of strings')
        for key in ('question_pdf', 'solution_pdf'):
            name = paper.get(key)
            if name is None and key == 'question_pdf':
                continue
            if not isinstance(name, str) or Path(name).name != name or not name.endswith('.pdf'):
                raise ValueError(label + f'{key} must name a PDF in assets/source/midterms')
            if not (root / 'assets/source/midterms' / name).is_file():
                raise ValueError(label + f'missing source PDF: {name}')
        questions = paper.get('questions')
        if not isinstance(questions, list) or not questions:
            raise ValueError(label + 'no questions')
        for number, question in enumerate(questions, 1):
            if question.get('number') != number:
                raise ValueError(label + 'question numbers must be consecutive, starting at 1')
            for key in ('title', 'question', 'solution'):
                if not isinstance(question.get(key), str) or not question[key].strip():
                    raise ValueError(label + f'question {number}: missing {key}')
            if not isinstance(question.get('parts'), list) or not all(isinstance(p, str) for p in question['parts']):
                raise ValueError(label + f'question {number}: invalid parts')
            if not isinstance(question.get('source_pages'), list) or not question['source_pages'] or not all(isinstance(p, int) and p > 0 for p in question['source_pages']):
                raise ValueError(label + f'question {number}: invalid source_pages')
        papers.append(paper)
    if not papers:
        raise ValueError('No midterm papers found in content/midterms/')
    return papers


def render_fragment(source, prefix, render_md):
    """Give repeated part headings and their local links unique IDs."""
    rendered = render_md(source)
    ids = re.findall(r'\bid="([^"]+)"', rendered)
    for anchor in sorted(ids, key=len, reverse=True):
        new = f'{prefix}-{anchor}'
        rendered = rendered.replace(f'id="{anchor}"', f'id="{new}"')
        rendered = rendered.replace(f'href="#{anchor}"', f'href="#{new}"')
    return rendered


def mode_links(year, mode, prefix=''):
    return '<nav class="midterm-mode" aria-label="Choose questions or solutions">' + ''.join(
        f'<a href="{prefix}{name}.html"' + (' aria-current="page"' if mode == name else '') + f'>{label}</a>'
        for name, label in [('questions', 'Questions'), ('solutions', 'Questions with solutions')]
    ) + '</nav>'


def question_links(paper):
    return ''.join(
        f'<a href="#question-{q["number"]}"><span class="midterm-nav-number">{q["number"]:02}</span><span>{html.escape(q["title"])}</span></a>'
        for q in paper['questions']
    )


def page_frame(*, title, description, prefix, breadcrumb, content, sidebar, toc, tools, chapter_navigation, page_class):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(description, quote=True)}"><title>{html.escape(title)} — Probability, understood</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css"><link rel="stylesheet" href="{prefix}assets/midterms.css"><link rel="stylesheet" href="{prefix}assets/cheat-sheet.css?v=source-formulas-2"><link rel="stylesheet" href="{prefix}assets/vendor/katex/katex.min.css"><script defer src="{prefix}assets/vendor/katex/katex.min.js"></script><script defer src="{prefix}assets/vendor/katex/contrib/auto-render.min.js"></script><script defer src="{prefix}assets/site.js"></script></head>
<body class="midterms-page {page_class}"><a class="skip" href="#lesson">Skip to the {('papers' if page_class == 'midterms-index' else 'questions')}</a>
<aside class="sidebar" aria-label="Midterm navigation"><a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Probability,<br>understood.</span></a><button class="nav-close" data-close-nav aria-label="Close navigation">×</button><p class="course-label">Your study companion</p>{chapter_navigation(prefix)}<p class="course-title">Midterms</p><nav class="slide-nav midterm-nav" aria-label="Papers and questions">{sidebar}</nav><div class="nav-footer"><a class="appendix-link" href="{prefix}exercises/index.html">Lesson exercises</a><a class="appendix-link" href="{prefix}midterms/index.html">All midterms</a><a class="appendix-link" href="{prefix}cheat-sheet/index.html">Exam cheat sheet · PDF</a><a class="appendix-link" href="{prefix}appendix/calculus.html">Calculus appendix</a><span>Try it yourself. Then understand every step.</span></div></aside>
<button class="scrim" data-close-nav aria-label="Close navigation"></button><div class="site-body"><header class="topbar"><button class="menu-button" aria-expanded="false" aria-label="Open midterm navigation">☰ Menu</button><div class="breadcrumb">{breadcrumb}</div><div class="top-tools">{tools}</div></header><div class="reading-progress" aria-hidden="true"><i data-reading-progress></i></div>
<div class="page-layout"><main class="lesson" id="lesson">{content}<footer class="footer"><p>Original papers: STAT 5701 · Dobrin Marchev. Source material remains attributed to its author.</p><p>Explanations are an independent personal study companion, not an official course publication.</p></footer></main><aside class="page-toc" aria-label="On this page"><p class="toc-label">On this page</p>{toc}<a href="#lesson">Back to the top ↑</a></aside></div></div></body></html>'''


def hub_page(papers, render_md, chapter_navigation):
    sidebar = ''.join(
        f'<div class="nav-group"><div class="nav-group-title">{html.escape(p["title"])}</div><a href="{p["year"]}/questions.html">Questions</a><a href="{p["year"]}/solutions.html">Questions with solutions</a></div>'
        for p in reversed(papers)
    )
    cards = []
    for paper in reversed(papers):
        year = paper['year']
        total_parts = sum(len(q['parts']) for q in paper['questions'])
        cards.append(f'''<section class="midterm-card" id="year-{year}"><p class="midterm-card-label">{year} paper</p><h2>{html.escape(paper['title'])}</h2><p class="midterm-card-meta">{len(paper['questions'])} questions · {total_parts} parts</p><div class="midterm-card-options"><a class="midterm-option" href="{year}/questions.html"><span class="midterm-option-number">01</span><span><strong>Questions</strong><span>Try every problem independently.</span></span><span aria-hidden="true">→</span></a><a class="midterm-option" href="{year}/solutions.html"><span class="midterm-option-number">02</span><span><strong>Questions with solutions</strong><span>Read the reasoning, one step at a time.</span></span><span aria-hidden="true">→</span></a></div></section>''')
    content = f'''<p class="eyebrow">Practice & understanding</p><h1>Midterms</h1><p class="lead">Choose a year, work through the questions on your own, then follow the solutions to understand each step.</p><div class="lesson-meta"><span>{len(papers)} papers</span><span class="meta-sep">/</span><span>{sum(len(p['questions']) for p in papers)} questions</span><span class="meta-sep">/</span><span>Separate practice and solution pages</span></div>{download_panel('../')}<div class="midterm-cards">{''.join(cards)}</div><p class="midterm-hub-note">Each solutions page repeats the full questions before the explanations, so you can study it on its own. You can also print either version.</p>'''
    toc = ''.join(f'<a href="#year-{p["year"]}">{html.escape(p["title"])}</a>' for p in reversed(papers))
    return page_frame(title='Midterms', description='Past STAT 5701 midterms, with separate questions-only pages and clearly explained worked solutions for each year.', prefix='../', breadcrumb='<strong>Midterms</strong>', content=content, sidebar=sidebar, toc=toc, tools='<button class="plain-button print-button" data-print>Print this page</button>', chapter_navigation=chapter_navigation, page_class='midterms-index')


def paper_page(paper, papers, mode, render_md, chapter_navigation):
    solutions = mode == 'solutions'
    year = paper['year']
    label = 'Questions with solutions' if solutions else 'Questions'
    title = f'{paper["title"]} · {label}'
    sidebar = f'<div class="nav-group"><div class="nav-group-title">{html.escape(paper["title"])}</div><a href="questions.html"'+(' aria-current="page"' if not solutions else '')+'>Questions</a><a href="solutions.html"'+(' aria-current="page"' if solutions else '')+'>Questions with solutions</a></div>'
    sidebar += f'<div class="nav-group"><div class="nav-group-title">Jump to a question</div>{question_links(paper)}</div>'
    sidebar += '<div class="nav-group"><div class="nav-group-title">Other papers</div>' + ''.join(f'<a href="../{p["year"]}/questions.html">{html.escape(p["title"])}</a>' for p in reversed(papers) if p['year'] != year) + '</div>'
    intro = render_fragment(paper['intro'], 'paper-intro', render_md)
    content = f'<p class="eyebrow">Midterms · {label}</p><h1>{html.escape(paper["title"])}</h1><p class="lead">{html.escape(paper["subtitle"])}</p>{mode_links(year, mode)}<div class="paper-intro prose">{intro}</div>'
    if solutions:
        content += '<p class="midterm-mode-note">Each question is followed by its complete worked solution. To practise first, open the questions page.</p>'
    else:
        content += '<p class="midterm-mode-note">Work through the questions at your own pace. Open “Questions with solutions” when you are ready to check your reasoning.</p>'
    if paper.get('question_pdf') and not solutions:
        content += f'<p class="midterm-source"><a href="../../assets/source/midterms/{html.escape(paper["question_pdf"], quote=True)}" target="_blank" rel="noopener">Original questions PDF ↗</a></p>'
    # A questions-only page never renders notes, answers, or links to an answer key.
    if solutions and paper['notes']:
        content += '<aside class="midterm-notes prose" aria-label="Reading the source paper"><h2 id="source-notes">About the source</h2>' + ''.join(render_fragment(note, f'source-note-{n}', render_md) for n, note in enumerate(paper['notes'], 1)) + '</aside>'
    content += '<div class="midterm-questions">'
    for question in paper['questions']:
        n = question['number']
        prompt = render_fragment(question['question'], f'question-{n}-prompt', render_md)
        content += f'<section class="midterm-question" id="question-{n}" aria-labelledby="question-{n}-title"><div class="midterm-question-heading"><span class="midterm-question-number">{n:02}</span><h2 id="question-{n}-title">{html.escape(question["title"])}</h2></div><div class="question-prompt prose">{prompt}</div>'
        if solutions:
            worked = render_fragment(question['solution'], f'question-{n}-solution', render_md)
            pages = ', '.join(str(p) for p in question['source_pages'])
            content += f'<div class="question-solution"><h3 class="solution-label" id="question-{n}-worked-solution">Worked solution</h3><div class="prose">{worked}</div></div><p class="midterm-source">Source: original paper, {"pages" if len(question["source_pages"]) > 1 else "page"} {pages}.</p>'
        content += '</section>'
    content += '</div>'
    if solutions:
        content += f'<section class="midterm-source-end" id="original-paper"><h2>Original answer key</h2><p>Compare these explanations with the preserved source.</p><a href="../../assets/source/midterms/{html.escape(paper["solution_pdf"], quote=True)}" target="_blank" rel="noopener">Open original answer key PDF ↗</a></section>'
    content += f'<nav class="midterm-bottom" aria-label="Continue studying"><a href="../index.html">← All midterms</a><a href="{"questions" if solutions else "solutions"}.html">{"Try the questions" if solutions else "Read the solutions"} →</a></nav>'
    toc = question_links(paper)
    tools = '<button class="plain-button print-button" data-print>Print '+('with solutions' if solutions else 'questions')+'</button>'
    return page_frame(title=title, description=f'{paper["title"]}: '+('the full questions with step-by-step worked solutions.' if solutions else 'all questions in a separate practice paper.'), prefix='../../', breadcrumb=f'<span class="crumb-course"><a href="../index.html">Midterms</a> / </span><strong>{html.escape(paper["title"])}</strong>', content=content, sidebar=sidebar, toc=toc, tools=tools, chapter_navigation=chapter_navigation, page_class='midterm-solutions' if solutions else 'midterm-practice')


def build_midterms(root, out, render_md, chapter_navigation, papers=None):
    papers = load_midterms(root) if papers is None else papers
    folder = out / 'midterms'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(hub_page(papers, render_md, chapter_navigation))
    for paper in papers:
        destination = folder / str(paper['year'])
        destination.mkdir(parents=True, exist_ok=True)
        for mode in ('questions', 'solutions'):
            (destination / f'{mode}.html').write_text(paper_page(paper, papers, mode, render_md, chapter_navigation))
    return len(papers)
