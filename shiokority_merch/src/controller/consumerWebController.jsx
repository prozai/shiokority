import consumerWeb from '../model/consumerWebModel';

class consumerController {
  // Register consumer
  static async registerConsumer(consumer_data) {
    try {
      return await consumerWeb.registerConsumer(consumer_data);
    } catch (error) {
      throw new Error(error.message || 'Registration failed');
    }
  }

  // Login consumer
  static async login(data) {
    return await consumerWeb.login(data);
  }

  // Get consumer profile
  static async getProfile() {
    try {
      return await consumerWeb.getProfile();
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Send payment to merchant
  static async sendPayment(merch_email, amount) {
    try {
      return await consumerWeb.sendPayment(merch_email, amount);
    } catch (error) {
      throw new Error('Payment failed');
    }
  }
}

export default consumerController;