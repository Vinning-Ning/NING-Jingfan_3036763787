# Card and Krueger (1994) — Replication

This project replicates Card and Krueger (1994), "Minimum Wages and Employment:
A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania,"
*American Economic Review*, 84(4), 772–793, and extends it with a store-size
heterogeneity analysis.

## Structure

- `report.pdf` — the empirical report
- `AI_USE_DISCLOSURE.md` — how AI was used at each stage
- `code/run_all.do` — the workflow that generates all tables and figures
- `data/raw/` — original input data
- `data/processed/` — processed data used in the analysis
- `outputs/tables/` — generated tables
- `outputs/figures/` — generated figures
- `skills/SKILL.md` — the reusable skill that generates the main outputs

## Reproduce

Place `public.csv` in `data/raw/` (see `data/raw/README.md`), then run:

```
cd code
do run_all.do
```

The workflow constructs all variables, reproduces Table 2, Table 3, Table 4,
and Figure 1, and runs the store-size extension. It writes the replication log
to `outputs/tables/`, the figure to `outputs/figures/`, and the processed
dataset to `data/processed/`.

## Key definitions

FTE employment equals full-time workers plus managers plus 0.5 times part-time
workers. GAP is the proportional wage increase needed to reach the new $5.05
minimum. The difference-in-differences estimate uses heteroskedasticity-robust
standard errors; Table 4 uses conventional standard errors to match the paper.

## Data access

`public.csv` is the course-provided restaurant survey data, distributed for
ECO6067 teaching and coursework only. Obtain Package 01 from the course project
page and place it in `data/raw/`. Do not redistribute or upload the data to
public repositories.
