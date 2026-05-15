from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import process_query, ACTIVE, IND

app = FastAPI(title="Smart Agent", version="2.0.0")

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
    response = process_query(query.message)
    return {"response": response, "industry": ACTIVE, "status": "success"}

@app.get("/health")
def health():
    return {"status": "running", "industry": ACTIVE, "industry_name": IND["name"]}

@app.get("/")
def root():
    return {"message": "Agent chal raha hai!", "docs": "/docs", "industry": ACTIVE}
