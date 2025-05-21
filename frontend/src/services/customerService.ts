import { api } from '../config/api';
import { Customer } from '../types/common';

export const customerService = {
  async list() {
    const response = await api.get('/customers');
    return response.data;
  },

  async getById(id: string) {
    const response = await api.get(`/customers/${id}`);
    return response.data;
  },

  async create(data: Omit<Customer, 'id'>) {
    const response = await api.post('/customers', data);
    return response.data;
  },

  async update(id: string, data: Partial<Customer>) {
    const response = await api.put(`/customers/${id}`, data);
    return response.data;
  },

  async delete(id: string) {
    await api.delete(`/customers/${id}`);
  },

  async getPurchaseHistory(id: string) {
    const response = await api.get(`/customers/${id}/purchases`);
    return response.data;
  },

  async getTopCustomers() {
    const response = await api.get('/customers/top');
    return response.data;
  }
}; 