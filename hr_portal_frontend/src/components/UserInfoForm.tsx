import React, { useState } from 'react';
import { Form, Input, Button } from 'antd';

interface UserInfoFormProps {
  data: any;
  onSubmit: (values: any) => void;
}

const UserInfoForm: React.FC<UserInfoFormProps> = ({ data, onSubmit }) => {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <Form initialValues={data} layout="vertical" onFinish={onSubmit}>
      <Form.Item name="first_name" label="First Name">
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="last_name" label="Last Name">
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="age" label="Age">
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="sex" label="Sex">
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="sexual_orientation" label="Sexual Orientation">
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="preferred_pronouns" label="Preferred Pronouns">
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="phone_number" label="Phone Number">
        <Input disabled={!isEditing} />
      </Form.Item>
      <Button type="primary" onClick={() => setIsEditing(true)} style={{ marginRight: 8 }}>
        Edit
      </Button>
      {isEditing && (
        <>
          <Button type="primary" htmlType="submit" style={{ marginRight: 8 }}>
            Save
          </Button>
          <Button onClick={() => setIsEditing(false)}>Cancel</Button>
        </>
      )}
    </Form>
  );
};

export default UserInfoForm;