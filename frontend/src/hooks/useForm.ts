import { useState, useCallback } from 'react';
import { validators } from '../utils/validators';

type ValidationRule = (value: any) => string | undefined;

interface FieldConfig {
  value: any;
  rules?: ValidationRule[];
}

interface FormConfig {
  [key: string]: FieldConfig;
}

interface FormErrors {
  [key: string]: string | undefined;
}

export const useForm = <T extends object>(initialConfig: FormConfig) => {
  const [values, setValues] = useState<T>(() => {
    const initialValues: any = {};
    Object.keys(initialConfig).forEach(key => {
      initialValues[key] = initialConfig[key].value;
    });
    return initialValues;
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validateField = useCallback((name: string, value: any) => {
    const fieldConfig = initialConfig[name];
    if (!fieldConfig.rules) return undefined;

    for (const rule of fieldConfig.rules) {
      const error = rule(value);
      if (error) return error;
    }

    return undefined;
  }, [initialConfig]);

  const validateForm = useCallback(() => {
    const newErrors: FormErrors = {};
    let isValid = true;

    Object.keys(initialConfig).forEach(name => {
      const error = validateField(name, values[name as keyof T]);
      if (error) {
        newErrors[name] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  }, [initialConfig, values, validateField]);

  const handleChange = useCallback((name: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [name]: value }));
    setTouched(prev => ({ ...prev, [name]: true }));

    const error = validateField(name as string, value);
    setErrors(prev => ({ ...prev, [name]: error }));
  }, [validateField]);

  const handleBlur = useCallback((name: keyof T) => {
    setTouched(prev => ({ ...prev, [name]: true }));
    const error = validateField(name as string, values[name]);
    setErrors(prev => ({ ...prev, [name]: error }));
  }, [validateField, values]);

  const reset = useCallback(() => {
    const initialValues: any = {};
    Object.keys(initialConfig).forEach(key => {
      initialValues[key] = initialConfig[key].value;
    });
    setValues(initialValues as T);
    setErrors({});
    setTouched({});
  }, [initialConfig]);

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    validateForm,
    reset,
    isValid: Object.keys(errors).length === 0
  };
}; 