# Probability, understood

Six visual, interactive lessons that build probability and statistics from first principles.

**[Start learning →](https://chandusan.github.io/probability-understood/)**

| Lesson | Explore |
| --- | --- |
| 1 · The story inside the data | Center, spread, variance, and the shape of data |
| 2 · A language for uncertainty | Sample spaces, events, and probability axioms |
| 3 · Count without counting twice | Permutations, combinations, and poker |
| 4 · Find the easier question | Complements, birthdays, and inclusion–exclusion |
| 5 · Let evidence change your mind | Conditioning, independence, Bayes, and random walks |
| 6 · Turn chance into a number | Random variables, PMFs, CDFs, and densities |

Includes 13 interactive experiments, 13 concept checks, worked solutions, visual memory cues, and a source-page coverage map for each lesson. Each HTML lesson is self-contained and works offline. Use **Print lesson** for a reading copy with solutions expanded.

## Coverage audit

**[Read the page-by-page audit](https://chandusan.github.io/probability-understood/audit.html)**, completed October 1, 2026. It maps all 243 source pages to lesson sections, records gaps found in the initial version, and explains what was expanded or clarified. The structured records live in `audit/`.

Coverage includes the mathematical ideas, examples, exercises, and proof steps; source wording and decorative slide art are not duplicated. Expand the worked-example panels for the full treatment. The estimated lesson times describe the core path; completing all source exercises takes additional time.

## Edit and build

Edit lesson fragments in `src/01.html` through `src/06.html`, shared styling in `src/style.css`, and experiments in `src/interactive.js`. Course metadata and page assembly are in `build.py`.

Rebuild with Python 3 (standard library only):

```sh
python3 build.py
```

This produces the publishable files in `docs/` and an offline `probability-lessons.zip`. Open `docs/index.html` directly, or preview with:

```sh
python3 -m http.server 8000 --directory docs
```

GitHub Pages publishes the committed `docs/` folder on the `main` branch. After editing, rebuild and commit both the source and generated pages; pushing to `main` updates the site.

## Sources and attribution

An original teaching companion to six STAT 5701 slide PDFs by Dobrin Marchev, covering 243 PDF pages. Each lesson links to its source and identifies the corresponding page ranges. This is not an official course publication. New analogies, diagrams, and interactive experiments supplement the slides; precision notes explain corrections where needed.

The original PDFs are not included. Their Google Drive links retain their existing access permissions.
