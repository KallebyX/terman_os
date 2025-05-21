import { useState, useCallback } from 'react';
import { useApi } from './useApi';
import { CashierStatus } from '../types/pdv';

export const useCashier = () => {
    const [status, setStatus] = useState<CashierStatus>('closed');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const api = useApi();

    const openCashier = useCallback(async (initialAmount: number) => {
        try {
            setLoading(true);
            setError(null);

            const response = await api.pdv.openCashier({
                initial_amount: initialAmount,
                opened_at: new Date().toISOString()
            });

            setStatus('open');
            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [api.pdv]);

    const closeCashier = useCallback(async (finalAmount: number) => {
        try {
            setLoading(true);
            setError(null);

            const response = await api.pdv.closeCashier({
                final_amount: finalAmount,
                closed_at: new Date().toISOString()
            });

            setStatus('closed');
            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [api.pdv]);

    const getCashierStatus = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);

            const response = await api.pdv.getCashierStatus();
            setStatus(response.status);
            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [api.pdv]);

    return {
        status,
        loading,
        error,
        openCashier,
        closeCashier,
        getCashierStatus
    };
}; 