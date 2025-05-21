import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '../components/ui/Button';

const NotFoundPage = () => {
  return (
    <div className="min-h-screen bg-background-lightGray flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <div className="text-9xl font-bold text-primary-500 mb-4">404</div>
        <h1 className="text-3xl font-bold text-secondary-900 mb-2">Página não encontrada</h1>
        <p className="text-secondary-600 mb-8 max-w-md">
          A página que você está procurando não existe ou foi movida para outro endereço.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            as={Link}
            to="/"
            variant="primary"
            size="lg"
            className="min-w-[200px]"
          >
            Voltar para o início
          </Button>
          <Button
            as={Link}
            to="/marketplace"
            variant="outline"
            size="lg"
            className="min-w-[200px]"
          >
            Visitar Marketplace
          </Button>
        </div>
      </motion.div>
    </div>
  );
};

export default NotFoundPage;
