import asyncio
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AutoApplier:
    """
    Automated job application service
    Uses Playwright for browser automation
    """
    
    def __init__(self):
        self.application_log = []
        self.success_count = 0
        self.failure_count = 0
    
    def match_skills(self, resume_skills: Dict[str, List[str]], 
                    job_skills: List[str]) -> float:
        """
        Calculate skill match percentage between resume and job
        """
        if not job_skills:
            return 0.0
        
        all_resume_skills = []
        for category_skills in resume_skills.values():
            all_resume_skills.extend(category_skills)
        
        matched_count = 0
        for job_skill in job_skills:
            for resume_skill in all_resume_skills:
                if job_skill.lower() in resume_skill.lower() or \
                   resume_skill.lower() in job_skill.lower():
                    matched_count += 1
                    break
        
        match_percentage = (matched_count / len(job_skills)) * 100
        return min(match_percentage, 100.0)
    
    def filter_jobs(self, jobs: List[Dict], resume_skills: Dict[str, List[str]], 
                   min_match: float = 60.0) -> List[Dict]:
        """
        Filter jobs based on skill matching
        """
        filtered_jobs = []
        
        for job in jobs:
            job_skills = job.get('skills', [])
            match_score = self.match_skills(resume_skills, job_skills)
            
            if match_score >= min_match:
                job['match_score'] = match_score
                filtered_jobs.append(job)
        
        # Sort by match score descending
        filtered_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        return filtered_jobs
    
    async def apply_to_job(self, job: Dict, applicant_info: Dict) -> Dict:
        """
        Simulate applying to a job
        In production, this would use Playwright for actual application
        """
        try:
            application_record = {
                "job_id": job.get('id'),
                "job_title": job.get('title'),
                "company": job.get('company'),
                "applied_at": datetime.now().isoformat(),
                "status": "pending",
                "match_score": job.get('match_score', 0)
            }
            
            self.application_log.append(application_record)
            self.success_count += 1
            
            logger.info(f"Applied to {job.get('title')} at {job.get('company')}")
            return {"success": True, "application": application_record}
        except Exception as e:
            self.failure_count += 1
            logger.error(f"Error applying to job: {e}")
            return {"success": False, "error": str(e)}
    
    async def apply_to_jobs(self, jobs: List[Dict], 
                           applicant_info: Dict) -> List[Dict]:
        """
        Apply to multiple jobs concurrently
        """
        tasks = [self.apply_to_job(job, applicant_info) for job in jobs]
        results = await asyncio.gather(*tasks)
        return results
    
    def get_statistics(self) -> Dict:
        """
        Get application statistics
        """
        return {
            "total_applications": len(self.application_log),
            "successful": self.success_count,
            "failed": self.failure_count,
            "success_rate": (self.success_count / max(1, len(self.application_log))) * 100,
            "recent_applications": self.application_log[-10:]  # Last 10
        }
