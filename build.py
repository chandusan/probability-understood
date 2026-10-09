"""Build the slide-by-slide probability and statistics companions. No network needed."""
from pathlib import Path
import html
import json
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
GROUPS = [(1, 2, 'The starting point'), (3, 12, 'Finding the centre'), (13, 22, 'Understanding spread'), (23, 26, 'Variance & its uses'), (27, 31, 'Normal models & practice')]
SHORT_TITLES = ['A story inside the data', 'What does “centre” mean?', 'The mean: equal shares', 'Why squared error finds the mean', 'The geometry of the mean', 'Finding the median', 'Why absolute error finds the median', 'Spheres, diamonds & octahedra', 'One observation changes', 'Reading the geometric picture', 'Which centre should we use?', 'Skewness & the long tail', 'Why an 88 needs context', 'What spread tells us', 'Range & population support', 'Min–max scaling & outliers', 'Percentiles & interpolation', 'Quartiles & probability', 'The middle half: IQR', 'Diamonds: the first sample', 'Add two expensive diamonds', 'Reading a boxplot', 'Variance, estimation & n − 1', 'PCA, scaling & model variance', 'Population versus sample', 'Interpreting standard deviation', 'Birth weights & the bell curve', 'The 68–95–99.7 rule', 'Heart rates: every calculation', 'Which professor varies most?', 'Four ways to change the spread']
LAB_TITLES = {'mean-projection':'The mean as an orthogonal projection', 'loss':'Mean and median loss functions', 'norms':'L1 and L2 distance boundaries', 'octahedron':'Grow an octahedron toward the median', 'outlier':'Move an outlier: mean versus median', 'minmax':'Min–max scaling with an extreme value', 'quantile':'Interpolate a percentile rank', 'boxplot':'The diamonds boxplot', 'variance':'Pairwise comparisons and Bessel’s correction', 'pca':'Rotate a PCA direction', 'standardize':'Measure age and income in standard deviations', 'normal':'Explore the empirical rule'}

