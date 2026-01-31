// src/routes/register.tsx
import { createFileRoute, Navigate } from '@tanstack/react-router'
import Signup from '@/features/auth/components/Signup'
import { useAuth } from '@/features/auth/hooks/useAuth'
import { Link } from '@tanstack/react-router'

export const Route = createFileRoute('/Signup')({
  component: SignUpPage,
})

function SignUpPage() {
  const { isAuthenticated } = useAuth()

  if (isAuthenticated) {
    return <Navigate to="/home" />
  }

  return (
    <>
      <header className="w-full px-6 lg:px-20 py-6 flex items-center justify-between absolute top-0 z-10">
        <Link
          to="/"
          className="flex items-center gap-2 text-white hover:opacity-80 transition-opacity"
        >
          <div className="size-8 text-primary">
            <svg
              fill="currentColor"
              viewBox="0 0 48 48"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M4 42.4379C4 42.4379 14.0962 36.0744 24 41.1692C35.0664 46.8624 44 42.2078 44 42.2078L44 7.01134C44 7.01134 35.068 11.6577 24.0031 5.96913C14.0971 0.876274 4 7.27094 4 7.27094L4 42.4379Z"></path>
            </svg>
          </div>
          <h2 className="text-white text-2xl font-bold leading-tight tracking-tight">
            Hypertube
          </h2>
        </Link>
        <Link
          to="/SignIn"
          className="text-white text-sm font-semibold hover:underline"
        >
          Sign In
        </Link>
      </header>

      <main
        className="flex-1 flex items-center justify-center cinematic-bg px-4 py-20 min-h-screen"
        data-alt="Dark cinematic background with blurred movie posters"
      >
        <Signup />
      </main>
    </>
  )
}
