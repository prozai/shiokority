import axios from 'axios';

class Merchant {
  // Merchant login method
  // # 131
  static async login(data) {
    try {
      const response = await axios.post('/login', data, { withCredentials: true });
      localStorage.setItem('merchant_token', response.data.token); // Assuming the API returns a token
      return response.data;
    } catch (error) {
      throw new Error('Wrong email or password');
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
}

export default Merchant;