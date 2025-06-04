# demo-wan-i2v/backend/Dockerfile
FROM nvidia/cuda:12.9.0-devel-ubuntu22.04

WORKDIR /app

# 1) Системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3.11 python3-pip git curl wget ffmpeg build-essential ninja-build \
      libglib2.0-0 libsndfile1 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 2) Скопировать requirements и установить их
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# 3) Скопировать исходники приложения и скрипт
COPY app /app/app
COPY start_script_backend.sh /app/start_script_backend.sh
RUN chmod +x /app/start_script_backend.sh

# 4) Запуск
CMD ["/app/start_script_backend.sh"]
