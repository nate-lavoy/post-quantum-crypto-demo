import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export const getUserInfo = (token: string) =>
  axios.get(`${BASE_URL}/me/info`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const updateUserInfo = (token: string, data: any) =>
  axios.put(`${BASE_URL}/me/info`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });