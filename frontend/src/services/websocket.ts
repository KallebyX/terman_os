import { io, Socket } from 'socket.io-client';
import { useAuth } from '../hooks/useAuth';

class WebSocketService {
    private socket: Socket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;

    connect() {
        const token = localStorage.getItem('@TermanOS:token');
        
        this.socket = io(import.meta.env.VITE_WS_URL, {
            auth: {
                token
            },
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            reconnectionAttempts: this.maxReconnectAttempts
        });

        this.setupEventListeners();
    }

    private setupEventListeners() {
        if (!this.socket) return;

        this.socket.on('connect', () => {
            console.log('WebSocket conectado');
            this.reconnectAttempts = 0;
        });

        this.socket.on('disconnect', (reason) => {
            console.log('WebSocket desconectado:', reason);
        });

        this.socket.on('connect_error', (error) => {
            console.error('Erro de conexão:', error);
            this.reconnectAttempts++;

            if (this.reconnectAttempts >= this.maxReconnectAttempts) {
                const { signOut } = useAuth();
                signOut();
            }
        });

        // Eventos específicos do sistema
        this.socket.on('order_status_update', (data) => {
            // Emitir evento para atualização da UI
            window.dispatchEvent(new CustomEvent('orderStatusUpdate', { detail: data }));
        });

        this.socket.on('new_notification', (data) => {
            window.dispatchEvent(new CustomEvent('newNotification', { detail: data }));
        });

        this.socket.on('stock_alert', (data) => {
            window.dispatchEvent(new CustomEvent('stockAlert', { detail: data }));
        });
    }

    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
    }

    emit(event: string, data: any) {
        if (this.socket) {
            this.socket.emit(event, data);
        }
    }

    subscribe(event: string, callback: (data: any) => void) {
        if (this.socket) {
            this.socket.on(event, callback);
        }
    }

    unsubscribe(event: string, callback: (data: any) => void) {
        if (this.socket) {
            this.socket.off(event, callback);
        }
    }
}

export const websocketService = new WebSocketService(); 