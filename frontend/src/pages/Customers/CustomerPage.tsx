import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../../components/ui';
import { DataTable } from '../../components/shared/DataTable';
import { ConfirmDialog } from '../../components/shared/ConfirmDialog';
import { LoadingSpinner } from '../../components/shared/LoadingSpinner';
import { ErrorMessage } from '../../components/shared/ErrorMessage';
import { useCustomers } from '../../hooks/useCustomers';
import { Customer } from '../../types';
import { formatDate } from '../../utils/format';

export const CustomerPage: React.FC = () => {
  const navigate = useNavigate();
  const { customers, isLoading, error, deleteCustomer, fetchCustomers } = useCustomers();
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  const columns = [
    { key: 'name', title: 'Nome' },
    { key: 'email', title: 'E-mail' },
    { key: 'phone', title: 'Telefone' },
    { key: 'document', title: 'CPF/CNPJ' },
    {
      key: 'created_at',
      title: 'Data de Cadastro',
      render: (row: Customer) => formatDate(row.created_at)
    },
    {
      key: 'actions',
      title: 'Ações',
      render: (row: Customer) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="outline"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/customers/${row.id}/edit`);
            }}
          >
            Editar
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={(e) => {
              e.stopPropagation();
              setSelectedCustomer(row);
              setShowDeleteDialog(true);
            }}
          >
            Excluir
          </Button>
        </div>
      )
    }
  ];

  const handleDelete = async () => {
    if (selectedCustomer) {
      try {
        await deleteCustomer(selectedCustomer.id);
        setShowDeleteDialog(false);
        setSelectedCustomer(null);
      } catch (error: any) {
        alert(error.message);
      }
    }
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchCustomers} />;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Clientes</h1>
        <Button onClick={() => navigate('/customers/new')}>
          Novo Cliente
        </Button>
      </div>

      <DataTable
        data={customers}
        columns={columns}
        onRowClick={(row) => navigate(`/customers/${row.id}`)}
      />

      <ConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => {
          setShowDeleteDialog(false);
          setSelectedCustomer(null);
        }}
        onConfirm={handleDelete}
        title="Excluir Cliente"
        message={`Tem certeza que deseja excluir o cliente ${selectedCustomer?.name}?`}
        confirmText="Excluir"
        cancelText="Cancelar"
      />
    </div>
  );
}; 