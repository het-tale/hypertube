// src/features/auth/context/AuthContext.tsx
import { createContext, useContext } from 'react'
import type { ReactNode } from 'react'
import {
  useMe,
  useLogin,
  useRegister,
  useLogout,
} from '../hooks/useAuthQueries'
import type {
  User,
  LoginCredentials,
  RegisterCredentials,
} from '../types/auth.types'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<User>
  register: (credentials: RegisterCredentials) => Promise<User>
  logout: () => Promise<void>
  refetchUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: user, isLoading, refetch } = useMe()
  const loginMutation = useLogin()
  const registerMutation = useRegister()
  const logoutMutation = useLogout()

  const login = async (credentials: LoginCredentials) => {
    return loginMutation.mutateAsync(credentials)
  }

  const register = async (credentials: RegisterCredentials) => {
    return registerMutation.mutateAsync(credentials)
  }

  const logout = async () => {
    await logoutMutation.mutateAsync()
  }

  const refetchUser = async () => {
    await refetch()
  }

  return (
    <AuthContext.Provider
      value={{
        user: user ?? null,
        isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        refetchUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuthContext() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuthContext must be used within AuthProvider')
  }
  return context
}
