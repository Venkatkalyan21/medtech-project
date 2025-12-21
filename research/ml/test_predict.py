import pandas as pd

df = pd.read_csv("ckd_synthetic.csv")

df = df.fillna(df.median(numeric_only=True))
print(df.isnull().sum())