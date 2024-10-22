// src/views/EditUser.jsx
import React, { useState, useEffect } from 'react';
import AdministratorController from '../controller/administratorController';
import { useParams, useNavigate } from 'react-router-dom';

const EditUser = () => {
  const { cust_id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    address: '',
    phone: '',
    status: ''
  });
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserDetails = async () => {
      setStatusMessage('Loading user details...');
      try {
        const user = await AdministratorController.getUserById(cust_id);
        if (user) {
          setFormData({
            email: user.cust_email,
            first_name: user.cust_fname,
            last_name: user.cust_lname,
            address: user.cust_address,
            phone: user.cust_phone,
            status: user.cust_status
          });
        }
        setStatusMessage('');
      } catch (error) {
        setError('Failed to load user details.');
      }
    };

    fetchUserDetails();
  }, [cust_id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage('Updating user...');
    try {
      const response = await AdministratorController.updateUser(cust_id, formData);
      setStatusMessage(response.success ? 'User updated successfully.' : 'Failed to update user.');
      if (response.success) navigate('/dashboard');
    } catch {
      setError('Error occurred while updating the user.');
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen flex justify-center items-center">
      <form onSubmit={handleSubmit} className="w-full max-w-lg bg-white p-8 rounded-lg shadow-lg">
        <h3 className="text-2xl font-bold mb-6 text-[#153247]">Edit User</h3>
        {['email', 'first_name', 'last_name', 'address', 'phone'].map((field) => (
          <div className="mb-4" key={field}>
            <label className="block text-gray-700 text-sm font-bold mb-2 capitalize">{field.replace('_', ' ')}</label>
            <input
              type={field === 'email' ? 'email' : 'text'}
              name={field}
              value={formData[field]}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>
        ))}
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Status</label>
          <select
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="1">Active</option>
            <option value="0">Deactivated</option>
          </select>
        </div>
        <button type="submit" className="bg-[#153247] text-white py-2 px-4 rounded w-full hover:bg-green-600 font-semibold">
          Update 
        </button>
        <button type="button" onClick={() => navigate('/user-management')} className="bg-gray-400 text-white py-2 px-4 rounded w-full mt-2 hover:bg-gray-500 font-semibold">
          Cancel
        </button>
        {statusMessage && <p className="mt-4 text-center text-gray-600">{statusMessage}</p>}
        {error && <p className="mt-4 text-center text-red-600">{error}</p>}
      </form>
    </div>
  );
};

export default EditUser;
