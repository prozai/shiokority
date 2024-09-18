import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './views/Login';
import Register from './views/Register';
import Profile from './views/Profile';
import BankPage from './views/BankPage';
import TransactionHistory from './views/TransactionHistory';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/bankpage" element={<BankPage />} />
        <Route path="/transactionhistory" element={<TransactionHistory />} />

        {/* Default route */}
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;