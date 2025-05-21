import axios from 'axios';
import { toast } from 'react-toastify';

// Determinar a URL base da API com base no ambiente
const isDocker = process.env.NODE_ENV === 'production' || window.location.hostname !== 'localhost';
const apiUrl = isDocker 
  ? import.meta.env.VITE_API_URL_DOCKER 
  : 'http://localhost:8000';

console.log('API URL:', apiUrl); // Log para debug

// Remover barras duplicadas em URLs e garantir barra final
const formatUrl = (url) => {
  if (!url) return url;
  // Remover barras duplicadas, exceto após o protocolo (http:// ou https://)
  const cleanUrl = url.replace(/(https?:\/\/)|(\/)+/g, "$1$2");
  // Garantir que a URL termina com uma barra
  return cleanUrl.endsWith('/') ? cleanUrl : `${cleanUrl}/`;
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 10000, // Timeout de 10 segundos
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Interceptor para adicionar token JWT em todas as requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('@TermanOS:token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de respostas e refresh de token
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('@TermanOS:token');
      localStorage.removeItem('@TermanOS:user');
      window.location.href = '/login';
    }

    const message = error.response?.data?.message || 'Ocorreu um erro na requisição';
    toast.error(message);

    return Promise.reject(error);
  }
);

export { api };
