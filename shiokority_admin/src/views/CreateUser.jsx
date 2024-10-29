// src/views/CreateUser.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';

const AdminAddUser = () => {
  const navigate = useNavigate(); 
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    address: '',
    phone: '',
    status: true
  });
  const [statusMessage, setStatusMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage('Adding user...');
    try {
      const response = await AdministratorController.addUser(formData);
      setStatusMessage(response.message);
      setFormData({ email: '', password: '', first_name: '', last_name: '', address: '', phone: '', status: true});
    } catch (error) {
      setStatusMessage(error.message);
    }
  };

  const handleCancel = () => {
    navigate('/user-management');  // Navigate back to user-management
};

  return (
    <div className="p-6 bg-gray-100 min-h-screen flex justify-center items-center">
      <form onSubmit={handleSubmit} className="w-full max-w-lg bg-white p-8 rounded-lg shadow-lg">
        <h3 className="text-2xl font-bold mb-6">Add User</h3>

        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="User Email"
            value={formData.email}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="User Password"
            value={formData.password}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="first_name" className="block text-gray-700 text-sm font-bold mb-2">First Name</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            placeholder="User First Name"
            value={formData.first_name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="last_name" className="block text-gray-700 text-sm font-bold mb-2">Last Name</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            placeholder="User Last Name"
            value={formData.last_name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="address" className="block text-gray-700 text-sm font-bold mb-2">Address</label>
          <input
            type="text"
            id="address"
            name="address"
            placeholder="User Address"
            value={formData.address}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="phone" className="block text-gray-700 text-sm font-bold mb-2">Phone</label>
          <input
            type="text"
            id="phone"
            name="phone"
            placeholder="User Phone Number"
            value={formData.phone}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="status" className="block text-gray-700 text-sm font-bold mb-2">Status</label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value={true}>Active</option>
            <option value={false}>Deactivated</option>
          </select>
        </div>

        <button
          type="submit"
          className="bg-[#153247] text-white py-2 px-4 rounded-lg hover:bg-green-600 w-full font-semibold"
        >
          + Add User
        </button>

        <button type="button" onClick={handleCancel} className="bg-gray-400 text-white py-2 px-4 rounded w-full mt-2 hover:bg-gray-500 font-semibold">
                    Cancel
                </button>

        {statusMessage && <p className="mt-4 text-center text-gray-600">{statusMessage}</p>}
      </form>
    </div>
  );
};

export default AdminAddUser;
