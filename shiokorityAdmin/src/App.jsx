import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './Dashboard'
import Login from './login'
import EditMerchant from './EditMerchant'

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