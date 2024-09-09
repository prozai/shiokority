import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';
import CreateMerchant from './CreateMerchant';
import ViewMerchant from './ViewMerchant';

function Dashboard() {
  const [controller] = useState(() => new AdministratorController());
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    setStatus(controller.status);
  }, [controller.status]);

  const handleLogout = async () => {
    await controller.handleLogout(navigate);
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