import React, { forwardRef } from 'react';
import InputMask from 'react-input-mask';
import { Input } from '../ui/Input';

interface MaskedInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  mask: string;
  label?: string;
  error?: string;
}

export const MaskedInput = forwardRef<HTMLInputElement, MaskedInputProps>(
  ({ mask, label, error, ...props }, ref) => {
    return (
      <InputMask
        mask={mask}
        {...props}
      >
        {(inputProps: any) => (
          <Input
            ref={ref}
            label={label}
            error={error}
            {...inputProps}
          />
        )}
      </InputMask>
    );
  }
);

MaskedInput.displayName = 'MaskedInput'; 