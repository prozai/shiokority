// src/views/ViewManagement.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';
import ViewMerchant from './ViewMerchant'; // Existing component for viewing merchants
import ViewUser from './ViewUser'; // Existing component for viewing users
import Sidebar from '../components/SideBar'; // Import Sidebar component

const ViewManagement = () => {
  const [status, setStatus] = useState('');
  const [activeTab, setActiveTab] = useState('merchant'); // Can be 'merchant' or 'user'
  const navigate = useNavigate();

  const handleAddMerchant = () => {
    navigate('/create-merchant');
  };

  const handleAddUser = () => {
    navigate('/create-user');
  };

  const handleLogout = async () => {
    try {
      await AdministratorController.logout();
      setStatus('Logged out successfully');
      navigate('/login');
    } catch (error) {
      setStatus('Logout failed: ' + error.message);
    }
  };

  const handleSetup2FA = () => {
    navigate('/setup2FA');
  };

  const handleUserManagement = () => {
    navigate('/user-management');
  };

  return (
    <div className="flex h-screen">
      {/* Use Sidebar Component */}
      <Sidebar 
        handleLogout={handleLogout} 
        handleSetup2FA={handleSetup2FA} 
        handleUserManagement={handleUserManagement} 
      />

      {/* Main Content */}
      <div className="p-6 bg-gray-100 min-h-screen flex-1">
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
    </div>
  );
};

export default ViewManagement;
