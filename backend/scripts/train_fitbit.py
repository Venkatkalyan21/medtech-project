import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import joblib
import os

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FITBIT_DIR = os.path.join(os.path.dirname(BASE_DIR), "fitbit")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Create models directory if not exists
os.makedirs(MODELS_DIR, exist_ok=True)

def train_fitbit_model():
    print("Loading fitbit datasets...")
    try:
        activity = pd.read_csv(os.path.join(FITBIT_DIR, "dailyActivity_merged1.csv"))
        sleep = pd.read_csv(os.path.join(FITBIT_DIR, "sleepDay_merged.csv"))
        weight = pd.read_csv(os.path.join(FITBIT_DIR, "weightLogInfo_merged.csv"))
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # Standardize date columns
    print("Preprocessing dates...")
    activity["Date"] = pd.to_datetime(activity["ActivityDate"])
    sleep["Date"] = pd.to_datetime(sleep["SleepDay"])
    weight["Date"] = pd.to_datetime(weight["Date"])

    activity.drop(columns=["ActivityDate"], inplace=True)
    sleep.drop(columns=["SleepDay"], inplace=True)

    # Aggregate sleep
    sleep_agg = sleep.groupby(["Id", "Date"], as_index=False).mean(numeric_only=True)

    # Merge datasets
    print("Merging datasets...")
    merged = pd.merge(activity, sleep_agg, on=["Id", "Date"], how="left")
    merged = pd.merge(merged, weight, on=["Id", "Date"], how="left")

    # Feature Engineering
    df = merged.copy()
    df["day"] = df["Date"].dt.day
    df["month"] = df["Date"].dt.month
    df["weekday"] = df["Date"].dt.weekday
    df.drop(columns=["Date"], inplace=True)

    # Drop ID
    df.drop(columns=["Id"], inplace=True)

    # Drop columns with 100% nulls
    df = df.dropna(axis=1, how="all")

    # Impute missing values
    print("Imputing missing values...")
    imputer = SimpleImputer(strategy="median")
    # Fit and transform
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    # Scale data
    print("Scaling data...")
    scaler = RobustScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_imputed), columns=df.columns)

    # Train Isolation Forest
    print("Training Isolation Forest...")
    model = IsolationForest(
        n_estimators=400,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    )
    model.fit(df_scaled)

    # Save assets
    print("Saving models...")
    joblib.dump(model, os.path.join(MODELS_DIR, "fitbit_model.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "fitbit_scaler.pkl"))
    joblib.dump(imputer, os.path.join(MODELS_DIR, "fitbit_imputer.pkl"))
    
    # Save column names to ensure input data matches training data
    joblib.dump(df.columns.tolist(), os.path.join(MODELS_DIR, "fitbit_columns.pkl"))

    print("✅ Fitbit anomaly model trained and saved.")

if __name__ == "__main__":
    train_fitbit_model()
