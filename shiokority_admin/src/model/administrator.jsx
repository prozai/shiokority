import axios from 'axios';

const ADMIN_PREFIX = '/admin';

class Administrator {
    
  static async login(data) {
    try {
      const response = await axios.post(`${ADMIN_PREFIX}/auth/login`, data);      
      localStorage.setItem('token', response.data.token);
      return response.data;
    } catch (error) {
      throw new Error('Wrong email or password');
    }
  }

  static async logout() {
    try {
      await axios.post(`${ADMIN_PREFIX}/auth/logout`); // Assuming your API has a logout endpoint
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('token');
    }
  }

  static isLoggedIn() {
    return !!localStorage.getItem('token');
  }

  //My work of art
  static async addUser(data) {
    const response = await axios.post(`${ADMIN_PREFIX}/add-user`, data); 
    if (response.status !== 200){
      throw new Error(response.data.message || "Adding of user failed!");
    }
    return response.data;
  }

  // Fetch all users from the backend
  static async getAllUsers() {
    try {
      const response = await axios.get(`${ADMIN_PREFIX}/get-users`); // Updated endpoint
      return response.data;
    } catch (error) {
      console.error('Error fetching users (2): ', error); // Updated error message
      throw error;
    }
  }

  // Fetch a user by ID
  static async getUserById(cust_id) {
    try {
      const response = await axios.get(`${ADMIN_PREFIX}/get-user/${cust_id}`);
      if (response.status !== 200) {
        throw new Error('User not found');
      }
      return response.data;
    } catch (error) {
      console.error('Error fetching user by ID:', error);
      throw error;
    }
  }

  static async updateUser(userId, userData) {
    try {
      const response = await axios.put(`${ADMIN_PREFIX}/users/${userId}/update`, userData);  // Updated endpoint for editing user
      return response.data;
    } catch (error) {
      throw new Error('Error updating user details');
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