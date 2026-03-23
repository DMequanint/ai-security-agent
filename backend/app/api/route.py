from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.agent.orchestrator import run_agent
from app.schemas.models import SecurityEvent
import json
import httpx

router = APIRouter()

@router.post("/")
async def agent(event: SecurityEvent):
    """
    Returns structured ThreatAssessment JSON and streams explanation
    """
    assessment = await run_agent(event)

    async def generator():
        # Structured JSON first
        yield json.dumps(assessment.model_dump()) + "\n\n"

        # Prompt for local LLM (Ollama)
        prompt = f"""
You are a cybersecurity analyst.

Event: {event.event}
Logs: {event.logs}
Assessment: {assessment.model_dump()}

Explain:
- What the threat is
- Why it is dangerous
- What actions should be taken
"""

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": True},
            ) as response:

                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
                        except Exception:
                            continue

    return StreamingResponse(generator(), media_type="text/plain")
