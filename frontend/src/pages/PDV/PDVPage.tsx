import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { useNavigate } from 'react-router-dom';
// import { PDVLayout } from '../../layouts/PDVLayout';

const PDVPage = () => {
  const navigate = useNavigate();
  // Estados
  const [cart, setCart] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [showCustomerModal, setShowCustomerModal] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('');
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  
  // Estados para dados reais
  const [products, setProducts] = useState([]);
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
    const fetchProducts = async () => {
      try {
        const response = await api.get('/products/produtos/');
        
        if (response.status !== 200) {
          throw new Error(`Erro na requisição: ${response.status}`);
        }
        
        if (response.data && (response.data.results || Array.isArray(response.data))) {
          setProducts(response.data.results || response.data);
        } else {
          throw new Error('Formato de resposta inválido');
        }
      } catch (error) {
        console.error('Erro ao buscar produtos:', error);
        // Mostrar mensagem de erro para o usuário
        alert('Não foi possível carregar a lista de produtos. Por favor, tente novamente mais tarde.');
      }
    };

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

    fetchProducts();
    fetchCustomers();
  }, []);
  
  // Filtrar produtos
  const filteredProducts = products.filter(product => 
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.code.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  // Adicionar ao carrinho
  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      setCart(cart.map(item => 
        item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
      ));
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  };
  
  // Remover do carrinho
  const removeFromCart = (productId) => {
    setCart(cart.filter(item => item.id !== productId));
  };
  
  // Atualizar quantidade
  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity < 1) return;
    
    setCart(cart.map(item => 
      item.id === productId ? { ...item, quantity: newQuantity } : item
    ));
  };
  
  // Calcular total
  const cartTotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  
  // Finalizar venda
  const finalizeSale = () => {
    if (cart.length === 0) {
      alert('Adicione produtos ao carrinho para finalizar a venda.');
      return;
    }
    
    if (!selectedCustomer) {
      alert('Selecione um cliente para finalizar a venda.');
      return;
    }
    
    setShowPaymentModal(true);
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
        items: cart.map(item => ({
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
      setCart([]);
      setSelectedCustomer(null);
      setPaymentMethod('');
      setShowPaymentModal(false);
    } catch (error) {
      console.error('Erro ao processar pagamento:', error);
      alert('Erro ao finalizar venda. Por favor, tente novamente.');
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
                onClick={finalizeSale}
                disabled={cart.length === 0}
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
            <div className="mb-6">
              <Input
                placeholder="Buscar produtos por nome ou código..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                leftIcon={<i className="fas fa-search"></i>}
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredProducts.map(product => (
                <Card
                  key={product.id}
                  variant="elevated"
                  className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => addToCart(product)}
                >
                  <div className="p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">{product.name}</h3>
                      <span className="text-xs bg-secondary-100 text-secondary-800 px-2 py-1 rounded">
                        {product.code}
                      </span>
                    </div>
                    <div className="flex justify-between items-end">
                      <span className="text-lg font-bold text-secondary-900">
                        R$ {product.price.toFixed(2)}
                      </span>
                      <span className={`text-sm ${product.stock > 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {product.stock > 0 ? `${product.stock} em estoque` : 'Esgotado'}
                      </span>
                    </div>
                  </div>
                </Card>
              ))}
              
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
              {cart.length > 0 ? (
                <div className="space-y-4">
                  {cart.map(item => (
                    <Card key={item.id} variant="bordered" className="p-3">
                      <div className="flex justify-between mb-2">
                        <h4 className="font-medium">{item.name}</h4>
                        <button
                          className="text-red-500 hover:text-red-700"
                          onClick={() => removeFromCart(item.id)}
                        >
                          <i className="fas fa-times"></i>
                        </button>
                      </div>
                      <div className="flex justify-between items-center">
                        <div className="flex items-center">
                          <button
                            className="w-6 h-6 flex items-center justify-center bg-secondary-100 rounded-l"
                            onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          >
                            -
                          </button>
                          <span className="w-8 h-6 flex items-center justify-center bg-white border-y border-secondary-200">
                            {item.quantity}
                          </span>
                          <button
                            className="w-6 h-6 flex items-center justify-center bg-secondary-100 rounded-r"
                            onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          >
                            +
                          </button>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-secondary-500">R$ {item.price.toFixed(2)} un</p>
                          <p className="font-semibold">R$ {(item.price * item.quantity).toFixed(2)}</p>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <div className="text-secondary-400 text-4xl mb-4">
                    <i className="fas fa-shopping-cart"></i>
                  </div>
                  <p className="text-secondary-500">Carrinho vazio</p>
                  <p className="text-sm text-secondary-400 mt-1">Adicione produtos clicando nos itens à esquerda</p>
                </div>
              )}
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
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div className="p-6 border-b border-secondary-200 flex justify-between items-center">
              <h3 className="text-lg font-semibold">Finalizar Venda</h3>
              <button
                className="text-secondary-500 hover:text-secondary-700"
                onClick={() => setShowPaymentModal(false)}
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
            
            <div className="p-6">
              <div className="mb-6">
                <h4 className="font-medium mb-2">Cliente</h4>
                <Card variant="bordered" className="p-3">
                  <p className="font-semibold">{selectedCustomer?.name}</p>
                  <p className="text-sm text-secondary-500">{selectedCustomer?.email}</p>
                  <p className="text-sm text-secondary-500">{selectedCustomer?.phone}</p>
                </Card>
              </div>
              
              <div className="mb-6">
                <h4 className="font-medium mb-2">Resumo da Compra</h4>
                <div className="bg-secondary-50 rounded-lg p-3">
                  <div className="flex justify-between mb-1">
                    <span className="text-secondary-700">Itens</span>
                    <span>{cart.length}</span>
                  </div>
                  <div className="flex justify-between mb-1">
                    <span className="text-secondary-700">Quantidade</span>
                    <span>{cart.reduce((total, item) => total + item.quantity, 0)}</span>
                  </div>
                  <div className="flex justify-between font-bold mt-2 pt-2 border-t border-secondary-200">
                    <span>Total</span>
                    <span>R$ {cartTotal.toFixed(2)}</span>
                  </div>
                </div>
              </div>
              
              <div className="mb-6">
                <h4 className="font-medium mb-2">Forma de Pagamento</h4>
                <div className="grid grid-cols-2 gap-3">
                  {['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'Pix', 'Boleto', 'Transferência'].map(method => (
                    <div
                      key={method}
                      className={`border rounded-lg p-3 cursor-pointer transition-colors ${
                        paymentMethod === method
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-secondary-200 hover:border-primary-300'
                      }`}
                      onClick={() => setPaymentMethod(method)}
                    >
                      <div className="flex items-center">
                        <div className={`w-4 h-4 rounded-full border mr-2 ${
                          paymentMethod === method
                            ? 'border-primary-500 bg-primary-500'
                            : 'border-secondary-300'
                        }`}>
                          {paymentMethod === method && (
                            <div className="w-2 h-2 bg-white rounded-full m-0.5"></div>
                          )}
                        </div>
                        <span>{method}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="flex justify-between">
                <Button
                  variant="outline"
                  onClick={() => setShowPaymentModal(false)}
                >
                  Cancelar
                </Button>
                <Button
                  variant="primary"
                  onClick={processPayment}
                  disabled={!paymentMethod}
                >
                  Confirmar Pagamento
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PDVPage;
