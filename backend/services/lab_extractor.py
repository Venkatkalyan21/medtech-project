import re
from services.lab_keywords import lab_keywords

def extract_lab_values(text):
    results = {}
    patterns = lab_keywords
    for key, pattern in patterns.items():
        find = re.search(pattern, text, re.IGNORECASE)
        if find:
            try:
                if key == "blood_pressure":
                    # Store as a list [systolic, diastolic]
                    results["bp_sys"] = float(find.group(2))
                    results["bp_dia"] = float(find.group(3))
                else:
                    results[key] = float(find.group(2))
            except:
                pass
    return results
