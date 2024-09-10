import Administrator from '../model/administrator';
import Merchant from '../model/merchant';  

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


}

export default AdministratorController;