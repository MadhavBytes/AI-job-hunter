# Frontend Setup - Quick Start Guide

## Fast Setup (5 minutes)

If you're on Mac/Linux or Windows with WSL:

### Step 1: Clone and Setup
```bash
cd frontend
npm install
```

### Step 2: Create Directory Structure
```bash
mkdir -p src/{components,services,styles}
```

### Step 3: Copy Configuration Files

The following files are already in this directory:
- `package.json` - DONE
- `vite.config.ts` - DONE
- Create `tsconfig.json` - use template below
- Create `postcss.config.js` - use template below
- Create `tailwind.config.js` - use template below

### Step 4: Add Source Files (see REACT_COMPONENTS.md)

Create files in src/ based on the documentation

### Step 5: Run Development Server
```bash
npm run dev
```
Open http://localhost:5173 in your browser

---

## Main Features Checklist

- Resume Upload (PDF/DOCX)
- Job Listing with Foorilla-style Cards
- Advanced Filtering (12+ filters)
- Smart Resume Matching
- Job Details Modal
- One-Click Auto-Apply
- Application Tracking Dashboard
- Resume Parser Integration
- Zustand State Management
- Tailwind CSS Styling

---

## Key Components

1. Header - Navigation with resume status
2. Dashboard - Three-column layout (Filters|Jobs|Sidebar)
3. FilterSidebar - All job filters
4. JobList - Job cards with match %
5. JobDetails - Full job description modal
6. ResumeUpload - Drag & drop resume
7. ApplicationForm - Auto-filled application form

---

## API Integration

Backend runs on: http://localhost:8000

Endpoints:
- GET /api/jobs/search - Search jobs
- POST /api/resumes/upload - Upload resume
- POST /api/applications/auto-apply - Auto-apply
- GET /api/applications - View applications
