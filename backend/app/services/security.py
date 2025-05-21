from functools import wraps
from flask import request, jsonify
from app import redis_client
import hashlib
import json
from datetime import datetime, timedelta

class SecurityService:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.max_failed_attempts = 5
        self.lockout_duration = 900  # 15 minutos

    def rate_limit(self, limit=100, period=60):
        """Implementa limitação de taxa por IP"""
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                ip = request.remote_addr
                key = f'rate_limit:{ip}:{f.__name__}'
                
                current = self.redis.get(key)
                if current is None:
                    self.redis.setex(key, period, 1)
                elif int(current) >= limit:
                    return jsonify({
                        'error': 'Too many requests',
                        'retry_after': self.redis.ttl(key)
                    }), 429
                else:
                    self.redis.incr(key)
                
                return f(*args, **kwargs)
            return wrapped
        return decorator

    def check_brute_force(self, user_id):
        """Verifica tentativas de login mal sucedidas"""
        key = f'login_attempts:{user_id}'
        attempts = self.redis.get(key)
        
        if attempts and int(attempts) >= self.max_failed_attempts:
            return False
        return True

    def record_failed_login(self, user_id):
        """Registra tentativa de login mal sucedida"""
        key = f'login_attempts:{user_id}'
        
        if self.redis.exists(key):
            self.redis.incr(key)
        else:
            self.redis.setex(key, self.lockout_duration, 1)

    def clear_login_attempts(self, user_id):
        """Limpa tentativas de login após sucesso"""
        key = f'login_attempts:{user_id}'
        self.redis.delete(key)

    def validate_request_signature(self, signature, payload):
        """Valida assinatura de requisições webhook"""
        expected = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
        return signature == expected

security_service = SecurityService(redis_client) 