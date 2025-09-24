#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h postgresql -U orthanc -d orthanc > /backups/orthanc_backup_$DATE.sql
find /backups -name "orthanc_backup_*.sql" -mtime +7 -delete
echo "Backup completed: orthanc_backup_$DATE.sql"
