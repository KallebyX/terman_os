import React from 'react';
import { Modal, Button, Input } from '../../../components/ui';
import { Product } from '../../../types';

interface StockMovementProps {
  product: Product | null;
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (quantity: number, type: 'add' | 'remove') => void;
}

export const StockMovement: React.FC<StockMovementProps> = ({
  product,
  isOpen,
  onClose,
  onConfirm
}) => {
  const [quantity, setQuantity] = React.useState(0);
  const [type, setType] = React.useState<'add' | 'remove'>('add');

  if (!product) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Movimentação de Estoque"
    >
      <div className="space-y-4">
        <div>
          <p className="font-medium">{product.name}</p>
          <p className="text-sm text-gray-500">Estoque atual: {product.stock}</p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Tipo de Movimentação</label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value as 'add' | 'remove')}
            className="form-select w-full"
          >
            <option value="add">Entrada</option>
            <option value="remove">Saída</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Quantidade</label>
          <Input
            type="number"
            min={1}
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
          />
        </div>

        <div className="flex justify-end space-x-2">
          <Button variant="outline" onClick={onClose}>
            Cancelar
          </Button>
          <Button
            onClick={() => {
              onConfirm(quantity, type);
              setQuantity(0);
              onClose();
            }}
            disabled={quantity <= 0}
          >
            Confirmar
          </Button>
        </div>
      </div>
    </Modal>
  );
}; 