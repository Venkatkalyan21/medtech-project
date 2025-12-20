from .severity_engine import calculate_deviation, classify_severity
from services.normal_ranges import normal_ranges
def check_abnormalities(values):
    results = {}

    for test_name, value in values.items():

        if test_name not in normal_ranges:
            results[test_name] = {"status": "UNKNOWN"}
            continue

        low, high = normal_ranges[test_name]

        deviation = calculate_deviation(value, low, high)
        severity = classify_severity(deviation)

        if value < low:
            status = "LOW"
        elif value > high:
            status = "HIGH"
        else:
            status = "NORMAL"

        results[test_name] = {
            "status": status,
            "percent_deviation": deviation,
            "severity": severity
        }

    return results
