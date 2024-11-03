import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';
import ViewMerchant from './ViewMerchant'; // Existing component for viewing merchants
import ViewUser from './ViewUser'; // Existing component for viewing users
import Sidebar from '../components/SideBar'; // Import Sidebar component
import TopNotificationBar from '../components/TopNotificationBar'; // Import TopNotificationBar component
import TopNavbar from '../components/TopNavBar';

const ViewManagement = () => {
  const [activeTab, setActiveTab] = useState('merchant'); // Can be 'merchant' or 'user'
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await AdministratorController.logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error.message);
    }
  };

  const handleSetup2FA = () => {
    navigate('/setup2FA');
  };

  const handleUserManagement = () => {
    navigate('/user-management');
  };

  const handleAuditTrail = () => {
    navigate('/auditTrail');
  };

  const initialAlerts = [
    { color: 'bg-red-500', message: 'Red Alert' },
  ];


  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar Section */}
      <Sidebar 
        handleLogout={handleLogout} 
        handleSetup2FA={handleSetup2FA} 
        handleUserManagement={handleUserManagement} 
        handleAuditTrail={handleAuditTrail}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Section */}
        <div className="flex flex-col">
          {/* Top Notification Bar */}
          <TopNotificationBar initialAlerts={initialAlerts} />

          {/* Top Navbar */}
          <TopNavbar title="User Management" />
        </div>

        {/* Tab and Content Section */}
        <div className="flex-1 overflow-auto p-4 bg-gray-100">
          {/* Tab Buttons */}
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

          {/* Conditionally Render Merchant or User Lists */}
          <div className="flex-1 overflow-auto">
            {activeTab === 'merchant' && (
              <div className="h-full overflow-auto">
                <ViewMerchant /> {/* Render the merchant list */}
              </div>
            )}

            {activeTab === 'user' && (
              <div className="h-full overflow-auto">
                <ViewUser /> {/* Render the user list */}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewManagement;
