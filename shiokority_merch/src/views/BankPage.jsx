import React, { useState } from 'react';
import merchantController from '../controller/merchantController';

const BankPage = () => {
  const [formData, setFormData] = useState({
    merch_email: '',
    amount: 0
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Use merchantController to handle payment
      const response = await merchantController.processPayment(formData.merch_email, formData.amount);
      setMessage(response.message); // Display the response message
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div>
      <h2>Bank Demo</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="merch_email"
          placeholder="Merchant Email"
          value={formData.merch_email}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="amount"
          placeholder="Payment Amount"
          value={formData.amount}
          onChange={handleChange}
          required
        />
        <button type="submit">Send Payment</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default BankPage;