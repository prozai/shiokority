// src/services/api.jsx
import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: '', // Change this to your EC2 URL in production
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;