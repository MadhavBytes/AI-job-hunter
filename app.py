from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Job Hunter")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Foorilla API configuration
FOORILLA_BASE_URL = "https://jobdataapi.com/api"

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "AI Job Hunter API is running"}

@app.get("/api/jobs/search")
async def search_jobs(
    title: str = None,
    location: str = None,
    job_type: str = None,
    limit: int = 20,
    max_age: int = 30
):
    """
    Search jobs from Foorilla jobdata API
    Using public API (no auth required)
    """
    try:
        params = {
            "limit": min(limit, 100),
            "max_age": max_age
        }
        
        if title:
            params["title"] = title
        if location:
            params["location"] = location
        if job_type:
            params["job_type"] = job_type
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{FOORILLA_BASE_URL}/jobs/",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "total": len(data.get('results', [])),
                    "jobs": data.get('results', []),
                    "filters_applied": {
                        "title": title,
                        "location": location,
                        "job_type": job_type,
                        "max_age_days": max_age
                    }
                }
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch jobs")
    
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jobs/regions")
async def get_regions():
    """Get available job regions from Foorilla"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{FOORILLA_BASE_URL}/jobregions/")
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        logger.error(f"Error fetching regions: {str(e)}")
        return {"error": str(e)}

@app.get("/api/jobs/types")
async def get_job_types():
    """Get available job types from Foorilla"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{FOORILLA_BASE_URL}/jobtypes/")
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        logger.error(f"Error fetching job types: {str(e)}")
        return {"error": str(e)}

@app.get("/api/jobs/countries")
async def get_countries():
    """Get available job countries from Foorilla"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{FOORILLA_BASE_URL}/jobcountries/")
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code)
    except Exception as e:
        logger.error(f"Error fetching countries: {str(e)}")
        return {"error": str(e)}

@app.get("/")
async def root():
    """Serve HTML frontend"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Job Hunter</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            header { text-align: center; color: white; margin-bottom: 40px; }
            header h1 { font-size: 2.5em; margin-bottom: 10px; }
            header p { font-size: 1.1em; opacity: 0.9; }
            .search-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 30px; }
            .search-box h2 { margin-bottom: 20px; color: #333; }
            .search-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 15px; }
            input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 1em; }
            button { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; font-weight: bold; margin-top: 10px; }
            button:hover { background: #764ba2; }
            .jobs-container { background: white; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); padding: 30px; }
            .job-card { border: 1px solid #eee; padding: 20px; margin-bottom: 15px; border-radius: 5px; cursor: pointer; transition: all 0.3s; }
            .job-card:hover { box-shadow: 0 5px 15px rgba(0,0,0,0.1); transform: translateY(-2px); }
            .job-title { font-size: 1.3em; font-weight: bold; color: #333; margin-bottom: 10px; }
            .job-company { color: #667eea; font-weight: bold; margin-bottom: 8px; }
            .job-location { color: #666; margin-bottom: 8px; }
            .job-type { display: inline-block; background: #f0f0f0; padding: 5px 10px; border-radius: 3px; font-size: 0.9em; margin-right: 10px; }
            .loading { text-align: center; padding: 20px; color: #667eea; font-weight: bold; }
            .error { background: #fee; color: #c00; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .success { background: #efe; color: #0a0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🤖 AI Job Hunter</h1>
                <p>Search and apply to jobs automatically using Foorilla Job Data API</p>
            </header>
            
            <div class="search-box">
                <h2>Search Jobs</h2>
                <div class="search-grid">
                    <input type="text" id="jobTitle" placeholder="Job Title (e.g., Python Developer)">
                    <input type="text" id="jobLocation" placeholder="Location (e.g., United States)">
                    <select id="jobType">
                        <option value="">Job Type (All)</option>
                        <option value="Full-time">Full-time</option>
                        <option value="Part-time">Part-time</option>
                        <option value="Contract">Contract</option>
                        <option value="Internship">Internship</option>
                    </select>
                    <input type="number" id="maxAge" placeholder="Days Posted (e.g., 30)" value="30" min="1" max="365">
                </div>
                <button onclick="searchJobs()">Search Jobs</button>
            </div>
            
            <div id="messageContainer"></div>
            
            <div class="jobs-container">
                <h2 style="margin-bottom: 20px; color: #333;">Job Results</h2>
                <div id="jobsContainer"></div>
            </div>
        </div>
        
        <script>
        async function searchJobs() {
            const title = document.getElementById('jobTitle').value;
            const location = document.getElementById('jobLocation').value;
            const jobType = document.getElementById('jobType').value;
            const maxAge = document.getElementById('maxAge').value;
            
            const messageContainer = document.getElementById('messageContainer');
            messageContainer.innerHTML = '<div class="loading">Searching jobs...</div>';
            
            try {
                const params = new URLSearchParams();
                if(title) params.append('title', title);
                if(location) params.append('location', location);
                if(jobType) params.append('job_type', jobType);
                params.append('limit', '50');
                params.append('max_age', maxAge);
                
                const response = await fetch(`/api/jobs/search?${params}`);
                const data = await response.json();
                
                if(data.success && data.jobs.length > 0) {
                    messageContainer.innerHTML = `<div class="success">Found ${data.total} jobs matching your criteria!</div>`;
                    displayJobs(data.jobs);
                } else {
                    messageContainer.innerHTML = '<div class="error">No jobs found. Try different search terms.</div>';
                    document.getElementById('jobsContainer').innerHTML = '';
                }
            } catch(error) {
                messageContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                console.error('Error:', error);
            }
        }
        
        function displayJobs(jobs) {
            const container = document.getElementById('jobsContainer');
            container.innerHTML = jobs.map(job => `
                <div class="job-card">
                    <div class="job-title">${job.title || 'Job Title'}</div>
                    <div class="job-company">${job.company || 'Company Name'}</div>
                    <div class="job-location">📍 ${job.location || 'Location Not Specified'}</div>
                    ${job.job_type ? `<span class="job-type">${job.job_type}</span>` : ''}
                    ${job.salary_min ? `<div style="color: #667eea; margin-top: 10px; font-weight: bold;">💰 Salary: $${job.salary_min} - $${job.salary_max || 'Negotiable'}</div>` : ''}
                    ${job.description ? `<div style="margin-top: 15px; color: #666; font-size: 0.95em;">${job.description.substring(0, 200)}...</div>` : ''}
                    <button onclick="applyJob('${job.id}')" style="margin-top: 15px; background: #667eea;">View & Apply</button>
                </div>
            `).join('');
        }
        
        function applyJob(jobId) {
            alert(`Job ID: ${jobId}\n\nAuto-apply feature coming soon!\nIntegrating with Foorilla application system...`);
        }
        
        // Load jobs on page load
        window.onload = function() {
            searchJobs();
        };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
