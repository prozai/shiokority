import axios from 'axios';

class consumerWeb {
  // Register a new consumer
  static async registerConsumer(consumer_data) {
    try {
      const response = await axios.post('/api/register-consumer', consumer_data);  // Assuming the backend API endpoint
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  // Login consumer
  static async login(data) {
    try {
      const response = await axios.post('/api/login-consumer', data, { withCredentials: true });
      localStorage.setItem('consumer_token', response.data.token); // Save token or session management
      return response.data;
    } catch (error) {
      throw new Error('Invalid email or password');
    }
  }

  // Fetch consumer profile details
  static async getProfile() {
    try {
      const response = await axios.get('/api/consumer/profile', { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Send payment to merchant (API call)
  static async sendPayment(merch_email, amount) {
    try {
      const response = await axios.post('/api/consumer/send-payment', { merch_email, amount });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to send payment');
    }
  }
}

export default consumerWeb;