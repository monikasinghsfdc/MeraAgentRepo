"""
FastAPI Server — Yeh file kabhi nahi badalti!
Sab kuch config se aata hai.
"""

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent_executor, CONFIG, ACTIVE, IND

with open("configs/master_config.json") as f:
    CFG = json.load(f)

app = FastAPI(
    title=f"Smart Agent — {IND['name']}",
    description="Config-driven agent. Koi file nahi badalti.",
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
            "industry_name": IND["name"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
def get_config():
    """Current active config dekho"""
    return {
        "active_industry": ACTIVE,
        "industry_name": IND["name"],
        "tools_loaded": IND["tools"],
        "llm": CFG["llm"]["provider"],
        "model": CFG["llm"]["model"]
    }

@app.get("/industries")
def list_industries():
    """Saari available industries"""
    return {
        "industries": list(CFG["industries"].keys()),
        "active": ACTIVE,
        "switch_hint": "master_config.json mein 'active_industry' badlo"
    }

@app.get("/health")
def health():
    return {"status": "running", "active": ACTIVE}
