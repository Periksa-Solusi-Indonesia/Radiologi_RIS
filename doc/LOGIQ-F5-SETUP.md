# Panduan Konfigurasi LOGIQ F5 dengan Orthanc

## Overview
Dokumen ini menjelaskan cara mengkonfigurasi alat USG GE LOGIQ F5 untuk:
1. Menerima Worklist dari Orthanc Server
2. Mengirim gambar DICOM ke Orthanc PACS

---

## Prerequisites

### Informasi Network yang Dibutuhkan
- **IP Address LOGIQ F5**: `192.168.1.100` (sesuaikan dengan IP aktual)
- **IP Address Orthanc Server**: `<IP_SERVER_ANDA>`
- **Port DICOM Orthanc**: `4242`
- **Port DICOM LOGIQ F5**: `104` (default)

### Konfigurasi yang Sudah Dilakukan di Orthanc
✅ Worklist Plugin enabled
✅ LOGIQF5 terdaftar di DicomModalities
✅ AE Title Orthanc: `ORTHANC`
✅ AE Title LOGIQ F5: `LOGIQF5`
✅ Python script untuk generate worklist

---

## Konfigurasi di LOGIQ F5

### 1. Konfigurasi Worklist Server

Worklist memungkinkan LOGIQ F5 untuk mengambil data pasien dari Orthanc.

**Langkah-langkah:**

1. Masuk ke menu **Setup/Configuration** di LOGIQ F5
2. Navigasi ke **DICOM** → **Worklist Settings**
3. Masukkan konfigurasi berikut:

```
Worklist Server Settings:
├─ Enable Worklist: YES
├─ Server AE Title: ORTHANC
├─ Server IP Address: <IP_ORTHANC_SERVER>
├─ Server Port: 4242
├─ Local AE Title: LOGIQF5
└─ Query Mode: C-FIND
```

4. Test koneksi dengan tombol **Test/Verify**
5. Save konfigurasi

### 2. Konfigurasi Storage Server (PACS)

Storage server memungkinkan LOGIQ F5 mengirim gambar ke Orthanc.

**Langkah-langkah:**

1. Masuk ke **Setup** → **DICOM** → **Storage Settings**
2. Tambahkan Destination baru:

```
Storage Destination: ORTHANC
├─ Destination AE Title: ORTHANC
├─ Destination IP: <IP_ORTHANC_SERVER>
├─ Destination Port: 4242
├─ Local AE Title: LOGIQF5
├─ Store Mode: Automatic/Manual
└─ Compression: None (atau Lossless)
```

3. Test koneksi dengan **C-ECHO**
4. Save konfigurasi

### 3. Konfigurasi Network (jika belum)

**Langkah-langkah:**

1. Masuk ke **Setup** → **Network Settings**
2. Konfigurasi:

```
Network Configuration:
├─ IP Address: 192.168.1.100 (static)
├─ Subnet Mask: 255.255.255.0
├─ Gateway: <IP_GATEWAY>
└─ DNS: <IP_DNS>
```

3. Pastikan LOGIQ F5 dan Orthanc Server dalam network yang sama atau routable

---

## Penggunaan Worklist

### Workflow

1. **Generate Worklist di Server**
   ```bash
   cd radiology-cron
   python3 main.py
   ```

2. **Query Worklist di LOGIQ F5**
   - Buka aplikasi USG
   - Pilih menu **Patient** atau **Worklist**
   - Klik **Query** atau **Refresh**
   - Daftar pasien akan muncul dari Orthanc

3. **Pilih Pasien**
   - Pilih pasien dari daftar worklist
   - Data pasien otomatis terisi (Nama, ID, Accession Number, dll)
   - Mulai pemeriksaan USG

4. **Kirim Hasil ke PACS**
   - Setelah pemeriksaan selesai
   - Pilih **Send** atau **Store**
   - Pilih destination: **ORTHANC**
   - Images akan dikirim ke Orthanc PACS

---

## Troubleshooting

### Worklist Tidak Muncul

**Cek di LOGIQ F5:**
- Pastikan koneksi network aktif
- Test koneksi ke Orthanc (C-ECHO)
- Periksa AE Title sudah benar (LOGIQF5 ↔ ORTHANC)
- Cek filter query (tanggal, modality)

**Cek di Orthanc Server:**
```bash
# Cek apakah worklist files ada
ls -l worklists/

# Cek log Orthanc
docker logs -f orthanc

# Generate ulang worklist
cd radiology-cron
python3 main.py
```

### Tidak Bisa Kirim Gambar

**Cek di LOGIQ F5:**
- Test C-ECHO ke ORTHANC
- Pastikan IP dan port benar
- Cek storage mode (auto/manual)

**Cek di Orthanc:**
```bash
# Cek Orthanc berjalan
docker ps | grep orthanc

# Cek port 4242 terbuka
netstat -an | grep 4242

# Cek log
docker logs -f orthanc
```

### Network Connection Failed

1. **Ping Test**
   ```bash
   # Dari server ke LOGIQ F5
   ping 192.168.1.100
   ```

2. **Port Test**
   ```bash
   # Test DICOM port dari LOGIQ F5
   telnet <IP_ORTHANC> 4242
   ```

3. **Firewall**
   - Pastikan port 4242 terbuka di firewall server
   - Disable firewall sementara untuk testing

---

## File Konfigurasi

### orthanc.json (di Server)
```json
{
  "DicomModalities": {
    "LOGIQF5": ["LOGIQF5", "192.168.1.100", 104]
  },
  "DicomAet": "ORTHANC",
  "DicomPort": 4242,
  "Worklists": {
    "Enable": true,
    "Database": "/worklists"
  }
}
```

### config.json (Python Script)
```json
{
  "default_ae_titles": {
    "US": "LOGIQF5"
  },
  "network": {
    "logiq_f5_ip": "192.168.1.100",
    "logiq_f5_port": 104,
    "orthanc_ae_title": "ORTHANC",
    "orthanc_port": 4242
  }
}
```

---

## Testing Checklist

- [ ] Network connectivity (ping)
- [ ] DICOM port accessible (telnet)
- [ ] C-ECHO successful dari LOGIQ F5 ke Orthanc
- [ ] Worklist query berhasil
- [ ] Data pasien muncul dengan benar
- [ ] C-STORE gambar berhasil
- [ ] Gambar tersimpan di Orthanc PACS

---

## Contact & Support

Untuk pertanyaan lebih lanjut:
- Dokumentasi Orthanc: https://book.orthanc-server.com/
- GE LOGIQ F5 Manual: Lihat dokumentasi alat
- Project Repository: [link repo]

---

**Update:** 2 Oktober 2025
**Version:** 1.0
