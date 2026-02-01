import { api } from '@/lib/axios'
import type {
  User,
  LoginCredentials,
  RegisterCredentials,
} from '../types/auth.types'

export const authApi = {
  // Get current user (verify session)
  me: async (): Promise<User> => {
    const { data } = await api.get<User>('/users/me')
    return data
  },

  // Login
  login: async (credentials: LoginCredentials): Promise<User> => {
    const { data } = await api.post<User>('/auth/login', credentials)
    return data
  },

  // Register
  register: async (credentials: RegisterCredentials): Promise<User> => {
    const { data } = await api.post<User>('/auth/register', credentials)
    return data
  },

  // Logout
  logout: async (): Promise<void> => {
    await api.post('/auth/logout')
  },
}
