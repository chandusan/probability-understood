# Probability, understood

A slide-by-slide teaching companion to **01 Data Summary**, **02 Probability · Part 1**, **03 Counting**, **04 Probability · Part 2**, **05 Probability · Part 3**, **06 Random Variables**, **07 Random Variables · Part 2**, **08 Random Variables · Part 3**, **09 Expectation**, and **10 Special Distributions**. Each of the 438 pages starts with the original slide image, then develops its ideas through intuition, worked examples, proofs, and questions from our study sessions.

**[Open the Data Summary companion](https://chandusan.github.io/probability-understood/)**

**[Open Probability · Part 1](https://chandusan.github.io/probability-understood/probability-part1/01.html)**

**[Open Counting](https://chandusan.github.io/probability-understood/counting/01.html)**

**[Open Probability · Part 2](https://chandusan.github.io/probability-understood/probability-part2/01.html)**

**[Open Probability · Part 3](https://chandusan.github.io/probability-understood/probability-part3/01.html)**

**[Open Random Variables](https://chandusan.github.io/probability-understood/random-variables/01.html)**

**[Open Random Variables · Part 2](https://chandusan.github.io/probability-understood/random-variables-part2/01.html)**

**[Open Random Variables · Part 3](https://chandusan.github.io/probability-understood/random-variables-part3/01.html)**

**[Open Expectation](https://chandusan.github.io/probability-understood/expectation/01.html)**

**[Open Special Distributions](https://chandusan.github.io/probability-understood/special-distributions/01.html)**

**[Open the calculus appendix](https://chandusan.github.io/probability-understood/appendix/calculus.html)** — a short, self-contained reference for differentiation, integration, and the CDF–density connection, with optional product and chain rule examples. The appendix has no outgoing links to slides. It is linked from every lesson and directly from the relevant Random Variables slides.

**[Open lesson exercises](https://chandusan.github.io/probability-understood/exercises/index.html)** — exercises and standalone practice questions from all ten PDFs, organized by lesson. Each question has a collapsed, fully worked solution. The same collection appears at the bottom of its lesson’s final slide.

**[Open Midterms](https://chandusan.github.io/probability-understood/midterms/index.html)** — the Fall 2024 and Fall 2025 papers, each with separate questions and questions-with-solutions pages.

**[Open the exam cheat sheets](https://chandusan.github.io/probability-understood/cheat-sheet/index.html)** — download the combined lessons 03–10, De Morgan’s laws and calculus sheet as a high-resolution PNG. The earlier original-formula reference for PDFs 01–09 remains available as a one-page A4 landscape PDF.

The chapter selector switches between the ten companions. The previous six-lesson site is preserved in Git at `archive/before-slide-rebuild-2026-10-03`.

## What is included

- All 438 original slides, rendered at 2,000 pixels wide and expandable for reading.
- Rich explanations of every slide, including the full exercise solutions and qualifications where the source wording is imprecise.
- 12 Data Summary experiments: projection, absolute/squared loss, L1/L2 boundaries, a growing octahedron, outlier sensitivity, min–max scaling, percentile interpolation, boxplots, Bessel's correction, standardization, PCA, and the empirical rule.
- 11 Probability experiments: coin frequencies, binomial counts, crossing chords, Buffon’s needle, uniform densities, set operations, rectangles, partial orders, De Morgan’s laws, car turns, and dice sums.
- 9 Counting experiments: branching trees, overlapping card events, permutations versus combinations, constrained pipelines, generalized binomial series, stars and bars, lottery matches, poker hands, and tournament symmetry.
- 8 new Probability Part 2 experiments: bin occupancy, birthday collisions, repeated-letter arrangements, event overlap, exact versus minimum bridge suit counts, inclusion–exclusion coefficients, dice-face coverage, and full or partial derangements. Earlier experiments on tournaments, chords, and lottery matches are reused where relevant.
- 5 Probability Part 3 experiments: conditional event regions, pairwise versus mutual independence, screening base rates, posterior urn probabilities and predictions, and gambler’s ruin.
- 5 Random Variables experiments: dependent ad clicks, first-trigger stopping strings, linked outcome/PMF/CDF views for three distributions, distance geometry with its CDF and density, and a mixed distribution with a point mass at zero.
- 4 Random Variables Part 2 experiments: exact image-audit counts, joint/marginal/conditional dice distributions, engagement-specific churn rates, and posterior tier predictions.
- 3 new experiments for lessons 08–10: joint-density slices and conditioning, weighted means and variance, and a comparison of binomial, Poisson, geometric, and hypergeometric distributions.
- Two past midterm papers: 12 questions across Fall 2024 and Fall 2025, with separate practice pages and fully worked solutions.
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

Edit Data Summary explanations in `content/slides/01.md` through `31.md`, Probability Part 1 in `content/probability-part1/01.md` through `43.md`, Counting in `content/counting/01.md` through `53.md`, Probability Part 2 in `content/probability-part2/01.md` through `36.md`, Probability Part 3 in `content/probability-part3/01.md` through `44.md`, Random Variables in `content/random-variables/01.md` through `36.md`, and Random Variables Part 2 in `content/random-variables-part2/01.md` through `36.md`. The new chapters are in `content/random-variables-part3/01.md` through `49.md`, `content/expectation/01.md` through `49.md`, and `content/special-distributions/01.md` through `61.md`. Each file starts with a title and an introductory paragraph. Standard Markdown, TeX math, tables, and `<details markdown="1">` sections are supported.

Edit the calculus reference in `content/appendix/calculus.md`; it builds to `docs/appendix/calculus.html` and is separate from slide counts and completion progress.

Edit lesson practice in `content/exercises/<chapter-id>.json`. Each entry records its source slide numbers, full question, and standalone solution. `exercises.py` builds the ten collection pages and the exercise hub, and reuses exactly the same cards at the end of each lesson. Solutions use native `<details>` controls and are closed by default. Exercise pages offer separate printing of questions alone or questions with solutions. The source inventory includes explicit exercises and standalone practice prompts; ordinary worked examples remain in the original lessons.

Edit midterm question and solution content in `content/midterms/2024.json` and `content/midterms/2025.json`. The `midterms.py` renderer uses the same question field in both modes, then adds worked explanations only on the solutions page. It builds the hub at `docs/midterms/index.html`, with `questions.html` and `solutions.html` under each year. The questions page contains no hidden solutions or source answer-key links. Both modes support printing and local math rendering, and all question and solution headings have unique anchors. Midterms are separate from the 438-slide count and browser-local slide progress. The main build validates paper metadata and source PDFs before replacing `docs/`.

The page layout and slide navigation are assembled in `build.py`; the reading interface is in `src/site.css` and `src/site.js`. Experiments are authored in `src/labs/`, with shared styles and local state/height handling in `src/lab.css` and `src/lab-frame.js`. The Part 2 experiments also share `src/rules-math.js`, `src/rules-labs.js`, and `src/rules-labs.css`. Run their exact-count and probability checks with `node scripts/check_probability_part2.cjs`. Part 3 uses `src/cond-math.js`, `src/cond-labs.js`, and `src/cond-labs.css`; validate its finite outcome counts, Bayes calculations, and independent absorbing-chain solution with `node scripts/check_probability_part3.cjs`. Random Variables uses `src/rv-math.js`, `src/rv-labs.js`, and `src/rv-labs.css`; run `node scripts/check_random_variables.cjs` for exhaustive path counts, CDF endpoint checks, and independent numerical area/derivative checks. Random Variables Part 2 uses `src/joint-math.js`, `src/joint-labs.js`, and `src/joint-labs.css`; run `node scripts/check_random_variables_part2.cjs` for independent finite-outcome enumeration, exact table counts, and conditional-distribution checks.

The cheat-sheet page is built by `cheat_sheet.py`. Its primary download, `assets/downloads/all-lessons-and-calculus.png`, combines lessons 03–10 and calculus in a 7000 × 3220 image with seven columns. Descriptive Statistics (01) and introductory Probability (02) are omitted; the two-event and generalized De Morgan laws from 02 are retained in the Rules of Probability panel. The 53 sections contain 367 rendered formula instances. Counting Rules 1–3 and the generalized binomial theorem are omitted. Permutations and combinations share a table with single-line definitions and expressions. The binomial theorem is one line. Poker rows contain only the hand name, inline pattern and counting expression; all counts are retained and descriptive prose is removed. Rules of Probability contains De Morgan’s laws and the general inclusion–exclusion rule, including the disjoint-event case. Panel 05 removes the standalone conditional-probability definition and the urn, predictive-urn and gambler’s-ruin examples and retains compact definitions, prerequisite conditions and formulas. Panel 06 keeps the PMF, PDF, CDF and mixed-distribution formulas and essential properties in compact notes with tighter spacing; examples and long explanations are omitted. Panel 07 preserves all joint, marginal and conditional formulas and essential properties, with duplicate normalization instructions removed and compact relative-risk notation. All remaining panels use concise property notes and tighter spacing, retaining their substantive formulas, supports, parameter conditions and convergence domains. Examples and long explanations are omitted; counting remains in its single-line table format. The smaller `all-lessons-and-calculus-preview.jpg` is only an overview; the download supplies the full-resolution PNG. The same download is available on the midterms hub.

The earlier exam reference is built from `content/cheat-sheet.json`. The version 3 JSON contains typed LaTeX formulas in lesson and slide order, with an audit record for every one of the 377 slides in PDFs 01–09. Repeated formulas, source notation, and source calculation errors are retained. The website renders these expressions with KaTeX. The matching one-page A4 landscape PDF lives in `assets/downloads/probability-statistics-exam-cheat-sheet.pdf`; it contains native mathematical text and no slide screenshots. The build validates these inputs before replacing `docs/`. The page and downloads are linked from lessons, exercises, and midterms, without changing slide progress.

To regenerate the PDF, install Tectonic and PyMuPDF, then run `python scripts/build_formula_sheet.py --tectonic /path/to/tectonic`. This typesets the formulas afresh with LaTeX and arranges them on one page in teaching order. Render and inspect the result, verify that every expression parses in KaTeX, then run `python build.py`. Keep the web formulas and PDF synchronized. The one-page constraint requires very small text; the website provides the same formulas at a larger size.

The builder recreates `docs/` from these sources. Do not edit generated pages directly. It validates all 438 expected source files, slide images, and experiment references before replacing the generated directory.

The preserved PDFs live in `assets/source/`. Data Summary images are in `assets/slides/`; Probability Part 1 images are in `assets/slides/probability-part1/`; Counting images are in `assets/slides/counting/`; Probability Part 2 images are in `assets/slides/probability-part2/`; Probability Part 3 images are in `assets/slides/probability-part3/`; Random Variables images are in `assets/slides/random-variables/`; Random Variables Part 2 images are in `assets/slides/random-variables-part2/`. The new image folders are `assets/slides/random-variables-part3/`, `assets/slides/expectation/`, and `assets/slides/special-distributions/`. To regenerate images, use `scripts/render_slides.py --chapter all` with Poppler and Pillow available; image regeneration is not part of the normal build.

## Publishing

GitHub Pages serves `docs/` from `main`. After editing and rebuilding, commit both the source and generated pages; pushing to `main` publishes the update. The historical `01-data.html` link redirects to the first slide. The historical `02-foundations.html` link redirects to Probability Part 1. The historical `03-counting.html` link redirects to Counting. The historical `04-rules.html` link redirects to Probability Part 2. The `05-conditional.html` link opens Probability Part 3. The `06-random-variables.html` link opens Random Variables. The `07-random-variables-part2.html` link opens Random Variables Part 2. Existing chapter URLs and stored progress remain compatible. The former six-lesson site and audit pages remain in the archived version.

## Sources and attribution

Original slides: **Dobrin Marchev, STAT 5701**, from the supplied `01-DataSummary.pdf`, `02-Probability-Part1.pdf`, `03-Counting.pdf`, `04-Probability-Part2.pdf`, `05-Probability-Part3.pdf`, `06-RandomVariables.pdf`, `07-RandomVariables2.pdf`, `08-RandomVariables3.pdf`, `09-Expectation.pdf`, and `10-SpecialDistributions.pdf`. Slide images and source material remain attributed to their author. Explanations, examples, proofs, corrections, and experiments are an independent personal study companion, not an official course publication.

Original sources: [Data Summary](https://drive.google.com/file/d/10qzlEP0KcW0O1Prun81YHoZrWd50y3OY/view), [Probability Part 1](https://drive.google.com/file/d/1hRhUQHsHpt8Iltyr2HL3YMRuVfV3KgrR/view), [Probability Part 2](https://drive.google.com/file/d/1UZS4g0hVz42I1jnsBmiKRB3jGzCkfyfw/view), [Probability Part 3](https://drive.google.com/file/d/10BdvgFEaR7wI0MJX8QDlAH44GlTS59Xs/view), [Random Variables](https://drive.google.com/file/d/1nzYAnJSMFWGW9uvUu8u-0zVoHzasxwWI/view), [Random Variables Part 2](https://drive.google.com/file/d/1JHT6t9eGVWAbVLCSzXsa_kvlcdsI4kkG/view), [Random Variables Part 3](https://drive.google.com/file/d/1Ml1cB7VL49NhlWVU_n00IGNPctEzg2hz/view), [Expectation](https://drive.google.com/file/d/1ixjyyyuSFiTuoq15RoDb84uRoE17NHl8/view), [Special Distributions](https://drive.google.com/file/d/1FqlWIXkJUOvw2Yie5RvEt0eDhTyz9Mx3/view).

Probability slide numbers follow PDF page order; some printed footer numbers differ. The source images are preserved unchanged, while the teaching text explicitly qualifies source assumptions where needed. Your questions about orientation, continuous density, set inclusion, and infinite operations are integrated into the relevant lessons.

Counting includes worked solutions to every source exercise and the pasted questions about generalized binomial coefficients and stars and bars. Source corrections are explained beside the unchanged images: full houses number 3,744, high-card hands 1,302,540, and the source’s two errors cancel in its poker total. The bonus-number caveat in the lottery is treated separately from the six-main-number model.

Probability Part 2 supplies complete solutions to all 36 slides, including the image-only Scrabble example, both digit/counting exercises, derangements, subset avoidance, and nonrepeatwords. The explanations identify the incorrect numerical factor on bridge slide 26 and the repeated region label on slide 30, while retaining the original images. Lottery prize assumptions, the random-chord model, and the difference between exactly five and at least five cards are stated explicitly.

Probability Part 3 develops all 44 slides through explicit conditional probabilities, complete exercise solutions, finite outcome tables, and step-by-step recurrence algebra. It includes both card-order questions, all urn questions, the full four-toss independence check, the fox-tag exercise, the soccer model, the screening example, the two-stage fraud problem, and fair and biased gambler’s ruin. The original PDF is preserved. The companion explains the screening solution’s inconsistent sensitivity (96% in the question, 95% in the source calculation), clarifies the urn arithmetic, and qualifies the random-walk aside: recurrence does not guarantee two synchronized walkers meet when their starting parities differ.

Random Variables covers all 36 source slides, with complete dependent-click and early-stopping enumerations, every ordinary and nontraditional dice probability, explicit geometric area and derivative calculations, the polynomial-CDF exercise, a mixed spending distribution, the infinite-PMF normalization, and lottery net gains. It distinguishes probability mass from density, explains every CDF endpoint and jump, and qualifies the source's differentiability statements and paying-user density wording. Original slide images and the PDF remain unchanged.

Random Variables Part 2 covers all 36 source slides: density and mixed-CDF exercises, the complete polynomial-CDF solution, joint hypergeometric and multinomial counting, exact dice tables and event sums, marginalization, conditional-binomial derivations, relative-risk comparisons, and normalization and prediction in the nine-cell tier model. It explains which mixed-CDF jumps to include, requires n > −1 for the power density, distinguishes an overall churn baseline from a disjoint comparison group, and completes the source’s unanswered tier-prediction question with the most probable category and the conditional-mean alternative. Original slides and PDF are preserved unchanged.

Lessons 08–10 add 159 source-aligned explanations: double integrals and their geometry, continuous joint and conditional distributions, the multivariate normal, expectation and moments, variance, moment-generating functions, and the main discrete distributions. Worked problems show the event or quantity before the calculation, state the required assumptions, and explain corrections beside the unchanged original slides. The new explorers share `src/multi-math.js`, `src/multi-labs.js`, and `src/multi-labs.css`; run their independent enumeration and numerical checks with `node scripts/check_lessons_08_10.cjs`.

## Midterm sources

The supplied `Midterm` folder contains two exam years. The source files are preserved under `assets/source/midterms/`:

- **Fall 2024:** [original questions](https://drive.google.com/file/d/1MpULV1JulTh_vqa_7cNefaCCZsHDizGZ/view), saved as `midterm-2024-questions.pdf`; [original solutions](https://drive.google.com/file/d/1u_5OXZ398iQJxbejUvIiKWbjP9P4eKkq/view), saved as `midterm-2024-source-solutions.pdf`.
- **Fall 2025:** [original solutions paper](https://drive.google.com/file/d/1MBGWcb-6UASCbFPmqa6G3SCvpitEIJyt/view), saved as `midterm-2025-source-solutions.pdf`. Its questions are transcribed into a separate practice page because the supplied PDF also contains answers.

Each paper has six questions. All parts are included, including the Fall 2025 bonus. The solutions repeat the full question before explaining the model, calculation, and reasoning. Where a source answer needs qualification or correction, the explanation makes this explicit. Original papers remain unchanged and attributed to Dobrin Marchev, STAT 5701. The Midterms link appears in every lesson's navigation; the standalone calculus appendix keeps its existing navigation.

Vendored dependencies: KaTeX 0.16.22 (MIT) and D3 7.9.0 (ISC). Their licenses are included under `assets/vendor/`. The build dependency is Python-Markdown 3.8.2.
