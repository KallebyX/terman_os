import React from 'react';
import { Input } from '../../../components/ui';

interface ProductSearchProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
}

export const ProductSearch: React.FC<ProductSearchProps> = ({
  searchTerm,
  onSearchChange
}) => {
  return (
    <Input
      type="text"
      placeholder="Buscar produto por nome ou código..."
      value={searchTerm}
      onChange={(e) => onSearchChange(e.target.value)}
      className="w-full"
    />
  );
}; 