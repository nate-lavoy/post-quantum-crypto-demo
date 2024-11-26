import { useEffect, useState } from 'react';
import { getUserInfo, updateUserInfo } from '../api/user';
import UserInfoForm from '../components/UserInfoForm';

const UserInfoPage = () => {
  const [userData, setUserData] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      const token = sessionStorage.getItem('jwt');
      if (token) {
        const response = await getUserInfo(token);
        setUserData(response.data);
      }
    };
    fetchData();
  }, []);

  const handleUpdate = async (values: any) => {
    const token = sessionStorage.getItem('jwt');
    if (token) {
      await updateUserInfo(token, values);
      setUserData(values); // Update local state after successful submission.
    }
  };

  return userData ? (
    <div style={{ maxWidth: 600, margin: 'auto' }}>
      <h1>User Info</h1>
      <UserInfoForm data={userData} onSubmit={handleUpdate} />
    </div>
  ) : (
    <p>Loading...</p>
  );
};

export default UserInfoPage;