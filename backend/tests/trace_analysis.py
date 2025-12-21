import os
import sys
import traceback

# Add current dir to path
sys.path.append(os.getcwd())

print("Loading services...")
try:
    from services.ocr_engine import extract_text_from_pdf
    from services.lab_extractor import extract_lab_values
    from services.abnormality_engine import check_abnormalities
    from services.health_score import generate_health_score
    from services.ml_service import ml_service
    from services.agent_service import get_agent_analysis
    print("✅ Services loaded")
except Exception:
    traceback.print_exc()
    sys.exit(1)

def run_test():
    file_path = "uploads/88562088-3554-4c3a-892d-bc2dce078516.pdf"
    if not os.path.exists(file_path):
        print(f"❌ File missing: {file_path}")
        return

    try:
        print("\n1. Running OCR...")
        text = extract_text_from_pdf(file_path)
        print(f"✅ OCR Done, length: {len(text)}")

        print("\n2. Extracting Labs...")
        labs = extract_lab_values(text)
        print(f"✅ Labs: {labs}")

        print("\n3. Checking Abnormalities...")
        alerts = check_abnormalities(labs)
        print(f"✅ Alerts: {len(alerts)}")

        print("\n4. Running ML Prediction...")
        ckd_input = ml_service.map_labs_to_ckd(labs)
        ckd_result = ml_service.predict_ckd(ckd_input)
        print(f"✅ ML Result: {ckd_result}")

        print("\n5. Running Agent Analysis...")
        agent_analysis = get_agent_analysis(labs, alerts, ckd_result)
        print(f"✅ Agent Analysis: {agent_analysis.keys()}")
        
        print("\n✨ ALL STEPS PASSED")

    except Exception:
        print("\n❌ FAILED at some step")
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
