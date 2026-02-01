// src/routes/login.tsx (or wherever your route is)
import { createFileRoute, Navigate } from '@tanstack/react-router'

import { useAuth } from '@/features/auth/hooks/useAuth'
import SignIn from '@/features/auth/components/Signin'

export const Route = createFileRoute('/SignIn')({
  component: SignInPage,
})

function SignInPage() {
  const { isAuthenticated } = useAuth()

  if (isAuthenticated) {
    console.log(
      'User is authenticated, redirecting to home page.',
      isAuthenticated,
    )
    return <Navigate to="/home" />
  }

  return (
    <div
      className="relative min-h-screen w-full flex flex-col movie-bg bg-cover bg-center bg-no-repeat"
      data-alt="Cinematic movie poster collage background dark"
    >
      <header className="flex items-center justify-between px-10 py-6 w-full z-10">
        <div className="flex items-center gap-2 text-primary">
          <div className="size-8">
            <svg
              fill="currentColor"
              viewBox="0 0 48 48"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M4 42.4379C4 42.4379 14.0962 36.0744 24 41.1692C35.0664 46.8624 44 42.2078 44 42.2078L44 7.01134C44 7.01134 35.068 11.6577 24.0031 5.96913C14.0971 0.876274 4 7.27094 4 7.27094L4 42.4379Z"></path>
            </svg>
          </div>
          <h1 className="text-3xl font-black leading-tight tracking-[-0.015em]">
            Hypertube
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <select className="bg-black/50 border border-white/30 rounded px-3 py-1 text-sm focus:ring-primary">
            <option>English</option>
            <option>French</option>
            <option>Spanish</option>
          </select>
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center px-4 pb-20">
        <SignIn />
      </main>

      <footer className="bg-black/80 py-8 px-10 border-t border-white/10">
        <div className="max-w-250 mx-auto">
          <p className="text-[#737373] mb-6">
            Questions? Call 1-800-HYPER-TUBE
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-[#737373]">
            <a className="hover:underline" href="#">
              FAQ
            </a>
            <a className="hover:underline" href="#">
              Help Center
            </a>
            <a className="hover:underline" href="#">
              Terms of Use
            </a>
            <a className="hover:underline" href="#">
              Privacy
            </a>
            <a className="hover:underline" href="#">
              Cookie Preferences
            </a>
            <a className="hover:underline" href="#">
              Corporate Information
            </a>
          </div>
          <div className="mt-8">
            <select className="bg-black border border-[#333] rounded px-4 py-2 text-sm text-[#737373]">
              <option>English</option>
              <option>Français</option>
            </select>
          </div>
        </div>
      </footer>
    </div>
  )
}
