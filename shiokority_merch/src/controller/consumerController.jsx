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
  static async sendPayment(cust_email, amount, cardNumber, expiryDate, cvv, uen) {
    try {
      return await Consumer.sendPayment(cust_email, amount, cardNumber, expiryDate, cvv, uen);  
    } catch (error) {
      throw new Error(error.message);
    }
  }

  //Added by lu
  static async getMerchantData() {
    try {
      const response = await fetch('/consumer/view-merchant');

      // Check if the response is OK (status code in the range 200-299)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Parse the JSON response
      const merchantsData = await response.json(); 

      // Check if merchantsData is an array
      if (!Array.isArray(merchantsData)) {
        throw new Error('Expected an array of merchants');
      }

      return merchantsData; // Return the array of merchant data
    } catch (error) {
      console.error('Error fetching merchant data:', error);
      throw new Error('Failed to fetch merchant data');
    }
  }

}

export default consumerController;