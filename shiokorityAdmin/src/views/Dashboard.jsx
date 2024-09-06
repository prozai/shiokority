import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import CreateMerchant from './CreateMerchant'
import ViewMerchant from "./ViewMerchant";
import { useDashboardController } from '../controller/administratorController';



function Dashboard() {
  const navigate = useNavigate();
  const { handleLogout } = useDashboardController();

  return (
  <div>
    <h2>Dashboard</h2>
    <p>Welcome to the admin dashboard!</p>
    
    <button onClick={handleLogout}>Logout</button>

    <CreateMerchant />
    <ViewMerchant />

  </div>
);
}

export default Dashboard