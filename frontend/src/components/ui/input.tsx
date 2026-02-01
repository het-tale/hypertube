// src/components/ui/Input.tsx (Updated)
import { forwardRef, useState } from 'react'
import type { InputHTMLAttributes, ReactNode } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string
  label?: string
  icon?: ReactNode
  variant?: 'default' | 'signup'
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      error,
      label,
      type = 'text',
      icon,
      variant = 'default',
      className = '',
      ...props
    },
    ref,
  ) => {
    const [showPassword, setShowPassword] = useState(false)
    const isPassword = type === 'password'
    const inputType = isPassword && showPassword ? 'text' : type

    const baseStyles =
      variant === 'signup'
        ? 'w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-white/10 bg-white/5 focus:border-primary h-12 text-base placeholder:text-gray-600 transition-all'
        : 'w-full h-14 rounded bg-[#333] border text-white placeholder:text-[#8c8c8c] focus:ring-2 focus:ring-primary/50 focus:border-transparent text-base transition-all'

    const paddingStyles = icon ? 'pl-10 pr-4' : 'p-4'
    const passwordPadding = isPassword ? 'pr-12' : ''

    return (
      <div className="flex flex-col">
        {label && (
          <label
            className={`font-semibold mb-2 ml-1 ${
              variant === 'signup'
                ? 'text-white text-xs uppercase tracking-wider'
                : 'text-sm text-white/90'
            }`}
          >
            {label}
          </label>
        )}
        <div className="relative">
          {icon && (
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-xl">
              {icon}
            </span>
          )}
          <input
            ref={ref}
            type={inputType}
            className={`${baseStyles} ${paddingStyles} ${passwordPadding} ${
              error
                ? 'border-red-500'
                : variant === 'signup'
                  ? 'border-white/10'
                  : 'border-transparent'
            } ${className}`}
            {...props}
          />
          {isPassword && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
              tabIndex={-1}
            >
              <span className="material-symbols-outlined text-xl">
                {showPassword ? 'visibility_off' : 'visibility'}
              </span>
            </button>
          )}
        </div>
        {error && <span className="text-red-500 text-sm mt-1">{error}</span>}
      </div>
    )
  },
)

Input.displayName = 'Input'
