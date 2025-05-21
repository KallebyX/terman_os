import React from 'react';
import { cn } from '../../utils/cn';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  containerClassName?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  helperText,
  error,
  leftIcon,
  rightIcon,
  fullWidth = true,
  containerClassName,
  className,
  id,
  ...props
}) => {
  // Gerar ID aleatório se não for fornecido
  const inputId = id || `input-${Math.random().toString(36).substring(2, 9)}`;
  
  // Estado de erro
  const hasError = !!error;
  
  // Estilos condicionais
  const inputStyles = cn(
    'px-3 py-2 bg-white border rounded-md focus:outline-none focus:ring-2 transition-colors',
    hasError 
      ? 'border-danger text-danger focus:border-danger focus:ring-danger/30' 
      : 'border-secondary-300 focus:border-primary-500 focus:ring-primary-500/30',
    (leftIcon ? 'pl-10' : ''),
    (rightIcon ? 'pr-10' : ''),
    className
  );
  
  // Largura total
  const widthStyles = fullWidth ? 'w-full' : '';

  return (
    <div className={cn('mb-4', widthStyles, containerClassName)}>
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-secondary-700 mb-1">
          {label}
        </label>
      )}
      
      <div className="relative">
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-secondary-500">
            {leftIcon}
          </div>
        )}
        
        <input
          id={inputId}
          className={inputStyles}
          aria-invalid={hasError}
          aria-describedby={hasError ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
          {...props}
        />
        
        {rightIcon && (
          <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-secondary-500">
            {rightIcon}
          </div>
        )}
      </div>
      
      {helperText && !hasError && (
        <p id={`${inputId}-helper`} className="mt-1 text-sm text-secondary-500">
          {helperText}
        </p>
      )}
      
      {hasError && (
        <p id={`${inputId}-error`} className="mt-1 text-sm text-danger">
          {error}
        </p>
      )}
    </div>
  );
};

export default Input;
