import { AxiosError } from 'axios';

interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

export const errorHandler = {
  getErrorMessage(error: unknown): string {
    if (error instanceof AxiosError) {
      const data = error.response?.data as ApiError;
      
      if (data?.message) {
        return data.message;
      }

      if (data?.errors) {
        return Object.values(data.errors)
          .flat()
          .join(', ');
      }

      switch (error.response?.status) {
        case 400:
          return 'Requisição inválida';
        case 401:
          return 'Não autorizado';
        case 403:
          return 'Acesso negado';
        case 404:
          return 'Recurso não encontrado';
        case 422:
          return 'Dados inválidos';
        case 500:
          return 'Erro interno do servidor';
        default:
          return 'Ocorreu um erro inesperado';
      }
    }

    if (error instanceof Error) {
      return error.message;
    }

    return 'Ocorreu um erro inesperado';
  },

  isNetworkError(error: unknown): boolean {
    return error instanceof AxiosError && !error.response;
  },

  isAuthenticationError(error: unknown): boolean {
    return error instanceof AxiosError && error.response?.status === 401;
  },

  isValidationError(error: unknown): boolean {
    return error instanceof AxiosError && error.response?.status === 422;
  }
}; 