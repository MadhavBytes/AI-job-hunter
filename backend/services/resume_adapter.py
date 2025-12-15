"""
Intelligent Resume Adapter using Ollama LLM
Adapts resume to match specific job requirements and highlights relevant skills
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class JobDescription:
    """Job description structure"""
    title: str
    company: str
    description: str
    required_skills: List[str]
    nice_to_have_skills: List[str]
    experience_level: str
    salary_range: Optional[str] = None

@dataclass
class AdaptedResume:
    """Adapted resume structure"""
    original_resume: str
    adapted_resume: str
    highlighted_skills: List[str]
    matching_skills: List[str]
    missing_skills: List[str]
    relevance_score: float
    adaptation_summary: str

class ResumeAdapter:
    """
    Intelligent resume adapter using Ollama LLM.
    Adapts resumes to match job requirements and optimizes for ATS (Applicant Tracking System)
    """
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = ollama_base_url
        self.model = model
        self.headers = {"Content-Type": "application/json"}
    
    def extract_skills_from_resume(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume using LLM
        """
        prompt = f"""Extract all technical and professional skills from this resume. 
        Return only a comma-separated list of skills.
        
        Resume:
        {resume_text}
        
        Skills (comma-separated):"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()["response"].strip()
                skills = [s.strip() for s in result.split(",")]
                return [s for s in skills if s]  # Filter empty strings
            else:
                logger.error(f"Error extracting skills: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error in extract_skills_from_resume: {e}")
            return []
    
    def match_skills(self, resume_skills: List[str], job_skills: List[str]) -> Dict[str, List[str]]:
        """
        Match resume skills with job requirements
        """
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matching = [skill for skill in job_skills if skill.lower() in resume_skills_lower]
        missing = [skill for skill in job_skills if skill.lower() not in resume_skills_lower]
        
        return {
            "matching": matching,
            "missing": missing,
            "match_percentage": (len(matching) / len(job_skills) * 100) if job_skills else 0
        }
    
    def adapt_resume_for_job(self, resume_text: str, job_description: JobDescription) -> AdaptedResume:
        """
        Main method: Adapt resume to match job requirements
        Highlights relevant experience, reorders content for ATS optimization
        """
        
        # Extract skills from resume
        resume_skills = self.extract_skills_from_resume(resume_text)
        
        # Match skills
        skill_match = self.match_skills(resume_skills, job_description.required_skills)
        
        # Generate adapted resume
        adaptation_prompt = f"""You are an expert resume writer and recruiter. 
        Adapt this resume to match the job requirements while keeping it truthful and authentic.
        
        Focus on:
        1. Reorder experience and skills to highlight relevant ones first
        2. Emphasize achievements that match job requirements
        3. Use keywords from job description for ATS optimization
        4. Maintain professional tone and structure
        5. Highlight matching skills: {', '.join(skill_match['matching'])}
        
        Original Resume:
        {resume_text}
        
        Job Title: {job_description.title}
        Company: {job_description.company}
        Required Skills: {', '.join(job_description.required_skills)}
        Experience Level: {job_description.experience_level}
        
        Job Description:
        {job_description.description}
        
        Adapted Resume:"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": adaptation_prompt,
                    "stream": False,
                    "temperature": 0.4
                },
                timeout=120
            )
            
            if response.status_code == 200:
                adapted_resume = response.json()["response"].strip()
                
                # Calculate relevance score
                relevance_score = (skill_match['match_percentage'] / 100) * 100
                
                adaptation_summary = f"""Resume Adaptation Summary:
                - Total Required Skills: {len(job_description.required_skills)}
                - Matching Skills: {len(skill_match['matching'])}
                - Missing Skills: {len(skill_match['missing'])}
                - Match Percentage: {skill_match['match_percentage']:.1f}%
                - Relevance Score: {relevance_score:.1f}/100
                """
                
                return AdaptedResume(
                    original_resume=resume_text,
                    adapted_resume=adapted_resume,
                    highlighted_skills=skill_match['matching'],
                    matching_skills=skill_match['matching'],
                    missing_skills=skill_match['missing'],
                    relevance_score=relevance_score,
                    adaptation_summary=adaptation_summary
                )
            else:
                logger.error(f"Error adapting resume: {response.status_code}")
                raise Exception(f"Failed to adapt resume: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error in adapt_resume_for_job: {e}")
            raise
    
    def generate_cover_letter(self, resume_text: str, job_description: JobDescription) -> str:
        """
        Generate AI-powered cover letter tailored to job
        """
        
        cover_letter_prompt = f"""Write a professional, compelling cover letter for this job application.
        
        Resume Details:
        {resume_text}
        
        Job Details:
        Title: {job_description.title}
        Company: {job_description.company}
        Description: {job_description.description}
        Required Skills: {', '.join(job_description.required_skills)}
        
        The cover letter should:
        1. Be 3-4 paragraphs
        2. Highlight relevant experience from resume
        3. Show enthusiasm for the role and company
        4. Address key requirements
        5. Include a strong closing
        6. Be professional and concise
        
        Cover Letter:
        
        Dear Hiring Manager,
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": cover_letter_prompt,
                    "stream": False,
                    "temperature": 0.5
                },
                timeout=120
            )
            
            if response.status_code == 200:
                cover_letter = "Dear Hiring Manager,\n" + response.json()["response"].strip()
                return cover_letter
            else:
                logger.error(f"Error generating cover letter: {response.status_code}")
                raise Exception(f"Failed to generate cover letter: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error in generate_cover_letter: {e}")
            raise
    
    def check_ollama_connection(self) -> bool:
        """
        Check if Ollama service is running and accessible
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
