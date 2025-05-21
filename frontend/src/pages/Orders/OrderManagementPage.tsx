import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { Badge } from '../../components/ui/Badge';
import { useAuth } from '../../contexts/AuthContext';

// Tipos para pedidos
interface OrderItem {
  id: number;
  productId: number;
  productName: string;
  quantity: number;
  unitPrice: number;
}

interface Order {
  id: string;
  customerId: number;
  customerName: string;
  customerEmail: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  paymentStatus: 'pending' | 'paid' | 'refunded';
  paymentMethod: 'credit_card' | 'pix' | 'bank_transfer' | 'cash';
  createdAt: string;
  updatedAt: string;
  shippingAddress?: string;
  trackingCode?: string;
  notes?: string;
}

const OrderManagementPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const { userRole } = useAuth();
  const navigate = useNavigate();
  
  // Carregar pedidos (simulado)
  useEffect(() => {
    const fetchOrders = async () => {
      setIsLoading(true);
      try {
        // Simulação de carregamento de dados
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Dados simulados de pedidos
        const mockOrders: Order[] = [
          {
            id: 'PED-2025-001',
            customerId: 1,
            customerName: 'Indústria ABC Ltda',
            customerEmail: 'compras@industriaabc.com',
            items: [
              { id: 1, productId: 1, productName: 'Mangueira Hidráulica 1/2"', quantity: 5, unitPrice: 89.90 },
              { id: 2, productId: 4, productName: 'Kit Reparo para Mangueiras', quantity: 2, unitPrice: 120.00 }
            ],
            total: 689.50,
            status: 'delivered',
            paymentStatus: 'paid',
            paymentMethod: 'credit_card',
            createdAt: '2025-05-10T14:30:00Z',
            updatedAt: '2025-05-12T16:45:00Z',
            shippingAddress: 'Av. Industrial, 1000, São Paulo, SP',
            trackingCode: 'BR123456789'
          },
          {
            id: 'PED-2025-002',
            customerId: 2,
            customerName: 'Metalúrgica XYZ',
            customerEmail: 'suprimentos@metalxyz.com',
            items: [
              { id: 3, productId: 2, productName: 'Conexão Rápida 3/4"', quantity: 10, unitPrice: 45.50 },
              { id: 4, productId: 3, productName: 'Adaptador Hidráulico', quantity: 8, unitPrice: 32.75 }
            ],
            total: 717.00,
            status: 'processing',
            paymentStatus: 'paid',
            paymentMethod: 'bank_transfer',
            createdAt: '2025-05-15T09:20:00Z',
            updatedAt: '2025-05-15T14:10:00Z',
            shippingAddress: 'Rua das Indústrias, 500, Belo Horizonte, MG'
          },
          {
            id: 'PED-2025-003',
            customerId: 3,
            customerName: 'Construtora Horizonte',
            customerEmail: 'materiais@construtora-horizonte.com',
            items: [
              { id: 5, productId: 8, productName: 'Mangueira de Alta Temperatura', quantity: 3, unitPrice: 145.50 },
              { id: 6, productId: 7, productName: 'Válvula de Controle', quantity: 2, unitPrice: 195.00 }
            ],
            total: 826.50,
            status: 'shipped',
            paymentStatus: 'paid',
            paymentMethod: 'credit_card',
            createdAt: '2025-05-18T11:45:00Z',
            updatedAt: '2025-05-19T08:30:00Z',
            shippingAddress: 'Av. Construtores, 750, Rio de Janeiro, RJ',
            trackingCode: 'BR987654321'
          },
          {
            id: 'PED-2025-004',
            customerId: 4,
            customerName: 'Fábrica de Móveis Silva',
            customerEmail: 'compras@moveissilva.com',
            items: [
              { id: 7, productId: 5, productName: 'Mangueira Flexível 1"', quantity: 4, unitPrice: 75.30 },
              { id: 8, productId: 6, productName: 'Conexão em T', quantity: 12, unitPrice: 28.90 }
            ],
            total: 647.80,
            status: 'pending',
            paymentStatus: 'pending',
            paymentMethod: 'pix',
            createdAt: '2025-05-20T10:15:00Z',
            updatedAt: '2025-05-20T10:15:00Z',
            shippingAddress: 'Rua dos Marceneiros, 300, Curitiba, PR'
          },
          {
            id: 'PED-2025-005',
            customerId: 5,
            customerName: 'Transportadora Expressa',
            customerEmail: 'manutencao@transportadoraexpressa.com',
            items: [
              { id: 9, productId: 1, productName: 'Mangueira Hidráulica 1/2"', quantity: 8, unitPrice: 89.90 },
              { id: 10, productId: 7, productName: 'Válvula de Controle', quantity: 3, unitPrice: 195.00 }
            ],
            total: 1304.20,
            status: 'cancelled',
            paymentStatus: 'refunded',
            paymentMethod: 'credit_card',
            createdAt: '2025-05-05T16:20:00Z',
            updatedAt: '2025-05-07T09:45:00Z',
            shippingAddress: 'Rodovia BR-101, Km 200, Joinville, SC',
            notes: 'Pedido cancelado a pedido do cliente'
          }
        ];
        
        setOrders(mockOrders);
      } catch (error) {
        console.error('Erro ao carregar pedidos:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchOrders();
  }, []);
  
  // Filtrar pedidos
  const filteredOrders = orders.filter(order => {
    const matchesStatus = filterStatus === 'all' || order.status === filterStatus;
    const matchesSearch = 
      order.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      order.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      order.customerEmail.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesStatus && matchesSearch;
  });
  
  // Atualizar status do pedido
  const updateOrderStatus = (orderId: string, newStatus: Order['status']) => {
    setOrders(prevOrders => 
      prevOrders.map(order => 
        order.id === orderId 
          ? { ...order, status: newStatus, updatedAt: new Date().toISOString() } 
          : order
      )
    );
    
    if (selectedOrder?.id === orderId) {
      setSelectedOrder(prev => prev ? { ...prev, status: newStatus, updatedAt: new Date().toISOString() } : null);
    }
  };
  
  // Renderizar detalhes do pedido
  const renderOrderDetails = () => {
    if (!selectedOrder) return null;
    
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Card variant="elevated" className="mb-6">
          <div className="p-6 border-b border-secondary-200">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-xl font-bold">{selectedOrder.id}</h2>
                <p className="text-secondary-600">
                  {new Date(selectedOrder.createdAt).toLocaleDateString('pt-BR', { 
                    day: '2-digit', 
                    month: '2-digit', 
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
              <div className="flex space-x-2">
                <Badge 
                  variant={
                    selectedOrder.status === 'delivered' ? 'success' :
                    selectedOrder.status === 'shipped' ? 'info' :
                    selectedOrder.status === 'processing' ? 'primary' :
                    selectedOrder.status === 'pending' ? 'warning' :
                    'danger'
                  }
                >
                  {selectedOrder.status === 'delivered' ? 'Entregue' :
                   selectedOrder.status === 'shipped' ? 'Enviado' :
                   selectedOrder.status === 'processing' ? 'Em processamento' :
                   selectedOrder.status === 'pending' ? 'Pendente' :
                   'Cancelado'}
                </Badge>
                <Badge 
                  variant={
                    selectedOrder.paymentStatus === 'paid' ? 'success' :
                    selectedOrder.paymentStatus === 'pending' ? 'warning' :
                    'danger'
                  }
                >
                  {selectedOrder.paymentStatus === 'paid' ? 'Pago' :
                   selectedOrder.paymentStatus === 'pending' ? 'Pagamento pendente' :
                   'Reembolsado'}
                </Badge>
              </div>
            </div>
          </div>
          
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-2">Informações do Cliente</h3>
              <p><span className="text-secondary-600">Nome:</span> {selectedOrder.customerName}</p>
              <p><span className="text-secondary-600">Email:</span> {selectedOrder.customerEmail}</p>
              {selectedOrder.shippingAddress && (
                <p><span className="text-secondary-600">Endereço:</span> {selectedOrder.shippingAddress}</p>
              )}
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Informações do Pedido</h3>
              <p>
                <span className="text-secondary-600">Método de Pagamento:</span> 
                {selectedOrder.paymentMethod === 'credit_card' ? 'Cartão de Crédito' :
                 selectedOrder.paymentMethod === 'pix' ? 'PIX' :
                 selectedOrder.paymentMethod === 'bank_transfer' ? 'Transferência Bancária' :
                 'Dinheiro'}
              </p>
              {selectedOrder.trackingCode && (
                <p><span className="text-secondary-600">Código de Rastreio:</span> {selectedOrder.trackingCode}</p>
              )}
              <p>
                <span className="text-secondary-600">Última Atualização:</span> 
                {new Date(selectedOrder.updatedAt).toLocaleDateString('pt-BR', { 
                  day: '2-digit', 
                  month: '2-digit', 
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          </div>
          
          <div className="p-6 border-t border-secondary-200">
            <h3 className="font-semibold mb-4">Itens do Pedido</h3>
            <div className="overflow-x-auto">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell isHeader>Produto</TableCell>
                    <TableCell isHeader>Quantidade</TableCell>
                    <TableCell isHeader>Preço Unitário</TableCell>
                    <TableCell isHeader>Subtotal</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {selectedOrder.items.map(item => (
                    <TableRow key={item.id}>
                      <TableCell>{item.productName}</TableCell>
                      <TableCell>{item.quantity}</TableCell>
                      <TableCell>R$ {item.unitPrice.toFixed(2)}</TableCell>
                      <TableCell>R$ {(item.quantity * item.unitPrice).toFixed(2)}</TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell colSpan={3} className="text-right font-bold">Total</TableCell>
                    <TableCell className="font-bold">R$ {selectedOrder.total.toFixed(2)}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
          </div>
          
          {selectedOrder.notes && (
            <div className="p-6 border-t border-secondary-200">
              <h3 className="font-semibold mb-2">Observações</h3>
              <p className="text-secondary-700">{selectedOrder.notes}</p>
            </div>
          )}
          
          {userRole === 'admin' || userRole === 'staff' ? (
            <div className="p-6 border-t border-secondary-200 bg-secondary-50">
              <h3 className="font-semibold mb-4">Ações</h3>
              <div className="flex flex-wrap gap-3">
                {selectedOrder.status === 'pending' && (
                  <Button 
                    variant="primary"
                    onClick={() => updateOrderStatus(selectedOrder.id, 'processing')}
                  >
                    Iniciar Processamento
                  </Button>
                )}
                
                {selectedOrder.status === 'processing' && (
                  <Button 
                    variant="primary"
                    onClick={() => updateOrderStatus(selectedOrder.id, 'shipped')}
                  >
                    Marcar como Enviado
                  </Button>
                )}
                
                {selectedOrder.status === 'shipped' && (
                  <Button 
                    variant="success"
                    onClick={() => updateOrderStatus(selectedOrder.id, 'delivered')}
                  >
                    Confirmar Entrega
                  </Button>
                )}
                
                {(selectedOrder.status === 'pending' || selectedOrder.status === 'processing') && (
                  <Button 
                    variant="danger"
                    onClick={() => updateOrderStatus(selectedOrder.id, 'cancelled')}
                  >
                    Cancelar Pedido
                  </Button>
                )}
                
                <Button 
                  variant="outline"
                  onClick={() => navigate(`/admin/orders/print/${selectedOrder.id}`)}
                >
                  Imprimir Pedido
                </Button>
              </div>
            </div>
          ) : null}
        </Card>
        
        <div className="mb-6">
          <Button
            variant="text"
            onClick={() => setSelectedOrder(null)}
          >
            <i className="fas fa-arrow-left mr-2"></i>
            Voltar para lista de pedidos
          </Button>
        </div>
      </motion.div>
    );
  };
  
  // Renderizar lista de pedidos
  const renderOrdersList = () => {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Card variant="elevated" className="overflow-hidden">
          <div className="p-6 border-b border-secondary-200">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <h2 className="text-xl font-bold">Pedidos</h2>
              
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Buscar pedidos..."
                    className="pl-10 pr-4 py-2 border border-secondary-300 rounded-md focus:ring-primary-500 focus:border-primary-500 w-full"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i className="fas fa-search text-secondary-400"></i>
                  </div>
                </div>
                
                <select
                  className="px-4 py-2 border border-secondary-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                >
                  <option value="all">Todos os Status</option>
                  <option value="pending">Pendentes</option>
                  <option value="processing">Em Processamento</option>
                  <option value="shipped">Enviados</option>
                  <option value="delivered">Entregues</option>
                  <option value="cancelled">Cancelados</option>
                </select>
              </div>
            </div>
          </div>
          
          {isLoading ? (
            <div className="p-8 text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-primary-500 border-t-transparent"></div>
              <p className="mt-2 text-secondary-600">Carregando pedidos...</p>
            </div>
          ) : filteredOrders.length === 0 ? (
            <div className="p-8 text-center">
              <div className="text-secondary-400 text-5xl mb-4">
                <i className="fas fa-box-open"></i>
              </div>
              <h3 className="text-xl font-medium text-secondary-700 mb-2">Nenhum pedido encontrado</h3>
              <p className="text-secondary-500 mb-4">
                Não há pedidos correspondentes aos filtros aplicados.
              </p>
              <Button 
                variant="primary"
                onClick={() => {
                  setFilterStatus('all');
                  setSearchTerm('');
                }}
              >
                Limpar Filtros
              </Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell isHeader>ID</TableCell>
                    <TableCell isHeader>Cliente</TableCell>
                    <TableCell isHeader>Data</TableCell>
                    <TableCell isHeader>Total</TableCell>
                    <TableCell isHeader>Status</TableCell>
                    <TableCell isHeader>Pagamento</TableCell>
                    <TableCell isHeader>Ações</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredOrders.map(order => (
                    <TableRow key={order.id}>
                      <TableCell>{order.id}</TableCell>
                      <TableCell>{order.customerName}</TableCell>
                      <TableCell>
                        {new Date(order.createdAt).toLocaleDateString('pt-BR')}
                      </TableCell>
                      <TableCell>R$ {order.total.toFixed(2)}</TableCell>
                      <TableCell>
                        <Badge 
                          variant={
                            order.status === 'delivered' ? 'success' :
                            order.status === 'shipped' ? 'info' :
                            order.status === 'processing' ? 'primary' :
                            order.status === 'pending' ? 'warning' :
                            'danger'
                          }
                        >
                          {order.status === 'delivered' ? 'Entregue' :
                           order.status === 'shipped' ? 'Enviado' :
                           order.status === 'processing' ? 'Em processamento' :
                           order.status === 'pending' ? 'Pendente' :
                           'Cancelado'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge 
                          variant={
                            order.paymentStatus === 'paid' ? 'success' :
                            order.paymentStatus === 'pending' ? 'warning' :
                            'danger'
                          }
                        >
                          {order.paymentStatus === 'paid' ? 'Pago' :
                           order.paymentStatus === 'pending' ? 'Pendente' :
                           'Reembolsado'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="text"
                          size="sm"
                          onClick={() => setSelectedOrder(order)}
                        >
                          <i className="fas fa-eye mr-1"></i>
                          Detalhes
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </Card>
      </motion.div>
    );
  };
  
  return (
    <div className="p-6">
      {selectedOrder ? renderOrderDetails() : renderOrdersList()}
    </div>
  );
};

export default OrderManagementPage;
