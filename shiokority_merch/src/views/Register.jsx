import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';

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
        navigate('/login'); // Redirect to login page on successful registration
      }
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="merch_email"
          placeholder="Email"
          value={formData.merch_email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="merch_pass"
          placeholder="Password"
          value={formData.merch_pass}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="merch_name"
          placeholder="Name"
          value={formData.merch_name}
          onChange={handleChange}
        />
        <input
          type="text"
          name="merch_phone"
          placeholder="Phone"
          value={formData.merch_phone}
          onChange={handleChange}
        />
        <input
          type="text"
          name="merch_address"
          placeholder="Address"
          value={formData.merch_address}
          onChange={handleChange}
        />
        <input
          type="text"
          name="uen"
          placeholder="UEN"
          value={formData.uen}
          onChange={handleChange}
        />
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Register;