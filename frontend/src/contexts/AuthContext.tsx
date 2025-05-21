/add backend/tests/import React, { createContext, useContext, useState, useEffect } from 'react';

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
      setUserName(authData.name || authData.email.split('@')[0]);
    }
  }, []);

  // Função de login
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // Simulação de autenticação - em produção, isso seria uma chamada à API
      // Verificação simplificada para demonstração
      if (email && password) {
        let role = 'client';
        
        // Determinar o papel do usuário com base no email
        // Exemplo: emails com "admin" são administradores
        if (email.includes('admin')) {
          role = 'admin';
        }
        
        // Extrair nome do usuário do email
        const name = email.split('@')[0];
        
        // Armazenar dados de autenticação
        const authData = { email, role, name };
        localStorage.setItem('auth', JSON.stringify(authData));
        
        // Simular token JWT para autenticação
        localStorage.setItem('access_token', 'jwt_token_simulado');
        
        setIsAuthenticated(true);
        setUserRole(role);
        setUserName(name);
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
