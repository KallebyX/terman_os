import React, { useState, useEffect } from 'react';
import { Tab } from '@headlessui/react';
import { CompanyForm } from './components/CompanyForm';
import { UsersTable } from './components/UsersTable';
import { UserForm } from './components/UserForm';
import { Modal } from '../../components/ui';
import { ConfirmDialog } from '../../components/shared/ConfirmDialog';
import { LoadingSpinner } from '../../components/shared/LoadingSpinner';
import { ErrorMessage } from '../../components/shared/ErrorMessage';
import { api } from '../../services/api';

export const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [companyData, setCompanyData] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [showUserForm, setShowUserForm] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const [companyResponse, usersResponse] = await Promise.all([
        api.get('/settings/company'),
        api.get('/settings/users')
      ]);

      setCompanyData(companyResponse.data);
      setUsers(usersResponse.data);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Erro ao carregar configurações');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCompanySubmit = async (data: any) => {
    try {
      await api.put('/settings/company', data);
      setCompanyData(data);
      alert('Dados da empresa atualizados com sucesso!');
    } catch (error: any) {
      alert(error.response?.data?.message || 'Erro ao atualizar dados da empresa');
    }
  };

  const handleUserSubmit = async (data: any) => {
    try {
      if (selectedUser) {
        await api.put(`/settings/users/${selectedUser.id}`, data);
        setUsers(users.map(user =>
          user.id === selectedUser.id ? { ...user, ...data } : user
        ));
      } else {
        const response = await api.post('/settings/users', data);
        setUsers([...users, response.data]);
      }
      setShowUserForm(false);
      setSelectedUser(null);
    } catch (error: any) {
      alert(error.response?.data?.message || 'Erro ao salvar usuário');
    }
  };

  const handleDeleteUser = async () => {
    if (!selectedUser) return;

    try {
      await api.delete(`/settings/users/${selectedUser.id}`);
      setUsers(users.filter(user => user.id !== selectedUser.id));
      setShowDeleteConfirm(false);
      setSelectedUser(null);
    } catch (error: any) {
      alert(error.response?.data?.message || 'Erro ao excluir usuário');
    }
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Configurações</h1>

      <Tab.Group selectedIndex={activeTab} onChange={setActiveTab}>
        <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
          <Tab
            className={({ selected }) =>
              `w-full rounded-lg py-2.5 text-sm font-medium leading-5
              ${selected
                ? 'bg-white text-blue-700 shadow'
                : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
              }`
            }
          >
            Empresa
          </Tab>
          <Tab
            className={({ selected }) =>
              `w-full rounded-lg py-2.5 text-sm font-medium leading-5
              ${selected
                ? 'bg-white text-blue-700 shadow'
                : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
              }`
            }
          >
            Usuários
          </Tab>
        </Tab.List>
        <Tab.Panels>
          <Tab.Panel>
            <div className="bg-white rounded-lg shadow p-6">
              <CompanyForm
                onSubmit={handleCompanySubmit}
                initialValues={companyData}
              />
            </div>
          </Tab.Panel>
          <Tab.Panel>
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b">
                <button
                  onClick={() => {
                    setSelectedUser(null);
                    setShowUserForm(true);
                  }}
                  className="bg-blue-500 text-white px-4 py-2 rounded-lg"
                >
                  Novo Usuário
                </button>
              </div>
              <div className="p-6">
                <UsersTable
                  users={users}
                  onEdit={(user) => {
                    setSelectedUser(user);
                    setShowUserForm(true);
                  }}
                  onDelete={(user) => {
                    setSelectedUser(user);
                    setShowDeleteConfirm(true);
                  }}
                />
              </div>
            </div>
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>

      <Modal
        isOpen={showUserForm}
        onClose={() => {
          setShowUserForm(false);
          setSelectedUser(null);
        }}
        title={selectedUser ? 'Editar Usuário' : 'Novo Usuário'}
      >
        <UserForm
          onSubmit={handleUserSubmit}
          initialValues={selectedUser}
        />
      </Modal>

      <ConfirmDialog
        isOpen={showDeleteConfirm}
        onClose={() => {
          setShowDeleteConfirm(false);
          setSelectedUser(null);
        }}
        onConfirm={handleDeleteUser}
        title="Excluir Usuário"
        message={`Tem certeza que deseja excluir o usuário ${selectedUser?.name}?`}
      />
    </div>
  );
};

export default SettingsPage; 