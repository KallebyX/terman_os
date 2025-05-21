import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ClientLayoutProps {
  children: React.ReactNode;
}

export const ClientLayout: React.FC<ClientLayoutProps> = ({ children }) => {
  const location = useLocation();
  const { user, signOut } = useAuth();

  const menuItems = [
    { title: 'Meus Pedidos', path: '/client/orders', icon: 'shopping-cart' },
    { title: 'Meu Perfil', path: '/client/profile', icon: 'user' },
    { title: 'Endereços', path: '/client/addresses', icon: 'map-marker-alt' },
    { title: 'Favoritos', path: '/client/favorites', icon: 'heart' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link to="/">
                  <img
                    className="h-8 w-auto"
                    src="/images/logo.png"
                    alt="Logo"
                  />
                </Link>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link
                  to="/marketplace"
                  className="border-transparent text-gray-500 hover:border-primary-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Marketplace
                </Link>
              </div>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:items-center">
              <div className="ml-3 relative">
                <div className="flex items-center space-x-4">
                  <span className="text-gray-700">{user?.name}</span>
                  <button
                    onClick={signOut}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    Sair
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row gap-8">
            <div className="w-full lg:w-64 flex-shrink-0">
              <nav className="space-y-1">
                {menuItems.map((item) => {
                  const isActive = location.pathname === item.path;
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`group flex items-center px-3 py-2 text-sm font-medium rounded-md ${
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
            <div className="flex-1">
              <div className="bg-white shadow rounded-lg">
                {children}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}; 