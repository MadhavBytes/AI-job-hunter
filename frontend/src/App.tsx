import { useState, useEffect } from 'react'
import './App.css'

interface Job {
  id: string
  title: string
  company: string
  location: string
  salary?: string
  type: string
  description: string
  posted: string
}

function App() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([])
  const [resume, setResume] = useState<File | null>(null)
  const [appliedJobs, setAppliedJobs] = useState<Set<string>>(new Set())
  const [selectedJob, setSelectedJob] = useState<Job | null>(null)
  const [filters, setFilters] = useState({ jobType: '', location: '', keyword: '' })

  useEffect(() => {
    const sampleJobs: Job[] = [
      { id: '1', title: 'Senior React Developer', company: 'Tech Corp', location: 'San Francisco', salary: '$150K-$200K', type: 'Full-time', description: 'Experienced React dev needed', posted: '2d' },
      { id: '2', title: 'Full Stack Engineer', company: 'StartupXYZ', location: 'New York', salary: '$120K-$160K', type: 'Full-time', description: 'Build web apps', posted: '1d' },
      { id: '3', title: 'Data Scientist', company: 'DataCorp', location: 'Remote', salary: '$130K-$170K', type: 'Remote', description: 'ML and analytics', posted: '3d' },
      { id: '4', title: 'DevOps Engineer', company: 'CloudTech', location: 'Seattle', salary: '$140K-$180K', type: 'Full-time', description: 'Infrastructure work', posted: '1w' }
    ]
    setJobs(sampleJobs)
    setFilteredJobs(sampleJobs)
  }, [])

  const handleResumeUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setResume(e.target.files[0])
  }

  const handleFilterChange = (field: string, value: string) => {
    const newFilters = { ...filters, [field]: value }
    setFilters(newFilters)
    applyFilters(newFilters)
  }

  const applyFilters = (current: typeof filters) => {
    let filtered = jobs.filter(job => {
      if (current.jobType && job.type !== current.jobType) return false
      if (current.location && !job.location.toLowerCase().includes(current.location.toLowerCase())) return false
      if (current.keyword && !job.title.toLowerCase().includes(current.keyword.toLowerCase())) return false
      return true
    })
    setFilteredJobs(filtered)
  }

  const handleApply = (job: Job) => {
    if (!resume) { alert('Please upload your resume'); return }
    setAppliedJobs(prev => new Set(prev).add(job.id))
    alert(`Applied to ${job.title}`)
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header"><h1>AI Job Hunter</h1></div>
        <div className="resume-section">
          <h3>Resume</h3>
          <label className="resume-upload">
            <input type="file" accept=".pdf,.doc,.docx" onChange={handleResumeUpload} style={{display:'none'}} />
            <span>{resume ? resume.name : 'Upload Resume'}</span>
          </label>
        </div>
        <div className="filters-section">
          <h3>Filters</h3>
          <div className="filter-group">
            <label>Job Type</label>
            <select value={filters.jobType} onChange={(e) => handleFilterChange('jobType', e.target.value)}>
              <option value="">All Types</option>
              <option value="Full-time">Full-time</option>
              <option value="Remote">Remote</option>
              <option value="Contract">Contract</option>
            </select>
          </div>
          <div className="filter-group">
            <label>Location</label>
            <input type="text" placeholder="City" value={filters.location} onChange={(e) => handleFilterChange('location', e.target.value)} />
          </div>
          <div className="filter-group">
            <label>Keyword</label>
            <input type="text" placeholder="Job title" value={filters.keyword} onChange={(e) => handleFilterChange('keyword', e.target.value)} />
          </div>
        </div>
      </aside>
      <main className="main-content">
        <div className="content-header"><h2>Jobs</h2><p>{filteredJobs.length} found</p></div>
        <div className="jobs-container">
          {filteredJobs.map(job => (
            <div key={job.id} className={`job-card ${appliedJobs.has(job.id) ? 'applied' : ''}`} onClick={() => setSelectedJob(job)}>
              <h3>{job.title}</h3>
              <p className="company">{job.company}</p>
              <p>📍 {job.location} | {job.type}</p>
              <p>{job.salary}</p>
              <button onClick={(e) => { e.stopPropagation(); handleApply(job) }} disabled={appliedJobs.has(job.id)}>
                {appliedJobs.has(job.id) ? 'Applied' : 'Apply'}
              </button>
            </div>
          ))}
        </div>
      </main>
      {selectedJob && <div className="modal-overlay" onClick={() => setSelectedJob(null)}>
        <div className="modal" onClick={(e) => e.stopPropagation()}>
          <h2>{selectedJob.title}</h2>
          <p>{selectedJob.company}</p>
          <p>{selectedJob.location} | {selectedJob.salary}</p>
          <p>{selectedJob.description}</p>
          <button onClick={() => { handleApply(selectedJob); setSelectedJob(null) }} disabled={appliedJobs.has(selectedJob.id)}>
            {appliedJobs.has(selectedJob.id) ? 'Applied' : 'Apply'}
          </button>
        </div>
      </div>}
    </div>
  )
}

export default App
