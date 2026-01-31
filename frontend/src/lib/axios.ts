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
  (error) => {
    // You can still log errors or handle specific cases
    if (error.response?.status === 401) {
      console.log('Unauthorized request')
    }
    return Promise.reject(error)
  },
)
