import requests
import json

BASE_URL = "http://localhost:8000"

def test_ckd():
    print("\n--- Testing CKD Endpoint ---")
    data = {
        "age": 48.0, "al": 1.0, "ane": "no", "appet": "good", "ba": "notpresent", "bgr": 121.0, 
        "bp": 80.0, "bu": 36.0, "cad": "no", "dm": "yes", "hemo": 15.4, 
        "htn": "yes", "pc": "normal", "pcc": "notpresent", "pcv": 44, 
        "pe": "no", "pot": 4.4, "rbc": "normal", "sc": 1.2, "sg": 1.020, "sod": 138.0, "su": 0.0
    }
    # Note: Our trained model might have variations in field names, but the web_app usually sends a flat dict.
    # The payload structure is {"data": { ... }}
    payload = {"data": data}
    try:
        response = requests.post(f"{BASE_URL}/predict/ckd", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ CKD Success")
        else:
            print("❌ CKD Failed")
    except Exception as e:
        print(f"❌ CKD Error: {e}")

def test_heart():
    print("\n--- Testing Heart Endpoint ---")
    data = {
        "age_years": 50, 
        "bmi": 25, 
        "ap_hi": 120, 
        "ap_lo": 80, 
        "cholesterol": 1, 
        "gluc": 1, 
        "smoke": 0, 
        "alco": 0, 
        "active": 1
    }
    # Payload is direct for Heart endpoint
    try:
        response = requests.post(f"{BASE_URL}/predict/heart", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ Heart Success")
        else:
            print("❌ Heart Failed")
    except Exception as e:
        print(f"❌ Heart Error: {e}")

def test_fitbit():
    print("\n--- Testing Fitbit Endpoint ---")
    data = {
        "TotalSteps": 10000,
        "TotalDistance": 8.0,
        "TrackerDistance": 8.0,
        "LoggedActivitiesDistance": 0,
        "VeryActiveDistance": 4.0,
        "ModeratelyActiveDistance": 2.0,
        "LightActiveDistance": 2.0,
        "SedentaryActiveDistance": 0,
        "VeryActiveMinutes": 60,
        "FairlyActiveMinutes": 30,
        "LightlyActiveMinutes": 200,
        "SedentaryMinutes": 500,
        "Calories": 2500,
        "TotalSleepRecords": 1,
        "TotalMinutesAsleep": 400,
        "TotalTimeInBed": 450,
        "date": "2024-01-01"
    }
    try:
        response = requests.post(f"{BASE_URL}/predict/fitbit", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ Fitbit Success")
        else:
            print("❌ Fitbit Failed")
    except Exception as e:
        print(f"❌ Fitbit Error: {e}")

if __name__ == "__main__":
    test_ckd()
    test_heart()
    test_fitbit()
