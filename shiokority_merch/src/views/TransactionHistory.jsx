import React, { useEffect, useState } from 'react';
import merchantController from '../controller/merchantController';
import Sidebar from '../components/sidebar';
import { CreditCard, Clock, Receipt, Calendar } from 'lucide-react';

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

  const formatDateTime = (dateStr) => {
    return dateStr.replace(' GMT', '')
  }

  useEffect(() => {
    fetchTransactionHistory();
  }, []);

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 p-6 overflow-hidden">
        <div className="bg-white rounded-xl shadow-md h-full">
          {/* Header */}
          <div className="border-b sticky top-0 z-10 bg-white px-6 py-4">
            <div className="flex items-center space-x-3">
              <div className="rounded-full bg-blue-100 p-2">
                <CreditCard className="h-6 w-6 text-blue-600" />
              </div>
              <h2 className="text-2xl font-bold text-[#153247]">Transaction History</h2>
            </div>
            {message && (
              <div className="text-red-500 text-sm mt-2">{message}</div>
            )}
          </div>

          {/* Transaction List */}
          <div className="max-h-[calc(100vh-180px)] overflow-y-auto px-6">
            {transactions.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-gray-500">
                <Receipt className="h-12 w-12 text-gray-400 mb-2" />
                <p>No transactions found</p>
              </div>
            ) : (
              <div className="py-4 space-y-4">
                {transactions.map((transaction) => (
                  <div
                    key={transaction.payment_id}
                    className="bg-white border rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition duration-200"
                  >
                    {/* Transaction Header */}
                    <div className="flex items-center justify-between px-6 py-4 bg-gray-50 border-b">
                      <div className="flex items-center space-x-3">
                        <Clock className="h-5 w-5 text-gray-400" />
                        <span className="text-sm font-medium text-gray-600">
                          Transaction ID: {transaction.payment_record_id}
                        </span>
                      </div>
                      <span 
                        className={`px-3 py-1 rounded-full text-sm font-medium ${
                          transaction.payment_record_status === 'completed' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-red-100 text-red-700'
                        }`}
                      >
                        {transaction.payment_record_status}
                      </span>
                    </div>

                    {/* Transaction Details */}
                    <div className="px-6 py-4 space-y-4">
                      {/* Date */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <Calendar className="h-5 w-5 text-gray-400" />
                          <span className="text-gray-600">Date & Time</span>
                        </div>
                        <span className="text-gray-900 font-medium">
                          {formatDateTime(transaction.payment_record_date_created)}
                        </span>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Amount */}
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <Receipt className="h-5 w-5 text-gray-400" />
                            <span className="text-gray-600">Amount</span>
                          </div>
                          <span className="font-semibold text-lg text-gray-900">
                            ${parseFloat(transaction.payment_record_amount).toFixed(2)}
                          </span>
                        </div>
                        
                        {/* Type */}
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <CreditCard className="h-5 w-5 text-gray-400" />
                            <span className="text-gray-600">Type</span>
                          </div>
                          <span className="text-gray-900 capitalize">
                            {transaction.payment_record_type}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TransactionHistory;
