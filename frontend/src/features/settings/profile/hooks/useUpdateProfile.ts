// features/profile/hooks/useUpdateProfile.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/axios'
import { toast } from 'sonner' // or your toast library

interface UpdateProfilePayload {
  firstName?: string
  lastName?: string
  username?: string
  email?: string
  bio?: string
  preferred_language?: string
  profilePicture?: File
}

export const useUpdateProfile = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: UpdateProfilePayload) => {
      const formData = new FormData()

      // Append text fields
      if (data.firstName || data.lastName) {
        const fullName = `${data.firstName || ''} ${data.lastName || ''}`.trim()
        formData.append('full_name', fullName)
      }
      if (data.username) formData.append('username', data.username)
      if (data.email) formData.append('email', data.email)
      if (data.bio) formData.append('bio', data.bio)
      if (data.preferred_language)
        formData.append('preferred_language', data.preferred_language)

      // Append profile picture if provided
      if (data.profilePicture) {
        formData.append('profile_picture', data.profilePicture)
      }
      console.log('FormData entries:')
      for (const pair of formData.entries()) {
        console.log(`${pair[0]}: ${pair[1]}`)
      }
      const response = await api.put('/users/me', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      return response.data
    },
    onSuccess: () => {
      // Invalidate user query to refetch updated data
      queryClient.invalidateQueries({ queryKey: ['me'] })
      toast.success('Profile updated successfully')
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || 'Failed to update profile'
      toast.error(message)
    },
  })
}
