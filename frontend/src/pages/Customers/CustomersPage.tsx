import React, { useState } from 'react';
import { useCustomers } from '../../hooks/useCustomers';
import { Button } from '../../components/ui/Button';
import { Table, Thead, Tbody, Th, Td } from '../../components/ui/Table';
import { Modal } from '../../components/ui/Modal';
import { CustomerForm } from './components/CustomerForm';
import { Badge } from '../../components/ui/Badge';

interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  status: 'active' | 'inactive';
  createdAt: string;
}

export const CustomersPage: React.FC = () => {
  const { customers, loading, addCustomer, updateCustomer, deleteCustomer } = useCustomers();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  const handleSubmit = async (data: Partial<Customer>) => {
    try {
      if (selectedCustomer) {
        await updateCustomer(selectedCustomer.id, data);
      } else {
        await addCustomer(data as Omit<Customer, 'id' | 'createdAt'>);
      }
      setIsModalOpen(false);
      setSelectedCustomer(null);
    } catch (error) {
      console.error('Erro ao salvar cliente:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Clientes</h1>
        <Button onClick={() => setIsModalOpen(true)}>
          Novo Cliente
        </Button>
      </div>

      {loading ? (
        <div>Carregando...</div>
      ) : (
        <Table>
          <Thead>
            <tr>
              <Th>Nome</Th>
              <Th>Email</Th>
              <Th>Telefone</Th>
              <Th>Status</Th>
              <Th>Ações</Th>
            </tr>
          </Thead>
          <Tbody>
            {customers.map(customer => (
              <tr key={customer.id}>
                <Td>{customer.name}</Td>
                <Td>{customer.email}</Td>
                <Td>{customer.phone}</Td>
                <Td>
                  <Badge
                    variant={customer.status === 'active' ? 'success' : 'danger'}
                  >
                    {customer.status === 'active' ? 'Ativo' : 'Inativo'}
                  </Badge>
                </Td>
                <Td>
                  <div className="flex space-x-2">
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => {
                        setSelectedCustomer(customer);
                        setIsModalOpen(true);
                      }}
                    >
                      Editar
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => {
                        if (window.confirm('Deseja realmente excluir este cliente?')) {
                          deleteCustomer(customer.id);
                        }
                      }}
                    >
                      Excluir
                    </Button>
                  </div>
                </Td>
              </tr>
            ))}
          </Tbody>
        </Table>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedCustomer(null);
        }}
        title={selectedCustomer ? 'Editar Cliente' : 'Novo Cliente'}
      >
        <CustomerForm
          initialData={selectedCustomer}
          onSubmit={handleSubmit}
          onCancel={() => {
            setIsModalOpen(false);
            setSelectedCustomer(null);
          }}
        />
      </Modal>
    </div>
  );
}; 