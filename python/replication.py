"""
Card & Krueger (1994) -- Replication
"Minimum Wages and Employment: A Case Study of the Fast-Food Industry
in New Jersey and Pennsylvania", American Economic Review 84(4), 772-793.

Reconstructs the analysis variables from the raw survey data and reproduces
the paper's Table 2, Table 3, Table 4, and Figure 1.

Input : data/public.csv  (410 stores, 46 columns)
Output: printed tables, table2.csv / table3.csv / table4.csv, figure_1.png

Variable definitions (paper pp. 775, 779):
  FTE   = full-time workers + managers/assistant managers + 0.5 * part-time
          (EMPFT + NMGRS + 0.5 * EMPPT)
  GAP   = proportional wage increase needed to reach $5.05; 0 for PA stores
          and NJ stores already paying >= $5.05
  %full-time = 100 * EMPFT / FTE
  full-meal price = soda + fries + entree (tax inclusive)

Sample rules:
  * Wave-2 employment is 0 for the 6 permanently closed stores (STATUS2==3);
    the 4 temporarily-closed stores (STATUS2 in {2,4,5}) remain missing.
  * Table 4 sample = stores with valid employment (both waves) and valid
    starting wage (both waves), EXCEPT that the closed stores are exempt from
    the wave-2 wage requirement.  -> N = 357.
"""

import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Make all file paths relative to this script's location (python/ folder),
# so the script can be run from any working directory.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# 0. Load raw data
# ----------------------------------------------------------------------------
df = pd.read_csv("../data/public.csv")
os.makedirs("output", exist_ok=True)

