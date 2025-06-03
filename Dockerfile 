###############################################################################
# ──────────────────────────────  STAGE 1 : builder  ──────────────────────────
###############################################################################
FROM nvidia/cuda:12.9.0-devel-ubuntu22.04 AS builder

ARG INSTALL_WAN=true
ARG INSTALL_COMFY=true

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CMAKE_BUILD_PARALLEL_LEVEL=8 \
    PIP_PREFER_BINARY=1 \
    PATH="/opt/venv/bin:$PATH"

# ───────────────  Системные зависимости + Python 3.11  ───────────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.11 python3.11-venv python3.11-dev python3-pip \
        git curl wget ffmpeg ninja-build build-essential \
        aria2 git-lfs libgl1 libglib2.0-0 vim gcc && \
    ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip   && \
    python3.11 -m venv /opt/venv        && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ───────────────  NCCL 2.26.5  ───────────────
RUN wget -qO- https://developer.download.nvidia.com/compute/redist/nccl/v2.26.5/nccl_2.26.5-1+cuda12.9_x86_64.txz \
    | tar -xJ -C /usr/local/ && ldconfig

# ───────────────  Базовые python-пакеты  ───────────────
RUN pip install --upgrade pip setuptools wheel && \
    pip install packaging pyyaml opencv-python moviepy gdown triton

# ───────────────  WAN 2.1 + ускорители  ───────────────
RUN if [ "$INSTALL_WAN" = "true" ]; then \
      echo "🔧 Устанавливаем WAN 2.1 + FlashAttention" && \
      pip install torch==2.8.0+cu129 torchvision==0.19.0+cu129 torchaudio==2.4.0+cu129 \
          --extra-index-url https://download.pytorch.org/whl/cu129 && \
      pip install \
          git+https://github.com/Wan-Video/Wan2.1@main \
          git+https://github.com/ali-vilab/TeaCache@73d9573 \
          git+https://github.com/thu-ml/SageAttention@v2.0.1 && \
      pip install ninja && \
      MAX_JOBS=64 python -m pip -v install flash-attn --no-build-isolation && \
      pip install "huggingface_hub[cli]" && \
      huggingface-cli download Wan-AI/Wan2.1-I2V-14B-720P \
          --local-dir /models/wan14B-720p --quiet ; \
   else \
      echo "❌ WAN установка отключена" ; \
   fi

# ───────────────  ComfyUI + кастом-ноды  ───────────────
RUN if [ "$INSTALL_COMFY" = "true" ]; then \
      echo "🔧 Устанавливаем ComfyUI + плагины" && \
      pip install comfy-cli jupyterlab==4.* jupyterlab-lsp jupyter-server \
                 jupyter-server-terminals ipykernel jupyterlab_code_formatter && \
      /usr/bin/yes | comfy --workspace /ComfyUI install && \
      for repo in \
        https://github.com/ssitu/ComfyUI_UltimateSDUpscale.git \
        https://github.com/kijai/ComfyUI-KJNodes.git \
        https://github.com/rgthree/rgthree-comfy.git \
        https://github.com/kijai/ComfyUI-WanVideoWrapper.git ; \
      do \
        cd /ComfyUI/custom_nodes; \
        repo_dir=$(basename "$repo" .git); \
        git clone --recursive "$repo"; \
        [ -f "/ComfyUI/custom_nodes/$repo_dir/requirements.txt" ] && \
            pip install -r "/ComfyUI/custom_nodes/$repo_dir/requirements.txt"; \
      done ; \
   else \
      echo "❌ Comfy установка отключена" ; \
   fi

###############################################################################
# ──────────────────────────────  STAGE 2 : final  ────────────────────────────
###############################################################################
FROM nvidia/cuda:12.9.0-runtime-ubuntu22.04 AS final

ARG INSTALL_WAN=true
ARG INSTALL_COMFY=true

ENV PATH="/opt/venv/bin:$PATH" \
    WAN_MODEL_PATH=/models/wan14B-720p

# Копируем виртуальное окружение и, при наличии, веса + ComfyUI
COPY --from=builder /opt/venv /opt/venv
RUN if [ "$INSTALL_WAN" = "true" ]; then mkdir -p /models/wan14B-720p; fi
COPY --from=builder /models/wan14B-720p /models/wan14B-720p
COPY --from=builder /ComfyUI /ComfyUI

# Приложение и вспомогательные файлы
WORKDIR /app
COPY backend /app
COPY src/start_script.sh /start_script.sh
COPY 4xLSDIR.pth /4xLSDIR.pth
RUN chmod +x /start_script.sh

# Открываем порты: 8000 (API), 8188 (Comfy), 8888 (Jupyter)
EXPOSE 8000 8188 8888

CMD ["/start_script.sh"]
