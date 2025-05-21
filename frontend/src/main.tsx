import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

// Configuração para garantir que o ambiente está correto
const apiUrl = import.meta.env.MODE === 'development' 
  ? import.meta.env.VITE_API_URL 
  : import.meta.env.VITE_API_URL_DOCKER;

console.log('Ambiente:', import.meta.env.MODE);
console.log('API URL:', apiUrl);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
