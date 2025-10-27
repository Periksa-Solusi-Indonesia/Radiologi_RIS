# Dokumentasi Worklist API - Radiologi RIS

## Overview
Dokumen ini menjelaskan cara menggunakan REST API Orthanc untuk pembuatan worklist dari aplikasi web, menggantikan pendekatan DCMTK yang lebih kompleks.

## Prerequisites

### Konfigurasi Orthanc
Pastikan konfigurasi berikut ada di `orthanc.json`:
```json
{
  "RestApiWriteToFileSystemEnabled": true,
  "RemoteAccessAllowed": true,
  "AuthenticationEnabled": false,
  "Worklists": {
    "Enable": true,
    "Database": "/worklists"
  },
  "DicomAet": "ORTHANC",
  "DicomPort": 4242
}
```

### Plugin Worklists
Pastikan plugin worklists sudah terinstall dan aktif:
```bash
# Cek plugin yang aktif
curl http://localhost:8042/plugins
```

## API Endpoint

### Membuat Worklist Baru
Gunakan endpoint `/tools/create-dicom` dengan metode POST untuk membuat worklist baru.

**Endpoint:** `POST http://localhost:8042/tools/create-dicom`

**Contoh Request:**
```bash
curl -X POST http://localhost:8042/tools/create-dicom \
  -H "Content-Type: application/json" \
  -d '{
    "PatientID": "12345",
    "PatientName": "Toto",
    "PatientBirthDate": "19800115",
    "PatientSex": "M",
    "ScheduledProcedureStepSequence": {
      "ScheduledStationAETitle": "WLM_SCP",
      "ScheduledProcedureStepStartDate": "20231201",
      "ScheduledProcedureStepStartTime": "080000"
    }
  }'
```

**Contoh dengan PowerShell:**
```powershell
$body = @{
  "PatientID" = "12345"
  "PatientName" = "Toto"
  "PatientBirthDate" = "19800115"
  "PatientSex" = "M"
  "ScheduledProcedureStepSequence" = @{
    "ScheduledStationAETitle" = "WLM_SCP"
    "ScheduledProcedureStepStartDate" = "20231201"
    "ScheduledProcedureStepStartTime" = "080000"
  }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8042/tools/create-dicom" -Method POST -Body $body -ContentType "application/json"
```

**Response:**
```json
{
  "ID": "c793b5e4-6695b080-bc3bea4f-e6267026-74ea477d",
  "ParentPatient": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "ParentSeries": "b2c3d4e5-f6g7-8901-bcde-f23456789012"
}
```

### Query Worklist
Gunakan endpoint `/tools/find` dengan metode POST untuk mencari worklist yang sudah dibuat.

**Endpoint:** `POST http://localhost:8042/tools/find`

**Contoh Request:**
```bash
curl -X POST http://localhost:8042/tools/find \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Patient",
    "Query": {
      "PatientName": "Toto"
    }
  }'
```

**Query dengan Patient Birth Date:**
```bash
curl -X POST http://localhost:8042/tools/find \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Patient",
    "Query": {
      "PatientBirthDate": "19800115"
    }
  }'
```

**Query dengan Patient Sex:**
```bash
curl -X POST http://localhost:8042/tools/find \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Patient",
    "Query": {
      "PatientSex": "M"
    }
  }'
```

**Query dengan Multiple Criteria:**
```bash
curl -X POST http://localhost:8042/tools/find \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Patient",
    "Query": {
      "PatientName": "DOE^JOHN",
      "PatientBirthDate": "19800115",
      "PatientSex": "M"
    }
  }'
```

## DICOM Tags yang Umum Digunakan

### Informasi Pasien
- `PatientID`: ID unik pasien
- `PatientName`: Nama pasien (format: LAST^FIRST)
- `PatientBirthDate`: Tanggal lahir (YYYYMMDD)
- `PatientSex`: Jenis kelamin (M/F/O)

### Format Data Pasien

#### Patient Birth Date
- Format: YYYYMMDD (contoh: "19800115" untuk 15 Januari 1980)
- Wajib diisi dengan 8 digit
- Tidak menggunakan pemisah seperti tanda hubung atau garis miring

#### Patient Sex
- Format: Single character
  - "M" untuk Male (Laki-laki)
  - "F" untuk Female (Perempuan)
  - "O" untuk Other (Lainnya)
- Case-sensitive: gunakan huruf kapital

### Informasi Pemeriksaan
- `AccessionNumber`: Nomor akses unik untuk pemeriksaan
- `StudyDescription`: Deskripsi studi
- `RequestedProcedureDescription`: Deskripsi prosedur yang diminta
- `Modality`: Modalitas pemeriksaan (US, CT, MR, dll)

