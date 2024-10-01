import axios from 'axios';


class Merchant {

  constructor(merch_id, merch_name, merch_phone, merch_email, date_created, date_updated_on, status) {
    this.merch_id = merch_id;
    this.merch_name = merch_name;
    this.merch_phone = merch_phone;
    this.merch_email = merch_email;
    this.date_created = date_created;
    this.date_updated_on = date_updated_on;
    this.status = status;
  }

  static async createMerchant(merchantData) {
    const response = await axios.post('/create-merchant', merchantData);
    if (response.status !== 200) {
      throw new Error(response.data.message || 'Merchant creation failed!');
    }
    return response.data;
  }


  static async getMerchantData() {
    try {
      const response = await fetch('/admin/view-merchant');
      const merchantsData = await response.json();

      return merchantsData.map(
        (merchant) =>
          new Merchant(
            merchant.merch_id,
            merchant.merch_name,
            merchant.merch_phone,
            merchant.merch_email,
            merchant.date_created,
            merchant.date_updated_on,
            merchant.status
          )
      );
    } catch (error) {
      console.error('Error fetching merchant data:', error);
      throw new Error('Failed to fetch merchant data');
    }
  }

  static async fetchMerchantById(merchId) {
    try {
      const response = await axios.get(`/admin/merchants/${merchId}`);
      return response.data;
    } catch (error) {
      console.error("There was an error fetching the merchant data!", error);
      throw error;
    }
  }

  static async updateMerchant(merchId, merchantData) {
    try {
      const response = await axios.put(`/admin/merchants/${merchId}`, merchantData);
      return response.data;
    } catch (error) {
      console.error("There was an error updating the merchant!", error);
      throw error;
    }
  }

  static async updateMerchantStatus(merch_id, status) {
    try {
      const response = await axios.put(`/admin/suspend-merchants/${merch_id}`, { status });
      return response.data;
    } catch (error) {
      console.error('Error suspending merchant:', error);
      throw error;
    }
  }

}

export default Merchant;