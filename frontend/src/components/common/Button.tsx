import React from 'react';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost' | 'success';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  disabled,
  className = '',
  ...props
}) => {
  const sizeClasses = {
    sm: 'px-2.5 py-1.5 text-xs font-medium',
    md: 'px-4 py-2 text-sm font-semibold',
    lg: 'px-5 py-2.5 text-base font-semibold',
  };

  const variantClasses = {
    primary: 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-sm hover:shadow-indigo-500/25 disabled:bg-indigo-900/50 disabled:text-indigo-400',
    secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-100 border border-slate-700 disabled:opacity-50',
    outline: 'bg-transparent hover:bg-slate-800/60 text-slate-300 border border-slate-700 hover:border-slate-600 disabled:opacity-50',
    danger: 'bg-rose-600 hover:bg-rose-500 text-white shadow-sm hover:shadow-rose-500/25 disabled:opacity-50',
    ghost: 'bg-transparent hover:bg-slate-800 text-slate-400 hover:text-slate-200 disabled:opacity-50',
    success: 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm hover:shadow-emerald-500/25 disabled:opacity-50',
  };

  return (
    <button
      disabled={disabled || isLoading}
      className={`inline-flex items-center justify-center gap-2 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:ring-offset-2 focus:ring-offset-slate-950 cursor-pointer disabled:cursor-not-allowed ${sizeClasses[size]} ${variantClasses[variant]} ${className}`}
      {...props}
    >
      {isLoading ? (
        <Loader2 className="h-4 w-4 animate-spin text-current" />
      ) : (
        leftIcon
      )}
      {children}
      {!isLoading && rightIcon}
    </button>
  );
};
