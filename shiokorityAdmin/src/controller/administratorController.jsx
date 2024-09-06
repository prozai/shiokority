import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Administrator from '../model/administrator';

export const useLoginController = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  const handleEmailChange = (e) => setEmail(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus('Logging in...');
    try {
      await Administrator.login(email, password);
      setStatus('Login successful');
      navigate('/dashboard');
    } catch (error) {
      setStatus('Login failed: ' + error.message);
    }
  };

  return {
    email,
    password,
    status,
    handleEmailChange,
    handlePasswordChange,
    handleSubmit
  };
};

export const useDashboardController = () => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        await Administrator.logout();
        navigate('/login');
    };

    return {
        handleLogout
    };
};