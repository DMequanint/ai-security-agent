from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.route import router  # import from your actual route.py

app = FastAPI(title="AI Security SOC Agent")

# Allow frontend requests from Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the router at /agent
app.include_router(router, prefix="/agent")
