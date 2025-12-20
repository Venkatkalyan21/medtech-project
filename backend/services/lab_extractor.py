import re
from services.lab_keywords import lab_keywords

def extract_lab_values(text):
    results = {}
    patterns = lab_keywords
    for key, pattern in patterns.items():
        find = re.search(pattern, text, re.IGNORECASE)
        if find:
            try:
                results[key] = float(find.group(2))
            except:
                pass
    return results
