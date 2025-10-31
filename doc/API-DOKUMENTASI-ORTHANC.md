# Dokumentasi API Orthanc (Referensi Cepat)

Dokumen ini merangkum endpoint REST API Orthanc yang paling berguna, contoh pemakaian, dan catatan penting untuk integrasi aplikasi. Cocok untuk kebutuhan PACS/Worklist dan integrasi modality.

## Ringkasan
- Basis URL default: `http://localhost:8042`
- Format: HTTP + JSON
- Status auth saat ini: `AuthenticationEnabled = false` (tidak butuh login). Jika diaktifkan, gunakan Basic Auth.
- Versi image: `orthancteam/orthanc:latest-full` (include plugin umum seperti DICOMweb)

## Konfigurasi & Keamanan
- Auth: Jika diaktifkan, gunakan `curl -u user:pass ...` atau header `Authorization: Basic ...`.
- Remote access: Pastikan `RemoteAccessAllowed` sesuai kebutuhan.
- Production: Hindari `POST /tools/reset` di jam layanan.

## Endpoint Inti
- `GET /patients` — Daftar pasien
- `GET /studies` — Daftar studi
- `GET /series` — Daftar series
- `GET /instances` — Daftar instance
- `GET /patients/{id}` — Detail pasien
- `GET /studies/{id}` — Detail studi
- `GET /series/{id}` — Detail series
- `GET /instances/{id}` — Detail instance

Contoh ambil tags instance:
```bash
curl http://localhost:8042/instances/{INSTANCE_ID}/tags
```

## Endpoint Tools (Paling Sering Dipakai)
- `GET /tools/now` — Waktu server (ISO 8601)
- `GET /tools/generate-uid?level={Study|Series|Instance}` — Generate UID DICOM
- `GET /tools/dicom-conformance` — Conformance statement
- `POST /tools/create-dicom` — Buat objek DICOM dari JSON (dipakai untuk Worklist)
- `POST /tools/find` — Cari resource lokal berdasarkan DICOM tags
- `POST /tools/lookup` — Map DICOM UIDs ke Orthanc IDs
- `POST /tools/execute-script` — Eksekusi Lua (gunakan dengan hati-hati)
- `POST /tools/reset` — Hot restart Orthanc (reload config)

Contoh create worklist sederhana:
```bash
curl -X POST http://localhost:8042/tools/create-dicom \
  -H "Content-Type: application/json" \
  -d '{
    "Tags": {
      "PatientID": "PID-001",
      "PatientName": "DOE^JOHN",
      "PatientBirthDate": "19800115",
      "PatientSex": "M",
      "AccessionNumber": "ACC123",
      "ScheduledProcedureStepSequence": [
        {
          "Modality": "US",
          "ScheduledProcedureStepStartDate": "20251201",
          "ScheduledProcedureStepDescription": "US ABDOMEN"
        }
      ]
    }
  }'
```

Contoh find pasien:
```bash
curl -X POST http://localhost:8042/tools/find \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Patient",
    "Query": { "PatientName": "DOE^JOHN" }
  }'
```

## Modalities (DICOM C-STORE/C-FIND/C-MOVE/C-GET)
Pastikan modality terdaftar di `DicomModalities` dalam `orthanc.json`.

- `POST /modalities/{NAME}/echo` — C-ECHO (tes koneksi)
- `POST /modalities/{NAME}/store` — Kirim resource ke modality (C-STORE)
- `POST /modalities/{NAME}/query` — C-FIND terhadap modality
- `POST /queries/{QUERY_ID}/retrieve` — Retrieve (C-MOVE atau C-GET)

Contoh echo:
```bash
curl -X POST http://localhost:8042/modalities/LOGIQF5/echo
```

Contoh store satu instance:
```bash
curl -X POST http://localhost:8042/modalities/LOGIQF5/store \
  -H "Content-Type: application/json" \
  -d '{ "Resources": ["{INSTANCE_ID}"] }'
```

Contoh query studi di modality:
```bash
curl -X POST http://localhost:8042/modalities/LOGIQF5/query \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Study",
    "Query": { "StudyDate": "20250101-" }
  }'
```

## DICOMweb (QIDO-RS, WADO-RS, STOW-RS)
Dengan image `latest-full`, DICOMweb umumnya tersedia:
- `GET /dicom-web/studies` — QIDO-RS query studi
- `GET /dicom-web/studies/{StudyInstanceUID}` — WADO-RS retrieve meta
- `POST /dicom-web/studies` — STOW-RS upload DICOM (multipart)

Contoh QIDO studi:
```bash
curl "http://localhost:8042/dicom-web/studies?PatientName=DOE*"
```

## Worklists
- Konfigurasi: lihat `orthanc.json` bagian `Worklists`.
- Cara buat via REST: lihat `doc/WORKLIST-API.md` (detail lengkap & contoh).

## Plugins
- `GET /plugins` — Daftar plugin aktif
- Beberapa fitur (Worklists, DICOMweb) tersedia via plugin

## Catatan PowerShell (Windows)
- Hindari single quotes; gunakan double quotes sesuai contoh.
- Untuk body JSON kompleks, gunakan `ConvertTo-Json` di PowerShell.

## Referensi
- Orthanc REST API (resmi):
  `https://orthanc.uclouvain.be/book/users/rest.html#sending-resources-to-remote-modalities-through-dicom-c-store`
- Dokumen internal: `doc/WORKLIST-API.md`, `doc/REFERENCES.md`

---
Terakhir diperbarui: otomatis oleh repo ini. Jika butuh endpoint tambahan atau contoh bahasa tertentu (JS/Python/PowerShell), beri tahu, akan saya tambah.