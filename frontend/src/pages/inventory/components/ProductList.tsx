import React from 'react';
import { DataTable } from '../../../components/shared/DataTable';
import { Button, Badge } from '../../../components/ui';
import { Product } from '../../../types';
import { formatCurrency } from '../../../utils/format';

interface ProductListProps {
  products: Product[];
  onEdit: (product: Product) => void;
  onDelete: (product: Product) => void;
  onStockMovement: (product: Product) => void;
}

export const ProductList: React.FC<ProductListProps> = ({
  products,
  onEdit,
  onDelete,
  onStockMovement
}) => {
  const columns = [
    { key: 'code', title: 'Código' },
    { key: 'name', title: 'Nome' },
    {
      key: 'price',
      title: 'Preço',
      render: (product: Product) => formatCurrency(product.price)
    },
    {
      key: 'stock',
      title: 'Estoque',
      render: (product: Product) => (
        <span className={product.stock <= 10 ? 'text-red-500 font-medium' : ''}>
          {product.stock}
        </span>
      )
    },
    {
      key: 'status',
      title: 'Status',
      render: (product: Product) => (
        <Badge color={product.status === 'active' ? 'green' : 'red'}>
          {product.status === 'active' ? 'Ativo' : 'Inativo'}
        </Badge>
      )
    },
    {
      key: 'actions',
      title: 'Ações',
      render: (product: Product) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => onEdit(product)}
          >
            Editar
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onStockMovement(product)}
          >
            Estoque
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onDelete(product)}
          >
            Excluir
          </Button>
        </div>
      )
    }
  ];

  return (
    <DataTable
      data={products}
      columns={columns}
    />
  );
}; 