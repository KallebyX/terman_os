import React from 'react';
import { cn } from '../../utils/cn';

interface SidebarProps {
  children?: React.ReactNode;
  className?: string;
  collapsed?: boolean;
  onToggle?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  children,
  className,
  collapsed = false,
  onToggle,
  ...props
}) => {
  return (
    <aside
      className={cn(
        'h-screen bg-white border-r border-secondary-200 transition-all duration-300',
        collapsed ? 'w-16' : 'w-64',
        className
      )}
      {...props}
    >
      <div className="flex flex-col h-full">
        {/* Logo e botão de toggle */}
        <div className="flex items-center justify-between p-4 border-b border-secondary-200">
          <div className={cn('flex items-center', collapsed && 'justify-center w-full')}>
            {/* Logo */}
            <div className="flex-shrink-0">
              <img 
                src="/logo.png" 
                alt="Mangueiras Terman" 
                className={cn('transition-all', collapsed ? 'w-8 h-8' : 'w-10 h-10')} 
              />
            </div>
            
            {/* Nome da empresa - escondido quando colapsado */}
            {!collapsed && (
              <span className="ml-3 text-lg font-semibold text-secondary-900">Terman OS</span>
            )}
          </div>
          
          {/* Botão de toggle */}
          {onToggle && (
            <button
              onClick={onToggle}
              className={cn(
                'text-secondary-500 hover:text-secondary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-full p-1',
                collapsed && 'hidden'
              )}
              aria-label={collapsed ? 'Expandir menu' : 'Colapsar menu'}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={collapsed ? 'M13 5l7 7-7 7M5 5l7 7-7 7' : 'M11 19l-7-7 7-7m8 14l-7-7 7-7'} />
              </svg>
            </button>
          )}
        </div>
        
        {/* Conteúdo do sidebar */}
        <div className="flex-1 overflow-y-auto py-4">
          {children}
        </div>
      </div>
    </aside>
  );
};

interface SidebarItemProps {
  icon?: React.ReactNode;
  label: string;
  active?: boolean;
  collapsed?: boolean;
  onClick?: () => void;
  href?: string;
}

export const SidebarItem: React.FC<SidebarItemProps> = ({
  icon,
  label,
  active = false,
  collapsed = false,
  onClick,
  href,
  ...props
}) => {
  const content = (
    <div
      className={cn(
        'flex items-center px-4 py-3 cursor-pointer transition-colors rounded-md',
        active 
          ? 'bg-primary-50 text-primary-700' 
          : 'text-secondary-700 hover:bg-secondary-50 hover:text-secondary-900',
        collapsed ? 'justify-center' : ''
      )}
      onClick={onClick}
      {...props}
    >
      {icon && <span className={cn('text-xl', !collapsed && 'mr-3')}>{icon}</span>}
      {!collapsed && <span>{label}</span>}
    </div>
  );
  
  if (href) {
    return (
      <a href={href} className="block no-underline">
        {content}
      </a>
    );
  }
  
  return content;
};

export default Sidebar;
