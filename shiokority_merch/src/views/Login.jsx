import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import merchantController from '../controller/merchantController';

const Login = () => {
  const [formData, setFormData] = useState({
    merch_email: '',
    password: ''
  });
  const [message, setMessage] = useState('');
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await merchantController.login(formData);
      setMessage(response.message);
      if (response.success) {
        navigate('/profile'); // Redirect to profile page on success
      }
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
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
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}

      <p>Don't have an account? <button onClick={() => navigate('/register')}>Register</button></p>
    </div>
  );
};

export default Login;