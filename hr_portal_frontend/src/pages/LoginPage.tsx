import { useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { login, signup } from '../api/auth';

const LoginPage = () => {
  const navigate = useNavigate();

  const handleLogin = async (values: any) => {
    try {
      const response = await login(values);
      sessionStorage.setItem('jwt', response.data.access_token);
      navigate('/dashboard');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto' }}>
      <h1>Login</h1>
      <AuthForm onSubmit={handleLogin} />
    </div>
  );
};

export default LoginPage;