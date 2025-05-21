import React from 'react';
import { Button } from '../ui/Button';

interface FormProps {
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent) => void;
  submitLabel?: string;
  isSubmitting?: boolean;
  showCancel?: boolean;
  onCancel?: () => void;
  cancelLabel?: string;
}

export const Form: React.FC<FormProps> = ({
  children,
  onSubmit,
  submitLabel = 'Salvar',
  isSubmitting = false,
  showCancel = false,
  onCancel,
  cancelLabel = 'Cancelar'
}) => {
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      {children}
      <div className="flex justify-end space-x-2">
        {showCancel && (
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
          >
            {cancelLabel}
          </Button>
        )}
        <Button
          type="submit"
          isLoading={isSubmitting}
        >
          {submitLabel}
        </Button>
      </div>
    </form>
  );
}; 