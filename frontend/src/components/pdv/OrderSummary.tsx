import React from 'react';
import { Card, Button } from '../ui';
import { OrderItem } from '../../types/pdv';
import { formatCurrency } from '../../utils/formatters';

interface OrderSummaryProps {
    items: OrderItem[];
    onRemoveItem: (index: number) => void;
    onUpdateQuantity: (index: number, quantity: number) => void;
    onFinalize: () => void;
    onCancel: () => void;
}

export const OrderSummary: React.FC<OrderSummaryProps> = ({
    items,
    onRemoveItem,
    onUpdateQuantity,
    onFinalize,
    onCancel
}) => {
    const total = items.reduce((sum, item) => 
        sum + (item.price * item.quantity - (item.discount || 0)), 0
    );

    return (
        <Card className="p-4">
            <h2 className="text-lg font-bold mb-4">Resumo do Pedido</h2>

            <div className="space-y-4 mb-4">
                {items.map((item, index) => (
                    <div key={index} className="flex items-center justify-between">
                        <div className="flex-1">
                            <p className="font-medium">{item.product.name}</p>
                            <p className="text-sm text-gray-500">
                                {formatCurrency(item.price)} x {item.quantity}
                            </p>
                            {item.discount > 0 && (
                                <p className="text-sm text-red-600">
                                    Desconto: {formatCurrency(item.discount)}
                                </p>
                            )}
                        </div>
                        <div className="flex items-center space-x-2">
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={() => onUpdateQuantity(index, item.quantity - 1)}
                                disabled={item.quantity <= 1}
                            >
                                -
                            </Button>
                            <span className="w-8 text-center">{item.quantity}</span>
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={() => onUpdateQuantity(index, item.quantity + 1)}
                                disabled={item.quantity >= item.product.stock_quantity}
                            >
                                +
                            </Button>
                            <Button
                                variant="danger"
                                size="sm"
                                onClick={() => onRemoveItem(index)}
                            >
                                Remover
                            </Button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-4">
                    <span className="text-lg font-bold">Total:</span>
                    <span className="text-2xl font-bold text-green-600">
                        {formatCurrency(total)}
                    </span>
                </div>

                <div className="flex space-x-4">
                    <Button
                        variant="danger"
                        onClick={onCancel}
                        className="flex-1"
                    >
                        Cancelar
                    </Button>
                    <Button
                        variant="primary"
                        onClick={onFinalize}
                        className="flex-1"
                        disabled={items.length === 0}
                    >
                        Finalizar Pedido
                    </Button>
                </div>
            </div>
        </Card>
    );
}; 