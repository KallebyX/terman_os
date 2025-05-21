import axios from 'axios';

/**
 * Verifica se o token JWT está expirado
 * @param token Token JWT a ser verificado
 * @returns Verdadeiro se o token estiver expirado
 */
export const isTokenExpired = (token: string): boolean => {
  try {
    // Decodificar o token (parte do payload)
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const payload = JSON.parse(window.atob(base64));
    
    // Verificar se o token expirou
    const expirationTime = payload.exp * 1000; // Converter para milissegundos
    return Date.now() >= expirationTime;
  } catch (error) {
    console.error('Erro ao verificar expiração do token:', error);
    return true; // Em caso de erro, considerar o token como expirado
  }
};

/**
 * Obtém o perfil do usuário a partir do token JWT
 * @param token Token JWT
 * @returns Objeto com informações do usuário
 */
export const getUserFromToken = (token: string): any => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(window.atob(base64));
  } catch (error) {
    console.error('Erro ao decodificar token:', error);
    return null;
  }
};

/**
 * Atualiza o token de acesso usando o token de refresh
 * @returns Promise com o novo token de acesso ou null em caso de erro
 */
export const refreshAccessToken = async (): Promise<string | null> => {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      return null;
    }
    
    const response = await axios.post('/api/accounts/token/refresh/', {
      refresh: refreshToken
    });
    
    if (response.data && response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      return response.data.access;
    }
    
    return null;
  } catch (error) {
    console.error('Erro ao atualizar token:', error);
    return null;
  }
};

/**
 * Configura o interceptor do Axios para adicionar o token JWT em todas as requisições
 * e atualizar automaticamente o token quando expirado
 */
export const setupAxiosInterceptors = () => {
  // Interceptor para adicionar o token em todas as requisições
  axios.interceptors.request.use(
    async (config) => {
      let token = localStorage.getItem('access_token');
      
      // Se o token existir e estiver expirado, tentar atualizá-lo
      if (token && isTokenExpired(token)) {
        const newToken = await refreshAccessToken();
        if (newToken) {
          token = newToken;
        } else {
          // Se não conseguir atualizar o token, fazer logout
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('auth');
          window.location.href = '/login';
          return Promise.reject('Sessão expirada. Por favor, faça login novamente.');
        }
      }
      
      // Adicionar o token ao cabeçalho da requisição
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
  // Interceptor para tratar erros de resposta
  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      // Se o erro for 401 (não autorizado), tentar atualizar o token
      if (error.response && error.response.status === 401) {
        const originalRequest = error.config;
        
        // Evitar loop infinito
        if (!originalRequest._retry) {
          originalRequest._retry = true;
          
          const newToken = await refreshAccessToken();
          
          if (newToken) {
            // Atualizar o cabeçalho da requisição original
            originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
            return axios(originalRequest);
          } else {
            // Se não conseguir atualizar o token, fazer logout
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('auth');
            window.location.href = '/login';
          }
        }
      }
      
      return Promise.reject(error);
    }
  );
};
