import axios from 'axios';
import { useQuery } from '@tanstack/react-query';

class Merchant {

  constructor(merch_id, merch_name, merch_phone, merch_email, date_created, date_updated_on, merch_status) {
    this.merch_id = merch_id;
    this.merch_name = merch_name;
    this.merch_phone = merch_phone;
    this.merch_email = merch_email;
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
          merchant.merch_status
        )
    );
  }

}

export default Merchant;