# frontend/Dockerfile

# 1. Базовый образ Node.js
FROM node:18-slim AS frontend

WORKDIR /app

# 2. Копируем package.json + package-lock.json и устанавливаем зависимости
COPY frontend/package.json ./frontend/package-lock.json /app/
RUN npm install

# 3. Копируем исходники (React-код и public)
COPY frontend/src /app/src
COPY frontend/public /app/public

# 4. Копируем и делаем исполняемым скрипт запуска
COPY frontend/src/start_script_frontend.sh /start_script.sh
RUN chmod +x /start_script.sh

# 5. Открываем порт
EXPOSE 3000

# 6. Запуск Vite
CMD ["/start_script_frontend.sh"]
