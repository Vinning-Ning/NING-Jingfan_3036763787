* Card & Krueger (1994) -- Replication (SUBMISSION VERSION)
* Reproduces Tables 2, 3, 4, Figure 1, and the store-size extension.
*
* Uses RELATIVE paths so the workflow runs on any machine after cloning.
* Run: cd to the code/ folder, then  do run_all.do
* Input : ../data/raw/public.csv
* Output: ../outputs/tables/ (log), ../outputs/figures/ (figure), ../data/processed/ (data)

version 15
clear all
set more off

cap mkdir "../outputs/tables"
cap mkdir "../outputs/figures"
cap mkdir "../data/processed"
log using "../outputs/tables/replication_stata.log", replace text

* Load raw data
import delimited using "../data/raw/public.csv", clear varnames(1) case(lower)

* FTE employment = full-time + managers + 0.5 * part-time
gen fte1 = empft + nmgrs + 0.5 * emppt
gen fte2 = empft2 + nmgrs2 + 0.5 * emppt2
replace fte2 = 0 if status2 == 3          // permanently closed -> 0
gen dfte = fte2 - fte1                    // change in FTE

* GAP = proportional wage increase needed to reach $5.05 (paper p. 779)
gen gap = 0
replace gap = (5.05 - wage_st) / wage_st if state == 1 & wage_st < 5.05

* Full-meal price (tax inclusive) = soda + fries + entree
gen meal1 = psoda + pfry + pentree
gen meal2 = psoda2 + pfry2 + pentree2

* % full-time = 100 * full-time (non-management) / FTE
gen pct_ft1 = 100 * empft  / fte1
gen pct_ft2 = 100 * empft2 / fte2

* Chain dummies (Wendy's = reference) and company-ownership dummy
gen chain_bk   = (chain == 1)
gen chain_kfc  = (chain == 2)
gen chain_roys = (chain == 3)
gen coowned    = (co_owned == 1)

* Region: three NJ regions + two eastern-PA regions
gen region = .
replace region = 1 if northj   == 1
replace region = 2 if centralj == 1
replace region = 3 if southj   == 1
replace region = 4 if pa1      == 1
replace region = 5 if pa2      == 1
label define regionlbl 1 "North NJ" 2 "Central NJ" 3 "South NJ" ///
                       4 "PA Philadelphia suburbs" 5 "PA Easton"
label values region regionlbl

* Wave-1 starting-wage categories (within-NJ comparison)
gen wcat = .
replace wcat = 1 if wage_st == 4.25
replace wcat = 2 if wage_st > 4.25 & wage_st < 5.00
replace wcat = 3 if wage_st >= 5.00 & wage_st < .
label define wcatlbl 1 "low $4.25" 2 "mid $4.26-4.99" 3 "high >= $5.00"
label values wcat wcatlbl

* Table 2 -- means of key variables by state
display _n "TABLE 2 -- means by state"
tab chain state, col nofreq
tabstat fte1 pct_ft1 wage_st meal1 hrsopen fte2 pct_ft2 wage_st2 meal2 hrsopen2 ///
        , by(state) stat(mean sd n) format(%9.3f)
foreach v in fte1 fte2 wage_st wage_st2 meal2 hrsopen2 {
    ttest `v', by(state)
}
gen wage_st_425  = (wage_st  == 4.25)
gen wage_st2_425 = (wage_st2 == 4.25)
gen wage_st2_505 = (round(wage_st2, 0.01) == 5.05)
tabstat wage_st_425 wage_st2_425 wage_st2_505 bonus special2, ///
        by(state) stat(mean) format(%9.3f)

* Table 3 -- average FTE employment per store
display _n "TABLE 3 -- average FTE employment per store"
tabstat fte1 fte2, by(state) stat(mean sd n) format(%9.3f)
tabstat fte1 fte2 if state == 1, by(wcat) stat(mean sd n) format(%9.3f)
tabstat dfte, by(state) stat(mean sd n) format(%9.3f)
tabstat dfte if state == 1, by(wcat) stat(mean sd n) format(%9.3f)

* Row 5: temporarily-closed stores set to 0
gen fte2b = fte2
replace fte2b = 0 if inlist(status2, 2, 4, 5)
gen dfteb = fte2b - fte1
tabstat dfteb, by(state) stat(mean sd n) format(%9.3f)

display _n "DiD via OLS (heteroskedasticity-robust SE): reg dfte state, robust"
reg dfte state, robust

* Table 4 -- reduced-form models (N = 357)
display _n "TABLE 4 -- reduced-form models for the change in FTE employment"
preserve
keep if !missing(fte1) & !missing(fte2) & !missing(wage_st) ///
      & (!missing(wage_st2) | status2 == 3)

display _n "Sample size (paper: 357):"
count
summarize dfte
summarize gap if state == 1

reg dfte state
estimates store m1
reg dfte state chain_bk chain_kfc chain_roys coowned
estimates store m2
reg dfte gap
estimates store m3
reg dfte gap chain_bk chain_kfc chain_roys coowned
estimates store m4
reg dfte gap chain_bk chain_kfc chain_roys coowned i.region
estimates store m5

estimates table m1 m2 m3 m4 m5, b(%9.3f) se stats(N)
restore

* Independent extension -- store-size heterogeneity in the employment effect
display _n "EXTENSION -- store-size heterogeneity in the employment effect"

* Median split at Wave-I FTE employment (computed on the balanced sample)
summarize fte1 if !missing(dfte), detail
gen large = fte1 > r(p50) if !missing(fte1)

display _n "Median-split DiD, large stores (robust):"
reg dfte i.state if large == 1, robust
display _n "Median-split DiD, small stores (robust):"
reg dfte i.state if large == 0, robust

display _n "Interaction: state x large (robust)"
reg dfte i.state##i.large, robust

display _n "Continuous interaction: state x fte1 (robust)"
reg dfte c.state##c.fte1, robust

* Save the processed dataset (all constructed variables)
save "../data/processed/processed_data.dta", replace

* Figure 1 -- distribution of starting wages (2 states x 2 waves)
histogram wage_st  if state == 1, bin(20) name(h1, replace) ///
    title("New Jersey, February 1992") xtitle("Starting wage ($/hour)")
histogram wage_st  if state == 0, bin(20) name(h2, replace) ///
    title("Pennsylvania, February 1992") xtitle("Starting wage ($/hour)")
histogram wage_st2 if state == 1, bin(20) name(h3, replace) ///
    title("New Jersey, November 1992") xtitle("Starting wage ($/hour)")
histogram wage_st2 if state == 0, bin(20) name(h4, replace) ///
    title("Pennsylvania, November 1992") xtitle("Starting wage ($/hour)")
graph combine h1 h2 h3 h4, cols(2) title("Figure 1. Distribution of starting wage rates")
graph export "../outputs/figures/figure_1_stata.png", replace

log close
display _n "Done. Outputs in ../outputs/ and ../data/processed/"
