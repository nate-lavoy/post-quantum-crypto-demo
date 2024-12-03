import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginSignupPage from './pages/LoginSignupPage';
import DashboardPage from './pages/DashboardPage';
import UserInfoPage from './pages/UserInfoPage';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<LoginSignupPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/user-info" element={<UserInfoPage />} />
    </Routes>
  </Router>
);

export default App;