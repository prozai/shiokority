import api from '../services/api';

class Merchant {
  // Register a new merchant
  // # 130
  static async registerMerchant(merch_data) {
    try {
      const response = await api.post('merchant/register-merchant', merch_data);  // Updated path
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }
  // Merchant login method
  // # 131
  static async login(data) {
    try {
      const response = await api.post('merchant/login', data, { withCredentials: true });
      localStorage.setItem('isMerchantLoggedIn', response.data.success); // Assuming the API returns a token
      localStorage.setItem('access_token', response.data.access_token); // Assuming the API returns a token
      localStorage.setItem('refresh_token', response.data.merchant.refresh_token); // Store merchant ID after login
      return response.data;
    } catch (error) {
      throw new Error('Invalid email or password');
    }
  }

  // Merchant logout method
  // # 132
  static async logout() {
    try {
      await api.post('merchant/logout', {});
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('isMerchantLoggedIn');
      
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  // Get the merchant's profile details
  static async getProfile() {
    try {
      const response = await api.get('merchant/profile');
      return response.data;
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Update merchant details
  static async updateProfile(data) {
    try {
      const response = await api.put('merchant/update', data);
      return response.data;
    } catch (error) {
      throw new Error('Unable to update profile');
    }
  }
  // Send payment to merchant (API call)
  static async processPayment(merch_email, amount) {
    try {
      const response = await api.post('merchant/bankpage', {merch_email,amount});
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to process payment');
    }
  }

  // Fetch the merchant's transaction history
  static async getTransactionHistory() {
    try {
      const response = await api.get("merchant/viewTransactionHistory");
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message);
    }
  }
}

export default Merchant;