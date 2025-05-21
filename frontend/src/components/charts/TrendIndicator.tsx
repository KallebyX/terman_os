import React from 'react';
import { ArrowUpIcon, ArrowDownIcon, MinusIcon } from '@heroicons/react/solid';

interface TrendIndicatorProps {
  value: number;
  showValue?: boolean;
  className?: string;
}

export const TrendIndicator: React.FC<TrendIndicatorProps> = ({
  value,
  showValue = true,
  className = ''
}) => {
  const getColor = () => {
    if (value > 0) return 'text-green-600';
    if (value < 0) return 'text-red-600';
    return 'text-gray-400';
  };

  const getIcon = () => {
    if (value > 0) return <ArrowUpIcon className="w-4 h-4" />;
    if (value < 0) return <ArrowDownIcon className="w-4 h-4" />;
    return <MinusIcon className="w-4 h-4" />;
  };

  return (
    <div className={`flex items-center ${getColor()} ${className}`}>
      {getIcon()}
      {showValue && (
        <span className="ml-1 text-sm">
          {Math.abs(value).toFixed(1)}%
        </span>
      )}
    </div>
  );
}; 