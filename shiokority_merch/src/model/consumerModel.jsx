import axios from 'axios';

class Consumer {
  // Register a new consumer
  static async registerConsumer(cust_data) {
    try {
      const response = await axios.post('consumer/register-consumer', cust_data);  // Assuming the backend API endpoint
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  // Login consumer
  static async loginConsumer(data) {
    try {
      const response = await axios.post('consumer/login-consumer', data, { withCredentials: true });
      localStorage.setItem('cust_token', response.data.token); // Save token or session management
      localStorage.setItem('cust_id', response.data.customer.cust_id);
      return response.data;
    } catch (error) {
      throw new Error('Invalid email or password');
    }
  }

  static async logoutConsumer() {
    try {
      await axios.post('consumer/logout-consumer', {}, { withCredentials: true });
      localStorage.removeItem('cust_token');
      localStorage.setItem('cust_id');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  // Check if consumer is logged in
  static isLoggedIn() {
    return !!localStorage.getItem('cust_token');
  }

  // Fetch consumer profile details
  static async getProfileConsumer() {
    try {
      const response = await axios.get('consumer/profile-consumer', { withCredentials: true });
      return response.data;
    } catch (error) {
      throw new Error('Unable to fetch profile');
    }
  }

  // Send payment to merchant (API call)
  static async sendPayment(cust_email, amount, cardNumber, expiryDate, cvv, uen) {
    try {
      const response = await axios.post('consumer/send-payment', { cust_email, amount, cardNumber, expiryDate, cvv, uen});
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to send payment');
    }
  }

  //Added by lu
  static async getMerchantData() {
    try {
      const response = await fetch('/consumer/view-merchant');
      // const merchantsData = await response.json();
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