import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { useNavigate } from 'react-router-dom';
import { ProductSearch } from './components/ProductSearch';
import { Cart } from './components/Cart';
import { PaymentModal } from './components/PaymentModal';
import { useProducts } from '../../hooks/useProducts';
import { useToast } from '../../components/ui/Toast';
import { ProductList } from '../../components/pdv/ProductList';
import { Product } from '../../types/common';
// import { PDVLayout } from '../../layouts/PDVLayout';

interface CartItem extends Product {
  quantity: number;
}

const PDVPage = () => {
  const navigate = useNavigate();
  const { products, loading } = useProducts();
  const { addToast } = useToast();
  // Estados
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [showCustomerModal, setShowCustomerModal] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('');
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  
  // Estados para dados reais
  const [customers, setCustomers] = useState([]);

  // Verificar se há um cliente recém-cadastrado na navegação
  useEffect(() => {
    const location = window.location;
    if (location.state && location.state.newCustomer) {
      setSelectedCustomer(location.state.newCustomer);
      // Limpar o estado para evitar problemas ao recarregar a página
      window.history.replaceState({}, document.title);
    }
  }, []);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await api.get('/accounts/customers/');
        
        if (response.status !== 200) {
          throw new Error(`Erro na requisição: ${response.status}`);
        }
        
        if (response.data && (response.data.results || Array.isArray(response.data))) {
          setCustomers(response.data.results || response.data);
        } else {
          throw new Error('Formato de resposta inválido');
        }
      } catch (error) {
        console.error('Erro ao buscar clientes:', error);
        // Mostrar mensagem de erro para o usuário
        alert('Não foi possível carregar a lista de clientes. Por favor, tente novamente mais tarde.');
      }
    };

    fetchCustomers();
  }, []);
  
  // Filtrar produtos
  const filteredProducts = products.filter(product => 
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.code.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  // Adicionar ao carrinho
  const handleSelectProduct = (product: Product) => {
    setCartItems(prev => {
      const existingItem = prev.find(item => item.id === product.id);
      if (existingItem) {
        return prev.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };
  
  // Remover do carrinho
  const handleRemoveItem = (productId: string) => {
    setCartItems(prev => prev.filter(item => item.id !== productId));
  };
  
  // Atualizar quantidade
  const handleUpdateQuantity = (productId: string, quantity: number) => {
    setCartItems(prev =>
      prev.map(item =>
        item.id === productId ? { ...item, quantity } : item
      )
    );
  };
  
  // Calcular total
  const cartTotal = cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  
  // Finalizar venda
  const handleFinalizeSale = async () => {
    if (cartItems.length === 0) {
      alert('Adicione produtos ao carrinho para finalizar a venda.');
      return;
    }
    
    if (!selectedCustomer) {
      alert('Selecione um cliente para finalizar a venda.');
      return;
    }
    
    try {
      const sale = {
        items: cartItems.map(item => ({
          productId: item.id,
          quantity: item.quantity,
          price: item.price
        })),
        total: cartTotal
      };

      await api.post('/sales', sale);
      setCartItems([]);
      setSelectedCustomer(null);
      setPaymentMethod('');
      setShowPaymentModal(false);
      addToast('Venda realizada com sucesso!', 'success');
    } catch (error) {
      console.error('Erro ao finalizar venda:', error);
      alert('Erro ao finalizar venda. Por favor, tente novamente mais tarde.');
      addToast('Erro ao finalizar venda', 'error');
    }
  };
  
  // Processar pagamento
  const processPayment = async () => {
    if (!paymentMethod) {
      alert('Selecione um método de pagamento.');
      return;
    }
    
    try {
      // Preparar dados do pedido
      const orderData = {
        customer: selectedCustomer.id,
        items: cartItems.map(item => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price
        })),
        payment_method: paymentMethod.toLowerCase().replace(' ', '_'),
        notes: 'Pedido criado via PDV'
      };
      
      // Enviar pedido para a API
      const response = await api.post('/orders/create/', orderData);
      
      if (response.status !== 201 && response.status !== 200) {
        throw new Error(`Erro ao criar pedido: ${response.status}`);
      }
      
      // Mostrar mensagem de sucesso
      alert(`Venda finalizada com sucesso!\nPedido #${response.data.id || response.data.order_id}\nCliente: ${selectedCustomer.name}\nTotal: R$ ${cartTotal.toFixed(2)}\nForma de pagamento: ${paymentMethod}`);
      
      // Limpar carrinho e fechar modal
      setCartItems([]);
      setSelectedCustomer(null);
      setPaymentMethod('');
      setShowPaymentModal(false);
    } catch (error) {
      console.error('Erro ao processar pagamento:', error);
      alert('Erro ao finalizar venda. Por favor, tente novamente.');
      addToast('Erro ao finalizar venda', 'error');
    }
  };
  
  return (
    <div className="flex h-screen overflow-hidden bg-background-lightGray">
      {/* Área principal */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Cabeçalho */}
        <header className="bg-white border-b border-secondary-200 py-4 px-6">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-secondary-900">PDV - Ponto de Venda</h1>
            <div className="flex items-center space-x-4">
              <Button 
                variant="outline"
                onClick={() => setShowCustomerModal(true)}
              >
                {selectedCustomer ? (
                  <span>Cliente: {selectedCustomer.name}</span>
                ) : (
                  <span>Selecionar Cliente</span>
                )}
              </Button>
              <Button 
                variant="primary"
                onClick={handleFinalizeSale}
                disabled={cartItems.length === 0}
              >
                Finalizar Venda
              </Button>
            </div>
          </div>
        </header>
        
        {/* Conteúdo principal */}
        <div className="flex-1 overflow-hidden flex">
          {/* Lista de produtos */}
          <div className="w-2/3 p-6 overflow-auto">
            <ProductSearch
              searchTerm={searchTerm}
              onSearchChange={setSearchTerm}
            />
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {loading ? (
                <div>Carregando produtos...</div>
              ) : (
                <ProductList
                  products={products}
                  onSelectProduct={handleSelectProduct}
                />
              )}
              
              {filteredProducts.length === 0 && (
                <div className="col-span-full text-center py-12">
                  <p className="text-secondary-500">Nenhum produto encontrado.</p>
                </div>
              )}
            </div>
          </div>
          
          {/* Carrinho */}
          <div className="w-1/3 bg-white border-l border-secondary-200 flex flex-col">
            <div className="p-4 border-b border-secondary-200">
              <h2 className="text-lg font-semibold">Carrinho de Compras</h2>
            </div>
            
            <div className="flex-1 overflow-auto p-4">
              <Cart
                items={cartItems}
                onUpdateQuantity={handleUpdateQuantity}
                onRemoveItem={handleRemoveItem}
                onFinalize={handleFinalizeSale}
              />
            </div>
            
            <div className="p-4 border-t border-secondary-200 bg-secondary-50">
              <div className="flex justify-between mb-2">
                <span className="text-secondary-700">Subtotal</span>
                <span className="font-medium">R$ {cartTotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between mb-4">
                <span className="text-secondary-700">Desconto</span>
                <span className="font-medium">R$ 0,00</span>
              </div>
              <div className="flex justify-between text-lg font-bold">
                <span>Total</span>
                <span>R$ {cartTotal.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Modal de seleção de cliente */}
      {showCustomerModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl">
            <div className="p-6 border-b border-secondary-200 flex justify-between items-center">
              <h3 className="text-lg font-semibold">Selecionar Cliente</h3>
              <button
                className="text-secondary-500 hover:text-secondary-700"
                onClick={() => setShowCustomerModal(false)}
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
            
            <div className="p-6">
              <Input
                placeholder="Buscar cliente..."
                leftIcon={<i className="fas fa-search"></i>}
                className="mb-4"
              />
              
              <div className="overflow-x-auto">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell isHeader>Nome</TableCell>
                      <TableCell isHeader>Email</TableCell>
                      <TableCell isHeader>Telefone</TableCell>
                      <TableCell isHeader>Ações</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {customers.map(customer => (
                      <TableRow key={customer.id}>
                        <TableCell>{customer.name}</TableCell>
                        <TableCell>{customer.email}</TableCell>
                        <TableCell>{customer.phone}</TableCell>
                        <TableCell>
                          <Button
                            variant="primary"
                            size="sm"
                            onClick={() => {
                              setSelectedCustomer(customer);
                              setShowCustomerModal(false);
                            }}
                          >
                            Selecionar
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
              
              <div className="mt-6 flex justify-between">
                <Button
                  variant="outline"
                  onClick={() => setShowCustomerModal(false)}
                >
                  Cancelar
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    navigate('/customers/new?redirect=pdv');
                  }}
                >
                  Cadastrar Novo Cliente
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Modal de pagamento */}
      {showPaymentModal && (
        <PaymentModal
          isOpen={showPaymentModal}
          onClose={() => setShowPaymentModal(false)}
          onConfirm={processPayment}
          paymentMethod={paymentMethod}
          onPaymentMethodChange={setPaymentMethod}
          total={cartTotal}
        />
      )}
    </div>
  );
};

export default PDVPage;
