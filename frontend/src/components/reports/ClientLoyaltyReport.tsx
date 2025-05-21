import React from 'react';
import { Card } from '../ui';
import { PieChart } from '../charts';
import { useClientLoyalty } from '../../hooks/useClientLoyalty';

export const ClientLoyaltyReport: React.FC = () => {
  const { data, loading } = useClientLoyalty();

  return (
    <Card className="p-6">
      <h2 className="text-xl font-bold mb-6">Programa de Fidelidade</h2>

      {loading ? (
        <div>Carregando...</div>
      ) : (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg p-6 text-white">
            <p className="text-sm opacity-80">Pontos Disponíveis</p>
            <p className="text-4xl font-bold mt-2">{data?.availablePoints || 0}</p>
            <div className="mt-4">
              <div className="h-2 bg-white/20 rounded-full">
                <div 
                  className="h-full bg-white rounded-full"
                  style={{ width: `${data?.progressToNextReward || 0}%` }}
                />
              </div>
              <p className="text-sm mt-2">
                Faltam {data?.pointsToNextReward || 0} pontos para seu próximo prêmio
              </p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium mb-4">Histórico de Pontos</h3>
            <div className="h-64">
              <PieChart
                data={{
                  labels: ['Ganhos', 'Utilizados', 'Expirados'],
                  datasets: [{
                    data: [
                      data?.totalPointsEarned || 0,
                      data?.totalPointsUsed || 0,
                      data?.totalPointsExpired || 0
                    ],
                    backgroundColor: [
                      '#10B981',
                      '#6366F1',
                      '#EF4444'
                    ]
                  }]
                }}
              />
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium mb-4">Prêmios Disponíveis</h3>
            <div className="grid grid-cols-2 gap-4">
              {data?.availableRewards?.map((reward) => (
                <div key={reward.id} className="p-4 border rounded-lg">
                  <p className="font-medium">{reward.name}</p>
                  <p className="text-sm text-gray-500 mt-1">{reward.description}</p>
                  <p className="text-indigo-600 font-bold mt-2">{reward.pointsRequired} pontos</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}; 