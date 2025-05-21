import axios from 'axios';

// Determinar a URL base da API com base no ambiente
const isDocker = process.env.NODE_ENV === 'production' || window.location.hostname !== 'localhost';
const apiUrl = isDocker 
  ? import.meta.env.VITE_API_URL_DOCKER 
  : import.meta.env.VITE_API_URL;

console.log('API URL:', apiUrl); // Log para debug

const api = axios.create({
  baseURL: apiUrl || '/api',
  timeout: 10000, // Timeout de 10 segundos
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Interceptor para adicionar token JWT em todas as requisições
api.interceptors.request.use(
  (config) => {
    // Verificar primeiro o token no localStorage com a chave 'token' (nova implementação)
    let token = localStorage.getItem('token');
    
    // Se não encontrar, tentar com 'access_token' (implementação anterior)
    if (!token) {
      token = localStorage.getItem('access_token');
    }
    
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Adicionar timestamp para evitar cache em requisições GET
    if (config.method?.toLowerCase() === 'get') {
      config.params = {
        ...config.params,
        _t: new Date().getTime()
      };
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de respostas e refresh de token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Se o erro for 401 (não autorizado) e não for uma tentativa de refresh
    if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url?.includes('token/refresh')) {
      originalRequest._retry = true;
      
      try {
        // Tentar renovar o token
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(
            `${api.defaults.baseURL}/api/accounts/token/refresh/`,
            { refresh: refreshToken }
          );
          
          // Armazenar novo token de acesso
          localStorage.setItem('access_token', response.data.access);
          // Também armazenar na nova chave para compatibilidade
          localStorage.setItem('token', response.data.access);
          
          // Atualizar o cabeçalho da requisição original
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
          
          // Repetir a requisição original
          return axios(originalRequest);
        }
      } catch (refreshError) {
        // Se não conseguir renovar, redirecionar para login
        localStorage.removeItem('auth');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    // Tratamento de outros erros
    if (error.response) {
      if (error.response.status === 401) {
        console.error('Não autorizado, redirecionando para login...');
        localStorage.removeItem('auth');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('token');
        window.location.href = '/login';
      } else if (error.response.status === 403) {
        console.error('Acesso proibido: Você não tem permissão para acessar este recurso.');
      } else if (error.response.status === 404) {
        console.error('Recurso não encontrado.');
      } else if (error.response.status === 500) {
        console.error('Erro interno do servidor.');
      } else {
        console.error(`Erro: ${error.response.status} - ${error.response.data.message || JSON.stringify(error.response.data)}`);
      }
    } else if (error.request) {
      console.error('Sem resposta do servidor. Verifique sua conexão com a internet.');
    } else {
      console.error('Erro na configuração da requisição:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;
