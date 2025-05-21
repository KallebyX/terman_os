import React, { createContext, useContext, useState, useCallback } from 'react';
import { User } from '../types';
import { api } from '../services/api';
import { useNavigate } from 'react-router-dom';

interface AuthContextData {
  user: User | null;
  signed: boolean;
  loading: boolean;
  signIn: (credentials: SignInCredentials) => Promise<void>;
  signOut: () => void;
  updateUser: (user: User) => void;
}

interface SignInCredentials {
  email: string;
  password: string;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const signIn = useCallback(async ({ email, password }: SignInCredentials) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { user, token } = response.data;

      localStorage.setItem('@TermanOS:token', token);
      localStorage.setItem('@TermanOS:user', JSON.stringify(user));

      api.defaults.headers.authorization = `Bearer ${token}`;
      setUser(user);
      navigate('/dashboard');
    } catch (error) {
      throw new Error('Erro na autenticação');
    }
  }, [navigate]);

  const signOut = useCallback(() => {
    localStorage.removeItem('@TermanOS:token');
    localStorage.removeItem('@TermanOS:user');
    setUser(null);
    navigate('/');
  }, [navigate]);

  const updateUser = useCallback((userData: User) => {
    setUser(userData);
    localStorage.setItem('@TermanOS:user', JSON.stringify(userData));
  }, []);

  return (
    <AuthContext.Provider value={{ signed: !!user, user, loading, signIn, signOut, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
