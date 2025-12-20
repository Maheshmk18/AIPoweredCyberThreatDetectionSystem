import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './Analyze.css';

function Analyze() {
    const [text, setText] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [fileResults, setFileResults] = useState(null);
    const navigate = useNavigate();

    const handleTextAnalysis = async (e) => {
        e.preventDefault();
        if (!text.trim()) return;

        setLoading(true);
        setResult(null);

        try {
            const response = await api.post('/analyze/text', { text });
            setResult(response.data);
        } catch (error) {
            alert(error.response?.data?.message || 'Analysis failed');
        } finally {
            setLoading(false);
        }
    };

    const handleFileAnalysis = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        setFileResults(null);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await api.post('/analyze/file', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setFileResults(response.data);
        } catch (error) {
            alert(error.response?.data?.message || 'File analysis failed');
        } finally {
            setLoading(false);
        }
    };

    const getSeverityClass = (prediction) => {
        switch (prediction) {
            case 'malicious': return 'severity-malicious';
            case 'suspicious': return 'severity-suspicious';
            default: return 'severity-normal';
        }
    };

    return (
        <div className="analyze-container">
            <div className="analyze-header">
                <button className="back-button" onClick={() => navigate('/dashboard')}>
                    ← Back to Dashboard
                </button>
                <h1>Analyze Logs</h1>
                <p className="analyze-subtitle">Upload files or analyze individual log entries</p>
            </div>

            <div className="analyze-content">
                {/* Text Analysis */}
                <div className="card analyze-card">
                    <div className="card-header">
                        <h3 className="card-title">📝 Single Log Analysis</h3>
                    </div>
                    <form onSubmit={handleTextAnalysis} className="analyze-form">
                        <div className="input-group">
                            <label className="input-label">Enter Log Text</label>
                            <textarea
                                className="input textarea"
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                                placeholder="Example: admin login failed 5 times from unknown IP address"
                                rows="4"
                                required
                            />
                        </div>
                        <button type="submit" className="btn btn-primary w-full" disabled={loading}>
                            {loading ? (
                                <>
                                    <div className="spinner"></div>
                                    Analyzing...
                                </>
                            ) : (
                                '🔍 Analyze Log'
                            )}
                        </button>
                    </form>

                    {result && (
                        <div className="result-card fade-in">
                            <div className="result-header">
                                <h4>Analysis Result</h4>
                            </div>
                            <div className="result-body">
                                <div className="result-item">
                                    <span className="result-label">Original:</span>
                                    <span className="result-value">{result.original}</span>
                                </div>
                                <div className="result-item">
                                    <span className="result-label">Prediction:</span>
                                    <span className={`badge badge-${result.prediction}`}>
                                        {result.prediction.toUpperCase()}
                                    </span>
                                </div>
                                <div className="result-item">
                                    <span className="result-label">Confidence:</span>
                                    <div className="confidence-display">
                                        <div className="confidence-bar">
                                            <div
                                                className={`confidence-fill ${getSeverityClass(result.prediction)}`}
                                                style={{ width: `${result.score * 100}%` }}
                                            ></div>
                                        </div>
                                        <span className="confidence-value">{(result.score * 100).toFixed(1)}%</span>
                                    </div>
                                </div>
                                <div className="result-item">
                                    <span className="result-label">Sequence:</span>
                                    <span className="result-value sequence-text">{result.sequence}</span>
                                </div>
                                {result.probabilities && (
                                    <div className="probabilities">
                                        <h5>Detailed Probabilities:</h5>
                                        <div className="prob-grid">
                                            <div className="prob-item">
                                                <span className="prob-label">Normal:</span>
                                                <span className="prob-value">{(result.probabilities.normal * 100).toFixed(1)}%</span>
                                            </div>
                                            <div className="prob-item">
                                                <span className="prob-label">Suspicious:</span>
                                                <span className="prob-value">{(result.probabilities.suspicious * 100).toFixed(1)}%</span>
                                            </div>
                                            <div className="prob-item">
                                                <span className="prob-label">Malicious:</span>
                                                <span className="prob-value">{(result.probabilities.malicious * 100).toFixed(1)}%</span>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                {/* File Upload Analysis */}
                <div className="card analyze-card">
                    <div className="card-header">
                        <h3 className="card-title">📁 Bulk File Analysis</h3>
                    </div>
                    <form onSubmit={handleFileAnalysis} className="analyze-form">
                        <div className="input-group">
                            <label className="input-label">Upload Log File (CSV or TXT)</label>
                            <div className="file-upload-area">
                                <input
                                    type="file"
                                    id="file-input"
                                    className="file-input"
                                    accept=".csv,.txt"
                                    onChange={(e) => setFile(e.target.files[0])}
                                    required
                                />
                                <label htmlFor="file-input" className="file-upload-label">
                                    <span className="upload-icon">📤</span>
                                    <span className="upload-text">
                                        {file ? file.name : 'Click to select file or drag and drop'}
                                    </span>
                                    <span className="upload-hint">CSV or TXT files (max 100 logs)</span>
                                </label>
                            </div>
                        </div>
                        <button type="submit" className="btn btn-primary w-full" disabled={loading}>
                            {loading ? (
                                <>
                                    <div className="spinner"></div>
                                    Analyzing File...
                                </>
                            ) : (
                                '🚀 Analyze File'
                            )}
                        </button>
                    </form>

                    {fileResults && (
                        <div className="result-card fade-in">
                            <div className="result-header">
                                <h4>File Analysis Complete</h4>
                            </div>
                            <div className="file-stats">
                                <div className="stat-box">
                                    <div className="stat-value">{fileResults.total_logs}</div>
                                    <div className="stat-label">Total Logs</div>
                                </div>
                                <div className="stat-box normal">
                                    <div className="stat-value">{fileResults.statistics.normal}</div>
                                    <div className="stat-label">Normal</div>
                                </div>
                                <div className="stat-box suspicious">
                                    <div className="stat-value">{fileResults.statistics.suspicious}</div>
                                    <div className="stat-label">Suspicious</div>
                                </div>
                                <div className="stat-box malicious">
                                    <div className="stat-value">{fileResults.statistics.malicious}</div>
                                    <div className="stat-label">Malicious</div>
                                </div>
                            </div>
                            <div className="results-table-container">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Log Event</th>
                                            <th>Prediction</th>
                                            <th>Score</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {fileResults.results.slice(0, 20).map((log, index) => (
                                            <tr key={index}>
                                                <td>{index + 1}</td>
                                                <td className="log-event">{log.original}</td>
                                                <td>
                                                    <span className={`badge badge-${log.prediction}`}>
                                                        {log.prediction}
                                                    </span>
                                                </td>
                                                <td>{(log.score * 100).toFixed(1)}%</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                                {fileResults.results.length > 20 && (
                                    <p className="text-muted text-center mt-2">
                                        Showing first 20 of {fileResults.results.length} results
                                    </p>
                                )}
                            </div>
                            <button
                                className="btn btn-secondary w-full mt-2"
                                onClick={() => navigate('/dashboard')}
                            >
                                View All Logs in Dashboard
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Analyze;
