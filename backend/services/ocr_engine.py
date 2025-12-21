import pytesseract
from pdf2image import convert_from_path
import os
import pdfplumber

# Legacy paths - kept for fallback
TESSERACT_PATH = r"C:\tessract\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text_from_pdf(pdf_path: str):
    # Try pdfplumber first (best for text-based PDFs)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if text.strip():
                print("✅ Text extracted via pdfplumber")
                return text
    except Exception as e:
        print(f"pdfplumber failed: {e}")

    # Fallback to OCR if pdfplumber found nothing or failed
    print("Falling back to Tesseract OCR...")
    try:
        pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
        text_output = ""
        for page in pages:
            text_output += pytesseract.image_to_string(page)
        return text_output
    except Exception as e:
        raise RuntimeError(f"OCR failed: {e}. Ensure Tesseract and Poppler are installed for scanned reports.")
