import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';

const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const [paymentData, setPaymentData] = useState({ merch_email: '', amount: 0 });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await consumerController.getProfile();
        setProfileData(data.consumer);
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
        </div>
      ) : (
        <p>{message || 'Loading profile...'}</p>
      )}
    </div>
  );
};

export default profileConsumer;