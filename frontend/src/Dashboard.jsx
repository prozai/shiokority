import React, { useState, useEffect, useRef } from 'react'
import { useQuery } from "@tanstack/react-query"
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


function Dashboard() {
  const navigate = useNavigate();
  
  // const {data:admin, isLoading} = useQuery({
  //   queryKey:["admin"],
  //   queryFn: async () => {
  //     const response = await fetch('/login/admin')
  //     return await response.json()
  //   }
  // })
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
    
    {/* {isLoading && <div>Loading...</div>}
    {!isLoading && (
      <div>
        <p>Email: {admin.admin_username}</p>
        <p>Password: {admin.pass_hash}</p>
        <p>Status: {admin.status}</p>
      </div>
    )} */}
    <button onClick={handleLogout}>Logout</button>

  </div>
);
}

export default Dashboard