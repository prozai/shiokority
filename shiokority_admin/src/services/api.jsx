// src/services/api.jsx
import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: 'https://api.shiokority.online', // Change this to your EC2 URL in production
  withCredentials: true,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'keep-alive': true
  }
});

export default api;