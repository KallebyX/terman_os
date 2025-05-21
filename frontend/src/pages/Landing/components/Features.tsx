import React from 'react';

const features = [
  {
    title: 'PDV Intuitivo',
    description: 'Interface simples e rápida para suas vendas no dia a dia.',
    icon: 'shopping-cart'
  },
  {
    title: 'Controle de Estoque',
    description: 'Gerencie seu estoque em tempo real com alertas automáticos.',
    icon: 'box'
  },
  {
    title: 'Gestão de Clientes',
    description: 'Cadastre e acompanhe seus clientes de forma organizada.',
    icon: 'users'
  },
  {
    title: 'Relatórios Detalhados',
    description: 'Analise seu negócio com relatórios e gráficos completos.',
    icon: 'chart-bar'
  }
];

export const Features: React.FC = () => (
  <div className="py-12 bg-gray-50">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="lg:text-center">
        <h2 className="text-base text-primary-600 font-semibold tracking-wide uppercase">
          Funcionalidades
        </h2>
        <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          Tudo que você precisa em um só lugar
        </p>
        <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
          Gerencie seu negócio de forma eficiente com nossas ferramentas integradas.
        </p>
      </div>

      <div className="mt-10">
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <div key={feature.title} className="relative">
              <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                <i className={`fas fa-${feature.icon} text-lg`} />
              </div>
              <p className="ml-16 text-lg leading-6 font-medium text-gray-900">
                {feature.title}
              </p>
              <p className="mt-2 ml-16 text-base text-gray-500">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
); 