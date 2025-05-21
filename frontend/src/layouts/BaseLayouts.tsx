import React from 'react';
import { cn } from '../utils/cn';
import { Header } from '../components/ui/Header';
import { Sidebar } from '../components/ui/Sidebar';

export const DashboardLayout = ({ children, className }) => {
  return (
    <div className={cn("min-h-screen bg-background-lightGray", className)}>
      {children}
    </div>
  );
};

export const AuthLayout = ({ children, className }) => {
  return (
    <div className={cn("min-h-screen bg-background-lightGray flex items-center justify-center p-4", className)}>
      <div className="w-full max-w-md">
        {children}
      </div>
    </div>
  );
};

export const AdminLayout = ({ children, className }) => {
  const [collapsed, setCollapsed] = React.useState(false);
  
  return (
    <div className={cn("flex h-screen overflow-hidden", className)}>
      <Sidebar 
        collapsed={collapsed} 
        onToggle={() => setCollapsed(!collapsed)}
      >
        {/* Itens do menu administrativo */}
        <SidebarItem 
          icon={<i className="fas fa-chart-line"></i>} 
          label="Dashboard" 
          active={true} 
          collapsed={collapsed} 
          href="/admin/dashboard"
        />
        <SidebarItem 
          icon={<i className="fas fa-shopping-cart"></i>} 
          label="PDV" 
          collapsed={collapsed} 
          href="/admin/pdv"
        />
        <SidebarItem 
          icon={<i className="fas fa-boxes"></i>} 
          label="Estoque" 
          collapsed={collapsed} 
          href="/admin/inventory"
        />
        <SidebarItem 
          icon={<i className="fas fa-users"></i>} 
          label="Clientes" 
          collapsed={collapsed} 
          href="/admin/customers"
        />
        <SidebarItem 
          icon={<i className="fas fa-cog"></i>} 
          label="Configurações" 
          collapsed={collapsed} 
          href="/admin/settings"
        />
      </Sidebar>
      
      <div className={cn("flex flex-col flex-1 overflow-hidden")}>
        <Header>
          <HeaderTitle>
            <h1 className="text-xl font-semibold text-secondary-900">Terman OS</h1>
          </HeaderTitle>
          <HeaderActions>
            <button className="text-secondary-500 hover:text-secondary-700">
              <i className="fas fa-bell"></i>
            </button>
            <button className="text-secondary-500 hover:text-secondary-700">
              <i className="fas fa-user-circle"></i>
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

export const ContentLayout = ({ children, className }) => {
  return (
    <div className={cn("container mx-auto py-8 px-4", className)}>
      {children}
    </div>
  );
};

// Componentes auxiliares
const SidebarItem = ({ icon, label, active, collapsed, href }) => {
  return (
    <a 
      href={href} 
      className={cn(
        "flex items-center px-4 py-3 text-secondary-700 hover:bg-secondary-50 hover:text-secondary-900 rounded-md transition-colors",
        active && "bg-primary-50 text-primary-700",
        collapsed && "justify-center"
      )}
    >
      {icon && <span className={cn("text-xl", !collapsed && "mr-3")}>{icon}</span>}
      {!collapsed && <span>{label}</span>}
    </a>
  );
};

const HeaderTitle = ({ children }) => {
  return <div className="flex items-center">{children}</div>;
};

const HeaderActions = ({ children }) => {
  return <div className="flex items-center space-x-3">{children}</div>;
};
