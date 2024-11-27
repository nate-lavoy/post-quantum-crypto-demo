import { useEffect, useState } from 'react';
import { getUserInfo, updateUserInfo } from '../api/user';
import UserInfoForm from '../components/UserInfoForm';
import './UserInfoPage.css'; // Import the custom CSS file

const UserInfoPage = () => {
  const [userData, setUserData] = useState<any>(null);
  const [loading, setLoading] = useState(true); // Track loading state
  const [error, setError] = useState<string | null>(null); // Track errors

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = sessionStorage.getItem('jwt');
        if (!token) {
          throw new Error('JWT token not found. Please log in again.');
        }

        console.log('Fetching user info...');
        const response = await getUserInfo(token);

        console.log('Response received:', response);
        setUserData(response.data); // Set user data
      } catch (err: any) {
        console.error('Error fetching user info:', err);
        setError(err.message || 'Failed to fetch user info.');
      } finally {
        setLoading(false); // Stop loading spinner
      }
    };

    fetchData();
  }, []);

  const handleUpdate = async (values: any) => {
    try {
      const token = sessionStorage.getItem('jwt');
      if (!token) {
        throw new Error('JWT token not found. Please log in again.');
      }

      console.log('Updating user info...');
      await updateUserInfo(token, values);

      console.log('User info updated successfully.');
      setUserData(values); // Update local state after successful submission
    } catch (err: any) {
      console.error('Error updating user info:', err);
      setError(err.message || 'Failed to update user info.');
    }
  };

  if (loading) {
    return <p className="loading-text">Loading...</p>; // Show loading spinner
  }

  if (error) {
    return <p className="error-text">{error}</p>; // Show error message
  }

  return (
    <div className="user-info-container">
      <div className="user-info-card">
        <h1 className="user-info-title">Your Profile</h1>
        <UserInfoForm data={userData} onSubmit={handleUpdate} />
      </div>
    </div>
  );
};

export default UserInfoPage;
