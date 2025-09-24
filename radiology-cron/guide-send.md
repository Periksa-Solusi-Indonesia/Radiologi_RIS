# Analisis File main.py - Generator DICOM Worklist

## Import dan Setup (Baris 1-10)
```python
import os, datetime, json, logging
from pydicom.dataset import FileDataset
import pydicom
```
- **Fungsi**: Import library untuk manipulasi file, tanggal, JSON, logging, dan DICOM
- **Modality**: Semua modality menggunakan library yang sama

## Konfigurasi Logging (Baris 8-10)
```python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```
- **Fungsi**: Setup logging untuk monitoring proses
- **Modality**: Log yang sama untuk semua modality

## Path dan Konfigurasi Default (Baris 12-26)
```python
DEFAULT_CONFIG = {
    "default_modalities": ["CT", "MR", "XR", "US"],
    "default_ae_titles": {
        "CT": "CT01",
        "MR": "MR01", 
        "XR": "XR01",
        "US": "US01"
    }
}
```
- **Fungsi**: Definisi modality yang didukung dan AE Title masing-masing
- **Modality Specific**: 
  - **CT**: AE Title "CT01"
  - **MR**: AE Title "MR01" 
  - **XR**: AE Title "XR01"
  - **US**: AE Title "US01"

## Fungsi load_config() (Baris 28-36)
- **Fungsi**: Load konfigurasi dari file atau buat default
- **Modality**: Konfigurasi berlaku untuk semua modality

## Fungsi get_his_data() (Baris 38-62)
- **Fungsi**: Simulasi data dari HIS/RIS (perlu diganti dengan API real)
- **Modality Specific**:
  - **CT**: Study "CT THORAX CONTRAST", waktu 08:15
  - **MR**: Study "MR BRAIN", waktu 09:00

## Fungsi generate_worklist_dcm() (Baris 64-98)
**Bagian penting yang disesuaikan per modality:**

```python
# Modality-specific fields
sps_item.Modality = order.get('modality', 'CT')  # CT/MR/XR/US
sps_item.ScheduledStationAETitle = order.get('ae_title', 'CT01')  # Sesuai modality
```

**DICOM Tags yang disesuaikan:**
- **Modality**: Menentukan jenis pemeriksaan (CT/MR/XR/US)
- **ScheduledStationAETitle**: AE Title sesuai alat modality
- **ScheduledProcedureStepDescription**: Deskripsi pemeriksaan sesuai modality

## Fungsi cleanup_old_worklists() (Baris 100-116)
- **Fungsi**: Hapus worklist > 24 jam
- **Modality**: Berlaku untuk semua modality

## Fungsi main() (Baris 118-140)
- **Fungsi**: Eksekusi utama - generate worklist untuk semua order
- **Modality**: Proses semua modality dalam satu run

## Yang Perlu Disesuaikan per Modality:

1. **AE Titles**: Sesuaikan dengan nama alat aktual
2. **Study Descriptions**: Sesuaikan dengan protokol pemeriksaan
3. **Scheduling**: Waktu operasional berbeda per modality
4. **Integration**: API HIS/RIS untuk data real-time
5. **DICOM Tags**: Tag tambahan spesifik modality jika diperlukan

## Contoh Kustomisasi per Modality

### CT Scanner
```python
"CT": {
    "ae_title": "SIEMENS_CT01",
    "protocols": ["CT HEAD", "CT THORAX", "CT ABDOMEN"],
    "contrast_options": ["PLAIN", "CONTRAST", "DUAL_PHASE"]
}
```

### MRI
```python
"MR": {
    "ae_title": "PHILIPS_MR01", 
    "protocols": ["MR BRAIN", "MR SPINE", "MR KNEE"],
    "sequences": ["T1", "T2", "FLAIR", "DWI"]
}
```

### X-Ray
```python
"XR": {
    "ae_title": "CANON_XR01",
    "protocols": ["CHEST PA", "ABDOMEN", "EXTREMITY"],
    "positions": ["PA", "AP", "LATERAL", "OBLIQUE"]
}
```

### Ultrasound
```python
"US": {
    "ae_title": "GE_US01",
    "protocols": ["USG ABDOMEN", "USG PELVIS", "ECHO"],
    "probes": ["CONVEX", "LINEAR", "PHASED_ARRAY"]
}
```
