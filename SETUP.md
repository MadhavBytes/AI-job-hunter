# 🚀 AI Job Hunter - Local Setup Guide

Complete step-by-step instructions for setting up the AI Job Hunter locally on your Windows/Mac/Linux system.

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+
- **RAM**: 8GB minimum (16GB recommended for Ollama + browser)
- **Storage**: 10GB for Ollama models + dependencies
- **Python**: 3.9+ ([Download](https://www.python.org/downloads/))
- **Node.js**: 16+ ([Download](https://nodejs.org/))

### Accounts & Keys Needed
1. **Foorilla API Key** (FREE tier)
   - Visit: https://foorilla.com/
   - Sign up for free account
   - Get API key from dashboard

2. **GitHub Account** (already have)
   - For cloning the repo

## ⚡ Quick Start (5 Steps)

### Step 1: Clone Repository

**On Windows (PowerShell):**
```powershell
# Navigate to where you want the project
cd C:\projects  # or your preferred location

# Clone the repo
git clone https://github.com/MadhavBytes/AI-job-hunter.git
cd AI-job-hunter
```

**On Mac/Linux (Terminal):**
```bash
cd ~/projects  # or your preferred location
git clone https://github.com/MadhavBytes/AI-job-hunter.git
cd AI-job-hunter
```

### Step 2: Setup Python Backend

**Create Virtual Environment:**

```bash
# Create venv
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Setup Environment Variables:**
```bash
# Copy example file
cp .env.example .env

# Edit .env with your Foorilla API key
# Windows: notepad .env
# Mac/Linux: nano .env
```

Edit `.env`:
```env
FOORILLA_API_KEY=your_foorilla_api_key_here
```

### Step 3: Install & Start Ollama

**Download Ollama:**
- Go to https://ollama.ai
- Download for your OS
- Install (follow default settings)

**Start Ollama Server:**

```bash
# Start Ollama (runs on http://localhost:11434)
ollama serve

# In a NEW terminal, pull Llama 2 model:
ollama pull llama2
# Note: ~4GB download, first time only
```

### Step 4: Start FastAPI Backend

```bash
# Make sure venv is activated
cd backend
python -m uvicorn main:app --reload

# You should see:
# Uvicorn running on http://127.0.0.1:8000
# API docs: http://localhost:8000/docs
```

### Step 5: Setup Frontend (Optional)

```bash
# Open new terminal, from project root
cd frontend
npm install
npm run dev

# Frontend will be at http://localhost:5173
```

## ✅ Verify Installation

### Backend Health Check

```bash
# In a new terminal (with venv activated)
curl http://localhost:8000/health

# Should return:
# {"status": "healthy"}
```

### Test API with Foorilla

```bash
curl -X GET "http://localhost:8000/api/jobs/search?title=Python&location=US&limit=5" \
  -H "Content-Type: application/json"
```

### Check Ollama Connection

```bash
curl http://localhost:11434/api/tags

# Should return list of models including llama2
```

## 🗂️ Project Structure After Setup

```
AI-job-hunter/
├── venv/                    # Python virtual environment
├── backend/
│   ├── main.py             # FastAPI app
│   ├── config.py           # Settings
│   └── services/
│       └── foorilla_service.py  # Job API integration
├── frontend/               # React app (create after step 5)
├── data/                   # Created on first run (database)
├── resumes/
│   └── uploads/            # Resume storage
├── logs/                   # Application logs
├── .env                    # Your configuration (SECRET!)
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## 🐛 Troubleshooting

### Issue: `python: command not found`
**Solution**: Python not in PATH. Install from python.org or use `python3`:
```bash
python3 -m venv venv
```

### Issue: `venv\Scripts\activate` doesn't work on PowerShell
**Solution**: Allow script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again
```

### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Ensure venv is activated:
```bash
# Should see (venv) at start of terminal line
# If not: activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Then install again
pip install -r requirements.txt
```

### Issue: Ollama not connecting
**Solution**: Check if service is running:
```bash
# Windows: Check if ollama.exe is running in Task Manager
# Mac: Check if Ollama app is in menu bar
# Linux: Check process
ps aux | grep ollama
```

### Issue: Foorilla API key returns 401
**Solution**: 
1. Verify key in `.env` file (no spaces!)
2. Check key is valid at https://foorilla.com/accounts/dashboard/
3. Ensure free tier hasn't been exceeded

### Issue: Port 8000 already in use
**Solution**: Change port:
```bash
python -m uvicorn main:app --reload --port 8001
```

## 📱 Using the Application

### Via API (Backend only)
```bash
# Search jobs
curl -X GET "http://localhost:8000/api/jobs/search?title=Python&location=US"

# Get job types available
curl -X GET "http://localhost:8000/api/jobs/filters/types"

# Get regions/countries
curl -X GET "http://localhost:8000/api/jobs/filters/regions"
```

### Via Frontend (When built)
1. Open http://localhost:5173
2. Upload your resume
3. Set job preferences
4. Search and auto-apply!

## 🔧 Development Tips

### Using WSL2 on Windows (Recommended for MLOps)

If you use WSL2 (great for Docker):

```bash
# In WSL2 terminal
cd /mnt/c/projects/AI-job-hunter
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Ollama from Windows CMD, then connect:
# In .env, set: OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### Hot Reload for Development

FastAPI auto-reloads on file changes:
```bash
python -m uvicorn main:app --reload
# Edit files and changes apply immediately
```

### View API Documentation

While backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Database Access

```bash
# View SQLite database
sqlite3 data/job_hunter.db

# List tables
.tables

# Query applications
SELECT * FROM applications;
```

## 🚀 Next Steps After Setup

1. **Test Foorilla API integration**
   - Call `/api/jobs/search` endpoint
   - Verify job results from Foorilla

2. **Build Resume Parser**
   - Upload PDF/DOCX resume
   - Test text extraction

3. **Test LLM Integration**
   - Verify Ollama is working
   - Test resume adaptation with job description

4. **Build Frontend**
   - Create React components
   - Connect to backend API

## 📚 Useful Links

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Ollama Models**: https://ollama.ai/library
- **Foorilla API**: https://jobdataapi.com/docs/
- **Python Virtual Envs**: https://docs.python.org/3/tutorial/venv.html
- **React + Vite**: https://vitejs.dev/guide/

## 💬 Need Help?

If you encounter issues:
1. Check this troubleshooting guide
2. Check individual service logs
3. Create an issue on GitHub
4. Check service documentation

## ✨ You're All Set!

Once setup is complete, you have:
- ✅ Python FastAPI backend running
- ✅ Ollama LLM service running
- ✅ Foorilla API configured
- ✅ Database ready
- ✅ React frontend ready to build

Happy coding! 🚀
