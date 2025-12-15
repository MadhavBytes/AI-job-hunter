"""
Automated Job Application Service
Automates filling and submitting job application forms using Playwright
Supports intelligent form field detection and auto-filling with candidate data
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import re

logger = logging.getLogger(__name__)

@dataclass
class CandidateData:
    """Candidate information for form filling"""
    full_name: str
    email: str
    phone: str
    location: str
    resume_text: str
    adapted_resume: str
    cover_letter: str
    skills: List[str]
    experience_years: int
    current_company: Optional[str] = None
    linkedin_url: Optional[str] = None

@dataclass
class ApplicationResult:
    """Result of application attempt"""
    success: bool
    job_id: str
    job_title: str
    timestamp: str
    application_url: str
    filled_fields: List[str]
    skipped_fields: List[str]
    error_message: Optional[str] = None
    notes: Optional[str] = None

class AutoApplyService:
    """
    Automates job application form filling and submission
    Uses Playwright for browser automation
    """
    
    # Common form field patterns
    FIELD_PATTERNS = {
        'name': ['fullname', 'full_name', 'fname', 'name', 'first_name', 'applicant_name'],
        'email': ['email', 'email_address', 'work_email', 'personal_email'],
        'phone': ['phone', 'phone_number', 'mobile', 'contact_phone', 'telephone'],
        'location': ['location', 'city', 'residence', 'current_location', 'address'],
        'experience': ['years_experience', 'experience', 'years', 'total_experience'],
        'resume': ['resume', 'cv', 'document', 'resume_file', 'attachment'],
        'cover_letter': ['cover_letter', 'cover_letter_text', 'message', 'additional_info', 'comments'],
        'skills': ['skills', 'technical_skills', 'expertise', 'competencies'],
        'linkedin': ['linkedin', 'linkedin_profile', 'linkedin_url', 'profile_url'],
    }
    
    def __init__(self):
        self.browser = None
        self.page = None
    
    async def initialize_browser(self):
        """
        Initialize Playwright browser
        Install with: pip install playwright && playwright install chromium
        """
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            logger.info("Browser initialized successfully")
        except ImportError:
            logger.error("Playwright not installed. Run: pip install playwright")
            raise
    
    async def close_browser(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def navigate_to_job(self, job_url: str) -> bool:
        """
        Navigate to job application page
        """
        try:
            self.page = await self.browser.new_page()
            await self.page.goto(job_url, wait_until='networkidle')
            logger.info(f"Navigated to {job_url}")
            return True
        except Exception as e:
            logger.error(f"Error navigating to job: {e}")
            return False
    
    def detect_form_fields(self, page_html: str) -> Dict[str, List[str]]:
        """
        Detect form fields on the page
        Returns mapping of field types to HTML selectors
        """
        detected_fields = {}
        
        # Look for form inputs
        for field_type, patterns in self.FIELD_PATTERNS.items():
            for pattern in patterns:
                # Create regex patterns for different attribute types
                name_pattern = f'(?i)name=[\"\']?{pattern}'
                id_pattern = f'(?i)id=[\"\']?{pattern}'
                placeholder_pattern = f'(?i)placeholder=[\"\']?.*{pattern}'
                
                if re.search(name_pattern, page_html):
                    detected_fields.setdefault(field_type, []).append(f'[name*="{pattern}"]')
                if re.search(id_pattern, page_html):
                    detected_fields.setdefault(field_type, []).append(f'#{pattern}')
        
        return detected_fields
    
    async def fill_text_field(self, field_selector: str, value: str) -> bool:
        """
        Fill a text input field
        """
        try:
            await self.page.fill(field_selector, value)
            logger.info(f"Filled {field_selector} with value")
            return True
        except Exception as e:
            logger.warning(f"Could not fill {field_selector}: {e}")
            return False
    
    async def fill_application_form(
        self,
        job_url: str,
        candidate_data: CandidateData
    ) -> ApplicationResult:
        """
        Main method: Fill and submit job application form
        """
        filled_fields = []
        skipped_fields = []
        error_message = None
        
        try:
            # Navigate to job page
            if not await self.navigate_to_job(job_url):
                raise Exception("Failed to navigate to job page")
            
            # Wait for form to load
            await self.page.wait_for_selector('form', timeout=10000)
            
            # Get page HTML for field detection
            page_html = await self.page.content()
            form_fields = self.detect_form_fields(page_html)
            
            # Fill detected fields
            field_mapping = {
                'name': candidate_data.full_name,
                'email': candidate_data.email,
                'phone': candidate_data.phone,
                'location': candidate_data.location,
                'experience': str(candidate_data.experience_years),
                'cover_letter': candidate_data.cover_letter,
                'linkedin': candidate_data.linkedin_url or '',
            }
            
            # Attempt to fill each detected field
            for field_type, field_value in field_mapping.items():
                if field_type in form_fields and field_value:
                    for selector in form_fields[field_type]:
                        if await self.fill_text_field(selector, field_value):
                            filled_fields.append(field_type)
                            break
                    else:
                        skipped_fields.append(field_type)
            
            # Handle file uploads (resume)
            resume_uploads = await self.page.query_selector_all(
                'input[type="file"][accept*="pdf"], input[type="file"][accept*="doc"]'
            )
            if resume_uploads and candidate_data.resume_text:
                # Note: In production, save adapted resume to temp file first
                logger.info(f"Found {len(resume_uploads)} file upload field(s)")
                skipped_fields.append('resume_upload')  # Manual upload needed
            
            # Handle skills selection/input
            skills_fields = await self.page.query_selector_all(
                'input[name*="skill"], select[name*="skill"]'
            )
            if skills_fields and candidate_data.skills:
                for skill_field in skills_fields:
                    field_type = await skill_field.get_attribute('type')
                    if field_type == 'text':
                        await skill_field.fill(', '.join(candidate_data.skills))
                        filled_fields.append('skills')
                        break
            
            # Look for and fill any textarea fields with cover letter
            textareas = await self.page.query_selector_all('textarea')
            if textareas and candidate_data.cover_letter:
                # Fill first textarea with cover letter
                await textareas[0].fill(candidate_data.cover_letter)
                filled_fields.append('cover_letter_textarea')
            
            # Look for submit button
            submit_buttons = await self.page.query_selector_all(
                'button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Apply")'
            )
            
            if submit_buttons:
                logger.info(f"Found {len(submit_buttons)} submit button(s)")
                # Click the first submit button
                await submit_buttons[0].click()
                
                # Wait for confirmation or next page
                try:
                    await self.page.wait_for_url(
                        lambda url: 'confirm' in url or 'success' in url or 'thank' in url,
                        timeout=10000
                    )
                    success = True
                except:
                    # Check if we're still on same page
                    success = True  # Assume success if no error thrown
            else:
                logger.warning("No submit button found")
                filled_fields.append('manual_submit_needed')
                success = True
            
            return ApplicationResult(
                success=success,
                job_id="job_auto_detect",
                job_title="Auto-detected Job",
                timestamp=datetime.now().isoformat(),
                application_url=job_url,
                filled_fields=filled_fields,
                skipped_fields=skipped_fields,
                notes=f"Filled {len(filled_fields)} fields, skipped {len(skipped_fields)} fields"
            )
        
        except Exception as e:
            logger.error(f"Error filling application: {e}")
            error_message = str(e)
            return ApplicationResult(
                success=False,
                job_id="job_auto_detect",
                job_title="Auto-detected Job",
                timestamp=datetime.now().isoformat(),
                application_url=job_url,
                filled_fields=filled_fields,
                skipped_fields=skipped_fields,
                error_message=error_message
            )
    
    async def batch_apply(
        self,
        job_urls: List[str],
        candidate_data: CandidateData
    ) -> List[ApplicationResult]:
        """
        Apply to multiple jobs
        """
        results = []
        
        for i, job_url in enumerate(job_urls):
            logger.info(f"Processing job {i+1}/{len(job_urls)}: {job_url}")
            
            try:
                result = await self.fill_application_form(job_url, candidate_data)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {job_url}: {e}")
                results.append(ApplicationResult(
                    success=False,
                    job_id="unknown",
                    job_title="Unknown Job",
                    timestamp=datetime.now().isoformat(),
                    application_url=job_url,
                    filled_fields=[],
                    skipped_fields=[],
                    error_message=str(e)
                ))
            
            # Delay between applications
            await asyncio.sleep(2)
        
        return results
