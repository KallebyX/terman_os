import React, { createContext, useContext, useState, useEffect } from 'react';

// Definindo o tipo para o contexto de autenticação
interface AuthContextType {
  isAuthenticated: boolean;
  userRole: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

// Criando o contexto com valores padrão
const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userRole: null,
  login: async () => false,
  logout: () => {},
});

// Hook personalizado para usar o contexto de autenticação
export const useAuth = () => useContext(AuthContext);

// Provedor do contexto de autenticação
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userRole, setUserRole] = useState<string | null>(null);

  // Verificar se o usuário já está autenticado ao carregar a página
  useEffect(() => {
    const storedAuth = localStorage.getItem('auth');
    if (storedAuth) {
      const authData = JSON.parse(storedAuth);
      setIsAuthenticated(true);
      setUserRole(authData.role);
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
        
        // Armazenar dados de autenticação
        const authData = { email, role };
        localStorage.setItem('auth', JSON.stringify(authData));
        
        setIsAuthenticated(true);
        setUserRole(role);
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
    setIsAuthenticated(false);
    setUserRole(null);
  };

  // Valores fornecidos pelo contexto
  const value = {
    isAuthenticated,
    userRole,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
