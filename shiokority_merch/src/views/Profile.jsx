import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';

const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState('');
  const [balance, setBalance] = useState(0);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await merchantController.getProfile();
        setProfileData(data.merchant);
        // Fetch transactions and balance after profile data is available
        if (data.merchant?.merch_id) {
          fetchTransactionHistory(data.merchant.merch_id);
        }
      } catch (error) {
        setMessage(error.message);
      }
    };

    const fetchTransactionHistory = async (merch_id) => {
      try {
        const data = await merchantController.getTransactionHistory(merch_id);
        setTransactions(data.transactions);
        setBalance(data.balance);
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };

    fetchProfile();

    // Poll for new transactions every 10 seconds
    const interval = setInterval(() => {
      if (profileData?.merch_id) {
        fetchTransactionHistory(profileData.merch_id);
      }
    }, 10000); // Poll every 10 seconds
    
    // Clean up the interval when the component unmounts
    return () => clearInterval(interval);
  }, []); // Remove profileData from the dependency array

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
          <p>Current Balance: ${balance.toFixed(2)}</p>

          <h3>Recent Transactions</h3>
          {transactions.length > 0 ? (
            <ul>
              {transactions.map((transaction) => (
                <li key={transaction.payment_id}>
                  Transaction ID: {transaction.payment_id},
                  Amount: ${transaction.amount},
                  Date: {new Date(transaction.payment_date).toLocaleString()}
                </li>
              ))}
            </ul>
          ) : (
            <p>No transactions found.</p>
          )}
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>{message || 'Loading profile...'}</p>
      )}
    </div>
  );
};

export default Profile;