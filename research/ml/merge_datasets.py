import sys
import pandas as pd

uci = pd.read_csv("uci_ready.csv")
try:
    kag = pd.read_csv("kidney_disease.csv")
except FileNotFoundError:
    print("kidney_disease.csv not found; proceeding with UCI only.")
    kag = None

def normalize_target(df: pd.DataFrame) -> pd.DataFrame:
    # normalize common target column names to 'class'
    if "classification" in df.columns:
        df = df.rename(columns={"classification": "class"})
    if "CKD" in df.columns:
        df = df.rename(columns={"CKD": "class"})
    if "Class" in df.columns and "class" not in df.columns:
        df = df.rename(columns={"Class": "class"})
    # canonicalize textual labels where present
    if "class" in df.columns:
        df["class"] = df["class"].astype(str).str.strip().str.lower().map(
            {"ckd": "1", "notckd": "0", "yes": "1", "no": "0", "present": "1", "notpresent": "0",
             "true": "1", "false": "0"}
        ).fillna(df["class"])
    return df

uci = normalize_target(uci)
if kag is not None:
    kag = normalize_target(kag)

# ensure at least one dataset has a target
if "class" not in uci.columns and (kag is None or "class" not in kag.columns):
    print("No 'class' (target) column found in either dataset; cannot merge with target. Add/normalize target first.", file=sys.stderr)
    sys.exit(1)

# decide final columns to keep: intersection of available columns (prefer consistency)
if kag is None:
    final_cols = list(uci.columns)
else:
    common = set(uci.columns).intersection(set(kag.columns))
    final = sorted(common)
    # make sure 'class' is included if present in either dataset
    if "class" in uci.columns or "class" in kag.columns:
        if "class" not in final:
            final.append("class")
    final_cols = final

def ensure_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    for c in cols:
        if c not in df.columns:
            df[c] = pd.NA
    return df[cols]

if kag is None:
    merged = uci[final_cols].copy()
else:
    uci_final = ensure_columns(uci, final_cols)
    kag_final = ensure_columns(kag, final_cols)
    merged = pd.concat([uci_final, kag_final], ignore_index=True)

# try to coerce 'class' into numeric 0/1 where possible
if "class" in merged.columns:
     # map common textual labels first, keep original numeric where mapping doesn't apply,
   # then coerce to numeric and use pandas nullable Int64
    s = merged["class"].astype(str).str.strip().str.lower()
    mapped = s.map({"ckd": 1, "notckd": 0, "yes": 1, "no": 0, "present": 1, "notpresent": 0, "true": 1, "false": 0})
    # preserve existing numeric values when mapping didn't change anything
    original_num = pd.to_numeric(merged["class"], errors="coerce")
    merged["class"] = mapped.where(mapped.notna(), original_num)
    merged["class"] = pd.to_numeric(merged["class"], errors="coerce").astype("Int64")
merged.to_csv("ckd_real_merged.csv", index=False)
print("Merged dataset shape:", merged.shape)