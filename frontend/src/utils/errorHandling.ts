import { AxiosError } from 'axios';

/**
 * Extrai a mensagem de erro de uma resposta da API
 */
export const getErrorMessage = (error: any): string => {
  if (error.response) {
    // O servidor respondeu com um status de erro
    const { data, status } = error.response;
    
    // Verificar se há uma mensagem de erro específica na resposta
    if (data.message) {
      return data.message;
    }
    
    // Verificar se há erros de validação
    if (data.errors) {
      return Object.values(data.errors).flat().join(', ');
    }
    
    // Mensagens padrão baseadas no status HTTP
    switch (status) {
      case 400:
        return 'Requisição inválida. Verifique os dados enviados.';
      case 401:
        return 'Não autorizado. Faça login novamente.';
      case 403:
        return 'Acesso negado. Você não tem permissão para esta ação.';
      case 404:
        return 'Recurso não encontrado.';
      case 422:
        return 'Dados inválidos. Verifique as informações enviadas.';
      case 500:
        return 'Erro interno do servidor. Tente novamente mais tarde.';
      default:
        return `Erro ${status}: ${data.detail || 'Ocorreu um erro inesperado'}`;
    }
  } else if (error.request) {
    // A requisição foi feita mas não houve resposta
    return 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet.';
  } else {
    // Erro na configuração da requisição
    return error.message || 'Ocorreu um erro inesperado.';
  }
};

/**
 * Trata erros de API de forma padronizada
 */
export const handleApiError = (error: any, defaultMessage: string = 'Ocorreu um erro inesperado'): string => {
  console.error('API Error:', error);
  
  // Registrar erro para análise (em produção, poderia enviar para um serviço de monitoramento)
  if (process.env.NODE_ENV !== 'production') {
    console.group('Detalhes do erro:');
    console.error('Mensagem:', error.message);
    console.error('Status:', error.response?.status);
    console.error('Dados:', error.response?.data);
    console.groupEnd();
  }
  
  return getErrorMessage(error) || defaultMessage;
};

/**
 * Verifica se o erro é de autenticação (401)
 */
export const isAuthError = (error: AxiosError): boolean => {
  return error.response?.status === 401;
};

/**
 * Verifica se o erro é de permissão (403)
 */
export const isPermissionError = (error: AxiosError): boolean => {
  return error.response?.status === 403;
};

/**
 * Verifica se o erro é de validação (422 ou 400 com erros específicos)
 */
export const isValidationError = (error: AxiosError): boolean => {
  return error.response?.status === 422 || 
    (error.response?.status === 400 && error.response?.data?.errors !== undefined);
};
