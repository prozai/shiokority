import axios from 'axios';

const updateMerchantStatus = async (merch_id) => {
  try {
    // Sending a request to update the merchant's status
    const response = await axios.put(`/admin/suspend-merchants/${merch_id}`);
    
    if (response.status === 200) {
      alert('Merchant status updated successfully');
      // Optionally, you can refresh the merchant data here after the update
      // Example: fetchData();
    } else {
      alert('Failed to update merchant status');
    }
  } catch (error) {
    console.error('Error updating merchant status:', error);
    alert('An error occurred while updating merchant status');
  }
};

export default updateMerchantStatus;
