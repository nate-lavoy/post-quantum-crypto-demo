import { Layout, Menu } from 'antd';
import { Link } from 'react-router-dom';
import './DashboardPage.css'; // Import the custom CSS file

const { Sider, Content } = Layout;

const DashboardPage = () => {
  return (
    <Layout className="dashboard-container">
      {/* Sidebar */}
      <Sider className="dashboard-sider">
        <div className="dashboard-logo">NYU HR</div>
        <Menu theme="dark" mode="inline" className="dashboard-menu">
          <Menu.Item key="1">
            <Link to="/dashboard">Home</Link>
          </Menu.Item>
          <Menu.Item key="2">
            <Link to="/user-info">User Info</Link>
          </Menu.Item>
        </Menu>
      </Sider>

      {/* Main Content */}
      <Content className="dashboard-content">
        <h1 className="dashboard-title">Welcome to Your Dashboard</h1>
        <p className="dashboard-description">Here you can manage your account and view information.</p>
      </Content>
    </Layout>
  );
};

export default DashboardPage;
