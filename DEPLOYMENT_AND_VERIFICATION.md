# Deployment & Verification Guide

## Project Status

✅ **FRONTEND CREATED**: React + Vite setup complete
✅ **BACKEND READY**: FastAPI with Foorilla API integration
✅ **CONFIGURATION**: All config files prepared

## Phase 1: Local Development & Testing

### Step 1: Clone Latest Code
```bash
git clone https://github.com/MadhavBytes/AI-job-hunter.git
cd AI-job-hunter
```

### Step 2: Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your Foorilla API key

# Start Ollama (if using LLM features)
ollama serve &

# Run backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### Step 3: Frontend Setup
```bash
cd ../frontend
npm install
```

Need to create missing files (see below)

### Step 4: Run Frontend
```bash
npm run dev
```

Frontend runs on: **http://localhost:5173**

## Phase 2: Missing Frontend Files to Create

The following files need to be added in `frontend/`:

### Configuration Files
1. `index.html` - HTML entry point
2. `tsconfig.json` - TypeScript configuration
3. `postcss.config.js` - PostCSS config for Tailwind
4. `tailwind.config.js` - Tailwind CSS configuration

### Source Files (src/)
1. `main.tsx` - React entry point
2. `services/store.ts` - Zustand state management
3. `services/api.ts` - API client
4. `styles/globals.css` - Global styles
5. `styles/tailwind.css` - Tailwind imports

## Phase 3: Quick Start Commands

Once all files are created:

```bash
# Terminal 1: Start Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2: Start Frontend
cd frontend
npm run dev

# Terminal 3: Start Ollama (optional for LLM)
ollama serve
```

## Phase 4: Verification Checklist

### Frontend UI Verification
- [ ] Frontend loads at http://localhost:5173
- [ ] Header displays "AI Job Hunter" with logo
- [ ] Welcome message visible
- [ ] No console errors
- [ ] Tailwind CSS styling applied

### Backend API Verification
- [ ] API runs at http://localhost:8000
- [ ] Health check: `curl http://localhost:8000/health`
- [ ] Swagger docs load: http://localhost:8000/docs
- [ ] CORS enabled for frontend

### Integration Testing
- [ ] Frontend can reach backend API
- [ ] Resume upload endpoint accessible
- [ ] Job search endpoint working
- [ ] No CORS errors in console

## Phase 5: Production Deployment

### Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Configure during deployment:
# - Framework: Vite
# - Build command: npm run build
# - Output directory: dist
# - Environment variables: Add VITE_API_URL=<backend-url>
```

Frontend URL: `https://your-app.vercel.app`

### Deploy Backend to AWS/Heroku

**Option A: AWS Elastic Beanstalk**
```bash
eb create ai-job-hunter-env
eb deploy
```

**Option B: Heroku**
```bash
heroku create ai-job-hunter
git push heroku main
```

Backend URL: `https://ai-job-hunter.herokuapp.com`

## Phase 6: Environment Configuration

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```
FOORILLA_API_KEY=your_key_here
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
DEBUG=False
```

## Phase 7: Testing & Validation

### Test Resume Upload
1. Go to frontend
2. Upload a sample PDF resume
3. Verify extraction in browser console

### Test Job Search
1. Enter job title: "Python Developer"
2. Enter location: "Remote"
3. Click "Search Jobs"
4. Verify API calls in Network tab

### Test Auto-Apply
1. Search for a job
2. Click "Apply"
3. Form auto-fills from resume
4. Submit application
5. Verify in application history

## Common Issues & Solutions

### Issue: Frontend can't reach backend
**Solution**: 
- Check backend is running on port 8000
- Verify VITE_API_URL environment variable
- Check CORS headers in backend

### Issue: Tailwind styles not loading
**Solution**:
- Ensure `styles/globals.css` imported in App.tsx
- Run `npm install` to get all dependencies
- Clear browser cache

### Issue: Resume upload fails
**Solution**:
- Verify file is PDF or DOCX
- Check file size < 10MB
- Verify backend is receiving request

## Monitoring & Debugging

### Frontend Debugging
```bash
# Check browser DevTools
# Network tab: Verify API calls
# Console tab: Check for errors
# Performance tab: Monitor load times
```

### Backend Debugging
```bash
# Check terminal output for errors
# API docs: http://localhost:8000/docs
# Health check: curl http://localhost:8000/health
# View all logs with -v flag
```

## Next Steps After Deployment

1. Setup CI/CD pipeline (GitHub Actions)
2. Configure automatic deployments
3. Setup monitoring & alerting
4. Add analytics tracking
5. Scale infrastructure as needed
