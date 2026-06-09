from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.orchestrator import run_full_analysis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OpsGuardian AI",
    description="Multi-Agent Operational Readiness Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "project": "OpsGuardian AI",
        "message": "Multi-Agent Operational Readiness API is online"
    }


@app.post("/analysis/run")
def run_analysis(payload: dict):
    return run_full_analysis(payload)