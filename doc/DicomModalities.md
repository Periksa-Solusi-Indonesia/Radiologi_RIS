# Penjelasan DicomModalities (Orthanc)

Dokumen ini menjelaskan apa itu `DicomModalities` di Orthanc, bagaimana cara mengonfigurasinya, serta contoh penggunaan melalui REST API untuk operasi DICOM umum (C‑ECHO, C‑STORE, C‑FIND, C‑MOVE).

## Ringkasan Fungsi
- `DicomModalities` mendefinisikan daftar perangkat/servis DICOM eksternal yang dapat dihubungi oleh Orthanc sebagai **klien (SCU)**.
- Setiap entri berisi **AE Title**, **IP**, dan **port** dari perangkat target.
- Orthanc menggunakan daftar ini untuk menjalankan operasi aktif ke perangkat lain:
  - C‑ECHO (test koneksi)
  - C‑STORE (mengirim gambar/studi)
  - C‑FIND (query metadata/studi)
  - C‑MOVE (retrieve studi dari PACS ke Orthanc)
- Catatan: Perangkat yang **menghubungi Orthanc** (Orthanc sebagai **server/SCP**) tidak wajib didefinisikan di sini. `DicomModalities` diperlukan ketika **Orthanc yang menginisiasi** komunikasi ke perangkat lain.

## Struktur Konfigurasi
Contoh di `orthanc.json`:
```json
{
  "DicomModalities": {
    "PACS_SERVER": ["PACS_SERVER", "127.0.0.1", 4242],
    "SIMULATOR": ["WLM_SCP", "127.0.0.1", 11112],
    "ORTHANC": ["ORTHANC", "127.0.0.1", 4242]
  }
}
```
Format setiap item: `"<label>": ["<AE Title>", "<IP>", <port>]`
- `label`: nama alias (bebas) untuk referensi di REST API (misal `/modalities/<label>/echo`).
- `AE Title`: identitas DICOM perangkat target (harus cocok dengan konfigurasi perangkat).
- `IP` & `port`: alamat dan port DICOM target.

## Operasi REST Terkait Modalities
Semua contoh menggunakan `curl` ke Orthanc: `http://localhost:8042`. Jika autentikasi Orthanc diaktifkan, tambahkan `-u user:password`.

### 1) C‑ECHO (Test Koneksi)
```bash
curl -X POST http://localhost:8042/modalities/PACS_SERVER/echo
```
- Hasil `200 OK` menandakan Orthanc dapat berkomunikasi dengan target AE.

### 2) C‑STORE (Kirim Studi/Gambar)
Kirim instance/studi yang ada di Orthanc ke modality/PACS target.
```bash
# Kirim seluruh instances dari sebuah study ID Orthanc
curl -X POST http://localhost:8042/modalities/PACS_SERVER/store \
  -H "Content-Type: application/json" \
  -d '{ "Resources": [ { "Type": "Study", "ID": "<ORTHANC_STUDY_ID>" } ] }'
```
- Ganti `<ORTHANC_STUDY_ID>` dengan ID study di Orthanc (UUID internal Orthanc).

### 3) C‑FIND (Query)
Melakukan query metadata (misal level Study/Patient) ke modality target.
```bash
curl -X POST http://localhost:8042/modalities/PACS_SERVER/query \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Study",
    "Query": {
      "PatientName": "DOE*",
      "StudyDate": "20240101-20241231"
    }
  }'
```
- Response berisi daftar referensi hasil query.

### 4) C‑MOVE (Retrieve)
Retrieve hasil C‑FIND dari PACS ke Orthanc.
```bash
curl -X POST http://localhost:8042/modalities/PACS_SERVER/move \
  -H "Content-Type: application/json" \
  -d '{
    "Level": "Study",
    "Query": {
      "AccessionNumber": "ACC123456"
    }
  }'
```
- Study yang cocok akan ditransfer ke Orthanc.

## Keterkaitan dengan Worklist (MWL)
- Untuk **Modality Worklist**: biasanya alat (mis. USG) melakukan **C‑FIND ke Orthanc** (Orthanc bertindak sebagai **SCP**) dan Orthanc menjawab daftar Worklist.
- `DicomModalities` **tidak wajib** agar alat dapat melakukan query ke Orthanc. Namun, berguna jika Anda ingin Orthanc **berkomunikasi balik** (mis. uji C‑ECHO ke alat, atau mengirim hasil ke PACS lain).
- Pastikan **AE Title konsisten**:
  - Payload Worklist `ScheduledStationAETitle` harus sama dengan AE Title alat (contoh `LOGIQF5`).
  - Jika Anda menambahkan alat ke `DicomModalities`, AE Title di entri tersebut juga harus sama.

## Contoh Entri untuk LOGIQ F5
Tambahkan di `orthanc.json`:
```json
{
  "DicomModalities": {
    "LOGIQF5": ["LOGIQF5", "192.168.1.100", 104]
  }
}
```
Uji koneksi:
```bash
curl -X POST http://localhost:8042/modalities/LOGIQF5/echo
```
Jika OK, Orthanc dapat berkomunikasi ke alat tersebut (SCU → SCP).

## Tips & Troubleshooting
- **Firewall/Network**: pastikan port DICOM terbuka (`4242` untuk Orthanc; banyak perangkat memakai `104`).
- **AE Title mismatch** adalah penyebab umum kegagalan C‑ECHO/MWL; pastikan sama persis di kedua sisi.
- **Timeouts**: sesuaikan `DicomScuTimeout`, `DicomScpTimeout` jika perlu.
- **Plugin**: verifikasi plugin yang diperlukan aktif (`GET /plugins`).
- **Log**: cek log Orthanc untuk detail error saat operasi DICOM.

## Best Practices
- Tetapkan penamaan `label` yang deskriptif untuk memudahkan automasi.
- Simpan kredensial dan konfigurasi di environment/berkas terpisah (hindari hard‑code IP/port di kode aplikasi).
- Gunakan REST API Orthanc untuk orkestrasi (uji echo, kirim studi, retrieve) dari sistem HIS/RIS atau backend.
- Untuk Worklist, buat entri lewat REST (`POST /tools/create-dicom`) dan konsistenkan AE Title pada `ScheduledStationAETitle`.

## Referensi
- Dokumentasi REST: https://book.orthanc-server.com/users/rest.html
- Worklists Plugin: https://orthanc.uclouvain.be/book/plugins/worklists-plugin.html