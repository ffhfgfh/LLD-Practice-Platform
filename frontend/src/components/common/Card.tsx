import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  hoverEffect?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  onClick,
  hoverEffect = false,
}) => {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm p-5 shadow-sm ${
        hoverEffect
          ? 'transition-all duration-200 hover:border-slate-700 hover:bg-slate-900 hover:shadow-md'
          : ''
      } ${onClick ? 'cursor-pointer' : ''} ${className}`}
    >
      {children}
    </div>
  );
};
