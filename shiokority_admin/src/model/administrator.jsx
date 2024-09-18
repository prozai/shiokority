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

  //My work of art
  static async addUser(data) {
    const response = await axios.post('/admin/add-user', data); 
    if (response.status !== 200){
      throw new Error(response.data.message || "Adding of user failed!");
    }
    return response.data;
  }

  // Fetch all users from the backend
  static async getAllUsers() {
    try {
      const response = await axios.get('/admin/get-users'); // Updated endpoint
      return response.data;
    } catch (error) {
      console.error('Error fetching users (2): ', error); // Updated error message
      throw error;
    }
  }

  static async updateUser(userId, userData) {
    try {
      const response = await axios.put(`/admin/users/${userId}/update`, userData);  // Updated endpoint for editing user
      return response.data;
    } catch (error) {
      throw new Error('Error updating user details');
    }
  }

  
}

export default Administrator;