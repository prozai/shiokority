import axios from 'axios';

class Merchant {
  // Register a new merchant
  // # 130
  static async registerMerchant(merch_data) {
    try {
      const response = await axios.post('merchant/register', merch_data);  // Updated path
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }
  // Merchant login method
  // # 131
  static async login(data) {
    try {
      const response = await axios.post('merchant/login', data, { withCredentials: true });
      localStorage.setItem('merch_token', response.data.token); // Assuming the API returns a token
      localStorage.setItem('merch_id', response.data.merchant.merch_id); // Store merchant ID after login
      return response.data;
    } catch (error) {
      throw new Error('Invalid email or password');
    }
  }

  // Merchant logout method
  // # 132
  static async logout() {
    try {
      await axios.post('merchant/logout', {}, { withCredentials: true });
      localStorage.removeItem('merch_token');
      localStorage.setItem('merch_id');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  // Check if merchant is logged in
  static isLoggedIn() {
    return !!localStorage.getItem('merch_token');
  }

  // Get the merchant's profile details
  static async getProfile() {
    try {
      const response = await axios.get('merchant/profile', { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Update merchant details
  static async updateProfile(data) {
    try {
      const response = await axios.put('merchant/update', data, { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Unable to update profile');
    }
  }
  // Send payment to merchant (API call)
  static async processPayment(merch_email, amount) {
    try {
      const response = await axios.post('merchant/bankpage', {merch_email,amount});
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to process payment');
    }
  }

  // Fetch the merchant's transaction history
  static async getTransactionHistory() {
    try {
      const response = await axios.get("merchant/transactions");
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch transaction history and balance');
    }
  }
}

export default Merchant;