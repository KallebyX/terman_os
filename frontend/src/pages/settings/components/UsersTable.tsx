import React from 'react';
import { DataTable } from '../../../components/shared/DataTable';
import { Button, Badge } from '../../../components/ui';
import { formatDate } from '../../../utils/format';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive';
  created_at: string;
}

interface UsersTableProps {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (user: User) => void;
}

export const UsersTable: React.FC<UsersTableProps> = ({
  users,
  onEdit,
  onDelete
}) => {
  const columns = [
    { key: 'name', title: 'Nome' },
    { key: 'email', title: 'E-mail' },
    {
      key: 'role',
      title: 'Função',
      render: (user: User) => (
        <span className="capitalize">{user.role}</span>
      )
    },
    {
      key: 'status',
      title: 'Status',
      render: (user: User) => (
        <Badge color={user.status === 'active' ? 'green' : 'red'}>
          {user.status === 'active' ? 'Ativo' : 'Inativo'}
        </Badge>
      )
    },
    {
      key: 'created_at',
      title: 'Data de Cadastro',
      render: (user: User) => formatDate(user.created_at)
    },
    {
      key: 'actions',
      title: 'Ações',
      render: (user: User) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => onEdit(user)}
          >
            Editar
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onDelete(user)}
          >
            Excluir
          </Button>
        </div>
      )
    }
  ];

  return <DataTable data={users} columns={columns} />;
}; 