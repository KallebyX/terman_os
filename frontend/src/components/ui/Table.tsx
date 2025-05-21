import React from 'react';
import { cn } from '../../utils/cn';

interface TableProps {
  children: React.ReactNode;
  className?: string;
  striped?: boolean;
  hoverable?: boolean;
  bordered?: boolean;
  compact?: boolean;
}

export const Table: React.FC<TableProps> = ({
  children,
  className,
  striped = true,
  hoverable = true,
  bordered = false,
  compact = false,
  ...props
}) => {
  return (
    <div className="w-full overflow-x-auto">
      <table 
        className={cn(
          'w-full text-left',
          bordered && 'border border-secondary-200',
          className
        )}
        {...props}
      >
        {children}
      </table>
    </div>
  );
};

interface TableHeadProps {
  children: React.ReactNode;
  className?: string;
}

export const TableHead: React.FC<TableHeadProps> = ({ children, className, ...props }) => {
  return (
    <thead className={cn('bg-secondary-50', className)} {...props}>
      {children}
    </thead>
  );
};

interface TableBodyProps {
  children: React.ReactNode;
  className?: string;
}

export const TableBody: React.FC<TableBodyProps> = ({ children, className, ...props }) => {
  return (
    <tbody className={className} {...props}>
      {children}
    </tbody>
  );
};

interface TableRowProps {
  children: React.ReactNode;
  className?: string;
  isHeader?: boolean;
  striped?: boolean;
  hoverable?: boolean;
  compact?: boolean;
}

export const TableRow: React.FC<TableRowProps> = ({ 
  children, 
  className, 
  isHeader = false,
  striped = true,
  hoverable = true,
  compact = false,
  ...props 
}) => {
  return (
    <tr 
      className={cn(
        !isHeader && striped && 'even:bg-secondary-50',
        !isHeader && hoverable && 'hover:bg-primary-50',
        className
      )} 
      {...props}
    >
      {children}
    </tr>
  );
};

interface TableCellProps {
  children: React.ReactNode;
  className?: string;
  isHeader?: boolean;
  bordered?: boolean;
  compact?: boolean;
}

export const TableCell: React.FC<TableCellProps> = ({ 
  children, 
  className, 
  isHeader = false,
  bordered = false,
  compact = false,
  ...props 
}) => {
  const Component = isHeader ? 'th' : 'td';
  
  return (
    <Component 
      className={cn(
        isHeader ? 'font-semibold text-secondary-900' : 'text-secondary-700',
        bordered && 'border border-secondary-200',
        compact ? 'px-3 py-2' : 'px-4 py-3',
        className
      )} 
      {...props}
    >
      {children}
    </Component>
  );
};

export default Table;
