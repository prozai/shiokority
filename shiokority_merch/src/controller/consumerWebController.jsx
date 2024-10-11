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
  static async loginConsumer(data) {
    return await consumerWeb.loginConsumer(data);
  }

  // Logout consumer
  static async logoutConsumer() {
    return await consumerWeb.logoutConsumer();
  }

  // Get consumer profile
  static async getProfileConsumer() {
    try {
      return await consumerWeb.getProfileConsumer();
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