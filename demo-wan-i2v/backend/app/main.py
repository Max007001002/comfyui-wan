# backend/app/main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from .worker import generate_video_task_async
from uuid import uuid4
import os

app = FastAPI(title="WAN-2.1 i2v Demo")

# Создаем директорию для загруженных изображений
os.makedirs("/app/uploads", exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.post("/api/generate")
async def generate(
        image: UploadFile = File(...),
        prompt: str = Form(...),
        negative_prompt: str = Form(""),
        duration: float = Form(2),
        fps: int = Form(16),
        steps: int = Form(32),
):
    # Валидация входных данных
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    if duration < 0.1 or duration > 10:
        raise HTTPException(status_code=400, detail="Duration must be between 0.1 and 10 seconds")

    if fps < 1 or fps > 60:
        raise HTTPException(status_code=400, detail="FPS must be between 1 and 60")

    if steps < 1 or steps > 100:
        raise HTTPException(status_code=400, detail="Steps must be between 1 and 100")

    try:
        job_id = str(uuid4())
        content = await image.read()

        # Сохраняем изображение
        image_path = f"/app/uploads/{job_id}.jpg"
        with open(image_path, "wb") as f:
            f.write(content)

        # Запускаем задачу в Celery
        generate_video_task_async.delay(
            job_id,
            content,
            prompt,
            negative_prompt,
            duration,
            fps,
            steps
        )

        return {
            "job_id": job_id,
            "status": "queued",
            "message": "Video generation task has been queued"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
