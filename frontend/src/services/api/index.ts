import axios, { AxiosInstance } from 'axios';
import { setupInterceptors } from './interceptors';
import { AuthService } from './auth';
import { ProductService } from './product';
import { OrderService } from './order';
import { ClientService } from './client';
import { ReportService } from './report';

class API {
    private axios: AxiosInstance;
    public auth: AuthService;
    public products: ProductService;
    public orders: OrderService;
    public clients: ClientService;
    public reports: ReportService;

    constructor() {
        this.axios = axios.create({
            baseURL: import.meta.env.VITE_API_URL,
            headers: {
                'Content-Type': 'application/json'
            }
        });

        setupInterceptors(this.axios);

        // Inicializar serviços
        this.auth = new AuthService(this.axios);
        this.products = new ProductService(this.axios);
        this.orders = new OrderService(this.axios);
        this.clients = new ClientService(this.axios);
        this.reports = new ReportService(this.axios);
    }

    setAuthToken(token: string | null) {
        if (token) {
            this.axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
            delete this.axios.defaults.headers.common['Authorization'];
        }
    }
}

export const api = new API(); 