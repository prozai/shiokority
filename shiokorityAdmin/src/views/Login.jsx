import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  const loginMutation = useMutation({
    mutationFn: (loginData) =>
      axios.post('/login/admin', loginData),
    onSuccess: (data) => {
      console.log('Login successful:', data);
      // Handle successful login (e.g., redirect, store token)
      navigate('/dashboard');
    },
    onError: (error) => {
      console.error('Login failed:', error);
      // Handle error (e.g., display error message)
      setStatus('Login failed')
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    loginMutation.mutate({ email, password });
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
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
