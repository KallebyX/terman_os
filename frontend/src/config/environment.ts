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
};

export default environment;