### Informasi Jadwal
- `ScheduledProcedureStepSequence`: Sequence informasi jadwal
  - `ScheduledStationAETitle`: AE title stasiun
  - `ScheduledProcedureStepStartDate`: Tanggal jadwal (YYYYMMDD)
  - `ScheduledProcedureStepStartTime`: Waktu jadwal (HHMMSS)
  - `ScheduledProcedureStepDescription`: Deskripsi prosedur
  - `ScheduledProcedureStepID`: ID prosedur

## Contoh Lengkap dengan Data Pasien Lengkap

Berikut adalah contoh lengkap pembuatan worklist dengan semua data pasien termasuk tanggal lahir dan jenis kelamin:

```bash
curl -X POST http://localhost:8042/tools/create-dicom \
  -H "Content-Type: application/json" \
  -d '{
    "PatientID": "P001234",
    "PatientName": "DOE^JOHN",
    "PatientBirthDate": "19800115",
    "PatientSex": "M",
    "AccessionNumber": "ACC123456",
    "StudyDescription": "USG ABDOMEN",
    "ScheduledProcedureStepSequence": {
      "ScheduledStationAETitle": "WLM_SCP",
      "ScheduledProcedureStepStartDate": "20231201",
      "ScheduledProcedureStepStartTime": "083000",
      "ScheduledProcedureStepDescription": "USG ABDOMEN COMPLETE",
      "ScheduledProcedureStepID": "PROC001"
    }
  }'
```

## Integrasi dengan Aplikasi Web

### Contoh Implementasi dengan JavaScript
```javascript
async function createWorklist(patientData) {
  const response = await fetch('http://localhost:8042/tools/create-dicom', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      PatientID: patientData.id,
      PatientName: patientData.name,
      PatientBirthDate: patientData.birthDate,
      PatientSex: patientData.sex,
      AccessionNumber: patientData.accessionNumber,
      ScheduledProcedureStepSequence: {
        ScheduledStationAETitle: "WLM_SCP",
        ScheduledProcedureStepStartDate: patientData.date,
        ScheduledProcedureStepStartTime: patientData.time,
        ScheduledProcedureStepDescription: patientData.description
      }
    })
  });
  
  return await response.json();
}

// Penggunaan
const patientData = {
  id: "P001234",
  name: "DOE^JOHN",
  birthDate: "19800115",
  sex: "M",
  accessionNumber: "ACC123456",
  date: "20231201",
  time: "083000",
  description: "USG ABDOMEN"
};

createWorklist(patientData)
  .then(result => console.log('Worklist created:', result))
  .catch(error => console.error('Error:', error));
```

### Contoh Implementasi dengan Python
```python
import requests
import json

def create_worklist(patient_data):
    url = "http://localhost:8042/tools/create-dicom"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "PatientID": patient_data["id"],
        "PatientName": patient_data["name"],
        "PatientBirthDate": patient_data["birth_date"],
        "PatientSex": patient_data["sex"],
        "AccessionNumber": patient_data["accession_number"],
        "ScheduledProcedureStepSequence": {
            "ScheduledStationAETitle": "WLM_SCP",
            "ScheduledProcedureStepStartDate": patient_data["date"],
            "ScheduledProcedureStepStartTime": patient_data["time"],
            "ScheduledProcedureStepDescription": patient_data["description"]
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Penggunaan
patient_data = {
    "id": "P001234",
    "name": "DOE^JOHN",
    "birth_date": "19800115",
    "sex": "M",
    "accession_number": "ACC123456",
    "date": "20231201",
    "time": "083000",
    "description": "USG ABDOMEN"
}

result = create_worklist(patient_data)
print(f"Worklist created with ID: {result['ID']}")
```

## Keuntungan Menggunakan API vs DCMTK

### REST API (Orthanc)
- Lebih modern dan mudah diintegrasikan dengan aplikasi web
- Tidak memerlukan pemahaman mendalam tentang format DICOM biner
- Dapat dikontrol dari jarak jauh melalui HTTP
- Lebih fleksibel untuk integrasi dengan sistem lain

### DCMTK
- Standar industri untuk komunikasi DICOM
- Kontrol penuh atas semua aspek DICOM
- Tidak bergantung pada server tambahan
- Lebih kompatibel dengan peralatan medis yang ada

## Troubleshooting

### Error 404 Not Found
- Pastikan endpoint URL benar
- Verifikasi plugin worklists sudah terinstall

### Error 400 Bad Request
- Periksa format JSON yang dikirim
- Pastikan semua field yang diperlukan ada

### Worklist Tidak Muncul di Modality
- Verifikasi AE title sudah benar di konfigurasi modality
- Pastikan jaringan antara Orthanc dan modality terhubung
- Cek log Orthanc untuk error terkait

### Verifikasi Worklist di Orthanc
```bash
# Cek apakah worklist tersimpan
curl http://localhost:8042/tools/find -X POST -d '{
  "Level": "Patient",
  "Query": {"PatientName": "NAMA_PASIEN"}
}'
```



https://orthanc.uclouvain.be/book/plugins/worklists-plugin.html#troubleshooting-c-find-queries

https://www.dicomlibrary.com/dicom/modality/