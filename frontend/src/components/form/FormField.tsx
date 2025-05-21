import React from 'react';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { Checkbox } from '../ui/Checkbox';

interface FormFieldProps {
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'checkbox';
  name: string;
  label: string;
  value: any;
  onChange: (value: any) => void;
  error?: string;
  options?: Array<{ value: string; label: string }>;
  required?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

export const FormField: React.FC<FormFieldProps> = ({
  type,
  name,
  label,
  value,
  onChange,
  error,
  options = [],
  required = false,
  disabled = false,
  placeholder
}) => {
  switch (type) {
    case 'select':
      return (
        <Select
          name={name}
          label={label}
          value={value}
          onChange={e => onChange(e.target.value)}
          options={options}
          error={error}
          required={required}
          disabled={disabled}
        />
      );

    case 'checkbox':
      return (
        <Checkbox
          name={name}
          label={label}
          checked={value}
          onChange={e => onChange(e.target.checked)}
          error={error}
          disabled={disabled}
        />
      );

    default:
      return (
        <Input
          type={type}
          name={name}
          label={label}
          value={value}
          onChange={e => onChange(e.target.value)}
          error={error}
          required={required}
          disabled={disabled}
          placeholder={placeholder}
        />
      );
  }
}; 