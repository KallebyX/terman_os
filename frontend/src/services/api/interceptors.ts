import { AxiosInstance } from 'axios';
import { toast } from 'react-toastify';
import { useAuth } from '../../hooks/useAuth';

export const setupInterceptors = (axios: AxiosInstance) => {
    axios.interceptors.request.use(
        config => {
            // Adicionar token a cada requisição
            const token = localStorage.getItem('@TermanOS:token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        error => {
            return Promise.reject(error);
        }
    );

    axios.interceptors.response.use(
        response => response,
        error => {
            if (error.response) {
                switch (error.response.status) {
                    case 401:
                        // Token expirado ou inválido
                        const { signOut } = useAuth();
                        signOut();
                        toast.error('Sessão expirada. Por favor, faça login novamente.');
                        break;
                    case 403:
                        toast.error('Você não tem permissão para realizar esta ação.');
                        break;
                    case 429:
                        toast.error('Muitas requisições. Por favor, aguarde um momento.');
                        break;
                    default:
                        toast.error(error.response.data.message || 'Ocorreu um erro na requisição.');
                }
            } else {
                toast.error('Erro de conexão. Verifique sua internet.');
            }
            return Promise.reject(error);
        }
    );
}; 