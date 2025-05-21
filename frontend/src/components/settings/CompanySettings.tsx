import React, { useState } from 'react';
import { Card } from '../ui/Card';
import { Form } from '../form/Form';
import { FormField } from '../form/FormField';
import { FileUpload } from '../form/FileUpload';
import { useForm } from '../../hooks/useForm';
import { validators } from '../../utils/validators';
import { useToast } from '../ui/Toast';

interface CompanySettingsProps {
  initialData: {
    name: string;
    cnpj: string;
    email: string;
    phone: string;
    address: string;
    logo?: string;
  };
  onSave: (data: any) => Promise<void>;
}

export const CompanySettings: React.FC<CompanySettingsProps> = ({
  initialData,
  onSave
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [logo, setLogo] = useState<File | null>(null);
  const { addToast } = useToast();

  const form = useForm({
    name: {
      value: initialData.name,
      rules: [validators.required, validators.minLength(3)]
    },
    cnpj: {
      value: initialData.cnpj,
      rules: [validators.required, validators.cnpj]
    },
    email: {
      value: initialData.email,
      rules: [validators.required, validators.email]
    },
    phone: {
      value: initialData.phone,
      rules: [validators.required, validators.phone]
    },
    address: {
      value: initialData.address,
      rules: [validators.required]
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.validateForm()) return;

    try {
      setIsSubmitting(true);
      await onSave({
        ...form.values,
        logo: logo ? await uploadLogo(logo) : initialData.logo
      });
      addToast('Configurações salvas com sucesso!', 'success');
    } catch (error) {
      addToast('Erro ao salvar configurações', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const uploadLogo = async (file: File): Promise<string> => {
    // Implementar lógica de upload do logo
    return '';
  };

  return (
    <Card>
      <div className="p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-6">
          Dados da Empresa
        </h3>

        <Form
          onSubmit={handleSubmit}
          submitLabel="Salvar Alterações"
          isSubmitting={isSubmitting}
        >
          <div className="mb-6">
            <FileUpload
              label="Logo da Empresa"
              onFileSelect={setLogo}
              accept="image/*"
              maxSize={2 * 1024 * 1024} // 2MB
            />
            {initialData.logo && !logo && (
              <img
                src={initialData.logo}
                alt="Logo atual"
                className="mt-2 h-20 w-auto"
              />
            )}
          </div>

          <FormField
            type="text"
            name="name"
            label="Nome da Empresa"
            value={form.values.name}
            onChange={(value) => form.handleChange('name', value)}
            error={form.touched.name ? form.errors.name : undefined}
          />

          <FormField
            type="text"
            name="cnpj"
            label="CNPJ"
            value={form.values.cnpj}
            onChange={(value) => form.handleChange('cnpj', value)}
            error={form.touched.cnpj ? form.errors.cnpj : undefined}
          />

          <FormField
            type="email"
            name="email"
            label="E-mail"
            value={form.values.email}
            onChange={(value) => form.handleChange('email', value)}
            error={form.touched.email ? form.errors.email : undefined}
          />

          <FormField
            type="text"
            name="phone"
            label="Telefone"
            value={form.values.phone}
            onChange={(value) => form.handleChange('phone', value)}
            error={form.touched.phone ? form.errors.phone : undefined}
          />

          <FormField
            type="text"
            name="address"
            label="Endereço"
            value={form.values.address}
            onChange={(value) => form.handleChange('address', value)}
            error={form.touched.address ? form.errors.address : undefined}
          />
        </Form>
      </div>
    </Card>
  );
}; 