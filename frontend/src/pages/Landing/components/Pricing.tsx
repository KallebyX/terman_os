import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../../../components/ui';

const plans = [
  {
    name: 'Básico',
    price: '99',
    description: 'Ideal para pequenos negócios',
    features: [
      'PDV com 1 usuário',
      'Controle de estoque básico',
      'Cadastro de clientes',
      'Relatórios essenciais'
    ]
  },
  {
    name: 'Profissional',
    price: '199',
    description: 'Para negócios em crescimento',
    features: [
      'PDV com 3 usuários',
      'Controle de estoque avançado',
      'Gestão de clientes',
      'Relatórios completos',
      'Integração fiscal'
    ]
  },
  {
    name: 'Empresarial',
    price: '399',
    description: 'Solução completa para sua empresa',
    features: [
      'PDV com usuários ilimitados',
      'Gestão completa de estoque',
      'CRM avançado',
      'Relatórios personalizados',
      'Integração fiscal',
      'Suporte prioritário'
    ]
  }
];

export const Pricing: React.FC = () => (
  <div className="bg-white py-12">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center">
        <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Planos para todos os tamanhos
        </h2>
        <p className="mt-4 text-lg text-gray-500">
          Escolha o plano ideal para o seu negócio
        </p>
      </div>

      <div className="mt-12 grid gap-8 lg:grid-cols-3">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className="border rounded-lg shadow-sm divide-y divide-gray-200"
          >
            <div className="p-6">
              <h3 className="text-lg font-medium text-gray-900">{plan.name}</h3>
              <p className="mt-2 text-sm text-gray-500">{plan.description}</p>
              <p className="mt-4">
                <span className="text-4xl font-extrabold text-gray-900">
                  R${plan.price}
                </span>
                <span className="text-base font-medium text-gray-500">/mês</span>
              </p>
              <Link to="/register">
                <Button
                  variant={plan.name === 'Profissional' ? 'primary' : 'outline'}
                  fullWidth
                  className="mt-6"
                >
                  Começar agora
                </Button>
              </Link>
            </div>
            <div className="p-6">
              <ul className="space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex">
                    <i className="fas fa-check text-green-500 flex-shrink-0 mt-1" />
                    <span className="ml-3 text-gray-500">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
); 