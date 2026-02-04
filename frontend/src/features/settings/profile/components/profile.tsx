import ProfileForm from './profileForm'

const ProfileSettings = () => {
  return (
    <div className="max-w-200 mx-auto px-4 md:px-8 py-10">
      <div className="mb-10">
        <h1 className="text-white text-4xl font-black leading-tight tracking-tight mb-2">
          Profile Settings
        </h1>
        <p className="text-text-muted text-lg">
          Manage your personal information and how others see you.
        </p>
      </div>
      <ProfileForm />
    </div>
  )
}

export default ProfileSettings
