import React from 'react';
import { Input, Button } from '../ui';

interface FormField {
  name: string;
  label: string;
  type?: string;
  required?: boolean;
  options?: Array<{ value: string; label: string }>;
}

interface FormProps {
  fields: FormField[];
  onSubmit: (data: any) => void;
  initialValues?: Record<string, any>;
  submitText?: string;
  isLoading?: boolean;
}

export const Form: React.FC<FormProps> = ({
  fields,
  onSubmit,
  initialValues = {},
  submitText = 'Salvar',
  isLoading = false
}) => {
  const [values, setValues] = React.useState(initialValues);
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    fields.forEach(field => {
      if (field.required && !values[field.name]) {
        newErrors[field.name] = 'Campo obrigatório';
      }
    });

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit(values);
  };

  const handleChange = (name: string, value: string) => {
    setValues(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {fields.map(field => (
        <div key={field.name}>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {field.label}
            {field.required && <span className="text-red-500">*</span>}
          </label>
          {field.type === 'select' ? (
            <select
              name={field.name}
              value={values[field.name] || ''}
              onChange={e => handleChange(field.name, e.target.value)}
              className="form-select w-full"
            >
              <option value="">Selecione...</option>
              {field.options?.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          ) : (
            <Input
              type={field.type || 'text'}
              name={field.name}
              value={values[field.name] || ''}
              onChange={e => handleChange(field.name, e.target.value)}
              error={errors[field.name]}
            />
          )}
          {errors[field.name] && (
            <p className="text-red-500 text-sm mt-1">{errors[field.name]}</p>
          )}
        </div>
      ))}
      <div className="flex justify-end">
        <Button type="submit" isLoading={isLoading}>
          {submitText}
        </Button>
      </div>
    </form>
  );
}; 