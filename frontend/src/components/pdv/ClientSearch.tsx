import React, { useState, useEffect } from 'react';
import { Input, Card } from '../ui';
import { useClients } from '../../hooks/useClients';
import { Client } from '../../types/client';
import { useDebounce } from '../../hooks/useDebounce';

interface ClientSearchProps {
    onSelect: (client: Client) => void;
}

export const ClientSearch: React.FC<ClientSearchProps> = ({ onSelect }) => {
    const [search, setSearch] = useState('');
    const debouncedSearch = useDebounce(search, 300);
    const { searchClients, loading } = useClients();
    const [results, setResults] = useState<Client[]>([]);
    const [showResults, setShowResults] = useState(false);

    useEffect(() => {
        const fetchClients = async () => {
            if (debouncedSearch.length >= 3) {
                const clients = await searchClients(debouncedSearch);
                setResults(clients);
                setShowResults(true);
            } else {
                setResults([]);
                setShowResults(false);
            }
        };

        fetchClients();
    }, [debouncedSearch, searchClients]);

    return (
        <div className="relative">
            <Input
                placeholder="Buscar cliente por nome, CPF ou telefone..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onFocus={() => setShowResults(true)}
            />

            {showResults && (
                <Card className="absolute w-full mt-1 z-50 max-h-64 overflow-y-auto">
                    {loading ? (
                        <div className="p-4 text-center">Buscando...</div>
                    ) : results.length > 0 ? (
                        <div>
                            {results.map((client) => (
                                <div
                                    key={client.id}
                                    className="p-3 hover:bg-gray-50 cursor-pointer"
                                    onClick={() => {
                                        onSelect(client);
                                        setSearch(client.name);
                                        setShowResults(false);
                                    }}
                                >
                                    <p className="font-medium">{client.name}</p>
                                    <p className="text-sm text-gray-500">
                                        CPF: {client.cpf} | Tel: {client.phone}
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="p-4 text-center text-gray-500">
                            Nenhum cliente encontrado
                        </div>
                    )}
                </Card>
            )}
        </div>
    );
}; 