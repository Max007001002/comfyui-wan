import os, io, torch
import moviepy.video.io.ImageSequenceClip as msc
from PIL import Image
from celery import Celery
from wan.image2video import WanI2V
import teacache 
# import sageattention, flash_attn

celery_app = Celery("worker", broker=os.getenv("BROKER_URL", "redis://redis:6379/0"))

MODEL_DIR = os.getenv("WAN_MODEL_PATH", "/models/wan14B-720p")
pipe = None

def load_pipe():
    global pipe
    if pipe is None:
        try:
            pipe = WanI2VPipeline.from_pretrained(
                MODEL_DIR, torch_dtype=torch.float16
            ).to("cuda")
            teacache.patch(pipe.unet)
            sageattention.apply_sage_attention(pipe.unet, int8_kv=True)
        except Exception as e:
            print(f"Error loading pipeline: {str(e)}")
            raise
    return pipe

@celery_app.task(name="generate_video_task_async", bind=True)
def generate_video_task_async(self, job_id, img_bytes, prompt, neg, dur, fps, steps):
    try:
        device = torch.device("cuda")
        
        # Улучшенное декодирование изображения
        image = Image.open(io.BytesIO(img_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        pipeline = load_pipe()
        frames = pipeline(
            prompt=prompt,
            negative_prompt=neg,
            image=image,
            num_inference_steps=steps,
            fps=fps
        )

        # Создаем директорию для видео, если её нет
        os.makedirs("/app/videos", exist_ok=True)
        out_path = f"/app/videos/{job_id}.mp4"
        
        # Создаем и сохраняем видео
        clip = msc.ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(out_path, codec="libx264", preset="veryfast")
        
        return {"status": "success", "output_path": out_path}
    except Exception as e:
        print(f"Error in video generation: {str(e)}")
        return {"status": "error", "message": str(e)} 