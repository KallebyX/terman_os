import React, { useState } from 'react';
import { Modal, Button, Input, Select } from '../ui';
import { PaymentMethod } from '../../types/pdv';
import { usePayment } from '../../hooks/usePayment';
import { formatCurrency } from '../../utils/formatters';
import QRCode from 'react-qr-code';

interface PaymentModalProps {
    isOpen: boolean;
    onClose: () => void;
    orderId: number;
    totalAmount: number;
    onPaymentComplete: () => void;
}

export const PaymentModal: React.FC<PaymentModalProps> = ({
    isOpen,
    onClose,
    orderId,
    totalAmount,
    onPaymentComplete
}) => {
    const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>('credit_card');
    const [installments, setInstallments] = useState(1);
    const [cardData, setCardData] = useState({
        number: '',
        holder: '',
        expiry: '',
        cvv: ''
    });
    
    const { processPayment, loading, error } = usePayment();

    const handleSubmit = async () => {
        try {
            await processPayment(orderId, {
                method: paymentMethod,
                amount: totalAmount,
                installments: paymentMethod === 'credit_card' ? installments : undefined,
                cardData: paymentMethod === 'credit_card' ? cardData : undefined
            });
            onPaymentComplete();
            onClose();
        } catch (err) {
            console.error('Erro ao processar pagamento:', err);
        }
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title="Pagamento">
            <div className="space-y-4">
                <div>
                    <p className="text-lg font-bold">
                        Total: {formatCurrency(totalAmount)}
                    </p>
                </div>

                <Select
                    value={paymentMethod}
                    onChange={(value) => setPaymentMethod(value as PaymentMethod)}
                    options={[
                        { value: 'credit_card', label: 'Cartão de Crédito' },
                        { value: 'debit_card', label: 'Cartão de Débito' },
                        { value: 'pix', label: 'PIX' },
                        { value: 'cash', label: 'Dinheiro' }
                    ]}
                    label="Forma de Pagamento"
                />

                {paymentMethod === 'credit_card' && (
                    <div className="space-y-4">
                        <Input
                            label="Número do Cartão"
                            value={cardData.number}
                            onChange={(e) => setCardData({ ...cardData, number: e.target.value })}
                            mask="9999 9999 9999 9999"
                        />
                        <Input
                            label="Nome do Titular"
                            value={cardData.holder}
                            onChange={(e) => setCardData({ ...cardData, holder: e.target.value })}
                        />
                        <div className="grid grid-cols-2 gap-4">
                            <Input
                                label="Validade"
                                value={cardData.expiry}
                                onChange={(e) => setCardData({ ...cardData, expiry: e.target.value })}
                                mask="99/99"
                            />
                            <Input
                                label="CVV"
                                value={cardData.cvv}
                                onChange={(e) => setCardData({ ...cardData, cvv: e.target.value })}
                                mask="999"
                                type="password"
                            />
                        </div>
                        <Select
                            value={installments}
                            onChange={(value) => setInstallments(Number(value))}
                            options={Array.from({ length: 12 }, (_, i) => ({
                                value: i + 1,
                                label: `${i + 1}x de ${formatCurrency(totalAmount / (i + 1))}`
                            }))}
                            label="Parcelas"
                        />
                    </div>
                )}

                {paymentMethod === 'pix' && (
                    <div className="flex flex-col items-center space-y-4">
                        <QRCode value="PIX_KEY_HERE" size={200} />
                        <p className="text-sm text-gray-500">
                            Escaneie o código QR com seu aplicativo de pagamento
                        </p>
                    </div>
                )}

                {error && (
                    <p className="text-red-600 text-sm">{error}</p>
                )}

                <div className="flex justify-end space-x-4">
                    <Button variant="outline" onClick={onClose}>
                        Cancelar
                    </Button>
                    <Button
                        variant="primary"
                        onClick={handleSubmit}
                        loading={loading}
                        disabled={loading}
                    >
                        Confirmar Pagamento
                    </Button>
                </div>
            </div>
        </Modal>
    );
}; 