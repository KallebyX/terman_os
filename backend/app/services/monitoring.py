import logging
from datetime import datetime
from app import db
from app.models.system_log import SystemLog
from functools import wraps
import time
import traceback

class MonitoringService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log_error(self, error, context=None):
        """Registra erros do sistema"""
        log_entry = SystemLog(
            level='ERROR',
            message=str(error),
            stack_trace=traceback.format_exc(),
            context=context,
            timestamp=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.commit()
        
        self.logger.error(f"Error: {error}", exc_info=True, extra=context or {})

    def monitor_performance(self, name):
        """Decorator para monitorar performance de funções"""
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                start_time = time.time()
                result = f(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Registrar métricas
                self.record_metric(
                    name=f"function.{name}",
                    value=execution_time,
                    metric_type='timing'
                )
                
                return result
            return wrapped
        return decorator

    def record_metric(self, name, value, metric_type='counter'):
        """Registra métricas do sistema"""
        from app.models.system_metric import SystemMetric
        
        metric = SystemMetric(
            name=name,
            value=value,
            type=metric_type,
            timestamp=datetime.utcnow()
        )
        db.session.add(metric)
        db.session.commit()

    def monitor_database(self):
        """Monitora estatísticas do banco de dados"""
        try:
            result = db.session.execute("""
                SELECT 
                    pg_database_size(current_database()) as db_size,
                    (SELECT count(*) FROM pg_stat_activity) as connections,
                    (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections
            """)
            stats = result.fetchone()
            
            self.record_metric('database.size', stats.db_size, 'gauge')
            self.record_metric('database.connections', stats.connections, 'gauge')
            self.record_metric('database.active_connections', stats.active_connections, 'gauge')
            
        except Exception as e:
            self.log_error(e, {'context': 'database_monitoring'})

    def monitor_api_request(self):
        """Decorator para monitorar requisições da API"""
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = f(*args, **kwargs)
                    status = 'success'
                except Exception as e:
                    self.log_error(e, {
                        'function': f.__name__,
                        'args': args,
                        'kwargs': kwargs
                    })
                    status = 'error'
                    raise
                finally:
                    execution_time = time.time() - start_time
                    self.record_metric(
                        f"api.request.{f.__name__}.{status}",
                        execution_time,
                        'timing'
                    )
                
                return result
            return wrapped
        return decorator

monitoring_service = MonitoringService() 