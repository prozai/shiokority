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
      const response = await consumerController.sendPayment(paymentData.merch_email, paymentData.amount);
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
          <p>Name: {profileData.first_name} {profileData.last_name}</p>
          <p>Email: {profileData.email}</p>
          <p>Address: {profileData.address}</p>

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
              name="amount"
              placeholder="Payment Amount"
              value={paymentData.amount}
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