# ----------------------------------------------------------------------------
# 1. Variable construction
# ----------------------------------------------------------------------------
df["fte1"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
df["fte2"] = df["EMPFT2"] + df["NMGRS2"] + 0.5 * df["EMPPT2"]
df.loc[df["STATUS2"] == 3, "fte2"] = 0.0            # permanently closed -> 0
df["dfte"] = df["fte2"] - df["fte1"]

df["gap"] = 0.0
nj_low = (df["STATE"] == 1) & (df["WAGE_ST"] < 5.05)
df.loc[nj_low, "gap"] = (5.05 - df.loc[nj_low, "WAGE_ST"]) / df.loc[nj_low, "WAGE_ST"]

df["meal1"] = df["PSODA"] + df["PFRY"] + df["PENTREE"]
df["meal2"] = df["PSODA2"] + df["PFRY2"] + df["PENTREE2"]

# % full-time = 100 * full-time (non-management) / FTE
df["pct_ft1"] = 100.0 * df["EMPFT"] / df["fte1"]
df["pct_ft2"] = 100.0 * df["EMPFT2"] / df["fte2"]

df["chain_bk"] = (df["CHAIN"] == 1).astype(int)
df["chain_kfc"] = (df["CHAIN"] == 2).astype(int)
df["chain_roys"] = (df["CHAIN"] == 3).astype(int)
df["co_owned"] = df["CO_OWNED"].astype(int)

df["region"] = ""
df.loc[df["NORTHJ"] == 1, "region"] = "northj"
df.loc[df["CENTRALJ"] == 1, "region"] = "centralj"
df.loc[df["SOUTHJ"] == 1, "region"] = "southj"
df.loc[df["PA1"] == 1, "region"] = "pa1"
df.loc[df["PA2"] == 1, "region"] = "pa2"


def wage_cat(w):
    if pd.isna(w):
        return np.nan
    if w == 4.25:
        return "low"
    if w < 5.00:
        return "mid"
    return "high"


df["wcat"] = df["WAGE_ST"].apply(wage_cat)

nj = df[df["STATE"] == 1]
pa = df[df["STATE"] == 0]


def mean_se(x):
    x = x.dropna()
    return (x.mean(), x.std(ddof=1) / np.sqrt(len(x))) if len(x) else (np.nan, np.nan)


def diff_se(m1, s1, m2, s2):
    return m1 - m2, np.sqrt(s1 ** 2 + s2 ** 2)


# ----------------------------------------------------------------------------
# 2. Table 2 -- means of key variables by state
# ----------------------------------------------------------------------------
print("=" * 92)
print("TABLE 2 -- means by state.  (paper values in brackets)")
print("=" * 92)
print(f"{'Variable':32s} {'NJ':>8s} {'PA':>8s} {'t':>8s}   [paper NJ / PA]")

t2 = [
    ("% Burger King", (nj["CHAIN"] == 1), (pa["CHAIN"] == 1), None, None, True),
    ("% KFC", (nj["CHAIN"] == 2), (pa["CHAIN"] == 2), None, None, True),
    ("% Roy Rogers", (nj["CHAIN"] == 3), (pa["CHAIN"] == 3), None, None, True),
    ("% Wendy's", (nj["CHAIN"] == 4), (pa["CHAIN"] == 4), None, None, True),
    ("% company-owned", nj["CO_OWNED"], pa["CO_OWNED"], None, None, True),
    ("FTE, wave 1", nj["fte1"], pa["fte1"], 20.4, 23.3, False),
    ("% full-time, wave 1", nj["pct_ft1"], pa["pct_ft1"], 32.8, None, False),
    ("starting wage, wave 1", nj["WAGE_ST"], pa["WAGE_ST"], 4.61, None, False),
    ("% wage=$4.25, wave 1", (nj["WAGE_ST"] == 4.25), (pa["WAGE_ST"] == 4.25), 30.5, None, True),
    ("full-meal price, wave 1", nj["meal1"], pa["meal1"], None, None, False),
    ("hours open, wave 1", nj["HRSOPEN"], pa["HRSOPEN"], None, None, False),
    ("% recruiting bonus, wave 1", nj["BONUS"], pa["BONUS"], None, None, True),
    ("FTE, wave 2", nj["fte2"], pa["fte2"], 21.0, 21.2, False),
    ("% full-time, wave 2", nj["pct_ft2"], pa["pct_ft2"], 35.9, 30.4, False),
    ("starting wage, wave 2", nj["WAGE_ST2"], pa["WAGE_ST2"], 5.08, 4.62, False),
    ("% wage=$4.25, wave 2", (nj["WAGE_ST2"] == 4.25), (pa["WAGE_ST2"] == 4.25), 0.0, 25.3, True),
    ("% wage=$5.05, wave 2", (nj["WAGE_ST2"] == 5.05), (pa["WAGE_ST2"] == 5.05), 85.2, 1.3, True),
    ("full-meal price, wave 2", nj["meal2"], pa["meal2"], 3.41, 3.03, False),
    ("hours open, wave 2", nj["HRSOPEN2"], pa["HRSOPEN2"], 14.4, 14.7, False),
    ("% recruiting bonus, wave 2", nj["SPECIAL2"], pa["SPECIAL2"], 20.3, 23.4, True),
]

table2_rows = []
for label, xnj, xpa, pnj, ppa, is_pct in t2:
    mnj, snj = mean_se(xnj)
    mpa, spa = mean_se(xpa)
    t = (mnj - mpa) / np.sqrt(snj ** 2 + spa ** 2) if snj and spa else np.nan
    if is_pct:
        mnj, mpa = 100 * mnj, 100 * mpa
    pnj_s = f"{pnj:.1f}" if pnj is not None else "-"
    ppa_s = f"{ppa:.1f}" if ppa is not None else "-"
    table2_rows.append([label, mnj, mpa, t, pnj_s, ppa_s])
    print(f"{label:32s} {mnj:8.2f} {mpa:8.2f} {t:8.2f}   [{pnj_s} / {ppa_s}]")

pd.DataFrame(table2_rows, columns=["variable", "NJ", "PA", "t", "paper_NJ", "paper_PA"]).to_csv(
    "output/table2.csv", index=False)

# ----------------------------------------------------------------------------
# 3. Table 3 -- average employment per store before and after
# ----------------------------------------------------------------------------
print("\n" + "=" * 92)
print("TABLE 3 -- average FTE employment per store (mean; SE in parentheses)")
print("=" * 92)

groups = {
    "PA": pa,
    "NJ": nj,
    "low": nj[nj["wcat"] == "low"],
    "mid": nj[nj["wcat"] == "mid"],
    "high": nj[nj["wcat"] == "high"],
}

cols_short = ["PA", "NJ", "low", "mid", "high"]
col_labels = {"PA": "PA", "NJ": "NJ", "low": "low $4.25",
              "mid": "mid $4.26-4.99", "high": "high >=$5.00"}
hdr = f"{'row':28s}" + "".join(f"{col_labels[g]:>16s}" for g in cols_short)
print(hdr)

# Rows 1 & 2: levels
row1 = {g: mean_se(sub["fte1"]) for g, sub in groups.items()}
row2 = {g: mean_se(sub["fte2"]) for g, sub in groups.items()}
for rowname, cells in [("1. FTE before", row1), ("2. FTE after", row2)]:
    line = f"{rowname:28s}" + "".join(f"{cells[g][0]:7.2f} ({cells[g][1]:4.2f})".rjust(16) for g in cols_short)
    print(line)

# Rows 3-5: changes
# Row 3 = change in means (unbalanced); Rows 4/5 = paired change (balanced)
row3 = {g: (mean_se(sub["fte2"])[0] - mean_se(sub["fte1"])[0],
             np.sqrt(mean_se(sub["fte2"])[1] ** 2 + mean_se(sub["fte1"])[1] ** 2))
        for g, sub in groups.items()}
row4 = {g: mean_se(sub["dfte"]) for g, sub in groups.items()}

df5 = df.copy()
df5.loc[df5["STATUS2"].isin([2, 4, 5]), "fte2"] = 0.0
df5["dfte"] = df5["fte2"] - df5["fte1"]
g5 = {
    "PA": df5[df5["STATE"] == 0],
    "NJ": df5[df5["STATE"] == 1],
    "low": df5[(df5["STATE"] == 1) & (df5["wcat"] == "low")],
    "mid": df5[(df5["STATE"] == 1) & (df5["wcat"] == "mid")],
    "high": df5[(df5["STATE"] == 1) & (df5["wcat"] == "high")],
}
row5 = {g: mean_se(sub["dfte"]) for g, sub in g5.items()}

for name, r in [("3. change (all available)", row3),
                ("4. change (balanced)", row4),
                ("5. change (temp-closed=0)", row5)]:
    line = f"{name:28s}" + "".join(f"{r[g][0]:7.2f} ({r[g][1]:4.2f})".rjust(16) for g in cols_short)
    print(line)

# Differences (columns iii, vii, viii)
print("\n  Differences (SE = sqrt(se_a^2 + se_b^2)):")
for a, b, lbl in [("NJ", "PA", "NJ - PA"), ("low", "high", "low - high"), ("mid", "high", "mid - high")]:
    d, se = diff_se(row4[a][0], row4[a][1], row4[b][0], row4[b][1])
    t = d / se
    print(f"    {lbl:10s} = {d:6.2f}  (se {se:4.2f}, t {t:5.2f})   [paper: NJ-PA 2.76, t=2.03]")

# Canonical DiD via OLS on the balanced change
s = df.dropna(subset=["dfte", "STATE"])
X = sm.add_constant(s["STATE"].astype(float))
m = sm.OLS(s["dfte"].astype(float), X).fit()
print(f"\n  [OLS, balanced] DiD = {m.params['STATE']:.2f} (se {m.bse['STATE']:.2f}, "
      f"t {m.tvalues['STATE']:.2f}, n {len(s)})   paper: 2.76 (t 2.03)")

# ----------------------------------------------------------------------------
# 4. Table 4 -- reduced-form regressions for the change in employment
# ----------------------------------------------------------------------------
print("\n" + "=" * 92)
print("TABLE 4 -- reduced-form models for the change in FTE employment")
print("=" * 92)

# Sample: valid employment both waves + valid wave-1 wage + (valid wave-2 wage
# OR permanently closed).  Reproduces the paper's N = 357.
sample4 = df[(df["fte1"].notna()) & (df["fte2"].notna()) &
             (df["WAGE_ST"].notna()) &
             (df["WAGE_ST2"].notna() | (df["STATUS2"] == 3))].copy()

print(f"N = {len(sample4)}  [paper: 357]")
print(f"dep. var.: mean = {sample4['dfte'].mean():.3f}, sd = {sample4['dfte'].std(ddof=1):.3f}"
      f"  [paper: -0.237, 8.825]")
print(f"mean GAP among NJ stores = {sample4[sample4['STATE']==1]['gap'].mean():.3f}  [paper: 0.11]")

chain_controls = ["chain_bk", "chain_kfc", "chain_roys", "co_owned"]
reg = pd.get_dummies(sample4["region"], prefix="reg", drop_first=True).astype(float)
sample4 = pd.concat([sample4.reset_index(drop=True), reg.reset_index(drop=True)], axis=1)

specs = [
    ("(i)", "NJ dummy, no controls", "STATE", None),
    ("(ii)", "NJ dummy + chain/own", "STATE", "chain"),
    ("(iii)", "GAP, no controls", "gap", None),
    ("(iv)", "GAP + chain/own", "gap", "chain"),
    ("(v)", "GAP + chain/own + region", "gap", "region"),
]
paper4 = {"(i)": "2.33 (1.19)", "(ii)": "2.30 (1.20)", "(iii)": "15.65 (6.08)",
          "(iv)": "14.92 (6.21)", "(v)": "11.91 (7.39)"}

print(f"{'col':6s} {'spec':28s} {'coef':>8s} {'se':>7s} {'t':>7s}   paper")
table4_rows = []
for key, label, treat, ctl in specs:
    cols = [treat]
    if ctl == "chain":
        cols += chain_controls
    elif ctl == "region":
        cols += chain_controls + list(reg.columns)
    X = sm.add_constant(sample4[cols].astype(float))
    m = sm.OLS(sample4["dfte"].astype(float), X).fit()
    table4_rows.append([key, label, m.params[treat], m.bse[treat], m.tvalues[treat], paper4[key]])
    print(f"{key:6s} {label:28s} {m.params[treat]:8.3f} {m.bse[treat]:7.2f} {m.tvalues[treat]:7.2f}   {paper4[key]}")

pd.DataFrame(table4_rows, columns=["col", "spec", "coef", "se", "t", "paper"]).to_csv(
    "output/table4.csv", index=False)

# ----------------------------------------------------------------------------
# 5. Figure 1 -- distribution of starting wages (2 states x 2 waves)
# ----------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharex=True, sharey=True)
bins = np.arange(4.0, 6.6, 0.25)
panels = [
    ("New Jersey, February 1992", "WAGE_ST", 1),
    ("Pennsylvania, February 1992", "WAGE_ST", 0),
    ("New Jersey, November 1992", "WAGE_ST2", 1),
    ("Pennsylvania, November 1992", "WAGE_ST2", 0),
]
for ax, (title, wvar, state) in zip(axes.ravel(), panels):
    w = df.loc[df["STATE"] == state, wvar].dropna()
    ax.hist(w, bins=bins, color="#9b7b5f", edgecolor="white", linewidth=0.6)
    ax.axvline(4.25, color="#bf5b3f", linestyle="--", linewidth=1.1)
    ax.axvline(5.05, color="#17324d", linestyle="--", linewidth=1.1)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel("Number of stores", fontsize=9)
fig.text(0.5, 0.02, "Starting wage ($/hour)", ha="center", fontsize=10)
fig.suptitle("Figure 1. Distribution of starting wage rates", fontsize=12)
plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig("output/figure_1.png", dpi=150)

# ----------------------------------------------------------------------------
# 6. Independent extension -- store-size heterogeneity in the employment effect
# ----------------------------------------------------------------------------
print("\n" + "=" * 92)
print("EXTENSION -- store-size heterogeneity in the employment effect")
print("=" * 92)

# Median of wave-1 FTE employment, computed on the balanced sample (paper: 19.5).
median_fte1 = df.dropna(subset=["dfte"])["fte1"].median()
print(f"median wave-1 FTE (balanced sample) = {median_fte1:.2f}")

df["large"] = np.where(df["fte1"].isna(), np.nan,
                       (df["fte1"] > median_fte1).astype(float))


def _did(data):
    """DiD of dfte on STATE (HC1 robust SE), for a subset of stores."""
    d = data.dropna(subset=["dfte", "STATE"])
    X = sm.add_constant(d["STATE"].astype(float))
    m = sm.OLS(d["dfte"].astype(float), X).fit(cov_type="HC1")
    return m.params["STATE"], m.bse["STATE"], m.tvalues["STATE"]


# (a) Median split: DiD separately for large and small stores
large_did = _did(df[df["large"] == 1.0])
small_did = _did(df[df["large"] == 0.0])
print(f"median-split DiD: large = {large_did[0]:+.2f} (se {large_did[1]:.2f}, "
      f"t {large_did[2]:.2f})")
print(f"median-split DiD: small = {small_did[0]:+.2f} (se {small_did[1]:.2f}, "
      f"t {small_did[2]:.2f})")

# (b) Interaction: state x large
d = df.dropna(subset=["dfte", "STATE", "large"])
Xi = sm.add_constant(d[["STATE", "large"]].astype(float))
Xi["STATE_large"] = d["STATE"] * d["large"]
mi = sm.OLS(d["dfte"].astype(float), Xi.astype(float)).fit(cov_type="HC1")
print(f"interaction state x large = {mi.params['STATE_large']:.2f} "
      f"(se {mi.bse['STATE_large']:.2f}, t {mi.tvalues['STATE_large']:.2f})")

# (c) Continuous interaction: state x wave-1 FTE
d2 = df.dropna(subset=["dfte", "STATE", "fte1"])
Xc = sm.add_constant(d2[["STATE", "fte1"]].astype(float))
Xc["STATE_fte1"] = d2["STATE"] * d2["fte1"]
mc = sm.OLS(d2["dfte"].astype(float), Xc.astype(float)).fit(cov_type="HC1")
print(f"continuous interaction state x fte1 = {mc.params['STATE_fte1']:.2f} "
      f"(se {mc.bse['STATE_fte1']:.2f}, t {mc.tvalues['STATE_fte1']:.2f})")

# Save Table 3 to CSV (levels + changes)
t3 = pd.DataFrame({
    "row": ["1. FTE before", "2. FTE after", "3. change (all available)",
            "4. change (balanced)", "5. change (temp-closed=0)"],
})
for g in cols_short:
    t3[g] = [row1[g][0], row2[g][0], row3[g][0], row4[g][0], row5[g][0]]
    t3[g + "_se"] = [row1[g][1], row2[g][1], row3[g][1], row4[g][1], row5[g][1]]
t3.to_csv("output/table3.csv", index=False)

# Save the processed analysis dataset (constructed variables)
df.to_csv("output/processed_data.csv", index=False)

print("\nSaved outputs to output/: figure_1.png, table2.csv, table3.csv, table4.csv, processed_data.csv")
