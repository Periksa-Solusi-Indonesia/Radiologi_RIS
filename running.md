# Integrasi Orthanc dengan Alat USG melalui Modality Worklist (MWL)

Panduan ini menjelaskan langkah-langkah menghubungkan sistem PACS Orthanc ke alat USG yang mendukung Modality Worklist (C-FIND).

---

## ✅ Prasyarat

- Orthanc sudah berjalan dan plugin Modality Worklist aktif
- Folder `./worklists/` berisi file `.dcm` worklist valid
- Alat USG memiliki fitur **MWL Client / C-FIND SCU**
- `findscu` (DCMTK) dapat digunakan untuk tes lokal

---

## 🧩 1. Konfigurasi DICOM pada Alat USG

Masukkan pengaturan berikut di menu DICOM / Network Setting alat USG:

| Parameter               | Nilai                                |
|------------------------|----------------------------------------|
| **Remote AE Title**    | `ORTHANC` *(default AE Orthanc)*       |
| **Server IP Address**  | IP server tempat Orthanc berjalan      |
| **Port**               | `4242` *(default port DICOM Orthanc)*  |
| **Local AE Title**     | `USG01` *(bebas, tapi harus konsisten)*|

---

## 🛠️ 2. Tambahkan AE USG ke File `orthanc.json`

Edit `orthanc.json` agar Orthanc mengizinkan koneksi dari AE `USG01`:

```json
"DicomModalities": {
  "USG01": ["USG01", "192.168.0.150", 4242]
}
Ganti 192.168.0.150 dengan IP alat USG kamu.