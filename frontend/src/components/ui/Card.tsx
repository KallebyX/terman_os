import React from 'react';
import { cn } from '../../utils/cn';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  variant = 'default',
  padding = 'md',
  onClick,
  ...props
}) => {
  // Variantes de estilo
  const variantStyles = {
    default: 'bg-white shadow-sm',
    bordered: 'bg-white border border-secondary-200',
    elevated: 'bg-white shadow-md hover:shadow-lg transition-shadow duration-300',
  };

  // Tamanhos de padding
  const paddingStyles = {
    none: 'p-0',
    sm: 'p-3',
    md: 'p-5',
    lg: 'p-7',
  };

  // Cursor pointer se houver onClick
  const cursorStyle = onClick ? 'cursor-pointer' : '';

  return (
    <div
      className={cn(
        'rounded-lg overflow-hidden',
        variantStyles[variant],
        paddingStyles[padding],
        cursorStyle,
        className
      )}
      onClick={onClick}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
