import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';
import ShiokorityMerchLogo from '../asset/image/ShiokorityMerch.png';

const Register = () => {
  const [formData, setFormData] = useState({
    merch_email: '',
    merch_pass: '',
    merch_name: '',
    merch_phone: '',
    merch_address: '',
    uen: ''
  });
  const [message, setMessage] = useState('');
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await merchantController.registerMerchant(formData);
      setMessage(response.message);
      if (response.success) {
        navigate('/login');
      }
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleLogoClick = () => {
    navigate('/login');
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        {/* Logo at the top left */}
        <img
          src={ShiokorityMerchLogo}
          alt="Shiokority Merch"
          className="h-20 mr-1 cursor-pointer"
          onClick={handleLogoClick}
        />
        <h3 className="text-3xl font-bold mb-6 text-[#153247]">Register</h3>

        <div className="mb-4">
          <label htmlFor="merch_email" className="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input
            type="email"
            name="merch_email"
            placeholder="Email"
            value={formData.merch_email}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="merch_pass" className="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input
            type="password"
            name="merch_pass"
            placeholder="Password"
            value={formData.merch_pass}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="merch_name" className="block text-gray-700 text-sm font-bold mb-2">Name</label>
          <input
            type="text"
            name="merch_name"
            placeholder="Name"
            value={formData.merch_name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="merch_phone" className="block text-gray-700 text-sm font-bold mb-2">Phone</label>
          <input
            type="text"
            name="merch_phone"
            placeholder="Phone"
            value={formData.merch_phone}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="merch_address" className="block text-gray-700 text-sm font-bold mb-2">Address</label>
          <input
            type="text"
            name="merch_address"
            placeholder="Address"
            value={formData.merch_address}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="uen" className="block text-gray-700 text-sm font-bold mb-2">UEN</label>
          <input
            type="text"
            name="uen"
            placeholder="UEN"
            value={formData.uen}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <button type="submit" className="w-full bg-[#153247] text-white font-semibold py-2 rounded-lg hover:bg-[#1e4b64] focus:outline-none focus:ring-2 focus:ring-[#153247] focus:ring-offset-2">
          Submit
        </button>

        {message && <p className="mt-4 text-center text-gray-600">{message}</p>}
          <div className="text-center">
          <a href="/" className="text-sm text-[#153247] hover:text-[#1e4b64] hover:underline">
            Back
          </a>
          </div>
      </form>
    </div>
  
  );
};

export default Register;
