// frontend/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // важно, чтобы Vite слушал все интерфейсы контейнера
    port: 3000,
  },
});
