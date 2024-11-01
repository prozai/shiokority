import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Login from './views/Login';
import Register from './views/Register';
import Dashboard from './views/Dashboard';
import Profile from './views/Profile';
import BankPage from './views/BankPage';
import TransactionHistory from './views/TransactionHistory';
import LoginConsumer from './views/loginConsumer';
import ProfileConsumer from './views/profileConsumer';
import RegisterConsumer from './views/registerConsumer';
import PayMerchant from './views/payMerch';

// Protected Route for Merchants
const MerchantRoute = () => {
  const isMerchantLogin = localStorage.getItem('isMerchantLoggedIn') === 'true';
  
  if (!isMerchantLogin) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};

// Protected Route for Consumers
const ConsumerRoute = () => {
  const isConsumerLogin = localStorage.getItem('isConsumerLoggedIn') === 'true';
  
  if (!isConsumerLogin) {
    return <Navigate to="/login-consumer" replace />;
  }
  return <Outlet />;
};



function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login-consumer" element={<LoginConsumer />} />
        <Route path="/register-consumer" element={<RegisterConsumer />} />
        <Route path="/" element={<Login />} />
        

        {/* Protected Merchant Routes */}
        <Route element={<MerchantRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/bankpage" element={<BankPage />} />
          <Route path="/transactions" element={<TransactionHistory />} />
        </Route>

        {/* Protected Consumer Routes */}
        <Route element={<ConsumerRoute />}>
          <Route path="/pay-merchant" element={<PayMerchant />} />
          <Route path="/profile-consumer/:pay_uen" element={<ProfileConsumer />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;