import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Dashboard from './views/Dashboard'
import Login from './views/Login'
import EditMerchant from './views/EditMerchant'
import AdministratorController from './controller/administratorController';

const ProtectedRoute = () => {
  if (!AdministratorController.isLoggedIn()) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
};


function App() {

  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/edit-merchant/:merchId" element={<EditMerchant />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Route>
      
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;