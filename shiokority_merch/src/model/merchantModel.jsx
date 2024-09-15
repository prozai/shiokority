import axios from 'axios';

class Merchant {
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
  // Merchant login method
  // # 131
  static async login(data) {
    try {
      const response = await axios.post('/login', data, { withCredentials: true });
      localStorage.setItem('merchant_token', response.data.token); // Assuming the API returns a token
      return response.data;
    } catch (error) {
      throw new Error('Invalid email or password');
    }
  }

  // Merchant logout method
  // # 132
  static async logout() {
    try {
      await axios.post('/logout', {}, { withCredentials: true });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('merchant_token');
    }
  }

  // Check if merchant is logged in
  static isLoggedIn() {
    return !!localStorage.getItem('merchant_token');
  }

  // Get the merchant's profile details
  static async getProfile() {
    try {
      const response = await axios.get('/profile', { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Update merchant details
  static async updateProfile(data) {
    try {
      const response = await axios.put('/update', data, { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Unable to update profile');
    }
  }
  // Send payment to merchant (API call)
  static async processPayment(merch_email, amount) {
    try {
      const response = await axios.post('/bankpage', {merch_email,amount});
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to process payment');
    }
  }

  // Fetch the merchant's transaction history
  static async getTransactionHistory() {
    try {
      const merch_id = localStorage.getItem('merch_id'); // Fetch merch_id from localStorage
      if (!merch_id) {
        throw new Error('Merchant ID is missing.');
      }
      
      const response = await axios.get(`/merchant/transactions?merch_id=${merch_id}`, { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch transaction history and balance');
    }
  }
}

export default Merchant;