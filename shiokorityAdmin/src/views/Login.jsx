import React from 'react';
import { useLoginController } from '../controller/administratorController';

const Login = () => {
  const {
    email,
    password,
    status,
    handleEmailChange,
    handlePasswordChange,
    handleSubmit
  } = useLoginController();

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