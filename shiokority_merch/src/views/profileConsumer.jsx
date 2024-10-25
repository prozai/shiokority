import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';
import CardValidation from './CardValidation';

const ProfileConsumer = () => {
  const [profileData, setProfileData] = useState(null);
  const [paymentData, setPaymentData] = useState({ 
    merch_email: '', 
    amount: 0,
    cardNumber: '',
    expiryDate: '',
    cvv: ''
  });
  const [cardValidation, setCardValidation] = useState({
    cardNumber: false,
    expiryDate: false,
    cvv: false
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await consumerController.getProfileConsumer();
      setProfileData(data);
    } catch (error) {
      setMessage(error.message);
    }
  };
  
  const handlePaymentChange = (e) => {
    setPaymentData({ ...paymentData, [e.target.name]: e.target.value });
  };

  const handleCardValidationChange = (cardData, isValid) => {
    setPaymentData(prev => ({ ...prev, ...cardData }));
    setCardValidation(prev => ({ ...prev, [Object.keys(cardData)[0]]: isValid }));
  };

  const handleSendPayment = async (e) => {
    e.preventDefault();
    try {
      if (!Object.values(cardValidation).every(Boolean)) {
        setMessage('Please correct the card information');
        return;
      }
      
      const response = await consumerController.sendPayment(
        paymentData.merch_email, 
        paymentData.amount,
        paymentData.cardNumber,
        paymentData.expiryDate,
        paymentData.cvv,
        paymentData.uen
      );
      setMessage(response.message);
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleLogout = async () => {
    await consumerController.logoutConsumer();
    navigate('/login-consumer');
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <h2 className="text-3xl font-bold mb-5 text-gray-800">Consumer Profile</h2>
          {profileData ? (
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600">Name</p>
                <p className="font-semibold">{profileData.cust_fname} {profileData.cust_lname}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600">Email</p>
                <p className="font-semibold">{profileData.cust_email}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600">Phone</p>
                <p className="font-semibold">{profileData.cust_phone}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600">Address</p>
                <p className="font-semibold">{profileData.cust_address}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4 shadow">
                <p className="text-sm text-gray-600">Balance</p>
                <p className="font-semibold">{profileData.cust_amount}</p>
              </div>

              <div className="mt-8">
                <h3 className="text-2xl font-bold mb-4 text-gray-800">Send Payment</h3>
                <form onSubmit={handleSendPayment} className="space-y-4">
                  <input
                    type="text"
                    name="uen"
                    placeholder="UEN"
                    value={paymentData.uen}
                    onChange={handlePaymentChange}
                    required
                    className="w-full px-3 py-2 placeholder-gray-300 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-indigo-100 focus:border-indigo-300"
                  />
                  <input
                    type="number"
                    name="amount"
                    placeholder="Payment Amount"
                    value={paymentData.amount}
                    onChange={handlePaymentChange}
                    required
                    className="w-full px-3 py-2 placeholder-gray-300 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-indigo-100 focus:border-indigo-300"
                  />
                  <CardValidation onChange={handleCardValidationChange} />

                  <button 
                    type="submit" 
                    className={`w-full px-3 py-4 text-white rounded-md focus:outline-none ${
                      Object.values(cardValidation).every(Boolean)
                        ? 'bg-indigo-500 hover:bg-indigo-600'
                        : 'bg-gray-400 cursor-not-allowed'
                    }`}
                    disabled={!Object.values(cardValidation).every(Boolean)}
                  >
                    Send Payment
                  </button>
                </form>
              </div>

              <button onClick={handleLogout} className="mt-6 w-full px-3 py-4 text-white bg-red-500 rounded-md focus:bg-red-600 focus:outline-none">Logout</button>
              {message && <p className="mt-4 text-3xl text-center text-gray-600 ">{message}</p>}
            </div>
          ) : (
            <p className="text-center text-gray-600">{message || 'Loading profile...'}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfileConsumer;