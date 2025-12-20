import pytesseract
from pdf2image import convert_from_path
import os

TESSERACT_PATH = r"C:\tessract\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text_from_pdf(pdf_path: str):

    pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)

    text_output = ""

    for page in pages:
        text_output += pytesseract.image_to_string(page)

    return text_output
