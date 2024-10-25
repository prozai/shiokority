// src/views/Dashboard.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';
import { FiHome, FiSettings, FiBell, FiUser } from 'react-icons/fi';

import Sidebar from '../components/SideBar'; // Import Sidebar component
import TopNotificationBar from '../components/TopNotificationBar'; // Import TopNotificationBar component

function Dashboard() {
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

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

  // Define alerts to pass to TopNotificationBar
  const initialAlerts = [
    { color: 'bg-pink-500', message: 'Pink Alert' },
    { color: 'bg-gray-500', message: 'Gray Alert' },
    { color: 'bg-green-500', message: 'Green Alert' },
    { color: 'bg-orange-500', message: 'Orange Alert' },
    { color: 'bg-blue-500', message: 'Blue Alert' },
    { color: 'bg-black', message: 'Black Alert' },
  ];

  return (
    <div className="flex h-screen bg-gray-200">
      {/* Use Sidebar Component */}
      <Sidebar 
        handleLogout={handleLogout} 
        handleSetup2FA={handleSetup2FA} 
        handleUserManagement={handleUserManagement} 
      />

      {/* Main Content */}
      <main className="flex-1 p-6">
        {/* Top Navbar */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <div className="flex space-x-4">
            <FiHome size={24} />
            <FiSettings size={24} />
            <FiBell size={24} />
            <FiUser size={24} />
          </div>
        </div>

        {/* Top Notification Bar */}
        <TopNotificationBar initialAlerts={initialAlerts} />

        {/* Notifications */}
        <section className="bg-white p-4 rounded-lg shadow-lg">
          <h2 className="text-lg font-semibold mb-4">Notifications</h2>
          <p className="text-gray-600 mb-4">Notifications on this page. Read more details here.</p>
          <div className="flex space-x-4">
            <NotificationButton text="SUCCESS" color="bg-green-500" />
            <NotificationButton text="INFO" color="bg-blue-500" />
            <NotificationButton text="WARNING" color="bg-orange-500" />
            <NotificationButton text="DANGER" color="bg-red-500" />
          </div>
        </section>
        
        {/* Status Message */}
        {status && <p className="mt-4 text-center text-red-500">{status}</p>}
      </main>
    </div>
  );
}

const NotificationButton = ({ text, color }) => (
  <button className={`${color} text-white py-2 px-4 rounded-full w-1/4 font-bold hover:opacity-90`}>
    {text}
  </button>
);

export default Dashboard;
