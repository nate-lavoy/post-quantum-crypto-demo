import React, { useState } from 'react';
import { Form, Input, Button } from 'antd';

interface UserInfoFormProps {
  data: any;
  onSubmit: (values: any) => void;
}

const UserInfoForm: React.FC<UserInfoFormProps> = ({ data, onSubmit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [form] = Form.useForm(); // Use Ant Design's form instance

  // Handle cancel action
  const handleCancel = () => {
    form.resetFields(); // Reset form fields to initial values
    setIsEditing(false); // Exit edit mode
  };

  return (
    <Form
      form={form}
      initialValues={data}
      layout="vertical"
      onFinish={(values) => {
        onSubmit(values); // Call parent handler
        setIsEditing(false); // Exit edit mode after saving
      }}
    >
      <Form.Item name="first_name" label="First Name" rules={[{ required: true, message: 'First Name is required' }]}>
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="last_name" label="Last Name" rules={[{ required: true, message: 'Last Name is required' }]}>
        <Input disabled={!isEditing} />
      </Form.Item>
      <Form.Item name="age" label="Age" rules={[{ type: 'number', message: 'Age must be a number' }]}>
        <Input type="number" disabled={!isEditing} />
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
      <Form.Item name="phone_number" label="Phone Number" rules={[{ pattern: /^[0-9]+$/, message: 'Phone number must be numeric' }]}>
        <Input disabled={!isEditing} />
      </Form.Item>

      {/* Buttons */}
      {!isEditing ? (
        <Button type="primary" onClick={() => setIsEditing(true)}>
          Edit
        </Button>
      ) : (
        <>
          <Button type="primary" htmlType="submit" style={{ marginRight: 8 }}>
            Save
          </Button>
          <Button onClick={handleCancel}>Cancel</Button>
        </>
      )}
    </Form>
  );
};

export default UserInfoForm;
