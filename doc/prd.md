### Product Requirements Document (PRD): Orthanc DICOM Server

Berikut adalah contoh PRD (Product Requirements Document) untuk implementasi server Orthanc DICOM yang dirancang untuk menyimpan data DICOM dan mengirim worklist ke modalitas (alat pencitraan medis).

---

### 1. Pendahuluan

#### 1.1. Tujuan
Dokumen ini menjelaskan persyaratan fungsional dan non-fungsional untuk membangun dan mengimplementasikan server DICOM menggunakan Orthanc. Proyek ini bertujuan untuk menyediakan solusi yang efisien untuk penyimpanan arsip gambar medis (PACS) dan manajemen worklist, mendukung alur kerja pencitraan medis yang terintegrasi.

#### 1.2. Cakupan Proyek
Sistem ini akan:
* Berfungsi sebagai arsip sentral untuk data DICOM.
* Menyimpan studi DICOM yang dikirim dari modalitas.
* Mengirim Worklist ke modalitas yang meminta.
* Menyediakan antarmuka web untuk manajemen data.

---

### 2. Persyaratan Fungsional

#### 2.1. Penyimpanan PACS
* Sistem harus dapat menerima dan menyimpan studi DICOM dari modalitas mana pun menggunakan protokol C-STORE SCU/SCP.
* Setiap studi harus disimpan dengan metadata DICOM lengkap (misalnya, nama pasien, ID, tanggal studi, modalitas).
* Sistem harus mampu mengidentifikasi dan menolak studi DICOM yang tidak valid atau rusak.

#### 2.2. Worklist Management
* Sistem harus dapat menanggapi permintaan Worklist dari modalitas (C-FIND SCU/SCP).
* Informasi Worklist (nama pasien, ID, studi yang diminta, dll.) harus berasal dari sumber eksternal (misalnya, sistem HIS/RIS).
* Sistem harus dapat mengirimkan informasi Worklist yang relevan sesuai dengan parameter yang diminta oleh modalitas (misalnya, berdasarkan tanggal atau ID pasien).
* Sistem harus dapat menyimpan log permintaan Worklist untuk tujuan audit.

#### 2.3. Antarmuka Pengguna (Web)
* Antarmuka web harus menyediakan fitur pencarian studi berdasarkan metadata (nama pasien, ID, tanggal).
* Pengguna harus dapat melihat detail metadata dari setiap studi.
* Antarmuka harus memungkinkan pengguna untuk menghapus atau mengarsipkan studi.
* Antarmuka harus menyediakan manajemen Worklist, memungkinkan pengguna untuk melihat atau mengedit entri Worklist (jika diperlukan).

---

### 3. Persyaratan Non-Fungsional

#### 3.1. Performa
* Sistem harus dapat menangani setidaknya **50 studi DICOM per jam** selama jam sibuk.
* Waktu respons untuk permintaan Worklist tidak boleh lebih dari **2 detik**.
* Waktu pengambilan gambar studi DICOM dari server tidak boleh lebih dari **10 detik**.

#### 3.2. Keamanan
* Akses ke antarmuka web Orthanc harus dilindungi dengan autentikasi (nama pengguna dan kata sandi).
* Akses ke Orthanc API harus diamankan.
* Komunikasi dengan modalitas harus menggunakan mekanisme keamanan yang relevan jika tersedia.

#### 3.3. Skalabilitas dan Ketersediaan
* Arsitektur sistem harus dapat ditingkatkan untuk mengakomodasi pertumbuhan volume data di masa depan.
* Sistem harus memiliki rencana pencadangan (backup) data DICOM secara teratur.
* Sistem harus memiliki ketersediaan setidaknya **99%**.

#### 3.4. Integrasi
* Sistem harus dapat terintegrasi dengan sistem informasi rumah sakit (HIS/RIS) untuk mendapatkan data Worklist.
* Integrasi ini akan dilakukan melalui API yang telah ditentukan.

---

### 4. Implementasi

#### 4.1. Arsitektur Teknis
* **Aplikasi Utama:** Orthanc DICOM Server
* **Basis Data:** PostgreSQL (direkomendasikan untuk skalabilitas dan integritas data)
* **Penyimpanan Data:** Penyimpanan lokal, SAN, atau NAS untuk data studi DICOM.
* **Plugin:** Penggunaan plugin Orthanc seperti `orthanc-postgresql` untuk basis data dan `orthanc-worklists` untuk manajemen worklist.
* 

#### 4.2. Rencana Implementasi
* **Tahap 1:** Instalasi dan konfigurasi dasar Orthanc.
* **Tahap 2:** Konfigurasi Worklist SCP dengan plugin terkait dan integrasi dengan sumber data HIS/RIS.
* **Tahap 3:** Pengujian end-to-end, termasuk pengiriman studi dari modalitas dan pengiriman Worklist ke modalitas.
* **Tahap 4:** Implementasi kebijakan keamanan dan pencadangan (backup).
* **Tahap 5:** Peluncuran dan monitoring.

---

### 5. Definisi dan Akronim

* **DICOM:** Digital Imaging and Communications in Medicine.
* **PACS:** Picture Archiving and Communication System.
* **HIS:** Hospital Information System.
* **RIS:** Radiology Information System.
* **Worklist:** Daftar pasien dan studi yang dijadwalkan untuk sebuah modalitas.
* **Modalitas:** Alat pencitraan medis (CT, MRI, X-ray, dll.).
* **PRD:** Product Requirements Document.