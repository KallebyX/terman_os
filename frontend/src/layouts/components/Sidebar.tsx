import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const menuItems = [
  {
    title: 'Dashboard',
    path: '/dashboard',
    icon: 'chart-line',
    roles: ['admin', 'manager', 'employee']
  },
  {
    title: 'PDV',
    path: '/pdv',
    icon: 'cash-register',
    roles: ['admin', 'manager', 'employee']
  },
  {
    title: 'Inventário',
    path: '/inventory',
    icon: 'box',
    roles: ['admin', 'manager']
  },
  {
    title: 'Clientes',
    path: '/customers',
    icon: 'users',
    roles: ['admin', 'manager', 'employee']
  },
  {
    title: 'Pedidos',
    path: '/orders',
    icon: 'shopping-cart',
    roles: ['admin', 'manager', 'employee']
  },
  {
    title: 'Relatórios',
    path: '/reports',
    icon: 'chart-bar',
    roles: ['admin', 'manager']
  },
  {
    title: 'Configurações',
    path: '/settings',
    icon: 'cog',
    roles: ['admin']
  }
];

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const { user } = useAuth();

  const filteredMenuItems = menuItems.filter(
    item => item.roles.includes(user?.role || '')
  );

  return (
    <div className="hidden lg:flex lg:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col flex-grow bg-white pt-5 pb-4 overflow-y-auto">
          <div className="flex-grow flex flex-col">
            <nav className="flex-1 px-2 space-y-1">
              {filteredMenuItems.map((item) => {
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-primary-100 text-primary-900'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <i
                      className={`fas fa-${item.icon} mr-3 flex-shrink-0 h-6 w-6 ${
                        isActive
                          ? 'text-primary-500'
                          : 'text-gray-400 group-hover:text-gray-500'
                      }`}
                    />
                    {item.title}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
}; 