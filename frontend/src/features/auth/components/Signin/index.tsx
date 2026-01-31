// src/features/auth/components/SignInForm.tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Link, useNavigate } from '@tanstack/react-router'
import { useAuth } from '../../hooks/useAuth'
import { loginSchema, type LoginFormData } from '../../schemas/auth.schemas'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

const SignIn = () => {
  const { login } = useAuth()
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      rememberMe: false,
    },
  })

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login({
        email: data.emailOrPhone, // Adjust based on your API
        password: data.password,
      })
      navigate({ to: '/' })
    } catch (err: any) {
      const message = err.response?.data?.message || 'Invalid credentials'
      setError('root', { message })
    }
  }

  const handleOAuthLogin = (provider: 'google' | '42') => {
    // Redirect to OAuth endpoint
    window.location.href = `${import.meta.env.VITE_API_URL}/auth/${provider}`
  }

  return (
    <div className="glass-card w-full max-w-112.5 p-10 md:p-16 rounded-lg shadow-2xl">
      <h2 className="text-3xl font-bold mb-8">Sign In</h2>

      {errors.root && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500 rounded text-red-500 text-sm">
          {errors.root.message}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          {...register('emailOrPhone')}
          placeholder="Email or phone number"
          error={errors.emailOrPhone?.message}
          autoComplete="username"
        />

        <Input
          {...register('password')}
          type="password"
          placeholder="Password"
          error={errors.password?.message}
          autoComplete="current-password"
        />

        <Button type="submit" isLoading={isSubmitting} className="mt-4">
          Sign In
        </Button>

        <div className="flex items-center justify-between text-sm text-[#b3b3b3] mt-2">
          <div className="flex items-center gap-2">
            <input
              {...register('rememberMe')}
              className="rounded bg-[#737373] border-none focus:ring-0 checked:bg-primary cursor-pointer"
              id="remember"
              type="checkbox"
            />
            <label htmlFor="remember" className="cursor-pointer">
              Remember me
            </label>
          </div>
          <Link to="/" className="hover:underline transition-colors">
            Need help?
          </Link>
        </div>
      </form>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-[#444]"></span>
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-transparent px-2 text-[#b3b3b3] font-medium tracking-wider">
            OR CONTINUE WITH
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3">
        <Button
          type="button"
          variant="secondary"
          onClick={() => handleOAuthLogin('google')}
          className="flex items-center justify-center gap-3"
        >
          <svg className="size-5" viewBox="0 0 24 24">
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
          Google
        </Button>

        <Button
          type="button"
          variant="oauth"
          onClick={() => handleOAuthLogin('42')}
          className="flex items-center justify-center gap-3"
        >
          <span className="font-black text-xl">42</span>
          School 42
        </Button>
      </div>

      <div className="mt-8 text-[#737373]">
        New to Hypertube?{' '}
        <Link to="/Signup" className="text-white hover:underline">
          Sign up now
        </Link>
        .
      </div>

      <div className="mt-4 text-xs text-[#8c8c8c]">
        This page is protected by Google reCAPTCHA to ensure you're not a bot.{' '}
        <a
          className="text-blue-500 hover:underline"
          href="https://policies.google.com/privacy"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn more.
        </a>
      </div>
    </div>
  )
}
export default SignIn
