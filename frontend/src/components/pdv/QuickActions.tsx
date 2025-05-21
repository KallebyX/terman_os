import React from 'react';
import { Button } from '../ui';
import { useAuth } from '../../hooks/useAuth';

interface QuickActionsProps {
    onOpenDrawer: () => void;
    onOpenCashier: () => void;
    onCloseCashier: () => void;
    onPrintLastReceipt: () => void;
}

export const QuickActions: React.FC<QuickActionsProps> = ({
    onOpenDrawer,
    onOpenCashier,
    onCloseCashier,
    onPrintLastReceipt
}) => {
    const { user } = useAuth();
    const isManager = user?.role === 'manager' || user?.role === 'admin';

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button
                variant="outline"
                onClick={onOpenDrawer}
                className="flex flex-col items-center p-4"
            >
                <span className="material-icons text-2xl mb-2">point_of_sale</span>
                <span>Abrir Gaveta</span>
            </Button>

            {isManager && (
                <>
                    <Button
                        variant="outline"
                        onClick={onOpenCashier}
                        className="flex flex-col items-center p-4"
                    >
                        <span className="material-icons text-2xl mb-2">login</span>
                        <span>Abrir Caixa</span>
                    </Button>

                    <Button
                        variant="outline"
                        onClick={onCloseCashier}
                        className="flex flex-col items-center p-4"
                    >
                        <span className="material-icons text-2xl mb-2">logout</span>
                        <span>Fechar Caixa</span>
                    </Button>
                </>
            )}

            <Button
                variant="outline"
                onClick={onPrintLastReceipt}
                className="flex flex-col items-center p-4"
            >
                <span className="material-icons text-2xl mb-2">receipt_long</span>
                <span>Última Impressão</span>
            </Button>
        </div>
    );
}; 