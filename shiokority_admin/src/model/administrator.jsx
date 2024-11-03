import axios from 'axios';
import { ADMIN_PREFIX } from '../constants';
// export const ADMIN_PREFIX = '/admin';
import api from '../services/api';
class Administrator {
    
  static async login(data) {
    try {
      const response = await api.post(`${ADMIN_PREFIX}/auth/login`, data);   
      
      if (response.data.success) {
        localStorage.setItem('isAdminLoggedIn', 'true');
        return response.data;
      }
      else {
        localStorage.setItem('isAdminLoggedIn', 'false');
        return response.data;
      }
    } catch (error) {
      throw new Error(error.response.data.message);
    }
  }

  static async logout() {
    try {
      await axios.post(`${ADMIN_PREFIX}/auth/logout`); // Assuming your API has a logout endpoint
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('isAdminLoggedIn');
    }
  }

  static async isLoggedIn() {
    try {
      return await axios.get(`${ADMIN_PREFIX}/auth/isLoggedIn`);
    } catch (error) {
      return false;
    }
  }

  static async verify2FA(code) {
    try {
      const response = await axios.post(`${ADMIN_PREFIX}/2fa/verify`, { code });
      return response.data;
    } catch (error) {
      throw new Error('Failed to verify 2FA');
    }
  }

  static async getQRcode() {
    try {
      const response = await axios.get(`${ADMIN_PREFIX}/getQRcode`, { responseType: 'blob' });
      return response.data;
    } catch (error) {
      throw new Error('Failed to get QR code');
    }
  }

  static async getSecretKey() {
    try {
      const response = await axios.get(`${ADMIN_PREFIX}/getSecretKey`);
      return response.data;
    } catch (error) {
      throw new Error('Failed to get secret key');
    }
  }


}

export default Administrator;