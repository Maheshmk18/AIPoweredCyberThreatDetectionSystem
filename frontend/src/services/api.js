import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Authentication
export const authService = {
    register: async (email, password) => {
        const response = await api.post('/auth/register', { email, password });
        return response.data;
    },

    login: async (email, password) => {
        const response = await api.post('/auth/login', { email, password });
        if (response.data.success && response.data.token) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('email', response.data.email);
        }
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('email');
    },

    verifyToken: async () => {
        try {
            const response = await api.get('/auth/verify');
            return response.data;
        } catch (error) {
            return { success: false };
        }
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },

    getCurrentUser: () => {
        return localStorage.getItem('email');
    },
};

// Log Analysis
export const logService = {
    analyzeText: async (text) => {
        const response = await api.post('/analyze/text', { text });
        return response.data;
    },

    analyzeFile: async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post('/analyze/file', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    getAllLogs: async (limit = 100) => {
        const response = await api.get(`/logs?limit=${limit}`);
        return response.data;
    },

    getMaliciousLogs: async (limit = 50) => {
        const response = await api.get(`/logs/malicious?limit=${limit}`);
        return response.data;
    },

    getLogsByPrediction: async (prediction, limit = 100) => {
        const response = await api.get(`/logs/filter/${prediction}?limit=${limit}`);
        return response.data;
    },

    getStatistics: async () => {
        const response = await api.get('/statistics');
        return response.data;
    },

    deleteLog: async (logId) => {
        const response = await api.delete(`/logs/${logId}`);
        return response.data;
    },

    clearAllLogs: async () => {
        const response = await api.delete('/logs/clear/all');
        return response.data;
    },
};

export default api;
