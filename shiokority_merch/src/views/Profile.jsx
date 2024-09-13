import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';

const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const [message, setMessage] = useState('');
  
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await merchantController.getProfile();
        setProfileData(data.merchant);
      } catch (error) {
        setMessage(error.message);
      }
    };

    fetchProfile();
  }, []);

  const handleLogout = async () => {
    await merchantController.logout();
    navigate('/login'); // Redirect to login after logout
  };

  return (
    <div>
      <h2>Merchant Profile</h2>
      {profileData ? (
        <div>
          <p>Name: {profileData.name}</p>
          <p>Email: {profileData.email}</p>
          <p>Phone: {profileData.phone}</p>
          <p>Address: {profileData.address}</p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>{message || 'Loading profile...'}</p>
      )}
    </div>
  );
};

export default Profile;