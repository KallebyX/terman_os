#!/bin/bash

# Configurações
BACKUP_DIR="/backups"
KEEP_DAYS=7
DB_CONTAINER="terman_db"
DB_USER="postgres"
DB_NAME="terman_db"

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Nome do arquivo de backup
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"

# Realizar backup
docker exec $DB_CONTAINER pg_dump -U $DB_USER $DB_NAME > $BACKUP_FILE

# Comprimir backup
gzip $BACKUP_FILE

# Remover backups antigos
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +$KEEP_DAYS -delete

# Enviar para S3 (opcional)
# aws s3 cp $BACKUP_FILE.gz s3://seu-bucket/backups/ 