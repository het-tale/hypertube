// features/profile/components/ProfileForm.tsx
import { useMe } from '@/features/auth/hooks/useAuthQueries'
import { useForm } from 'react-hook-form'
import { profileSchema, type ProfileFormData } from '../schemas/profile.schema'
import { zodResolver } from '@hookform/resolvers/zod'
import { useUpdateProfile } from '../hooks/useUpdateProfile'
import { useState, useRef } from 'react'

const ProfileForm = () => {
  const { data: user, refetch } = useMe()
  const updateProfileMutation = useUpdateProfile()
  const fileInputRef = useRef<HTMLInputElement>(null)

  // State for image preview
  const [previewImage, setPreviewImage] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isDirty },
    setError,
    reset,
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      firstName: user?.full_name?.split(' ')[0] || '',
      lastName: user?.full_name?.split(' ')[1] || '',
      username: user?.username || '',
      email: user?.email || '',
      bio: user?.bio || '',
      preferred_language: user?.preferred_language || '',
    },
  })

  // Handle file selection
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Validate file size
    if (file.size > 800_000) {
      setError('profilePicture', {
        message: 'File size must be less than 800KB',
      })
      return
    }

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
    if (!validTypes.includes(file.type)) {
      setError('profilePicture', {
        message: 'Only JPG, PNG, and GIF files are accepted',
      })
      return
    }

    // Create preview
    const reader = new FileReader()
    reader.onloadend = () => {
      setPreviewImage(reader.result as string)
    }
    reader.readAsDataURL(file)

    setSelectedFile(file)
  }

  // Handle remove photo
  const handleRemovePhoto = () => {
    setPreviewImage(null)
    setSelectedFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  // Handle form submission
  const onSubmit = async (data: ProfileFormData) => {
    try {
      console.log('Submitting data:', data)
      await updateProfileMutation.mutateAsync({
        firstName: data.firstName,
        lastName: data.lastName,
        username: data.username,
        email: data.email,
        bio: data.bio,
        preferred_language: data.preferred_language,
        profilePicture: selectedFile || undefined,
      })

      // Reset preview state after successful update
      setPreviewImage(null)
      setSelectedFile(null)
      refetch() // Refetch user data to get updated profile picture URL
    } catch (error: any) {
      // Handle specific validation errors
      if (error.response?.status === 409) {
        const detail = error.response.data.detail
        if (detail.includes('email')) {
          setError('email', { message: 'Email is already in use' })
        } else if (detail.includes('username')) {
          setError('username', { message: 'Username is already taken' })
        }
      }
    }
  }

  // Handle cancel
  const handleCancel = () => {
    reset()
    handleRemovePhoto()
  }

  // Current display image (preview or existing)
  const displayImage = previewImage || user?.profile_picture

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-12">
      {/* Profile Picture Section */}
      <section className="bg-card-dark p-6 rounded-xl border border-gray-200 dark:border-border-dark">
        <div className="flex flex-col sm:flex-row items-center gap-8">
          <div className="relative group">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-32 ring-4 ring-primary/20 group-hover:ring-primary transition-all cursor-pointer"
              style={{
                backgroundImage: displayImage
                  ? `url("${displayImage}")`
                  : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              }}
              onClick={() => fileInputRef.current?.click()}
            >
              {!displayImage && (
                <div className="absolute inset-0 flex items-center justify-center text-white text-4xl font-bold">
                  {user?.full_name?.charAt(0) || 'U'}
                </div>
              )}
              <div className="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="material-symbols-outlined text-white text-3xl">
                  photo_camera
                </span>
              </div>
            </div>

            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/jpg,image/png,image/gif"
              className="hidden"
              onChange={handleFileSelect}
            />
          </div>

          <div className="flex-1 text-center sm:text-left">
            <h3 className="text-white text-xl font-bold mb-1">
              Profile Picture
            </h3>
            <p className="text-text-muted text-sm mb-4">
              JPG, GIF or PNG. Max size of 800K.
            </p>

            {/* Show warning if image is selected but not saved */}
            {selectedFile && (
              <p className="text-yellow-500 text-sm mb-3 flex items-center gap-1">
                <span className="material-symbols-outlined text-sm">
                  warning
                </span>
                Click "Save Changes" to update your profile picture
              </p>
            )}

            {errors.profilePicture && (
              <p className="text-red-500 text-sm mb-3">
                {errors.profilePicture.message}
              </p>
            )}

            <div className="flex flex-wrap gap-3 justify-center sm:justify-start">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="px-5 py-2 bg-primary hover:bg-primary/90 text-white text-sm font-bold rounded-lg transition-all flex items-center gap-2"
              >
                <span className="material-symbols-outlined text-sm">
                  upload
                </span>
                Change Photo
              </button>
              <button
                type="button"
                onClick={handleRemovePhoto}
                disabled={!previewImage}
                className="px-5 py-2 bg-gray-200 dark:bg-border-dark hover:bg-gray-300 dark:hover:bg-gray-700 text-gray-900 dark:text-white text-sm font-bold rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Remove
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Form Fields Section */}
      <section className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* First Name */}
          <div className="flex flex-col gap-2">
            <label className="text-white text-sm font-semibold">
              First Name
            </label>
            <input
              {...register('firstName')}
              className="form-input w-full rounded-lg text-white bg-card-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
              placeholder="Enter first name"
              type="text"
            />
            {errors.firstName && (
              <p className="text-red-500 text-sm">{errors.firstName.message}</p>
            )}
          </div>

          {/* Last Name */}
          <div className="flex flex-col gap-2">
            <label className="text-white text-sm font-semibold">
              Last Name
            </label>
            <input
              {...register('lastName')}
              className="form-input w-full rounded-lg text-white bg-card-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
              placeholder="Enter last name"
              type="text"
            />
            {errors.lastName && (
              <p className="text-red-500 text-sm">{errors.lastName.message}</p>
            )}
          </div>
        </div>

        {/* Username */}
        <div className="flex flex-col gap-2">
          <label className="text-white text-sm font-semibold">Username</label>
          <div className="relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted">
              @
            </span>
            <input
              {...register('username')}
              className="form-input w-full rounded-lg text-white bg-card-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 pl-8 pr-4 transition-all"
              placeholder="username"
              type="text"
            />
          </div>
          {errors.username && (
            <p className="text-red-500 text-sm">{errors.username.message}</p>
          )}
        </div>

        {/* Email */}
        <div className="flex flex-col gap-2">
          <label className="text-white text-sm font-semibold">
            Email Address
          </label>
          <div className="flex gap-3">
            <input
              {...register('email')}
              className="form-input flex-1 rounded-lg text-white bg-card-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
              placeholder="email@address.com"
              type="email"
            />
            {user?.is_active && (
              <div className="flex items-center px-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-500 text-xs font-bold uppercase tracking-wider">
                Verified
              </div>
            )}
          </div>
          {errors.email && (
            <p className="text-red-500 text-sm">{errors.email.message}</p>
          )}
        </div>

        {/* Bio */}
        <div className="flex flex-col gap-2 pt-4">
          <label className="text-white text-sm font-semibold">Bio</label>
          <textarea
            {...register('bio')}
            className="form-textarea w-full rounded-lg text-white bg-card-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary p-4 transition-all resize-none"
            placeholder="Tell us about yourself..."
            rows={4}
          />
          {errors.bio && (
            <p className="text-red-500 text-sm">{errors.bio.message}</p>
          )}
        </div>
      </section>

      {/* Action Buttons */}
      <div className="flex items-center justify-between border-t border-gray-200 dark:border-border-dark pt-8 pb-10">
        <button
          type="button"
          onClick={handleCancel}
          disabled={isSubmitting}
          className="px-8 py-3 bg-transparent hover:bg-card-dark text-text-muted hover:text-white text-base font-bold rounded-lg transition-all disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting || (!isDirty && !selectedFile)}
          className="px-10 py-3 bg-primary hover:bg-primary/90 text-white text-base font-extrabold rounded-lg shadow-xl shadow-primary/20 transition-all hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0"
        >
          {isSubmitting ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </form>
  )
}

export default ProfileForm
