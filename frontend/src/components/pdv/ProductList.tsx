import React from 'react';
import { Product } from '../../types/common';
import { Card } from '../ui/Card';

interface ProductListProps {
  products: Product[];
  onSelectProduct: (product: Product) => void;
}

export const ProductList: React.FC<ProductListProps> = ({
  products,
  onSelectProduct
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {products.map(product => (
        <Card
          key={product.id}
          className="cursor-pointer hover:shadow-md transition-shadow"
          onClick={() => onSelectProduct(product)}
        >
          <div className="flex items-center space-x-4">
            {product.images[0] && (
              <img
                src={product.images[0]}
                alt={product.name}
                className="w-16 h-16 object-cover rounded"
              />
            )}
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                {product.name}
              </h3>
              <p className="text-sm text-gray-500">
                {product.description}
              </p>
              <p className="mt-1 text-lg font-medium text-gray-900">
                R$ {product.price.toFixed(2)}
              </p>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}; 