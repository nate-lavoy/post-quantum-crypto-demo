import React from 'react';
import { Form, Input, Button } from 'antd';

interface AuthFormProps {
  onSubmit: (values: { email: string; password: string }) => void;
}

const AuthForm: React.FC<AuthFormProps> = ({ onSubmit }) => {
  return (
    <Form onFinish={onSubmit} layout="vertical">
      <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
        <Input />
      </Form.Item>
      <Form.Item name="password" label="Password" rules={[{ required: true }]}>
        <Input.Password />
      </Form.Item>
      <Button type="primary" htmlType="submit">
        Submit
      </Button>
    </Form>
  );
};

export default AuthForm;