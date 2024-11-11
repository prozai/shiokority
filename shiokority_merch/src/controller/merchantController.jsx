import Merchant from '../model/merchantModel';

class merchantController {
  // Register a new merchant
  // # 130
  static async registerMerchant(merch_data) {
    try {
      return await Merchant.registerMerchant(merch_data);
    } catch (error) {
      throw new Error(error.message || 'Registration failed');
    }
  }

  // Merchant login
  // # 131
  static async login(data) {
    return await Merchant.login(data);
  }

  // Logout the merchant
  // # 132
  static async logout() {
    return await Merchant.logout();
  }

  // Get the merchant's profile
  static async getProfile() {
    try {
      return await Merchant.getProfile();
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Handle fetching merchant transactions and balance
  static async getTransactionHistory() {
    return await Merchant.getTransactionHistory();
  }
}

export default merchantController;