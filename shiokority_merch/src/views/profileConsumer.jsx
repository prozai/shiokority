import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';
import CardValidation from './CardValidation';
import ShiokorityPayLogo from '../asset/image/ShiokorityPay.png';


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
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <div className="flex justify-center mb-8">
          <img src={ShiokorityPayLogo} alt="Shiokority Pay" className="h-40" />
        </div>
          <h2 className="text-2xl font-bold text-[#153247] mb-6">Consumer Profile</h2>

          {profileData ? (
            <div>
              <div className="mb-6 space-y-4">
                <p className="text-gray-700"><span className="font-semibold">Name:</span> {profileData.cust_fname} {profileData.cust_lname}</p>
                <p className="text-gray-700"><span className="font-semibold">Email:</span> {profileData.cust_email}</p>
                <p className="text-gray-700"><span className="font-semibold">Phone:</span> {profileData.cust_phone}</p>
                <p className="text-gray-700"><span className="font-semibold">Address:</span> {profileData.cust_address}</p>
              </div>

              <div className="mt-8">
                <h3 className="text-2xl font-bold mb-4 text-gray-800">Send Payment</h3>
                <form onSubmit={handleSendPayment} className="space-y-4">
                  <input
                    type="email"
                    name="merch_email"
                    placeholder="Merchant Email"
                    value={paymentData.merch_email}
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
                      ? 'bg-[#153247] hover:bg-green-600'
                      : 'bg-gray-400 cursor-not-allowed'
                  }`}
                  disabled={!Object.values(cardValidation).every(Boolean)}
                >
                  Send Payment
                </button>
              </form>

              <button
                onClick={handleLogout}
                className="mt-6 w-full px-3 py-4 text-white bg-red-500 rounded-md hover:bg-red-600 focus:outline-none"
              >
                Logout
              </button>

              {message && <p className="mt-4 text-center text-gray-600">{message}</p>}
            </div>
          ) : (
            <p className="text-center text-gray-600">{message || 'Loading profile...'}</p>
          )}
        </div>
      </div>
  );
};

export default ProfileConsumer;
