import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';

const ClientDashboard = () => {
  const [activeTab, setActiveTab] = useState('pedidos');
  
  // Dados simulados de pedidos
  const orders = [
    { 
      id: 'PED-2025-001', 
      date: '15/05/2025', 
      status: 'entregue', 
      total: 345.90,
      items: 3,
      tracking: 'BR45678912345'
    },
    { 
      id: 'PED-2025-002', 
      date: '28/04/2025', 
      status: 'em_producao', 
      total: 1250.00,
      items: 5,
      tracking: null
    },
    { 
      id: 'PED-2025-003', 
      date: '10/04/2025', 
      status: 'enviado', 
      total: 789.50,
      items: 2,
      tracking: 'BR98765432109'
    },
    { 
      id: 'PED-2025-004', 
      date: '02/04/2025', 
      status: 'entregue', 
      total: 450.00,
      items: 1,
      tracking: 'BR12345678901'
    },
    { 
      id: 'PED-2025-005', 
      date: '15/03/2025', 
      status: 'entregue', 
      total: 675.30,
      items: 4,
      tracking: 'BR45612378901'
    }
  ];
  
  // Dados simulados do cliente
  const clientData = {
    name: 'João Silva',
    email: 'joao.silva@email.com',
    phone: '(11) 98765-4321',
    address: 'Av. Paulista, 1000, Apto 123',
    city: 'São Paulo',
    state: 'SP',
    zipCode: '01310-100',
    company: 'Indústrias Silva Ltda.',
    since: '10/01/2023',
    totalOrders: 12,
    totalSpent: 'R$ 15.450,00'
  };
  
  // Dados simulados de cotações
  const quotes = [
    {
      id: 'COT-2025-001',
      date: '18/05/2025',
      status: 'pendente',
      items: 2,
      validUntil: '25/05/2025'
    },
    {
      id: 'COT-2025-002',
      date: '05/05/2025',
      status: 'aprovada',
      items: 3,
      validUntil: '12/05/2025'
    },
    {
      id: 'COT-2025-003',
      date: '20/04/2025',
      status: 'expirada',
      items: 1,
      validUntil: '27/04/2025'
    }
  ];
  
  // Função para renderizar o status do pedido
  const renderOrderStatus = (status) => {
    switch(status) {
      case 'pendente':
        return <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium">Pendente</span>;
      case 'em_producao':
        return <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">Em Produção</span>;
      case 'enviado':
        return <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">Enviado</span>;
      case 'entregue':
        return <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">Entregue</span>;
      case 'cancelado':
        return <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">Cancelado</span>;
      case 'aprovada':
        return <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">Aprovada</span>;
      case 'expirada':
        return <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium">Expirada</span>;
      default:
        return <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium">{status}</span>;
    }
  };
  
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
              <p className="text-sm font-medium text-secondary-900">{clientData.name}</p>
              <p className="text-xs text-secondary-500">{clientData.email}</p>
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
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card variant="elevated" className="p-6">
                  <h3 className="text-lg font-medium text-secondary-900 mb-4">Informações Pessoais</h3>
                  
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-secondary-500">Nome Completo</p>
                      <p className="font-medium">{clientData.name}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-secondary-500">E-mail</p>
                      <p className="font-medium">{clientData.email}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-secondary-500">Telefone</p>
                      <p className="font-medium">{clientData.phone}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-secondary-500">Empresa</p>
                      <p className="font-medium">{clientData.company}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-secondary-500">Cliente desde</p>
                      <p className="font-medium">{clientData.since}</p>
                    </div>
                  </div>
                </Card>
                
                <Card variant="elevated" className="p-6">
                  <h3 className="text-lg font-medium text-secondary-900 mb-4">Endereço</h3>
                  
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-secondary-500">Endereço</p>
                      <p className="font-medium">{clientData.address}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-secondary-500">Cidade</p>
                      <p className="font-medium">{clientData.city}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-secondary-500">Estado</p>
                      <p className="font-medium">{clientData.state}</p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-secondary-500">CEP</p>
                      <p className="font-medium">{clientData.zipCode}</p>
                    </div>
                  </div>
                </Card>
                
                <Card variant="elevated" className="p-6 md:col-span-2">
                  <h3 className="text-lg font-medium text-secondary-900 mb-4">Resumo de Atividades</h3>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="bg-secondary-50 p-4 rounded-lg">
                      <p className="text-sm text-secondary-500 mb-1">Total de Pedidos</p>
                      <p className="text-2xl font-bold">{clientData.totalOrders}</p>
                    </div>
                    
                    <div className="bg-secondary-50 p-4 rounded-lg">
                      <p className="text-sm text-secondary-500 mb-1">Valor Total</p>
                      <p className="text-2xl font-bold">{clientData.totalSpent}</p>
                    </div>
                    
                    <div className="bg-secondary-50 p-4 rounded-lg">
                      <p className="text-sm text-secondary-500 mb-1">Último Pedido</p>
                      <p className="text-2xl font-bold">{orders[0]?.date || 'N/A'}</p>
                    </div>
                    
                    <div className="bg-secondary-50 p-4 rounded-lg">
                      <p className="text-sm text-secondary-500 mb-1">Cotações Ativas</p>
                      <p className="text-2xl font-bold">{quotes.filter(q => q.status === 'pendente').length}</p>
                    </div>
                  </div>
                </Card>
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
    </div>
  );
};

export default ClientDashboard;
