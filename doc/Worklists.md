# Worklists Orthanc — Panduan Praktis

Dokumen ini menjelaskan cara membuat Worklist di Orthanc agar dapat diambil oleh alat USG (mis. LOGIQ F5), beserta prasyarat, contoh payload, konfigurasi modality, verifikasi, dan troubleshooting.

## Prasyarat

- Orthanc dan plugin Worklists aktif:
  - `docker-compose.yaml` mengaktifkan `MODALITY_WORKLISTS_PLUGIN_ENABLED: "true"` dan mount `./worklists`.
  - `orthanc.json` berisi:
    - `Worklists.Enable: true` dan `Worklists.Database: "/worklists"`.
    - `DicomAet: "ORTHANC"` dan `DicomPort: 4242` (port DICOM).
- Orthanc REST API aktif di `http://localhost:8042` (opsional `AuthenticationEnabled: false` saat pengujian).
- Alat USG berada pada jaringan yang sama dan dapat mengakses IP Orthanc; port DICOM `4242` terbuka.
- Verifikasi plugin: `curl http://localhost:8042/plugins` harus menampilkan plugin Worklists.

## Membuat Worklist (REST API — Disarankan)

- Endpoint: `POST http://localhost:8042/tools/create-dicom`
- Format JSON (minimal untuk MWL):
  - Tanggal `YYYYMMDD`, waktu `HHMMSS`.
  - `ScheduledStationAETitle` harus sama PERSIS dengan AE Title alat USG (contoh: `LOGIQF5`).
- Contoh `curl`:
  ```bash
  curl -X POST http://localhost:8042/tools/create-dicom \
    -H "Content-Type: application/json" \
    -d '{
      "PatientID": "US251027001",
      "PatientName": "TEST^PATIENT",
      "AccessionNumber": "ACC123456",
      "ScheduledProcedureStepSequence": {
        "ScheduledStationAETitle": "LOGIQF5",
        "ScheduledProcedureStepStartDate": "20231201",
        "ScheduledProcedureStepStartTime": "080000",
        "ScheduledProcedureStepDescription": "US ABDOMEN"
      }
    }'
  ```
- Contoh PowerShell (Windows):
  ```powershell
  Invoke-WebRequest -Uri http://localhost:8042/tools/create-dicom -Method POST -ContentType 'application/json' -Body '{
    "PatientID":"US251027001",
    "PatientName":"TEST^PATIENT",
    "AccessionNumber":"ACC123456",
    "ScheduledProcedureStepSequence":{
      "ScheduledStationAETitle":"LOGIQF5",
      "ScheduledProcedureStepStartDate":"20231201",
      "ScheduledProcedureStepStartTime":"080000",
      "ScheduledProcedureStepDescription":"US ABDOMEN"
    }
  }'
  ```
- Contoh Python: lihat `doc/WORKLIST-API.md` fungsi `create_worklist(patient_data)`.

## Kunci Payload yang Sukses

- `PatientID`, `PatientName`: isi sesuai HIS/RIS.
- `AccessionNumber`: penting untuk korelasi di modality.
- `ScheduledProcedureStepSequence`:
  - `ScheduledStationAETitle`: AE Title alat (mis. `LOGIQF5`).
  - `ScheduledProcedureStepStartDate`: `YYYYMMDD` (mis. `20231201`).
  - `ScheduledProcedureStepStartTime`: `HHMMSS` (mis. `083000`).
  - `ScheduledProcedureStepDescription`: deskripsi (mis. `US ABDOMEN`).

## Alternatif: File System Worklists (Legacy)

- Letakkan file DICOM Worklist di folder `./worklists` (di-mount ke Orthanc `"/worklists"`).
- Plugin Worklists menyajikan entri dari folder ini.
- Lebih terbatas dibanding REST API (kurang fleksibel untuk integrasi web).

## Konfigurasi Alat USG (LOGIQ F5)

- Storage/PACS (untuk kirim hasil):
  - `Destination AE Title`: `ORTHANC`
  - `Destination IP`: `<IP Orthanc>`
  - `Destination Port`: `4242`
- Worklist Query (Provider):
  - `AE Title`: `ORTHANC` (atau sesuai server MWL yang merespon).
  - `Provider IP`: `<IP Orthanc>`
  - `Provider Port`: `4242`
- Pastikan AE Title pada payload `ScheduledStationAETitle` cocok dengan AE Title alat (mis. `LOGIQF5`). Banyak modality hanya menampilkan worklist yang “ditujukan” untuk AE Title mereka.
- Uji koneksi:
  - Jalankan C‑ECHO dari USG ke Orthanc (harus sukses).
  - Masuk menu Worklist di USG, lakukan Query/Refresh, pastikan entri muncul.

## Verifikasi di Orthanc

- Health check: `GET http://localhost:8042/system` → 200 OK.
- Cek plugin: `GET http://localhost:8042/plugins`.
- Cek entri lewat `tools/find` (opsional, sesuai kebutuhan):
  ```bash
  curl http://localhost:8042/tools/find -X POST -H "Content-Type: application/json" -d '{
    "Level": "Patient",
    "Query": {"PatientName": "TEST*"}
  }'
  ```
- Cek daftar objek: `GET http://localhost:8042/patients`.

## Troubleshooting

- Worklist tidak muncul di modality:
  - AE Title pada `ScheduledStationAETitle` tidak cocok dengan AE alat.
  - Alat meng‑query ke IP/Port yang salah (default Orthanc DICOM: `4242`).
  - Masalah jaringan (firewall/NAT); pastikan port terbuka.
  - Plugin Worklists tidak aktif; cek `GET /plugins`.
- Error 400 (Bad Request):
  - Format tanggal/waktu salah (`YYYYMMDD`, `HHMMSS`).
  - Field wajib hilang (`PatientID`, `PatientName`, `ScheduledProcedureStepSequence`).
- Error 404:
  - Endpoint salah atau plugin belum aktif.

## Best Practices

- Gunakan REST API untuk pembuatan real‑time dari frontend/backend; lebih mudah diautomasi.
- Simpan mapping HIS/RIS ke DICOM tags (ID pasien, accession, deskripsi) agar payload konsisten.
- Amankan Orthanc REST (aktifkan `AuthenticationEnabled`) dan gunakan Basic Auth di backend/proxy.
- Dokumentasikan AE Title, IP, dan port di alat dan server untuk audit.