#!/usr/bin/env python3
"""Fill the report with real numbers.

Usage:  python make_results_table.py <data_dir> <tables_dir>

Reads  <data_dir>/results.csv (columns: feature_set, model, accuracy, precision,
recall, f1, roc_auc) and <data_dir>/train.csv, val.csv, test.csv (index or a
'Date' column, plus 'target').
Writes <tables_dir>/results_table.tex and <tables_dir>/summary_macros.tex.
"""
import sys, math
import pandas as pd

import os
data_dir, tab_dir = sys.argv[1], sys.argv[2]
opt = dict(a.lstrip("-").split("=") for a in sys.argv[3:])   # e.g. --test_n=297 --test_up=149
res = pd.read_csv(f"{data_dir}/results.csv")
res["feature_set"] = res["feature_set"].str.replace("-only", "", regex=False)

def load(name):
    df = pd.read_csv(f"{data_dir}/{name}.csv")
    dcol = "Date" if "Date" in df.columns else df.columns[0]
    df[dcol] = pd.to_datetime(df[dcol])
    return df, dcol

have_splits = all(os.path.exists(f"{data_dir}/{n}.csv") for n in ("train", "val", "test"))
if have_splits:
    tr, dc = load("train"); va, _ = load("val"); te, _ = load("test")
    rng = lambda d: f"{d[dc].min():%d %b %Y} to {d[dc].max():%d %b %Y}"
    n_te, up = len(te), te["target"].mean()
else:
    n_te, up = int(opt["test_n"]), int(opt["test_up"]) / int(opt["test_n"])
base = max(up, 1 - up)
moe = 1.96 * math.sqrt(0.5 * 0.5 / n_te) * 100

sets = [("numerical", "Numerical-only"), ("sentiment", "Sentiment-only"), ("multimodal", "Multimodal")]
models = ["Logistic Regression", "Random Forest", "XGBoost"]
cols = ["accuracy", "precision", "recall", "f1", "roc_auc"]

best_row = res.loc[res["roc_auc"].idxmax()]
lines = [r"\begin{tabular}{@{}llccccc@{}}", r"\toprule",
         r"Feature set & Model & Accuracy & Precision & Recall & F1 & ROC-AUC \\", r"\midrule"]
for si, (key, label) in enumerate(sets):
    for mi, m in enumerate(models):
        r = res[(res.feature_set == key) & (res.model == m)].iloc[0]
        cells = []
        for c in cols:
            v = f"{r[c]:.3f}"
            if r.name == best_row.name and c == "roc_auc":
                v = r"\textbf{" + v + "}"
            cells.append(v)
        lines.append(f"{label if mi == 0 else ''} & {m} & " + " & ".join(cells) + r" \\")
    if si < 2:
        lines.append(r"\midrule")
lines += [r"\midrule", rf"\multicolumn{{2}}{{l}}{{Majority-class baseline}} & {base:.3f} & -- & -- & -- & 0.500 \\",
          r"\bottomrule", r"\end{tabular}"]
open(f"{tab_dir}/results_table.tex", "w").write("\n".join(lines) + "\n")

best_by = res.groupby("feature_set")["roc_auc"].max()
macros = {
    "TestDays": str(n_te),
    "UpShareTest": f"{up*100:.1f}\\%", "BaselineAcc": f"{base*100:.1f}\\%",
    "MarginErr": f"$\\pm${moe:.1f}",
    "BestModel": best_row["model"],
    "BestFeatureSet": {"numerical": "numerical-only", "sentiment": "sentiment-only", "multimodal": "multimodal"}[best_row["feature_set"]],
    "BestAcc": f"{best_row['accuracy']*100:.1f}\\%", "BestAUC": f"{best_row['roc_auc']:.3f}",
    "NumBestAUC": f"{best_by['numerical']:.3f}", "MMBestAUC": f"{best_by['multimodal']:.3f}",
    "AUCDelta": f"{best_by['multimodal'] - best_by['numerical']:+.3f}",
}
if have_splits:
    macros.update({"TrainDays": str(len(tr)), "ValDays": str(len(va)), "TrainRange": rng(tr), "ValRange": rng(va), "TestRange": rng(te)})
else:  # keep yellow placeholders for what cannot be derived from results.csv alone
    for k, t in [("TrainDays","train days"),("ValDays","validation days"),("TrainRange","train date range"),("ValRange","validation date range"),("TestRange","test date range")]:
        macros[k] = r"\tbd{%s}" % t
with open(f"{tab_dir}/summary_macros.tex", "w") as f:
    for k, v in macros.items():
        f.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
print("written", tab_dir)
