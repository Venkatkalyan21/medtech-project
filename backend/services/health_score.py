def generate_health_score(alert_data):
    score = 100
    for field in alert_data.values():
        if field["status"] == "NORMAL":
            continue

        if field["severity"] == "Mild":
            score -= 3
        elif field["severity"] == "Medium":
            score -= 7
        elif field["severity"] == "High":
            score -= 15

    return max(score, 0)
