import api from '../services/api';

class Consumer {
  // Register a new consumer
  static async registerConsumer(cust_data) {
    try {
      const response = await api.post('/consumer/register-consumer', cust_data);  // Assuming the backend API endpoint
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  // Login consumer
  static async loginConsumer(data) {
    try {
      const response = await api.post('/consumer/login-consumer', data);
      localStorage.setItem('isConsumerLoggedIn', response.data.success); 
      localStorage.setItem('access_token', response.data.access_token); // Save token or session management
      localStorage.setItem('refresh_token', response.data.refresh_token); 
      localStorage.setItem('cust_id', response.data.customer.cust_id);
      return response.data;
    } catch (error) {
      throw new Error('Invalid email or password');
    }
  }

  static async logoutConsumer() {
    try {
      await api.post('/consumer/logout-consumer', {});
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('cust_id');
      localStorage.removeItem('isConsumerLoggedIn');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }


  // Fetch consumer profile details
  static async getProfileConsumer() {
    try {
      const response = await api.get('/consumer/profile-consumer');
      return response.data;
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Send payment to merchant (API call)
  static async sendPayment(cust_email, amount, cardNumber, expiryDate, cvv, uen) {
    try {
      const response = await api.post(`/consumer/send-payment`, { cust_email, amount, cardNumber, expiryDate, cvv, uen});
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to send payment');
    }
  }

  //Added by lu
  static async getMerchantData() {
    try {
      const response = await api.get('/consumer/view-merchant');
      return response.data;
      // Map only the merchant IDs
      // return merchantsData.map((merchant) => merchant.merch_id);
    } catch (error) {
      console.error('Error fetching merchant data:', error);
      throw new Error('Failed to fetch merchant data');
    }
  }

}

export default Consumer;