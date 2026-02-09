from fastapi import APIRouter, File, UploadFile
import os
# ✅ 현재 위치(app/api) 기준 임포트
from services.palm_service import PalmService

router = APIRouter()

# 모델 경로 설정
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "num_02.pt")
service = PalmService(MODEL_PATH)

@router.post("/hand/analyze")
async def analyze_hand(file: UploadFile = File(...)):
    contents = await file.read()
    result = service.analyze(contents)
    return {"status": "success", "data": result}