import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';
// Import your logo image
import ShiokorityMerchLogo from '../asset/image/ShiokorityMerch.png';

const Login = () => {
  const [formData, setFormData] = useState({
    merch_email: '',
    password: ''
  });
  const [status, setStatus] = useState('');
  const [showPassword, setShowPassword] = useState(false); // Track password visibility
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
      navigate('/profile'); // Navigate to the profile page
    } catch (error) {
      setStatus('Login failed: ' + error.message);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prevState) => !prevState); // Toggle password visibility
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
    <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        
         {/* Logo */}
         <div className="flex justify-center mb-8">
          {/* Update the src to use the imported image */}
          <img src={ShiokorityMerchLogo} alt="Shiokority Merch" className="h-40" />
        </div>

         {/* Status Message */}
         {status && <p className="text-center text-red-500 mb-4">{status}</p>}

         {/* Form */}
         <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="email" className="sr-only">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Email"
              className="appearance-none border border-gray-300 rounded-lg w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-[#153247]"
            />
          </div>

          <div className="mb-6 relative">
            <label htmlFor="password" className="sr-only">Password:</label>
            <input
              type={showPassword ? "text" : "password"}  // Toggle between "password" and "text"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Password"
              className="appearance-none border border-gray-300 rounded-lg w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-[#153247]"
            />
           {/* Eye Icon to toggle password visibility */}
           <span 
              className="absolute right-4 top-2 cursor-pointer"
              onClick={togglePasswordVisibility}
            >
              {showPassword ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M17.94 17.94A10.015 10.015 0 0 0 21 12a10.015 10.015 0 0 0-4-7.94M12 3C7.03 3 2.53 7.03 1.05 12A10.016 10.016 0 0 0 4 17.94M12 3c4.97 0 9.47 4.03 10.95 9a10.015 10.015 0 0 1-4 7.94M15 12a3 3 0 1 1-3-3" />
                  <path d="M1 1l22 22" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              )}
            </span>
          </div>

          <div className="flex items-center justify-center">
            <button
              type="submit"
              className="bg-[#153247] hover:bg-[#122c3c] text-white font-bold py-3 px-6 rounded-full focus:outline-none focus:shadow-outline w-full"
            >
              Login
            </button>
          </div>
        </form>

        {/* Register Link */}
        <p className="text-center mt-4">
          Don't have an account?{' '}
          <button className="text-[#153247] hover:underline" onClick={() => navigate('/register')}>
            Create New account
          </button>
        </p>
      </div>
    </div>
  );
};

export default Login;
