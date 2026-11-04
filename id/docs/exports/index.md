# Ekspor dan verifikasi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/exports/

Serahkan berkas yang bisa diperiksa penerima sendiri terhadap ruang kerja Anda.

Simpan referensiEkspor ZIP yang ditandatanganiPenerima memverifikasi

Baru mengenal tanda tangan dan checkpoint? [Ubah contoh catatan](https://phishdestroy.github.io/TgWitness/id/docs/concepts/#chain) dan lihat pemeriksaan mana yang menangkapnya.

Ingin menyimpan salinan di luar sistem pengumpul? Kunjungi [pengaturan S3](https://phishdestroy.github.io/TgWitness/id/docs/exports/#s3), [Object Lock,](https://phishdestroy.github.io/TgWitness/id/docs/exports/#s3-retention) atau [pemulihan terverifikasi](https://phishdestroy.github.io/TgWitness/id/docs/exports/#s3-restore).

## Simpan sebagai referensi tepercaya

Catat sidik jari kunci ruang kerja di tempat selain kolektor. Selama pengumpulan, simpan juga checkpoint bertanda tangan di tempat lain, atau jalankan [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/witness/). Itulah yang dipakai penerima untuk memeriksa kunci dan keadaan jurnal sebelumnya.

## Unduh ZIP yang telah ditandatangani

**Ekspor** → ZIP bukti bertanda tangan. Isinya seluruh jurnal dan manifes berkas bertanda tangan. Bentuk laporan yang mudah dibaca di [Report studio](https://phishdestroy.github.io/TgWitness/id/docs/reports/), atau kirim hanya data pilihan sebagai [ekstrak serah terima](https://phishdestroy.github.io/TgWitness/id/docs/handover/).

Laporan HTML, PDF, dan JSON punya segelnya sendiri. CSV hanya salinan kerja; untuk integritas gunakan CSV di dalam ZIP yang sudah diverifikasi.

## Verifikasi dengan salinan TgWitness yang tepercaya

Di lingkungan proyek, dengan sidik jari dan path Anda sendiri:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Jika lolos, Anda melihat `key_pinned: true` dan `checkpoint_checked: true`. Simpan keluaran itu di samping arsip. Checkpoint harus berada di akhir ekspor atau sebelumnya.

## Gunakan hasil verifikasi

- **Berkas:** manifes mengikat hash-nya, tanda tangan mengikat jurnal. Setiap perubahan akan terlihat.
- **Identitas:** sidik jari yang Anda simpan membuktikan itu kunci yang Anda harapkan.
- **Keadaan sebelumnya:** checkpoint membandingkan ekspor dengan awal jurnal yang disimpan sebelum serah terima.
- **Cakupan:** celah, hasil akuisisi, dan uji kirim → sunting → hapus menunjukkan apa yang benar-benar ditangkap pengaturan ini.

Detail: [apa yang dibuktikan verifikasi dan apa yang tidak](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope).

## Siapkan salinan cadangan di luar lokasi di S3

**Ekspor → Salinan luar** di ruang kerja Anda. Berfungsi dengan AWS S3 dan apa pun yang kompatibel dengan S3. Menyalin segmen jurnal, berkas tersimpan, checkpoint beserta cap waktunya, dan ekspor obrolan yang selesai, masing-masing dienkripsi dengan `AES-256-GCM` sebelum meninggalkan kolektor.

Demo online menampilkan kontrol ini dengan unggahan nonaktif. Masukkan kredensial asli hanya di instalasi Anda sendiri.

[![Panel salinan lengkap di luar situs: titik akhir, wilayah, bucket, kunci akses, jadwal, penguncian objek, dan kontrol kunci pemulihan](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Panel lengkap dengan opsi lanjutan yang diperluas. Tidak ada kredensial penyimpanan yang ditampilkan.

| Bidang | Apa yang harus dimasukkan |
| --- | --- |
| Titik akhir | URL penyimpanan, tanpa path bucket atau kredensial. Contoh: `https://s3.example.invalid`. |
| Wilayah | Sesuai kebutuhan penyedia Anda. Bawaan `us-east-1`. |
| Bucket | Bucket yang sudah ada dan bisa Anda tulisi. Contoh: `example-case-backup`. |
| Folder di dalam bucket | Prefiks, bawaan `tgwitness`. Prefiks per ruang kerja ditambahkan di atasnya. |
| ID Kunci Akses / Kunci Akses Rahasia | Keduanya bersama, disimpan di brankas. Kosongkan keduanya nanti untuk mempertahankannya. |
| Alamat bergaya jalur | Aktif: `endpoint/bucket`. Nonaktif: `bucket.endpoint`. Tergantung penyedia. |
| Interval penyalinan | 1 sampai 1.440 menit, bawaan 5. Hanya selama aplikasi berjalan. |
| Penyimpanan Object Lock | Hari dan mode, jika bucket mendukung Object Lock. Nol mempertahankan bawaan bucket. |

1. Buat bucket, isi tujuan dan kredensial dengan **Simpan salinan luar** tidak dicentang, lalu klik **Simpan pengaturan salinan luar**.
2. **Uji koneksi** mengunggah objek uji terenkripsi.
3. **Unduh kunci enkripsi** dan simpan jauh dari kolektor. Tanpa kunci, tidak ada pemulihan.
4. Centang **Simpan salinan luar**, simpan, lalu **Salin sekarang** atau biarkan jadwal berjalan.

## Periksa retensi dan kemajuan penyalinan

Di **Opsi lain**, pilih hari retensi dan `GOVERNANCE` atau `COMPLIANCE`. TgWitness membaca kembali retensi dari objek yang diunggah dan memberi tahu: terkonfirmasi, tidak ada, atau pemeriksaan gagal.

Panel menampilkan lintasan terakhir, jumlah objek, byte, batas jurnal yang disalin, dan galat. Berkas lokal yang hilang dilaporkan dan dicoba lagi pada lintasan berikutnya; sisanya tetap disalin.

Unggahan lewat koneksi langsung, SOCKS5, atau HTTP. Dengan rute khusus MTProxy, salinan menunggu dengan galat.

## Simpan kunci pemulihan secara terpisah

JSON kunci berisi kunci dekripsi, tujuan, prefiks, dan sidik jari kunci. Untuk pemulihan Anda perlu itu ditambah kredensial penyimpanan dengan akses baca.

Mengubah endpoint, bucket, atau prefiks? Unduh kuncinya lagi. Salinan baru dimulai di tujuan baru; ekspor lama tetap di tempatnya.

## Pulihkan dan verifikasi di mesin lain

Anda perlu instalasi TgWitness yang tepercaya, JSON kunci, kredensial baca-saja, dan folder kosong:

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

Semuanya diperiksa dulu di folder sementara pribadi: seluruh jurnal, checkpoint, hash dan ukuran berkas. Path tidak aman, segmen yang bertentangan, atau jurnal yang lebih pendek dari checkpoint-nya akan gagal, dan saat itu tidak ada yang ditulis.

Jika berhasil, Anda mendapat `events.jsonl`, `media/`, `checkpoints/`, dan `exports/`. Simpan keluaran JSON perintahnya bersama itu dan bandingkan dengan checkpoint atau catatan saksi yang Anda simpan sendiri.
