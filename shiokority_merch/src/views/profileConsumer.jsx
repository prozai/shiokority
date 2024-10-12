import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';

const ProfileConsumer = () => {
  const [profileData, setProfileData] = useState(null);
  const [paymentData, setPaymentData] = useState({ merch_email: '', amount: 0 });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await consumerController.getProfileConsumer();
        setProfileData(data);
      } catch (error) {
        setMessage(error.message);
      }
    };

    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setPaymentData({ ...paymentData, [e.target.name]: e.target.value });
  };

  const handleSendPayment = async (e) => {
    e.preventDefault();
    try {
      const response = await consumerController.sendPayment(profileData.cust_email, paymentData.merch_email, paymentData.merch_amount );
      setMessage(response.message);
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleLogout = async () => {
    await consumerController.logout();
    navigate('/login-consumer'); // Redirect to login after logout
  };

  return (
    <div>
      <h2>Consumer Profile</h2>
      {profileData ? (
        <div>
          <p>Name: {profileData.cust_fname} {profileData.cust_lname}</p>
          <p>Email: {profileData.cust_email}</p>
          <p>Phone: {profileData.cust_phone}</p>
          <p>Address: {profileData.cust_address}</p>

          <h3>Send Payment</h3>
          <form onSubmit={handleSendPayment}>
            <input
              type="email"
              name="merch_email"
              placeholder="Merchant Email"
              value={paymentData.merch_email}
              onChange={handleChange}
              required
            />
            <input
              type="number"
              name="merch_amount"
              placeholder="Payment Amount"
              value={paymentData.merch_amount}
              onChange={handleChange}
              required
            />
            <button type="submit">Send Payment</button>
          </form>

          {message && <p>{message}</p>}
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>{message || 'Loading profile...'}</p>
      )}
    </div>
  );
};

export default ProfileConsumer;