import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import consumerController from '../controller/consumerController';


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

  return (
    <div>
      <h2>Consumer Registration</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="cust_email"
          placeholder="Email"
          value={formData.cust_email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="cust_pass"
          placeholder="Password"
          value={formData.cust_pass}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="cust_fname"
          placeholder="First Name"
          value={formData.cust_fname}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="cust_lname"
          placeholder="Last Name"
          value={formData.cust_lname}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="cust_phone"
          placeholder="Phone"
          value={formData.cust_phone}
          onChange={handleChange}
        />
        <input
          type="text"
          name="cust_address"
          placeholder="Address"
          value={formData.cust_address}
          onChange={handleChange}
        />
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default RegisterConsumer;