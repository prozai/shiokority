import { ADMIN_PREFIX } from '../constants';
import api from '../services/api';

class Administrator {
    
  static async login(data) {
    try {
          
      const response = await api.post(`${ADMIN_PREFIX}/auth/login`, data);   
      
      if (response.data.success) {
        localStorage.setItem('isAdminLoggedIn', 'true');
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
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
      await api.post(`${ADMIN_PREFIX}/auth/logout`); // Assuming your API has a logout endpoint
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('isAdminLoggedIn');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  static async verify2FA(code) {
    try {
      const response = await api.post(`${ADMIN_PREFIX}/2fa/verify`, { code });
      return response.data;
    } catch (error) {
      throw new Error('Failed to verify 2FA');
    }
  }

  static async getQRcode() {
    try {
      const response = await api.get(`${ADMIN_PREFIX}/getQRcode`, { responseType: 'blob' });
      return response.data;
    } catch (error) {
      throw new Error('Failed to get QR code');
    }
  }

  static async getSecretKey() {
    try {
      const response = await api.get(`${ADMIN_PREFIX}/getSecretKey`);
      return response.data;
    } catch (error) {
      throw new Error('Failed to get secret key');
    }
  }


}

export default Administrator;