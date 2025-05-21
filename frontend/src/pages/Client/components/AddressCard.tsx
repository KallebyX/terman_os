import React from 'react';
import { Card, Button } from '../../../components/ui';
import { Address } from '../../../types';

interface AddressCardProps {
  addresses: Address[];
  onAddAddress: () => void;
  onEditAddress: (address: Address) => void;
  onDeleteAddress: (address: Address) => void;
}

export const AddressCard: React.FC<AddressCardProps> = ({
  addresses,
  onAddAddress,
  onEditAddress,
  onDeleteAddress
}) => (
  <Card className="p-6">
    <div className="flex items-center justify-between mb-4">
      <h2 className="text-lg font-medium">Endereços</h2>
      <Button variant="outline" onClick={onAddAddress}>
        Adicionar Endereço
      </Button>
    </div>
    <div className="space-y-4">
      {addresses.length === 0 ? (
        <p className="text-gray-500">Nenhum endereço cadastrado</p>
      ) : (
        addresses.map((address) => (
          <div
            key={address.id}
            className="border rounded-lg p-4 space-y-2"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="font-medium">{address.name}</p>
                <p className="text-sm text-gray-500">
                  {address.street}, {address.number}
                  {address.complement && ` - ${address.complement}`}
                </p>
                <p className="text-sm text-gray-500">
                  {address.neighborhood} - {address.city}/{address.state}
                </p>
                <p className="text-sm text-gray-500">CEP: {address.zipcode}</p>
              </div>
              <div className="flex space-x-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => onEditAddress(address)}
                >
                  Editar
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => onDeleteAddress(address)}
                >
                  Excluir
                </Button>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  </Card>
); 