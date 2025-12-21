import pandas as pd
import numpy as np

n = 200
np.random.seed(42)

age = np.random.randint(25, 90, n)
gender = np.random.choice(["M", "F"], n)
creatinine = np.round(np.random.normal(1.1, 0.4, n), 2)

def calc_egfr(c, a):
    return 175 * (c ** -1.154) * (a ** -0.203)

egfr = np.array([round(calc_egfr(c, a), 1) for c, a in zip(creatinine, age)])

bmi = np.round(np.random.normal(24, 4, n), 1)
glucose = np.round(np.random.normal(105, 20, n), 2)
systolic = np.random.randint(100, 170, n)

CKD = (egfr < 60).astype(int)

df = pd.DataFrame({
    "age": age,
    "gender": gender,
    "creatinine": creatinine,
    "egfr": egfr,
    "bmi": bmi,
    "glucose": glucose,
    "systolic": systolic,
    "CKD": CKD
})

df.to_csv("ckd_synthetic.csv", index=False)
print(df.head())
