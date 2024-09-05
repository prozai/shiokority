import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './views/Dashboard'
import Login from './views/Login'
import EditMerchant from './views/EditMerchant'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/edit-merchant/:merchId" element={<EditMerchant />} />
      </Routes>
    </Router>
  );
}

export default App;