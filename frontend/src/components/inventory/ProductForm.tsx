import React, { useState } from 'react';
import { Form } from '../form/Form';
import { FormField } from '../form/FormField';
import { FileUpload } from '../form/FileUpload';
import { useForm } from '../../hooks/useForm';
import { validators } from '../../utils/validators';
import { Product } from '../../types/common';

interface ProductFormProps {
  initialData?: Product;
  onSubmit: (data: Partial<Product>) => Promise<void>;
  onCancel: () => void;
}

export const ProductForm: React.FC<ProductFormProps> = ({
  initialData,
  onSubmit,
  onCancel
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [images, setImages] = useState<File[]>([]);

  const form = useForm({
    name: {
      value: initialData?.name || '',
      rules: [validators.required, validators.minLength(3)]
    },
    description: {
      value: initialData?.description || '',
      rules: [validators.required]
    },
    price: {
      value: initialData?.price || 0,
      rules: [validators.required, validators.price]
    },
    stock: {
      value: initialData?.stock || 0,
      rules: [validators.required, validators.numeric]
    },
    category: {
      value: initialData?.category || '',
      rules: [validators.required]
    },
    minStock: {
      value: initialData?.minStock || 0,
      rules: [validators.required, validators.numeric]
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.validateForm()) return;

    try {
      setIsSubmitting(true);
      await onSubmit({
        ...form.values,
        price: Number(form.values.price),
        stock: Number(form.values.stock),
        minStock: Number(form.values.minStock),
        images: images.length > 0 ? await uploadImages(images) : undefined
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const uploadImages = async (files: File[]): Promise<string[]> => {
    // Implementar lógica de upload de imagens
    return [];
  };

  return (
    <Form
      onSubmit={handleSubmit}
      submitLabel={initialData ? 'Atualizar' : 'Cadastrar'}
      isSubmitting={isSubmitting}
      showCancel
      onCancel={onCancel}
    >
      <FormField
        type="text"
        name="name"
        label="Nome do Produto"
        value={form.values.name}
        onChange={(value) => form.handleChange('name', value)}
        error={form.touched.name ? form.errors.name : undefined}
      />

      <FormField
        type="text"
        name="description"
        label="Descrição"
        value={form.values.description}
        onChange={(value) => form.handleChange('description', value)}
        error={form.touched.description ? form.errors.description : undefined}
      />

      <div className="grid grid-cols-2 gap-4">
        <FormField
          type="number"
          name="price"
          label="Preço"
          value={form.values.price}
          onChange={(value) => form.handleChange('price', value)}
          error={form.touched.price ? form.errors.price : undefined}
        />

        <FormField
          type="number"
          name="stock"
          label="Estoque"
          value={form.values.stock}
          onChange={(value) => form.handleChange('stock', value)}
          error={form.touched.stock ? form.errors.stock : undefined}
        />
      </div>

      <FormField
        type="select"
        name="category"
        label="Categoria"
        value={form.values.category}
        onChange={(value) => form.handleChange('category', value)}
        error={form.touched.category ? form.errors.category : undefined}
        options={[
          { value: '', label: 'Selecione uma categoria' },
          { value: 'electronics', label: 'Eletrônicos' },
          { value: 'clothing', label: 'Vestuário' },
          { value: 'food', label: 'Alimentos' },
          { value: 'books', label: 'Livros' }
        ]}
      />

      <FormField
        type="number"
        name="minStock"
        label="Estoque Mínimo"
        value={form.values.minStock}
        onChange={(value) => form.handleChange('minStock', value)}
        error={form.touched.minStock ? form.errors.minStock : undefined}
      />

      <div className="mt-4">
        <FileUpload
          label="Imagens do Produto"
          onFileSelect={(file) => setImages([...images, file])}
          accept="image/*"
          maxSize={5 * 1024 * 1024} // 5MB
        />
        {images.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {images.map((file, index) => (
              <div
                key={index}
                className="relative"
              >
                <img
                  src={URL.createObjectURL(file)}
                  alt={`Preview ${index + 1}`}
                  className="w-20 h-20 object-cover rounded"
                />
                <button
                  type="button"
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
                  onClick={() => setImages(images.filter((_, i) => i !== index))}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </Form>
  );
}; 