LAB_TITLES.update({
    'prob-coin':'Watch a coin frequency settle',
    'prob-binomial':'Count sixes across ten dice',
    'prob-chords':'Which pairs of chords cross?',
    'prob-needle':'Fold the angle and cross a line',
    'prob-uniform':'Density, interval width and probability',
    'prob-events':'Build and combine events',
    'prob-rectangles':'Union and intersection in the plane',
    'prob-inclusion':'Explore a partial order of sets',
    'prob-demorgan':'See De Morgan’s laws one outcome at a time',
    'prob-cars':'Three turns with an adjustable right-turn probability',
    'prob-dice':'Count outcomes in the two-dice grid',
    'count-tree':'Build a counting tree one choice at a time',
    'count-cards':'See where the ace and diamond counts overlap',
    'count-arrangements':'Turn ordered arrangements into groups',
    'count-stars':'Turn repeated choices into stars and bars',
    'count-series':'Build a generalized binomial series term by term',
    'count-pipeline':'Count feature pipelines with constraints',
    'count-lottery':'Count every possible lottery match',
    'count-poker':'Build and compare five-card poker hands',
    'count-tournament':'Why two players meet with probability two over n',
    'rules-occupancy':'Explore the load of one chosen bin',
    'rules-birthday':'Compare birthday collision events',
    'rules-multiset':'Count arrangements of repeated letters',
    'rules-overlap':'Change event overlap and the union',
    'rules-bridge':'Compare exact and minimum bridge suit counts',
    'rules-inclusion':'Count one outcome through inclusion–exclusion',
    'rules-coverage':'Make every die face appear',
    'rules-derangements':'Avoid your own name in a random permutation',
    'cond-events':'Keep only the outcomes allowed by the condition',
    'cond-coins':'Check pairwise and mutual independence with four tosses',
    'cond-bayes':'See how base rates change a positive-test probability',
    'cond-urns':'Update the urn, then predict the next draw',
    'cond-ruin':'Compare one-step and eventual winning probabilities',
})
CHAPTERS = [
    {'id':'data-summary','number':'01','title':'Data Summary','folder':'slides',
     'content':'slides','images':'slides','pdf':'01-data-summary.pdf','height':1125,
     'groups':GROUPS,'titles':SHORT_TITLES,'legacy':'01-data.html'},
    {'id':'probability-part1','number':'02','title':'Probability · Part 1','folder':'probability-part1',
     'content':'probability-part1','images':'slides/probability-part1','pdf':'02-probability-part1.pdf','height':1500,
     'groups':[(1,4,'From data to uncertainty'),(5,10,'Experiments & random outcomes'),(11,17,'Building a sample space'),(18,27,'The language of events'),(28,34,'Set laws & inclusion'),(35,39,'Many events & probability rules'),(40,43,'Counting equally likely outcomes')],
     'titles':['From observed data to possible worlds','What makes a system deterministic?','What does a random error mean?','Randomness, chaos & predictability','A coin’s long-run regularity','Two dice, 36 distinct outcomes','Count the sixes in ten dice','A needle, a floor & a probability','A whole price path is one outcome','When do two random chords cross?','A language for uncertainty','What belongs in a sample space?','Countable versus uncountable','Counting a grid of possibilities','Describe a needle’s landing','Coordinates for a random needle','Orientation, uniformity & crossing','An event is a set of outcomes','Membership: an outcome in an event','Three cars, eight possible stories','Impossible and certain events','Union: at least one event happens','Intersection: both events happen','Overlapping rectangles','Complement: everything outside an event','Translate words into sets','Work the die example','Why the set laws work','Split an event into two pieces','Empty space and the whole space','Disjoint means at most one','Inclusion makes a partial order','Three consequences of inclusion','Which inclusions are always true?','From two events to a family','Union over many events','Intersection over many events','De Morgan’s laws for any family','Three axioms that hold it together','When counting becomes probability','Three cars: counting and weighting','Two dice: sums of at least ten','A complete probability argument'],
     'legacy':'02-foundations.html'},
    {'id':'counting','number':'03','title':'Counting','folder':'counting',
     'content':'counting','images':'slides/counting','pdf':'03-counting.pdf','height':1500,
     'groups':[(1,8,'Probability meets counting'),(9,18,'Build choices step by step'),(19,27,'Order, groups & constraints'),(28,34,'Coefficients & repeated choices'),(35,40,'A lottery, counted carefully'),(41,51,'The anatomy of poker hands'),(52,53,'Two final challenges')],
     'titles':['Why counting unlocks probability','The three probability axioms','What is a probability space?','When outcomes are equally likely','Three cars, counted carefully','Two dice: solve the exercise','Probability rules as bookkeeping','An ace or a diamond?','The art of counting once','Add disjoint alternatives','Multiply sequential choices','Read a counting tree','Gold and silver among eight finalists','Extend the multiplication rule','Follow a three-stage tree','Count the licence plates','Factorials: arranging everything','All 24 orders of four letters','Keep each subject together','Arrange only some of the objects','Assign three committee roles','Build a constrained feature pipeline','When order changes the outcome','An all-male executive committee','List the groups of three','Why divide by k factorial?','Understand the choose notation','Where binomial coefficients come from','Extend the binomial theorem','Which counting rule applies?','Build a longer sequence','Repetition and identical objects','Donuts, stars and bars','A strategy for new problems','Six numbers from forty-nine','Prizes and the winning rules','A ticket with no matches','Exactly one match','Two, three or four matches','Five matches and the bonus caveat','The universe of poker hands','Rank patterns and card categories','The rarest poker hands','See the structure of one pair','Count all one-pair hands','Count two-pair hands','Three of a kind and full houses','Quads and the straight flushes','Ten ways to make a straight','A flush, with straights removed','Check the entire poker distribution','Ten coin tosses: both exercises','Will two tournament players meet?'],
     'legacy':'03-counting.html'},
    {'id':'probability-part2','number':'04','title':'Probability · Part 2','folder':'probability-part2',
     'content':'probability-part2','images':'slides/probability-part2','pdf':'04-probability-part2.pdf','height':1500,
     'groups':[(1,4,'Symmetry before enumeration'),(5,7,'The power of the complement'),(8,13,'Occupancy & birthday collisions'),(14,16,'Repeated objects & rare patterns'),(17,21,'Add probabilities without double counting'),(22,27,'Bridge hands & overlapping events'),(28,34,'Inclusion–exclusion in action'),(35,36,'Permutations & the appearance of e')],
     'titles':['Choose a probability strategy','Will two tennis players meet?','Count matches with symmetry','Why random chords cross one third of the time','Prove the complement rule','Lotto: count matches and define a prize','Six robberies in six districts','The load of one specified bin','Choose the hits, then place the rest','Recognize the binomial distribution','Birthdays: count the collision-free rooms','Derive the birthday product','Why twenty-three people are enough','Arrange a multiset of repeated objects','Can shuffled letters become poetry?','Compute the probability of one exact string','Add two events and remove the overlap','Partition a union into disjoint regions','Derive the addition rule step by step','Two cities in the final five','Translate or, both, neither and exactly one','What makes a bridge hand equally likely?','Four questions about two major suits','Exactly five spades','Hearts, symmetry and dependence','Five spades and five hearts together','Exactly five versus at least five','Add three events without overcounting','Read the seven regions of a Venn diagram','Check every region in the proof','At least one six in three rolls','All six faces in ten rolls','Divisibility and long runs of digits','General inclusion–exclusion','Names in a hat and derangements','Partial derangements and nonrepeatwords'],
     'legacy':'04-rules.html'},
    {'id':'probability-part3','number':'05','title':'Probability · Part 3','folder':'probability-part3',
     'content':'probability-part3','images':'slides/probability-part3','pdf':'05-probability-part3.pdf','height':1500,
     'groups':[(1,6,'Probability after new information'),(7,13,'What independence really means'),(14,20,'Condition on the next draw'),(21,26,'Total probability & Bayes’ rule'),(27,30,'Base rates & evidence'),(31,36,'Update beliefs, then predict'),(37,44,'A random walk to the boundary')],
     'titles':['A roadmap for conditional probability','A die after learning it is even','How information changes the model','Derive the conditional probability formula','Why divide by the condition’s probability?','Neither subscription, given at most one','Independence means unchanged proportions','See independence in a probability grid','Independent versus mutually exclusive','Pairwise versus mutual independence','At least one and exactly one event','Four tosses: pairwise is not enough','A fox’s tags: condition on at most one loss','Multiply probabilities along a path','Three cards: specified order or any order','Two draws from an urn','Name the events before multiplying','Count black then red without replacement','Why the second draw has the original red fraction','Exactly one red, and the very last draw','Derive the law of total probability','Score first, win, and reverse the condition','Bayes’ rule: compare the paths to evidence','Start Bayes’ proof with the right denominator','Factor the intersection in the useful direction','Add every route to the observed evidence','A positive test and a rare condition','Separate sensitivity from the posterior','Correct the test calculation and explain base rates','Bayes’ rule for many possible sources','Two red draws: which urn and what comes next?','Calculate the likelihood within each urn','Update the probability of the chosen urn','Track the balls remaining after the evidence','Predict with the updated urn probabilities','Fraud flags and a second piece of evidence','Gambler’s ruin: state the stopping problem','Random walks: recurrence and meeting are different','Set the boundary probabilities','Condition on the next play','Solve by successive differences and telescoping','An optional characteristic-equation solution','Finish the biased-game calculation','The fair game and the complete answer'],
     'legacy':'05-conditional.html'},
]

