import Consumer from '../model/consumerWebModel';

class consumerController {
  // Register consumer
  static async registerConsumer(consumer_data) {
    try {
      return await Consumer.registerConsumer(consumer_data);
    } catch (error) {
      throw new Error(error.message || 'Registration failed');
    }
  }

  // Login consumer
  static async login(data) {
    return await Consumer.login(data);
  }

  // Get consumer profile
  static async getProfile() {
    try {
      return await Consumer.getProfile();
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Send payment to merchant
  static async sendPayment(merch_email, amount) {
    try {
      return await Consumer.sendPayment(merch_email, amount);
    } catch (error) {
      throw new Error('Payment failed');
    }
  }
}

export default consumerController;