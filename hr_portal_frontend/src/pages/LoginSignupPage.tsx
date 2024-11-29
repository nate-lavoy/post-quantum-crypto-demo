import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { login, signup } from '../api/auth';
import { Tabs, message } from 'antd'; // Import message from antd
import './LoginSignupPage.css';

const LoginSignupPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('login');
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (values: any) => {
    try {
      setError(null); // Clear previous errors
      const response = await login(values);
      sessionStorage.setItem('jwt', response.data.access_token);
      navigate('/dashboard');
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Login failed. Please try again.';
      setError(errorMessage);
      message.error(errorMessage);
    }
  };

  const handleSignup = async (values: any) => {
    try {
      setError(null); // Clear previous errors
      await signup(values);
      message.success('Signup successful! Please login.');
      setActiveTab('login');
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Signup failed. Please try again.';
      setError(errorMessage);
      message.error(errorMessage);
    }
  };

  return (
    <div className="login-signup-container">
      <div className="login-signup-card">
        <h1 className="login-signup-title">NYU HR</h1>
        
        {error && <div className="error-message">{error}</div>}
        
        <Tabs
          activeKey={activeTab}
          onChange={(key) => {
            setActiveTab(key);
            setError(null); // Clear error when switching tabs
          }}
          centered
          className="custom-tabs"
        >
          <Tabs.TabPane tab="Login" key="login">
            <AuthForm onSubmit={handleLogin} />
          </Tabs.TabPane>
          <Tabs.TabPane tab="Signup" key="signup">
            <AuthForm onSubmit={handleSignup} />
          </Tabs.TabPane>
        </Tabs>
      </div>
    </div>
  );
};

export default LoginSignupPage;