from functools import wraps
from app import redis_client
import json
from datetime import timedelta

class CacheService:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_timeout = 300  # 5 minutos

    def cached(self, timeout=None, key_prefix=''):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                cache_key = self._make_cache_key(f, key_prefix, args, kwargs)
                cached_value = self.redis.get(cache_key)

                if cached_value is not None:
                    return json.loads(cached_value)

                value = f(*args, **kwargs)
                self.redis.setex(
                    cache_key,
                    timeout or self.default_timeout,
                    json.dumps(value)
                )
                return value
            return decorated_function
        return decorator

    def invalidate(self, key_pattern):
        """Invalida todas as chaves que correspondem ao padrão"""
        keys = self.redis.keys(key_pattern)
        if keys:
            self.redis.delete(*keys)

    def _make_cache_key(self, f, key_prefix, args, kwargs):
        """Gera uma chave única para o cache"""
        key_parts = [key_prefix, f.__name__]
        
        # Adiciona argumentos posicionais
        for arg in args:
            key_parts.append(str(arg))
        
        # Adiciona argumentos nomeados ordenados
        for key, value in sorted(kwargs.items()):
            key_parts.append(f"{key}:{value}")
        
        return ':'.join(key_parts)

    def rate_limit(self, key, limit=100, period=60):
        """Implementa limitação de taxa"""
        current = self.redis.get(key)
        
        if current is None:
            self.redis.setex(key, period, 1)
            return True
        
        if int(current) >= limit:
            return False
        
        self.redis.incr(key)
        return True

cache_service = CacheService(redis_client) 