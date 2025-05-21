import React, { useState } from 'react';
import { useProducts } from '../../hooks/useProducts';
import { Button } from '../../components/ui/Button';
import { Table, Thead, Tbody, Th, Td } from '../../components/ui/Table';
import { Modal } from '../../components/ui/Modal';
import { ProductForm } from './components/ProductForm';
import { Product } from '../../types/common';

export const ProductsPage: React.FC = () => {
  const { products, loading, addProduct, updateProduct, deleteProduct } = useProducts();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  const handleSubmit = async (data: Partial<Product>) => {
    try {
      if (selectedProduct) {
        await updateProduct(selectedProduct.id, data);
      } else {
        await addProduct(data as Omit<Product, 'id' | 'createdAt' | 'updatedAt'>);
      }
      setIsModalOpen(false);
      setSelectedProduct(null);
    } catch (error) {
      console.error('Erro ao salvar produto:', error);
    }
  };

  const handleEdit = (product: Product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este produto?')) {
      await deleteProduct(id);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Produtos</h1>
        <Button onClick={() => setIsModalOpen(true)}>
          Novo Produto
        </Button>
      </div>

      {loading ? (
        <div>Carregando...</div>
      ) : (
        <Table>
          <Thead>
            <tr>
              <Th>Nome</Th>
              <Th>Preço</Th>
              <Th>Estoque</Th>
              <Th>Categoria</Th>
              <Th>Ações</Th>
            </tr>
          </Thead>
          <Tbody>
            {products.map(product => (
              <tr key={product.id}>
                <Td>{product.name}</Td>
                <Td>R$ {product.price.toFixed(2)}</Td>
                <Td>{product.stock}</Td>
                <Td>{product.category}</Td>
                <Td>
                  <div className="flex space-x-2">
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => handleEdit(product)}
                    >
                      Editar
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => handleDelete(product.id)}
                    >
                      Excluir
                    </Button>
                  </div>
                </Td>
              </tr>
            ))}
          </Tbody>
        </Table>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedProduct(null);
        }}
        title={selectedProduct ? 'Editar Produto' : 'Novo Produto'}
      >
        <ProductForm
          initialData={selectedProduct}
          onSubmit={handleSubmit}
          onCancel={() => {
            setIsModalOpen(false);
            setSelectedProduct(null);
          }}
        />
      </Modal>
    </div>
  );
}; 