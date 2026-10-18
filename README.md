# Card and Krueger (1994) — Replication Package

This package reproduces Table 2, Table 3, Table 4, and Figure 1 of Card and
Krueger (1994), "Minimum Wages and Employment: A Case Study of the Fast-Food
Industry in New Jersey and Pennsylvania," *American Economic Review*, 84(4),
772–793, together with an independent store-size heterogeneity extension.

## Contents

- `stata/replication_submit.do` — Stata workflow with relative paths; reproduces
  the four assigned outputs and runs the extension
- `stata/replication.do` — the same workflow with absolute paths, for local use
- `data/public.csv` — raw survey data, not committed; see Data access below
- `DATA_DICTIONARY.md` — column definitions

## Requirements

Stata 15 or newer. The workflow uses only built-in commands.

## How to reproduce

Place `public.csv` in `data/`, then run the submission workflow from the
`stata/` folder:

```
do replication_submit.do
```

The workflow reads `../data/public.csv` and writes all results to
`stata/output/`.

## Variable construction

FTE employment equals full-time workers plus managers plus 0.5 times part-time
workers. GAP is the proportional wage increase needed to reach the new $5.05
minimum. Full-meal price is the sum of soda, fries, and entrée prices, tax
inclusive. The share of full-time workers equals 100 times full-time workers
divided by FTE.

## Sample handling

Wave-2 employment is set to 0 for the 6 permanently closed stores and treated
as missing for the 4 temporarily closed stores. Table 4 uses the 357 stores
with valid employment and starting-wage data in both waves.

## Data access

`public.csv` is the course-provided restaurant survey data, distributed for
ECO6067 teaching and coursework only. Obtain Package 01 from the course project
page (Google Drive) and place `public.csv` in `data/`. Do not redistribute or
upload the data to public repositories.
