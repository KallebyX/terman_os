import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { Badge } from '../../components/ui/Badge';

// Tipo para produtos
interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image: string;
  category: string;
  stock: number;
  rating: number;
  featured: boolean;
}

// Tipo para itens do carrinho
interface CartItem {
  product: Product;
  quantity: number;
}

const MarketplacePage: React.FC = () => {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  
  // Estados
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showCart, setShowCart] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  
  // Categorias
  const categories = [
    { id: 'all', name: 'Todos os Produtos' },
    { id: 'mangueiras', name: 'Mangueiras' },
    { id: 'conexoes', name: 'Conexões' },
    { id: 'adaptadores', name: 'Adaptadores' },
    { id: 'acessorios', name: 'Acessórios' }
  ];
  
  // Produtos simulados
  useEffect(() => {
    // Em produção, isso seria uma chamada à API
    const mockProducts: Product[] = [
      {
        id: 1,
        name: 'Mangueira Hidráulica 1/2"',
        description: 'Mangueira hidráulica de alta pressão para aplicações industriais.',
        price: 89.90,
        image: '/images/products/mangueira-1.jpg',
        category: 'mangueiras',
        stock: 25,
        rating: 4.5,
        featured: true
      },
      {
        id: 2,
        name: 'Conexão Rápida 3/4"',
        description: 'Conexão rápida para mangueiras hidráulicas de 3/4 polegadas.',
        price: 45.50,
        image: '/images/products/conexao-1.jpg',
        category: 'conexoes',
        stock: 42,
        rating: 4.2,
        featured: false
      },
      {
        id: 3,
        name: 'Adaptador Hidráulico',
        description: 'Adaptador para sistemas hidráulicos de alta pressão.',
        price: 32.75,
        image: '/images/products/adaptador-1.jpg',
        category: 'adaptadores',
        stock: 18,
        rating: 4.0,
        featured: false
      },
      {
        id: 4,
        name: 'Kit Reparo para Mangueiras',
        description: 'Kit completo para reparo de mangueiras hidráulicas danificadas.',
        price: 120.00,
        image: '/images/products/kit-1.jpg',
        category: 'acessorios',
        stock: 10,
        rating: 4.8,
        featured: true
      },
      {
        id: 5,
        name: 'Mangueira Flexível 1"',
        description: 'Mangueira flexível para aplicações de baixa pressão.',
        price: 75.30,
        image: '/images/products/mangueira-2.jpg',
        category: 'mangueiras',
        stock: 15,
        rating: 4.3,
        featured: false
      },
      {
        id: 6,
        name: 'Conexão em T',
        description: 'Conexão em T para sistemas hidráulicos complexos.',
        price: 28.90,
        image: '/images/products/conexao-2.jpg',
        category: 'conexoes',
        stock: 30,
        rating: 4.1,
        featured: false
      },
      {
        id: 7,
        name: 'Válvula de Controle',
        description: 'Válvula de controle para sistemas hidráulicos industriais.',
        price: 195.00,
        image: '/images/products/valvula-1.jpg',
        category: 'acessorios',
        stock: 8,
        rating: 4.7,
        featured: true
      },
      {
        id: 8,
        name: 'Mangueira de Alta Temperatura',
        description: 'Mangueira especial para ambientes com alta temperatura.',
        price: 145.50,
        image: '/images/products/mangueira-3.jpg',
        category: 'mangueiras',
        stock: 12,
        rating: 4.6,
        featured: false
      }
    ];
    
    setProducts(mockProducts);
    
    // Se houver um ID de produto na URL, exibir detalhes do produto
    if (id) {
      const product = mockProducts.find(p => p.id === parseInt(id));
      if (product) {
        setSelectedProduct(product);
      }
    }
    
    // Carregar carrinho do localStorage
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      try {
        setCart(JSON.parse(savedCart));
      } catch (error) {
        console.error('Erro ao carregar carrinho:', error);
      }
    }
  }, [id]);
  
  // Salvar carrinho no localStorage quando atualizado
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);
  
  // Filtrar produtos
  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         product.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  });
  
  // Adicionar ao carrinho
  const addToCart = (product: Product) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.product.id === product.id);
      
      if (existingItem) {
        return prevCart.map(item => 
          item.product.id === product.id 
            ? { ...item, quantity: item.quantity + 1 } 
            : item
        );
      } else {
        return [...prevCart, { product, quantity: 1 }];
      }
    });
  };
  
  // Remover do carrinho
  const removeFromCart = (productId: number) => {
    setCart(prevCart => prevCart.filter(item => item.product.id !== productId));
  };
  
  // Atualizar quantidade no carrinho
  const updateQuantity = (productId: number, quantity: number) => {
    if (quantity < 1) return;
    
    setCart(prevCart => 
      prevCart.map(item => 
        item.product.id === productId 
          ? { ...item, quantity } 
          : item
      )
    );
  };
  
  // Calcular total do carrinho
  const cartTotal = cart.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  
  // Ir para o checkout
  const goToCheckout = () => {
    navigate('/marketplace/checkout');
  };
  
  // Renderizar grid de produtos
  const renderProductGrid = () => {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredProducts.map(product => (
          <motion.div
            key={product.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Card
              variant="elevated"
              className="h-full flex flex-col overflow-hidden transition-transform hover:scale-105"
            >
              {product.featured && (
                <div className="absolute top-2 right-2 z-10">
                  <Badge variant="primary">Destaque</Badge>
                </div>
              )}
              
              <div 
                className="h-48 bg-secondary-100 relative cursor-pointer"
                onClick={() => navigate(`/marketplace/product/${product.id}`)}
              >
                <div className="absolute inset-0 flex items-center justify-center text-secondary-400">
                  <i className="fas fa-image text-4xl"></i>
                </div>
              </div>
              
              <div className="p-4 flex-grow">
                <h3 
                  className="font-semibold text-lg mb-2 cursor-pointer hover:text-primary-600"
                  onClick={() => navigate(`/marketplace/product/${product.id}`)}
                >
                  {product.name}
                </h3>
                
                <p className="text-sm text-secondary-600 mb-3 line-clamp-2">
                  {product.description}
                </p>
                
                <div className="flex items-center mb-3">
                  <div className="flex text-yellow-400 mr-2">
                    {[1, 2, 3, 4, 5].map(star => (
                      <span key={star}>
                        {product.rating >= star 
                          ? <i className="fas fa-star"></i>
                          : product.rating >= star - 0.5
                            ? <i className="fas fa-star-half-alt"></i>
                            : <i className="far fa-star"></i>
                        }
                      </span>
                    ))}
                  </div>
                  <span className="text-sm text-secondary-500">
                    ({product.rating.toFixed(1)})
                  </span>
                </div>
                
                <div className="flex items-center justify-between mt-auto">
                  <span className="text-xl font-bold">
                    R$ {product.price.toFixed(2)}
                  </span>
                  
                  <Badge 
                    variant={product.stock > 10 ? "success" : product.stock > 0 ? "warning" : "danger"}
                  >
                    {product.stock > 10 
                      ? "Em estoque" 
                      : product.stock > 0 
                        ? `Apenas ${product.stock}` 
                        : "Esgotado"
                    }
                  </Badge>
                </div>
              </div>
              
              <div className="p-4 border-t border-secondary-200">
                <Button
                  variant="primary"
                  className="w-full"
                  disabled={product.stock === 0}
                  onClick={() => addToCart(product)}
                >
                  <i className="fas fa-shopping-cart mr-2"></i>
                  Adicionar ao Carrinho
                </Button>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    );
  };
  
  // Renderizar lista de produtos
  const renderProductList = () => {
    return (
      <Card variant="elevated" className="overflow-hidden">
        <div className="overflow-x-auto">
          <Table>
            <TableHead>
              <TableRow>
                <TableCell isHeader>Produto</TableCell>
                <TableCell isHeader>Categoria</TableCell>
                <TableCell isHeader>Preço</TableCell>
                <TableCell isHeader>Estoque</TableCell>
                <TableCell isHeader>Avaliação</TableCell>
                <TableCell isHeader>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredProducts.map(product => (
                <TableRow key={product.id}>
                  <TableCell>
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-secondary-100 rounded-md mr-3 flex items-center justify-center text-secondary-400">
                        <i className="fas fa-image"></i>
                      </div>
                      <div>
                        <h3 
                          className="font-medium cursor-pointer hover:text-primary-600"
                          onClick={() => navigate(`/marketplace/product/${product.id}`)}
                        >
                          {product.name}
                        </h3>
                        <p className="text-xs text-secondary-500 line-clamp-1">
                          {product.description}
                        </p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge 
                      variant={
                        product.category === 'mangueiras' ? 'info' :
                        product.category === 'conexoes' ? 'success' :
                        product.category === 'adaptadores' ? 'warning' :
                        'secondary'
                      }
                    >
                      {categories.find(c => c.id === product.category)?.name || product.category}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <span className="font-semibold">
                      R$ {product.price.toFixed(2)}
                    </span>
                  </TableCell>
                  <TableCell>
                    <Badge 
                      variant={product.stock > 10 ? "success" : product.stock > 0 ? "warning" : "danger"}
                    >
                      {product.stock > 10 
                        ? "Em estoque" 
                        : product.stock > 0 
                          ? `Apenas ${product.stock}` 
                          : "Esgotado"
                      }
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex text-yellow-400">
                      {[1, 2, 3, 4, 5].map(star => (
                        <span key={star}>
                          {product.rating >= star 
                            ? <i className="fas fa-star"></i>
                            : product.rating >= star - 0.5
                              ? <i className="fas fa-star-half-alt"></i>
                              : <i className="far fa-star"></i>
                          }
                        </span>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="primary"
                      size="sm"
                      disabled={product.stock === 0}
                      onClick={() => addToCart(product)}
                    >
                      <i className="fas fa-shopping-cart mr-1"></i>
                      Adicionar
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </Card>
    );
  };
  
  // Renderizar detalhes do produto
  const renderProductDetails = () => {
    if (!selectedProduct) return null;
    
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="mb-4">
          <Button
            variant="text"
            onClick={() => {
              setSelectedProduct(null);
              navigate('/marketplace');
            }}
          >
            <i className="fas fa-arrow-left mr-2"></i>
            Voltar para produtos
          </Button>
        </div>
        
        <Card variant="elevated" className="overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6">
              <div className="bg-secondary-100 h-80 rounded-lg flex items-center justify-center text-secondary-400">
                <i className="fas fa-image text-6xl"></i>
              </div>
              
              <div className="flex mt-4 space-x-2">
                {[1, 2, 3, 4].map(i => (
                  <div 
                    key={i}
                    className="w-20 h-20 bg-secondary-100 rounded cursor-pointer flex items-center justify-center text-secondary-400"
                  >
                    <i className="fas fa-image"></i>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h1 className="text-2xl font-bold">{selectedProduct.name}</h1>
                {selectedProduct.featured && (
                  <Badge variant="primary">Destaque</Badge>
                )}
              </div>
              
              <div className="flex items-center mb-4">
                <div className="flex text-yellow-400 mr-2">
                  {[1, 2, 3, 4, 5].map(star => (
                    <span key={star} className="text-lg">
                      {selectedProduct.rating >= star 
                        ? <i className="fas fa-star"></i>
                        : selectedProduct.rating >= star - 0.5
                          ? <i className="fas fa-star-half-alt"></i>
                          : <i className="far fa-star"></i>
                      }
                    </span>
                  ))}
                </div>
                <span className="text-secondary-500">
                  ({selectedProduct.rating.toFixed(1)})
                </span>
              </div>
              
              <div className="text-3xl font-bold mb-4">
                R$ {selectedProduct.price.toFixed(2)}
              </div>
              
              <p className="text-secondary-700 mb-6">
                {selectedProduct.description}
              </p>
              
              <div className="mb-6">
                <Badge 
                  variant={
                    selectedProduct.category === 'mangueiras' ? 'info' :
                    selectedProduct.category === 'conexoes' ? 'success' :
                    selectedProduct.category === 'adaptadores' ? 'warning' :
                    'secondary'
                  }
                  className="text-sm"
                >
                  {categories.find(c => c.id === selectedProduct.category)?.name || selectedProduct.category}
                </Badge>
                
                <Badge 
                  variant={selectedProduct.stock > 10 ? "success" : selectedProduct.stock > 0 ? "warning" : "danger"}
                  className="ml-2 text-sm"
                >
                  {selectedProduct.stock > 10 
                    ? "Em estoque" 
                    : selectedProduct.stock > 0 
                      ? `Apenas ${selectedProduct.stock} unidades` 
                      : "Esgotado"
                  }
                </Badge>
              </div>
              
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-32">
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    Quantidade
                  </label>
                  <div className="flex border border-secondary-300 rounded-md overflow-hidden">
                    <button 
                      className="px-3 py-2 bg-secondary-100 text-secondary-700 hover:bg-secondary-200"
                      onClick={() => {
                        const item = cart.find(item => item.product.id === selectedProduct.id);
                        if (item && item.quantity > 1) {
                          updateQuantity(selectedProduct.id, item.quantity - 1);
                        }
                      }}
                    >
                      <i className="fas fa-minus"></i>
                    </button>
                    <div className="flex-1 px-3 py-2 text-center">
                      {cart.find(item => item.product.id === selectedProduct.id)?.quantity || 1}
                    </div>
                    <button 
                      className="px-3 py-2 bg-secondary-100 text-secondary-700 hover:bg-secondary-200"
                      onClick={() => {
                        const item = cart.find(item => item.product.id === selectedProduct.id);
                        if (item) {
                          updateQuantity(selectedProduct.id, item.quantity + 1);
                        }
                      }}
                    >
                      <i className="fas fa-plus"></i>
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3">
                <Button
                  variant="primary"
                  className="flex-1"
                  disabled={selectedProduct.stock === 0}
                  onClick={() => addToCart(selectedProduct)}
                >
                  <i className="fas fa-shopping-cart mr-2"></i>
                  Adicionar ao Carrinho
                </Button>
                
                <Button
                  variant="outline"
                  className="flex-1"
                >
                  <i className="fab fa-whatsapp mr-2 text-green-500"></i>
                  Consultar via WhatsApp
                </Button>
              </div>
            </div>
          </div>
        </Card>
      </motion.div>
    );
  };
  
  // Renderizar carrinho
  const renderCart = () => {
    return (
      <motion.div
        initial={{ opacity: 0, x: 300 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 300 }}
        className="fixed inset-y-0 right-0 w-full sm:w-96 bg-white shadow-xl z-50 flex flex-col"
      >
        <div className="p-4 border-b border-secondary-200 flex justify-between items-center">
          <h2 className="text-xl font-bold">Carrinho de Compras</h2>
          <button 
            className="text-secondary-500 hover:text-secondary-700"
            onClick={() => setShowCart(false)}
          >
            <i className="fas fa-times text-xl"></i>
          </button>
        </div>
        
        <div className="flex-grow overflow-y-auto p-4">
          {cart.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-secondary-400 text-5xl mb-4">
                <i className="fas fa-shopping-cart"></i>
              </div>
              <h3 className="text-xl font-medium text-secondary-700 mb-2">Seu carrinho está vazio</h3>
              <p className="text-secondary-500 mb-4">
                Adicione produtos ao carrinho para continuar.
              </p>
              <Button 
                variant="primary"
                onClick={() => setShowCart(false)}
              >
                Continuar Comprando
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              {cart.map(item => (
                <Card key={item.product.id} variant="bordered" className="p-3">
                  <div className="flex">
                    <div className="w-20 h-20 bg-secondary-100 rounded flex items-center justify-center text-secondary-400 mr-3">
                      <i className="fas fa-image"></i>
                    </div>
                    
                    <div className="flex-grow">
                      <div className="flex justify-between">
                        <h3 className="font-medium">{item.product.name}</h3>
                        <button 
                          className="text-secondary-400 hover:text-red-500"
                          onClick={() => removeFromCart(item.product.id)}
                        >
                          <i className="fas fa-trash-alt"></i>
                        </button>
                      </div>
                      
                      <p className="text-sm text-secondary-500 mb-2">
                        R$ {item.product.price.toFixed(2)}
                      </p>
                      
                      <div className="flex justify-between items-center">
                        <div className="flex border border-secondary-300 rounded-md overflow-hidden">
                          <button 
                            className="px-2 py-1 bg-secondary-100 text-secondary-700 hover:bg-secondary-200"
                            onClick={() => {
                              if (item.quantity > 1) {
                                updateQuantity(item.product.id, item.quantity - 1);
                              }
                            }}
                          >
                            <i className="fas fa-minus"></i>
                          </button>
                          <div className="w-8 px-2 py-1 text-center">
                            {item.quantity}
                          </div>
                          <button 
                            className="px-2 py-1 bg-secondary-100 text-secondary-700 hover:bg-secondary-200"
                            onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                          >
                            <i className="fas fa-plus"></i>
                          </button>
                        </div>
                        
                        <div className="font-semibold">
                          R$ {(item.product.price * item.quantity).toFixed(2)}
                        </div>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
        
        {cart.length > 0 && (
          <div className="p-4 border-t border-secondary-200">
            <div className="flex justify-between mb-4">
              <span className="font-medium">Subtotal:</span>
              <span className="font-bold">R$ {cartTotal.toFixed(2)}</span>
            </div>
            
            <Button
              variant="primary"
              className="w-full mb-2"
              onClick={goToCheckout}
            >
              Finalizar Compra
            </Button>
            
            <Button
              variant="text"
              className="w-full"
              onClick={() => setShowCart(false)}
            >
              Continuar Comprando
            </Button>
          </div>
        )}
      </motion.div>
    );
  };
  
  // Se estiver visualizando detalhes do produto
  if (selectedProduct) {
    return (
      <div className="container mx-auto px-4 py-8">
        {renderProductDetails()}
        {showCart && renderCart()}
        
        <div className="fixed bottom-4 right-4 z-40">
          <Button
            variant="primary"
            className="rounded-full w-14 h-14 flex items-center justify-center shadow-lg relative"
            onClick={() => setShowCart(true)}
          >
            <i className="fas fa-shopping-cart text-xl"></i>
            {cart.length > 0 && (
              <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
                {cart.reduce((total, item) => total + item.quantity, 0)}
              </span>
            )}
          </Button>
        </div>
      </div>
    );
  }
  
  // Página principal do marketplace
  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <h1 className="text-3xl font-bold mb-4 md:mb-0">Marketplace Mangueiras Terman</h1>
          
          <div className="flex items-center space-x-3">
            <Button
              variant="outline"
              onClick={() => navigate('/')}
            >
              <i className="fas fa-home mr-2"></i>
              Página Inicial
            </Button>
            
            <Button
              variant="primary"
              onClick={() => setShowCart(true)}
              className="relative"
            >
              <i className="fas fa-shopping-cart mr-2"></i>
              Carrinho
              {cart.length > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
                  {cart.reduce((total, item) => total + item.quantity, 0)}
                </span>
              )}
            </Button>
          </div>
        </div>
        
        {/* Banner promocional */}
        <div className="mb-8 bg-gradient-to-r from-primary-500 to-primary-700 rounded-lg shadow-lg overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2">
            <div className="p-8 flex flex-col justify-center">
              <h2 className="text-white text-3xl font-bold mb-4">
                Produtos de Alta Qualidade para Sua Indústria
              </h2>
              <p className="text-white text-opacity-90 mb-6">
                Mangueiras, conexões e acessórios com os melhores preços e garantia de qualidade.
              </p>
              <div>
                <Button
                  variant="light"
                  className="mr-3"
                >
                  Ver Ofertas
                </Button>
                <Button
                  variant="outline"
                  className="text-white border-white hover:bg-white hover:text-primary-700"
                >
                  Solicitar Orçamento
                </Button>
              </div>
            </div>
            <div className="hidden md:flex items-center justify-center p-8">
              <div className="w-full h-64 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                <i className="fas fa-industry text-white text-opacity-80 text-8xl"></i>
              </div>
            </div>
          </div>
        </div>
        
        {/* Filtros e Controles */}
        <div className="mb-8 bg-white rounded-lg shadow-sm p-4">
          <div className="flex flex-col md:flex-row md:items-center gap-4">
            <div className="md:w-1/3">
              <label className="block text-sm font-medium text-secondary-700 mb-1">Buscar</label>
              <div className="relative">
                <input
                  type="text"
                  className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Nome ou descrição do produto..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i className="fas fa-search text-secondary-400"></i>
                </div>
              </div>
            </div>
            
            <div className="md:w-1/3">
              <label className="block text-sm font-medium text-secondary-700 mb-1">Categoria</label>
              <select
                className="w-full px-4 py-2 border border-secondary-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="md:w-1/3">
              <label className="block text-sm font-medium text-secondary-700 mb-1">Visualização</label>
              <div className="flex border border-secondary-300 rounded-md overflow-hidden">
                <button
                  className={`flex-1 py-2 px-4 ${
                    viewMode === 'grid' 
                      ? 'bg-primary-500 text-white' 
                      : 'bg-white text-secondary-700 hover:bg-secondary-50'
                  }`}
                  onClick={() => setViewMode('grid')}
                >
                  <i className="fas fa-th-large mr-2"></i>
                  Grid
                </button>
                <button
                  className={`flex-1 py-2 px-4 ${
                    viewMode === 'list' 
                      ? 'bg-primary-500 text-white' 
                      : 'bg-white text-secondary-700 hover:bg-secondary-50'
                  }`}
                  onClick={() => setViewMode('list')}
                >
                  <i className="fas fa-list mr-2"></i>
                  Lista
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Produtos em destaque */}
        {selectedCategory === 'all' && searchTerm === '' && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Produtos em Destaque</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {products.filter(p => p.featured).map(product => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <Card
                    variant="elevated"
                    className="h-full flex flex-col overflow-hidden transition-transform hover:scale-105"
                  >
                    <div className="absolute top-2 right-2 z-10">
                      <Badge variant="primary">Destaque</Badge>
                    </div>
                    
                    <div 
                      className="h-48 bg-secondary-100 relative cursor-pointer"
                      onClick={() => navigate(`/marketplace/product/${product.id}`)}
                    >
                      <div className="absolute inset-0 flex items-center justify-center text-secondary-400">
                        <i className="fas fa-image text-4xl"></i>
                      </div>
                    </div>
                    
                    <div className="p-4 flex-grow">
                      <h3 
                        className="font-semibold text-lg mb-2 cursor-pointer hover:text-primary-600"
                        onClick={() => navigate(`/marketplace/product/${product.id}`)}
                      >
                        {product.name}
                      </h3>
                      
                      <p className="text-sm text-secondary-600 mb-3 line-clamp-2">
                        {product.description}
                      </p>
                      
                      <div className="flex items-center mb-3">
                        <div className="flex text-yellow-400 mr-2">
                          {[1, 2, 3, 4, 5].map(star => (
                            <span key={star}>
                              {product.rating >= star 
                                ? <i className="fas fa-star"></i>
                                : product.rating >= star - 0.5
                                  ? <i className="fas fa-star-half-alt"></i>
                                  : <i className="far fa-star"></i>
                              }
                            </span>
                          ))}
                        </div>
                        <span className="text-sm text-secondary-500">
                          ({product.rating.toFixed(1)})
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between mt-auto">
                        <span className="text-xl font-bold">
                          R$ {product.price.toFixed(2)}
                        </span>
                        
                        <Badge 
                          variant={product.stock > 10 ? "success" : product.stock > 0 ? "warning" : "danger"}
                        >
                          {product.stock > 10 
                            ? "Em estoque" 
                            : product.stock > 0 
                              ? `Apenas ${product.stock}` 
                              : "Esgotado"
                          }
                        </Badge>
                      </div>
                    </div>
                    
                    <div className="p-4 border-t border-secondary-200">
                      <Button
                        variant="primary"
                        className="w-full"
                        disabled={product.stock === 0}
                        onClick={() => addToCart(product)}
                      >
                        <i className="fas fa-shopping-cart mr-2"></i>
                        Adicionar ao Carrinho
                      </Button>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        )}
        
        {/* Lista de Produtos */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">
            {selectedCategory === 'all' 
              ? 'Todos os Produtos' 
              : categories.find(c => c.id === selectedCategory)?.name || 'Produtos'
            }
            {searchTerm && ` - Resultados para "${searchTerm}"`}
            {` (${filteredProducts.length})`}
          </h2>
          
          {filteredProducts.length === 0 ? (
            <Card variant="elevated" className="p-8 text-center">
              <div className="text-secondary-400 text-5xl mb-4">
                <i className="fas fa-search"></i>
              </div>
              <h3 className="text-xl font-medium text-secondary-700 mb-2">Nenhum produto encontrado</h3>
              <p className="text-secondary-500 mb-4">
                Tente ajustar os filtros ou buscar por outros termos.
              </p>
              <Button 
                variant="primary"
                onClick={() => {
                  setSearchTerm('');
                  setSelectedCategory('all');
                }}
              >
                Limpar Filtros
              </Button>
            </Card>
          ) : (
            viewMode === 'grid' ? renderProductGrid() : renderProductList()
          )}
        </div>
      </motion.div>
      
      {showCart && renderCart()}
      
      <div className="fixed bottom-4 right-4 z-40">
        <Button
          variant="primary"
          className="rounded-full w-14 h-14 flex items-center justify-center shadow-lg relative"
          onClick={() => setShowCart(true)}
        >
          <i className="fas fa-shopping-cart text-xl"></i>
          {cart.length > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
              {cart.reduce((total, item) => total + item.quantity, 0)}
            </span>
          )}
        </Button>
      </div>
    </div>
  );
};

export default MarketplacePage;
