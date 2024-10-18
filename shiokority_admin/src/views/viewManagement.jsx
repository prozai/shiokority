// src/views/ViewManagement.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ViewMerchant from './ViewMerchant'; // Existing component for viewing merchants
import ViewUser from './ViewUser'; // Existing component for viewing users

const ViewManagement = () => {
  const [activeTab, setActiveTab] = useState('merchant'); // Can be 'merchant' or 'user'
  const navigate = useNavigate();

  const handleAddMerchant = () => {
    navigate('/create-merchant');
  };

  const handleAddUser = () => {
    navigate('/create-user');
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h3 className="text-2xl font-bold mb-4">User Management</h3>

      {/* Toggle between Merchant and User lists */}
      <div className="mb-4">
        <button
          className={`p-2 mr-2 ${activeTab === 'merchant' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'}`}
          onClick={() => setActiveTab('merchant')}
        >
          Merchant List
        </button>
        <button
          className={`p-2 ${activeTab === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'}`}
          onClick={() => setActiveTab('user')}
        >
          User List
        </button>
      </div>

      {/* Conditionally render Merchant or User lists based on the selected tab */}
      {activeTab === 'merchant' && (
        <div>
          <ViewMerchant /> {/* Render the merchant list */}
        </div>
      )}

      {activeTab === 'user' && (
        <div>
          <ViewUser /> {/* Render the user list */}
        </div>
      )}
    </div>
  );
};

export default ViewManagement;