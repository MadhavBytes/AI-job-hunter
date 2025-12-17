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

function extractKeywordsFromResume(text: string): string[] {
  const keywords = text.match(/\b[A-Za-z]+\b/g) || []
  return [...new Set(keywords.map(k => k.toLowerCase()))].slice(0, 20)
}

function calculateMatchScore(job: Job, keywords: string[]): number {
  const jobText = (job.title + ' ' + job.description + ' ' + job.company).toLowerCase()
  let matches = 0
  keywords.forEach(keyword => {
    if (jobText.includes(keyword)) matches++
  })
  return Math.round((matches / keywords.length) * 100) || 0
}

function App() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([])
  const [resume, setResume] = useState<File | null>(null)
  const [resumeText, setResumeText] = useState('')
  const [appliedJobs, setAppliedJobs] = useState<Set<string>>(new Set())
  const [selectedJob, setSelectedJob] = useState<Job | null>(null)
  const [isAutoApplying, setIsAutoApplying] = useState(false)
  const [autoApplyProgress, setAutoApplyProgress] = useState(0)
  const [keywords, setKeywords] = useState<string[]>([])

  useEffect(() => {
    const sampleJobs: Job[] = [
      { id: '1', title: 'Senior React Developer', company: 'Tech Corp', location: 'San Francisco', salary: '$150K-$200K', type: 'Full-time', description: 'Expert React and TypeScript developer needed', posted: '2d' },
      { id: '2', title: 'Full Stack Engineer', company: 'StartupXYZ', location: 'New York', salary: '$120K-$160K', type: 'Full-time', description: 'Build web apps with Node and React', posted: '1d' },
      { id: '3', title: 'Data Scientist', company: 'DataCorp', location: 'Remote', salary: '$130K-$170K', type: 'Remote', description: 'Python ML and data analytics', posted: '3d' },
      { id: '4', title: 'DevOps Engineer', company: 'CloudTech', location: 'Seattle', salary: '$140K-$180K', type: 'Full-time', description: 'Docker Kubernetes infrastructure', posted: '1w' },
      { id: '5', title: 'Frontend Developer', company: 'WebInc', location: 'Remote', salary: '$100K-$140K', type: 'Remote', description: 'React JavaScript CSS HTML', posted: '5d' },
      { id: '6', title: 'Backend Developer', company: 'APITech', location: 'Austin', salary: '$110K-$150K', type: 'Full-time', description: 'Node.js Express API development', posted: '4d' }
    ]
    setJobs(sampleJobs)
    setFilteredJobs(sampleJobs)
  }, [])

  const handleResumeUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const file = e.target.files[0]
      setResume(file)
      const reader = new FileReader()
      reader.onload = (event) => {
        const text = event.target?.result as string
        setResumeText(text)
        const extracted = extractKeywordsFromResume(text)
        setKeywords(extracted)
        filterJobsByResume(extracted)
      }
      reader.readAsText(file)
    }
  }

  const filterJobsByResume = (keywords: string[]) => {
    const scored = jobs.map(job => ({
      job,
      score: calculateMatchScore(job, keywords)
    })).sort((a, b) => b.score - a.score)
    
    setFilteredJobs(scored.map(item => item.job))
  }

  const handleAutoApply = async () => {
    if (!resume) {
      alert('Please upload your resume first')
      return
    }
    
    setIsAutoApplying(true)
    setAutoApplyProgress(0)
    
    const unmatchedJobs = filteredJobs.filter(job => !appliedJobs.has(job.id))
    let applied = 0
    
    for (const job of unmatchedJobs) {
      await new Promise(resolve => setTimeout(resolve, 500))
      setAppliedJobs(prev => new Set(prev).add(job.id))
      applied++
      setAutoApplyProgress(Math.round((applied / unmatchedJobs.length) * 100))
    }
    
    setIsAutoApplying(false)
    alert(`Auto-applied to ${applied} jobs!`)
  }

  const handleManualApply = (job: Job) => {
    if (!resume) {
      alert('Please upload your resume')
      return
    }
    setAppliedJobs(prev => new Set(prev).add(job.id))
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header"><h1>⚡ Job Hunter</h1></div>
        <div className="resume-section">
          <h3>Resume</h3>
          <label className="resume-upload">
            <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={handleResumeUpload} style={{display:'none'}} />
            <span>{resume ? '✓ ' + resume.name : 'Upload Resume'}</span>
          </label>
        </div>
        {resume && keywords.length > 0 && (
          <div className="keywords-section">
            <h3>Detected Skills</h3>
            <div className="keywords-list">
              {keywords.slice(0, 8).map(kw => <span key={kw} className="keyword-tag">{kw}</span>)}
            </div>
          </div>
        )}
        {resume && (
          <button className="auto-apply-btn" onClick={handleAutoApply} disabled={isAutoApplying}>
            {isAutoApplying ? `Applying... ${autoApplyProgress}%` : '🤖 Auto-Apply All'}
          </button>
        )}
      </aside>
      <main className="main-content">
        <div className="content-header"><h2>Matching Jobs</h2><p>{filteredJobs.length} found</p></div>
        <div className="jobs-container">
          {filteredJobs.map((job, idx) => {
            const score = calculateMatchScore(job, keywords)
            return (
              <div key={job.id} className={`job-card ${appliedJobs.has(job.id) ? 'applied' : ''}`} onClick={() => setSelectedJob(job)}>
                <div className="job-header">
                  <h3>{job.title}</h3>
                  {score > 0 && <span className="match-score">{score}% Match</span>}
                </div>
                <p className="company">{job.company}</p>
                <p>📍 {job.location} | {job.type}</p>
                <p>{job.salary}</p>
                <button onClick={(e) => { e.stopPropagation(); handleManualApply(job) }} disabled={appliedJobs.has(job.id)}>
                  {appliedJobs.has(job.id) ? '✓ Applied' : 'Apply'}
                </button>
              </div>
            )
          })}
        </div>
      </main>
      {selectedJob && <div className="modal-overlay" onClick={() => setSelectedJob(null)}>
        <div className="modal" onClick={(e) => e.stopPropagation()}>
          <button className="close-btn" onClick={() => setSelectedJob(null)}>×</button>
          <h2>{selectedJob.title}</h2>
          <p className="company">{selectedJob.company}</p>
          <p>📍 {selectedJob.location} | {selectedJob.salary}</p>
          <p className="description">{selectedJob.description}</p>
          <button className="modal-apply-btn" onClick={() => { handleManualApply(selectedJob); setSelectedJob(null) }} disabled={appliedJobs.has(selectedJob.id)}>
            {appliedJobs.has(selectedJob.id) ? '✓ Applied' : 'Apply Now'}
          </button>
        </div>
      </div>}
    </div>
  )
}

export default App
