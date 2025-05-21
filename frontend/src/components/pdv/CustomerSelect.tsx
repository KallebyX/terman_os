import React, { useState, useEffect } from 'react';
import { useCustomers } from '../../hooks/useCustomers';
import { Select } from '../ui/Select';
import { Button } from '../ui/Button';
import { CustomerForm } from '../customers/CustomerForm';
import { Modal } from '../ui/Modal';

interface CustomerSelectProps {
  value: string;
  onChange: (customerId: string) => void;
}

export const CustomerSelect: React.FC<CustomerSelectProps> = ({
  value,
  onChange
}) => {
  const { customers, loading, addCustomer } = useCustomers();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleNewCustomer = async (customerData: any) => {
    try {
      const newCustomer = await addCustomer(customerData);
      onChange(newCustomer.id);
      setIsModalOpen(false);
    } catch (error) {
      console.error('Erro ao criar cliente:', error);
    }
  };

  return (
    <div className="flex space-x-2">
      <div className="flex-1">
        <Select
          label="Cliente"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          options={[
            { value: '', label: 'Selecione um cliente' },
            ...customers.map(customer => ({
              value: customer.id,
              label: customer.name
            }))
          ]}
          disabled={loading}
        />
      </div>
      <div className="flex items-end">
        <Button
          variant="secondary"
          onClick={() => setIsModalOpen(true)}
        >
          Novo Cliente
        </Button>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Novo Cliente"
      >
        <CustomerForm
          onSubmit={handleNewCustomer}
          onCancel={() => setIsModalOpen(false)}
        />
      </Modal>
    </div>
  );
}; 