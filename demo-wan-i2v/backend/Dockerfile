# demo-wan-i2v/backend/Dockerfile

# 1. Базовый образ (с поддержкой CUDA, можно даже на Mac, GPU не будет, но образ с CUDA тоже подойдёт)
FROM nvidia/cuda:12.9.0-devel-ubuntu22.04 AS backend

# 2. Устанавливаем системные зависимости и Python 3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3-pip git curl wget ffmpeg build-essential ninja-build \
    libglib2.0-0 libsndfile1 ca-certificates && \
    ln -sf /usr/bin/python3.11 /usr/bin/python

# 3. Устанавливаем pip, FastAPI, Uvicorn, PyTorch и moviepy (+imageio-ffmpeg, если нужно)
# 3. Устанавливаем pip-пакеты
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
        torch torchvision torchaudio \
        fastapi uvicorn \
        moviepy imageio-ffmpeg

# 4. Копируем весь код backend внутрь контейнера
COPY ./backend/ /app/

WORKDIR /app

# 5. Копируем и делаем исполняемым скрипт запуска backend (скрипт лежит в frontend/src)
COPY ./frontend/src/start_script_backend.sh /start_script.sh
RUN chmod +x /start_script.sh

# 6. Открываем нужные порты (8000, 8188, 8888)
EXPOSE 8000 8188 8888

# 7. Запускаем скрипт, который стартует uvicorn (FastAPI)
CMD ["/start_script_backend.sh"]
