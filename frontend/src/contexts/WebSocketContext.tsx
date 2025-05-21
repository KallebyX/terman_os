import React, { createContext, useContext, useEffect, useState } from 'react';
import { websocketService } from '../services/websocket';
import { useAuth } from './AuthContext';

interface WebSocketContextData {
    connected: boolean;
    subscribe: (event: string, callback: (data: any) => void) => void;
    unsubscribe: (event: string, callback: (data: any) => void) => void;
    emit: (event: string, data: any) => void;
}

const WebSocketContext = createContext<WebSocketContextData>({} as WebSocketContextData);

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [connected, setConnected] = useState(false);
    const { signed } = useAuth();

    useEffect(() => {
        if (signed) {
            websocketService.connect();
            setConnected(true);
        } else {
            websocketService.disconnect();
            setConnected(false);
        }
    }, [signed]);

    const subscribe = (event: string, callback: (data: any) => void) => {
        websocketService.subscribe(event, callback);
    };

    const unsubscribe = (event: string, callback: (data: any) => void) => {
        websocketService.unsubscribe(event, callback);
    };

    const emit = (event: string, data: any) => {
        websocketService.emit(event, data);
    };

    return (
        <WebSocketContext.Provider value={{ connected, subscribe, unsubscribe, emit }}>
            {children}
        </WebSocketContext.Provider>
    );
};

export const useWebSocket = () => {
    const context = useContext(WebSocketContext);
    if (!context) {
        throw new Error('useWebSocket must be used within a WebSocketProvider');
    }
    return context;
}; 