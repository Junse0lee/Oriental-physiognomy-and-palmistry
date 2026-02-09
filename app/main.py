from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import face_analysis, hand_analysis

app = FastAPI()

# ✅ 1. CORS 설정 (프론트엔드 Next.js와 통신하기 위해 필수!)
# 개발 환경에서는 모든 출처를 허용하도록 설정합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    # ngrok 건너뛰기 헤더를 명시적으로 허용 리스트에 추가합니다.
    allow_headers=["*", "ngrok-skip-browser-warning"], 
)

# ✅ 2. API 라우터 등록
# 얼굴 분석: /face/analyze
app.include_router(face_analysis.router, prefix="/face", tags=["Face Analysis"])
# 손금 분석: /hand/analyze
app.include_router(hand_analysis.router, tags=["Hand Analysis"])

@app.get("/")
def root():
    return {"message": "Server is running"}