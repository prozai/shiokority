import axios from 'axios';

const ADMIN_PREFIX = '/admin';

class Consumer {

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

}

export default Consumer;