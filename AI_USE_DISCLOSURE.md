# AI Use Disclosure

## Where and how AI was used

AI (Claude Code) was used as a coding, analysis, and writing assistant at the
following stages.

1. **LaTeX formulas in the report.** AI helped draft and check the LaTeX
   expressions for the difference-in-differences estimator and the other
   equations in the empirical report.

2. **Comparison of replication results with the original paper.** Because the
   data are large, AI was used to compare the Stata replication output with the
   published values in each table of the original paper and to identify and
   explain any discrepancies. The Stata results were also compared with a
   separate Python implementation to guard against coding errors.

3. **Selection of the independent extension.** AI proposed several candidate
   extensions; the store-size heterogeneity analysis was selected from these
   proposals.

4. **Error correction in the do-file and report text.** AI was used to check
   and correct errors in the Stata code and in the wording of the report.

5. **GitHub-related advice.** AI provided guidance on initializing the
   repository, writing the `.gitignore` file, and staging meaningful commits.

6. **Compliance check.** AI was used to check the submission against the
   project requirements and to identify any missing items.

## How AI-generated code, analysis, and writing were checked

- Every replication result was compared with the paper's published value for
  the corresponding table; any discrepancy was investigated and explained.
- The analysis was implemented independently in Python and Stata, and the two
  implementations produced identical estimates.
- The LaTeX formulas and every number reported in the report were verified
  against the Stata output log.
- The choice of extension was reviewed against the project requirements before
  it was adopted.
- AI's corrections to the code and the report text were reviewed line by line
  before being accepted.
- GitHub and compliance advice was checked against the course instructions.

## Important AI errors or suggestions that you corrected or rejected

- AI initially identified stores paying the new minimum wage with
  `wage_st2 == 5.05`, which failed because of floating-point representation;
  this was corrected to `round(wage_st2, 0.01) == 5.05`.
- AI initially used a Table 4 sample that excluded the six permanently closed
  stores, giving N = 351 rather than the paper's 357; the correct sample
  restriction was identified and applied.
- AI initially reported the homoskedastic standard error for the
  difference-in-differences estimate (t = 2.38), which did not match the paper;
  the heteroskedasticity-robust standard error (t = 2.05) was adopted instead.
- AI suggested several possible extensions; only the store-size heterogeneity
  analysis was retained.
