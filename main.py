"""
FastAPI Server — Flat structure version
Saari files ek hi folder mein hain
"""

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent_executor, CONFIG, ACTIVE, IND

app = FastAPI(
    title="Smart Agent",
    description="Cloud-independent AI agent. Koi license nahi.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

@app.post("/chat")
async def chat(query: Query):
    try:
        result = agent_executor.invoke({"input": query.message})
        return {
            "response": result["output"],
            "industry": ACTIVE,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "running", "industry": ACTIVE}

@app.get("/")
def root():
    return {"message": "Agent chal raha hai!", "docs": "/docs"}
