import React, { useState, useEffect } from 'react';
import { Input } from '../ui/Input';
import { Card } from '../ui/Card';
import { formatCurrency } from '../../utils/formatters';
import { Product } from '../../types/common';

interface ProductSearchProps {
  products: Product[];
  onSelectProduct: (product: Product) => void;
}

export const ProductSearch: React.FC<ProductSearchProps> = ({
  products,
  onSelectProduct
}) => {
  const [search, setSearch] = useState('');
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);

  useEffect(() => {
    const filtered = products.filter(product =>
      product.name.toLowerCase().includes(search.toLowerCase()) ||
      product.id.toLowerCase().includes(search.toLowerCase())
    );
    setFilteredProducts(filtered.slice(0, 5));
  }, [search, products]);

  return (
    <div className="relative">
      <Input
        type="text"
        placeholder="Buscar produto por nome ou código"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {search && filteredProducts.length > 0 && (
        <Card className="absolute z-10 w-full mt-1 max-h-60 overflow-y-auto">
          {filteredProducts.map(product => (
            <div
              key={product.id}
              className="p-2 hover:bg-gray-50 cursor-pointer"
              onClick={() => {
                onSelectProduct(product);
                setSearch('');
              }}
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium text-gray-900">{product.name}</p>
                  <p className="text-sm text-gray-500">Código: {product.id}</p>
                </div>
                <p className="font-medium text-gray-900">
                  {formatCurrency(product.price)}
                </p>
              </div>
            </div>
          ))}
        </Card>
      )}
    </div>
  );
}; 