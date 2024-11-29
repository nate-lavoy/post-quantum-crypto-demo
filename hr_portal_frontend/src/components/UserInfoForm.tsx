// src/components/UserInfoForm.tsx
import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Space } from 'antd';
import { UserData, UserInfoFormProps, FormItem } from '../api/user';

const UserInfoForm: React.FC<UserInfoFormProps> = ({ 
  data, 
  onSubmit, 
  isLoading 
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [form] = Form.useForm<UserData>();

  useEffect(() => {
    if (data) {
      form.setFieldsValue(data);
    }
  }, [data, form]);

  const handleCancel = () => {
    form.setFieldsValue(data || {});
    setIsEditing(false);
  };

  const formItems: FormItem[] = [
    { 
      name: "first_name", 
      label: "First Name", 
      rules: [{ required: true, message: 'First Name is required' }] 
    },
    { 
      name: "last_name", 
      label: "Last Name", 
      rules: [{ required: true, message: 'Last Name is required' }] 
    },
    { 
      name: "age", 
      label: "Age", 
      rules: [{ pattern: /^[0-9]+$/, message: 'Age must be numeric' }],
      inputType: "number"
    },
    { name: "sex", label: "Sex" },
    { name: "sexual_orientation", label: "Sexual Orientation" },
    { name: "preferred_pronouns", label: "Preferred Pronouns" },
    { 
      name: "phone_number", 
      label: "Phone Number", 
      rules: [{ pattern: /^[0-9]+$/, message: 'Phone number must be numeric' }] 
    },
    { 
      name: "ssn", 
      label: "SSN", 
      rules: [{ pattern: /^\d{3}-?\d{2}-?\d{4}$/, message: 'Invalid SSN format' }] 
    }
  ];

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={(values: UserData) => {
        onSubmit(values);
        setIsEditing(false);
      }}
    >
      {formItems.map(item => (
        <Form.Item
          key={item.name}
          name={item.name}
          label={item.label}
          rules={item.rules}
        >
          <Input
            type={item.inputType || "text"}
            disabled={!isEditing}
          />
        </Form.Item>
      ))}

      <Form.Item>
        <Space>
          {!isEditing ? (
            <Button 
              type="primary" 
              onClick={() => setIsEditing(true)}
              disabled={isLoading}
            >
              Edit
            </Button>
          ) : (
            <>
              <Button 
                type="primary" 
                htmlType="submit"
                loading={isLoading}
              >
                Save Changes
              </Button>
              <Button 
                onClick={handleCancel}
                disabled={isLoading}
              >
                Cancel
              </Button>
            </>
          )}
        </Space>
      </Form.Item>
    </Form>
  );
};

export default UserInfoForm;