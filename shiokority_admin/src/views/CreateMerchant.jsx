// src/views/CreateMerchant.jsx
import React, { useState } from 'react';
import AdministratorController from '../controller/administratorController';

const MerchantForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    uen: '',
  });
  const [status, setStatus] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Submitting...');
    try {
      await AdministratorController.createMerchant(formData);
      setStatus('Merchant created successfully!');
      setFormData({ name: '', email: '', phone: '', address: '', uen: '' });
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen flex justify-center items-center">
      <form onSubmit={handleSubmit} className="w-full max-w-lg bg-white p-8 rounded-lg shadow-lg">
        <h3 className="text-2xl font-bold mb-6">Add Merchant</h3>

        <div className="mb-4">
          <label htmlFor="name" className="block text-gray-700 text-sm font-bold mb-2">Merchant Name</label>
          <input
            type="text"
            id="name"
            name="name"
            placeholder="Merchant Name"
            value={formData.name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="merchant@example.com"
            value={formData.email}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="phone" className="block text-gray-700 text-sm font-bold mb-2">Phone</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            placeholder="Merchant Phone Number"
            value={formData.phone}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="address" className="block text-gray-700 text-sm font-bold mb-2">Address</label>
          <input
            type="text"
            id="address"
            name="address"
            placeholder="Merchant Address"
            value={formData.address}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="uen" className="block text-gray-700 text-sm font-bold mb-2">UEN</label>
          <input
            type="text"
            id="uen"
            name="uen"
            placeholder="Unique Entity Number"
            value={formData.uen}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <button
          type="submit"
          className="bg-[#153247] text-white py-2 px-4 rounded-lg hover:bg-green-600 w-full font-semibold"
        >
          + Add Merchant
        </button>

        {status && <p className="mt-4 text-center text-gray-600">{status}</p>}
      </form>
    </div>
  );
};

export default MerchantForm;
