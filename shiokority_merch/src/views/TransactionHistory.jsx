import React, { useEffect, useState } from 'react';
import merchantController from '../controller/merchantController';
import Sidebar from '../components/sidebar';


const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState('');
  
  const fetchTransactionHistory = async () => {
    try {
        const data = await merchantController.getTransactionHistory();
        setTransactions(data);
        
    } catch (error) {
        setMessage(error.message);
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

          <ul className="space-y-4">
            {transactions.map((transaction) => (
              <li key={transaction.payment_id} className="bg-gray-100 p-4 rounded-lg shadow-sm">
                <p className="text-gray-700">
                  <span className="font-semibold">Transaction ID:</span> {transaction.payment_record_id}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Amount:</span> ${transaction.payment_record_amount}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Date:</span> {transaction.payment_record_date_created}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Type:</span> {transaction.payment_record_type}
                </p>
                <p className={`font-semibold ${transaction.payment_record_status === 'completed' ? 'text-green-500' : 'text-red-500'}`}>
                  Status: {transaction.payment_record_status}
                </p>
              </li>
            ))}
          </ul>
      </div>
    </div>
    </div>
  );
};

export default TransactionHistory;
