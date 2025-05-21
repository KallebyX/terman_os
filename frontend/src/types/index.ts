export interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
  document: string;
  address: {
    street: string;
    number: string;
    complement?: string;
    neighborhood: string;
    city: string;
    state: string;
    zipcode: string;
  };
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  name: string;
  code: string;
  description: string;
  price: number;
  stock: number;
  category: string;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: number;
  customer: Customer;
  items: Array<{
    product: Product;
    quantity: number;
    price: number;
  }>;
  total: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  payment_method: string;
  notes?: string;
  created_at: string;
  updated_at: string;
} 