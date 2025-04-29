from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import os
from typing import List, Optional

app = FastAPI(title="Jetson Embedding API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://apps.medicpro.london"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model paths (unchanged, still in jetson-containers)
MODEL_PATHS = {
    "all-MiniLM-L6-v2": "/home/mx/jetson-containers/data/models/torch/sentence_transformers/sentence-transformers_all-MiniLM-L6-v2",
    "all-mpnet-base-v2": "/home/mx/jetson-containers/data/models/torch/sentence_transformers/sentence-transformers_all-mpnet-base-v2"
}

# Load models
models = {}
for model_name, model_path in MODEL_PATHS.items():
    try:
        models[model_name] = SentenceTransformer(model_path)
    except Exception as e:
        print(f"Error loading model {model_name}: {str(e)}")

class EmbeddingRequest(BaseModel):
    text: str
    model_name: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    model_name: str

@app.get("/models")
async def list_models():
    """List available models"""
    return {"models": list(models.keys())}

@app.post("/embed", response_model=EmbeddingResponse)
async def create_embedding(request: EmbeddingRequest):
    """Generate embeddings for the input text using the specified model"""
    if request.model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {request.model_name} not found")
    
    try:
        embedding = models[request.model_name].encode(request.text)
        return EmbeddingResponse(
            embedding=embedding.tolist(),
            model_name=request.model_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 