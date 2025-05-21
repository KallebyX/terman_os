import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { motion } from 'framer-motion';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Table, TableHead, TableBody, TableRow, TableCell } from '../../components/ui/Table';

const InventoryPage = () => {
  // Estados
  const [searchTerm, setSearchTerm] = React.useState('');
  const [selectedCategory, setSelectedCategory] = React.useState('all');
  const [viewMode, setViewMode] = React.useState('cards'); // 'cards' ou 'table'
  
  // Estados para dados reais
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await api.get('/api/products');
        
        if (response.data && (response.data.results || Array.isArray(response.data))) {
          setProducts(response.data.results || response.data);
        } else {
          console.error('Formato de resposta inesperado:', response.data);
          alert('Erro no formato dos dados recebidos do servidor.');
        }
      } catch (error) {
        console.error('Erro ao buscar produtos:', error);
        // Mostrar mensagem de erro para o usuário
        alert('Não foi possível carregar os produtos. Por favor, tente novamente mais tarde.');
      }
    };

    fetchProducts();
  }, []);
  
  // Estados para categorias e fornecedores
  const [categories, setCategories] = useState([]);
  const [suppliers, setSuppliers] = useState([]);

  useEffect(() => {
    const fetchCategoriesAndSuppliers = async () => {
      try {
        const [categoriesResponse, suppliersResponse] = await Promise.all([
          api.get('/api/categories'),
          api.get('/api/suppliers')
        ]);
        
        // Verificar e processar dados de categorias
        if (categoriesResponse.data && (categoriesResponse.data.results || Array.isArray(categoriesResponse.data))) {
          setCategories(categoriesResponse.data.results || categoriesResponse.data);
        } else {
          console.error('Formato de resposta inesperado para categorias:', categoriesResponse.data);
        }
        
        // Verificar e processar dados de fornecedores
        if (suppliersResponse.data && (suppliersResponse.data.results || Array.isArray(suppliersResponse.data))) {
          setSuppliers(suppliersResponse.data.results || suppliersResponse.data);
        } else {
          console.error('Formato de resposta inesperado para fornecedores:', suppliersResponse.data);
        }
      } catch (error) {
        console.error('Erro ao buscar categorias e fornecedores:', error);
        // Mostrar mensagem de erro para o usuário
        alert('Não foi possível carregar categorias e fornecedores. Por favor, tente novamente mais tarde.');
      }
    };

    fetchCategoriesAndSuppliers();
  }, []);
  
  // Filtrar produtos
  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         product.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  });
  
  // Verificar estoque baixo
  const isLowStock = (product) => product.stock < product.minStock;
  
  // Renderizar cards de produtos
  const renderProductCards = () => {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredProducts.map(product => (
          <Card
            key={product.id}
            variant="elevated"
            className="overflow-hidden transition-transform hover:scale-105"
          >
            <div className="p-4 border-b border-secondary-200 flex justify-between items-center">
              <h3 className="font-semibold">{product.name}</h3>
              <span className="text-xs bg-secondary-100 text-secondary-800 px-2 py-1 rounded">
                {product.code}
              </span>
            </div>
            <div className="p-4">
              <p className="text-sm text-secondary-600 mb-3">{product.description}</p>
              
              <div className="grid grid-cols-2 gap-2 mb-3">
                <div>
                  <p className="text-xs text-secondary-500">Preço</p>
                  <p className="font-semibold">R$ {product.price.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-xs text-secondary-500">Custo</p>
                  <p className="font-semibold">R$ {product.cost.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-xs text-secondary-500">Estoque</p>
                  <p className={`font-semibold ${isLowStock(product) ? 'text-red-600' : 'text-green-600'}`}>
                    {product.stock} un
                  </p>
                </div>
                <div>
                  <p className="text-xs text-secondary-500">Mínimo</p>
                  <p className="font-semibold">{product.minStock} un</p>
                </div>
              </div>
              
              <div className="mb-3">
                <p className="text-xs text-secondary-500">Fornecedor</p>
                <p className="text-sm">{product.supplier}</p>
              </div>
              
              <div className="mb-3">
                <p className="text-xs text-secondary-500">Código de Barras</p>
                <p className="text-sm font-mono">{product.barcode}</p>
              </div>
              
              <div className="flex justify-between items-center text-xs text-secondary-500">
                <span>Atualizado: {product.lastUpdate}</span>
                <span className={`px-2 py-1 rounded-full ${
                  product.category === 'mangueiras' ? 'bg-blue-100 text-blue-800' :
                  product.category === 'conexoes' ? 'bg-green-100 text-green-800' :
                  product.category === 'adaptadores' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-purple-100 text-purple-800'
                }`}>
                  {categories.find(c => c.id === product.category)?.name || product.category}
                </span>
              </div>
              
              <div className="mt-4 flex space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1"
                >
                  Editar
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  className="flex-1"
                >
                  Movimentar
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    );
  };
  
  // Renderizar tabela de produtos
  const renderProductTable = () => {
    return (
      <Card variant="elevated" className="overflow-hidden">
        <div className="overflow-x-auto">
          <Table>
            <TableHead>
              <TableRow>
                <TableCell isHeader>Código</TableCell>
                <TableCell isHeader>Nome</TableCell>
                <TableCell isHeader>Categoria</TableCell>
                <TableCell isHeader>Estoque</TableCell>
                <TableCell isHeader>Preço</TableCell>
                <TableCell isHeader>Fornecedor</TableCell>
                <TableCell isHeader>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredProducts.map(product => (
                <TableRow key={product.id}>
                  <TableCell>{product.code}</TableCell>
                  <TableCell>{product.name}</TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      product.category === 'mangueiras' ? 'bg-blue-100 text-blue-800' :
                      product.category === 'conexoes' ? 'bg-green-100 text-green-800' :
                      product.category === 'adaptadores' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-purple-100 text-purple-800'
                    }`}>
                      {categories.find(c => c.id === product.category)?.name || product.category}
                    </span>
                  </TableCell>
                  <TableCell>
                    <span className={isLowStock(product) ? 'text-red-600 font-medium' : ''}>
                      {product.stock} / {product.minStock}
                    </span>
                  </TableCell>
                  <TableCell>R$ {product.price.toFixed(2)}</TableCell>
                  <TableCell>{product.supplier}</TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <button className="text-secondary-500 hover:text-secondary-700" title="Editar produto">
                        <i className="fas fa-edit"></i>
                      </button>
                      <button className="text-secondary-500 hover:text-secondary-700" title="Movimentar produto">
                        <i className="fas fa-exchange-alt"></i>
                      </button>
                      <button className="text-secondary-500 hover:text-secondary-700" title="Histórico de produto">
                        <i className="fas fa-history"></i>
                      </button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </Card>
    );
  };
  
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
            <Button variant="outline">
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
                <Button variant="text" size="sm" className="text-yellow-700">
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
                title="Selecionar categoria"
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
                  <Button variant="text" size="sm" className="text-secondary-700">
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
    </div>
  );
};

export default InventoryPage;
