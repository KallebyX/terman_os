import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Simulação de login - em produção, isso seria uma chamada à API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Verificar se o email e senha são válidos
      if (email && password) {
        const success = await login(email, password);
        
        if (success) {
          // Redirecionar com base no tipo de usuário (determinado pelo email)
          if (email.includes('admin')) {
            navigate('/admin/dashboard');
          } else if (email.includes('funcionario') || email.includes('staff')) {
            navigate('/admin/pdv'); // Funcionários vão direto para o PDV
          } else {
            navigate('/client');
          }
          
          console.log('Redirecionando após login bem-sucedido');
        } else {
          setError('Credenciais inválidas. Tente novamente.');
        }
      } else {
        setError('Por favor, preencha todos os campos.');
      }
    } catch (err) {
      setError('Falha no login. Verifique suas credenciais.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex flex-col justify-center items-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <div className="text-center mb-8">
          <Link to="/">
            <img 
              src="/logo.png" 
              alt="Mangueiras Terman" 
              className="h-16 mx-auto mb-4"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = 'https://via.placeholder.com/160x64?text=Mangueiras+Terman';
              }}
            />
          </Link>
          <h1 className="text-2xl font-bold text-secondary-900">Bem-vindo ao Terman OS</h1>
          <p className="text-secondary-600">Faça login para acessar o sistema</p>
        </div>

        <Card variant="elevated" className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium text-secondary-700 mb-1">
                Email
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
                required
                fullWidth
              />
            </div>

            <div className="mb-6">
              <div className="flex items-center justify-between mb-1">
                <label htmlFor="password" className="block text-sm font-medium text-secondary-700">
                  Senha
                </label>
                <Link to="/forgot-password" className="text-sm text-primary-600 hover:text-primary-800">
                  Esqueceu a senha?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                fullWidth
              />
            </div>

            <div className="mb-6">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-secondary-300 rounded"
                />
                <span className="ml-2 text-sm text-secondary-700">Lembrar de mim</span>
              </label>
            </div>

            <Button
              type="submit"
              variant="primary"
              fullWidth
              size="lg"
              isLoading={isLoading}
              disabled={isLoading}
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-secondary-600">
              Não tem uma conta?{' '}
              <Link to="/register" className="text-primary-600 hover:text-primary-800 font-medium">
                Cadastre-se
              </Link>
            </p>
          </div>
        </Card>

        <div className="mt-8 text-center">
          <Link to="/" className="text-sm text-secondary-600 hover:text-secondary-900">
            ← Voltar para a página inicial
          </Link>
        </div>
        
        <div className="mt-4 text-center">
          <p className="text-xs text-secondary-500 mb-2">Contas de demonstração:</p>
          <div className="grid grid-cols-3 gap-2 text-xs">
            <div className="bg-secondary-100 p-2 rounded">
              <strong>Admin:</strong><br/>
              admin@terman.com<br/>
              senha123
            </div>
            <div className="bg-secondary-100 p-2 rounded">
              <strong>Funcionário:</strong><br/>
              funcionario@terman.com<br/>
              senha123
            </div>
            <div className="bg-secondary-100 p-2 rounded">
              <strong>Cliente:</strong><br/>
              cliente@terman.com<br/>
              senha123
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default LoginPage;
