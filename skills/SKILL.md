# Skill: Reproduce Card and Krueger (1994)

This skill reproduces the four assigned outputs of Card and Krueger (1994) —
Table 2, Table 3, Table 4, and Figure 1 — together with a store-size
heterogeneity extension, from the raw restaurant survey data.

## Input

Place the raw data file `public.csv` in `data/`. The file must be unchanged.

## Run

From the `stata/` folder, run:

```
do replication.do
```

The workflow constructs all variables, reproduces the tables and figure, and
runs the extension. It requires Stata 15 or newer and uses only built-in
commands.

## Output

- `stata/output/replication_stata.log` — all tables and regression results
- `stata/output/figure_1_stata.png` — distribution of starting wages
- `stata/output/processed_data.dta` — the processed analysis dataset

## Key definitions

- FTE employment = full-time workers + managers + 0.5 x part-time workers.
- GAP = the proportional wage increase needed to reach the new $5.05 minimum.
- The difference-in-differences estimate uses heteroskedasticity-robust
  standard errors; Table 4 uses conventional (homoskedastic) standard errors to
  match the paper.

## Reusing the skill

To replicate a different difference-in-differences paper, replace the raw data
file and adjust the variable construction and regression commands in
`replication.do` accordingly. The overall structure — construct
variables, produce summary statistics, estimate the treatment effect, run the
extension, and save the outputs — transfers directly.
