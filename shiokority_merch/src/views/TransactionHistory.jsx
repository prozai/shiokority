import React, { useEffect, useState } from 'react';
import merchantController from '../controller/merchantController';
import Sidebar from '../components/sidebar';


const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState('');
  
  const fetchTransactionHistory = async () => {
    try {
        const merch_id = localStorage.getItem('merch_id');

        if (merch_id) {
            const data = await merchantController.getTransactionHistory(merch_id);
            setTransactions(data.transactions);
        } else {
            setMessage('Merchant ID not found.');
        }
    } catch (error) {
        setMessage('Unable to fetch transaction history');
    }
  };

  useEffect(() => {
    fetchTransactionHistory();
  }, []);

  return (
    <div className="flex h-screen bg-gray-200">
      {/* Sidebar */}
      <Sidebar />

    {/* Main Content */}
      <div className="flex-1 p-6">
        <div className="bg-white w-full max-w-3xl p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-[#153247] mb-6">Transaction History</h2>

        {transactions.length > 0 ? (
          <ul className="space-y-4">
            {transactions.map((transaction) => (
              <li key={transaction.payment_id} className="bg-gray-100 p-4 rounded-lg shadow-sm">
                <p className="text-gray-700">
                  <span className="font-semibold">Transaction ID:</span> {transaction.payment_id}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Amount:</span> ${transaction.amount}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Date:</span> {new Date(transaction.payment_date).toLocaleString()}
                </p>
                <p className={`font-semibold ${transaction.status === 'Success' ? 'text-green-500' : 'text-red-500'}`}>
                  Status: {transaction.status}
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-600">{message || 'No transactions available.'}</p>
        )}
      </div>
    </div>
    </div>
  );
};

export default TransactionHistory;
