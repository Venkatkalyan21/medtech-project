normal_ranges = {

    # -------- CBC CORE --------
    "hemoglobin": (13, 17),
    "rbc": (4.5, 6.0),
    "wbc": (4000, 11000),
    "platelets": (150, 450),
    "pcv": (40, 50),

    # -------- DIFFERENTIAL COUNT --------
    "neutrophils": (40, 75),
    "lymphocytes": (20, 40),
    "eosinophils": (1, 6),
    "monocytes": (2, 10),
    "basophils": (0, 1),

    # -------- RBC INDICES --------
    "mcv": (80, 100),
    "mch": (27, 32),
    "mchc": (32, 36),
    "rdw": (11, 15),

    # -------- THYROID --------
    "tsh": (0.4, 4.5),

    # -------- SUGAR --------
    "glucose": (70, 140),

    # -------- CHOLESTEROL --------
    "cholesterol": (125, 200),
    "hdl": (40, 60),
    "ldl": (0, 100),
    "triglycerides": (0, 150),

    # -------- LIVER (OPTIONAL FUTURE OCR) --------
    "sgot": (0, 35),
    "sgpt": (0, 35),
    "bilirubin": (0.1, 1.2),

    # -------- KIDNEY FUNCTION (FOR CKD DETECTION) --------
    "creatinine": (0.7, 1.3),
    "egfr": (90, 200),  # eGFR > 90 is normal
    "bun": (7, 20),
    "albumin": (3.5, 5.5),
    "urea": (10, 50)
}

