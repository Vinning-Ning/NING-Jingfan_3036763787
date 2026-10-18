# Card and Krueger (1994) — Replication

This project replicates Card and Krueger (1994), "Minimum Wages and Employment:
A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania,"
*American Economic Review*, 84(4), 772–793, and extends it with a store-size
heterogeneity analysis.

## Structure

- `report.pdf` — the empirical report
- `AI_USE_DISCLOSURE.md` — how AI was used at each stage
- `stata/replication.do` — the Stata workflow that generates all tables and figures
- `stata/output/processed_data.dta` — the processed analysis dataset
- `python/replication.py` — independent Python implementation used as a cross-check
- `data/` — original input data
- `skills/SKILL.md` — the reusable skill that generates the main outputs

## Reproduce

Place `public.csv` in `data/` (see `data/README.md`), then run:

```
cd stata
do replication.do
```

The workflow constructs all variables, reproduces Table 2, Table 3, Table 4,
and Figure 1, and runs the store-size extension. It writes the replication log,
the figure, and the processed dataset to `stata/output/`.

The independent Python implementation (`python/replication.py`) reproduces the
same results; run `python python/replication.py` from the repository root to
write the tables, figure, and processed data to `python/output/`.

## Key definitions

FTE employment equals full-time workers plus managers plus 0.5 times part-time
workers. GAP is the proportional wage increase needed to reach the new $5.05
minimum. The difference-in-differences estimate uses heteroskedasticity-robust
standard errors; Table 4 uses conventional standard errors to match the paper.

## Data access

`public.csv` is the course-provided restaurant survey data, distributed for
ECO6067 teaching and coursework only. Obtain Package 01 from the course project
page and place it in `data/`. Do not redistribute or upload the data to public
repositories.
