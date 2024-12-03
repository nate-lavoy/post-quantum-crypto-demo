// src/pages/UserInfoPage.tsx
import { useEffect, useState } from 'react';
import { message, Alert, Button, Input } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import { getUserInfo, updateUserInfo, checkUserInfoStatus } from '../api/user';
import UserInfoForm from '../components/UserInfoForm';
import { UserData } from '../api/user';
import './UserInfoPage.css';

const UserInfoPage = () => {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasInfo, setHasInfo] = useState<boolean>(false);
  const [privateKey, setPrivateKey] = useState<string>('');
  const [newPrivateKey, setNewPrivateKey] = useState<string | null>(null);

  useEffect(() => {
    checkExistingInfo();
  }, []);

  const checkExistingInfo = async () => {
    try {
      const token = sessionStorage.getItem('jwt');
      if (!token) throw new Error('JWT token not found. Please log in again.');

      const response = await checkUserInfoStatus(token);
      setHasInfo(response.data.has_info);
    } catch (err: any) {
      console.error('Error checking user info status:', err);
      message.error('Failed to check user information status');
    } finally {
      setLoading(false);
    }
  };

  const handleDecrypt = async () => {
    if (!privateKey.trim()) {
      message.error('Please enter your private key');
      return;
    }

    setLoading(true);
    try {
      const token = sessionStorage.getItem('jwt');
      if (!token) throw new Error('JWT token not found. Please log in again.');

      const response = await getUserInfo(token, privateKey);
      setUserData(response.data);
      setError(null);
      message.success('Data decrypted successfully');
    } catch (err: any) {
      console.error('Error decrypting user info:', err);
      setError('Invalid private key or decryption failed');
      message.error('Failed to decrypt data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (values: UserData) => {
    setLoading(true);
    try {
      const token = sessionStorage.getItem('jwt');
      if (!token) throw new Error('JWT token not found. Please log in again.');

      if (JSON.stringify(values) !== JSON.stringify(userData)) {
        const response = await updateUserInfo(token, values);
        
        if (response.data.private_key) {
          setNewPrivateKey(response.data.private_key);
        }
        
        message.success('Profile updated successfully');
      }
      
      setUserData(values);
      setError(null);
    } catch (err: any) {
      console.error('Error updating user info:', err);
      setError(err.response?.data?.detail || err.message);
      message.error('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadKey = () => {
    if (!newPrivateKey) return;
    
    const email = sessionStorage.getItem('email') || 'user';
    const filename = `${email.split('@')[0]}_privatekey.txt`;
    
    const blob = new Blob([newPrivateKey], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    message.success('Private key downloaded successfully!');
  };

  if (loading) {
    return <div className="user-info-container">Loading...</div>;
  }

  if (hasInfo && !userData) {
    return (
      <div className="user-info-container">
        <div className="user-info-card">
          <h1 className="user-info-title">Access Your Profile</h1>
          <div className="decrypt-form">
            <input
              type="password"
              value={privateKey}
              onChange={(e) => setPrivateKey(e.target.value)}
              placeholder="Enter your private key"
              className="decrypt-input"
            />
            <button 
              onClick={handleDecrypt}
              disabled={loading}
              className="decrypt-button"
            >
              Access Data
            </button>
            {error && <div className="error-message">{error}</div>}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="user-info-container">
      <div className="user-info-card">
        <h1 className="user-info-title">Your Profile</h1>
        {error && <div className="error-message">{error}</div>}
        {newPrivateKey && (
          <div className="private-key-section">
            <Alert
              message="Important: Download Your Private Key"
              description={
                <div>
                  <p>A new private key has been generated for your profile. Please download and keep it safe - you'll need it to access your information in the future.</p>
                  <div className="private-key-actions">
                    <Input.Password
                      value={newPrivateKey}
                      readOnly
                      className="private-key-input"
                    />
                    <Button
                      type="primary"
                      onClick={handleDownloadKey}
                      icon={<DownloadOutlined />}
                    >
                      Download Private Key
                    </Button>
                  </div>
                </div>
              }
              type="warning"
              showIcon
              className="private-key-alert"
            />
          </div>
        )}
        <UserInfoForm 
          data={userData} 
          onSubmit={handleSubmit}
          isLoading={loading}
        />
      </div>
    </div>
  );
};

export default UserInfoPage;