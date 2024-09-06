import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './views/Dashboard'
import Login from './views/Login'
import Adminstrator from './model/administrator';
import EditMerchant from './views/EditMerchant'


const PrivateRoute = ({ children }) => {
  const isAuthenticated = Adminstrator.isLoggedIn(); // You'll need to implement this method
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route 
            path="/dashboard" 
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route 
            path="/edit-merchant/:merchId" 
            element={
              <PrivateRoute>
                <EditMerchant />
              </PrivateRoute>
            }
          />
      </Routes>
    </Router>
  );
}

export default App;