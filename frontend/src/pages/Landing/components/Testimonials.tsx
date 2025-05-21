import React from 'react';

const testimonials = [
  {
    content: 'O sistema revolucionou a forma como gerenciamos nossa loja. Tudo ficou mais simples e organizado.',
    author: 'Maria Silva',
    role: 'Proprietária - Loja de Roupas',
    image: '/images/testimonials/maria.jpg'
  },
  {
    content: 'Excelente ferramenta para controle de estoque. Reduziu muito nosso tempo com processos manuais.',
    author: 'João Santos',
    role: 'Gerente - Supermercado',
    image: '/images/testimonials/joao.jpg'
  },
  {
    content: 'O suporte é incrível e o sistema é muito intuitivo. Recomendo para qualquer empresa.',
    author: 'Ana Costa',
    role: 'Diretora - Farmácia',
    image: '/images/testimonials/ana.jpg'
  }
];

export const Testimonials: React.FC = () => (
  <div className="bg-gray-50 py-12">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center">
        <h2 className="text-3xl font-extrabold text-gray-900">
          O que nossos clientes dizem
        </h2>
        <p className="mt-4 text-lg text-gray-500">
          Histórias reais de empresas que transformaram seus negócios
        </p>
      </div>

      <div className="mt-12 grid gap-8 lg:grid-cols-3">
        {testimonials.map((testimonial) => (
          <div
            key={testimonial.author}
            className="bg-white rounded-lg shadow-sm p-6"
          >
            <p className="text-gray-600 italic">"{testimonial.content}"</p>
            <div className="mt-4 flex items-center">
              <img
                className="h-12 w-12 rounded-full"
                src={testimonial.image}
                alt={testimonial.author}
              />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-900">
                  {testimonial.author}
                </p>
                <p className="text-sm text-gray-500">{testimonial.role}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
); 