import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';

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
  // Estados
  const [dateRange, setDateRange] = useState('month');
  
  // Dados simulados
  const kpiData = {
    sales: {
      value: 'R$ 45.789,00',
      change: '+12,5%',
      positive: true
    },
    orders: {
      value: '128',
      change: '+8,2%',
      positive: true
    },
    customers: {
      value: '32',
      change: '+15,7%',
      positive: true
    },
    averageTicket: {
      value: 'R$ 357,73',
      change: '+3,8%',
      positive: true
    }
  };
  
  const recentOrders = [
    { id: 'OS-2025-042', customer: 'Indústria ABC Ltda', date: '18/05/2025', value: 'R$ 1.250,00', status: 'completed' },
    { id: 'OS-2025-041', customer: 'Metalúrgica XYZ', date: '17/05/2025', value: 'R$ 3.780,50', status: 'processing' },
    { id: 'OS-2025-040', customer: 'Construtora Horizonte', date: '16/05/2025', value: 'R$ 890,25', status: 'completed' },
    { id: 'OS-2025-039', customer: 'Fábrica de Móveis Silva', date: '15/05/2025', value: 'R$ 2.340,00', status: 'pending' },
    { id: 'OS-2025-038', customer: 'Transportadora Expressa', date: '14/05/2025', value: 'R$ 1.670,80', status: 'completed' }
  ];
  
  const topProducts = [
    { name: 'Mangueira Hidráulica 1/2"', sales: 42, revenue: 'R$ 3.775,80' },
    { name: 'Kit Reparo para Mangueiras', sales: 28, revenue: 'R$ 3.360,00' },
    { name: 'Válvula de Controle', sales: 15, revenue: 'R$ 2.925,00' },
    { name: 'Mangueira de Alta Temperatura', sales: 18, revenue: 'R$ 2.619,00' },
    { name: 'Conexão Rápida 3/4"', sales: 35, revenue: 'R$ 1.592,50' }
  ];
  
  const lowStockAlerts = [
    { name: 'Válvula de Controle', stock: 8, minStock: 10 },
    { name: 'Adaptador Hidráulico', stock: 18, minStock: 20 },
    { name: 'Mangueira de Alta Temperatura', stock: 12, minStock: 15 }
  ];
  
  // Renderizar KPI cards
  const renderKpiCards = () => {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card variant="elevated" className="p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-secondary-500 text-sm mb-1">Vendas</p>
              <h3 className="text-2xl font-bold mb-1">{kpiData.sales.value}</h3>
              <p className={`text-sm ${kpiData.sales.positive ? 'text-green-500' : 'text-red-500'}`}>
                <i className={`fas fa-arrow-${kpiData.sales.positive ? 'up' : 'down'} mr-1`}></i>
                {kpiData.sales.change} este mês
              </p>
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
              <h3 className="text-2xl font-bold mb-1">{kpiData.orders.value}</h3>
              <p className={`text-sm ${kpiData.orders.positive ? 'text-green-500' : 'text-red-500'}`}>
                <i className={`fas fa-arrow-${kpiData.orders.positive ? 'up' : 'down'} mr-1`}></i>
                {kpiData.orders.change} este mês
              </p>
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
              <h3 className="text-2xl font-bold mb-1">{kpiData.customers.value}</h3>
              <p className={`text-sm ${kpiData.customers.positive ? 'text-green-500' : 'text-red-500'}`}>
                <i className={`fas fa-arrow-${kpiData.customers.positive ? 'up' : 'down'} mr-1`}></i>
                {kpiData.customers.change} este mês
              </p>
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
              <h3 className="text-2xl font-bold mb-1">{kpiData.averageTicket.value}</h3>
              <p className={`text-sm ${kpiData.averageTicket.positive ? 'text-green-500' : 'text-red-500'}`}>
                <i className={`fas fa-arrow-${kpiData.averageTicket.positive ? 'up' : 'down'} mr-1`}></i>
                {kpiData.averageTicket.change} este mês
              </p>
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
            <p className="text-secondary-500">Bem-vindo de volta, Admin</p>
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
            
            <Button variant="primary">
              <i className="fas fa-sync-alt mr-2"></i>
              Atualizar
            </Button>
          </div>
        </div>
        
        {/* KPI Cards */}
        {renderKpiCards()}
        
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
              data={{}} 
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
              data={{}} 
              options={{ 
                title: 'Vendas por Categoria',
                legend: true
              }} 
            />
          </Card>
        </div>
        
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
                    <TableRow key={index}>
                      <TableCell>{product.name}</TableCell>
                      <TableCell>{product.sales} un</TableCell>
                      <TableCell>{product.revenue}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </Card>
        </div>
        
        {/* Alertas de Estoque Baixo */}
        {lowStockAlerts.length > 0 && (
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
            <div className="relative">
              <div className="absolute top-0 bottom-0 left-4 w-0.5 bg-secondary-200"></div>
              
              <div className="relative pl-12 pb-8">
                <div className="absolute left-0 top-1 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-500">
                  <i className="fas fa-file-invoice"></i>
                </div>
                <div>
                  <p className="font-medium">Novo pedido criado</p>
                  <p className="text-sm text-secondary-500">Pedido OS-2025-042 para Indústria ABC Ltda</p>
                  <p className="text-xs text-secondary-400 mt-1">Hoje, 14:32</p>
                </div>
              </div>
              
              <div className="relative pl-12 pb-8">
                <div className="absolute left-0 top-1 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-500">
                  <i className="fas fa-check"></i>
                </div>
                <div>
                  <p className="font-medium">Pedido concluído</p>
                  <p className="text-sm text-secondary-500">Pedido OS-2025-040 para Construtora Horizonte</p>
                  <p className="text-xs text-secondary-400 mt-1">Hoje, 11:15</p>
                </div>
              </div>
              
              <div className="relative pl-12 pb-8">
                <div className="absolute left-0 top-1 w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-500">
                  <i className="fas fa-user"></i>
                </div>
                <div>
                  <p className="font-medium">Novo cliente cadastrado</p>
                  <p className="text-sm text-secondary-500">Metalúrgica XYZ</p>
                  <p className="text-xs text-secondary-400 mt-1">Ontem, 16:48</p>
                </div>
              </div>
              
              <div className="relative pl-12">
                <div className="absolute left-0 top-1 w-8 h-8 rounded-full bg-yellow-100 flex items-center justify-center text-yellow-500">
                  <i className="fas fa-exclamation-triangle"></i>
                </div>
                <div>
                  <p className="font-medium">Alerta de estoque</p>
                  <p className="text-sm text-secondary-500">Válvula de Controle abaixo do estoque mínimo</p>
                  <p className="text-xs text-secondary-400 mt-1">Ontem, 09:23</p>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </motion.div>
    </div>
  );
};

export default DashboardPage;
