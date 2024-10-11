import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './views/Login';
import Register from './views/Register';
import Dashboard from './views/Dashboard'
import Profile from './views/Profile';
import BankPage from './views/BankPage';
import TransactionHistory from './views/TransactionHistory';
import LoginConsumer from './views/loginConsumer';
import ProfileConsumer from './views/profileConsumer';
import RegisterConsumer from './views/registerConsumer';
//import './index.css';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/bankpage" element={<BankPage />} />
        <Route path="/transactions" element={<TransactionHistory />} />
        <Route path="/login-consumer" element={<LoginConsumer />} />
        <Route path="/profile-consumer" element={<ProfileConsumer />} />
        <Route path="/register-consumer" element={<RegisterConsumer />} />
        

        {/* Default route */}
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;