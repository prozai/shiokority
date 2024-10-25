// src/components/Sidebar.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import ShiokorityAdminLogo from '../asset/image/ShiokorityAdmin.png';

const Sidebar = ({ handleLogout, handleSetup2FA, handleUserManagement }) => {
  const navigate = useNavigate();

  const handleLogoClick = () => {
    navigate('/dashboard');
  };

  return (
    <aside className="w-64 bg-[#153247] p-4 text-white flex flex-col items-center">
      {/* Centered Logo */}
      <img
        src={ShiokorityAdminLogo}
        alt="Shiokority Admin"
        className="h-24 mb-6 cursor-pointer"
        onClick={handleLogoClick}
      />
      {/* Centered Administrator text */}
      <h2 className="text-xl font-bold mb-4 text-center">Administrator</h2>

      {/* Navigation Menu */}
      <nav className="flex flex-col w-full space-y-4">
        <button
          onClick={handleUserManagement}
          className="w-full p-2 text-center hover:bg-[#0c1821] rounded-lg"
        >
          User Management
        </button>
        <SidebarLink text="Feature Management" />
        <SidebarLink text="Customer Support" />
        <SidebarLink text="System Management" />
        <SidebarLink text="Predictive Analytics Tools" />
      </nav>

      {/* Bottom buttons, aligned at the bottom */}
      <div className="mt-auto w-full">
        <button
          onClick={handleSetup2FA}
          className="bg-[#0f1e28] hover:bg-[#0c1821] text-white font-bold py-2 px-4 rounded-full w-full"
        >
          Setup 2FA
        </button>

        <button
          onClick={handleLogout}
          className="mt-2 bg-[#0f1e28] hover:bg-[#0c1821] text-white font-bold py-2 px-4 rounded-full w-full"
        >
          Logout
        </button>
      </div>
    </aside>
  );
};

const SidebarLink = ({ text }) => (
  <div className="p-2 text-center rounded-lg hover:bg-[#0c1821] w-full cursor-pointer">
    {text}
  </div>
);

export default Sidebar;
