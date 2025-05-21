import { useState, useEffect, useCallback } from 'react';
import { api } from '../config/api';
import { useToast } from '../components/ui/Toast';

interface CompanySettings {
  name: string;
  cnpj: string;
  email: string;
  phone: string;
  address: string;
  logo?: string;
}

interface SystemSettings {
  allowNegativeStock: boolean;
  requireCustomerForSale: boolean;
  defaultTaxRate: number;
  emailNotifications: boolean;
}

export const useSettings = () => {
  const [loading, setLoading] = useState(true);
  const [companySettings, setCompanySettings] = useState<CompanySettings | null>(null);
  const [systemSettings, setSystemSettings] = useState<SystemSettings | null>(null);
  const { addToast } = useToast();

  const fetchSettings = useCallback(async () => {
    try {
      setLoading(true);
      const [companyResponse, systemResponse] = await Promise.all([
        api.get('/settings/company'),
        api.get('/settings/system')
      ]);
      setCompanySettings(companyResponse.data);
      setSystemSettings(systemResponse.data);
    } catch (error) {
      addToast('Erro ao carregar configurações', 'error');
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const updateCompanySettings = async (data: Partial<CompanySettings>) => {
    try {
      const response = await api.put('/settings/company', data);
      setCompanySettings(response.data);
      addToast('Configurações da empresa atualizadas!', 'success');
    } catch (error) {
      addToast('Erro ao atualizar configurações da empresa', 'error');
      throw error;
    }
  };

  const updateSystemSettings = async (data: Partial<SystemSettings>) => {
    try {
      const response = await api.put('/settings/system', data);
      setSystemSettings(response.data);
      addToast('Configurações do sistema atualizadas!', 'success');
    } catch (error) {
      addToast('Erro ao atualizar configurações do sistema', 'error');
      throw error;
    }
  };

  const uploadLogo = async (file: File) => {
    try {
      const formData = new FormData();
      formData.append('logo', file);
      
      const response = await api.post('/settings/company/logo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      setCompanySettings(prev => prev ? { ...prev, logo: response.data.logo } : null);
      addToast('Logo atualizado com sucesso!', 'success');
    } catch (error) {
      addToast('Erro ao atualizar logo', 'error');
      throw error;
    }
  };

  return {
    loading,
    companySettings,
    systemSettings,
    updateCompanySettings,
    updateSystemSettings,
    uploadLogo,
    refetch: fetchSettings
  };
}; 