import { useState, useEffect } from 'react';
import { useAppStore } from './services/store';
import './styles/globals.css';

const App = () => {
  const [loading, setLoading] = useState(true);
  const resume = useAppStore((state) => state.resume);
  const setResume = useAppStore((state) => state.setResume);

  useEffect(() => {
    setLoading(false);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-slate-900 border-b border-slate-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              🤖 AI Job Hunter
            </div>
          </div>
          {resume && (
            <div className="flex items-center gap-2 px-3 py-1 bg-green-900 bg-opacity-50 rounded-full">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              <span className="text-sm text-green-300">Resume Loaded</span>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {!resume ? (
          <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg p-8 text-white text-center">
            <h2 className="text-3xl font-bold mb-4">Welcome to AI Job Hunter</h2>
            <p className="text-lg mb-6 opacity-90">Upload your resume to get started with smart job matching and auto-apply</p>
            <div className="bg-white bg-opacity-10 backdrop-blur rounded-lg p-6 border border-white border-opacity-20">
              <p className="text-base">Powered by AI Resume Parsing &bull; Foorilla Job API &bull; Automated Applications</p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Sidebar Filters */}
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 h-fit">
              <h3 className="text-lg font-semibold text-white mb-4">Filters</h3>
              <div className="space-y-4">
                <div>
                  <label className="text-sm text-gray-300">Job Title</label>
                  <input type="text" placeholder="e.g., Python Developer" className="w-full mt-2 bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-gray-400" />
                </div>
                <div>
                  <label className="text-sm text-gray-300">Location</label>
                  <input type="text" placeholder="e.g., Remote" className="w-full mt-2 bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-gray-400" />
                </div>
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded transition">
                  Search Jobs
                </button>
              </div>
            </div>

            {/* Main Content Area */}
            <div className="lg:col-span-2">
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 text-center text-gray-400">
                <p className="text-lg">Jobs will appear here once you search</p>
              </div>
            </div>

            {/* Right Sidebar */}
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 h-fit">
              <h3 className="text-lg font-semibold text-white mb-4">Resume Stats</h3>
              <div className="space-y-3">
                <div className="text-sm text-gray-300">
                  <span className="font-semibold text-blue-400">Skills:</span> {resume?.extracted_data?.skills?.length || 0}
                </div>
                <div className="text-sm text-gray-300">
                  <span className="font-semibold text-blue-400">Experience:</span> {resume?.extracted_data?.experience?.length || 0} roles
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
