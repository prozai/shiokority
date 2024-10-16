import Administrator from '../model/administrator';
import Merchant from '../model/merchant';  
import Consumer from '../model/consumer';

class AdministratorController {
  static async login(data) {
    return Administrator.login(data);
  }

  static async logout() {
    return Administrator.logout();
  }

  static isLoggedIn() {
    return Administrator.isLoggedIn();
  }

  static async createMerchant(data) {
    try {
      const result = await Merchant.createMerchant(data);
      return result;
    } catch (error) {
      console.error('Error in createMerchant:', error);
      throw error;
    }
  }

  static async getMerchantData() {
    return await Merchant.getMerchantData();
  }

  static async fetchMerchantById(merchId) {
    try {
      return await Merchant.fetchMerchantById(merchId);
    } catch (error) {
      throw error;
    }
  }

  static async updateMerchant(merchId, merchantData) {
    try {
      return await Merchant.updateMerchant(merchId, merchantData);
    } catch (error) {
      throw error;
    }
  }

  static async updateMerchantStatus(merch_id, status) {
    try {
      return await Merchant.updateMerchantStatus(merch_id, status);
    } catch (error) {
      throw error;
    }
  }

  // My work of art
  static async addUser(data) {
    try {
      const result = await Consumer.addUser(data);  // Calls the model method to add user
      return result;
    } catch (error) {
      console.error('Error in createUser:', error);
      throw error;
    }
  }

  static async getAllUsers() {
    try {
      const users = await Consumer.getAllUsers();  // Fetches all users from the model
      return users;
    } catch (error) {
      console.error('Error in getUsers:', error);
      throw error;
    }
  }

  // Fetch user by ID
  static async getUserById(cust_id) {
    try {
      const user = await Consumer.getUserById(cust_id);  // Fetch user details from the model
      return user;
    } catch (error) {
      console.error('Error in getUserById:', error);
      throw error;
    }
  }

  static async updateUser(userId, userData) {
    try {
      const result = await Consumer.updateUser(userId, userData);  // Calls the model method to update the user
      return result;
    } catch (error) {
      console.error('Error in updateUser:', error);
      throw error;
    }
  }

  static async verify2FA(code) {
    return await Administrator.verify2FA(code);
  }

  static async getQRcode() {
    return await Administrator.getQRcode();
  }

  static async getSecretKey() {
    return await Administrator.getSecretKey();
  }

}

export default AdministratorController;