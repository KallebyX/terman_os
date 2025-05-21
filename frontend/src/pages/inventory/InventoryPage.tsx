import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';
import { ProductForm } from './components/ProductForm';
import { ProductList } from './components/ProductList';
import { StockMovement } from './components/StockMovement';
import { ConfirmDialog } from '../../components/shared/ConfirmDialog';
import { LoadingSpinner } from '../../components/shared/LoadingSpinner';
import { ErrorMessage } from '../../components/shared/ErrorMessage';
import { useProducts } from '../../hooks/useProducts';
import { Product } from '../../types';

interface Product {
  id: string;
  name: string;
  code: string;
  description: string;
  category: string;
  price: number;
  cost: number;
  stock: number;
  minStock: number;
  supplier: string;
  barcode: string;
  lastUpdate: string;
}

interface Supplier {
  id: string;
  name: string;
  contact: string;
  phone: string;
}

const InventoryPage = () => {
  const {
    products,
    isLoading,
    error,
    createProduct,
    updateProduct,
    deleteProduct
  } = useProducts();

  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [showProductForm, setShowProductForm] = useState(false);
  const [showStockMovement, setShowStockMovement] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleProductSubmit = async (data: Partial<Product>) => {
    try {
      if (selectedProduct) {
        await updateProduct(selectedProduct.id, data);
      } else {
        await createProduct(data);
      }
      setShowProductForm(false);
      setSelectedProduct(null);
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleStockMovement = async (quantity: number, type: 'add' | 'remove') => {
    if (!selectedProduct) return;

    try {
      const newStock = type === 'add'
        ? selectedProduct.stock + quantity
        : selectedProduct.stock - quantity;

      await updateProduct(selectedProduct.id, { stock: newStock });
      setSelectedProduct(null);
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleDelete = async () => {
    if (!selectedProduct) return;

    try {
      await deleteProduct(selectedProduct.id);
      setShowDeleteConfirm(false);
      setSelectedProduct(null);
    } catch (error: any) {
      alert(error.message);
    }
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <h1 className="text-2xl font-bold mb-4 md:mb-0">Controle de Estoque</h1>
          
          <div className="flex flex-col sm:flex-row gap-3">
            <Button onClick={() => setShowProductForm(true)}>
              <i className="fas fa-plus mr-2"></i>
              Novo Produto
            </Button>
            <Button variant="outline">
              <i className="fas fa-building mr-2"></i>
              Fornecedores
            </Button>
            <Button variant="primary">
              <i className="fas fa-file-export mr-2"></i>
              Exportar
            </Button>
          </div>
        </div>
        
        {/* Alertas */}
        {products.filter(isLowStock).length > 0 && (
          <Card variant="bordered" className="mb-6 p-4 bg-yellow-50 border-yellow-200">
            <div className="flex items-start">
              <div className="text-yellow-500 mr-3">
                <i className="fas fa-exclamation-triangle text-xl"></i>
              </div>
              <div>
                <h3 className="font-semibold text-yellow-800 mb-1">Alerta de Estoque Baixo</h3>
                <p className="text-yellow-700 mb-2">
                  {products.filter(isLowStock).length} produtos estão com estoque abaixo do mínimo recomendado.
                </p>
                <Button variant="link" size="sm" className="text-yellow-700">
                  Ver Detalhes
                </Button>
              </div>
            </div>
          </Card>
        )}
        
        {/* Filtros e Controles */}
        <div className="mb-6 bg-white rounded-lg shadow-sm p-4">
          <div className="flex flex-col md:flex-row md:items-center gap-4">
            <div className="md:w-1/3">
              <label className="block text-sm font-medium text-secondary-700 mb-1">Buscar</label>
              <div className="relative">
                <input
                  type="text"
                  className="w-full pl-10 pr-4 py-2 border border-secondary-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Nome, código ou descrição..."
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
                    viewMode === 'cards' 
                      ? 'bg-primary-500 text-white' 
                      : 'bg-white text-secondary-700 hover:bg-secondary-50'
                  }`}
                  onClick={() => setViewMode('cards')}
                >
                  <i className="fas fa-th-large mr-2"></i>
                  Cards
                </button>
                <button
                  className={`flex-1 py-2 px-4 ${
                    viewMode === 'table' 
                      ? 'bg-primary-500 text-white' 
                      : 'bg-white text-secondary-700 hover:bg-secondary-50'
                  }`}
                  onClick={() => setViewMode('table')}
                >
                  <i className="fas fa-table mr-2"></i>
                  Tabela
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          <Card variant="elevated" className="p-4">
            <h3 className="text-sm font-medium text-secondary-500 mb-1">Total de Produtos</h3>
            <p className="text-2xl font-bold mb-2">{products.length}</p>
            <div className="flex items-center text-sm">
              <span className="text-green-500 mr-1">
                <i className="fas fa-arrow-up"></i>
              </span>
              <span>2 novos este mês</span>
            </div>
          </Card>
          
          <Card variant="elevated" className="p-4">
            <h3 className="text-sm font-medium text-secondary-500 mb-1">Valor em Estoque</h3>
            <p className="text-2xl font-bold mb-2">
              R$ {products.reduce((sum, p) => sum + (p.price * p.stock), 0).toFixed(2)}
            </p>
            <div className="flex items-center text-sm">
              <span className="text-green-500 mr-1">
                <i className="fas fa-chart-line"></i>
              </span>
              <span>Valor atualizado</span>
            </div>
          </Card>
          
          <Card variant="elevated" className="p-4">
            <h3 className="text-sm font-medium text-secondary-500 mb-1">Categorias</h3>
            <p className="text-2xl font-bold mb-2">{categories.length - 1}</p>
            <div className="flex items-center text-sm">
              <span className="text-blue-500 mr-1">
                <i className="fas fa-tag"></i>
              </span>
              <span>Produtos categorizados</span>
            </div>
          </Card>
          
          <Card variant="elevated" className="p-4">
            <h3 className="text-sm font-medium text-secondary-500 mb-1">Fornecedores</h3>
            <p className="text-2xl font-bold mb-2">{suppliers.length}</p>
            <div className="flex items-center text-sm">
              <span className="text-purple-500 mr-1">
                <i className="fas fa-building"></i>
              </span>
              <span>Parceiros ativos</span>
            </div>
          </Card>
        </div>
        
        {/* Lista de Produtos */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Produtos ({filteredProducts.length})</h2>
          
          {filteredProducts.length === 0 ? (
            <Card variant="elevated" className="p-8 text-center">
              <div className="text-secondary-400 text-5xl mb-4">
                <i className="fas fa-search"></i>
              </div>
              <h3 className="text-xl font-medium text-secondary-700 mb-2">Nenhum produto encontrado</h3>
              <p className="text-secondary-500 mb-4">
                Tente ajustar os filtros ou adicione novos produtos ao estoque.
              </p>
              <Button variant="primary">
                <i className="fas fa-plus mr-2"></i>
                Adicionar Produto
              </Button>
            </Card>
          ) : (
            viewMode === 'cards' ? renderProductCards() : renderProductTable()
          )}
        </div>
        
        {/* Fornecedores */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Fornecedores</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {suppliers.map(supplier => (
              <Card key={supplier.id} variant="elevated" className="p-4">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-semibold">{supplier.name}</h3>
                  <button className="text-secondary-500 hover:text-secondary-700" title="Mais opções">
                    <i className="fas fa-ellipsis-v"></i>
                  </button>
                </div>
                
                <div className="mb-3">
                  <p className="text-xs text-secondary-500 mb-1">Contato</p>
                  <p className="text-sm">{supplier.contact}</p>
                </div>
                
                <div className="mb-3">
                  <p className="text-xs text-secondary-500 mb-1">Telefone</p>
                  <p className="text-sm">{supplier.phone}</p>
                </div>
                
                <div className="flex justify-between items-center mt-4">
                  <Button variant="link" size="sm" className="text-secondary-700">
                    <i className="fas fa-file-alt mr-1"></i>
                    Cotações
                  </Button>
                  
                  <Button variant="outline" size="sm">
                    <i className="fas fa-phone-alt mr-1"></i>
                    Contatar
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </motion.div>

      <ProductForm
        isOpen={showProductForm}
        onClose={() => {
          setShowProductForm(false);
          setSelectedProduct(null);
        }}
        onSubmit={handleProductSubmit}
        initialValues={selectedProduct || undefined}
      />

      <StockMovement
        product={selectedProduct}
        isOpen={showStockMovement}
        onClose={() => {
          setShowStockMovement(false);
          setSelectedProduct(null);
        }}
        onConfirm={handleStockMovement}
      />

      <ConfirmDialog
        isOpen={showDeleteConfirm}
        onClose={() => {
          setShowDeleteConfirm(false);
          setSelectedProduct(null);
        }}
        onConfirm={handleDelete}
        title="Excluir Produto"
        message={`Tem certeza que deseja excluir o produto ${selectedProduct?.name}?`}
      />
    </div>
  );
};

export default InventoryPage;
