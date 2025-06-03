#!/usr/bin/env bash
set -e

# ───── 1. FastAPI  (порт 8000) ─────
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# ───── 2. Celery-воркеры  ─────
CUDA_VISIBLE_DEVICES=0 celery -A app.worker worker -Q gpu0 --concurrency=1 --hostname=worker0 &
CUDA_VISIBLE_DEVICES=1 celery -A app.worker worker -Q gpu1 --concurrency=1 --hostname=worker1 &

# ───── 3. ComfyUI  (порт 8188) ─────
if [[ "${INSTALL_COMFY}" == "true" ]]; then
  /ComfyUI/run.sh --listen 0.0.0.0 --port 8188 &
fi

# ───── 4. JupyterLab  (порт 8888) ─────
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser --LabApp.token='' &

# Ждём падения любого процесса
wait -n
