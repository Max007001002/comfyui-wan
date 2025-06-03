# WAN I2V Demo

A demo application for image-to-video generation using FastAPI, React, and Celery.

## Project Structure

```
demo-wan-i2v/
├─ backend/          # FastAPI backend
├─ frontend/         # React frontend
└─ infra/           # Infrastructure configuration
```

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

## Getting Started

1. Clone the repository
2. Copy the environment file:
   ```bash
   cp infra/.env.example infra/.env
   ```
3. Start the services:
   ```bash
   cd infra
   docker-compose up -d
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Features

- User authentication
- Image upload
- Video generation
- Real-time progress updates
- Video download

## License

MIT 