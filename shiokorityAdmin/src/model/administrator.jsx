import axios from 'axios';

class Administrator {
  static async login(email, password) {
    try {
      const response = await axios.post('/login/admin', { email, password });
      localStorage.setItem('token', response.data.token);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  static isLoggedIn() {
    return !!localStorage.getItem('token');
  }
  
}

export default Administrator;