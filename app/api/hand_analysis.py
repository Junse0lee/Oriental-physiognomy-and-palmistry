from fastapi import APIRouter, File, UploadFile
import os
from app.services.palm_service import PalmService

router = APIRouter()

# 모델 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "num_02.pt")

service= PalmService(MODEL_PATH)

@router.post("/hand/analyze")
async def analyze_hand(file: UploadFile = File(...)):
    contents = await file.read()
    result = service.analyze(contents)
    return {"status": "success", "data": result}