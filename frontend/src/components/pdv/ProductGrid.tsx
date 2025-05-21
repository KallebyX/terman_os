import React, { useState, useEffect } from 'react';
import { useProducts } from '../../hooks/useProducts';
import { Card, Input, Select } from '../ui';
import { Product } from '../../types/pdv';
import { formatCurrency } from '../../utils/formatters';

interface ProductGridProps {
    onProductSelect: (product: Product) => void;
}

export const ProductGrid: React.FC<ProductGridProps> = ({ onProductSelect }) => {
    const [search, setSearch] = useState('');
    const [category, setCategory] = useState('all');
    const { products, categories, loading, error } = useProducts();
    const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);

    useEffect(() => {
        let filtered = products;
        
        if (search) {
            filtered = filtered.filter(product => 
                product.name.toLowerCase().includes(search.toLowerCase()) ||
                product.code.toLowerCase().includes(search.toLowerCase())
            );
        }

        if (category !== 'all') {
            filtered = filtered.filter(product => 
                product.category === category
            );
        }

        setFilteredProducts(filtered);
    }, [search, category, products]);

    return (
        <div className="space-y-4">
            <div className="flex gap-4">
                <Input
                    placeholder="Buscar produto..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="flex-1"
                />
                <Select
                    value={category}
                    onChange={(value) => setCategory(value)}
                    options={[
                        { value: 'all', label: 'Todas Categorias' },
                        ...categories.map(cat => ({
                            value: cat.id,
                            label: cat.name
                        }))
                    ]}
                    className="w-48"
                />
            </div>

            {loading ? (
                <div className="flex justify-center items-center h-64">
                    <span>Carregando produtos...</span>
                </div>
            ) : error ? (
                <div className="text-red-600 text-center">
                    Erro ao carregar produtos
                </div>
            ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {filteredProducts.map(product => (
                        <Card
                            key={product.id}
                            className="p-4 cursor-pointer hover:shadow-lg transition-shadow"
                            onClick={() => onProductSelect(product)}
                        >
                            {product.image && (
                                <img
                                    src={product.image}
                                    alt={product.name}
                                    className="w-full h-32 object-cover mb-2 rounded"
                                />
                            )}
                            <h3 className="font-medium truncate">{product.name}</h3>
                            <p className="text-sm text-gray-500 mb-2">
                                Código: {product.code}
                            </p>
                            <div className="flex justify-between items-center">
                                <span className="text-lg font-bold text-green-600">
                                    {formatCurrency(product.price)}
                                </span>
                                <span className={`text-sm ${
                                    product.stock_quantity > product.min_stock
                                        ? 'text-green-600'
                                        : 'text-red-600'
                                }`}>
                                    Estoque: {product.stock_quantity}
                                </span>
                            </div>
                        </Card>
                    ))}
                </div>
            )}

            {filteredProducts.length === 0 && !loading && (
                <div className="text-center text-gray-500 py-8">
                    Nenhum produto encontrado
                </div>
            )}
        </div>
    );
}; 