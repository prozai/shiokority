// src/views/Dashboard.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';

import Sidebar from '../components/SideBar'; // Import Sidebar component
import TopNotificationBar from '../components/TopNotificationBar'; // Import TopNotificationBar component
import TopNavbar from '../components/TopNavBar';

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
    { color: 'bg-red-500', message: 'Red Alert' },
    { color: 'bg-gray-500', message: 'Gray Alert' },
    { color: 'bg-green-500', message: 'Green Alert' },
    { color: 'bg-orange-500', message: 'Orange Alert' },
    { color: 'bg-blue-500', message: 'Blue Alert' },
    { color: 'bg-black', message: 'Black Alert' },
  ];

  return (
    <div className="flex h-screen bg-gray-200">
<<<<<<< HEAD
      {/* Sidebar */}
      <aside className="w-64 bg-[#153247] p-4 text-white flex flex-col items-center">
        <img
          src={ShiokorityAdminLogo}
          alt="Shiokority Admin"
          className="h-24 mb-6 cursor-pointer"
          onClick={handleLogoClick}
        />
        <h2 className="text-xl font-bold mb-4">Administrator</h2>
        
        <nav className="flex flex-col w-full space-y-4">
          <button
            onClick={handleUserManagement}
            className="w-full p-2 text-left hover:bg-[#0c1821] rounded-lg"
          >
            User Management
          </button>
          <SidebarLink text="Feature Management" />
          <SidebarLink text="System Management" />
          <SidebarLink text="Predictive Analytics Tools" />
        </nav>

        <button onClick={handleSetup2FA} className="mt-auto bg-[#0f1e28] hover:bg-[#0c1821] text-white font-bold py-2 px-4 rounded-full w-full">
          Setup 2FA
        </button>
        
        <button onClick={handleLogout} className="mt-2 bg-[#0f1e28] hover:bg-[#0c1821] text-white font-bold py-2 px-4 rounded-full w-full">
          Logout
        </button>
      </aside>
=======
      {/* Use Sidebar Component */}
      <Sidebar 
        handleLogout={handleLogout} 
        handleSetup2FA={handleSetup2FA} 
        handleUserManagement={handleUserManagement} 
      />
>>>>>>> bfe1984 (converted side bar into component and top notification into a component)

      {/* Main Content */}
      <main className="flex-1 p-6">
        {/* Top Navbar */}
        <TopNavbar title="Dashboard" />

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
