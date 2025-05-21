import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface MenuItem {
  label: string;
  path: string;
  icon: React.ReactNode;
  roles?: string[];
}

export const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const location = useLocation();

  const menuItems: MenuItem[] = [
    {
      label: 'Dashboard',
      path: '/dashboard',
      icon: <span className="material-icons">dashboard</span>
    },
    {
      label: 'PDV',
      path: '/pdv',
      icon: <span className="material-icons">point_of_sale</span>
    },
    {
      label: 'Produtos',
      path: '/produtos',
      icon: <span className="material-icons">inventory_2</span>
    },
    {
      label: 'Clientes',
      path: '/clientes',
      icon: <span className="material-icons">people</span>
    },
    {
      label: 'Pedidos',
      path: '/pedidos',
      icon: <span className="material-icons">receipt_long</span>
    },
    {
      label: 'Relatórios',
      path: '/relatorios',
      icon: <span className="material-icons">bar_chart</span>,
      roles: ['admin']
    },
    {
      label: 'Configurações',
      path: '/configuracoes',
      icon: <span className="material-icons">settings</span>,
      roles: ['admin']
    }
  ];

  const filteredMenuItems = menuItems.filter(
    item => !item.roles || item.roles.includes(user?.role || '')
  );

  return (
    <aside className="bg-white w-64 min-h-screen border-r border-gray-200">
      <div className="flex flex-col h-full">
        <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
          <nav className="mt-5 flex-1 px-2 space-y-1">
            {filteredMenuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  group flex items-center px-2 py-2 text-sm font-medium rounded-md
                  ${location.pathname === item.path
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}
                `}
              >
                {item.icon}
                <span className="ml-3">{item.label}</span>
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </aside>
  );
}; 