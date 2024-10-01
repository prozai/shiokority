import React, { useEffect, useState } from 'react';
import merchantController from '../controller/merchantController';

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
            setMessage('Merchant ID not found.')
        }
    } catch (error) {
        setMessage('Unable to fetch transaction history');
    }
};

useEffect(() => {
        fetchTransactionHistory();
    }, []);

  return (
    <div>
      <h2>Transaction History</h2>
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