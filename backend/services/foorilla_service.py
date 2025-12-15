import aiohttp
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from ..config import settings

logger = logging.getLogger(__name__)

class FoorillaService:
    """Service for interacting with Foorilla Job Data API"""
    
    def __init__(self):
        self.base_url = settings.FOORILLA_BASE_URL
        self.api_key = settings.FOORILLA_API_KEY
        self.timeout = settings.FOORILLA_TIMEOUT
        self.headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def search_jobs(self, 
                        title: Optional[str] = None,
                        location: Optional[str] = None,
                        job_type: Optional[str] = None,
                        max_age_days: int = 30,
                        limit: int = 50) -> Dict[str, Any]:
        """Search for jobs using Foorilla API"""
        try:
            params = {
                "max_age": max_age_days,
                "limit": limit
            }
            
            if title:
                params["title"] = title
            if location:
                params["location"] = location
            if job_type:
                params["job_type"] = job_type
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/jobs",
                    params=params,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Found {len(data.get('results', []))} jobs")
                        return data
                    else:
                        logger.error(f"API Error: {response.status}")
                        return {"error": "Failed to fetch jobs", "status": response.status}
        except Exception as e:
            logger.error(f"Exception in search_jobs: {str(e)}")
            return {"error": str(e)}
    
    async def get_job_details(self, job_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific job"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/jobs/{job_id}",
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": "Job not found"}
        except Exception as e:
            logger.error(f"Exception in get_job_details: {str(e)}")
            return {"error": str(e)}
    
    async def get_job_regions(self) -> List[Dict[str, Any]]:
        """Get available job regions/countries"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/jobregions",
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('results', [])
                    else:
                        return []
        except Exception as e:
            logger.error(f"Exception in get_job_regions: {str(e)}")
            return []
    
    async def get_job_types(self) -> List[Dict[str, Any]]:
        """Get available job types (full-time, part-time, etc)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/jobtypes",
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('results', [])
                    else:
                        return []
        except Exception as e:
            logger.error(f"Exception in get_job_types: {str(e)}")
            return []

# Create singleton instance
foorilla_service = FoorillaService()
