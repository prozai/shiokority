// src/components/Sidebar.jsx
import React from 'react';
import { FiUser, FiPieChart, FiFileText, FiMaximize2 } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';
import ShiokorityMerchLogo from '../asset/image/ShiokorityMerch.png';
import merchantController from '../controller/merchantController';

const Sidebar = () => {
  const navigate = useNavigate();

  const handleProfileClick = () => navigate('/profile');
  const handleViewTransactionHistory = () => navigate('/transactions');
  const handleLogoClick = () => navigate('/dashboard');
  const handleLogout = async () => {
    await merchantController.logout();
    navigate('/login');
  };

  return (
    <aside className="w-64 bg-[#153247] p-4 text-white flex flex-col items-center">
      <img src={ShiokorityMerchLogo} alt="Shiokority Merch" className="h-24 mb-6" onClick={handleLogoClick} />
      <h2 className="text-xl font-bold mb-4">Merchant</h2>
      
      <nav className="flex flex-col w-full space-y-4">
        <SidebarLink icon={<FiUser size={20} />} text="Profile" onClick={handleProfileClick} />
        <SidebarLink icon={<FiPieChart size={20} />} text="Analytics" />
        <SidebarLink icon={<FiFileText size={20} />} text="Transaction History" onClick={handleViewTransactionHistory} />
        
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
  );
};

const SidebarLink = ({ icon, text, onClick }) => (
  <div className="flex items-center p-2 rounded-lg hover:bg-[#0c1821] w-full cursor-pointer" onClick={onClick}>
    <span className="mr-3">{icon}</span>
    <span>{text}</span>
  </div>
);

export default Sidebar;
