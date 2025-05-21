import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Header / Hero Section */}
      <header className="bg-primary-500 text-white">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex flex-col md:flex-row items-center justify-between"
          >
            <div className="md:w-1/2 mb-8 md:mb-0">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Mangueiras Terman</h1>
              <p className="text-xl mb-8">Soluções completas em mangueiras hidráulicas para sua empresa</p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button 
                  size="lg" 
                  variant="secondary"
                  onClick={() => window.location.href = '/marketplace'}
                >
                  Conheça nossos produtos
                </Button>
                <Button 
                  size="lg" 
                  variant="outline"
                  className="bg-white text-primary-500 hover:bg-primary-50"
                  onClick={() => window.location.href = '/login'}
                >
                  Área do Cliente
                </Button>
              </div>
            </div>
            <div className="md:w-1/2 flex justify-center">
              <img 
                src="/logo.png" 
                alt="Mangueiras Terman" 
                className="w-64 h-64 object-contain"
              />
            </div>
          </motion.div>
        </div>
      </header>

      {/* Sobre nós */}
      <section className="py-16 bg-background-lightGray">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl font-bold text-center mb-12">Sobre a Mangueiras Terman</h2>
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="md:w-1/2">
                <p className="text-lg text-secondary-700 mb-4">
                  Há mais de 20 anos no mercado, a Mangueiras Terman é especializada em fornecer soluções completas em mangueiras hidráulicas para diversos setores industriais.
                </p>
                <p className="text-lg text-secondary-700 mb-4">
                  Nossa missão é oferecer produtos de alta qualidade, com atendimento personalizado e entrega rápida, garantindo a satisfação total de nossos clientes.
                </p>
                <p className="text-lg text-secondary-700">
                  Contamos com uma equipe técnica especializada, pronta para auxiliar na escolha da melhor solução para sua necessidade.
                </p>
              </div>
              <div className="md:w-1/2">
                <img 
                  src="/factory.jpg" 
                  alt="Fábrica Mangueiras Terman" 
                  className="rounded-lg shadow-md w-full h-auto"
                />
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Serviços */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl font-bold text-center mb-12">Nossos Serviços</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card variant="elevated" className="text-center p-6">
                <div className="text-primary-500 text-4xl mb-4">
                  <i className="fas fa-tools"></i>
                </div>
                <h3 className="text-xl font-semibold mb-3">Fabricação Personalizada</h3>
                <p className="text-secondary-700">
                  Fabricamos mangueiras hidráulicas sob medida para atender às necessidades específicas do seu projeto.
                </p>
              </Card>
              
              <Card variant="elevated" className="text-center p-6">
                <div className="text-primary-500 text-4xl mb-4">
                  <i className="fas fa-truck"></i>
                </div>
                <h3 className="text-xl font-semibold mb-3">Entrega Rápida</h3>
                <p className="text-secondary-700">
                  Contamos com logística própria para garantir a entrega rápida e segura dos produtos em todo o Brasil.
                </p>
              </Card>
              
              <Card variant="elevated" className="text-center p-6">
                <div className="text-primary-500 text-4xl mb-4">
                  <i className="fas fa-headset"></i>
                </div>
                <h3 className="text-xl font-semibold mb-3">Suporte Técnico</h3>
                <p className="text-secondary-700">
                  Nossa equipe técnica está disponível para auxiliar na escolha e instalação dos produtos.
                </p>
              </Card>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Produtos em Destaque */}
      <section className="py-16 bg-background-lightGray">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl font-bold text-center mb-12">Produtos em Destaque</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[1, 2, 3, 4].map((item) => (
                <Card 
                  key={item} 
                  variant="elevated" 
                  className="overflow-hidden transition-transform hover:scale-105"
                  onClick={() => window.location.href = '/marketplace'}
                >
                  <img 
                    src={`/product-${item}.jpg`} 
                    alt={`Produto ${item}`} 
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="font-semibold mb-2">Mangueira Hidráulica Tipo {item}</h3>
                    <p className="text-secondary-700 text-sm mb-3">
                      Ideal para aplicações industriais de alta pressão.
                    </p>
                    <Button variant="primary" fullWidth>Ver detalhes</Button>
                  </div>
                </Card>
              ))}
            </div>
            <div className="text-center mt-10">
              <Button 
                variant="outline" 
                size="lg"
                onClick={() => window.location.href = '/marketplace'}
              >
                Ver todos os produtos
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Depoimentos */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl font-bold text-center mb-12">O que nossos clientes dizem</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  name: "Empresa ABC",
                  role: "Setor Automotivo",
                  text: "Excelente qualidade nos produtos e atendimento rápido. Recomendo!"
                },
                {
                  name: "Indústria XYZ",
                  role: "Setor de Mineração",
                  text: "As mangueiras fornecidas pela Terman são de alta durabilidade e resistência."
                },
                {
                  name: "Construtora 123",
                  role: "Setor de Construção",
                  text: "Parceria de anos que tem nos atendido com excelência em todos os projetos."
                }
              ].map((testimonial, index) => (
                <Card key={index} variant="bordered" className="p-6">
                  <div className="flex flex-col h-full">
                    <div className="mb-4 text-primary-500">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <span key={star} className="text-xl">★</span>
                      ))}
                    </div>
                    <p className="text-secondary-700 italic mb-6 flex-grow">
                      "{testimonial.text}"
                    </p>
                    <div>
                      <p className="font-semibold">{testimonial.name}</p>
                      <p className="text-sm text-secondary-500">{testimonial.role}</p>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Contato */}
      <section className="py-16 bg-primary-500 text-white">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <h2 className="text-3xl font-bold mb-6">Entre em contato</h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              Estamos prontos para atender sua empresa e oferecer as melhores soluções em mangueiras hidráulicas.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Button 
                variant="secondary" 
                size="lg"
                className="bg-white text-primary-500 hover:bg-primary-50"
                onClick={() => window.open('https://wa.me/5511999999999', '_blank')}
              >
                <span className="mr-2">
                  <i className="fab fa-whatsapp"></i>
                </span>
                WhatsApp
              </Button>
              <Button 
                variant="outline" 
                size="lg"
                className="border-white text-white hover:bg-primary-600"
                onClick={() => window.location.href = 'mailto:contato@mangueirasterman.com.br'}
              >
                <span className="mr-2">
                  <i className="fas fa-envelope"></i>
                </span>
                E-mail
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-secondary-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-semibold mb-4">Mangueiras Terman</h3>
              <p className="text-secondary-300 mb-4">
                Soluções completas em mangueiras hidráulicas para sua empresa.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="text-white hover:text-primary-500">
                  <i className="fab fa-facebook-f"></i>
                </a>
                <a href="#" className="text-white hover:text-primary-500">
                  <i className="fab fa-instagram"></i>
                </a>
                <a href="#" className="text-white hover:text-primary-500">
                  <i className="fab fa-linkedin-in"></i>
                </a>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold mb-4">Produtos</h3>
              <ul className="space-y-2">
                <li><a href="/marketplace" className="text-secondary-300 hover:text-white">Mangueiras Hidráulicas</a></li>
                <li><a href="/marketplace" className="text-secondary-300 hover:text-white">Conexões</a></li>
                <li><a href="/marketplace" className="text-secondary-300 hover:text-white">Adaptadores</a></li>
                <li><a href="/marketplace" className="text-secondary-300 hover:text-white">Acessórios</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold mb-4">Links Úteis</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-secondary-300 hover:text-white">Sobre Nós</a></li>
                <li><a href="#" className="text-secondary-300 hover:text-white">Serviços</a></li>
                <li><a href="#" className="text-secondary-300 hover:text-white">Contato</a></li>
                <li><a href="/login" className="text-secondary-300 hover:text-white">Área do Cliente</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold mb-4">Contato</h3>
              <ul className="space-y-2">
                <li className="flex items-start">
                  <i className="fas fa-map-marker-alt mt-1 mr-2"></i>
                  <span className="text-secondary-300">Av. Industrial, 1000 - São Paulo/SP</span>
                </li>
                <li className="flex items-start">
                  <i className="fas fa-phone-alt mt-1 mr-2"></i>
                  <span className="text-secondary-300">(11) 9999-9999</span>
                </li>
                <li className="flex items-start">
                  <i className="fas fa-envelope mt-1 mr-2"></i>
                  <span className="text-secondary-300">contato@mangueirasterman.com.br</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-secondary-700 mt-8 pt-8 text-center text-secondary-400">
            <p>&copy; {new Date().getFullYear()} Mangueiras Terman. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
