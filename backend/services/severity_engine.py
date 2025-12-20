from .normal_ranges import normal_ranges

def calculate_deviation(value, low, high):
    mid = (low + high) / 2
    return round(((value - mid) / mid) * 100, 2)

def classify_severity(deviation):
    deviation = abs(deviation)

    if deviation < 5:
        return "Mild"
    elif deviation < 15:
        return "Medium"
    else:
        return "High"
