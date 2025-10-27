# Deployment Guide - Radiologi RIS

## Quick Start

1. **Start services:**
   ```bash
   docker-compose up -d atau  docker compose up -d
   ```

2. **Access interfaces:**
   - Orthanc Web: http://localhost:8042 (admin/admin123)
   - Database Admin: http://localhost:8081
   - DICOM Port: 4242

## Security Configuration

- **Authentication enabled** with users:
  - admin/admin123 (full access)
  - radiologist/radio123 (read access)

## Performance Settings

- Max 50 studies/hour capacity
- 2-second worklist response time
- 10-second DICOM retrieval timeout

## Backup & Monitoring

- **Manual backup:**
  ```bash
  docker-compose --profile backup run backup /scripts/backup.sh
  ```

- **Health monitoring:**
  ```bash
  python3 scripts/monitor.py
  ```

## Modality Configuration

Configured modalities:
- IO01: 192.168.1.50:104
- MR01: 192.168.1.51:104

https://www.dicomlibrary.com/dicom/modality/

## Worklist Generation

### Using Orthanc REST API (Recommended)

Create worklists directly through the Orthanc REST API:

```bash
# Example using curl
curl -X POST http://localhost:8042/tools/create-dicom \
  -H "Content-Type: application/json" \
  -d '{
    "PatientID": "12345",
    "PatientName": "Toto",
    "ScheduledProcedureStepSequence": {
      "ScheduledStationAETitle": "WLM_SCP",
      "ScheduledProcedureStepStartDate": "20231201",
      "ScheduledProcedureStepStartTime": "080000"
    }
  }'
```

For detailed documentation, see [WORKLIST-API.md](WORKLIST-API.md)

### Legacy Method (DCMTK)

```bash
cd radiology-cron
python3 main.py
```
- check : pip install pydicom

Note: This method is deprecated in favor of the REST API approach.

## Troubleshooting

- Check logs: `docker-compose logs orthanc`
- Verify DICOM connectivity: Test with modality ping
- Database issues: Check pgweb interface
