import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';
import ShiokorityPayLogo from '../asset/image/ShiokorityPay.png';

const RegisterConsumer = () => {
  const [formData, setFormData] = useState({
    cust_email: '',
    cust_pass: '',
    cust_fname: '',
    cust_lname: '',
    cust_phone: '',
    cust_address: ''
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await consumerController.registerConsumer(formData);
      setMessage(response.message);
      if (response.success) {
        navigate('/login-consumer');
      }
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleLogoClick = () => {
    navigate('/login-consumer');
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        <img
          src={ShiokorityPayLogo}
          alt="Shiokority Pay"
          className="h-20 mb-5 cursor-pointer"
          onClick={handleLogoClick}
        />
        <h3 className="text-3xl font-bold mb-6 text-[#153247]">Consumer Registration</h3>

        <div className="mb-4">
          <label htmlFor="cust_email" className="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input
            type="email"
            name="cust_email"
            placeholder="Email"
            value={formData.cust_email}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="cust_pass" className="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input
            type="password"
            name="cust_pass"
            placeholder="Password"
            value={formData.cust_pass}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="cust_fname" className="block text-gray-700 text-sm font-bold mb-2">First Name</label>
          <input
            type="text"
            name="cust_fname"
            placeholder="First Name"
            value={formData.cust_fname}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="cust_lname" className="block text-gray-700 text-sm font-bold mb-2">Last Name</label>
          <input
            type="text"
            name="cust_lname"
            placeholder="Last Name"
            value={formData.cust_lname}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="cust_phone" className="block text-gray-700 text-sm font-bold mb-2">Phone</label>
          <input
            type="text"
            name="cust_phone"
            placeholder="Phone"
            value={formData.cust_phone}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="cust_address" className="block text-gray-700 text-sm font-bold mb-2">Address</label>
          <input
            type="text"
            name="cust_address"
            placeholder="Address"
            value={formData.cust_address}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <button type="submit" className="w-full bg-[#153247] text-white font-semibold py-2 rounded-lg hover:bg-[#1e4b64] focus:outline-none focus:ring-2 focus:ring-[#153247] focus:ring-offset-2">
          Submit
        </button>

        {message && <p className="mt-4 text-center text-gray-600">{message}</p>}
        <div className="text-center mt-4">
          <a href="/" className="text-sm text-[#153247] hover:text-[#1e4b64] hover:underline">
            Back
          </a>
        </div>
      </form>
    </div>
  );
};

export default RegisterConsumer;
