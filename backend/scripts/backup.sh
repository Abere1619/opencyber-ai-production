#!/bin/bash

set -e

BACKUP_DIR="../backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "Starting database backup..."

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
echo "Backing up database..."
docker-compose -f docker-compose.prod.yml exec -T db pg_dump \
    -U opencyber \
    -d opencyber_ai \
    > $BACKUP_DIR/opencyber_backup_$TIMESTAMP.sql

# Backup uploads if they exist
if [ -d "../uploads" ]; then
    echo "Backing up uploads..."
    tar -czf $BACKUP_DIR/uploads_backup_$TIMESTAMP.tar.gz ../uploads
fi

echo "✅ Backup completed:"
echo "   Database: $BACKUP_DIR/opencyber_backup_$TIMESTAMP.sql"
echo "   Uploads: $BACKUP_DIR/uploads_backup_$TIMESTAMP.tar.gz"
