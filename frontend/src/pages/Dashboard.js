import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './Dashboard.css';

function Dashboard() {
    const [stats, setStats] = useState({ total: 0, normal: 0, suspicious: 0, malicious: 0 });
    const [logs, setLogs] = useState([]);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview');
    const [showCreateUser, setShowCreateUser] = useState(false);
    const [newUser, setNewUser] = useState({ email: '', role: 'normal_user' });
    const [tempPassword, setTempPassword] = useState('');
    const navigate = useNavigate();

    const email = localStorage.getItem('email');
    const role = localStorage.getItem('role');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [statsRes, logsRes] = await Promise.all([
                api.get('/statistics'),
                role === 'normal_user' ? api.get('/logs/me?limit=50') : api.get('/logs?limit=50')
            ]);

            setStats(statsRes.data.statistics);
            setLogs(logsRes.data.logs);

            // Fetch users if admin
            if (role === 'admin') {
                const usersRes = await api.get('/admin/users');
                setUsers(usersRes.data.users);
            }

            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            if (error.response?.status === 401) {
                localStorage.clear();
                navigate('/login');
            }
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    const handleCreateUser = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/admin/users/create', newUser);
            if (response.data.success) {
                setTempPassword(response.data.temporary_password);
                setNewUser({ email: '', role: 'normal_user' });
                fetchData();
            }
        } catch (error) {
            alert(error.response?.data?.message || 'Failed to create user');
        }
    };

    const getRoleIcon = (userRole) => {
        switch (userRole) {
            case 'admin': return '👑';
            case 'soc_analyst': return '🔍';
            default: return '👤';
        }
    };

    const getRoleName = (userRole) => {
        switch (userRole) {
            case 'admin': return 'Admin';
            case 'soc_analyst': return 'SOC Analyst';
            default: return 'Normal User';
        }
    };

    const handleClearAllLogs = async () => {
        const confirmed = window.confirm(
            '⚠️ WARNING: This will permanently delete ALL logs from the database!\n\n' +
            'This action cannot be undone.\n\n' +
            'Are you sure you want to continue?'
        );

        if (confirmed) {
            const doubleConfirm = window.confirm(
                '🚨 FINAL CONFIRMATION\n\n' +
                'You are about to delete ALL logs.\n\n' +
                'Click OK to proceed with deletion.'
            );

            if (doubleConfirm) {
                try {
                    setLoading(true);
                    const response = await api.delete('/logs/clear/all');
                    if (response.success) {
                        alert(`✅ Successfully deleted ${response.deleted_count} logs`);
                        fetchData(); // Refresh data
                    }
                } catch (error) {
                    alert(error.response?.data?.message || 'Failed to clear logs');
                } finally {
                    setLoading(false);
                }
            }
        }
    };

    if (loading) {
        return (
            <div className="dashboard-loading">
                <div className="spinner"></div>
                <p>Loading Dashboard...</p>
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            {/* Sidebar */}
            <aside className="dashboard-sidebar">
                <div className="sidebar-header">
                    <div className="logo">
                        <span className="logo-icon">🛡️</span>
                        <span className="logo-text">CyberGuard</span>
                    </div>
                    <div className="user-badge">
                        <span className="user-icon">{getRoleIcon(role)}</span>
                        <div className="user-info">
                            <div className="user-email">{email}</div>
                            <div className="user-role">{getRoleName(role)}</div>
                        </div>
                    </div>
                </div>

                <nav className="sidebar-nav">
                    <button
                        className={`nav-item ${activeTab === 'overview' ? 'active' : ''}`}
                        onClick={() => setActiveTab('overview')}
                    >
                        <span className="nav-icon">📊</span>
                        <span>Overview</span>
                    </button>

                    <button
                        className={`nav-item ${activeTab === 'logs' ? 'active' : ''}`}
                        onClick={() => setActiveTab('logs')}
                    >
                        <span className="nav-icon">📝</span>
                        <span>{role === 'normal_user' ? 'My Logs' : 'All Logs'}</span>
                    </button>

                    <button
                        className={`nav-item ${activeTab === 'alerts' ? 'active' : ''}`}
                        onClick={() => navigate('/alerts')}
                    >
                        <span className="nav-icon">🚨</span>
                        <span>Alerts</span>
                    </button>

                    <button
                        className="nav-item"
                        onClick={() => navigate('/analyze')}
                    >
                        <span className="nav-icon">🔍</span>
                        <span>Analyze Logs</span>
                    </button>

                    {role === 'admin' && (
                        <button
                            className={`nav-item ${activeTab === 'users' ? 'active' : ''}`}
                            onClick={() => setActiveTab('users')}
                        >
                            <span className="nav-icon">👥</span>
                            <span>User Management</span>
                        </button>
                    )}

                    <button className="nav-item nav-logout" onClick={handleLogout}>
                        <span className="nav-icon">🚪</span>
                        <span>Logout</span>
                    </button>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="dashboard-main">
                <header className="dashboard-header">
                    <div>
                        <h1>Security Dashboard</h1>
                        <p className="dashboard-subtitle">Real-time Threat Intelligence & Behaviour Analytics</p>
                    </div>
                    <div className="header-actions">
                        <div className="live-indicator">
                            <span className="pulse-dot"></span>
                            <span>Live</span>
                        </div>
                    </div>
                </header>

                {/* Overview Tab */}
                {activeTab === 'overview' && (
                    <div className="dashboard-content fade-in">
                        {/* Stats Cards */}
                        <div className="stats-grid">
                            <div className="stat-card">
                                <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' }}>
                                    📊
                                </div>
                                <div className="stat-details">
                                    <div className="stat-label">Total Logs</div>
                                    <div className="stat-value">{stats.total.toLocaleString()}</div>
                                </div>
                            </div>

                            <div className="stat-card">
                                <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}>
                                    ✓
                                </div>
                                <div className="stat-details">
                                    <div className="stat-label">Normal</div>
                                    <div className="stat-value">{stats.normal.toLocaleString()}</div>
                                </div>
                            </div>

                            <div className="stat-card">
                                <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' }}>
                                    ⚠️
                                </div>
                                <div className="stat-details">
                                    <div className="stat-label">Suspicious</div>
                                    <div className="stat-value">{stats.suspicious.toLocaleString()}</div>
                                </div>
                            </div>

                            <div className="stat-card">
                                <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' }}>
                                    🚨
                                </div>
                                <div className="stat-details">
                                    <div className="stat-label">Malicious</div>
                                    <div className="stat-value">{stats.malicious.toLocaleString()}</div>
                                </div>
                            </div>
                        </div>

                        {/* Charts */}
                        <div className="charts-grid">
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">Threat Distribution</h3>
                                </div>
                                <div className="chart-container">
                                    <div className="donut-chart">
                                        <svg viewBox="0 0 200 200" className="donut-svg">
                                            <circle cx="100" cy="100" r="80" fill="none" stroke="var(--status-normal)" strokeWidth="30" strokeDasharray={`${(stats.normal / stats.total) * 502.4} 502.4`} transform="rotate(-90 100 100)" />
                                            <circle cx="100" cy="100" r="80" fill="none" stroke="var(--status-suspicious)" strokeWidth="30" strokeDasharray={`${(stats.suspicious / stats.total) * 502.4} 502.4`} strokeDashoffset={`-${(stats.normal / stats.total) * 502.4}`} transform="rotate(-90 100 100)" />
                                            <circle cx="100" cy="100" r="80" fill="none" stroke="var(--status-malicious)" strokeWidth="30" strokeDasharray={`${(stats.malicious / stats.total) * 502.4} 502.4`} strokeDashoffset={`-${((stats.normal + stats.suspicious) / stats.total) * 502.4}`} transform="rotate(-90 100 100)" />
                                        </svg>
                                        <div className="donut-center">
                                            <div className="donut-value">{stats.total}</div>
                                            <div className="donut-label">Total Events</div>
                                        </div>
                                    </div>
                                    <div className="chart-legend">
                                        <div className="legend-item">
                                            <span className="legend-color" style={{ background: 'var(--status-normal)' }}></span>
                                            <span>Normal ({Math.round((stats.normal / stats.total) * 100)}%)</span>
                                        </div>
                                        <div className="legend-item">
                                            <span className="legend-color" style={{ background: 'var(--status-suspicious)' }}></span>
                                            <span>Suspicious ({Math.round((stats.suspicious / stats.total) * 100)}%)</span>
                                        </div>
                                        <div className="legend-item">
                                            <span className="legend-color" style={{ background: 'var(--status-malicious)' }}></span>
                                            <span>Malicious ({Math.round((stats.malicious / stats.total) * 100)}%)</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">Recent Activity</h3>
                                </div>
                                <div className="activity-list">
                                    {logs.slice(0, 5).map((log, index) => (
                                        <div key={index} className="activity-item">
                                            <div className={`activity-indicator ${log.prediction}`}></div>
                                            <div className="activity-content">
                                                <div className="activity-text">{log.event.substring(0, 60)}...</div>
                                                <div className="activity-meta">
                                                    <span className={`badge badge-${log.prediction}`}>{log.prediction}</span>
                                                    <span className="activity-time">{new Date(log.timestamp).toLocaleTimeString()}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Logs Tab */}
                {activeTab === 'logs' && (
                    <div className="dashboard-content fade-in">
                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">{role === 'normal_user' ? 'My Logs' : 'All System Logs'}</h3>
                                <div className="card-actions">
                                    <span className="text-muted">{logs.length} entries</span>
                                    {role === 'admin' && logs.length > 0 && (
                                        <button
                                            className="btn btn-danger btn-sm"
                                            onClick={handleClearAllLogs}
                                            style={{ marginLeft: '1rem' }}
                                        >
                                            🗑️ Clear All Logs
                                        </button>
                                    )}
                                </div>
                            </div>
                            <div className="table-container">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>Timestamp</th>
                                            <th>Event</th>
                                            <th>Prediction</th>
                                            <th>Score</th>
                                            {role !== 'normal_user' && <th>User</th>}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {logs.map((log, index) => (
                                            <tr key={index}>
                                                <td>{new Date(log.timestamp).toLocaleString()}</td>
                                                <td className="log-event">{log.event}</td>
                                                <td>
                                                    <span className={`badge badge-${log.prediction}`}>{log.prediction}</span>
                                                </td>
                                                <td>{(log.score * 100).toFixed(1)}%</td>
                                                {role !== 'normal_user' && <td>{log.user_email || 'System'}</td>}
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}

                {/* Users Tab (Admin Only) */}
                {activeTab === 'users' && role === 'admin' && (
                    <div className="dashboard-content fade-in">
                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">User Management</h3>
                                <button className="btn btn-primary" onClick={() => setShowCreateUser(!showCreateUser)}>
                                    + Create User
                                </button>
                            </div>

                            {showCreateUser && (
                                <div className="create-user-form">
                                    <form onSubmit={handleCreateUser}>
                                        <div className="form-row">
                                            <div className="input-group">
                                                <label className="input-label">Email</label>
                                                <input
                                                    type="email"
                                                    className="input"
                                                    value={newUser.email}
                                                    onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                                                    placeholder="user@company.com"
                                                    required
                                                />
                                            </div>
                                            <div className="input-group">
                                                <label className="input-label">Role</label>
                                                <select
                                                    className="select"
                                                    value={newUser.role}
                                                    onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                                                >
                                                    <option value="normal_user">Normal User</option>
                                                    <option value="soc_analyst">SOC Analyst</option>
                                                    <option value="admin">Admin</option>
                                                </select>
                                            </div>
                                            <button type="submit" className="btn btn-success">Create</button>
                                        </div>
                                    </form>

                                    {tempPassword && (
                                        <div className="temp-password-alert">
                                            <strong>⚠️ Temporary Password:</strong> {tempPassword}
                                            <p>Please share this with the user. They will be required to reset it on first login.</p>
                                        </div>
                                    )}
                                </div>
                            )}

                            <div className="table-container">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>Email</th>
                                            <th>Role</th>
                                            <th>Created</th>
                                            <th>Last Login</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {users.map((user, index) => (
                                            <tr key={index}>
                                                <td>{user.email}</td>
                                                <td>
                                                    <span className="role-badge">
                                                        {getRoleIcon(user.role)} {getRoleName(user.role)}
                                                    </span>
                                                </td>
                                                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                                                <td>{user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</td>
                                                <td>
                                                    {user.require_password_reset ? (
                                                        <span className="badge badge-suspicious">Reset Required</span>
                                                    ) : (
                                                        <span className="badge badge-normal">Active</span>
                                                    )}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default Dashboard;
