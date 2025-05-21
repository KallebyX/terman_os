import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import api from '../../services/api';
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
  
  // Carregar pedidos reais da API
  useEffect(() => {
    const fetchOrders = async () => {
      setIsLoading(true);
      try {
        // Usar endpoint correto com base no papel do usuário
        const endpoint = userRole === 'admin' || userRole === 'staff' 
          ? '/api/orders/orders/' 
          : '/api/orders/my-orders/';
        
        const headers = {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        };
          
        const response = await api.get(endpoint, { headers });
        
        if (response.status !== 200) {
          throw new Error(`Erro na requisição: ${response.status}`);
        }
        
        if (response.data && (response.data.results || Array.isArray(response.data))) {
          setOrders(response.data.results || response.data);
        } else {
          console.error('Formato de resposta inesperado:', response.data);
        }
      } catch (error) {
        console.error('Erro ao carregar pedidos:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchOrders();
  }, [userRole]);
  
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
  const updateOrderStatus = async (orderId: string, newStatus: Order['status']) => {
    try {
      const headers = {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      };
      
      // Chamar a API para atualizar o status
      const response = await api.patch(`/api/orders/orders/${orderId}/`, {
        status: newStatus
      }, { headers });
      
      if (response.status !== 200) {
        throw new Error(`Erro na atualização: ${response.status}`);
      }
      
      // Atualizar o estado local após confirmação da API
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
    } catch (error) {
      console.error('Erro ao atualizar status do pedido:', error);
      alert('Não foi possível atualizar o status do pedido. Por favor, tente novamente.');
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
