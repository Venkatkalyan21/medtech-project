from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import uuid

router = APIRouter()

UPLOAD_DIR = Path("uploaded_reports")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload_report")
async def upload_report(file: UploadFile = File(...)):

    # Validate file type (restrict allowed formats)
    allowed = ["application/pdf", "image/jpeg", "image/png"]

    if file.content_type not in allowed:
        return {"error": "File format not allowed!"}

    # random name to avoid overwrites
    file_id = uuid.uuid4().hex
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "msg": "File uploaded successfully!",
        "filename": file_path.name,
        "path": str(file_path)
    }
