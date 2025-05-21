import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CheckoutForm } from './components/CheckoutForm';
import { OrderSummary } from './components/OrderSummary';
import { api } from '../../services/api';

export const CheckoutPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const items = location.state?.items || [];

  const handleSubmit = async (paymentData: any) => {
    setIsLoading(true);
    try {
      const orderData = {
        items: items.map((item: any) => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price
        })),
        payment: {
          method: 'credit_card',
          ...paymentData
        }
      };

      const response = await api.post('/orders/create/', orderData);
      
      // Redirecionar para página de sucesso
      navigate('/checkout/success', {
        state: { orderId: response.data.id }
      });
    } catch (error: any) {
      alert(error.response?.data?.message || 'Erro ao processar pagamento');
    } finally {
      setIsLoading(false);
    }
  };

  if (items.length === 0) {
    navigate('/marketplace');
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold mb-8">Checkout</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="text-lg font-medium mb-4">Dados do Pagamento</h2>
          <CheckoutForm onSubmit={handleSubmit} isLoading={isLoading} />
        </div>

        <div>
          <OrderSummary items={items} />
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage; 