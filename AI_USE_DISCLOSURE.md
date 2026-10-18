# AI Use Disclosure

AI (Claude Code, Anthropic) was used as a coding, analysis, and writing
assistant throughout this project. This document records where AI was used, how
its outputs were checked, and which of its errors were corrected or rejected.

## 1. Where and how AI was used

- **Paper understanding.** AI extracted and summarised the research question,
  the institutional background of the New Jersey minimum-wage law, the
  economic mechanism, and the empirical design of Card and Krueger (1994).
- **Data and variable construction.** AI wrote the Stata workflow that
  constructs full-time-equivalent employment, the wage-gap variable, and the
  chain, ownership, and region indicators from `public.csv`.
- **Replication.** AI wrote the code that reproduces Tables 2, 3, and 4 and
  Figure 1, and cross-checked the results against the paper's published values.
- **Independent extension.** AI proposed several candidate extensions and
  implemented the store-size heterogeneity analysis that was selected.
- **Report and package.** AI drafted sections 4-6 of the empirical report, the
  comparison table, the README, and the folder structure of the
  reproducibility package.

## 2. How AI-generated code, analysis, and writing were checked

- Every replication result was compared with the paper's published value for
  the corresponding table; any discrepancy was investigated and explained.
- The analysis was implemented independently in Python and Stata; the two
  implementations produced identical estimates, which guards against coding
  errors.
- Variable definitions were verified against the paper's footnotes and text
  before being used.
- All numbers reported in the final report were verified against the Stata
  output log.

## 3. Important AI errors or suggestions that were corrected or rejected

- **Floating-point comparison.** AI's initial Stata code identified stores
  paying the new minimum wage with `wage_st2 == 5.05`, which silently returned
  zero matches because of floating-point representation. This was corrected to
  `round(wage_st2, 0.01) == 5.05`.
- **Regression sample.** AI initially excluded the six permanently closed
  stores from the Table 4 sample, giving N = 351 rather than the paper's 357.
  The correct sample restriction, which exempts closed stores from the wave-2
  wage requirement, was identified and applied.
- **Difference-in-differences standard error.** AI initially reported the
  homoskedastic OLS standard error (t = 2.38), which did not match the paper's
  t = 2.03. The heteroskedasticity-robust standard error (t = 2.05) was adopted
  instead.
- **Extension selection.** AI suggested several possible extensions; the
  store-size heterogeneity analysis was chosen as the most economically
  interpretable and clearly motivated option.
