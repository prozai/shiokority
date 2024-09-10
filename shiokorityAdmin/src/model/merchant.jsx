import axios from 'axios';
import { useQuery } from '@tanstack/react-query';

class Merchant {

  constructor(merch_id, merch_name, merch_phone, merch_username, date_created, date_updated_on, merch_status) {
    this.merch_id = merch_id;
    this.merch_name = merch_name;
    this.merch_phone = merch_phone;
    this.merch_username = merch_username;
    this.date_created = date_created;
    this.date_updated_on = date_updated_on;
    this.merch_status = merch_status;
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
            merchant.merch_username,
            merchant.date_created,
            merchant.date_updated_on,
            merchant.merch_status
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

}

export default Merchant;