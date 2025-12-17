import re
from typing import List, Dict
from io import BytesIO
import PyPDF2
from docx import Document

class ResumeParser:
    """
    Parse resume files and extract key information
    """
    
    TECH_KEYWORDS = {
        'programming': ['python', 'java', 'c++', 'javascript', 'typescript', 'go', 'rust', 'csharp', 'php', 'ruby'],
        'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring', 'rails', 'asp.net'],
        'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'elasticsearch'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'heroku', 'firebase'],
        'tools': ['git', 'jenkins', 'gitlab', 'github', 'jira', 'figma', 'notion'],
        'other': ['machine learning', 'ai', 'blockchain', 'api', 'rest', 'graphql', 'microservices']
    }
    
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """
        Extract text from PDF file
        """
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """
        Extract text from DOCX file
        """
        try:
            doc = Document(BytesIO(file_bytes))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    @staticmethod
    def extract_skills(text: str) -> Dict[str, List[str]]:
        """
        Extract technical skills from resume text
        """
        text_lower = text.lower()
        found_skills = {}
        
        for category, keywords in ResumeParser.TECH_KEYWORDS.items():
            found_skills[category] = []
            for keyword in keywords:
                if keyword in text_lower:
                    found_skills[category].append(keyword)
        
        return {k: v for k, v in found_skills.items() if v}
    
    @staticmethod
    def extract_email(text: str) -> str:
        """
        Extract email from resume
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    @staticmethod
    def extract_phone(text: str) -> str:
        """
        Extract phone number from resume
        """
        phone_pattern = r'\b(?:\+?1[-.]?)?(?:\(?\d{3}\)?[-.]?)?\d{3}[-.]?\d{4}\b'
        matches = re.findall(phone_pattern, text)
        return matches[0] if matches else ""
    
    @classmethod
    def parse_resume(cls, file_bytes: bytes, file_name: str) -> Dict:
        """
        Parse resume file and extract all information
        """
        # Determine file type and extract text
        if file_name.lower().endswith('.pdf'):
            text = cls.extract_text_from_pdf(file_bytes)
        elif file_name.lower().endswith('.docx'):
            text = cls.extract_text_from_docx(file_bytes)
        else:
            return {"error": "Unsupported file format"}
        
        # Extract information
        return {
            "skills": cls.extract_skills(text),
            "email": cls.extract_email(text),
            "phone": cls.extract_phone(text),
            "raw_text": text[:500]  # First 500 chars for preview
        }
