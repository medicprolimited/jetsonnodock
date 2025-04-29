# Jetson Embedding API

A web application for generating text embeddings using sentence transformer models hosted on a Jetson Orin Nano.

## Architecture

### Backend (Jetson Orin Nano)
- FastAPI application running on port 8002
- Two sentence transformer models:
  - all-MiniLM-L6-v2 (faster, smaller)
  - all-mpnet-base-v2 (more accurate, larger)
- Exposed via ngrok for internet access

### Frontend (Vercel)
- React-based web application
- Deployed at https://apps.medicpro.london/web-app1
- Connects to Jetson API via ngrok URL

## Directory Structure
```
/home/mx/jetsonnodock/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── jetson-embedding.service
├── frontend/
│   ├── src/
│   │   └── App.js
│   └── package.json
├── fastapi-env/
│   └── bin/
└── README.md

# Models are stored in:
/home/mx/jetson-containers/data/models/torch/sentence_transformers/
├── sentence-transformers_all-MiniLM-L6-v2
└── sentence-transformers_all-mpnet-base-v2
```

## Setup Instructions

### Backend Setup (Jetson)

1. Create and activate Python virtual environment:
```bash
python -m venv /home/mx/jetsonnodock/fastapi-env
source /home/mx/jetsonnodock/fastapi-env/bin/activate
```

2. Install dependencies:
```bash
cd /home/mx/jetsonnodock/backend
pip install -r requirements.txt
```

3. Set up systemd service:
```bash
sudo cp /home/mx/jetsonnodock/backend/jetson-embedding.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jetson-embedding
sudo systemctl start jetson-embedding
```

4. Set up ngrok:
```bash
ngrok http 8002
```

### Frontend Setup

1. Install dependencies:
```bash
cd /home/mx/jetsonnodock/frontend
npm install
```

2. Create `.env` file:
```
REACT_APP_API_URL=https://your-ngrok-url.ngrok.io
```

3. Start development server:
```bash
npm start
```

4. Build for production:
```bash
npm run build
```

## Deployment

### Backend
- The backend runs as a systemd service on the Jetson
- Update the ngrok URL in the frontend when it changes

### Frontend
- Push to GitHub for automatic deployment to Vercel
- Update the `REACT_APP_API_URL` environment variable in Vercel when the ngrok URL changes

## API Endpoints

- `GET /models`: List available models
- `POST /embed`: Generate embeddings
  - Request body: `{ "text": "string", "model_name": "string" }`
  - Response: `{ "embedding": number[], "model_name": "string" }`

## Security Notes

- CORS is configured to only allow requests from https://apps.medicpro.london
- The Jetson is configured to run in high-performance mode
- API is exposed via ngrok with authentication 