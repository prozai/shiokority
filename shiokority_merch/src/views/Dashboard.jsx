import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiHome, FiSettings, FiBell, FiUser, FiPieChart, FiFileText, FiMaximize2 } from 'react-icons/fi';
import ShiokorityMerchLogo from '../asset/image/ShiokorityMerch.png';
import merchantController from '../controller/merchantController';

function MerchantDashboard() {
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      // Assume logout logic is implemented in the controller
      await merchantController.logout();
      setStatus('Logged out successfully');
      navigate('/login');
    } catch (error) {
      setStatus('Logout failed: ' + error.message);
    }
  };

  return (
    <div className="flex h-screen bg-gray-200">
      {/* Sidebar */}
      <aside className="w-64 bg-[#153247] p-4 text-white flex flex-col items-center">
      <img src={ShiokorityMerchLogo} alt="Shiokority Merch" className="h-24 mb-6" />
        <h2 className="text-xl font-bold mb-4">Merchant</h2>
        
        <nav className="flex flex-col w-full space-y-4">
          <SidebarLink icon={<FiUser size={20} />} text="Profile" />
          <SidebarLink icon={<FiPieChart size={20} />} text="Analytics" />
          <SidebarLink icon={<FiFileText size={20} />} text="Transaction History" />
          {/* Pay Button with Circular Style */}
          <div className="flex flex-col items-center mt-4">
            <button className="flex flex-col items-center justify-center bg-[#153247] text-white w-16 h-16 rounded-full shadow-md hover:shadow-lg">
              <FiMaximize2 size={20} />
              <span className="text-xs">Pay</span>
            </button>
          </div>
        </nav>
        
        <button onClick={handleLogout} className="mt-auto bg-[#0f1e28] hover:bg-[#0c1821] text-white font-bold py-2 px-4 rounded-full w-full">
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

        {/* Alert and Notification Sections */}
        <section className="space-y-4 mb-8">
          <Alert color="bg-pink-500" />
          <Alert color="bg-gray-500" />
          <Alert color="bg-green-500" />
          <Alert color="bg-orange-500" />
          <Alert color="bg-blue-500" />
          <Alert color="bg-black" />
        </section>

        <section className="bg-white p-4 rounded-lg shadow-lg">
          <h2 className="text-lg font-semibold mb-4">Notifications</h2>
          <div className="flex space-x-4">
            <NotificationButton text="SUCCESS" color="bg-green-500" />
            <NotificationButton text="INFO" color="bg-blue-500" />
            <NotificationButton text="WARNING" color="bg-orange-500" />
            <NotificationButton text="DANGER" color="bg-red-500" />
          </div>
        </section>
        
        {status && <p className="mt-4 text-center text-red-500">{status}</p>}
      </main>
    </div>
  );
}

const SidebarLink = ({ icon, text }) => (
  <div className="flex items-center p-2 rounded-lg hover:bg-[#0c1821] w-full cursor-pointer">
    <span className="mr-3">{icon}</span>
    <span>{text}</span>
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

export default MerchantDashboard;