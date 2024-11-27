import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { login, signup } from '../api/auth';
import { Tabs } from 'antd';

const LoginSignupPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('login');

  const handleLogin = async (values: any) => {
    try {
      const response = await login(values);
      localStorage.setItem('jwt', response.data.access_token);
      navigate('/dashboard');
    } catch (error) {
      console.error(error);
    }
  };

  const handleSignup = async (values: any) => {
    try {
      await signup(values);
      setActiveTab('login'); // Switch to login tab after successful signup.
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto' }}>
      <Tabs activeKey={activeTab} onChange={setActiveTab}>
        <Tabs.TabPane tab="Login" key="login">
          <AuthForm onSubmit={handleLogin} />
        </Tabs.TabPane>
        <Tabs.TabPane tab="Signup" key="signup">
          <AuthForm onSubmit={handleSignup} />
        </Tabs.TabPane>
      </Tabs>
    </div>
  );
};

export default LoginSignupPage;