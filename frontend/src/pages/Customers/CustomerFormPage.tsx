import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import api from '../../services/api';

const CustomerFormPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const redirectTo = queryParams.get('redirect');
  
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zipcode: '',
    notes: ''
  });
  
  // Carregar dados do cliente se estiver editando
  useEffect(() => {
    if (id) {
      const fetchCustomer = async () => {
        setIsLoading(true);
        try {
          const response = await api.get(`/accounts/customers/${id}/`);
          
          if (response.status !== 200) {
            throw new Error(`Erro na requisição: ${response.status}`);
          }
          
          setFormData(response.data);
        } catch (error) {
          console.error('Erro ao carregar dados do cliente:', error);
          setError('Não foi possível carregar os dados do cliente. Por favor, tente novamente.');
        } finally {
          setIsLoading(false);
        }
      };
      
      fetchCustomer();
    }
  }, [id]);
  
  // Atualizar campo do formulário
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  // Enviar formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setError(null);
    
    try {
      let response;
      
      if (id) {
        // Atualizar cliente existente
        response = await api.put(`/accounts/customers/${id}/`, formData);
      } else {
        // Criar novo cliente
        response = await api.post('/accounts/customers/', formData);
      }
      
      if (response.status !== 200 && response.status !== 201) {
        throw new Error(`Erro na requisição: ${response.status}`);
      }
      
      // Redirecionar após salvar
      if (redirectTo === 'pdv') {
        navigate('/pdv', { state: { newCustomer: response.data } });
      } else {
        navigate('/customers');
      }
    } catch (error: any) {
      console.error('Erro ao salvar cliente:', error);
      setError(
        error.response?.data?.message || 
        'Não foi possível salvar os dados do cliente. Por favor, verifique os campos e tente novamente.'
      );
    } finally {
      setIsSaving(false);
    }
  };
  
  return (
    <div className="p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="mb-6">
          <h1 className="text-2xl font-bold">{id ? 'Editar Cliente' : 'Novo Cliente'}</h1>
          <p className="text-secondary-500">
            {id ? 'Atualize os dados do cliente' : 'Preencha os dados para cadastrar um novo cliente'}
          </p>
        </div>
        
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md text-red-700">
            <p>{error}</p>
          </div>
        )}
        
        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary-500 border-t-transparent"></div>
          </div>
        ) : (
          <Card variant="elevated">
            <form onSubmit={handleSubmit}>
              <div className="p-6 border-b border-secondary-200">
                <h2 className="text-lg font-semibold">Informações Básicas</h2>
              </div>
              
              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    Nome Completo *
                  </label>
                  <Input
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder="Nome completo do cliente"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    Email
                  </label>
                  <Input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="email@exemplo.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    Telefone *
                  </label>
                  <Input
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    required
                    placeholder="(00) 00000-0000"
                  />
                </div>
                
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    Endereço
                  </label>
                  <Input
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    placeholder="Rua, número, complemento"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    Cidade
                  </label>
                  <Input
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    placeholder="Cidade"
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-secondary-700 mb-1">
                      Estado
                    </label>
                    <Input
                      name="state"
                      value={formData.state}
                      onChange={handleChange}
                      placeholder="UF"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-secondary-700 mb-1">
                      CEP
                    </label>
                    <Input
                      name="zipcode"
                      value={formData.zipcode}
                      onChange={handleChange}
                      placeholder="00000-000"
                    />
                  </div>
                </div>
                
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    Observações
                  </label>
                  <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Informações adicionais sobre o cliente"
                  ></textarea>
                </div>
              </div>
              
              <div className="p-6 border-t border-secondary-200 bg-secondary-50 flex justify-between">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    if (redirectTo === 'pdv') {
                      navigate('/pdv');
                    } else {
                      navigate('/customers');
                    }
                  }}
                >
                  Cancelar
                </Button>
                
                <Button
                  type="submit"
                  variant="primary"
                  disabled={isSaving}
                >
                  {isSaving ? (
                    <>
                      <span className="animate-spin inline-block h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></span>
                      Salvando...
                    </>
                  ) : (
                    'Salvar Cliente'
                  )}
                </Button>
              </div>
            </form>
          </Card>
        )}
      </motion.div>
    </div>
  );
};

export default CustomerFormPage;
