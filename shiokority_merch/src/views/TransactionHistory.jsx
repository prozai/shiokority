import React, { useEffect, useState } from 'react';
import merchantController from '../controller/merchantController';

const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);
  const [balance, setBalance] = useState(0.0);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchTransactionHistory = async () => {
      try {
        const merch_id = localStorage.getItem('merch_id');
        if (merch_id) {
            const data = await merchantController.getTransactionHistory();
            setTransactions(data.transactions);
            setBalance(data.balance);
        } else {
            setMessage('Merchant ID not found');
        }
      } catch (error) {
        setMessage('Unable to fetch transaction history');
      }
    };

    fetchTransactionHistory();
  }, []);

  return (
    <div>
      <h2>Transaction History</h2>
        <p><strong>Current Balance:</strong> ${balance.toFixed(2)}</p>
        {transactions.length > 0 ? (
            <ul>
                {transactions.map((transaction) => (
                    <li key={transaction.payment_id}>
                        Transaction ID: {transaction.payment_id}, 
                        Amount: ${transaction.amount}, 
                        Date: {new Date(transaction.payment_date).toLocaleString()}, 
                        Status: {transaction.status}
                    </li>
                ))}
            </ul>
      ) : (
        <p>{message || 'No transactions available'}</p>
      )}
    </div>
  );
};

export default TransactionHistory;