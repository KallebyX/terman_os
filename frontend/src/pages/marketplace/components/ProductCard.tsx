import React from 'react';
import { Card, Button, Badge } from '../../../components/ui';
import { Product } from '../../../types';
import { formatCurrency } from '../../../utils/format';

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => (
  <Card className="h-full flex flex-col">
    <div className="aspect-w-1 aspect-h-1 w-full overflow-hidden rounded-t-lg bg-gray-200">
      {product.image && (
        <img
          src={product.image}
          alt={product.name}
          className="h-full w-full object-cover object-center"
        />
      )}
    </div>
    <div className="flex flex-col flex-1 p-4">
      <h3 className="text-lg font-medium text-gray-900">{product.name}</h3>
      <p className="mt-1 text-sm text-gray-500">{product.description}</p>
      <div className="mt-2">
        <Badge color={product.stock > 0 ? 'green' : 'red'}>
          {product.stock > 0 ? 'Em estoque' : 'Indisponível'}
        </Badge>
      </div>
      <div className="mt-4 flex items-center justify-between">
        <span className="text-xl font-bold text-gray-900">
          {formatCurrency(product.price)}
        </span>
        <Button
          size="sm"
          disabled={product.stock === 0}
          onClick={() => onAddToCart(product)}
        >
          Adicionar
        </Button>
      </div>
    </div>
  </Card>
); 