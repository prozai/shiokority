import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';
import ShiokorityMerchLogo from '../asset/image/ShiokorityMerch.png';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [status, setStatus] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Logging in...');
    try {
      await merchantController.login(formData);
      setStatus('Login successful');
      navigate('/dashboard'); // Redirect to the dashboard after successful login
    } catch (error) {
      setStatus('Login failed: ' + error.message);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(prevState => !prevState);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <div className="flex justify-center mb-8">
          <img src={ShiokorityMerchLogo} alt="Shiokority Merch" className="h-40" />
        </div>
        {status && <p className="text-center text-red-500 mb-4">{status}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
              className="border border-gray-300 rounded-lg w-full py-2 px-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#153247]"
            />
          </div>
          <div className="mb-6 relative">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              className="border border-gray-300 rounded-lg w-full py-2 px-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#153247]"
            />
            <span onClick={togglePasswordVisibility} className="absolute right-4 top-2 cursor-pointer">
              {showPassword ? <VisibleIcon /> : <InvisibleIcon />}
            </span>
          </div>
          <button type="submit" className="bg-[#153247] text-white font-bold py-3 px-6 rounded-full w-full">
            Login
          </button>
        </form>
        <p className="text-center mt-4">
          Don't have an account?{' '}
          <button className="text-[#153247] hover:underline" onClick={() => navigate('/register')}>
            Create New Account
          </button>
        </p>
        <div className="text-center mt-4 border-t pt-4">
          <p className="text-gray-600 mb-2">Are you a consumer?</p>
          <button 
            onClick={() => navigate('/login-consumer')}
            className="bg-gray-100 text-[#153247] font-bold py-2 px-6 rounded-full hover:bg-gray-200 w-full"
          >
            Go to Consumer Login
          </button>
        </div>
      </div>
    </div>
  );
};

const VisibleIcon = () => (
  <svg className="h-6 w-6 text-gray-500" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
    <path d="M17.94 17.94A10.015 10.015 0 0 0 21 12a10.015 10.015 0 0 0-4-7.94M12 3C7.03 3 2.53 7.03 1.05 12A10.016 10.016 0 0 0 4 17.94M12 3c4.97 0 9.47 4.03 10.95 9a10.015 10.015 0 0 1-4 7.94M15 12a3 3 0 1 1-3-3" />
    <path d="M1 1l22 22" />
  </svg>
);

const InvisibleIcon = () => (
  <svg className="h-6 w-6 text-gray-500" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
    <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
);

export default Login;
