import { api } from '../config/api';
import { Product } from '../types/common';

export const productService = {
  async list() {
    const response = await api.get('/products');
    return response.data;
  },

  async getById(id: string) {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  async create(data: Omit<Product, 'id'>) {
    const response = await api.post('/products', data);
    return response.data;
  },

  async update(id: string, data: Partial<Product>) {
    const response = await api.put(`/products/${id}`, data);
    return response.data;
  },

  async delete(id: string) {
    await api.delete(`/products/${id}`);
  },

  async updateStock(id: string, quantity: number, type: 'add' | 'remove', reason: string) {
    const response = await api.post(`/products/${id}/stock`, {
      quantity,
      type,
      reason
    });
    return response.data;
  },

  async getStockHistory(id: string) {
    const response = await api.get(`/products/${id}/stock-history`);
    return response.data;
  },

  async getLowStock() {
    const response = await api.get('/products/low-stock');
    return response.data;
  }
}; 