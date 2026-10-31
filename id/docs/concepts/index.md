# Lihat cara kerja bukti ini

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/concepts/

Sebuah pesan dapat berubah. Catatan tentang apa yang Anda amati harus tetap dapat diverifikasi.

Jelajahi dua eksperimen kecil di bawah ini. Eksperimen ini menggunakan pesan fiktif, berjalan di dalam browser Anda, dan tidak pernah terhubung ke Telegram.

## Satu pesan, tiga pengamatan

Ketika Telegram mengirimkan pesan baru, pemberitahuan pengeditan, dan pemberitahuan penghapusan, aplikasi pengumpul menambahkan tiga catatan terpisah. Pengeditan tidak menggantikan catatan pertama. Pemberitahuan penghapusan tidak menghapusnya.

01 / PERJALANAN PESANUrutan ilustratif

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Pengumpul · Jurnal · perbarui → · tambahkan →

TAMPILAN OBrolan SAAT INI Pesan #42

Pesan telah dihapus

Pesan tersebut telah menghilang dari tampilan obrolan.

JURNAL PENGAMATAN 3 catatan

1. 01

   `message.new`

   Bertemu pukul 10.00

   ✓
2. 02

   `message.edited`

   Bertemu pukul 11.00

   ✓
3. 03

   `message.deleted`

   Pemberitahuan penghapusan untuk #42

   ✓

Ketiga pengamatan yang diterima tetap tersimpan dalam jurnal tersebut.

Jalur yang disederhanakan untuk satu sumber yang telah dipilih. Catatan operasional juga mencakup jurnal asli. Pencatatan bergantung pada apa yang dapat dilihat oleh akun tersebut dan apa yang disediakan oleh Telegram.

Pemberitahuan penghapusan tidak memberikan waktu penghapusan yang dapat diandalkan maupun identitas orang yang menghapus pesan tersebut. Dengan tidak mengungkapkan nilai-nilai tersebut, perbedaan antara pengamatan dan dugaan tetap terjaga.

## Ubah catatan. Ikuti hash-nya.

Setiap catatan berisi hash dari catatan sebelumnya. Hash-nya sendiri mencakup bidang-bidang peristiwa, termasuk tautan tersebut. Titik pemeriksaan yang disimpan secara eksternal mengunci panjang jurnal tertentu dan hash awal.

02 / HASH-CHAIN SANDBOXSHA-256 asli · contoh catatan

CATATAN 01**Pesan diterima**`h₁ = SHA-256(e₁)`Tautan ke 64 nol

CATATAN 02**Bertemu pukul 11.00**`h₂ = SHA-256(e₂)`Termasuk h₁

CATATAN 03**Penghapusan terdeteksi**`h₃ = SHA-256(e₃)`Termasuk h₂

DISIMPAN DI TEMPAT LAIN**3 catatan · kepala `h₃`**Bandingkan batas yang telah diperbaiki ini dengan jurnal yang disediakan.

Mengubah suatu peristiwa akan mengubah hash-nya. Membangun ulang rantai akan mengubah bagian awalnya. Menghapus bagian akhir akan membuatnya lebih pendek daripada titik pemeriksaan yang disimpan.

**Periksa catatan 2 dan hash lengkapnya**

Ini adalah JSON UTF-8 yang telah di-hash persis seperti pada contoh ini. Nilai-nilainya fiktif; sembilan bidang dan serialisasinya sesuai dengan format jurnal.

```

```

Catatan yang disimpan 2 hash

``

Hash catatan 2 yang dihitung ulang

``

Sandbox ini menghitung hash, bukan tanda tangan. Verifikator yang sebenarnya juga memeriksa tanda tangan Ed25519, urutan, dan tautan setiap peristiwa. Membangun ulang hash saja tidak dapat menghasilkan tanda tangan yang valid di bawah kunci tepercaya.

## Aturan sebenarnya, dalam beberapa baris

HASH + TANDA TANGAN

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** menserialisasikan sembilan bidang peristiwa sebagai JSON UTF-8: kunci yang diurutkan, tanpa spasi kosong tambahan, tanpa pengkodean ASCII, dan tanpa NaN/infinity. Nilai `previous_hash` dari peristiwa tersebut adalah hi−1. Nilai h0 yang ditampilkan berarti 64 karakter nol; tanda tangan mencakup 32 byte ringkasan mentah.

Sembilan bidang tersebut adalah `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, dan `previous_hash`. Ini adalah [pengkodean JSON TgWitness yang terdokumentasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#event-canonicalization); hash dan tanda tangan itu sendiri bukanlah bidang input hash.

TITIK PERIKSA YANG DISIMPAN

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Verifikasi tanda tangan titik pemeriksaan di bawah kunci pengumpul yang disematkan, lalu bandingkan batasnya dengan jurnal yang telah diverifikasi. Ekspor yang dilakukan kemudian mungkin berisi lebih banyak catatan; namun, ekspor tersebut tetap harus sesuai dengan titik pemeriksaan sebelumnya.

## Tiga pertanyaan, tiga pemeriksaan yang berbeda

[01 / INTEGRITAS**Apakah catatan ini berubah?** Verifikasi hash dan tanda tangan menggunakan kunci tepercaya yang terpisah.](https://phishdestroy.github.io/TgWitness/id/docs/exports/)[02 / KONTINUITAS**Apa yang telah disimpan sebelumnya?** Bandingkan ekspor yang ditandatangani dengan titik pemeriksaan yang disimpan oleh saksi terpisah.](https://phishdestroy.github.io/TgWitness/id/docs/witness/)[03 / PENYAMPAIAN**Apakah peristiwa uji coba ini telah diterima?** Cocokkan tindakan pengiriman, pengeditan, dan penghapusan yang dikendalikan dengan jurnal masing-masing akun.](https://phishdestroy.github.io/TgWitness/id/docs/cases/)

Rantai hash yang cocok menjawab pertanyaan mengenai integritas. Hal ini tidak membuktikan pengiriman pesan Telegram secara lengkap, kebenaran suatu pesan, atau waktu pengamatan yang dapat dipercaya secara independen.

Ikuti [penyelidikan akun secara menyeluruh](https://phishdestroy.github.io/TgWitness/id/docs/cases/) mulai dari pengumpulan data hingga penyusunan berkas kasus.
