import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './Dashboard'
import Login from './login'

const queryClient = new QueryClient()

function App() {
  return (
      <QueryClientProvider client={queryClient}>
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </Router>
      </QueryClientProvider>
  );
}


export default App;