import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { Badge } from '../../components/ui/Badge';
import { ProductCard } from './components/ProductCard';
import { CartDrawer } from './components/CartDrawer';
import { ProductFilters } from './components/ProductFilters';
import { LoadingSpinner } from '../../components/shared/LoadingSpinner';
import { ErrorMessage } from '../../components/shared/ErrorMessage';
import { useProducts } from '../../hooks/useProducts';
import { Product } from '../../types';

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
  const { products, isLoading, error } = useProducts();
  
  // Estados
  const [cartItems, setCartItems] = useState<Array<Product & { quantity: number }>>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(0);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  
  // Categorias
  const categories = [...new Set(products.map(p => p.category))];
  
  // Filtrar produtos
  const filteredProducts = products.filter(product => {
    const matchesCategory = !selectedCategory || product.category === selectedCategory;
    const matchesSearch = !searchTerm || 
      product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPrice = (!minPrice || product.price >= minPrice) &&
      (!maxPrice || product.price <= maxPrice);

    return matchesCategory && matchesSearch && matchesPrice;
  });
  
  // Adicionar ao carrinho
  const handleAddToCart = (product: Product) => {
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
    setIsCartOpen(true);
  };
  
  // Remover do carrinho
  const handleRemoveItem = (productId: number) => {
    setCartItems(prev => prev.filter(item => item.id !== productId));
  };
  
  // Atualizar quantidade no carrinho
  const handleUpdateQuantity = (productId: number, quantity: number) => {
    if (quantity < 1) return;
    setCartItems(prev =>
      prev.map(item =>
        item.id === productId ? { ...item, quantity } : item
      )
    );
  };
  
  // Calcular total do carrinho
  const cartTotal = cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  
  // Ir para o checkout
  const handleCheckout = () => {
    // Implementar checkout
    navigate('/checkout', { state: { items: cartItems } });
  };
  
  // Renderizar grid de produtos
  const renderProductGrid = () => {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredProducts.map(product => (
          <ProductCard
            key={product.id}
            product={product}
            onAddToCart={handleAddToCart}
          />
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
                      {categories.find(c => c === product.category)?.name || product.category}
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
                      onClick={() => handleAddToCart(product)}
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
                  {categories.find(c => c === selectedProduct.category)?.name || selectedProduct.category}
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
                        const item = cartItems.find(item => item.id === selectedProduct.id);
                        if (item && item.quantity > 1) {
                          handleUpdateQuantity(selectedProduct.id, item.quantity - 1);
                        }
                      }}
                    >
                      <i className="fas fa-minus"></i>
                    </button>
                    <div className="flex-1 px-3 py-2 text-center">
                      {cartItems.find(item => item.id === selectedProduct.id)?.quantity || 1}
                    </div>
                    <button 
                      className="px-3 py-2 bg-secondary-100 text-secondary-700 hover:bg-secondary-200"
                      onClick={() => {
                        const item = cartItems.find(item => item.id === selectedProduct.id);
                        if (item) {
                          handleUpdateQuantity(selectedProduct.id, item.quantity + 1);
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
                  onClick={() => handleAddToCart(selectedProduct)}
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
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

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
              onClick={() => setIsCartOpen(true)}
              className="relative"
            >
              <i className="fas fa-shopping-cart mr-2"></i>
              Carrinho
              {cartItems.length > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
                  {cartItems.reduce((total, item) => total + item.quantity, 0)}
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
              <ProductFilters
                categories={categories}
                selectedCategory={selectedCategory}
                onCategoryChange={setSelectedCategory}
                searchTerm={searchTerm}
                onSearchChange={setSearchTerm}
                minPrice={minPrice}
                maxPrice={maxPrice}
                onPriceChange={(min, max) => {
                  setMinPrice(min);
                  setMaxPrice(max);
                }}
              />
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
                        onClick={() => handleAddToCart(product)}
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
              : categories.find(c => c === selectedCategory)?.name || 'Produtos'
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
      
      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        items={cartItems}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveItem}
        onCheckout={handleCheckout}
      />
    </div>
  );
};

export default MarketplacePage;
