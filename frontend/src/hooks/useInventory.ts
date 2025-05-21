import { useState, useEffect, useCallback } from 'react';
import { productService } from '../services/productService';
import { useToast } from '../components/ui/Toast';

export const useInventory = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lowStockProducts, setLowStockProducts] = useState([]);
  const { addToast } = useToast();

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      const [productsData, lowStockData] = await Promise.all([
        productService.list(),
        productService.getLowStock()
      ]);
      setProducts(productsData);
      setLowStockProducts(lowStockData);
    } catch (error) {
      addToast('Erro ao carregar produtos', 'error');
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const updateStock = async (
    productId: string,
    quantity: number,
    type: 'add' | 'remove',
    reason: string
  ) => {
    try {
      const updatedProduct = await productService.updateStock(
        productId,
        quantity,
        type,
        reason
      );
      setProducts(prev => prev.map(product =>
        product.id === productId ? updatedProduct : product
      ));
      addToast('Estoque atualizado com sucesso!', 'success');
      return updatedProduct;
    } catch (error) {
      addToast('Erro ao atualizar estoque', 'error');
      throw error;
    }
  };

  return {
    products,
    loading,
    lowStockProducts,
    updateStock,
    refetch: fetchProducts
  };
}; 