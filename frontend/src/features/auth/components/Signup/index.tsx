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

  const handleOAuthRegister = (provider: 'google' | 'github' | '42') => {
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

        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-white/10"></span>
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-black/0 px-2 text-gray-500 backdrop-blur-sm">
              Or register with
            </span>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3">
          <button
            type="button"
            onClick={() => handleOAuthRegister('google')}
            className="flex items-center justify-center h-12 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
          >
            <img
              className="w-5 h-5 opacity-80"
              alt="Google logo"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCijiQ26NRecx0JP5qt6direIlQaUah2xowjGCVHQWVcTPIjZWo3whl--bw5rLOB4Ice2UiP5mNANrXoC2VFTiAbp9irYvrWkHIugF3IcIokRsVChjT3pUncjVGn3n-i9LqYK6Vwck69vLYp7nVyH4fpBA9yeoWkRG2hgPIIrwJYjufgyaFDcEnFwhSpOKm4psKYrFg5ih_dFuxZ-aGxV7XeI7xeixezk-Ocoffahu837uInL47w_dYLZHzj7v8chvZ6xQHHl7b49o"
            />
          </button>
          <button
            type="button"
            onClick={() => handleOAuthRegister('github')}
            className="flex items-center justify-center h-12 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
          >
            <svg className="w-6 h-6 fill-white opacity-80" viewBox="0 0 24 24">
              <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.43.372.823 1.102.823 2.222 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"></path>
            </svg>
          </button>
          <button
            type="button"
            onClick={() => handleOAuthRegister('42')}
            className="flex items-center justify-center h-12 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all font-bold text-white text-xs"
          >
            42
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
