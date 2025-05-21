import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { getUserFromToken, setupAxiosInterceptors } from '../utils/auth';

// Definindo o tipo para o contexto de autenticação
interface AuthContextType {
  isAuthenticated: boolean;
  userRole: string | null;
  userName: string | null;
  userId: number | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

// Criando o contexto com valores padrão
const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userRole: null,
  userName: null,
  userId: null,
  login: async () => false,
  logout: () => {},
});

// Hook personalizado para usar o contexto de autenticação
export const useAuth = () => useContext(AuthContext);

// Provedor do contexto de autenticação
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userRole, setUserRole] = useState<string | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null);

  // Configurar interceptores do Axios
  useEffect(() => {
    setupAxiosInterceptors();
  }, []);

  // Verificar se o usuário já está autenticado ao carregar a página
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        // Decodificar o token para obter informações do usuário
        const userData = getUserFromToken(token);
        
        if (userData) {
          setIsAuthenticated(true);
          
          // Definir o papel do usuário com base nas claims do token
          let role = 'customer';
          if (userData.is_admin) {
            role = 'admin';
          } else if (userData.is_seller) {
            role = 'seller';
          } else if (userData.is_operator) {
            role = 'operator';
          }
          
          setUserRole(role);
          setUserName(userData.name || userData.email.split('@')[0]);
          setUserId(userData.user_id);
          
          // Armazenar dados de autenticação para uso offline
          const authData = { 
            email: userData.email, 
            role, 
            name: userData.name,
            user_id: userData.user_id
          };
          localStorage.setItem('auth', JSON.stringify(authData));
        }
      } catch (error) {
        console.error('Erro ao decodificar token:', error);
        logout(); // Limpar dados de autenticação em caso de erro
      }
    }
  }, []);

  // Função de login
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // Autenticação real - chamada à API para obter o token JWT
      const response = await axios.post('/api/accounts/login/', {
        email,
        password
      });

      if (response.data && response.data.access) {
        const { access, refresh, user } = response.data;
        
        // Armazenar tokens
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        
        // Definir o papel do usuário com base na resposta da API
        let role = 'customer';
        if (user.is_admin) {
          role = 'admin';
        } else if (user.is_seller) {
          role = 'seller';
        } else if (user.is_operator) {
          role = 'operator';
        }
        
        // Armazenar dados de autenticação
        const authData = { 
          email: user.email, 
          role, 
          name: user.first_name + ' ' + user.last_name,
          user_id: user.id
        };
        localStorage.setItem('auth', JSON.stringify(authData));
        
        // Atualizar estado
        setIsAuthenticated(true);
        setUserRole(role);
        setUserName(authData.name);
        setUserId(user.id);
        
        return true;
      }
      return false;
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      return false;
    }
  };

  // Função de logout
  const logout = () => {
    localStorage.removeItem('auth');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
    setUserRole(null);
    setUserName(null);
    setUserId(null);
  };

  // Valores fornecidos pelo contexto
  const value = {
    isAuthenticated,
    userRole,
    userName,
    userId,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
