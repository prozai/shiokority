import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';
import ShiokorityPayLogo from '../asset/image/ShiokorityPay.png'; // Assuming there's a logo for consumer as well

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
        navigate('/login-consumer'); // Redirect to login page on successful registration
      }
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleLogoClick = () => {
    navigate('/login-consumer'); // Redirect to login for consumer
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-[#153247] p-6">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        {/* Logo at the top left */}
        <img
          src={ShiokorityPayLogo} // Use appropriate logo
          alt="Shiokority Pay"
          className="h-20 mb-4 cursor-pointer"
          onClick={handleLogoClick}
        />
        <h3 className="text-3xl font-bold mb-6 text-[#153247]">Register</h3>

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
            required
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
            required
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

        <button type="submit" className="bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 w-full font-semibold">
          Register
        </button>

        {message && <p className="mt-4 text-center text-gray-600">{message}</p>}
      </form>
    </div>
  );
};

export default RegisterConsumer;