def render_md(text):
    """Protect TeX from Markdown escapes and table-pipe parsing."""
    math_parts=[]
    def protect(match):
        math_parts.append(match.group())
        return f'MATHPLACEHOLDER{len(math_parts)-1:05d}END'
    text=re.sub(r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)[^$]+?(?<!\\)\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)',protect,text)
    text=text.replace(r'\$', 'LITERALDOLLARPLACEHOLDER')
    md=markdown.Markdown(extensions=['extra','toc','sane_lists'])
    rendered=md.convert(text)
    rendered=rendered.replace('LITERALDOLLARPLACEHOLDER','<span class="no-math">$</span>')
    for i,tex in enumerate(math_parts):
        rendered=rendered.replace(f'MATHPLACEHOLDER{i:05d}END',html.escape(tex,quote=False))
    return rendered.replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')

def lab_page(name,fragment):
    extras='<link rel="stylesheet" href="../rules-labs.css"><script defer src="../rules-math.js"></script><script defer src="../rules-labs.js"></script>' if name.startswith('rules-') else ''
    if name.startswith('cond-'):
        extras='<link rel="stylesheet" href="../cond-labs.css"><script defer src="../cond-math.js"></script><script defer src="../cond-labs.js"></script>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(LAB_TITLES[name])}</title><link rel="icon" href="data:,"><link rel="stylesheet" href="../lab.css"><script src="../lab-frame.js"></script>{extras}</head><body data-lab="{name}"><main class="lab-root">{fragment}</main></body></html>'''

