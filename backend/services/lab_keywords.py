import re

lab_keywords = {

    # CBC Primary
    "hemoglobin": r"(haemoglobin|hemoglobin|hb)\s*([\d.]+)",
    "rbc": r"(rbc\s*count|rbc)\s*([\d.]+)",
    "wbc": r"(wbc\s*count|total\s*wbc|white\s*blood\s*cell)\s*([\d.]+)",
    "platelets": r"(platelet\s*count|platelets)\s*([\d.]+)",
    "pcv": r"(pcv|packed\s*cell\s*volume)\s*([\d.]+)",

    # Differential Count
    "neutrophils": r"(neutrophils)\s*([\d.]+)",
    "lymphocytes": r"(lymphocytes)\s*([\d.]+)",
    "eosinophils": r"(eosinophils)\s*([\d.]+)",
    "monocytes": r"(monocytes)\s*([\d.]+)",
    "basophils": r"(basophils)\s*([\d.]+)",

    # Red Cell Indices
    "mcv": r"(mcv)\s*([\d.]+)",
    "mch": r"(mch)\s*([\d.]+)",
    "mchc": r"(mchc)\s*([\d.]+)",
    "rdw": r"(rdw)\s*([\d.]+)",

    # Thyroid
    "tsh": r"(tsh)\s*([\d.]+)",

    # Sugar
    "glucose": r"(glucose|blood\s*sugar)\s*([\d.]+)",
    
    # Kidney Function Tests (for CKD detection)
    "creatinine": r"(creatinine|serum\s*creatinine)\s*([\d.]+)",
    "egfr": r"(egfr|e\.gfr|estimated\s*gfr|gfr)\s*([\d.]+)",
    "bun": r"(bun|blood\s*urea\s*nitrogen|urea\s*nitrogen)\s*([\d.]+)",
    "albumin": r"(albumin|serum\s*albumin)\s*([\d.]+)",
    
    # Cholesterol
    "cholesterol": r"(total\s*cholesterol|cholesterol)\s*([\d.]+)",
    "hdl": r"(hdl|hdl\s*cholesterol)\s*([\d.]+)",
    "ldl": r"(ldl|ldl\s*cholesterol)\s*([\d.]+)",
    "triglycerides": r"(triglycerides)\s*([\d.]+)",
}

