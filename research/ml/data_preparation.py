import sys
import pandas as pd

df = pd.read_csv("uci_ckd.csv")

# treat "?" as missing
df = df.replace("?", pd.NA)

# attempt numeric conversion but keep strings if conversion produces all NaN
for col in df.columns:
    conv = pd.to_numeric(df[col], errors="coerce")
    if conv.notna().sum() > 0:
        # keep converted values where possible, preserve non-convertible as NA
        df[col] = conv.where(conv.notna(), df[col])

print("Columns (UCI):", list(df.columns))

# locate target column
target_candidates = ["classification", "class", "CKD", "ckd", "Class"]
target_col = next((c for c in target_candidates if c in df.columns), None)
if target_col is None:
    print("No target column found. Columns:", list(df.columns))
    sys.exit(1)

def map_target(val):
    if pd.isna(val):
        return pd.NA
    s = str(val).strip().lower()
    if s in ("ckd", "yes", "present", "1", "true", "t"):
        return 1
    if s in ("notckd", "no", "notpresent", "0", "false", "f"):
        return 0
    try:
        # numeric strings
        return int(float(s))
    except Exception:
        return pd.NA

# if already numeric (0/1), keep; otherwise map common labels
if not pd.api.types.is_integer_dtype(df[target_col]) and not pd.api.types.is_float_dtype(df[target_col]):
    df[target_col] = df[target_col].apply(map_target)

df.to_csv("uci_ckd_clean.csv", index=False)

# optional: compare with Kaggle file if present
try:
    kaggle = pd.read_csv("kidney_disease.csv")
    print("Columns (Kaggle):", list(kaggle.columns))
except FileNotFoundError:
    print("kidney_disease.csv not found; skipping Kaggle compare.")

df = pd.read_csv("uci_ckd_clean.csv")

# Map categorical medical text to numeric
cat_map = {
    "normal": 1,
    "abnormal": 0,
    "yes": 1,
    "no": 0,
    "good": 1,
    "poor": 0,
    "present": 1,
    "notpresent": 0
}

categorical_columns = ["rbc","pc","pcc","ba","htn","dm","cad","appet","pe","ane"]

for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].replace(cat_map)

# convert remaining object columns to numeric if possible
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill numeric missing values with median
num_cols = df.select_dtypes(include=["float64","int64"]).columns
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

df.rename(columns={"class":"classification"}, inplace=True)
# Save training‑ready UCI dataset
df.to_csv("uci_ready.csv", index=False)

print("UCI Dataset cleaned → saved as uci_ready.csv")
print(df.head())
print(df.isna().sum())
