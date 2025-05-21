import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de respostas
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        // Redirecionar para login ou tratar o erro de autenticação
        console.error('Não autorizado, redirecionando para login...');
        // Limpar dados de autenticação
        localStorage.removeItem('auth');
        localStorage.removeItem('access_token');
        // Redirecionar para a página de login
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
