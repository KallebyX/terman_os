import React, { useState } from 'react';
import { Card } from '../ui/Card';
import { Table, Thead, Tbody, Th, Td } from '../ui/Table';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { Modal } from '../ui/Modal';
import { UserForm } from './UserForm';
import { formatDateTime } from '../../utils/formatters';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'manager' | 'seller';
  status: 'active' | 'inactive';
  lastLogin?: string;
}

interface UserManagementProps {
  users: User[];
  onCreateUser: (data: Omit<User, 'id'>) => Promise<void>;
  onUpdateUser: (id: string, data: Partial<User>) => Promise<void>;
  onDeleteUser: (id: string) => Promise<void>;
}

export const UserManagement: React.FC<UserManagementProps> = ({
  users,
  onCreateUser,
  onUpdateUser,
  onDeleteUser
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const handleEdit = (user: User) => {
    setSelectedUser(user);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este usuário?')) {
      await onDeleteUser(id);
    }
  };

  const handleSubmit = async (data: any) => {
    if (selectedUser) {
      await onUpdateUser(selectedUser.id, data);
    } else {
      await onCreateUser(data);
    }
    setIsModalOpen(false);
    setSelectedUser(null);
  };

  return (
    <Card>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-medium text-gray-900">
            Gerenciamento de Usuários
          </h3>
          <Button onClick={() => setIsModalOpen(true)}>
            Novo Usuário
          </Button>
        </div>

        <Table>
          <Thead>
            <tr>
              <Th>Nome</Th>
              <Th>E-mail</Th>
              <Th>Função</Th>
              <Th>Status</Th>
              <Th>Último Acesso</Th>
              <Th>Ações</Th>
            </tr>
          </Thead>
          <Tbody>
            {users.map(user => (
              <tr key={user.id}>
                <Td>{user.name}</Td>
                <Td>{user.email}</Td>
                <Td>
                  <Badge
                    variant={user.role === 'admin' ? 'success' : 'default'}
                  >
                    {user.role === 'admin' ? 'Administrador' : 
                     user.role === 'manager' ? 'Gerente' : 'Vendedor'}
                  </Badge>
                </Td>
                <Td>
                  <Badge
                    variant={user.status === 'active' ? 'success' : 'danger'}
                  >
                    {user.status === 'active' ? 'Ativo' : 'Inativo'}
                  </Badge>
                </Td>
                <Td>
                  {user.lastLogin ? formatDateTime(user.lastLogin) : 'Nunca'}
                </Td>
                <Td>
                  <div className="flex space-x-2">
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => handleEdit(user)}
                    >
                      Editar
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(user.id)}
                    >
                      Excluir
                    </Button>
                  </div>
                </Td>
              </tr>
            ))}
          </Tbody>
        </Table>

        <Modal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedUser(null);
          }}
          title={selectedUser ? 'Editar Usuário' : 'Novo Usuário'}
        >
          <UserForm
            initialData={selectedUser}
            onSubmit={handleSubmit}
            onCancel={() => {
              setIsModalOpen(false);
              setSelectedUser(null);
            }}
          />
        </Modal>
      </div>
    </Card>
  );
}; 