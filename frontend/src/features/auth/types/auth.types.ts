export interface User {
  id: string
  email: string
  username: string
  full_name?: string

  profile_picture?: string
  is_active: boolean
  created_at: string
  updated_at: string
  preferred_language?: string
  bio?: string
  // add other user fields
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  username: string
  password: string
  passwordConfirmation: string
}

export interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  register: (credentials: RegisterCredentials) => Promise<void>
  logout: () => Promise<void>
  refetchUser: () => Promise<void>
}
