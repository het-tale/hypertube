// src/features/auth/components/SignUpForm.tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Link, useNavigate } from '@tanstack/react-router'
import { useAuth } from '../../hooks/useAuth'
import {
  registerSchema,
  type RegisterFormData,
} from '../../schemas/auth.schemas'
import { Input } from '@/components/ui/input'

const Signup = () => {
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      agreeToTerms: false,
    },
  })

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await registerUser({
        username: data.username,
        email: data.email,
        password: data.password,
        passwordConfirmation: data.passwordConfirmation,
      })
      navigate({ to: '/home' })
    } catch (err: any) {
      const message = err.response?.data?.message || 'Registration failed'
      setError('root', { message })
    }
  }

  const handleOAuthRegister = (provider: 'google' | 'github' | '42' | 'discord') => {
    window.location.href = `${import.meta.env.VITE_API_URL}auth/login/${provider}`
  }

  return (
    <div className="w-full max-w-125 bg-black/60 backdrop-blur-md border border-white/10 p-8 lg:p-12 rounded-xl shadow-2xl">
      <div className="text-center mb-8">
        <h1 className="text-white text-3xl font-bold mb-2">Create Account</h1>
        <p className="text-gray-400 text-sm">
          Join Hypertube for unlimited movies and shows.
        </p>
      </div>

      {errors.root && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500 rounded text-red-500 text-sm">
          {errors.root.message}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Input
            {...register('firstName')}
            label="First Name"
            placeholder="John"
            variant="signup"
            error={errors.firstName?.message}
            autoComplete="given-name"
          />
          <Input
            {...register('lastName')}
            label="Last Name"
            placeholder="Doe"
            variant="signup"
            error={errors.lastName?.message}
            autoComplete="family-name"
          />
        </div>

        <Input
          {...register('username')}
          label="Username"
          placeholder="johndoe123"
          variant="signup"
          icon={<span className="material-symbols-outlined">person</span>}
          error={errors.username?.message}
          autoComplete="username"
        />

        <Input
          {...register('email')}
          type="email"
          label="Email Address"
          placeholder="john@example.com"
          variant="signup"
          icon={<span className="material-symbols-outlined">mail</span>}
          error={errors.email?.message}
          autoComplete="email"
        />

        <Input
          {...register('password')}
          type="password"
          label="Password"
          placeholder="••••••••"
          variant="signup"
          icon={<span className="material-symbols-outlined">lock</span>}
          error={errors.password?.message}
          autoComplete="new-password"
        />

        <Input
          {...register('passwordConfirmation')}
          type="password"
          label="Confirm Password"
          placeholder="••••••••"
          variant="signup"
          icon={<span className="material-symbols-outlined">lock</span>}
          error={errors.passwordConfirmation?.message}
          autoComplete="new-password"
        />

        <div className="flex items-start gap-3 py-2">
          <input
            {...register('agreeToTerms')}
            className="mt-1 rounded border-white/20 bg-white/5 text-primary focus:ring-primary focus:ring-offset-0 cursor-pointer"
            type="checkbox"
            id="agreeToTerms"
          />
          <label
            htmlFor="agreeToTerms"
            className="text-xs text-gray-400 leading-normal cursor-pointer"
          >
            <a
              className="text-primary hover:underline"
              href="/terms"
              target="_blank"
              rel="noopener noreferrer"
            >
              Terms of Service
            </a>{' '}
            and{' '}
            <a
              className="text-primary hover:underline"
              href="/privacy"
              target="_blank"
              rel="noopener noreferrer"
            >
              Privacy Policy
            </a>
            .
          </label>
        </div>
        {errors.agreeToTerms && (
          <span className="text-red-500 text-sm -mt-2 block">
            {errors.agreeToTerms.message}
          </span>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full h-14 bg-primary hover:bg-red-600 text-white font-bold rounded-lg shadow-lg shadow-primary/20 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed mt-4"
        >
          {isSubmitting ? (
            <span className="flex items-center justify-center gap-2">
              <svg
                className="animate-spin h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Creating Account...
            </span>
          ) : (
            'Create Account'
          )}
        </button>

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-white/10"></span>
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-black/60 px-3 text-gray-400 font-medium tracking-wider">
              Or register with
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => handleOAuthRegister('google')}
            className="flex items-center justify-center gap-2 h-12 rounded-lg bg-white hover:bg-gray-100 text-gray-800 font-medium transition-all duration-200 active:scale-95 shadow-lg shadow-black/10 hover:shadow-black/20"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            <span>Google</span>
          </button>
          <button
            type="button"
            onClick={() => handleOAuthRegister('github')}
            className="flex items-center justify-center gap-2 h-12 rounded-lg bg-linear-to-r from-gray-700 to-gray-600 hover:from-gray-800 hover:to-gray-700 text-white font-medium transition-all duration-200 active:scale-95 shadow-lg shadow-gray-700/20 hover:shadow-gray-700/40"
          >
            <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
              <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.43.372.823 1.102.823 2.222 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"></path>
            </svg>
            <span>GitHub</span>
          </button>
          <button
            type="button"
            onClick={() => handleOAuthRegister('42')}
            className="flex items-center justify-center gap-2 h-12 rounded-lg bg-black hover:bg-gray-900 border border-gray-700 text-white font-bold transition-all duration-200 active:scale-95 shadow-lg shadow-black/40 hover:shadow-black/60"
          >
            <span>42</span>
          </button>
          <button
            type="button"
            onClick={() => handleOAuthRegister('discord')}
            className="flex items-center justify-center gap-2 h-12 rounded-lg bg-[#5865F2] hover:bg-[#4752C4] text-white font-medium transition-all duration-200 active:scale-95 shadow-lg shadow-[#5865F2]/30 hover:shadow-[#5865F2]/50"
          >
            <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
              <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515a.074.074 0 0 0-.079.037c-.211.375-.444.864-.607 1.25a18.27 18.27 0 0 0-5.487 0c-.163-.386-.395-.875-.607-1.25a.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057a19.9 19.9 0 0 0 5.993 3.03a.078.078 0 0 0 .084-.028a14.975 14.975 0 0 0 1.293-2.1a.07.07 0 0 0-.038-.098a13.11 13.11 0 0 1-1.872-.892a.072.072 0 0 1-.009-.119c.125-.093.25-.19.37-.287a.075.075 0 0 1 .078-.01c3.928 1.793 8.18 1.793 12.062 0a.075.075 0 0 1 .079.009c.12.098.245.195.369.287a.072.072 0 0 1-.01.119a12.901 12.901 0 0 1-1.873.892a.075.075 0 0 0-.037.098a14.993 14.993 0 0 0 1.293 2.1a.078.078 0 0 0 .084.028a19.881 19.881 0 0 0 6.002-3.03a.079.079 0 0 0 .033-.057c.5-4.761-.838-8.878-3.557-12.643a.066.066 0 0 0-.031-.03zM8.02 15.278c-1.148 0-2.093-.952-2.093-2.122c0-1.171.929-2.122 2.093-2.122c1.165 0 2.093.951 2.093 2.122c0 1.17-.928 2.122-2.093 2.122zm7.975 0c-1.148 0-2.093-.952-2.093-2.122c0-1.171.929-2.122 2.093-2.122c1.165 0 2.093.951 2.093 2.122c0 1.17-.928 2.122-2.093 2.122z"></path>
            </svg>
            <span>Discord</span>
          </button>
        </div>
      </form>

      <div className="mt-8 text-center">
        <p className="text-gray-400 text-sm">
          Already have an account?{' '}
          <Link
            to="/SignIn"
            className="text-white font-semibold hover:text-primary transition-colors ml-1"
          >
            Sign In
          </Link>
        </p>
      </div>
    </div>
  )
}
export default Signup
