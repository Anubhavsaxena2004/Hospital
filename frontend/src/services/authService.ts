import axios from 'axios';

const API_URL = '/api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  department?: string;
  specialization?: string;
  phone_number?: string;
  is_on_duty: boolean;
}

export interface AuthResponse {
  user: User;
  token: string;
}

const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await axios.post(`${API_URL}/auth/login/`, credentials);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await axios.post(`${API_URL}/auth/logout/`);
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await axios.get(`${API_URL}/auth/user/`);
    return response.data;
  },

  updateUser: async (userData: Partial<User>): Promise<User> => {
    const response = await axios.put(`${API_URL}/auth/user/`, userData);
    return response.data;
  },

  changePassword: async (oldPassword: string, newPassword: string): Promise<void> => {
    await axios.post(`${API_URL}/auth/change-password/`, {
      old_password: oldPassword,
      new_password: newPassword,
    });
  },
};

export default authService; 