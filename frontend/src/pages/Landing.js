import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Landing.css';

function Landing() {
    const navigate = useNavigate();
    const [scrollY, setScrollY] = useState(0);

    useEffect(() => {
        const handleScroll = () => setScrollY(window.scrollY);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const scrollToSection = (id) => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <div className="landing-container">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-background">
                    <div className="cyber-grid"></div>
                    <div className="floating-particles"></div>
                </div>

                <nav className="landing-nav">
                    <div className="nav-logo">
                        <span className="logo-icon">🛡️</span>
                        <span className="logo-text">CyberGuard</span>
                    </div>
                    <div className="nav-links">
                        <a onClick={() => scrollToSection('features')}>Features</a>
                        <a onClick={() => scrollToSection('how-it-works')}>How It Works</a>
                        <a onClick={() => scrollToSection('technology')}>Technology</a>
                        <button className="nav-login-btn" onClick={() => navigate('/login')}>
                            Login
                        </button>
                    </div>
                </nav>

                <div className="hero-content">
                    <div className="hero-badge">
                        <span className="badge-icon">🤖</span>
                        <span>AI-Powered Threat Detection</span>
                    </div>

                    <h1 className="hero-title">
                        Protect Your Digital Assets with
                        <span className="gradient-text"> AI Intelligence</span>
                    </h1>

                    <p className="hero-subtitle">
                        Advanced transformer-based cybersecurity system that detects, analyzes,
                        and responds to threats in real-time using cutting-edge machine learning.
                    </p>

                    <div className="hero-buttons">
                        <button className="btn-primary" onClick={() => navigate('/login')}>
                            <span>Get Started</span>
                            <span className="btn-arrow">→</span>
                        </button>
                        <button className="btn-secondary" onClick={() => scrollToSection('demo')}>
                            <span className="play-icon">▶</span>
                            <span>Watch Demo</span>
                        </button>
                    </div>

                    <div className="hero-stats">
                        <div className="stat-item">
                            <div className="stat-value">99.8%</div>
                            <div className="stat-label">Detection Accuracy</div>
                        </div>
                        <div className="stat-item">
                            <div className="stat-value">&lt;1s</div>
                            <div className="stat-label">Response Time</div>
                        </div>
                        <div className="stat-item">
                            <div className="stat-value">24/7</div>
                            <div className="stat-label">Monitoring</div>
                        </div>
                    </div>
                </div>

                <div className="scroll-indicator" onClick={() => scrollToSection('features')}>
                    <div className="mouse">
                        <div className="wheel"></div>
                    </div>
                    <span>Scroll to explore</span>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="features-section">
                <div className="section-header">
                    <span className="section-badge">Features</span>
                    <h2 className="section-title">Comprehensive Security Suite</h2>
                    <p className="section-subtitle">
                        Everything you need to protect your organization from cyber threats
                    </p>
                </div>

                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon">🤖</div>
                        <h3>AI-Powered Detection</h3>
                        <p>DistilBERT transformer model analyzes patterns and detects anomalies with 99.8% accuracy</p>
                        <div className="feature-tags">
                            <span>Machine Learning</span>
                            <span>Real-time</span>
                        </div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🚨</div>
                        <h3>Real-Time Alerts</h3>
                        <p>Instant email notifications for suspicious and malicious activities with detailed analysis</p>
                        <div className="feature-tags">
                            <span>Email Alerts</span>
                            <span>Instant</span>
                        </div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">📊</div>
                        <h3>Advanced Analytics</h3>
                        <p>Interactive dashboards with charts, statistics, and threat intelligence visualization</p>
                        <div className="feature-tags">
                            <span>Dashboards</span>
                            <span>Analytics</span>
                        </div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">👥</div>
                        <h3>Role-Based Access</h3>
                        <p>Granular permissions for Admin, SOC Analysts, and Users with complete access control</p>
                        <div className="feature-tags">
                            <span>RBAC</span>
                            <span>Security</span>
                        </div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🔍</div>
                        <h3>Threat Investigation</h3>
                        <p>Deep dive into alerts with recommended actions and forensic analysis capabilities</p>
                        <div className="feature-tags">
                            <span>Forensics</span>
                            <span>Analysis</span>
                        </div>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">📁</div>
                        <h3>Bulk Analysis</h3>
                        <p>Upload and analyze thousands of logs simultaneously with comprehensive reporting</p>
                        <div className="feature-tags">
                            <span>Batch Processing</span>
                            <span>Scalable</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section id="how-it-works" className="how-it-works-section">
                <div className="section-header">
                    <span className="section-badge">Process</span>
                    <h2 className="section-title">How CyberGuard Works</h2>
                    <p className="section-subtitle">
                        AI-powered threat detection in 4 simple steps
                    </p>
                </div>

                <div className="process-timeline">
                    <div className="process-step">
                        <div className="step-number">01</div>
                        <div className="step-content">
                            <h3>Data Collection</h3>
                            <p>System logs are collected from various sources and normalized for analysis</p>
                            <div className="step-visual">
                                <div className="data-flow">
                                    <div className="data-node">📝 Logs</div>
                                    <div className="flow-arrow">→</div>
                                    <div className="data-node">🔄 Process</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="process-step">
                        <div className="step-number">02</div>
                        <div className="step-content">
                            <h3>AI Analysis</h3>
                            <p>DistilBERT transformer model analyzes patterns and behavioral anomalies</p>
                            <div className="step-visual">
                                <div className="ai-brain">
                                    <div className="brain-node"></div>
                                    <div className="brain-node"></div>
                                    <div className="brain-node"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="process-step">
                        <div className="step-number">03</div>
                        <div className="step-content">
                            <h3>Threat Classification</h3>
                            <p>Activities are classified as Normal, Suspicious, or Malicious with confidence scores</p>
                            <div className="step-visual">
                                <div className="classification">
                                    <span className="class-badge normal">Normal</span>
                                    <span className="class-badge suspicious">Suspicious</span>
                                    <span className="class-badge malicious">Malicious</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="process-step">
                        <div className="step-number">04</div>
                        <div className="step-content">
                            <h3>Alert & Response</h3>
                            <p>Security team receives instant alerts with recommended actions for rapid response</p>
                            <div className="step-visual">
                                <div className="alert-animation">
                                    <span className="alert-icon">🚨</span>
                                    <span className="alert-text">Alert Sent</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Technology Section */}
            <section id="technology" className="technology-section">
                <div className="section-header">
                    <span className="section-badge">Technology</span>
                    <h2 className="section-title">Built with Cutting-Edge Tech</h2>
                    <p className="section-subtitle">
                        Powered by industry-leading technologies and frameworks
                    </p>
                </div>

                <div className="tech-stack">
                    <div className="tech-category">
                        <h3>AI & Machine Learning</h3>
                        <div className="tech-items">
                            <div className="tech-item">
                                <span className="tech-icon">🤖</span>
                                <span>DistilBERT</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">🔥</span>
                                <span>PyTorch</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">🤗</span>
                                <span>Transformers</span>
                            </div>
                        </div>
                    </div>

                    <div className="tech-category">
                        <h3>Backend</h3>
                        <div className="tech-items">
                            <div className="tech-item">
                                <span className="tech-icon">🐍</span>
                                <span>Python</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">⚡</span>
                                <span>Flask</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">🍃</span>
                                <span>MongoDB</span>
                            </div>
                        </div>
                    </div>

                    <div className="tech-category">
                        <h3>Frontend</h3>
                        <div className="tech-items">
                            <div className="tech-item">
                                <span className="tech-icon">⚛️</span>
                                <span>React</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">🎨</span>
                                <span>CSS3</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">📊</span>
                                <span>Recharts</span>
                            </div>
                        </div>
                    </div>

                    <div className="tech-category">
                        <h3>Security</h3>
                        <div className="tech-items">
                            <div className="tech-item">
                                <span className="tech-icon">🔐</span>
                                <span>JWT</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">🔒</span>
                                <span>Bcrypt</span>
                            </div>
                            <div className="tech-item">
                                <span className="tech-icon">👤</span>
                                <span>RBAC</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <div className="cta-content">
                    <h2>Ready to Secure Your Organization?</h2>
                    <p>Join thousands of companies protecting their digital assets with AI-powered security</p>
                    <button className="btn-cta" onClick={() => navigate('/login')}>
                        <span>Get Started Now</span>
                        <span className="btn-arrow">→</span>
                    </button>
                </div>
                <div className="cta-background">
                    <div className="cta-glow"></div>
                </div>
            </section>

            {/* Footer */}
            <footer className="landing-footer">
                <div className="footer-content">
                    <div className="footer-brand">
                        <span className="logo-icon">🛡️</span>
                        <span className="logo-text">CyberGuard</span>
                        <p>AI-Powered Threat Detection System</p>
                    </div>
                    <div className="footer-links">
                        <div className="footer-column">
                            <h4>Product</h4>
                            <a onClick={() => scrollToSection('features')}>Features</a>
                            <a onClick={() => scrollToSection('how-it-works')}>How It Works</a>
                            <a onClick={() => scrollToSection('technology')}>Technology</a>
                        </div>
                        <div className="footer-column">
                            <h4>Resources</h4>
                            <a href="#">Documentation</a>
                            <a href="#">API Reference</a>
                            <a href="#">Support</a>
                        </div>
                        <div className="footer-column">
                            <h4>Company</h4>
                            <a href="#">About Us</a>
                            <a href="#">Contact</a>
                            <a href="#">Privacy Policy</a>
                        </div>
                    </div>
                </div>
                <div className="footer-bottom">
                    <p>© 2024 CyberGuard. All rights reserved.</p>
                    <p>Built with ❤️ for cybersecurity</p>
                </div>
            </footer>
        </div>
    );
}

export default Landing;
