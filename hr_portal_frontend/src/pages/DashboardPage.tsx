import { Layout, Menu } from 'antd';
import { Link } from 'react-router-dom';

const DashboardPage = () => {
  return (
    <Layout style={{ height: '100vh' }}>
      <Layout.Sider>
        <Menu theme="dark">
          <Menu.Item key="1">
            <Link to="/dashboard">Home</Link>
          </Menu.Item>
          <Menu.Item key="2">
            <Link to="/user-info">User Info</Link>
          </Menu.Item>
        </Menu>
      </Layout.Sider>
      <Layout.Content style={{ padding: '20px' }}>
        <h1>Hello User</h1>
      </Layout.Content>
    </Layout>
  );
};

export default DashboardPage;