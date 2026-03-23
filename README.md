# AI-Powered SOC Security Agent

A fullstack AI security monitoring system that simulates a Security Operations Center (SOC) dashboard with real-time threat analysis.

## Features

- Real-time security event ingestion
- AI-powered threat classification & risk scoring
- Structured analysis using Pydantic models
- Streaming responses via local LLM (Ollama)
- Interactive SOC dashboard (Next.js)

## Tech Stack

- Frontend: Next.js (React, TypeScript)
- Backend: FastAPI (Python, async)
- AI Layer: Pydantic-based agent + local LLM (Ollama)
- Streaming: HTTP streaming (chunked responses)

## Architecture
Next.js Dashboard  
↓  
FastAPI Agent API  
↓  
Pydantic Reasoning Engine  
↓  
Local LLM (Ollama)

## Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reloade

### Frontend
cd frontend
npm install
npm run dev

## Run Ollama
ollama serve 

## Use Case
Simulates real-world SOC workflows:

Detect suspicious activity
Score risk levels
Provide actionable recommendations

