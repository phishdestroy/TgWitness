# Ekspor dan verifikasi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/exports/

Berikan file kepada penerima yang dapat mereka periksa dengan membandingkannya terhadap ruang kerja pengumpulan dan riwayat yang tersimpan di dalamnya.

Simpan referensiEkspor ZIP yang ditandatanganiPenerima memverifikasi

Baru mengenal tanda tangan dan titik pemeriksaan? [Ubah catatan contoh](https://phishdestroy.github.io/TgWitness/id/docs/concepts/#chain) dan lihat pemeriksaan mana yang mendeteksinya.

Ingin menyimpan salinan di luar sistem pengumpul? Kunjungi [pengaturan S3](https://phishdestroy.github.io/TgWitness/id/docs/exports/#s3), [Object Lock,](https://phishdestroy.github.io/TgWitness/id/docs/exports/#s3-retention) atau [pemulihan terverifikasi](https://phishdestroy.github.io/TgWitness/id/docs/exports/#s3-restore).

## Simpan sebagai referensi tepercaya

Simpan sidik jari kunci publik ruang kerja di luar pengumpul. Selama proses pengumpulan, simpan titik pemeriksaan yang telah ditandatangani di tempat lain atau gunakan [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/witness/). Referensi ini memungkinkan penerima untuk memverifikasi kunci dan batas jurnal sebelumnya.

## Unduh ZIP yang telah ditandatangani

Buka **Ekspor** dan buat ZIP bukti yang ditandatangani. ZIP tersebut mencakup jurnal ruang kerja lengkap dan manifes file yang ditandatangani. Gunakan [Report Studio](https://phishdestroy.github.io/TgWitness/id/docs/reports/) untuk menyusun laporan yang mudah dibaca, atau [ekstrak](https://phishdestroy.github.io/TgWitness/id/docs/handover/) [penyerahan](https://phishdestroy.github.io/TgWitness/id/docs/handover/) untuk mengirimkan hanya data yang dipilih dan dipersingkat.

Laporan dalam format HTML, PDF, dan JSON dilengkapi dengan segel tanda tangan masing-masing dan dapat diverifikasi secara terpisah. CSV merupakan salinan yang praktis untuk analisis; gunakan file CSV yang tepat di dalam ZIP yang telah diverifikasi untuk memeriksa integritasnya. Simpan ZIP yang telah ditandatangani jika penerima juga memerlukan catatan sumber dan lampiran.

## Verifikasi dengan salinan TgWitness yang tepercaya

Di lingkungan proyek yang telah diinstal, ganti sidik jari contoh dan jalur file berikut:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Jika kedua referensi lolos, hasilnya akan melaporkan `key_pinned: true` dan `checkpoint_checked: true`. Simpan hasil verifikasi bersama arsip aslinya. Titik pemeriksaan yang disimpan harus berada pada atau sebelum batas ekspor.

## Gunakan hasil verifikasi

- **Periksa berkas yang dikirimkan:** manifes mengikat hash-nya, dan tanda tangan catatan mengikat jurnal yang disimpan. Berkas yang diubah atau rantai catatan yang terputus akan terdeteksi.
- **Periksa identitas ruang kerja:** sidik jari yang disimpan secara independen mengidentifikasi kunci penandatanganan yang Anda harapkan.
- **Bandingkan batas waktu sebelumnya:** titik pemeriksaan yang disimpan akan memverifikasi ekspor tersebut dengan awalan jurnal yang disimpan sebelum penyerahan.
- **Tinjau cakupan pengumpulan:** celah, hasil akuisisi, dan uji coba terkontrol kirim → edit → hapus menggambarkan peristiwa yang terekam oleh pengaturan ini.

Simpan hasil ini bersama salinan penerima. Perhatikan [apa yang ditetapkan oleh verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope) terkait ruang lingkup pemeriksaan serta penilaian terpisah atas klaim sumber dan cakupan pengumpulan.

## Siapkan salinan cadangan di luar lokasi di S3

Di ruang kerja Anda yang sedang berjalan, buka **Ekspor → Salinan di luar situs**. Fitur opsional ini kompatibel dengan AWS S3 dan layanan lain yang mendukung S3. Fitur ini menyalin segmen jurnal, foto dan file yang disimpan, titik pemeriksaan beserta respons cap waktunya, serta ekspor obrolan yang telah selesai. Setiap objek dienkripsi di pengumpul menggunakan `AES-256-GCM` sebelum diunggah.

Demo online ini menampilkan kontrol yang sama dengan fitur unggah yang dinonaktifkan. Masukkan kredensial penyimpanan hanya di ruang kerja Anda sendiri yang sedang berjalan.

[![Panel salinan lengkap di luar situs: titik akhir, wilayah, bucket, kunci akses, jadwal, penguncian objek, dan kontrol kunci pemulihan](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Panel lengkap dengan opsi lanjutan yang diperluas. Tidak ada kredensial penyimpanan yang ditampilkan.

| Bidang | Apa yang harus dimasukkan |
| --- | --- |
| Titik akhir | URL layanan penyimpanan, tanpa jalur bucket atau kredensial. Contoh fiktif: `https://s3.example.invalid`. |
| Wilayah | Wilayah yang disyaratkan oleh penyedia layanan Anda. Nilai default aplikasi adalah `us-east-1`. |
| Bucket | Sebuah bucket yang sudah ada dan dapat Anda akses. Contoh fiktif: `example-case-backup`. |
| Folder di dalam bucket | Awalan objek; default `tgwitness`. Aplikasi ini menambahkan awalan yang diturunkan dari sidik jari kunci penandatanganan ruang kerja ini. |
| ID Kunci Akses / Kunci Akses Rahasia | Masukkan kedua kredensial penyimpanan secara bersamaan. Kredensial tersebut disimpan di brankas ruang kerja. Biarkan keduanya kosong pada penyimpanan berikutnya untuk mempertahankan pasangan kredensial yang telah disimpan. |
| Alamat bergaya jalur | Gunakan `endpoint/bucket` jika diaktifkan, atau `bucket.endpoint` jika dinonaktifkan, sesuai dengan penyedia layanan. |
| Interval penyalinan | Dari 1 hingga 1.440 menit; default 5 menit. Aplikasi harus dalam keadaan berjalan untuk pencadangan terjadwal. |
| Penyimpanan Object Lock | Jumlah hari penyimpanan dan mode untuk bucket yang mendukung Object Lock. Nilai "Zero days" membuat pengaturan penyimpanan default bucket tetap berlaku. |

1. Buat bucket dengan penyedia layanan Anda, lalu masukkan tujuan dan kredensialnya. Biarkan opsi **“Simpan salinan di luar lokasi”** tidak dicentang saat mempersiapkan, lalu pilih **“Simpan salinan di luar lokasi**”.
2. Pilih "**Uji Koneksi**". Ini akan mengunggah objek uji terenkripsi dan memeriksa respons penyimpanan.
3. Pilih **"Unduh kunci enkripsi**". Simpan berkas tersebut terpisah dari pengumpul data; berkas ini diperlukan untuk pemulihan.
4. Aktifkan kotak centang "**Simpan salinan di luar situs**" dan simpan kembali. Pilih "**Salin sekarang"** untuk proses manual, atau biarkan penjadwalan berjalan.

## Periksa retensi dan kemajuan penyalinan

Di bawah **"More options**", pilih jangka waktu penyimpanan dan "`GOVERNANCE`" atau "`COMPLIANCE`" jika bucket Anda mendukung Object Lock. TgWitness membaca kembali mode penyimpanan dan batas waktu objek yang diunggah. Periksa hasil penyimpanan terpisah: dikonfirmasi, penyimpanan tidak ditemukan, atau pemeriksaan gagal.

Panel ini melaporkan putaran terakhir, jumlah objek, byte yang ditransfer, batas jurnal yang disalin, dan kesalahan apa pun. Media lokal yang hilang atau berubah akan dilaporkan dan dicoba kembali pada putaran berikutnya. File, titik pemeriksaan, dan ekspor yang antri setelah media tersebut masih dapat disalin.

Pengunggahan menggunakan rute Direct, SOCKS5, atau HTTP di ruang kerja. Pilih salah satu rute ini untuk penyalinan ke S3; rute yang hanya menggunakan MTProxy akan membuat penyalinan tertunda dengan pesan kesalahan.

## Simpan kunci pemulihan secara terpisah

Berkas JSON yang diunduh berisi kunci dekripsi, pengaturan tujuan, awalan objek ruang kerja, dan sidik jari kunci penandatanganan. Pemulihan memerlukan berkas kunci ini serta kredensial penyimpanan terpisah yang memiliki akses baca ke bucket. Simpanlah keduanya dalam rencana pemulihan Anda.

Jika Anda mengubah titik akhir (endpoint), bucket, atau awalan folder, unduh kembali berkas kunci agar pengaturan tujuannya sesuai. Aplikasi ini akan memulai salinan baru dari jurnal, berkas, dan titik pemeriksaan yang disimpan secara lokal di tujuan baru tersebut. Ekspor obrolan yang sudah selesai dan telah dihapus dari antrian unggahan lokal tetap berada di tujuan sebelumnya.

## Pulihkan dan verifikasi di mesin lain

Gunakan instalasi TgWitness yang tepercaya, berkas JSON kunci yang telah diunduh, kredensial penyimpanan dengan akses baca, dan direktori keluaran yang kosong. Ganti tempat penanda kredensial fiktif di bawah ini.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

File yang diunduh dan objek yang telah didekripsi disimpan di penyimpanan sementara pribadi sementara jurnal lengkap, titik pemeriksaan yang disimpan, serta hash dan ukuran media yang dilestarikan diperiksa. Jalur yang tidak aman, segmen jurnal yang bertentangan, dan jurnal yang lebih pendek dari titik pemeriksaannya akan ditolak. Verifikasi yang gagal tidak akan mempublikasikan file yang dipulihkan.

Pemulihan yang berhasil akan menghasilkan `events.jsonl`, `media/`, `checkpoints/`, dan `exports/` untuk materi yang tersedia dalam salinan tersebut. Simpan hasil JSON perintah tersebut bersama dengan materi yang telah dipulihkan.

Bandingkan materi yang dipulihkan dengan titik pemeriksaan atau catatan saksi yang Anda simpan secara independen, lalu tinjau cakupan pengumpulan yang terekam untuk periode yang Anda butuhkan.
