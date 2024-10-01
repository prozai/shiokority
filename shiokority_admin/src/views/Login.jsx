import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [status, setStatus] = useState('');
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
      console.log(formData);
      await AdministratorController.login(formData);
      setStatus('Login successful');
      navigate('/dashboard');
    } catch (error) {
      setStatus('Login failed: ' + error.message);
    }
  };

  return (  
    <div>
      <h2>Login</h2>
      {status && <p>{status}</p>} 
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
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;