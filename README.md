# Probability, understood

A slide-by-slide teaching companion to **01 Data Summary**, **02 Probability · Part 1**, **03 Counting**, **04 Probability · Part 2**, and **05 Probability · Part 3**. Each of the 207 pages starts with the original slide image, then develops its ideas through intuition, worked examples, proofs, and questions from our study sessions.

**[Open the Data Summary companion](https://chandusan.github.io/probability-understood/)**

**[Open Probability · Part 1](https://chandusan.github.io/probability-understood/probability-part1/01.html)**

**[Open Counting](https://chandusan.github.io/probability-understood/counting/01.html)**

**[Open Probability · Part 2](https://chandusan.github.io/probability-understood/probability-part2/01.html)**

**[Open Probability · Part 3](https://chandusan.github.io/probability-understood/probability-part3/01.html)**

The chapter selector switches between the five companions. The previous six-lesson site is preserved in Git at `archive/before-slide-rebuild-2026-10-03`.

## What is included

- All 207 original slides, rendered at 2,000 pixels wide and expandable for reading.
- Rich explanations of every slide, including the full exercise solutions and qualifications where the source wording is imprecise.
- 12 Data Summary experiments: projection, absolute/squared loss, L1/L2 boundaries, a growing octahedron, outlier sensitivity, min–max scaling, percentile interpolation, boxplots, Bessel's correction, standardization, PCA, and the empirical rule.
- 11 Probability experiments: coin frequencies, binomial counts, crossing chords, Buffon’s needle, uniform densities, set operations, rectangles, partial orders, De Morgan’s laws, car turns, and dice sums.
- 9 Counting experiments: branching trees, overlapping card events, permutations versus combinations, constrained pipelines, generalized binomial series, stars and bars, lottery matches, poker hands, and tournament symmetry.
- 8 new Probability Part 2 experiments: bin occupancy, birthday collisions, repeated-letter arrangements, event overlap, exact versus minimum bridge suit counts, inclusion–exclusion coefficients, dice-face coverage, and full or partial derangements. Earlier experiments on tournaments, chords, and lottery matches are reused where relevant.
- 5 Probability Part 3 experiments: conditional event regions, pairwise versus mutual independence, screening base rates, posterior urn probabilities and predictions, and gambler’s ruin.
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

Edit Data Summary explanations in `content/slides/01.md` through `31.md`, Probability Part 1 in `content/probability-part1/01.md` through `43.md`, Counting in `content/counting/01.md` through `53.md`, Probability Part 2 in `content/probability-part2/01.md` through `36.md`, and Probability Part 3 in `content/probability-part3/01.md` through `44.md`. Each file starts with a title and an introductory paragraph. Standard Markdown, TeX math, tables, and `<details markdown="1">` sections are supported.

The page layout and slide navigation are assembled in `build.py`; the reading interface is in `src/site.css` and `src/site.js`. Experiments are authored in `src/labs/`, with shared styles and local state/height handling in `src/lab.css` and `src/lab-frame.js`. The Part 2 experiments also share `src/rules-math.js`, `src/rules-labs.js`, and `src/rules-labs.css`. Run their exact-count and probability checks with `node scripts/check_probability_part2.cjs`. Part 3 uses `src/cond-math.js`, `src/cond-labs.js`, and `src/cond-labs.css`; validate its finite outcome counts, Bayes calculations, and independent absorbing-chain solution with `node scripts/check_probability_part3.cjs`.

The builder recreates `docs/` from these sources. Do not edit generated pages directly. It validates all 207 expected source files, slide images, and experiment references before replacing the generated directory.

The preserved PDFs live in `assets/source/`. Data Summary images are in `assets/slides/`; Probability Part 1 images are in `assets/slides/probability-part1/`; Counting images are in `assets/slides/counting/`; Probability Part 2 images are in `assets/slides/probability-part2/`; Probability Part 3 images are in `assets/slides/probability-part3/`. To regenerate images, use `scripts/render_slides.py --chapter all` with Poppler and Pillow available; image regeneration is not part of the normal build.

## Publishing

GitHub Pages serves `docs/` from `main`. After editing and rebuilding, commit both the source and generated pages; pushing to `main` publishes the update. The historical `01-data.html` link redirects to the first slide. The historical `02-foundations.html` link redirects to Probability Part 1. The historical `03-counting.html` link redirects to Counting. The historical `04-rules.html` link redirects to Probability Part 2. The `05-conditional.html` link opens Probability Part 3. Existing chapter URLs and stored progress remain compatible. The former six-lesson site and audit pages remain in the archived version.

## Sources and attribution

Original slides: **Dobrin Marchev, STAT 5701**, from the supplied `01-DataSummary.pdf`, `02-Probability-Part1.pdf`, `03-Counting.pdf`, `04-Probability-Part2.pdf`, and `05-Probability-Part3.pdf`. Slide images and source material remain attributed to their author. Explanations, examples, proofs, corrections, and experiments are an independent personal study companion, not an official course publication.

Original sources: [Data Summary](https://drive.google.com/file/d/10qzlEP0KcW0O1Prun81YHoZrWd50y3OY/view), [Probability Part 1](https://drive.google.com/file/d/1hRhUQHsHpt8Iltyr2HL3YMRuVfV3KgrR/view), [Probability Part 2](https://drive.google.com/file/d/1UZS4g0hVz42I1jnsBmiKRB3jGzCkfyfw/view), [Probability Part 3](https://drive.google.com/file/d/10BdvgFEaR7wI0MJX8QDlAH44GlTS59Xs/view).

Probability slide numbers follow PDF page order; some printed footer numbers differ. The source images are preserved unchanged, while the teaching text explicitly qualifies source assumptions where needed. Your questions about orientation, continuous density, set inclusion, and infinite operations are integrated into the relevant lessons.

Counting includes worked solutions to every source exercise and the pasted questions about generalized binomial coefficients and stars and bars. Source corrections are explained beside the unchanged images: full houses number 3,744, high-card hands 1,302,540, and the source’s two errors cancel in its poker total. The bonus-number caveat in the lottery is treated separately from the six-main-number model.

Probability Part 2 supplies complete solutions to all 36 slides, including the image-only Scrabble example, both digit/counting exercises, derangements, subset avoidance, and nonrepeatwords. The explanations identify the incorrect numerical factor on bridge slide 26 and the repeated region label on slide 30, while retaining the original images. Lottery prize assumptions, the random-chord model, and the difference between exactly five and at least five cards are stated explicitly.

Probability Part 3 develops all 44 slides through explicit conditional probabilities, complete exercise solutions, finite outcome tables, and step-by-step recurrence algebra. It includes both card-order questions, all urn questions, the full four-toss independence check, the fox-tag exercise, the soccer model, the screening example, the two-stage fraud problem, and fair and biased gambler’s ruin. The original PDF is preserved. The companion explains the screening solution’s inconsistent sensitivity (96% in the question, 95% in the source calculation), clarifies the urn arithmetic, and qualifies the random-walk aside: recurrence does not guarantee two synchronized walkers meet when their starting parities differ.

Vendored dependencies: KaTeX 0.16.22 (MIT) and D3 7.9.0 (ISC). Their licenses are included under `assets/vendor/`. The build dependency is Python-Markdown 3.8.2.
