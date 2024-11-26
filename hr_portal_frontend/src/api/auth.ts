import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export const signup = (data: { email: string; password: string }) =>
  axios.post(`${BASE_URL}/signup`, data);

export const login = (data: { email: string; password: string }) =>
  axios.post(`${BASE_URL}/login`, data);

export const getCurrentUser = (token: string) =>
  axios.get(`${BASE_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });