import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests if available
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Handle responses and errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth functions
export const auth = {
    login: async (username, password) => {
        const response = await api.post('/auth/login/', { username, password });
        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    },
    
    register: async (userData) => {
        const response = await api.post('/auth/register/', userData);
        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    },
    
    logout: async () => {
        try {
            await api.post('/auth/logout/');
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        }
    },
    
    getProfile: async () => {
        const response = await api.get('/auth/profile/');
        return response.data;
    },
    
    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },
    
    getUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
};

// Data functions
export const data = {
    uploadFile: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await axios.post(`${API_URL}/upload/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Token ${localStorage.getItem('token')}`
            }
        });
        return response.data;
    },
    
    getHistory: async () => {
        const response = await api.get('/history/');
        return response.data;
    },
    
    getSummary: async (batchId) => {
        const response = await api.get(`/summary/${batchId}/`);
        return response.data;
    },
    
    downloadReport: async (batchId, filename) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/report/${batchId}/`, {
                headers: {
                    'Authorization': `Token ${token}`
                },
                responseType: 'blob',
            });
            
            // Create a blob URL and trigger download
            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename || `report_${batchId}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            
            return true;
        } catch (error) {
            console.error('Error downloading PDF:', error);
            if (error.response?.status === 404) {
                throw new Error('Report not found');
            } else if (error.response?.status === 401) {
                throw new Error('Authentication required');
            } else {
                throw new Error('Failed to download report');
            }
        }
    }
};

export default api;
