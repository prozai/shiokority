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

    if (formData.amount <= 0) {
      setMessage("Please enter a valid payment amount.");
      return;
    }
    try {
      const response = await merchantController.processPayment(formData.merch_email, formData.amount);
      setMessage(response.message);
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#153247] p-6">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        <h3 className="text-2xl font-bold mb-6 text-[#153247]">Bank Demo</h3>
        
        <div className="mb-4">
          <label htmlFor="merch_email" className="block text-gray-700 text-sm font-bold mb-2">Merchant Email</label>
          <input
            type="email"
            name="merch_email"
            placeholder="Merchant Email"
            value={formData.merch_email}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="amount" className="block text-gray-700 text-sm font-bold mb-2">Payment Amount</label>
          <input
            type="number"
            name="amount"
            placeholder="Payment Amount"
            value={formData.amount}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <button type="submit" className="bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 w-full font-semibold">
          Send Payment
        </button>

        {message && <p className="mt-4 text-center text-gray-600">{message}</p>}
      </form>
    </div>
  );
};

export default BankPage;