def build():
    all_slides=[]
    for chapter in CHAPTERS:
        slides=[]
        if not (ROOT/'assets/source'/chapter['pdf']).exists():
            raise ValueError(f"Missing PDF for {chapter['id']}")
        for n,short in enumerate(chapter['titles'],1):
            path=ROOT/'content'/chapter['content']/f'{n:02}.md'
            source=path.read_text()
            match=re.match(r'^# (.+)\n\s*\n([^\n]+(?:\n(?!\n)[^\n]+)*)\n\s*\n',source)
            if not match: raise ValueError(f'{path}: expected title then opening paragraph')
            title,lead=match.groups();body=source[match.end():]
            slots=re.findall(r'data-interactive="([^"]+)"',body)
            for name in slots:
                if name not in LAB_TITLES or not (ROOT/'src/labs'/f'{name}.html').exists():
                    raise ValueError(f'{path}: missing interactive {name}')
            if not (ROOT/'assets'/chapter['images']/f'{n:02}.webp').exists():
                raise ValueError(f"Missing slide image {chapter['id']} {n}")
            words=len(re.sub(r'<[^>]*>|\$[^$]*\$',' ',source).split())
            slides.append({'n':n,'title':title,'short':short,'lead':lead,'body':body,'words':words,'labs':slots})
        chapter['slides']=slides
        all_slides.extend(slides)
    lab_fragments={name:(ROOT/'src/labs'/f'{name}.html').read_text() for name in LAB_TITLES}
    if OUT.exists(): shutil.rmtree(OUT)
    for chapter in CHAPTERS: (OUT/chapter['folder']).mkdir(parents=True)
    shutil.copytree(ROOT/'assets',OUT/'assets')
    for name in ('site.css','site.js','lab.css','lab-frame.js','rules-math.js','rules-labs.js','rules-labs.css','cond-math.js','cond-labs.js','cond-labs.css'): shutil.copyfile(ROOT/'src'/name,OUT/'assets'/name)
    (OUT/'assets/labs').mkdir()
    for name in LAB_TITLES:
        (OUT/'assets/labs'/f'{name}.html').write_text(lab_page(name,lab_fragments[name]))

    def page(s,chapter,home=False):
        slides=chapter['slides'];count=len(slides);titles=chapter['titles']
        n=s['n'];p='' if home else '../';sp=chapter['folder']+'/' if home else ''
        source_href=f"{p}assets/source/{chapter['pdf']}#page={n}"
        chapter_links=''.join(f'<a href="{p}{c["folder"]}/01.html"'+(' aria-current="true"' if c['id']==chapter['id'] else '')+f'><span>{c["number"]}</span> {html.escape(c["title"])}</a>' for c in CHAPTERS)
        chapter_nav=f'<nav class="chapter-nav" aria-label="Choose a chapter">{chapter_links}</nav>'
        page_note='<p class="source-note">Slide numbers follow the PDF page order; the printed footer numbers differ on some slides.</p>' if chapter['number']=='02' else ''
        text=render_md(s['body'])
        def embed(match):
            name=match.group(1);title=html.escape(LAB_TITLES[name])
            return f'<section class="experiment" aria-label="Interactive: {title}"><div class="experiment-label"><span>Explore the idea</span><a href="{p}assets/labs/{name}.html" target="_blank" rel="noopener">Open larger ↗</a></div><iframe src="{p}assets/labs/{name}.html" title="{title}" loading="lazy"></iframe></section>'
        text=re.sub(r'<div class="interactive-slot" data-interactive="([^"]+)">\s*</div>',embed,text)
        toc=''.join(f'<a href="#{anchor}">{re.sub("<[^>]*>","",label)}</a>' for anchor,label in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',text,re.S))
        nav=''
        for a,b,label in chapter['groups']:
            links=''
            for other in slides[a-1:b]:
                num=other['n'];active=' aria-current="page"' if num==n else ''
                search=html.escape(f'{num:02} {other["title"]} {other["short"]}'.lower(),quote=True)
                links+=f'<a class="slide-link" data-slide="{num}" data-search="{search}" href="{sp}{num:02}.html"{active}><span class="slide-num">{num:02}</span><span>{html.escape(other["short"])}</span></a>'
            nav+=f'<div class="nav-group"><div class="nav-group-title">{label}</div>{links}</div>'
        prev=f'<a href="{sp}{n-1:02}.html"><span>← Previous slide</span>{html.escape(titles[n-2])}</a>' if n>1 else '<span></span>'
        chapter_index=CHAPTERS.index(chapter)
        next_chapter=CHAPTERS[chapter_index+1] if chapter_index+1<len(CHAPTERS) else None
        nxt=f'<a href="{sp}{n+1:02}.html"><span>Next slide →</span>{html.escape(titles[n])}</a>' if n<count else (f'<a href="{p}{next_chapter["folder"]}/01.html"><span>Next chapter →</span>{html.escape(next_chapter["title"])}</a>' if next_chapter else f'<a href="{sp}01.html"><span>Back to the beginning →</span>Revisit the ideas</a>')
        group=next(label for a,b,label in chapter['groups'] if a<=n<=b)
        lead=render_md(s['lead']).removeprefix('<p>').removesuffix('</p>')
        title=render_md(s['title']).removeprefix('<p>').removesuffix('</p>')
        minutes=max(2,round(s['words']/170))
        lab_meta=f'<span class="meta-sep">/</span><span>{len(s["labs"])} interactive '+('experiment' if len(s['labs'])==1 else 'experiments')+'</span>' if s['labs'] else ''
        return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Slide {n} of {html.escape(chapter['title'],quote=True)}: {html.escape(s['short'],quote=True)}. Original slide, first-principles explanation, examples and worked practice."><title>{n:02} · {html.escape(s['short'])} — Probability, understood</title><link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{p}assets/site.css"><link rel="stylesheet" href="{p}assets/vendor/katex/katex.min.css"><script defer src="{p}assets/vendor/katex/katex.min.js"></script><script defer src="{p}assets/vendor/katex/contrib/auto-render.min.js"></script><script defer src="{p}assets/site.js"></script></head>
<body data-slide="{n}" data-slide-prefix="{sp}" data-chapter="{chapter['id']}" data-slide-count="{count}"><a class="skip" href="#lesson">Skip to the lesson</a>
<aside class="sidebar" aria-label="Course navigation"><a class="brand" href="{p}index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Probability,<br>understood.</span></a><button class="nav-close" data-close-nav aria-label="Close slide navigation">×</button><p class="course-label">Your study companion</p>{chapter_nav}<p class="course-title">{html.escape(chapter['title'])}</p><label class="sr-only" for="slide-search">Find a slide</label><input class="nav-search" id="slide-search" type="search" placeholder="Find a slide…" autocomplete="off"><nav class="slide-nav" aria-label="All {count} slides">{nav}<p class="no-results" hidden>No matching slides.</p></nav><div class="nav-footer"><span><strong data-completed-count>0</strong> of {count} slides understood</span><div class="progress-track" aria-hidden="true"><i data-course-progress></i></div><span>One idea at a time.</span><br><a data-resume hidden></a></div></aside>
<button class="scrim" data-close-nav aria-label="Close navigation"></button><div class="site-body"><header class="topbar"><button class="menu-button" aria-expanded="false" aria-label="Open slide navigation">☰ Slides</button><div class="breadcrumb"><span class="crumb-course">{html.escape(chapter['title'])} <span aria-hidden="true">/</span> </span><strong>Slide {n:02} of {count}</strong></div><div class="top-tools"><a href="{source_href}" target="_blank" rel="noopener">Original PDF ↗</a><button class="plain-button print-button" data-print>Print this slide</button></div></header><div class="reading-progress" aria-hidden="true"><i data-reading-progress></i></div>
<div class="page-layout"><main class="lesson" id="lesson"><p class="eyebrow">{html.escape(group)} · Slide {n:02}</p><h1>{title}</h1><p class="lead">{lead}</p><div class="lesson-meta"><span>~{minutes} min reading</span><span class="meta-sep">/</span><span>Source + intuition + practice</span>{lab_meta}</div>
<figure class="slide-figure" id="source-slide"><button class="slide-image-button" data-zoom-slide aria-label="Enlarge original slide {n}"><img class="slide-image" src="{p}assets/{chapter['images']}/{n:02}.webp" alt="Original slide {n}: {html.escape(s['short'],quote=True)}. The concepts and figures are explained below." width="2000" height="{chapter['height']}" fetchpriority="high"></button><figcaption class="slide-caption"><span>Original slide · STAT 5701 · Dobrin Marchev</span><button data-zoom-slide>Enlarge slide ↗</button></figcaption></figure>{page_note}
<div class="teaching-heading">Let’s understand it</div><article class="prose">{text}</article>
<section class="lesson-end" aria-label="Study progress"><button class="complete-button" data-complete aria-pressed="false">Mark this slide as understood</button><p class="completion-note">Your reading progress stays in this browser. Revisit any idea whenever you need.</p><nav class="page-turn" aria-label="Previous and next slides">{prev}{nxt}</nav></section>
<footer class="footer"><p>A personal teaching companion built from our questions, examples and explanations.</p><p>Original slides: Dobrin Marchev · STAT 5701. Slide images remain attributed to their author. This is an independent study resource.</p></footer></main>
<aside class="page-toc" aria-label="On this slide"><p class="toc-label">On this slide</p><a class="toc-source" href="#source-slide">The original slide</a>{toc}<a href="#lesson">Back to the top ↑</a></aside></div></div>
<dialog class="image-dialog" aria-label="Original slide {n}, enlarged"><div class="dialog-tools"><span>Slide {n:02} / {count}</span><button data-close-dialog>Close ×</button></div><img src="{p}assets/{chapter['images']}/{n:02}.webp" alt="Enlarged original slide {n}: {html.escape(s['short'],quote=True)}"><div class="dialog-tools"><a href="{source_href}" target="_blank" rel="noopener">Read the source PDF ↗</a></div></dialog></body></html>'''

    manifest=[]
    for chapter in CHAPTERS:
        for s in chapter['slides']:
            file=f"{chapter['folder']}/{s['n']:02}.html"
            (OUT/file).write_text(page(s,chapter))
            manifest.append({'chapter':chapter['id'],'slide':s['n'],'title':s['short'],'file':file,'image':f"assets/{chapter['images']}/{s['n']:02}.webp",'words':s['words'],'interactives':s['labs']})
        target=f"{chapter['folder']}/01.html"
        (OUT/chapter['legacy']).write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><title>{html.escape(chapter["title"])}</title></head><body><a href="{target}">Open {html.escape(chapter["title"])}</a></body></html>')
    (OUT/'index.html').write_text(page(CHAPTERS[0]['slides'][0],CHAPTERS[0],home=True))
    (OUT/'.nojekyll').touch()
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print(f'Built {len(all_slides)} slides across {len(CHAPTERS)} chapters, {sum(s["words"] for s in all_slides):,} words and {len(LAB_TITLES)} interactive experiments.')

if __name__=='__main__': build()
