import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const Navbar: React.FC = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    signOut();
    navigate('/login');
  };

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <img src="/logo.svg" alt="Logo" className="h-8 w-auto" />
            </Link>
          </div>

          <div className="flex items-center">
            <div className="hidden md:ml-4 md:flex md:items-center">
              {user?.role === 'admin' && (
                <Link
                  to="/admin"
                  className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  Painel Admin
                </Link>
              )}
              <Link
                to="/pdv"
                className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                PDV
              </Link>
              <div className="ml-3 relative">
                <button
                  onClick={handleLogout}
                  className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  Sair
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}; 