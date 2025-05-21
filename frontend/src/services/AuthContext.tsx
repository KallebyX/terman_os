import React, { createContext, useContext, useState, useEffect } from 'react';

// Definindo o tipo para o contexto de autenticação
interface AuthContextType {
  isAuthenticated: boolean;
  userRole: string | null;
  userName: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

// Criando o contexto com valores padrão
const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userRole: null,
  userName: null,
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

  // Verificar se o usuário já está autenticado ao carregar a página
  useEffect(() => {
    const storedAuth = localStorage.getItem('auth');
    if (storedAuth) {
      const authData = JSON.parse(storedAuth);
      setIsAuthenticated(true);
      setUserRole(authData.role);
      setUserName(authData.name);
    }
  }, []);

  // Função de login com armazenamento de token
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // Autenticação real - chamada à API para obter o token JWT
      const response = await fetch('/api/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const { access, refresh } = data;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        setIsAuthenticated(true);
        // Determinar o papel do usuário com base no token ou resposta
        // Exemplo: emails com "admin" são administradores
        let role = 'client';
        if (email.includes('admin')) {
          role = 'admin';
        }
        setUserRole(role);
        return true;
      }
      // Remover verificação simplificada e usar dados reais da API
      return false;
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      return false;
    }
  };

  // Função de logout com remoção de token
  const logout = () => {
    localStorage.removeItem('auth');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
    setUserRole(null);
    setUserName(null);
  };

  // Valores fornecidos pelo contexto
  const value = {
    isAuthenticated,
    userRole,
    userName,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;
