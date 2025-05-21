import React from 'react';
import { Link } from 'react-router-dom';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const Logo: React.FC<LogoProps> = ({ size = 'md', className = '' }) => {
  // Definir tamanhos com base no parâmetro size
  const sizes = {
    sm: 'h-8',
    md: 'h-12',
    lg: 'h-16',
  };

  // URL da imagem do logo
  const logoUrl = '/logo.png';
  
  // URL de fallback caso a imagem principal não carregue
  const fallbackUrl = 'https://via.placeholder.com/160x64?text=Mangueiras+Terman';
  
  // Cores da marca para o logo em SVG (fallback secundário)
  const primaryColor = '#00c853'; // Verde primário da Terman
  const secondaryColor = '#004d21'; // Verde secundário mais escuro

  // Função para lidar com erro de carregamento da imagem
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    const target = e.target as HTMLImageElement;
    target.onerror = null; // Prevenir loop infinito
    target.src = fallbackUrl;
  };

  return (
    <div className={`logo-container ${className}`}>
      <Link to="/" className="inline-block">
        <img
          src={logoUrl}
          alt="Mangueiras Terman"
          className={`${sizes[size]} transition-all duration-300 hover:opacity-90`}
          onError={handleImageError}
        />
      </Link>
      
      {/* SVG fallback que será mostrado apenas se o JavaScript estiver desabilitado e a imagem falhar */}
      <noscript>
        <svg 
          width="160" 
          height="64" 
          viewBox="0 0 160 64" 
          className={`${sizes[size]}`}
        >
          <rect width="160" height="64" fill={primaryColor} />
          <text 
            x="80" 
            y="32" 
            fontFamily="Arial, sans-serif" 
            fontSize="16" 
            fontWeight="bold" 
            fill={secondaryColor} 
            textAnchor="middle" 
            dominantBaseline="middle"
          >
            Mangueiras Terman
          </text>
        </svg>
      </noscript>
    </div>
  );
};

export default Logo;
