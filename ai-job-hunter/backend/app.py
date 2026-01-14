from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
import re
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

class Job(BaseModel):
    id: str
    title: str
    company: str = 'Company'
    location: str = 'Location'
    salary: str = 'Salary'
    experience_level: str = 'Level'
    job_type: str = 'Full-time'
    skills: List[str] = []
    remote_type: str = 'Unknown'
    industries: List[str] = []
    description: str = ''

class ResumeData(BaseModel):
    skills: List[str] = []
    experience_level: str = ''

class FilterRequest(BaseModel):
    remote_only: bool = False
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    skills: List[str] = []
        topics: List[str] = []
    regions: List[str] = []
    industries: List[str] = []
    salary_min: Optional[int] = None
    salary_currency: Optional[str] = 'USD'
    languages: List[str] = []
    remote_first: bool = False
    has_salary_info: bool = False

async def scrape_foorilla():
    """Scrape jobs from Foorilla.com with detailed parsing."""
    try:
        url = 'https://foorilla.com/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=headers, follow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs: List[Job] = []
            
            # Find all job links - they appear as list items with job titles
            # Looking for links that contain job postings
            job_links = soup.find_all('a', href=True)
            
            for idx, link in enumerate(job_links):
                title_text = link.get_text(strip=True)
                
                # Filter out navigation links and very short/long text
                if len(title_text) < 5 or len(title_text) > 300:
                    continue
                
                # Skip common navigation text
                skip_keywords = ['Topics', 'Regions', 'Filters', 'Settings', 'All', 'Latest',
                               'Followed', 'Saved', 'Companies', 'Following', 'Viewed', 'Applied',
                               'Hiring', 'Media', 'Account', 'foo🦍', 'Changelog', 'About', 'Terms', 
                               'Privacy', 'CSV', 'JSON', 'Top', 'foorilla', 'Billing']
                
                if any(keyword.lower() in title_text.lower() for keyword in skip_keywords):
                    continue
                
                # Extract job information
                # Try to find company code [XX] and job type
                company_match = re.search(r'\[(\w{2})\]', title_text)
                company = company_match.group(1) if company_match else 'Company'
                
                # Look for job type indicators
                job_type = 'Full-time'
                if 'Part Time' in title_text or 'Part-time' in title_text:
                    job_type = 'Part-time'
                elif 'Internship' in title_text or 'internship' in title_text:
                    job_type = 'Internship'
                elif 'Contract' in title_text:
                    job_type = 'Contract'
                elif 'Temporary' in title_text:
                    job_type = 'Temporary'
                
                # Extract experience level from common patterns
                experience_level = 'Mid-level'
                if 'Senior' in title_text:
                    experience_level = 'Senior'
                elif 'Lead' in title_text or 'Manager' in title_text or 'Director' in title_text or 'Executive' in title_text:
                    experience_level = 'Executive'
                elif 'Junior' in title_text or 'Intern' in title_text or 'Student' in title_text:
                    experience_level = 'Junior'
                
                # Check for remote option
                remote_type = 'On-site'
                if '[R]' in title_text or 'remote' in title_text.lower():
                    remote_type = 'Remote'
                elif 'hybrid' in title_text.lower():
                    remote_type = 'Hybrid'
                
                # Extract location if possible (usually at the end)
                location = 'Various'
                # Jobs typically have location info, try to extract it
                location_patterns = re.findall(r'([A-Z][a-z]+(?:,\s*[A-Z][a-z]+)?(?:,\s*[A-Z]{2})?)', title_text)
                if location_patterns:
                    location = location_patterns[-1]  # Take the last match as location
                
                # Create job object
                job = Job(
                    id=str(len(jobs) + 1),
                    title=title_text,
                    company=company,
                    location=location,
                    salary='Negotiable',
                    experience_level=experience_level,
                    job_type=job_type,
                    remote_type=remote_type,
                    skills=[],
                    industries=[]
                )
                jobs.append(job)
                
                # Stop at 30 jobs for now
                if len(jobs) >= 30:
                    break
            
            print(f'Scraped {len(jobs)} jobs from Foorilla')
            return jobs
    except Exception as e:
        print(f'Error scraping Foorilla: {e}')
        import traceback
        traceback.print_exc()
        return []
@app.get('/')
async def root():
    return {'status': 'API Running'}

@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get('/api/jobs')
async def get_jobs():
    jobs = await scrape_foorilla()
    return {'jobs': jobs}

@app.post('/api/jobs/filter')
async def filter_jobs(filters: FilterRequest):
    jobs = await scrape_foorilla()
    result = jobs
    if filters.remote_only:
        result = [j for j in result if 'remote' in j.remote_type.lower()]
    if filters.experience_level:
        result = [j for j in result if filters.experience_level.lower() in j.experience_level.lower()]
    if filters.job_type:
        result = [j for j in result if filters.job_type.lower() in j.job_type.lower()]
    if filters.skills:
        result = [j for j in result if any(s.lower() in [jsk.lower() for jsk in j.skills] for s in filters.skills)]
            if filters.remote_first:
        result = [j for j in result if j.remote_type == 'Remote']
    if filters.regions:
        result = [j for j in result if any(region.lower() in j.location.lower() for region in filters.regions)]
    if filters.industries:
        result = [j for j in result if any(ind.lower() in ' '.join(j.industries).lower() for ind in filters.industries)]
    if filters.topics:
        result = [j for j in result if any(topic.lower() in j.title.lower() for topic in filters.topics)]
    if filters.languages:
        result = [j for j in result if any(lang.lower() in j.title.lower() for lang in filters.languages)]
    if filters.salary_min:
        result = [j for j in result if j.salary != 'Negotiable']  # In production, parse salary properly
    if filters.has_salary_info:
        result = [j for j in result if j.salary != 'Negotiable' and j.salary != '']
    return {'jobs': result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=)