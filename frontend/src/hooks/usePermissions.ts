import { useAuth } from './useAuth';

type Permission = 'admin' | 'manager' | 'seller' | 'client';

interface PermissionCheck {
  canViewFinancials: boolean;
  canManageUsers: boolean;
  canViewReports: boolean;
  canExportReports: boolean;
  canManageInventory: boolean;
  canViewClientData: boolean;
  canManageProducts: boolean;
  canManageOrders: boolean;
}

export const usePermissions = (): PermissionCheck => {
  const { user } = useAuth();

  const userRole = user?.role as Permission;

  return {
    canViewFinancials: ['admin', 'manager'].includes(userRole),
    canManageUsers: ['admin'].includes(userRole),
    canViewReports: ['admin', 'manager', 'seller'].includes(userRole),
    canExportReports: ['admin', 'manager'].includes(userRole),
    canManageInventory: ['admin', 'manager'].includes(userRole),
    canViewClientData: ['admin', 'manager', 'seller'].includes(userRole),
    canManageProducts: ['admin', 'manager'].includes(userRole),
    canManageOrders: ['admin', 'manager', 'seller'].includes(userRole)
  };
}; 