import React from 'react';
import { twMerge } from 'tailwind-merge';

interface TableProps {
  children: React.ReactNode;
  className?: string;
}

export const Table: React.FC<TableProps> = ({ children, className }) => (
  <div className="overflow-x-auto">
    <table className={twMerge('min-w-full divide-y divide-gray-200', className)}>
      {children}
    </table>
  </div>
);

export const Thead: React.FC<TableProps> = ({ children, className }) => (
  <thead className={twMerge('bg-gray-50', className)}>
    {children}
  </thead>
);

export const Tbody: React.FC<TableProps> = ({ children, className }) => (
  <tbody className={twMerge('divide-y divide-gray-200 bg-white', className)}>
    {children}
  </tbody>
);

export const Th: React.FC<TableProps> = ({ children, className }) => (
  <th
    className={twMerge(
      'px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
      className
    )}
  >
    {children}
  </th>
);

export const Td: React.FC<TableProps> = ({ children, className }) => (
  <td
    className={twMerge(
      'px-6 py-4 whitespace-nowrap text-sm text-gray-500',
      className
    )}
  >
    {children}
  </td>
);
