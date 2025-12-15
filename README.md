# 🤖 AI Job Hunter - Automated Job Application System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Automate your job hunting with AI-powered resume adaptation and intelligent job filtering from Foorilla

## 🎯 Features

### 🔍 Smart Job Filtering (Foorilla API Integration)
- **Job Title/Keywords**: Search by job titles, technologies, and skills
- **Location Filtering**: Filter by country, region, city, or remote
- **Job Type**: Full-time, Part-time, Contract, Internship, Freelance
- **Salary Range**: Minimum salary filtering with currency support
- **Experience Level**: Entry-level, Mid-level, Senior, Executive
- **Industry**: Specific industry sectors (Tech, Finance, Healthcare, etc.)
- **Company Size**: Startup, SMB, Enterprise
- **Date Posted**: Jobs from last 7 days, 30 days, 90 days, all
- **Employment Status**: Work authorization requirements
- **Skills Match**: AI-powered skill matching with vector search

### 📄 Resume Management
- Upload PDF and DOCX resumes
- AI-powered resume parsing and extraction
- Resume tailoring for specific job applications
- Multiple resume versions for different roles
- Resume optimization suggestions

### 🤖 AI-Powered Features
- **Automatic Resume Adaptation**: Uses local Ollama LLM (Llama 2) to adapt resume based on job description
- **Intelligent Form Filling**: Auto-fill application forms with relevant resume data
- **Cover Letter Generation**: AI-generated cover letters
- **Skill Gap Analysis**: Identify missing skills and suggest learning paths

### 📊 Application Tracking
- Track all submitted applications
- Application status monitoring
- Interview scheduling
- Rejection feedback tracking
- Success rate analytics

### 🎨 Interactive UI
- Modern React frontend with Vite
- Real-time job search and filtering
- Application dashboard
- Resume builder and manager
- Application history and analytics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  FRONTEND (React + TypeScript + Vite)                   │
│  ├─ Job Search & Filtering UI                          │
│  ├─ Resume Manager                                     │
│  ├─ Application Dashboard                              │
│  └─ Settings & Preferences                             │
└────────────────────┬────────────────────────────────────┘
                     │ REST API / WebSocket
┌────────────────────▼────────────────────────────────────┐
│  BACKEND (FastAPI + Python 3.9+)                       │
│  ├─ Foorilla API Integration (jobdataapi.com)          │
│  │  ├─ Job Search with Advanced Filters                │
│  │  ├─ Job Details & Metadata                          │
│  │  └─ Region/Type/Industry lookups                    │
│  ├─ Resume Parser (PDF + DOCX)                         │
│  ├─ AI Form Filler (Playwright/Selenium)               │
│  ├─ LLM Service (Ollama + Llama 2)                     │
│  ├─ Application Tracker (SQLite)                       │
│  └─ Task Scheduler (Background jobs)                   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  SERVICES & INTEGRATIONS                               │
│  ├─ Foorilla Job Data API                              │
│  ├─ Ollama Local LLM (Llama 2/Mistral)                 │
│  ├─ SQLite Database                                    │
│  └─ Playwright (Web Automation)                        │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional)
- Foorilla API Key (free tier available at https://foorilla.com/)
- Ollama installed (for local LLM)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MadhavBytes/AI-job-hunter.git
   cd AI-job-hunter
   ```

2. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
   ```env
   FOORILLA_API_KEY=your_api_key_here
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   DEBUG=False
   ```

3. **Install Backend Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Start Ollama Server** (for AI features)
   ```bash
   ollama serve
   # In another terminal: ollama pull llama2
   ```

5. **Run Backend**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   # API will be available at http://localhost:8000
   ```

6. **Setup Frontend** (in new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   # Frontend will be available at http://localhost:5173
   ```

## 📡 Foorilla API Filters

All Foorilla filters are available through our API endpoints:

### GET /api/jobs/search

Query Parameters:
```json
{
  "title": "Python Developer",
  "location": "United States",
  "country": "US",
  "region": "California",
  "job_type": "Full-time",
  "min_salary": 100000,
  "currency": "USD",
  "experience_level": "Mid-level",
  "industry": "Technology",
  "company_size": "Enterprise",
  "remote_option": true,
  "max_age_days": 30,
  "limit": 50
}
```

## 🔑 API Endpoints

### Jobs
- `GET /api/jobs/search` - Search jobs with filters
- `GET /api/jobs/{job_id}` - Get job details
- `GET /api/jobs/filters/regions` - Get available regions
- `GET /api/jobs/filters/types` - Get job types
- `GET /api/jobs/filters/industries` - Get industries

### Resumes
- `POST /api/resumes/upload` - Upload resume (PDF/DOCX)
- `GET /api/resumes` - List user resumes
- `GET /api/resumes/{resume_id}` - Get resume details
- `DELETE /api/resumes/{resume_id}` - Delete resume

### Applications
- `POST /api/applications/auto-apply` - Auto-apply to job
- `GET /api/applications` - Get application history
- `GET /api/applications/{app_id}` - Get application details
- `PUT /api/applications/{app_id}/status` - Update application status

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.109
- **Server**: Uvicorn
- **Database**: SQLite + SQLAlchemy
- **Web Automation**: Playwright, Selenium
- **Resume Parsing**: PyPDF2, python-docx, pdf2image
- **AI/ML**: Ollama, llama-cpp-python
- **Job Data**: Foorilla jobdata API
- **Async**: aiohttp, asyncio

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Tailwind CSS
- **State Management**: Zustand/Redux
- **API Client**: Axios

## 📋 Project Status

- [x] Backend setup & FastAPI configuration
- [x] Foorilla API integration with filters
- [x] Configuration management
- [ ] Resume parser module
- [ ] LLM integration for resume adaptation
- [ ] Web automation module
- [ ] React frontend UI
- [ ] Application tracking database
- [ ] Docker & deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions, please create an issue on GitHub.

## 🙏 Acknowledgments

- Foorilla for the comprehensive Job Data API
- Ollama for local LLM capabilities
- FastAPI and React communities
