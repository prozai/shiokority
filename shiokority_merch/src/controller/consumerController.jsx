import Consumer from '../model/consumerModel';

class consumerController {
  // Register consumer
  static async registerConsumer(cust_data) {
    try {
      return await Consumer.registerConsumer(cust_data);
    } catch (error) {
      throw new Error(error.message || 'Registration failed');
    }
  }

  // Login consumer
  static async loginConsumer(data) {
    return await Consumer.loginConsumer(data);
  }

  // Logout consumer
  static async logoutConsumer() {
    return await Consumer.logoutConsumer();
  }

  // Get consumer profile
  static async getProfileConsumer() {
    try {
      return await Consumer.getProfileConsumer();
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Send payment to merchant
  static async sendPayment(cust_email, merch_email, merch_amount) {
    try {
      return await Consumer.sendPayment(cust_email, merch_email, merch_amount);
    } catch (error) {
      throw new Error('Payment failed');
    }
  }
}

export default consumerController;