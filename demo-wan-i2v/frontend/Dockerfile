# ---- Шаг 1. Базовый образ и рабочая директория ----
FROM node:18-slim
WORKDIR /app

# ---- Шаг 2. Копируем package.json и package-lock.json, чтобы закешировать установку зависимостей ----
COPY package.json package-lock.json ./

# Выполняем npm ci, но не запускаем скрипты (npm ci --ignore-scripts)
# node_modules будет закомпоновано в образ, но потом volume-та привязка их перезапишет и npm install заново установит
RUN npm ci --ignore-scripts

# ---- Шаг 3. Копируем только скрипт запуска (он лежит в корне frontend/) ----
COPY start_script_frontend.sh ./start_script_frontend.sh
RUN chmod +x ./start_script_frontend.sh

# ---- Шаг 4. Открываем порт, на котором будет слушать Vite ----
EXPOSE 3000

# ---- Шаг 5. По умолчанию контейнер при старте выполняет наш скрипт ----
ENTRYPOINT ["./start_script_frontend.sh"]
