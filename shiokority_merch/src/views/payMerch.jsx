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

  // Styles for the grid layout
  const containerStyle = {
    padding: '20px',
  };

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
    gap: '20px',
  };

  const cardStyle = {
    backgroundColor: '#f9f9f9',
    border: '1px solid #ddd',
    padding: '20px',
    textAlign: 'center',
    borderRadius: '5px',
    cursor: 'pointer', // Change cursor to pointer to indicate clickability
  };

  return (
    <div style={containerStyle}>
      <h1>Available Merchants</h1>
      <br />
      <div style={gridStyle}>
        {merchants.length > 0 ? (
          merchants.map((merchant) => (
            <div
              key={merchant.merch_id}
              style={cardStyle}
              onClick={() => handleMerchantClick(merchant.merch_uen)} // Call the click handler on card click
            >
              <h3>{merchant.merch_name}</h3>
              <p>Address: {merchant.merch_address}</p>
              <p>UEN: {merchant.merch_uen}</p>
            </div>
          ))
        ) : (
          <p>No merchants available.</p>
        )}
      </div>
    </div>
  );
};

export default PayMerchant;