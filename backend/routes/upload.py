from fastapi import APIRouter, UploadFile, File
import uuid, os
from database.mongo import reports_collection
from datetime import datetime

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_report(file: UploadFile = File(...)):

    report_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1]
    file_name = f"{report_id}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    reports_collection.insert_one({
        "report_id": report_id,
        "file_name": file_name,
        "uploaded_at": datetime.utcnow(),
        "status": "uploaded"
    })

    return {
        "status": "saved",
        "report_id": report_id,
        "file_name": file_name
    }
