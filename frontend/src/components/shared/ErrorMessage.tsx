import React from 'react';
import { Button } from '../ui';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => (
  <div className="flex flex-col items-center justify-center h-full">
    <p className="text-red-500 mb-4">{message}</p>
    {onRetry && (
      <Button onClick={onRetry}>Tentar novamente</Button>
    )}
  </div>
); 