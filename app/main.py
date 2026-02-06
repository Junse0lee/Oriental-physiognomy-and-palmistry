from fastapi import FastAPI
from app.api import face_analysis  # 우리가 만든 파일 불러오기

app = FastAPI(title="Oriental Physiognomy API")

# API 경로 연결 (prefix를 주면 주소 앞에 자동으로 붙습니다)
app.include_router(face_analysis.router, prefix="/face", tags=["Face Analysis"])

@app.get("/")
def root():
    return {"message": "Main Server is running"}