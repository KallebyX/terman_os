import React from 'react';
import { cn } from '../../utils/cn';

interface HeaderProps {
  children?: React.ReactNode;
  className?: string;
  fixed?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  children,
  className,
  fixed = false,
  ...props
}) => {
  return (
    <header
      className={cn(
        'bg-white border-b border-secondary-200 py-3 px-6',
        fixed ? 'fixed top-0 left-0 right-0 z-10' : '',
        className
      )}
      {...props}
    >
      <div className="flex items-center justify-between">
        {children}
      </div>
    </header>
  );
};

interface HeaderTitleProps {
  children: React.ReactNode;
  className?: string;
}

export const HeaderTitle: React.FC<HeaderTitleProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <div className={cn('flex items-center', className)} {...props}>
      {children}
    </div>
  );
};

interface HeaderActionsProps {
  children: React.ReactNode;
  className?: string;
}

export const HeaderActions: React.FC<HeaderActionsProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <div className={cn('flex items-center space-x-3', className)} {...props}>
      {children}
    </div>
  );
};
