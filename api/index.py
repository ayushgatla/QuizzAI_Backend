from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from pydantic import BaseModel
import os
import json
import re
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from utils.crew import agent_maneger
from utils.pdf_parser import extract_text
from utils.sessions import session_manager

app = FastAPI(
    title=Config.APP_NAME,
    description="AI-powered question generation from PDFs",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

def parse_agent_response(result: str):
    if isinstance(result, (dict, list)):
        return result
    if not isinstance(result, str):
        raise ValueError("Agent response is not a string")

    try:
        return json.loads(result)
    except Exception:
        m = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', result)
        if m:
            candidate = m.group(1)
            try:
                return json.loads(candidate)
            except Exception:
                candidate2 = candidate.replace("'", '"')
                return json.loads(candidate2)
        raise ValueError("Could not parse agent response as JSON")

@app.get("/")
def read_root():
    return {"message": "QuizzAI Backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Import remaining routes from main.py
from main import *

# Export the app for Vercel
