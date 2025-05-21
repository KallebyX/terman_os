import React from 'react';
import { twMerge } from 'tailwind-merge';

interface AlertProps {
  type: 'success' | 'error' | 'info' | 'warning';
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  type,
  title,
  children,
  className
}) => {
  const styles = {
    success: 'bg-green-50 text-green-800 border-green-200',
    error: 'bg-red-50 text-red-800 border-red-200',
    info: 'bg-blue-50 text-blue-800 border-blue-200',
    warning: 'bg-yellow-50 text-yellow-800 border-yellow-200'
  };

  return (
    <div
      className={twMerge(
        'rounded-lg border p-4',
        styles[type],
        className
      )}
    >
      {title && (
        <h3 className="mb-2 font-medium">{title}</h3>
      )}
      <div className="text-sm">{children}</div>
    </div>
  );
}; 