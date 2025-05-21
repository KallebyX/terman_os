import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VITE_API_URL || 'http://localhost:8000/api/v1',
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

export default api;
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        // Redirecionar para login ou tratar o erro de autenticação
        console.error('Não autorizado, redirecionando para login...');
      } else {
        console.error(`Erro: ${error.response.status} - ${error.response.data}`);
      }
    } else {
      console.error('Erro na rede ou no servidor.');
    }
    return Promise.reject(error);
  }
);
