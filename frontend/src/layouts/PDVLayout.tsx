import React from 'react';
import { cn } from '../utils/cn';
import { Header, HeaderTitle, HeaderActions } from '../components/ui/Header';
import { Sidebar } from '../components/ui/Sidebar';

export const PDVLayout = ({ children, className }) => {
  const [collapsed, setCollapsed] = React.useState(false);
  
  return (
    <div className={cn("flex h-screen overflow-hidden", className)}>
      <Sidebar 
        collapsed={collapsed} 
        onToggle={() => setCollapsed(!collapsed)}
      >
        {/* Itens do menu PDV */}
        <div className="px-4 py-3 text-secondary-700 hover:bg-secondary-50 hover:text-secondary-900 rounded-md transition-colors cursor-pointer">
          {!collapsed && <span>Nova Venda</span>}
          {collapsed && <span className="text-xl">+</span>}
        </div>
        <div className="px-4 py-3 text-secondary-700 hover:bg-secondary-50 hover:text-secondary-900 rounded-md transition-colors cursor-pointer">
          {!collapsed && <span>Histórico</span>}
          {collapsed && <span className="text-xl">H</span>}
        </div>
        <div className="px-4 py-3 text-secondary-700 hover:bg-secondary-50 hover:text-secondary-900 rounded-md transition-colors cursor-pointer">
          {!collapsed && <span>Clientes</span>}
          {collapsed && <span className="text-xl">C</span>}
        </div>
      </Sidebar>
      
      <div className={cn("flex flex-col flex-1 overflow-hidden")}>
        <Header>
          <HeaderTitle>
            <h1 className="text-xl font-semibold text-secondary-900">PDV - Ponto de Venda</h1>
          </HeaderTitle>
          <HeaderActions>
            <button className="text-secondary-500 hover:text-secondary-700">
              <span className="fas fa-bell"></span>
            </button>
            <button className="text-secondary-500 hover:text-secondary-700">
              <span className="fas fa-user-circle"></span>
            </button>
          </HeaderActions>
        </Header>
        
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
