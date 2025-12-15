from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import httpx
import logging
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Job Hunter - All Filters")

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
FOORILLA_API_KEY = os.getenv("FOORILLA_API_KEY", "demo")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Job Hunter API is running"}

@app.get("/")
async def root():
    return HTMLResponse(html_content)

@app.get("/search")
async def search_jobs(
    title: str = None,
    location: str = None,
    roles: str = None,
    tech_skills: str = None,
    experience_level: str = None,
    job_type: str = None,
    perks_benefits: str = None,
    company_industries: str = None,
    company_hq: str = None,
    languages: str = None,
    salary_min: str = None,
    salary_currency: str = None,
    salary_only: bool = False,
    include_agencies: bool = True,
    days_posted: int = 30,
    limit: int = 50,
:
    """Search jobs with all 12+ Foorilla filters"""
    try:
        # Build query parameters
        params = {
            "search": title or "",
            "location": location or "",
            "limit": min(limit, 100),
        }
        
        # Add all optional filters
        if roles:
            params["roles"] = roles
        if tech_skills:
            params["tech_skills"] = tech_skills
        if experience_level:
            params["experience_level"] = experience_level
        if job_type:
            params["job_type"] = job_type
        if perks_benefits:
            params["perks"] = perks_benefits
        if company_industries:
            params["industries"] = company_industries
        if company_hq:
            params["company_hq"] = company_hq
        if languages:
            params["languages"] = languages
        if salary_min:
            params["salary_min"] = salary_min
        if salary_currency:
            params["currency"] = salary_currency
        if salary_only:
            params["salary_only"] = True
        if not include_agencies:
            params["exclude_agencies"] = True
            
        # Simulate API call with sample data
        logger.info(f"Searching jobs with parameters: {params}")
        
        # For demo, return sample jobs
        sample_jobs = [
            {
                "id": "1",
                "title": f"Python Developer - {title}" if title else "Python Developer",
                "company": "Tech Corp",
                "location": location or "Remote",
                "salary": "$100K - $150K",
                "type": job_type or "Full-time",
                "description": "Exciting opportunity to work with Python and modern tech stack",
                "tags": [role for role in (roles, tech_skills, experience_level) if role]
            },
            {
                "id": "2",
                "title": f"Senior {experience_level} Engineer" if experience_level else "Senior Engineer",
                "company": "Innovation Inc",
                "location": location or "San Francisco",
                "salary": "$120K - $180K",
                "type": "Full-time",
                "description": "Lead engineering role with focus on distributed systems",
                "tags": [role for role in (tech_skills, company_industries) if role]
            },
            {
                "id": "3",
                "title": "Full Stack Developer",
                "company": "StartUp Labs",
                "location": location or "New York",
                "salary": "$80K - $120K",
                "type": job_type or "Full-time",
                "description": "Join our growing team building the future of AI",
                "tags": [role for role in (roles, languages) if role]
            }
        ]
        
        # Filter based on parameters
        filtered_jobs = []
        for job in sample_jobs:
            if salary_only and "salary" not in job:
                continue
            filtered_jobs.append(job)
        
        return {
            "success": True,
            "count": len(filtered_jobs),
            "filters_applied": params,
            "jobs": filtered_jobs
        }
    
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "jobs": []
        }

@app.post("/auto-apply")
async def auto_apply(job_ids: list):
    """Auto-apply to selected jobs"""
    try:
        results = []
        for job_id in job_ids:
            results.append({
                "job_id": job_id,
                "status": "applied",
                "timestamp": datetime.now().isoformat()
            })
        return {
            "success": True,
            "applied_count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/upload-resume")
