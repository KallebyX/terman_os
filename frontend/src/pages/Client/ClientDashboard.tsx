import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { Modal } from '../../components/ui';
import { OrderHistory } from './components/OrderHistory';
import { ProfileCard } from './components/ProfileCard';
import { AddressCard } from './components/AddressCard';
import { AddressForm } from './components/AddressForm';
import { ProfileForm } from './components/ProfileForm';
import { ConfirmDialog } from '../../components/shared/ConfirmDialog';
import { LoadingSpinner } from '../../components/shared/LoadingSpinner';
import { ErrorMessage } from '../../components/shared/ErrorMessage';
import { useAuth } from '../../hooks/useAuth';
import { useOrders } from '../../hooks/useOrders';
import { useAddresses } from '../../hooks/useAddresses';
import { Address, Order } from '../../types';

const ClientDashboard = () => {
  const { user, updateUser } = useAuth();
  const { orders, isLoading: ordersLoading } = useOrders();
  const {
    addresses,
    isLoading: addressesLoading,
    createAddress,
    updateAddress,
    deleteAddress
  } = useAddresses();

  const [activeTab, setActiveTab] = useState('pedidos');
  const [showProfileForm, setShowProfileForm] = useState(false);
  const [showAddressForm, setShowAddressForm] = useState(false);
  const [selectedAddress, setSelectedAddress] = useState<Address | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  const handleProfileUpdate = async (data: any) => {
    try {
      await updateUser(data);
      setShowProfileForm(false);
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleAddressSubmit = async (data: any) => {
    try {
      if (selectedAddress) {
        await updateAddress(selectedAddress.id, data);
      } else {
        await createAddress(data);
      }
      setShowAddressForm(false);
      setSelectedAddress(null);
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleDeleteAddress = async () => {
    if (!selectedAddress) return;

    try {
      await deleteAddress(selectedAddress.id);
      setShowDeleteConfirm(false);
      setSelectedAddress(null);
    } catch (error: any) {
      alert(error.message);
    }
  };

  if (ordersLoading || addressesLoading) return <LoadingSpinner />;

  return (
    <div className="min-h-screen bg-background-lightGray">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <Link to="/">
              <img 
                src="/logo.png" 
                alt="Mangueiras Terman" 
                className="h-10 mr-4"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = 'https://via.placeholder.com/160x40?text=Mangueiras+Terman';
                }}
              />
            </Link>
            <h1 className="text-xl font-semibold text-secondary-900">Área do Cliente</h1>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm font-medium text-secondary-900">{user?.name}</p>
              <p className="text-xs text-secondary-500">{user?.email}</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              as={Link}
              to="/logout"
            >
              Sair
            </Button>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Tabs */}
          <div className="border-b border-secondary-200 mb-6">
            <nav className="-mb-px flex space-x-8">
              <button
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'pedidos'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-secondary-300'
                }`}
                onClick={() => setActiveTab('pedidos')}
              >
                Meus Pedidos
              </button>
              <button
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'cotacoes'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-secondary-300'
                }`}
                onClick={() => setActiveTab('cotacoes')}
              >
                Cotações
              </button>
              <button
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'dados'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-secondary-300'
                }`}
                onClick={() => setActiveTab('dados')}
              >
                Meus Dados
              </button>
            </nav>
          </div>
          
          {/* Tab Content */}
          {activeTab === 'pedidos' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-secondary-900">Meus Pedidos</h2>
                <Button
                  variant="primary"
                  size="sm"
                  as={Link}
                  to="/marketplace"
                >
                  Fazer Novo Pedido
                </Button>
              </div>
              
              {orders.length > 0 ? (
                <Card variant="elevated" className="overflow-hidden">
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell isHeader>Pedido</TableCell>
                          <TableCell isHeader>Data</TableCell>
                          <TableCell isHeader>Status</TableCell>
                          <TableCell isHeader>Itens</TableCell>
                          <TableCell isHeader>Total</TableCell>
                          <TableCell isHeader>Ações</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {orders.map(order => (
                          <TableRow key={order.id}>
                            <TableCell>{order.id}</TableCell>
                            <TableCell>{order.date}</TableCell>
                            <TableCell>{renderOrderStatus(order.status)}</TableCell>
                            <TableCell>{order.items}</TableCell>
                            <TableCell>R$ {order.total.toFixed(2)}</TableCell>
                            <TableCell>
                              <div className="flex space-x-2">
                                <Button
                                  variant="text"
                                  size="sm"
                                  as={Link}
                                  to={`/client/pedidos/${order.id}`}
                                >
                                  Detalhes
                                </Button>
                                {order.tracking && (
                                  <Button
                                    variant="text"
                                    size="sm"
                                    as="a"
                                    href="#"
                                    onClick={(e) => {
                                      e.preventDefault();
                                      alert(`Rastreamento: ${order.tracking}`);
                                    }}
                                  >
                                    Rastrear
                                  </Button>
                                )}
                              </div>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </Card>
              ) : (
                <div className="text-center py-12 bg-white rounded-lg shadow-sm">
                  <div className="text-secondary-400 text-5xl mb-4">
                    <i className="fas fa-shopping-bag"></i>
                  </div>
                  <h3 className="text-xl font-medium mb-2">Nenhum pedido encontrado</h3>
                  <p className="text-secondary-500 mb-6">Você ainda não realizou nenhum pedido</p>
                  <Button
                    variant="primary"
                    as={Link}
                    to="/marketplace"
                  >
                    Fazer Primeiro Pedido
                  </Button>
                </div>
              )}
            </div>
          )}
          
          {activeTab === 'cotacoes' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-secondary-900">Minhas Cotações</h2>
                <Button
                  variant="primary"
                  size="sm"
                  as={Link}
                  to="/client/solicitar-cotacao"
                >
                  Solicitar Cotação
                </Button>
              </div>
              
              {quotes.length > 0 ? (
                <Card variant="elevated" className="overflow-hidden">
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell isHeader>Cotação</TableCell>
                          <TableCell isHeader>Data</TableCell>
                          <TableCell isHeader>Status</TableCell>
                          <TableCell isHeader>Itens</TableCell>
                          <TableCell isHeader>Válida até</TableCell>
                          <TableCell isHeader>Ações</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {quotes.map(quote => (
                          <TableRow key={quote.id}>
                            <TableCell>{quote.id}</TableCell>
                            <TableCell>{quote.date}</TableCell>
                            <TableCell>{renderOrderStatus(quote.status)}</TableCell>
                            <TableCell>{quote.items}</TableCell>
                            <TableCell>{quote.validUntil}</TableCell>
                            <TableCell>
                              <div className="flex space-x-2">
                                <Button
                                  variant="text"
                                  size="sm"
                                  as={Link}
                                  to={`/client/cotacoes/${quote.id}`}
                                >
                                  Detalhes
                                </Button>
                                {quote.status === 'pendente' && (
                                  <Button
                                    variant="text"
                                    size="sm"
                                    as="a"
                                    href="#"
                                    onClick={(e) => {
                                      e.preventDefault();
                                      alert(`Cotação aprovada: ${quote.id}`);
                                    }}
                                  >
                                    Aprovar
                                  </Button>
                                )}
                              </div>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </Card>
              ) : (
                <div className="text-center py-12 bg-white rounded-lg shadow-sm">
                  <div className="text-secondary-400 text-5xl mb-4">
                    <i className="fas fa-file-invoice-dollar"></i>
                  </div>
                  <h3 className="text-xl font-medium mb-2">Nenhuma cotação encontrada</h3>
                  <p className="text-secondary-500 mb-6">Você ainda não solicitou nenhuma cotação</p>
                  <Button
                    variant="primary"
                    as={Link}
                    to="/client/solicitar-cotacao"
                  >
                    Solicitar Cotação
                  </Button>
                </div>
              )}
            </div>
          )}
          
          {activeTab === 'dados' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-secondary-900">Meus Dados</h2>
                <Button
                  variant="outline"
                  size="sm"
                >
                  Editar Dados
                </Button>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ProfileCard
                  user={user!}
                  onEdit={() => setShowProfileForm(true)}
                />

                <AddressCard
                  addresses={addresses}
                  onAddAddress={() => {
                    setSelectedAddress(null);
                    setShowAddressForm(true);
                  }}
                  onEditAddress={(address) => {
                    setSelectedAddress(address);
                    setShowAddressForm(true);
                  }}
                  onDeleteAddress={(address) => {
                    setSelectedAddress(address);
                    setShowDeleteConfirm(true);
                  }}
                />
              </div>
            </div>
          )}
        </motion.div>
      </main>
      
      {/* Footer */}
      <footer className="bg-white border-t border-secondary-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <img 
                src="/logo.png" 
                alt="Mangueiras Terman" 
                className="h-8"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = 'https://via.placeholder.com/120x32?text=Mangueiras+Terman';
                }}
              />
            </div>
            <div className="flex space-x-6">
              <Link to="/termos" className="text-sm text-secondary-500 hover:text-secondary-900">
                Termos de Uso
              </Link>
              <Link to="/privacidade" className="text-sm text-secondary-500 hover:text-secondary-900">
                Política de Privacidade
              </Link>
              <Link to="/contato" className="text-sm text-secondary-500 hover:text-secondary-900">
                Contato
              </Link>
            </div>
            <div className="mt-4 md:mt-0 text-sm text-secondary-500">
              &copy; 2025 Mangueiras Terman. Todos os direitos reservados.
            </div>
          </div>
        </div>
      </footer>

      <Modal
        isOpen={showProfileForm}
        onClose={() => setShowProfileForm(false)}
        title="Editar Perfil"
      >
        <ProfileForm
          onSubmit={handleProfileUpdate}
          initialValues={user!}
        />
      </Modal>

      <Modal
        isOpen={showAddressForm}
        onClose={() => {
          setShowAddressForm(false);
          setSelectedAddress(null);
        }}
        title={selectedAddress ? 'Editar Endereço' : 'Novo Endereço'}
      >
        <AddressForm
          onSubmit={handleAddressSubmit}
          initialValues={selectedAddress || undefined}
        />
      </Modal>

      <ConfirmDialog
        isOpen={showDeleteConfirm}
        onClose={() => {
          setShowDeleteConfirm(false);
          setSelectedAddress(null);
        }}
        onConfirm={handleDeleteAddress}
        title="Excluir Endereço"
        message="Tem certeza que deseja excluir este endereço?"
      />

      <Modal
        isOpen={!!selectedOrder}
        onClose={() => setSelectedOrder(null)}
        title={`Pedido #${selectedOrder?.id}`}
      >
        {selectedOrder && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-gray-500">Status</h3>
              <p className="mt-1">{selectedOrder.status}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Itens</h3>
              <ul className="mt-2 divide-y">
                {selectedOrder.items.map((item, index) => (
                  <li key={index} className="py-2">
                    <div className="flex justify-between">
                      <span>{item.product.name}</span>
                      <span>
                        {item.quantity}x {formatCurrency(item.price)}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            <div className="border-t pt-4">
              <div className="flex justify-between font-medium">
                <span>Total</span>
                <span>{formatCurrency(selectedOrder.total)}</span>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default ClientDashboard;
