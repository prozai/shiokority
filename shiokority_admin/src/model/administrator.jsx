import axios from 'axios';

class Administrator {
  
  static async login(data) {
    try {
      const response = await axios.post('/login/admin', data);      
      localStorage.setItem('token', response.data.token);
      return response.data;
    } catch (error) {
      throw new Error('Wrong email or password');
    }
  }

  static async logout() {
    try {
      await axios.post('/logout/admin'); // Assuming your API has a logout endpoint
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('token');
    }
  }

  static isLoggedIn() {
    return !!localStorage.getItem('token');
  }

  
}

export default Administrator;