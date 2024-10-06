// src/components/LoginPage.jsx
import React from 'react';
import logo from '../assets/logo.png'; // Assuming the logo image is in the assets folder

const LoginPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-customBlue">  {/* Custom background color */}
      <div className="w-full max-w-md">
        <div className="bg-white shadow-lg rounded-lg px-12 py-10">
          {/* Logo Section */}
          <div className="flex justify-center mb-8">
            <img src={logo} alt="Shiokority Admin" className="w-24 h-24"/>
          </div>

          {/* Form Section */}
          <h2 className="text-2xl font-semibold text-center mb-6">Login</h2>

          <form>
            {/* Email Input */}
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                Email
              </label>
              <input
                type="email"
                id="email"
                placeholder="Enter your email"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>

            {/* Password Input */}
            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input
                type="password"
                id="password"
                placeholder="Enter your password"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>

            {/* Submit Button */}
            <div className="flex items-center justify-center">
              <button
                type="submit"
                className="bg-gray-800 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline hover:bg-gray-700 transition duration-300 w-full"
              >
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
