import React, { useState } from 'react';
import AdministratorController from '../controller/administratorController'; // Assuming you have a controller

const AdminAddUser = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    status: true // Default to 'true' for active status
  });
  const [statusMessage, setStatusMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: name === 'status' ? value === 'true' : value // Convert 'status' to boolean
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage('Adding user...');

    try {
      await AdministratorController.addUser(formData);
      setStatusMessage('User added successfully');
    } catch (error) {
      setStatusMessage('Failed to add user: ' + error.message);
    }
  };

  return (
    <div>
      <h2>Add User</h2>
      {statusMessage && <p>{statusMessage}</p>}
      <form onSubmit={handleSubmit}>
      <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>  
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="first_name">First Name:</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="last_name">Last Name:</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="status">Status:</label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value={true}>Active</option>
            <option value={false}>Deactivated</option>
          </select>
        </div>
        <button type="submit">Add User</button>
      </form>
    </div>
  );
};

export default AdminAddUser;