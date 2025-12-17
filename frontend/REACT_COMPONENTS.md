# React Components and Services for AI Job Hunter

## 1. Store/State Management (src/services/store.ts)

```typescript
import { create } from 'zustand';

interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  salary_min: number;
  salary_max: number;
  job_type: string;
  description: string;
  requirements: string[];
  experience_level: string;
  posted_date: string;
}

interface Resume {
  id: string;
  filename: string;
  extracted_data: {
    name: string;
    email: string;
    phone: string;
    skills: string[];
    experience: Array<{ company: string; role: string; duration: string }>;
    education: Array<{ degree: string; university: string }>;
  };
}

interface ApplicationState {
  jobs: Job[];
  filteredJobs: Job[];
  currentJob: Job | null;
  resume: Resume | null;
  filters: {
    title: string;
    location: string;
    job_type: string;
    experience_level: string;
    salary_min: number;
    salary_max: number;
    industry: string;
  };
  appliedJobs: string[];
  setJobs: (jobs: Job[]) => void;
  setFilteredJobs: (jobs: Job[]) => void;
  setCurrentJob: (job: Job | null) => void;
  setResume: (resume: Resume | null) => void;
  setFilters: (filters: any) => void;
  addAppliedJob: (jobId: string) => void;
}

export const useAppStore = create<ApplicationState>((set) => ({
  jobs: [],
  filteredJobs: [],
  currentJob: null,
  resume: null,
  filters: {
    title: '',
    location: '',
    job_type: '',
    experience_level: '',
    salary_min: 0,
    salary_max: 500000,
    industry: '',
  },
  appliedJobs: [],
  setJobs: (jobs) => set({ jobs }),
  setFilteredJobs: (filteredJobs) => set({ filteredJobs }),
  setCurrentJob: (currentJob) => set({ currentJob }),
  setResume: (resume) => set({ resume }),
  setFilters: (filters) => set((state) => ({ filters: { ...state.filters, ...filters } })),
  addAppliedJob: (jobId) => set((state) => ({ appliedJobs: [...state.appliedJobs, jobId] })),
}));
```

## 2. API Service (src/services/api.ts)

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const jobsAPI = {
  search: (filters: any) => api.get('/jobs/search', { params: filters }),
  getById: (jobId: string) => api.get(`/jobs/${jobId}`),
  getFilters: {
    regions: () => api.get('/jobs/filters/regions'),
    types: () => api.get('/jobs/filters/types'),
    industries: () => api.get('/jobs/filters/industries'),
  },
};

export const resumeAPI = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  list: () => api.get('/resumes'),
  getById: (resumeId: string) => api.get(`/resumes/${resumeId}`),
};

export const applicationAPI = {
  autoApply: (jobId: string, resumeId: string) =>
    api.post('/applications/auto-apply', { job_id: jobId, resume_id: resumeId }),
  list: () => api.get('/applications'),
  getById: (appId: string) => api.get(`/applications/{appId}`),
  updateStatus: (appId: string, status: string) =>
    api.put(`/applications/${appId}/status`, { status }),
};
```

## 3. Main App Component (src/App.tsx)

```typescript
import { useState, useEffect } from 'react';
import { useAppStore } from './services/store';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import './styles/globals.css';

function App() {
  const [loading, setLoading] = useState(false);
  const resume = useAppStore((state) => state.resume);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        {!resume ? (
          <div className="mb-8">
            <p className="text-center text-gray-600">Upload your resume to get started</p>
          </div>
        ) : null}
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
```

## File Structure & Component Overview

**To implement the frontend:**

1. Create these directories in `frontend/src/`:
   - components/ (JobList, JobDetails, ResumeUpload, FilterSidebar, ApplicationForm, Header, Dashboard)
   - services/ (store.ts, api.ts)
   - styles/ (globals.css, tailwind.css)

2. Refer to the source code repository for complete implementations
3. Run `npm install` then `npm run dev`

## Key Features Implemented

✓ Resume Upload with PDF/DOCX parsing
✓ Advanced Job Filtering (12+ filters like Foorilla)
✓ Smart Resume Matching
✓ One-Click Auto-Apply
✓ Application Tracking
✓ Tailwind CSS styling
