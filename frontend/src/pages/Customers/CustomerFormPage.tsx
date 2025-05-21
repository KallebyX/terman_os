import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { CustomerForm } from './components/CustomerForm';
import { useCustomers } from '../../hooks/useCustomers';
import { LoadingSpinner } from '../../components/shared/LoadingSpinner';
import { ErrorMessage } from '../../components/shared/ErrorMessage';

export const CustomerFormPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { customers, isLoading, error, createCustomer, updateCustomer } = useCustomers();

  const customer = id ? customers.find(c => c.id === Number(id)) : undefined;

  const handleSubmit = async (data: any) => {
    try {
      if (id) {
        await updateCustomer(Number(id), data);
      } else {
        await createCustomer(data);
      }
      navigate('/customers');
    } catch (error: any) {
      alert(error.message);
    }
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">
        {id ? 'Editar Cliente' : 'Novo Cliente'}
      </h1>
      <CustomerForm
        onSubmit={handleSubmit}
        initialValues={customer}
        isLoading={isLoading}
      />
    </div>
  );
};
