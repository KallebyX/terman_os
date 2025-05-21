export const validators = {
  required: (value: any): string | undefined => {
    if (!value && value !== 0) return 'Campo obrigatório';
    if (typeof value === 'string' && !value.trim()) return 'Campo obrigatório';
    return undefined;
  },

  email: (value: string): string | undefined => {
    if (!value) return undefined;
    const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
    if (!emailRegex.test(value)) return 'E-mail inválido';
    return undefined;
  },

  cpf: (value: string): string | undefined => {
    if (!value) return undefined;
    const cleaned = value.replace(/\D/g, '');
    if (cleaned.length !== 11) return 'CPF inválido';
    return undefined;
  },

  cnpj: (value: string): string | undefined => {
    if (!value) return undefined;
    const cleaned = value.replace(/\D/g, '');
    if (cleaned.length !== 14) return 'CNPJ inválido';
    return undefined;
  },

  phone: (value: string): string | undefined => {
    if (!value) return undefined;
    const cleaned = value.replace(/\D/g, '');
    if (cleaned.length < 10 || cleaned.length > 11) return 'Telefone inválido';
    return undefined;
  },

  cep: (value: string) => {
    const cep = value.replace(/\D/g, '');
    if (cep.length !== 8) return 'CEP inválido';
    return '';
  },

  minLength: (min: number) => (value: string): string | undefined => {
    if (!value) return undefined;
    if (value.length < min) return `Mínimo de ${min} caracteres`;
    return undefined;
  },

  maxLength: (max: number) => (value: string): string | undefined => {
    if (!value) return undefined;
    if (value.length > max) return `Máximo de ${max} caracteres`;
    return undefined;
  },

  passwordMatch: (password: string, confirmation: string) => {
    if (password !== confirmation) return 'As senhas não coincidem';
    return '';
  },

  numeric: (value: string): string | undefined => {
    if (!value) return undefined;
    if (!/^\d+$/.test(value)) return 'Apenas números são permitidos';
    return undefined;
  },

  price: (value: string): string | undefined => {
    if (!value) return undefined;
    const number = parseFloat(value.replace(',', '.'));
    if (isNaN(number) || number < 0) return 'Valor inválido';
    return undefined;
  }
}; 