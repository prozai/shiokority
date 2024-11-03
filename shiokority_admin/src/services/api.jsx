// src/services/api.jsx
import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:5001', // Change this to your EC2 URL in production
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage if you have authentication
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

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle specific HTTP errors
      switch (error.response.status) {
        case 401:
          // Handle unauthorized
          console.log('Unauthorized access');
          // You might want to redirect to login page
          break;
        case 404:
          console.log('Resource not found');
          break;
        case 500:
          console.log('Server error');
          break;
        default:
          console.log('An error occurred');
      }
    } else if (error.request) {
      // Network error
      console.log('Network error');
    }
    return Promise.reject(error);
  }
);

export default api;