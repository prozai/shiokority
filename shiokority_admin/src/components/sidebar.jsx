// src/components/Sidebar.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FiHome, FiSettings, FiBell, FiUser } from 'react-icons/fi';
import ShiokorityAdminLogo from '../asset/image/ShiokorityAdmin.png';
import AdministratorController from '../controller/administratorController';

const Sidebar = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await AdministratorController.logout();
    navigate('/login');
  };

  const handleSetup2FA = () => {
    navigate('/setup2FA');
  };

  const handleUserManagement = () => {
    navigate('/user-management');
  };

  const handleLogoClick = () => {
    navigate('/dashboard');
  };

  return (
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

      <button
        onClick={handleSetup2FA}
        className="mt-auto bg-[#0f1e28] hover:bg-[#0c1821] text-white font-bold py-2 px-4 rounded-full w-full"
      >
        Setup 2FA
      </button>
      
      <button
        onClick={handleLogout}
        className="mt-2 bg-[#0f1e28] hover:bg-[#0c1821] text-white font-bold py-2 px-4 rounded-full w-full"
      >
        Logout
      </button>
    </aside>
  );
};

const SidebarLink = ({ text }) => (
  <div className="p-2 rounded-lg hover:bg-[#0c1821] w-full text-center cursor-pointer">
    {text}
  </div>
);

export default Sidebar;
