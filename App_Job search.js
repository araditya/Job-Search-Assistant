import React, { useState } from 'react';
import JobTable from './JobTable';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [resume, setResume] = useState(null);
  const [jobs, setJobs] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('query', query);
    if (resume) formData.append('resume', resume);

    try {
      const res = await axios.post('/search_jobs', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setJobs(res.data);
    } catch (err) {
      setError(err.message || 'Request failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Job Search App</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: 12 }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search jobs..."
          style={{ marginRight: 8 }}
        />
        <input type="file" onChange={e => setResume(e.target.files[0])} accept=".txt,.pdf" style={{ marginRight: 8 }} />
        <button type="submit" disabled={loading}>{loading ? 'Searching...' : 'Search'}</button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {jobs && <JobTable jobs={jobs} />}
    </div>
  );
}

export default App;
