import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../../components/ui/Table';
import { Badge } from '../../components/ui/Badge';
import { Modal } from '../../components/ui/Modal';
import { DashboardLayout, ContentLayout } from '../../layouts/BaseLayouts';
import { Header, HeaderTitle, HeaderActions } from '../../components/ui/Header';

// Tipos
interface Customer {
  id: string;
  name: string;
  document: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  postalCode: string;
  createdAt: string;
}

const CustomerPage: React.FC = () => {
  // Estados
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentCustomer, setCurrentCustomer] = useState<Partial<Customer> | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  // Dados de exemplo
  const mockCustomers: Customer[] = [
    { 
      id: '1', 
      name: 'João Silva', 
      document: '123.456.789-00', 
      email: 'joao@email.com', 
      phone: '(11) 98765-4321',
      address: 'Rua das Flores, 123',
      city: 'São Paulo',
      state: 'SP',
      postalCode: '01234-567',
      createdAt: '2023-01-15'
    },
    { 
      id: '2', 
      name: 'Maria Oliveira', 
      document: '987.654.321-00', 
      email: 'maria@email.com', 
      phone: '(11) 91234-5678',
      address: 'Av. Paulista, 1000',
      city: 'São Paulo',
      state: 'SP',
      postalCode: '01310-100',
      createdAt: '2023-02-20'
    },
    { 
      id: '3', 
      name: 'Carlos Ferreira', 
      document: '456.789.123-00', 
      email: 'carlos@email.com', 
      phone: '(11) 94567-8912',
      address: 'Rua Augusta, 500',
      city: 'São Paulo',
      state: 'SP',
      postalCode: '01305-000',
      createdAt: '2023-03-10'
    },
  ];

  // Funções
  const openNewCustomerModal = () => {
    setCurrentCustomer({});
    setIsEditing(false);
    setIsModalOpen(true);
  };

  const openEditCustomerModal = (customer: Customer) => {
    setCurrentCustomer(customer);
    setIsEditing(true);
    setIsModalOpen(true);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCurrentCustomer(prev => prev ? { ...prev, [name]: value } : { [name]: value });
  };

  const handleSubmit = () => {
    // Aqui seria a lógica para salvar o cliente
    console.log('Cliente salvo:', currentCustomer);
    setIsModalOpen(false);
    setCurrentCustomer(null);
  };

  const filteredCustomers = mockCustomers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.document.includes(searchTerm) ||
    customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.phone.includes(searchTerm)
  );

  return (
    <DashboardLayout>
      <Header>
        <HeaderTitle>Cadastro de Clientes</HeaderTitle>
        <HeaderActions>
          <Button onClick={openNewCustomerModal}>Novo Cliente</Button>
        </HeaderActions>
      </Header>
      
      <ContentLayout>
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Clientes</CardTitle>
          </CardHeader>
          <CardContent>
            <Input 
              placeholder="Buscar por nome, documento, email ou telefone..." 
              className="mb-4"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nome</TableHead>
                  <TableHead>Documento</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Telefone</TableHead>
                  <TableHead>Cidade/UF</TableHead>
                  <TableHead>Cadastro</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredCustomers.map(customer => (
                  <TableRow key={customer.id}>
                    <TableCell className="font-medium">{customer.name}</TableCell>
                    <TableCell>{customer.document}</TableCell>
                    <TableCell>{customer.email}</TableCell>
                    <TableCell>{customer.phone}</TableCell>
                    <TableCell>{customer.city}/{customer.state}</TableCell>
                    <TableCell>{customer.createdAt}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => openEditCustomerModal(customer)}
                        >
                          Editar
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="sm"
                        >
                          Ver
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
                
                {filteredCustomers.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center py-8 text-text-muted">
                      Nenhum cliente encontrado
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </ContentLayout>

      {/* Modal de Cadastro/Edição */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={isEditing ? "Editar Cliente" : "Novo Cliente"}
        size="lg"
        footer={
          <div className="flex justify-end space-x-3">
            <Button variant="ghost" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSubmit}>
              Salvar
            </Button>
          </div>
        }
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Nome Completo"
            name="name"
            value={currentCustomer?.name || ''}
            onChange={handleInputChange}
          />
          <Input
            label="CPF/CNPJ"
            name="document"
            value={currentCustomer?.document || ''}
            onChange={handleInputChange}
          />
          <Input
            label="Email"
            name="email"
            type="email"
            value={currentCustomer?.email || ''}
            onChange={handleInputChange}
          />
          <Input
            label="Telefone"
            name="phone"
            value={currentCustomer?.phone || ''}
            onChange={handleInputChange}
          />
          <Input
            label="Endereço"
            name="address"
            value={currentCustomer?.address || ''}
            onChange={handleInputChange}
          />
          <Input
            label="Cidade"
            name="city"
            value={currentCustomer?.city || ''}
            onChange={handleInputChange}
          />
          <Input
            label="Estado"
            name="state"
            value={currentCustomer?.state || ''}
            onChange={handleInputChange}
          />
          <Input
            label="CEP"
            name="postalCode"
            value={currentCustomer?.postalCode || ''}
            onChange={handleInputChange}
          />
        </div>
      </Modal>
    </DashboardLayout>
  );
};

export default CustomerPage;