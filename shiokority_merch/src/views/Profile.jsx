import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';
import Sidebar from '../components/sidebar';


const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await merchantController.getProfile();
        setProfileData(data);
        // Fetch transactions and balance after profile data is available
        if (data.merchant?.merch_id) {
          fetchTransactionHistory(data.merchant.merch_id);
        }
      } catch (error) {
        setMessage('Failed to load data. Please try again later.');
      }
    };

    const fetchTransactionHistory = async () => {
      try {
        const data = await merchantController.getTransactionHistory();
        setTransactions(data);
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };

    fetchProfile();
    fetchTransactionHistory()

  }, [profileData?.merch_id]);


  const handleViewTransactionHistory = () => {
    navigate('/transactions');
  };

  return (
    <div className="flex h-screen bg-gray-200">
      {/* Sidebar */}
      <Sidebar />

{/* Main Content */}
<div className="flex-1 p-6">
        <div className="bg-white w-full max-w-3xl p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-[#153247] mb-6">Merchant Profile</h2>

        {profileData ? (
          <div>
            <div className="mb-6 space-y-4">
              <p className="text-gray-700"><span className="font-semibold">Name:</span> {profileData.merch_name}</p>
              <p className="text-gray-700"><span className="font-semibold">Email:</span> {profileData.merch_email}</p>
              <p className="text-gray-700"><span className="font-semibold">Phone:</span> {profileData.merch_phone}</p>
              <p className="text-gray-700"><span className="font-semibold">Address:</span> {profileData.merch_address}</p>
              <p className="text-gray-700"><span className="font-semibold">UEN:</span> {profileData.merch_uen}</p>
            </div>

            <h3 className="text-xl font-semibold mb-4">Recent Transactions</h3>

              <ul className="space-y-2 mb-6">
                {transactions.map((transaction) => (
                  <li key={transaction.payment_id} className="bg-gray-100 p-4 rounded-lg shadow-sm">
                    <p><span className="font-semibold">Transaction ID:</span> {transaction.payment_record_id}</p>
                    <p><span className="font-semibold">Amount:</span> ${transaction.payment_record_amount}</p>
                    <p><span className="font-semibold">Date:</span> {transaction.payment_record_date_created}</p>
                  </li>
                ))}
              </ul>

            <div className="flex space-x-4">
      
              <button
                onClick={handleViewTransactionHistory}
                className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 w-full font-semibold"
              >
                View Transaction History
              </button>
            </div>
          </div>
        ) : (
          <p className="text-gray-600">{message || 'Loading profile...'}</p>
        )}
      </div>
    </div>
    </div>
  );
};

export default Profile;
