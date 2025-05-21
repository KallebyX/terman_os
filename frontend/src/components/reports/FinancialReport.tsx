import React, { useState } from 'react';
import { Card, DateRangePicker, Tabs } from '../ui';
import { LineChart, PieChart } from '../charts';
import { useFinancialReport } from '../../hooks/useFinancialReport';
import { formatCurrency, formatPercentage } from '../../utils/formatters';

export const FinancialReport: React.FC = () => {
  const [dateRange, setDateRange] = useState<{ start: Date; end: Date }>();
  const [activeTab, setActiveTab] = useState('overview');
  const { data, loading, error } = useFinancialReport(dateRange);

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Relatório Financeiro</h2>
        <DateRangePicker
          value={dateRange}
          onChange={setDateRange}
          className="w-72"
        />
      </div>

      {loading && <div>Carregando...</div>}
      {error && <div>Erro ao carregar dados financeiros</div>}

      {data && (
        <>
          <div className="grid grid-cols-4 gap-4 mb-6">
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Receita Total</h3>
              <p className="text-2xl font-bold mt-2">{formatCurrency(data.totalRevenue)}</p>
              <p className={`text-sm mt-1 ${data.revenueGrowth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {data.revenueGrowth >= 0 ? '+' : ''}{formatPercentage(data.revenueGrowth)}
              </p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Lucro Líquido</h3>
              <p className="text-2xl font-bold mt-2">{formatCurrency(data.netProfit)}</p>
              <p className={`text-sm mt-1 ${data.profitGrowth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {data.profitGrowth >= 0 ? '+' : ''}{formatPercentage(data.profitGrowth)}
              </p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Margem de Lucro</h3>
              <p className="text-2xl font-bold mt-2">{formatPercentage(data.profitMargin)}</p>
              <p className="text-sm mt-1 text-gray-500">Meta: {formatPercentage(data.profitMarginGoal)}</p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Custos Operacionais</h3>
              <p className="text-2xl font-bold mt-2">{formatCurrency(data.operationalCosts)}</p>
              <p className="text-sm mt-1 text-gray-500">{formatPercentage(data.costsPercentage)} da receita</p>
            </Card>
          </div>

          <Tabs
            value={activeTab}
            onChange={setActiveTab}
            items={[
              { value: 'overview', label: 'Visão Geral' },
              { value: 'revenue', label: 'Receitas' },
              { value: 'expenses', label: 'Despesas' },
              { value: 'cashflow', label: 'Fluxo de Caixa' }
            ]}
            className="mb-6"
          />

          {activeTab === 'overview' && (
            <div className="grid grid-cols-2 gap-6">
              <Card className="p-4">
                <h3 className="text-lg font-medium mb-4">Receita vs Despesas</h3>
                <LineChart
                  data={data.revenueVsExpenses}
                  series={['revenue', 'expenses']}
                  height={300}
                />
              </Card>
              <Card className="p-4">
                <h3 className="text-lg font-medium mb-4">Distribuição de Despesas</h3>
                <PieChart
                  data={data.expenseDistribution}
                  height={300}
                />
              </Card>
            </div>
          )}

          {activeTab === 'revenue' && (
            <div className="space-y-6">
              <Card className="p-4">
                <h3 className="text-lg font-medium mb-4">Receita por Categoria</h3>
                <div className="space-y-4">
                  {data.revenueByCategory.map((category) => (
                    <div key={category.name} className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">{category.name}</p>
                        <p className="text-sm text-gray-500">{category.percentage}% do total</p>
                      </div>
                      <p className="font-bold">{formatCurrency(category.value)}</p>
                    </div>
                  ))}
                </div>
              </Card>
              
              <Card className="p-4">
                <h3 className="text-lg font-medium mb-4">Formas de Pagamento</h3>
                <div className="grid grid-cols-2 gap-4">
                  <PieChart
                    data={data.paymentMethods}
                    height={250}
                  />
                  <div className="space-y-4">
                    {data.paymentMethods.map((method) => (
                      <div key={method.name} className="flex justify-between items-center">
                        <div>
                          <p className="font-medium">{method.name}</p>
                          <p className="text-sm text-gray-500">{method.percentage}% das transações</p>
                        </div>
                        <p className="font-bold">{formatCurrency(method.value)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>
            </div>
          )}

          {activeTab === 'expenses' && (
            <div className="space-y-6">
              <Card className="p-4">
                <h3 className="text-lg font-medium mb-4">Maiores Despesas</h3>
                <table className="min-w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left py-3">Categoria</th>
                      <th className="text-right py-3">Valor</th>
                      <th className="text-right py-3">% do Total</th>
                      <th className="text-right py-3">vs Mês Anterior</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.topExpenses.map((expense) => (
                      <tr key={expense.category} className="border-b">
                        <td className="py-3">{expense.category}</td>
                        <td className="text-right py-3">{formatCurrency(expense.value)}</td>
                        <td className="text-right py-3">{formatPercentage(expense.percentage)}</td>
                        <td className={`text-right py-3 ${expense.growth >= 0 ? 'text-red-600' : 'text-green-600'}`}>
                          {expense.growth >= 0 ? '+' : ''}{formatPercentage(expense.growth)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Card>
            </div>
          )}

          {activeTab === 'cashflow' && (
            <div className="space-y-6">
              <Card className="p-4">
                <h3 className="text-lg font-medium mb-4">Fluxo de Caixa Diário</h3>
                <LineChart
                  data={data.dailyCashFlow}
                  series={['inflow', 'outflow', 'balance']}
                  height={300}
                />
              </Card>

              <div className="grid grid-cols-3 gap-4">
                <Card className="p-4">
                  <h3 className="text-sm text-gray-500">Saldo Atual</h3>
                  <p className="text-2xl font-bold mt-2">{formatCurrency(data.currentBalance)}</p>
                </Card>
                <Card className="p-4">
                  <h3 className="text-sm text-gray-500">Contas a Receber</h3>
                  <p className="text-2xl font-bold mt-2">{formatCurrency(data.accountsReceivable)}</p>
                </Card>
                <Card className="p-4">
                  <h3 className="text-sm text-gray-500">Contas a Pagar</h3>
                  <p className="text-2xl font-bold mt-2">{formatCurrency(data.accountsPayable)}</p>
                </Card>
              </div>
            </div>
          )}
        </>
      )}
    </Card>
  );
}; 