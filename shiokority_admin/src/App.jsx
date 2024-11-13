import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Dashboard from './views/Dashboard';
import Login from './views/Login';
import EditMerchant from './views/EditMerchant';
import ViewManagement from './views/viewManagement';
import CreateMerchant from './views/CreateMerchant';
import Setup2FA from './views/Setup2FA';
import Verify2FA from './views/Verify2FA';
import CreateUser from './views/CreateUser';
import EditUser from './views/EditUser';
import AuditTrail from './views/AuditTrail';
const ProtectedRoute = () => {
  const isLoggedIn = localStorage.getItem('isAdminLoggedIn') === 'true';
  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Login />} />
      
      {/* Protected Merchant Routes */}
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/user-management" element={<ViewManagement />} />
        <Route path="/edit-merchant/:merchId" element={<EditMerchant />} />
        <Route path="/edit-user/:userId" element={<EditUser />} />
        <Route path="/create-merchant" element={<CreateMerchant />} />
        <Route path="/create-user" element={<CreateUser />} />
        <Route path="/setup2FA" element={<Setup2FA />} />
        <Route path="/verify2FA" element={<Verify2FA />} />
        <Route path="/auditTrail" element={<AuditTrail />} />
      </Route>
    </Routes>
  );
}

export default App;
