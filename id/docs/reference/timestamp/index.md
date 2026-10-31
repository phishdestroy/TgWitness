# Cap waktu

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/

Stempel waktu RFC 3161 untuk titik pemeriksaan yang ditandatangani: apa yang dikirimkan ke otoritas dan bagaimana responsnya diverifikasi.

TgWitness menyiapkan permintaan RFC 3161 dan memverifikasi respons otoritas cap waktu (TSA). Prosedur manual ini tidak memilih TSA maupun mengirimkan data; mode bukti melakukan keduanya sesuai jadwal ([format bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Permintaan yang telah disiapkan **belum** merupakan **bukti cap waktu**.

## Apa yang diikat oleh bukti tersebut

Diagram alur · Pengamatan akun → Rantai SHA-256 dan tanda tangan Ed25519; Rantai SHA-256 dan tanda tangan Ed25519 → Titik pemeriksaan yang ditandatangani; Titik pemeriksaan yang ditandatangani → Hash byte-per-byte dan nonce acak; Hash byte-per-byte dan nonce acak → Permintaan RFC 3161; Permintaan RFC 3161 → TSA Independen; TSA Independen → Tanggapan TSA yang ditandatangani; Titik pemeriksaan yang ditandatangani → Verifikasi data, nonce, dan kepercayaan CA yang eksplisit; Tanggapan TSA yang ditandatangani → Verifikasi data, nonce, dan kepercayaan CA yang eksplisit · Pengamatan akun · Rantai SHA-256 dantanda tangan Ed25519 · Titik pemeriksaan yangditandatangani · Hash byte-per-byte dannonce acak · Permintaan RFC 3161 · TSA Independen · Tanggapan TSA yangditandatangani · Verifikasi data,nonce, dan kepercayaanCA yang eksplisit

**Diagram dalam bentuk teks**

1. Pengamatan akun → Rantai SHA-256 dan tanda tangan Ed25519
2. Rantai SHA-256 dan tanda tangan Ed25519 → Titik pemeriksaan yang ditandatangani
3. Titik pemeriksaan yang ditandatangani → Hash byte-per-byte dan nonce acak
4. Hash byte-per-byte dan nonce acak → Permintaan RFC 3161
5. Permintaan RFC 3161 → TSA Independen
6. TSA Independen → Tanggapan TSA yang ditandatangani
7. Titik pemeriksaan yang ditandatangani → Verifikasi data, nonce, dan kepercayaan CA yang eksplisit
8. Tanggapan TSA yang ditandatangani → Verifikasi data, nonce, dan kepercayaan CA yang eksplisit

Tanda tangan pengumpul mengikat catatan ke kuncinya. Respons TSA yang tepercaya dapat membuktikan bahwa pos pemeriksaan tertentu telah ada pada waktu yang dinyatakan oleh TSA. Pos pemeriksaan tersebut kemudian dapat mengikat awalan jurnal. Hal ini tidak membuktikan waktu setiap tindakan Telegram atau kebenaran konten yang direkam.

## Prosedur

1. Simpan sidik jari kunci pengumpul melalui saluran tepercaya yang terpisah. Kunci yang hanya disediakan oleh berkas ZIP yang diperiksa tidak cukup untuk mengidentifikasi pengumpul.
2. Di **Ekspor → Siapkan permintaan cap waktu**, unduh berkas ZIP permintaan dari ruang kerja yang dipilih. Ekstrak `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS`, dan `README.txt`. Jangan ubah byte titik pemeriksaan.
3. Pilih TSA yang sesuai dengan penyelidikan. Kirimkan `timestamp.tsq` menggunakan metode yang terdokumentasi, dengan `application/timestamp-query` untuk layanan HTTP. Simpan balasan biner asli sebagai `timestamp.tsr`, beserta titik akhir, waktu pengambilan, dan hasil permintaan. Permintaan tersebut berisi hash dan nonce, bukan pesan; metadata jaringan tetap mengungkapkan permintaan tersebut.
4. Peroleh sertifikat akar tepercaya secara terpisah dari balasan, beserta sertifikat perantara yang diperlukan. Sertifikat yang terdapat dalam balasan tidak otomatis menjadi tepercaya hanya karena disertakan di sana.
5. Dari instalasi TgWitness yang tepercaya, verifikasi:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Tambahkan `--intermediates tsa-intermediates.pem` atau `--openssl /path/to/openssl` jika diperlukan. OpenSSL harus mendukung `ts`. Pada Windows, verifikator juga mencari instalasi Git standar. OpenSSL 3.5.9 telah diuji secara lokal dengan CA/TSA sintetis.

1. Ekspor ZIP jurnal yang telah ditandatangani setelah titik pemeriksaan sehingga mencakup awalan tersebut. Verifikasi menggunakan sidik jari yang diketahui secara independen:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Simpan ZIP, titik pemeriksaan, permintaan, balasan, rantai sertifikat, hasil verifikasi, dan catatan serah terima di luar pengumpul. Lakukan verifikasi ulang saat penerimaan.

Untuk menyiapkan permintaan dari titik pemeriksaan yang disimpan:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Proses persiapan ini menstandarkan JSON dan menyertakan titik pemeriksaan yang sesuai ke dalam arsip. Gunakan **byte titik** pemeriksaan **dari arsip tersebut** untuk verifikasi TSA, meskipun berkas masukan memiliki spasi kosong yang berbeda.

## Batasan verifikasi

| Periksa | Perilaku saat ini |
| --- | --- |
| Data | Nilai SHA-256 dari byte titik pemeriksaan yang tepat harus sesuai dengan respons |
| Permintaan | Dengan `--request`, kueri asli dan nonce diverifikasi |
| Tanda tangan TSA | OpenSSL memverifikasi tanda tangan dan rantai sertifikat hingga ke CA yang ditentukan secara eksplisit |
| Tanda tangan pengumpul | Diverifikasi secara terpisah oleh verifikator jurnal dengan kunci yang disematkan |
| Pencabutan | Tidak ada pengambilan OCSP/CRL secara otomatis |
| Validitas jangka panjang | Tidak ada validasi arsip setelah sertifikat kedaluwarsa |
| Pengiriman terjadwal | Mode bukti, dinonaktifkan secara default |

`--request` secara teknis bersifat opsional, tetapi mengabaikannya akan menghalangi verifikasi nonce asli. Untuk prosedur lengkap ini, hasil `request_checked` harus bernilai benar. Verifikasi sertifikat mengikuti aturan dan waktu verifikasi OpenSSL yang terinstal. Penyimpanan jangka panjang memerlukan kebijakan bukti sertifikat/pencabutan yang terpisah.

Tanda tangan kriptografis yang valid tidak secara otomatis merupakan cap waktu yang memenuhi syarat atau penetapan kelayakan hukum. Jika seorang operator memalsukan pengamatan sebelum pencap waktu, TSA mengaitkan byte-byte tersebut; hal itu tidak membuktikan kebenarannya.

## Catatan serah terima

Catat pengenal kasus, pengirim dan penerima, waktu pengiriman UTC beserta sumbernya, tujuan, nama file/nilai SHA-256, sidik jari pengumpul, rentang urutan, celah yang diketahui, versi verifikator, dan hasil verifikasi. Tandatangani dan simpan catatan ini secara independen melalui proses organisasi Anda. Sistem catatan penyimpanan multi-pengguna tidak diimplementasikan dalam TgWitness.

Tidak ada TSA independen yang sedang beroperasi yang dihubungi selama pengembangan. Pengujian lokal menciptakan CA/TSA sintetis untuk memeriksa kompatibilitas dan penolakan terhadap data yang diubah, nonce, atau CA.
