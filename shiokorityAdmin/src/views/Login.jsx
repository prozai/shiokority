import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AdministratorController from '../controller/administratorController';

const Login = () => {
  const [controller] = useState(() => new AdministratorController());
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    setStatus(controller.status);
  }, [controller.status]);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    controller.setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    controller.setPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await controller.handleLogin(e, navigate);
  };

  return (  
    <div>
      <h2>Login</h2>
      {status && <p>{status}</p>} 
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={handleEmailChange}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;