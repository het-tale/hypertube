import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
  withCredentials: true, // Important for cookies!
  headers: {
    'Content-Type': 'application/json',
  },
})

// Optional: Add response interceptor for handling auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If 401 and haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Call your refresh endpoint
        await api.post('/auth/refresh')

        // Retry original request
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed → redirect to login
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  },
)
