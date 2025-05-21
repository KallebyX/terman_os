import { useState, useEffect } from 'react';
import { Product } from '../types/common';
import { api } from '../services/api';

export const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await api.get('/products');
      setProducts(response.data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar produtos');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const addProduct = async (product: Omit<Product, 'id' | 'createdAt' | 'updatedAt'>) => {
    const response = await api.post('/products', product);
    setProducts(prev => [...prev, response.data]);
    return response.data;
  };

  const updateProduct = async (id: string, data: Partial<Product>) => {
    const response = await api.put(`/products/${id}`, data);
    setProducts(prev => prev.map(p => p.id === id ? response.data : p));
    return response.data;
  };

  const deleteProduct = async (id: string) => {
    await api.delete(`/products/${id}`);
    setProducts(prev => prev.filter(p => p.id !== id));
  };

  return {
    products,
    loading,
    error,
    addProduct,
    updateProduct,
    deleteProduct,
    refetch: fetchProducts
  };
}; 