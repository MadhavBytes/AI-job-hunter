import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Filters
  const [locationFilter, setLocationFilter] = useState('All');
  const [visaOnly, setVisaOnly] = useState(false);
  const [minScore, setMinScore] = useState(0.0);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/jobs`);
      setJobs(response.data || []);
      setError(null);
    } catch (err) {
      setError(`Error fetching jobs: ${err.message}`);
      setJobs([]);
    } finally {
      setLoading(false);
    }
  };

  const uniqueLocations = Array.from(new Set(jobs.map((j) => j.location))).filter(Boolean);

  const filteredJobs = jobs.filter((job) => {
    if (locationFilter !== 'All' && job.location !== locationFilter) return false;
    if (visaOnly && !job.visa_sponsorship) return false;
    if (typeof job.match_score === 'number' && job.match_score < minScore) return false;
    return true;
  });

  // Resume upload state & handlers
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedInfo, setUploadedInfo] = useState(null);

  const handleFileChange = (e) => {
    const f = e.target.files && e.target.files[0];
    setSelectedFile(f || null);
    setUploadedInfo(null);
  };

  const uploadResume = async () => {
    if (!selectedFile) return;
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append('file', selectedFile);
      const res = await axios.post(`${API_URL}/api/upload-resume`, fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      setUploadedInfo(res.data);
    } catch (err) {
      setError(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>🤖 AI Job Hunter</h1>
        <p>Find your perfect AI job powered by machine learning</p>
      </header>
      <main>
        <div className="controls">
          <div className="filters">
            <label>
              Location:{' '}
              <select value={locationFilter} onChange={(e) => setLocationFilter(e.target.value)}>
                <option value="All">All</option>
                {uniqueLocations.map((loc) => (
                  <option key={loc} value={loc}>
                    {loc}
                  </option>
                ))}
              </select>
            </label>

            <label>
              <input type="checkbox" checked={visaOnly} onChange={(e) => setVisaOnly(e.target.checked)} />
              {' '}Visa sponsorship only
            </label>

            <label>
              Min Match Score: {minScore.toFixed(2)}
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={minScore}
                onChange={(e) => setMinScore(parseFloat(e.target.value))}
              />
            </label>

            <button onClick={fetchJobs} disabled={loading}>
              {loading ? 'Loading...' : 'Refresh Jobs'}
            </button>

            {/* Resume upload */}
            <label>
              Upload Resume:
              <input type="file" accept=".pdf,.docx,.txt,.md" onChange={(e) => handleFileChange(e)} />
            </label>
            <button onClick={uploadResume} disabled={!selectedFile || uploading}>
              {uploading ? 'Uploading...' : 'Upload Resume'}
            </button>
            {uploadedInfo && (
              <div className="upload-info">
                <p><strong>Uploaded:</strong> {uploadedInfo.filename} ({uploadedInfo.size} bytes)</p>
                <pre style={{textAlign: 'left', maxHeight: 120, overflow: 'auto'}}>{uploadedInfo.text_snippet}</pre>
              </div>
            )}
