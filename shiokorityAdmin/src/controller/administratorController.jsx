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

}

export default AdministratorController;