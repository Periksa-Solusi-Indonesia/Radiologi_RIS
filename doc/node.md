# Panduan Worklist Orthanc (Node.js)

Dokumen ini menjelaskan cara membuat entri Worklist di Orthanc melalui REST API menggunakan Node.js, agar dapat diambil oleh alat USG (mis. LOGIQ F5).

## Ringkasan Alur
- Backend/skrip membuat Worklist lewat `POST /tools/create-dicom` di Orthanc.
- Alat USG melakukan query MWL (Modality Worklist) ke Orthanc melalui DICOM port.
- Worklist yang cocok (AE Title, waktu, dsb.) akan muncul di alat USG untuk dipilih.

## Prasyarat
- Orthanc aktif dan plugin Worklists di-enable.
  - `docker-compose.yaml` sudah mengaktifkan `MODALITY_WORKLISTS_PLUGIN_ENABLED: "true"` dan mount folder `./worklists`.
  - `orthanc.json` berisi:
    - `Worklists.Enable: true`, `Worklists.Database: "/worklists"`
    - `DicomAet: "ORTHANC"`, `DicomPort: 4242`, `HttpPort: 8042`
- Jaringan alat USG ↔ Orthanc tersambung, port `4242` terbuka.
- Untuk pengujian, `AuthenticationEnabled` dapat `false`. Jika `true`, gunakan Basic Auth.

## Field Penting Payload
- `PatientID` dan `PatientName`: identitas pasien (format DICOM nama: `LAST^FIRST`).
- `AccessionNumber`: nomor pemeriksaan (penting untuk korelasi).
- `ScheduledProcedureStepSequence`:
  - `ScheduledStationAETitle`: harus sama dengan AE Title alat USG (contoh: `LOGIQF5`).
  - `ScheduledProcedureStepStartDate`: `YYYYMMDD` (mis. `20231201`).
  - `ScheduledProcedureStepStartTime`: `HHMMSS` (mis. `083000`).
  - `ScheduledProcedureStepDescription`: deskripsi prosedur (mis. `US ABDOMEN`).

## Contoh Payload
```json
{
  "PatientID": "US251027001",
  "PatientName": "TEST^PATIENT",
  "AccessionNumber": "ACC123456",
  "ScheduledProcedureStepSequence": {
    "ScheduledStationAETitle": "LOGIQF5",
    "ScheduledProcedureStepStartDate": "20231201",
    "ScheduledProcedureStepStartTime": "080000",
    "ScheduledProcedureStepDescription": "US ABDOMEN"
  }
}
```

## Implementasi dengan Node.js (fetch)
Node 18+ memiliki `fetch` global. Contoh sederhana:

```js
// create-worklist.js
const ORTHANC_BASE = process.env.ORTHANC_BASE || 'http://localhost:8042';
// Jika Orthanc memakai auth:
// const AUTH = 'Basic ' + Buffer.from('admin:admin123').toString('base64');

async function createWorklist(payload) {
  const res = await fetch(`${ORTHANC_BASE}/tools/create-dicom`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': AUTH,
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed: ${res.status} ${res.statusText} - ${text}`);
  }

  return res.json();
}

(async () => {
  try {
    const payload = {
      PatientID: 'US251027001',
      PatientName: 'TEST^PATIENT',
      AccessionNumber: 'ACC123456',
      ScheduledProcedureStepSequence: {
        ScheduledStationAETitle: 'LOGIQF5',
        ScheduledProcedureStepStartDate: '20231201',
        ScheduledProcedureStepStartTime: '080000',
        ScheduledProcedureStepDescription: 'US ABDOMEN',
      },
    };

    const result = await createWorklist(payload);
    console.log('Worklist created:', result);
  } catch (err) {
    console.error('Error:', err);
    process.exit(1);
  }
})();
```

Jalankan:
```
node create-worklist.js
```

## Alternatif dengan Axios
Jika ingin memakai `axios`:

```js
// create-worklist-axios.js
import axios from 'axios';

const client = axios.create({
  baseURL: process.env.ORTHANC_BASE || 'http://localhost:8042',
  headers: {
    'Content-Type': 'application/json',
    // Authorization: 'Basic ' + Buffer.from('admin:admin123').toString('base64'),
  },
});

async function createWorklist(payload) {
  const { data } = await client.post('/tools/create-dicom', payload);
  return data;
}

(async () => {
  try {
    const payload = {
      PatientID: 'US251027002',
      PatientName: 'DOE^JOHN',
      AccessionNumber: 'ACC654321',
      ScheduledProcedureStepSequence: {
        ScheduledStationAETitle: 'LOGIQF5',
        ScheduledProcedureStepStartDate: '20231202',
        ScheduledProcedureStepStartTime: '090000',
        ScheduledProcedureStepDescription: 'US THYROID',
      },
    };
    const result = await createWorklist(payload);
    console.log('Worklist created:', result);
  } catch (err) {
    console.error('Error:', err?.response?.data || err.message);
    process.exit(1);
  }
})();
```

## Verifikasi
- Cek Orthanc REST:
  - `GET http://localhost:8042/system` → harus 200 OK.
- Cek plugin:
  - `GET http://localhost:8042/plugins`
- Cari entri lewat `tools/find` jika perlu (lihat `doc/WORKLIST-API.md`).

## Konfigurasi Alat USG (LOGIQ F5)
- Storage/PACS:
  - AE Title: `ORTHANC`, IP Orthanc, Port `4242`.
- Worklist Provider:
  - AE Title: `ORTHANC` (atau sesuai server MWL), IP Orthanc, Port `4242`.
- Pastikan `ScheduledStationAETitle` pada payload sama dengan AE Title alat (`LOGIQF5`).
- Uji C-ECHO, lalu Query/Refresh Worklist di alat.

## Troubleshooting
- Tidak muncul di Worklist:
  - AE Title tidak cocok; cek `ScheduledStationAETitle`.
  - Format tanggal/waktu salah; gunakan `YYYYMMDD`, `HHMMSS`.
  - Jaringan/firewall blok port `4242`.
  - Plugin Worklists tidak aktif.
- 400 Bad Request:
  - Field wajib hilang atau format JSON tidak valid.
- 404 Not Found:
  - Endpoint salah atau plugin belum aktif.

## Best Practice
- Gunakan REST API untuk pembuatan real-time dari sistem HIS/RIS atau frontend/back-end.
- Tambahkan backend proxy (Next.js API route) untuk menghindari CORS dan mengelola kredensial Orthanc.
- Pertimbangkan aktivasi `AuthenticationEnabled` dan gunakan Basic Auth pada integrasi.

Referensi tambahan: lihat `doc/WORKLIST-API.md` dan `doc/LOGIQ-F5-SETUP.md` untuk detail payload dan konfigurasi modality.