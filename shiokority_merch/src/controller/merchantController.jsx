import axios from 'axios';

class merchantController {
  // Register a new merchant
  // # 130
  static async registerMerchant(merch_data) {
    try {
      const response = await axios.post('/register-merchant', merch_data);  // Updated path
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  // Merchant login
  // # 131
  static async login(data) {
    try {
      const response = await axios.post('/login', data, { withCredentials: true });
      localStorage.setItem('merchant_token', response.data.token);
      return response.data;
    } catch (error) {
      throw new Error('Invalid email or password');
    }
  }

  // Logout the merchant
  // # 132
  static async logout() {
    try {
      await axios.post('/logout', {}, { withCredentials: true });
      localStorage.removeItem('merchant_token');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  // Get the merchant's profile
  static async getProfile() {
    try {
      const response = await axios.get('/profile', { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }
}

export default merchantController;