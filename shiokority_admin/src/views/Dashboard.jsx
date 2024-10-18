import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';
import { FiHome, FiSettings, FiBell, FiUser } from 'react-icons/fi';

import ShiokorityAdminLogo from '../asset/image/ShiokorityAdmin.png';

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

  // Function to navigate to User Management
  const handleUserManagement = () => {
    navigate('/user-management');
  };

  // Function to navigate back to the Dashboard
  const handleLogoClick = () => {
    navigate('/dashboard');
  };

  return (
    <div className="flex h-screen bg-gray-200">
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
          <SidebarLink text="Customer Support" />
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

        {/* Alert Section */}
        <section className="space-y-4 mb-8">
          <Alert color="bg-pink-500" />
          <Alert color="bg-gray-500" />
          <Alert color="bg-green-500" />
          <Alert color="bg-orange-500" />
          <Alert color="bg-blue-500" />
          <Alert color="bg-black" />
        </section>

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

const SidebarLink = ({ text }) => (
  <div className="p-2 rounded-lg hover:bg-[#0c1821] w-full text-center cursor-pointer">
    {text}
  </div>
);

const Alert = ({ color }) => (
  <div className={`${color} text-white p-4 rounded-lg flex justify-between items-center`}>
    <span>Alert Message</span>
    <button className="text-white font-bold">×</button>
  </div>
);

const NotificationButton = ({ text, color }) => (
  <button className={`${color} text-white py-2 px-4 rounded-full w-1/4 font-bold hover:opacity-90`}>
    {text}
  </button>
);

export default Dashboard;
