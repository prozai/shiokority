import React, { useState, useEffect, useRef } from 'react'
import { useQuery } from "@tanstack/react-query"
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import CreateMerchant from './CreateMerchant'
import ViewMerchant from "./ViewMerchant";

function Dashboard() {
  const navigate = useNavigate();
  
  const handleLogout = async () => {
    try {
        // Notify the backend about the logout
        const response = await axios.post('/logout/admin');

        if (response.status === 200) {
          // Redirect to login page
          navigate('/login');
        }
        
    } catch (error) {
        console.error('Error logging out:', error);
        // Optionally handle errors here
    }
  };

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