import React from 'react';
import { Input } from '../../../components/ui';

interface ProductFiltersProps {
  categories: string[];
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
  searchTerm: string;
  onSearchChange: (term: string) => void;
  minPrice: number;
  maxPrice: number;
  onPriceChange: (min: number, max: number) => void;
}

export const ProductFilters: React.FC<ProductFiltersProps> = ({
  categories,
  selectedCategory,
  onCategoryChange,
  searchTerm,
  onSearchChange,
  minPrice,
  maxPrice,
  onPriceChange
}) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-medium mb-2">Categorias</h3>
      <div className="space-y-2">
        <div
          className={`cursor-pointer ${
            selectedCategory === '' ? 'text-primary-600 font-medium' : ''
          }`}
          onClick={() => onCategoryChange('')}
        >
          Todas
        </div>
        {categories.map((category) => (
          <div
            key={category}
            className={`cursor-pointer ${
              selectedCategory === category ? 'text-primary-600 font-medium' : ''
            }`}
            onClick={() => onCategoryChange(category)}
          >
            {category}
          </div>
        ))}
      </div>
    </div>

    <div>
      <h3 className="text-lg font-medium mb-2">Buscar</h3>
      <Input
        type="text"
        placeholder="Buscar produtos..."
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
      />
    </div>

    <div>
      <h3 className="text-lg font-medium mb-2">Preço</h3>
      <div className="flex items-center space-x-2">
        <Input
          type="number"
          placeholder="Min"
          value={minPrice || ''}
          onChange={(e) => onPriceChange(Number(e.target.value), maxPrice)}
        />
        <span>até</span>
        <Input
          type="number"
          placeholder="Max"
          value={maxPrice || ''}
          onChange={(e) => onPriceChange(minPrice, Number(e.target.value))}
        />
      </div>
    </div>
  </div>
); 