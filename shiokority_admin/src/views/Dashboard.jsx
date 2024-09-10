import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';
import CreateMerchant from './CreateMerchant';
import ViewMerchant from './ViewMerchant';

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

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome to the admin dashboard!</p>
      
      {status && <p>{status}</p>}
      
      <button onClick={handleLogout}>Logout</button>

      <CreateMerchant />
      <ViewMerchant />
    </div>
  );
}

export default Dashboard;