from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import modules
from .config import settings
from .api.routes import job_routes, resume_routes, application_routes
from .services.scheduler import setup_scheduler

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Startup and Shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("\U0001f680 Starting AI Job Hunter...")
    setup_scheduler()
    yield
    logger.info("\U0001f3cb Application shutting down...")

app = FastAPI(
    title="AI Job Hunter API",
    description="Automated job application hunting with AI resume adaptation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(job_routes.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(resume_routes.router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(application_routes.router, prefix="/api/applications", tags=["Applications"])

@app.get("/")
async def root():
    return {
        "message": "AI Job Hunter API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
