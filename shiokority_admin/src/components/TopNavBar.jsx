import React from 'react';
import { FiHome, FiSettings, FiBell, FiUser } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';

const TopNavbar = ({ title }) => {
  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate('/dashboard');
  };

  return (
    <div className="flex justify-between items-center mb-8">
      <h1 className="text-2xl font-bold">{title}</h1>
      <div className="flex space-x-4">
        <FiHome size={24} onClick={handleHomeClick} className="cursor-pointer" />
        <FiSettings size={24} />
        <FiBell size={24} />
        <FiUser size={24} />
      </div>
    </div>
  );
};

export default TopNavbar;
