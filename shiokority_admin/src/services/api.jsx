// src/services/api.jsx
import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:5001/', // Change this to your EC2 URL in production
  withCredentials: true,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add a request interceptor to add token to all requests
api.interceptors.request.use(
  (config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
          config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
  },
  (error) => {
      return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried refreshing token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        // Add Authorization header with refresh token
        const response = await api.post('admin/auth/refresh', {}, {
          headers: {
            'Authorization': `Bearer ${refreshToken}`  // Send refresh token in header
          }
        });
        
        if (response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token);
          api.defaults.headers['Authorization'] = `Bearer ${response.data.access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;