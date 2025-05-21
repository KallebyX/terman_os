import { AxiosInstance } from 'axios';
import { Order, OrderItem, PaymentMethod } from '../../types/pdv';

export class PDVService {
    constructor(private axios: AxiosInstance) {}

    async createOrder(data: {
        items: OrderItem[];
        paymentMethod: PaymentMethod;
        clientId?: number;
        discount?: number;
        notes?: string;
    }): Promise<Order> {
        const response = await this.axios.post('/pdv/orders', data);
        return response.data;
    }

    async getProducts(query?: string, category?: string) {
        const params = new URLSearchParams();
        if (query) params.append('query', query);
        if (category) params.append('category', category);

        const response = await this.axios.get('/pdv/products', { params });
        return response.data;
    }

    async processPayment(orderId: number, paymentData: {
        method: PaymentMethod;
        amount: number;
        installments?: number;
        cardData?: {
            number: string;
            holder: string;
            expiry: string;
            cvv: string;
        };
    }) {
        const response = await this.axios.post(`/pdv/orders/${orderId}/payment`, paymentData);
        return response.data;
    }

    async cancelOrder(orderId: number, reason: string) {
        const response = await this.axios.post(`/pdv/orders/${orderId}/cancel`, { reason });
        return response.data;
    }

    async getDailySummary() {
        const response = await this.axios.get('/pdv/summary/daily');
        return response.data;
    }
} 