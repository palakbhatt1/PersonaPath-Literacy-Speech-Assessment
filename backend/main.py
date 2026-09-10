from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import shutil

from inference import pronunciation_pipeline, analyze_presentation

app = FastAPI(title="PersonaPath API")

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup CORS
allowed_origin = os.environ.get("ALLOWED_ORIGIN", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "cors_origin": allowed_origin}

@app.post("/api/analyze_phase1")
async def analyze_phase1(
    audio: UploadFile = File(...), 
    reference_text: str = Form(...)
):
    if not audio or not reference_text:
        raise HTTPException(status_code=400, detail="Missing audio or reference text")
    
    file_path = "uploaded_audio.wav"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
        
    try:
        result = pronunciation_pipeline(file_path, reference_text)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_video(video: UploadFile = File(...)):
    if not video:
        raise HTTPException(status_code=400, detail="Missing video")
        
    file_path = "uploaded_video.mp4"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
        
    try:
        result = analyze_presentation(file_path)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
