import { useState, useCallback } from 'react';
import { useApi } from './useApi';
import { Product, OrderItem, PaymentMethod } from '../types/pdv';
import { useWebSocket } from '../contexts/WebSocketContext';

export const usePDV = () => {
    const [items, setItems] = useState<OrderItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const api = useApi();
    const { emit } = useWebSocket();

    const addItem = useCallback((product: Product, quantity: number = 1) => {
        setItems(current => {
            const existingIndex = current.findIndex(item => 
                item.product.id === product.id
            );

            if (existingIndex >= 0) {
                const newItems = [...current];
                newItems[existingIndex].quantity += quantity;
                return newItems;
            }

            return [...current, {
                product,
                quantity,
                price: product.price,
                discount: 0
            }];
        });
    }, []);

    const removeItem = useCallback((index: number) => {
        setItems(current => current.filter((_, i) => i !== index));
    }, []);

    const updateQuantity = useCallback((index: number, quantity: number) => {
        setItems(current => {
            const newItems = [...current];
            newItems[index].quantity = quantity;
            return newItems;
        });
    }, []);

    const applyDiscount = useCallback((index: number, discount: number) => {
        setItems(current => {
            const newItems = [...current];
            newItems[index].discount = discount;
            return newItems;
        });
    }, []);

    const finalizeOrder = useCallback(async (paymentData: {
        method: PaymentMethod;
        clientId?: number;
    }) => {
        try {
            setLoading(true);
            setError(null);

            const response = await api.pdv.createOrder({
                items: items.map(item => ({
                    product_id: item.product.id,
                    quantity: item.quantity,
                    price: item.price,
                    discount: item.discount
                })),
                paymentMethod: paymentData.method,
                clientId: paymentData.clientId
            });

            // Notificar outros usuários sobre novo pedido
            emit('new_order', {
                order_id: response.id,
                total: response.total,
                items_count: items.length
            });

            // Limpar carrinho
            setItems([]);

            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [items, api.pdv, emit]);

    const cancelOrder = useCallback(() => {
        setItems([]);
    }, []);

    return {
        items,
        loading,
        error,
        addItem,
        removeItem,
        updateQuantity,
        applyDiscount,
        finalizeOrder,
        cancelOrder
    };
}; 