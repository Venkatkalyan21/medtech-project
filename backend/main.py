from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.upload import router as upload_router
from routes.analyze import router as analyze_router
from routes.download import router as download_router

app = FastAPI(
    title="MedTech Early Disease Prediction API",
    version="1.0"
)

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(download_router)

@app.get("/")
def home():
    return {"message": "Backend is running!"}

