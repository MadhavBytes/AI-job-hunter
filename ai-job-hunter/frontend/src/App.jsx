import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:9000';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [parsedResume, setParsedResume] = useState(null);
  const [showUploadSuccess, setShowUploadSuccess] = useState(false);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/jobs`);
      setJobs(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching jobs:', err);
      setError('Failed to load jobs');
    } finally {
      setLoading(false);
    }
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setResumeFile(file);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/api/upload-resume`, formData);
      setParsedResume(response.data);
      setShowUploadSuccess(true);
      setTimeout(() => setShowUploadSuccess(false), 3000);
    } catch (err) {
      console.error('Error uploading resume:', err);
      alert('Failed to upload resume');
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🤖 AI Job Hunter</h1>
        <p>Automated Job Application Tool</p>
      </header>

      <main className="app-main">
        <section className="upload-section">
          <h2>Upload Your Resume</h2>
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleResumeUpload}
            className="file-input"
          />
          {showUploadSuccess && (
            <div className="success-message">
              ✅ Resume uploaded successfully!
              {parsedResume && (
                <div className="resume-info">
                  <p><strong>Skills:</strong> {parsedResume.skills.join(', ')}</p>
                  <p><strong>Experience:</strong> {parsedResume.experience_years} years</p>
                </div>
              )}
            </div>
          )}
        </section>

        <section className="jobs-section">
          <h2>Available Jobs</h2>
          {loading && <p>Loading jobs...</p>}
          {error && <p className="error">{error}</p>}
          {jobs.length > 0 ? (
            <table className="jobs-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Company</th>
                  <th>Location</th>
                  <th>Salary</th>
                  <th>Type</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id}>
                    <td>{job.title}</td>
                    <td>{job.company}</td>
                    <td>{job.location}</td>
                    <td>{job.salary}</td>
                    <td>{job.job_type}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            !loading && <p>No jobs available</p>
          )}
        </section>
      </main>

      <footer className="app-footer">
        <p>Backend: {API_URL} | Status: ✅ Ready</p>
      </footer>
    </div>
  );
}

export default App;