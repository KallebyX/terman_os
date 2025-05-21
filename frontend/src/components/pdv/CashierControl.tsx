import React, { useState, useEffect } from 'react';
import { Modal, Button, Input, Card } from '../ui';
import { useCashier } from '../../hooks/useCashier';
import { formatCurrency } from '../../utils/formatters';

interface CashierControlProps {
    isOpen: boolean;
    onClose: () => void;
    type: 'open' | 'close';
}

export const CashierControl: React.FC<CashierControlProps> = ({
    isOpen,
    onClose,
    type
}) => {
    const [amount, setAmount] = useState('');
    const [summary, setSummary] = useState<any>(null);
    const { openCashier, closeCashier, getCashierStatus, loading } = useCashier();

    useEffect(() => {
        if (type === 'close' && isOpen) {
            loadCashierSummary();
        }
    }, [type, isOpen]);

    const loadCashierSummary = async () => {
        const status = await getCashierStatus();
        setSummary(status.summary);
    };

    const handleSubmit = async () => {
        try {
            const value = parseFloat(amount.replace(',', '.'));
            
            if (type === 'open') {
                await openCashier(value);
            } else {
                await closeCashier(value);
            }
            
            onClose();
        } catch (error) {
            console.error('Erro ao manipular caixa:', error);
        }
    };

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title={type === 'open' ? 'Abrir Caixa' : 'Fechar Caixa'}
        >
            <div className="space-y-6">
                {type === 'close' && summary && (
                    <div className="grid grid-cols-2 gap-4">
                        <Card className="p-4">
                            <h3 className="text-sm text-gray-500">Total em Vendas</h3>
                            <p className="text-xl font-bold">{formatCurrency(summary.total_sales)}</p>
                        </Card>
                        <Card className="p-4">
                            <h3 className="text-sm text-gray-500">Quantidade de Vendas</h3>
                            <p className="text-xl font-bold">{summary.total_orders}</p>
                        </Card>
                        <Card className="p-4">
                            <h3 className="text-sm text-gray-500">Dinheiro</h3>
                            <p className="text-xl font-bold">{formatCurrency(summary.cash_total)}</p>
                        </Card>
                        <Card className="p-4">
                            <h3 className="text-sm text-gray-500">Cartões</h3>
                            <p className="text-xl font-bold">{formatCurrency(summary.card_total)}</p>
                        </Card>
                    </div>
                )}

                <div>
                    <Input
                        label={type === 'open' ? 'Valor Inicial' : 'Valor em Caixa'}
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        type="number"
                        step="0.01"
                        min="0"
                    />
                    {type === 'close' && summary && (
                        <p className="text-sm text-gray-500 mt-2">
                            Diferença: {formatCurrency(parseFloat(amount || '0') - summary.expected_amount)}
                        </p>
                    )}
                </div>

                <div className="flex justify-end space-x-4">
                    <Button variant="outline" onClick={onClose}>
                        Cancelar
                    </Button>
                    <Button
                        variant="primary"
                        onClick={handleSubmit}
                        loading={loading}
                        disabled={loading || !amount}
                    >
                        {type === 'open' ? 'Abrir Caixa' : 'Fechar Caixa'}
                    </Button>
                </div>
            </div>
        </Modal>
    );
}; 