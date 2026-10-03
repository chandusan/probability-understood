# Probability, understood

A slide-by-slide teaching companion to **01 Data Summary** and **02 Probability · Part 1**. Each of the 74 pages starts with the original slide image, then develops its ideas through intuition, worked examples, proofs, and questions from our study sessions.

**[Open the Data Summary companion](https://chandusan.github.io/probability-understood/)**

**[Open Probability · Part 1](https://chandusan.github.io/probability-understood/probability-part1/01.html)**

The chapter selector switches between the two companions. The previous six-lesson site is preserved in Git at `archive/before-slide-rebuild-2026-10-03`.

## What is included

- All 74 original slides, rendered at 2,000 pixels wide and expandable for reading.
- Rich explanations of every slide, including the full exercise solutions and qualifications where the source wording is imprecise.
- 12 Data Summary experiments: projection, absolute/squared loss, L1/L2 boundaries, a growing octahedron, outlier sensitivity, min–max scaling, percentile interpolation, boxplots, Bessel's correction, standardization, PCA, and the empirical rule.
- 11 Probability experiments: coin frequencies, binomial counts, crossing chords, Buffon’s needle, uniform densities, set operations, rectangles, partial orders, De Morgan’s laws, car turns, and dice sums.
- Expandable proofs and worked understanding checks.
- Slide search, previous/next navigation, a local section outline, and browser-local study progress tracked separately for each chapter.
- Local math rendering and chart dependencies. Reading and experiments do not require an account or an external service.

## Preview locally

The built site is already in `docs/`. From this repository:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Open <http://127.0.0.1:8765/>. Everything uses relative paths, including slide images and experiments, so this preview uses the same output as GitHub Pages.

## Edit and rebuild

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py
```

Edit Data Summary explanations in `content/slides/01.md` through `31.md`, and Probability Part 1 in `content/probability-part1/01.md` through `43.md`. Each file starts with a title and an introductory paragraph. Standard Markdown, TeX math, tables, and `<details markdown="1">` sections are supported.

The page layout and slide navigation are assembled in `build.py`; the reading interface is in `src/site.css` and `src/site.js`. Experiments are authored in `src/labs/`, with shared styles and local state/height handling in `src/lab.css` and `src/lab-frame.js`.

The builder recreates `docs/` from these sources. Do not edit generated pages directly. It validates all 74 expected source files, slide images, and experiment references before replacing the generated directory.

The preserved PDFs live in `assets/source/`. Data Summary images are in `assets/slides/`; Probability Part 1 images are in `assets/slides/probability-part1/`. To regenerate images, use `scripts/render_slides.py --chapter all` with Poppler and Pillow available; image regeneration is not part of the normal build.

## Publishing

GitHub Pages serves `docs/` from `main`. After editing and rebuilding, commit both the source and generated pages; pushing to `main` publishes the update. The historical `01-data.html` link redirects to the first slide. The historical `02-foundations.html` link redirects to Probability Part 1. Chapter 01 URLs and stored progress remain compatible. Other chapters and the former audit pages are absent from this rebuild.

## Sources and attribution

Original slides: **Dobrin Marchev, STAT 5701**, from the supplied `01-DataSummary.pdf` and `02-Probability-Part1.pdf`. Slide images and source material remain attributed to their author. Explanations, examples, proofs, corrections, and experiments are an independent personal study companion, not an official course publication.

Original sources: [Data Summary](https://drive.google.com/file/d/10qzlEP0KcW0O1Prun81YHoZrWd50y3OY/view), [Probability Part 1](https://drive.google.com/file/d/1hRhUQHsHpt8Iltyr2HL3YMRuVfV3KgrR/view).

Probability slide numbers follow PDF page order; some printed footer numbers differ. The source images are preserved unchanged, while the teaching text explicitly qualifies source assumptions where needed. Your questions about orientation, continuous density, set inclusion, and infinite operations are integrated into the relevant lessons.

Vendored dependencies: KaTeX 0.16.22 (MIT) and D3 7.9.0 (ISC). Their licenses are included under `assets/vendor/`. The build dependency is Python-Markdown 3.8.2.
