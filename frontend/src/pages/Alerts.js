import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './Alerts.css';

function Alerts() {
    const [alerts, setAlerts] = useState([]);
    const [filter, setFilter] = useState('all');
    const [loading, setLoading] = useState(true);
    const [investigatingAlert, setInvestigatingAlert] = useState(null);
    const navigate = useNavigate();

    const role = localStorage.getItem('role');

    useEffect(() => {
        fetchAlerts();
    }, [filter]);

    const fetchAlerts = async () => {
        try {
            let endpoint = '/logs?limit=100';

            if (role === 'normal_user') {
                endpoint = '/logs/me?limit=100';
            } else if (filter !== 'all') {
                endpoint = `/logs/filter/${filter}?limit=100`;
            }

            const response = await api.get(endpoint);

            // Filter for suspicious and malicious only
            const filteredAlerts = response.data.logs.filter(
                log => log.prediction === 'suspicious' || log.prediction === 'malicious'
            );

            setAlerts(filteredAlerts);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching alerts:', error);
            if (error.response?.status === 401) {
                localStorage.clear();
                navigate('/login');
            }
            setLoading(false);
        }
    };

    const getSeverityLevel = (prediction, score) => {
        if (prediction === 'malicious') {
            if (score > 0.9) return { level: 'critical', label: 'CRITICAL', color: '#dc2626' };
            return { level: 'high', label: 'HIGH', color: '#ef4444' };
        }
        if (score > 0.7) return { level: 'medium', label: 'MEDIUM', color: '#f59e0b' };
        return { level: 'low', label: 'LOW', color: '#fbbf24' };
    };

    const getTimeAgo = (timestamp) => {
        const seconds = Math.floor((new Date() - new Date(timestamp)) / 1000);

        if (seconds < 60) return `${seconds}s ago`;
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
        if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
        return `${Math.floor(seconds / 86400)}d ago`;
    };

    const handleInvestigate = (alert) => {
        setInvestigatingAlert(alert);
    };

    const handleResolve = (alert) => {
        if (window.confirm('Mark this alert as resolved?')) {
            // Remove from alerts list
            setAlerts(alerts.filter(a => a._id !== alert._id));
            alert('Alert marked as resolved');
        }
    };

    if (loading) {
        return (
            <div className="alerts-loading">
                <div className="spinner"></div>
                <p>Loading Alerts...</p>
            </div>
        );
    }

    const criticalAlerts = alerts.filter(a => getSeverityLevel(a.prediction, a.score).level === 'critical').length;
    const highAlerts = alerts.filter(a => getSeverityLevel(a.prediction, a.score).level === 'high').length;
    const mediumAlerts = alerts.filter(a => getSeverityLevel(a.prediction, a.score).level === 'medium').length;

    return (
        <div className="alerts-container">
            <div className="alerts-header">
                <div>
                    <button className="back-button" onClick={() => navigate('/dashboard')}>
                        ← Back to Dashboard
                    </button>
                    <h1>Security Alerts</h1>
                    <p className="alerts-subtitle">Real-time Threat Detection & Incident Monitoring</p>
                </div>

                <div className="alerts-summary">
                    <div className="summary-item critical">
                        <div className="summary-value">{criticalAlerts}</div>
                        <div className="summary-label">Critical</div>
                    </div>
                    <div className="summary-item high">
                        <div className="summary-value">{highAlerts}</div>
                        <div className="summary-label">High</div>
                    </div>
                    <div className="summary-item medium">
                        <div className="summary-value">{mediumAlerts}</div>
                        <div className="summary-label">Medium</div>
                    </div>
                </div>
            </div>

            <div className="alerts-filters">
                <button
                    className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                    onClick={() => setFilter('all')}
                >
                    All Alerts ({alerts.length})
                </button>
                <button
                    className={`filter-btn ${filter === 'malicious' ? 'active' : ''}`}
                    onClick={() => setFilter('malicious')}
                >
                    🚨 Malicious
                </button>
                <button
                    className={`filter-btn ${filter === 'suspicious' ? 'active' : ''}`}
                    onClick={() => setFilter('suspicious')}
                >
                    ⚠️ Suspicious
                </button>
            </div>

            <div className="alerts-grid">
                {alerts.length === 0 ? (
                    <div className="no-alerts">
                        <div className="no-alerts-icon">✓</div>
                        <h3>No Active Alerts</h3>
                        <p>All systems operating normally</p>
                    </div>
                ) : (
                    alerts.map((alert, index) => {
                        const severity = getSeverityLevel(alert.prediction, alert.score);

                        return (
                            <div key={index} className={`alert-card ${severity.level} fade-in`} style={{ animationDelay: `${index * 0.05}s` }}>
                                <div className="alert-header">
                                    <div className="alert-severity" style={{ background: severity.color }}>
                                        {severity.label}
                                    </div>
                                    <div className="alert-time">{getTimeAgo(alert.timestamp)}</div>
                                </div>

                                <div className="alert-body">
                                    <div className="alert-title">
                                        {alert.prediction === 'malicious' ? '🚨' : '⚠️'} {alert.prediction.toUpperCase()} BEHAVIOUR DETECTED
                                    </div>

                                    <div className="alert-event">
                                        <div className="event-label">Event:</div>
                                        <div className="event-text">{alert.event}</div>
                                    </div>

                                    <div className="alert-details">
                                        <div className="detail-item">
                                            <span className="detail-label">Confidence:</span>
                                            <div className="confidence-bar">
                                                <div
                                                    className="confidence-fill"
                                                    style={{
                                                        width: `${alert.score * 100}%`,
                                                        background: severity.color
                                                    }}
                                                ></div>
                                            </div>
                                            <span className="detail-value">{(alert.score * 100).toFixed(1)}%</span>
                                        </div>

                                        <div className="detail-item">
                                            <span className="detail-label">Timestamp:</span>
                                            <span className="detail-value">{new Date(alert.timestamp).toLocaleString()}</span>
                                        </div>

                                        {role !== 'normal_user' && alert.user_email && (
                                            <div className="detail-item">
                                                <span className="detail-label">User:</span>
                                                <span className="detail-value">{alert.user_email}</span>
                                            </div>
                                        )}

                                        <div className="detail-item">
                                            <span className="detail-label">Sequence:</span>
                                            <span className="detail-value sequence-text">{alert.sequence}</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="alert-footer">
                                    <button
                                        className="alert-action-btn investigate"
                                        onClick={() => handleInvestigate(alert)}
                                    >
                                        🔍 Investigate
                                    </button>
                                    <button
                                        className="alert-action-btn resolve"
                                        onClick={() => handleResolve(alert)}
                                    >
                                        ✓ Mark Resolved
                                    </button>
                                </div>
                            </div>
                        );
                    })
                )}
            </div>

            {/* Investigation Modal */}
            {investigatingAlert && (
                <div className="modal-overlay" onClick={() => setInvestigatingAlert(null)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>🔍 Alert Investigation</h2>
                            <button className="modal-close" onClick={() => setInvestigatingAlert(null)}>✕</button>
                        </div>
                        <div className="modal-body">
                            <div className="investigation-section">
                                <h3>Event Details</h3>
                                <div className="investigation-item">
                                    <strong>Full Event:</strong>
                                    <p>{investigatingAlert.event}</p>
                                </div>
                                <div className="investigation-item">
                                    <strong>Prediction:</strong>
                                    <span className={`badge badge-${investigatingAlert.prediction}`}>
                                        {investigatingAlert.prediction.toUpperCase()}
                                    </span>
                                </div>
                                <div className="investigation-item">
                                    <strong>Confidence Score:</strong>
                                    <p>{(investigatingAlert.score * 100).toFixed(2)}%</p>
                                </div>
                                <div className="investigation-item">
                                    <strong>Timestamp:</strong>
                                    <p>{new Date(investigatingAlert.timestamp).toLocaleString()}</p>
                                </div>
                                {role !== 'normal_user' && investigatingAlert.user_email && (
                                    <div className="investigation-item">
                                        <strong>User:</strong>
                                        <p>{investigatingAlert.user_email}</p>
                                    </div>
                                )}
                                <div className="investigation-item">
                                    <strong>Processed Sequence:</strong>
                                    <p className="sequence-text">{investigatingAlert.sequence}</p>
                                </div>
                            </div>

                            <div className="investigation-section">
                                <h3>Recommended Actions</h3>
                                <ul className="action-list">
                                    {investigatingAlert.prediction === 'malicious' ? (
                                        <>
                                            <li>🚨 Immediately isolate affected system</li>
                                            <li>🔒 Disable user account if compromised</li>
                                            <li>📋 Review recent activity logs</li>
                                            <li>🔍 Conduct forensic analysis</li>
                                            <li>📞 Notify security team</li>
                                        </>
                                    ) : (
                                        <>
                                            <li>⚠️ Monitor user activity closely</li>
                                            <li>📊 Review related logs</li>
                                            <li>🔍 Investigate source IP/location</li>
                                            <li>📝 Document findings</li>
                                        </>
                                    )}
                                </ul>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button className="btn btn-secondary" onClick={() => setInvestigatingAlert(null)}>
                                Close
                            </button>
                            <button
                                className="btn btn-danger"
                                onClick={() => {
                                    handleResolve(investigatingAlert);
                                    setInvestigatingAlert(null);
                                }}
                            >
                                Mark Resolved
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Alerts;
