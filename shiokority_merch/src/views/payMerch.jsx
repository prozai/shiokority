import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate
import consumerController from '../controller/consumerController';

const PayMerchant = () => {
  const [merchants, setMerchants] = useState([]);
  const navigate = useNavigate(); // Initialize navigate

  useEffect(() => {
    // Fetch merchant list from the backend
    const fetchMerchants = async () => {
      try {
        const merchantData = await consumerController.getMerchantData(); // Fetch complete merchant data
        console.log('Fetched merchant data:', merchantData); // Log fetched data for debugging
        setMerchants(merchantData); // Set fetched data to state
      } catch (error) {
        console.error('Failed to fetch merchants:', error);
      }
    };

    fetchMerchants();
  }, []);

  // Function to handle click on the merchant card
  const handleMerchantClick = (uen) => {
    // Navigate to the payment page with UEN as a URL parameter
    navigate(`/profile-consumer/${uen}`);
  };

  return (
    <div className="p-5">
      <h1 className="text-2xl font-semibold mb-4 text-center">Available Merchants</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
        {merchants.length > 0 ? (
          merchants.map((merchant) => (
            <div
              key={merchant.merch_id}
              className="bg-gray-100 border border-gray-300 p-5 rounded-md text-center cursor-pointer hover:bg-gray-200 transition"
              onClick={() => handleMerchantClick(merchant.merch_uen)} // Call the click handler on card click
            >
              <h3 className="text-lg font-medium">{merchant.merch_name}</h3>
              <p className="text-gray-600">Address: {merchant.merch_address}</p>
              <p className="text-gray-600">UEN: {merchant.merch_uen}</p>
            </div>
          ))
        ) : (
          <p className="text-gray-500">No merchants available.</p>
        )}
      </div>
    </div>
  );
};

export default PayMerchant;
