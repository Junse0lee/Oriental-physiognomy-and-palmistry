FROM python:3.10-slim

#시스템 의존성 설치
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH=/app

#현재 위치의 requirments.txt를 복사 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#실행 시 PYTHONPATH를 설정하여 app 패키지를 인식하게 함
#main:app 대신 app.main:app으로 호출해야 할 수 있습니다. 
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]