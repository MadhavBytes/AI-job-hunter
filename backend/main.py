from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Query
from fastapi.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime

# Import services
from .services.resume_parser import ResumeParser
from .services.auto_applier import AutoApplier
from .services.foorilla_service import FoorillaService

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class ResumeUploadResponse(BaseModel):
    success: bool
    message: str
    skills: dict
    email: str
    phone: str

class JobFilterRequest(BaseModel):
    resume_skills: dict
    min_match: float = 60.0
    job_title: Optional[str] = None
    location: Optional[str] = None

class JobFilterResponse(BaseModel):
    jobs: List[dict]
    total_count: int
    matched_count: int

class ApplicationResponse(BaseModel):
    success: bool
    total_applications: int
    successful: int
    failed: int
    success_rate: float

# Global instances
resume_parser = ResumeParser()
auto_applier = AutoApplier()
foorilla_service = FoorillaService()

# Startup and Shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting AI Job Hunter Backend...")
    yield
    logger.info("👋 Application shutting down...")

app = FastAPI(
    title="AI Job Hunter API",
    description="Automated job application hunting with AI resume adaptation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Resume endpoints
@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_name = file.filename or "resume"
        
        parsed_data = resume_parser.parse_resume(contents, file_name)
        
        return ResumeUploadResponse(
            success=True,
            message="Resume uploaded and parsed successfully",
            skills=parsed_data.get("skills", {}),
            email=parsed_data.get("email", ""),
            phone=parsed_data.get("phone", "")
        )
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Job search and filtering
@app.get("/api/search-jobs")
async def search_jobs(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None
):
    try:
        jobs = await foorilla_service.search_jobs(
            keyword=keyword,
            location=location,
            job_type=job_type
        )
        return {
            "success": True,
            "total_jobs": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/filter-jobs")
async def filter_jobs(request: JobFilterRequest):
    try:
        # First search for jobs
        jobs = await foorilla_service.search_jobs()
        
        # Filter jobs based on skills
        filtered_jobs = auto_applier.filter_jobs(
            jobs,
            request.resume_skills,
            request.min_match
        )
        
        return JobFilterResponse(
            jobs=filtered_jobs,
            total_count=len(jobs),
            matched_count=len(filtered_jobs)
        )
    except Exception as e:
        logger.error(f"Error filtering jobs: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Auto-apply endpoints
@app.post("/api/auto-apply")
async def auto_apply(
    jobs: List[dict],
    applicant_email: str,
    background_tasks: BackgroundTasks
):
    try:
        applicant_info = {"email": applicant_email}
        
        # Run applications in background
        background_tasks.add_task(
            asyncio.run,
            auto_applier.apply_to_jobs(jobs, applicant_info)
        )
        
        return ApplicationResponse(
            success=True,
            total_applications=len(jobs),
            successful=0,
            failed=0,
            success_rate=0.0
        )
    except Exception as e:
        logger.error(f"Error in auto-apply: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/applications-status")
async def get_applications_status():
    try:
        stats = auto_applier.get_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Error getting application status: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
