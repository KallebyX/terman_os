// Configurações de ambiente
const environment = {
  // URL base da API
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  
  // Tempo de expiração do token em milissegundos (padrão: 1 hora)
  tokenExpiration: 60 * 60 * 1000,
  
  // Configurações de paginação
  defaultPageSize: 10,
  
  // Configurações de upload de arquivos
  maxFileSize: 5 * 1024 * 1024, // 5MB
  allowedFileTypes: ['image/jpeg', 'image/png', 'application/pdf'],
  
  // Configurações de cache
  cacheTimeout: 5 * 60 * 1000, // 5 minutos
  
  // Modo de desenvolvimento
  isDevelopment: import.meta.env.MODE === 'development',
  
  // Configurações de autenticação
  auth: {
    tokenKey: 'token',
    refreshTokenKey: 'refresh_token',
    legacyTokenKey: 'access_token',
    authKey: 'auth',
    loginRedirect: '/login',
    homeRedirect: '/dashboard',
  },
  
  // Endpoints da API
  endpoints: {
    auth: {
      login: '/api/accounts/token/',
      refresh: '/api/accounts/token/refresh/',
      register: '/api/accounts/register/',
      profile: '/api/accounts/profile/',
    },
    orders: {
      list: '/api/orders/orders/',
      myOrders: '/api/orders/my-orders/',
      create: '/api/orders/create/',
    },
    products: {
      list: '/api/products/',
      pdvProducts: '/api/products/produtos/',
      top: '/api/products/top',
    },
    customers: {
      list: '/api/accounts/customers/',
    },
    dashboard: {
      kpis: '/api/dashboard/kpis',
      recent: '/api/orders/recent',
      lowStock: '/api/inventory/low-stock',
      activities: '/api/activities/recent',
    },
  }
};

export default environment;
