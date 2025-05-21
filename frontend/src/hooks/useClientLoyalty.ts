import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useAuth } from './useAuth';

interface LoyaltyReward {
  id: string;
  name: string;
  description: string;
  pointsRequired: number;
  available: boolean;
}

interface LoyaltyData {
  availablePoints: number;
  totalPointsEarned: number;
  totalPointsUsed: number;
  totalPointsExpired: number;
  progressToNextReward: number;
  pointsToNextReward: number;
  currentTier: string;
  nextTier: string;
  pointsHistory: Array<{
    id: string;
    date: string;
    points: number;
    type: 'earned' | 'used' | 'expired';
    description: string;
  }>;
  availableRewards: LoyaltyReward[];
}

export const useClientLoyalty = () => {
  const [data, setData] = useState<LoyaltyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchLoyalty = async () => {
      if (!user) return;

      try {
        setLoading(true);
        const response = await api.get('/client/loyalty');
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar dados de fidelidade'));
      } finally {
        setLoading(false);
      }
    };

    fetchLoyalty();
  }, [user]);

  return { data, loading, error };
}; 