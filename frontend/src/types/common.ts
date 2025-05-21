export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'client' | 'seller';
  createdAt: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
  images: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Order {
  id: string;
  clientId: string;
  products: {
    id: string;
    quantity: number;
    price: number;
  }[];
  total: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  createdAt: string;
  updatedAt: string;
} 