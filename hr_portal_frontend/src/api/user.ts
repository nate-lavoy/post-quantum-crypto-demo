// src/api/user.ts
import axios, { AxiosResponse } from 'axios';
import type { Rule } from 'antd/es/form';

export interface UserData {
  first_name?: string;
  last_name?: string;
  age?: number;
  sex?: string;
  sexual_orientation?: string;
  preferred_pronouns?: string;
  phone_number?: string;
  ssn?: string;
}

export interface ApiResponse {
  data?: UserData;
  private_key?: string;
}

export interface UserInfoFormProps {
  data: UserData | null;
  onSubmit: (values: UserData) => void;
  isLoading: boolean;
}

export interface FormItem {
  name: keyof UserData;
  label: string;
  rules?: Rule[];
  inputType?: string;
}

const BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getUserInfo = async (
  token: string, 
  privateKey: string
): Promise<AxiosResponse<UserData>> => {
  return api.post('/me/info/decrypt', 
    { private_key: privateKey },
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );
};

export const updateUserInfo = async (
  token: string, 
  data: UserData
): Promise<AxiosResponse<ApiResponse>> => {
  return api.put('/me/info',
    data,
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );
};

export const checkUserInfoStatus = async (
  token: string
): Promise<AxiosResponse<{ has_info: boolean }>> => {
  return api.get('/me/info/status', {
    headers: { Authorization: `Bearer ${token}` },
  });
};