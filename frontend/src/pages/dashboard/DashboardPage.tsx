import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { useAuth } from '../../contexts/AuthContext';

// Componente para gráficos
const Chart = ({ type, data, options }) => {
  // Em produção, isso usaria react-chartjs-2
  return (
    <div className="w-full h-64 bg-secondary-50 rounded-lg border border-secondary-200 flex items-center justify-center">
      <div className="text-center">
        <div className="text-secondary-400 text-4xl mb-2">
          <i className={`fas fa-${type === 'bar' ? 'chart-bar' : type === 'line' ? 'chart-line' : 'chart-pie'}`}></i>
        </div>
        <p className="text-secondary-600 font-medium">{options.title || 'Gráfico'}</p>
        <p className="text-secondary-500 text-sm">Dados simulados para demonstração</p>
      </div>
    </div>
  );
};

const DashboardPage: React.FC = () => {
  // Contexto de autenticação
  const { userName } = useAuth();
  
  // Estados
  const [dateRange, setDateRange] = useState('month');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Estados para dados reais
  const [kpiData, setKpiData] = useState<any>(null);
  const [recentOrders, setRecentOrders] = useState<any[]>([]);
  const [topProducts, setTopProducts] = useState<any[]>([]);
  const [lowStockAlerts, setLowStockAlerts] = useState<any[]>([]);
  const [activities, setActivities] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // Buscar todos os dados em paralelo para melhor performance
        const [kpiResponse, ordersResponse, productsResponse, stockAlertsResponse, activitiesResponse] = 
          await Promise.all([
            api.get(`/dashboard/kpis?range=${dateRange}`),
            api.get('/orders/recent'),
            api.get(`/products/top?range=${dateRange}`),
            api.get('/inventory/low-stock'),
            api.get('/activities/recent')
          ]);
        
        setKpiData(kpiResponse.data);
        setRecentOrders(ordersResponse.data);
        setTopProducts(productsResponse.data);
        setLowStockAlerts(stockAlertsResponse.data);
        setActivities(activitiesResponse.data);
      } catch (error: any) {
        console.error('Erro ao buscar dados do dashboard:', error);
        setError(
          error.response?.data?.message || 
          'Não foi possível carregar os dados do dashboard. Por favor, tente novamente mais tarde.'
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [dateRange]); // Refazer a busca quando o intervalo de datas mudar
  
  // Função para atualizar os dados
  const refreshData = () => {
    // Refaz a busca de dados
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const [kpiResponse, ordersResponse, productsResponse, stockAlertsResponse, activitiesResponse] = 
          await Promise.all([
            api.get(`/dashboard/kpis?range=${dateRange}`),
            api.get('/orders/recent'),
            api.get(`/products/top?range=${dateRange}`),
            api.get('/inventory/low-stock'),
            api.get('/activities/recent')
          ]);
        
        setKpiData(kpiResponse.data);
        setRecentOrders(ordersResponse.data);
        setTopProducts(productsResponse.data);
        setLowStockAlerts(stockAlertsResponse.data);
        setActivities(activitiesResponse.data);
      } catch (error: any) {
        console.error('Erro ao atualizar dados do dashboard:', error);
        setError(
          error.response?.data?.message || 
          'Não foi possível atualizar os dados. Por favor, tente novamente mais tarde.'
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  };

  // Renderizar KPI cards
  const renderKpiCards = () => {
    if (!kpiData) return null;
    
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card variant="elevated" className="p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-secondary-500 text-sm mb-1">Vendas</p>
              <h3 className="text-2xl font-bold mb-1">{kpiData.sales?.value || 'N/A'}</h3>
              {kpiData.sales && (
                <p className={`text-sm ${kpiData.sales.positive ? 'text-green-500' : 'text-red-500'}`}>
                  <i className={`fas fa-arrow-${kpiData.sales.positive ? 'up' : 'down'} mr-1`}></i>
                  {kpiData.sales.change} {dateRange === 'week' ? 'esta semana' : dateRange === 'month' ? 'este mês' : 'este ano'}
                </p>
              )}
            </div>
            <div className="bg-primary-100 p-3 rounded-full text-primary-600">
              <i className="fas fa-shopping-cart text-xl"></i>
            </div>
          </div>
        </Card>
        
        <Card variant="elevated" className="p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-secondary-500 text-sm mb-1">Pedidos</p>
              <h3 className="text-2xl font-bold mb-1">{kpiData.orders?.value || 'N/A'}</h3>
              {kpiData.orders && (
                <p className={`text-sm ${kpiData.orders.positive ? 'text-green-500' : 'text-red-500'}`}>
                  <i className={`fas fa-arrow-${kpiData.orders.positive ? 'up' : 'down'} mr-1`}></i>
                  {kpiData.orders.change} {dateRange === 'week' ? 'esta semana' : dateRange === 'month' ? 'este mês' : 'este ano'}
                </p>
              )}
            </div>
            <div className="bg-blue-100 p-3 rounded-full text-blue-600">
              <i className="fas fa-file-invoice text-xl"></i>
            </div>
          </div>
        </Card>
        
        <Card variant="elevated" className="p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-secondary-500 text-sm mb-1">Clientes</p>
              <h3 className="text-2xl font-bold mb-1">{kpiData.customers?.value || 'N/A'}</h3>
              {kpiData.customers && (
                <p className={`text-sm ${kpiData.customers.positive ? 'text-green-500' : 'text-red-500'}`}>
                  <i className={`fas fa-arrow-${kpiData.customers.positive ? 'up' : 'down'} mr-1`}></i>
                  {kpiData.customers.change} {dateRange === 'week' ? 'esta semana' : dateRange === 'month' ? 'este mês' : 'este ano'}
                </p>
              )}
            </div>
            <div className="bg-purple-100 p-3 rounded-full text-purple-600">
              <i className="fas fa-users text-xl"></i>
            </div>
          </div>
        </Card>
        
        <Card variant="elevated" className="p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-secondary-500 text-sm mb-1">Ticket Médio</p>
              <h3 className="text-2xl font-bold mb-1">{kpiData.averageTicket?.value || 'N/A'}</h3>
              {kpiData.averageTicket && (
                <p className={`text-sm ${kpiData.averageTicket.positive ? 'text-green-500' : 'text-red-500'}`}>
                  <i className={`fas fa-arrow-${kpiData.averageTicket.positive ? 'up' : 'down'} mr-1`}></i>
                  {kpiData.averageTicket.change} {dateRange === 'week' ? 'esta semana' : dateRange === 'month' ? 'este mês' : 'este ano'}
                </p>
              )}
            </div>
            <div className="bg-green-100 p-3 rounded-full text-green-600">
              <i className="fas fa-receipt text-xl"></i>
            </div>
          </div>
        </Card>
      </div>
    );
  };
  
  return (
    <div className="p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold mb-1">Dashboard</h1>
            <p className="text-secondary-500">Bem-vindo de volta, {userName || 'Usuário'}</p>
          </div>
          
          <div className="mt-4 md:mt-0 flex flex-wrap gap-3">
            <div className="flex border border-secondary-300 rounded-md overflow-hidden">
              <button
                className={`px-3 py-1.5 ${dateRange === 'week' ? 'bg-primary-500 text-white' : 'bg-white text-secondary-700 hover:bg-secondary-50'}`}
                onClick={() => setDateRange('week')}
              >
                Semana
              </button>
              <button
                className={`px-3 py-1.5 ${dateRange === 'month' ? 'bg-primary-500 text-white' : 'bg-white text-secondary-700 hover:bg-secondary-50'}`}
                onClick={() => setDateRange('month')}
              >
                Mês
              </button>
              <button
                className={`px-3 py-1.5 ${dateRange === 'year' ? 'bg-primary-500 text-white' : 'bg-white text-secondary-700 hover:bg-secondary-50'}`}
                onClick={() => setDateRange('year')}
              >
                Ano
              </button>
            </div>
            
            <Button variant="outline">
              <i className="fas fa-file-export mr-2"></i>
              Exportar
            </Button>
            
            <Button 
              variant="primary" 
              onClick={refreshData}
              disabled={isLoading}
            >
              <i className={`fas ${isLoading ? 'fa-spinner fa-spin' : 'fa-sync-alt'} mr-2`}></i>
              {isLoading ? 'Atualizando...' : 'Atualizar'}
            </Button>
          </div>
        </div>
        
        {/* Mensagem de erro */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6 flex items-center">
            <i className="fas fa-exclamation-circle mr-2"></i>
            <span>{error}</span>
          </div>
        )}
        
        {/* Estado de carregamento */}
        {isLoading && !kpiData ? (
          <div className="flex justify-center items-center py-12">
            <div className="text-center">
              <i className="fas fa-spinner fa-spin text-primary-500 text-3xl mb-4"></i>
              <p className="text-secondary-500">Carregando dados do dashboard...</p>
            </div>
          </div>
        ) : (
          <>
            {/* KPI Cards */}
            {renderKpiCards()}
          </>
        )}
        
        {!isLoading && (
          <>
            {/* Gráficos */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card variant="elevated" className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-semibold">Vendas por Período</h3>
                  <div className="text-secondary-500 text-sm">
                    <i className="fas fa-calendar-alt mr-1"></i>
                    {dateRange === 'week' ? 'Últimos 7 dias' : dateRange === 'month' ? 'Últimos 30 dias' : 'Este ano'}
                  </div>
                </div>
                <Chart 
                  type="line" 
                  data={kpiData?.salesChart || {}} 
                  options={{ 
                    title: 'Vendas por Período',
                    xAxis: 'Período',
                    yAxis: 'Valor (R$)'
                  }} 
                />
              </Card>
              
              <Card variant="elevated" className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-semibold">Vendas por Categoria</h3>
                  <div className="text-secondary-500 text-sm">
                    <i className="fas fa-calendar-alt mr-1"></i>
                    {dateRange === 'week' ? 'Últimos 7 dias' : dateRange === 'month' ? 'Últimos 30 dias' : 'Este ano'}
                  </div>
                </div>
                <Chart 
                  type="pie" 
                  data={kpiData?.categoriesChart || {}} 
                  options={{ 
                    title: 'Vendas por Categoria',
                    legend: true
                  }} 
                />
              </Card>
            </div>
          </>
        )}
        
        {!isLoading && (
          <>
            {/* Pedidos Recentes e Produtos Mais Vendidos */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card variant="elevated" className="overflow-hidden">
                <div className="p-6 border-b border-secondary-200">
                  <div className="flex justify-between items-center">
                    <h3 className="font-semibold">Pedidos Recentes</h3>
                    <Button variant="text" size="sm">
                      Ver Todos
                    </Button>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  {recentOrders.length > 0 ? (
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell isHeader>ID</TableCell>
                          <TableCell isHeader>Cliente</TableCell>
                          <TableCell isHeader>Data</TableCell>
                          <TableCell isHeader>Valor</TableCell>
                          <TableCell isHeader>Status</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {recentOrders.map(order => (
                          <TableRow key={order.id}>
                            <TableCell>{order.id}</TableCell>
                            <TableCell>{order.customer}</TableCell>
                            <TableCell>{order.date}</TableCell>
                            <TableCell>{order.value}</TableCell>
                            <TableCell>
                              <Badge 
                                variant={
                                  order.status === 'completed' ? 'success' :
                                  order.status === 'processing' ? 'info' :
                                  order.status === 'pending' ? 'warning' : 'secondary'
                                }
                              >
                                {order.status === 'completed' ? 'Concluído' :
                                 order.status === 'processing' ? 'Em Processo' :
                                 order.status === 'pending' ? 'Pendente' : order.status}
                              </Badge>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  ) : (
                    <div className="p-6 text-center text-secondary-500">
                      Nenhum pedido recente encontrado.
                    </div>
                  )}
                </div>
              </Card>
          
              <Card variant="elevated" className="overflow-hidden">
                <div className="p-6 border-b border-secondary-200">
                  <div className="flex justify-between items-center">
                    <h3 className="font-semibold">Produtos Mais Vendidos</h3>
                    <Button variant="text" size="sm">
                      Ver Todos
                    </Button>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  {topProducts.length > 0 ? (
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell isHeader>Produto</TableCell>
                          <TableCell isHeader>Vendas</TableCell>
                          <TableCell isHeader>Receita</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {topProducts.map((product, index) => (
                          <TableRow key={product.id || index}>
                            <TableCell>{product.name}</TableCell>
                            <TableCell>{product.sales} un</TableCell>
                            <TableCell>{product.revenue}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  ) : (
                    <div className="p-6 text-center text-secondary-500">
                      Nenhum produto encontrado.
                    </div>
                  )}
                </div>
              </Card>
            </div>
          </>
        )}
        
        {/* Alertas de Estoque Baixo */}
        {!isLoading && lowStockAlerts.length > 0 && (
          <Card variant="bordered" className="mb-8 p-6 bg-yellow-50 border-yellow-200">
            <div className="flex items-start">
              <div className="text-yellow-500 mr-4">
                <i className="fas fa-exclamation-triangle text-2xl"></i>
              </div>
              <div className="flex-grow">
                <h3 className="font-semibold text-yellow-800 mb-2">Alerta de Estoque Baixo</h3>
                <p className="text-yellow-700 mb-4">
                  Os seguintes produtos estão com estoque abaixo do mínimo recomendado.
                </p>
                
                <div className="bg-white rounded-lg overflow-hidden border border-yellow-200">
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell isHeader>Produto</TableCell>
                        <TableCell isHeader>Estoque Atual</TableCell>
                        <TableCell isHeader>Estoque Mínimo</TableCell>
                        <TableCell isHeader>Ação</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {lowStockAlerts.map((item, index) => (
                        <TableRow key={index}>
                          <TableCell>{item.name}</TableCell>
                          <TableCell className="text-red-600 font-medium">{item.stock}</TableCell>
                          <TableCell>{item.minStock}</TableCell>
                          <TableCell>
                            <Button variant="outline" size="sm">
                              Repor
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            </div>
          </Card>
        )}
        
        {/* Atividades Recentes */}
        {!isLoading && (
          <Card variant="elevated" className="mb-8">
            <div className="p-6 border-b border-secondary-200">
              <div className="flex justify-between items-center">
                <h3 className="font-semibold">Atividades Recentes</h3>
                <Button variant="text" size="sm">
                  Ver Todas
                </Button>
              </div>
            </div>
            <div className="p-6">
              {activities.length > 0 ? (
                <div className="relative">
                  <div className="absolute top-0 bottom-0 left-4 w-0.5 bg-secondary-200"></div>
                  
                  {activities.map((activity, index) => (
                    <div key={activity.id || index} className={`relative pl-12 ${index < activities.length - 1 ? 'pb-8' : ''}`}>
                      <div className={`absolute left-0 top-1 w-8 h-8 rounded-full 
                        ${activity.type === 'order_created' ? 'bg-blue-100 text-blue-500' : 
                          activity.type === 'order_completed' ? 'bg-green-100 text-green-500' : 
                          activity.type === 'new_customer' ? 'bg-purple-100 text-purple-500' : 
                          activity.type === 'stock_alert' ? 'bg-yellow-100 text-yellow-500' : 
                          'bg-secondary-100 text-secondary-500'} 
                        flex items-center justify-center`}>
                        <i className={`fas 
                          ${activity.type === 'order_created' ? 'fa-file-invoice' : 
                            activity.type === 'order_completed' ? 'fa-check' : 
                            activity.type === 'new_customer' ? 'fa-user' : 
                            activity.type === 'stock_alert' ? 'fa-exclamation-triangle' : 
                            'fa-bell'}`}></i>
                      </div>
                      <div>
                        <p className="font-medium">{activity.title}</p>
                        <p className="text-sm text-secondary-500">{activity.description}</p>
                        <p className="text-xs text-secondary-400 mt-1">{activity.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center text-secondary-500 py-4">
                  Nenhuma atividade recente encontrada.
                </div>
              )}
            </div>
          </Card>
        )}
      </motion.div>
    </div>
  );
};

export default DashboardPage;