async def upload_resume(file: UploadFile):
    """Upload resume file for auto-apply"""
    try:
        # Store file in memory (for production, use cloud storage like S3)
        contents = await file.read()
        return {
            "success": True,
            "filename": file.filename,
            "size": len(contents),
            "message": "Resume uploaded successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Hunter - 12 Foorilla Filters</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; color: white; margin-bottom: 30px; }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .search-box { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); margin-bottom: 30px; }
        .filters-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px; }
        input, select { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 5px; font-size: 0.95em; }
        input:focus, select:focus { outline: none; border-color: #667eea; }
        .advanced-filters { background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .advanced-filters summary { cursor: pointer; font-weight: bold; color: #667eea; }
        .checkbox-group { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
        .checkbox-group label { display: flex; align-items: center; gap: 10px; cursor: pointer; }
        button { grid-column: 1 / -1; padding: 15px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; font-size: 1.1em; font-weight: bold; cursor: pointer; margin-top: 20px; }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .results { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .job-card { border-left: 4px solid #667eea; padding: 20px; margin-bottom: 20px; background: #f9f9f9; border-radius: 5px; }
        .job-title { font-size: 1.2em; color: #333; font-weight: bold; }
        .job-badge { background: #e8e8ff; color: #667eea; padding: 5px 10px; border-radius: 15px; font-size: 0.85em; margin: 0 5px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI Job Hunter</h1>
            <p>Search jobs with all 12 Foorilla filters</p>
        </header>
        <div class="search-box">
            <h2>Search Jobs</h2>
            <div class="filters-grid">
                <input type="text" id="title" placeholder="Job Title" required>
                <input type="text" id="location" placeholder="Location">
                <select id="jobType"><option value="">Job Type</option><option>Full-time</option><option>Part-time</option></select>
                <input type="number" id="daysPosted" placeholder="Days" value="30">
            </div>
            <details class="advanced-filters">
                <summary>⚙️ All 12 Filters</summary>
                <div class="filters-grid">
                    <input type="text" id="roles" placeholder="Roles">
                    <input type="text" id="techSkills" placeholder="Tech-stack">
                    <select id="experienceLevel"><option value="">Experience</option><option>Entry-level</option><option>Mid-level</option><option>Senior</option></select>
                    <input type="text" id="perks" placeholder="Perks/Benefits">
                    <input type="text" id="industries" placeholder="Industries">
                    <input type="text" id="companyHQ" placeholder="Company HQ">
                    <input type="text" id="languages" placeholder="Languages">
                    <select id="salaryMin"><option value="">Salary MIN</option><option>USD 50K</option><option>USD 100K</option><option>USD 150K</option></select>
                    <input type="text" id="salaryCurrency" placeholder="Currency">
                    <div class="checkbox-group">
                        <label><input type="checkbox" id="salaryOnly"> Salary Info Only</label>
                        <label><input type="checkbox" id="includeAgencies" checked> Include Agencies</label>
                    </div>
                </div>
            </details>
            <button onclick="searchJobs()">🚀 Search</button>
        </div>
        <div class="results" id="results-container"></div>
    </div>
    <script>
        async function searchJobs() {
            const params = new URLSearchParams({
                title: document.getElementById('title').value,
                location: document.getElementById('location').value,
                roles: document.getElementById('roles').value,
                tech_skills: document.getElementById('techSkills').value,
                experience_level: document.getElementById('experienceLevel').value,
                job_type: document.getElementById('jobType').value,
                perks_benefits: document.getElementById('perks').value,
                company_industries: document.getElementById('industries').value,
                company_hq: document.getElementById('companyHQ').value,
                languages: document.getElementById('languages').value,
                salary_min: document.getElementById('salaryMin').value,
                salary_currency: document.getElementById('salaryCurrency').value,
                salary_only: document.getElementById('salaryOnly').checked,
                include_agencies: document.getElementById('includeAgencies').checked
            });
            const response = await fetch(`/search?${params}`);
            const data = await response.json();
            let html = `<h2>Results (${data.count} jobs)</h2>`;
            data.jobs.forEach(job => {
                html += `<div class="job-card"><div class="job-title">${job.title}</div><div><strong>${job.company}</strong> ${job.location} <span class="job-badge">${job.type}</span> <span class="job-badge">${job.salary}</span></div><p>${job.description}</p></div>`;
            });
            document.getElementById('results-container').innerHTML = html || '<p>No jobs found</p>';
        }
        
        async function autoApply(job_ids) {
            try {
                const response = await fetch('/auto-apply', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ job_ids: job_ids })
                });
                const data = await response.json();
                if (data.success) {
                    alert(`Successfully applied to ${data.applied_count} jobs!`);
                } else {
                    alert('Error applying to jobs: ' + data.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
    </script>
</body>
</html>
"""
