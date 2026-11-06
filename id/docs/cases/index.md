# Telegram · Selidiki seluruh obrolan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/cases/

Satu kasus utuh di kanal, grup, obrolan pribadi, dan bot: kumpulkan, hubungkan titik-titiknya, susun ulang lini masa, serahkan.

Satu insiden karangan, dari awal sampai akhir. Pengumpulan, pencarian, dan profil orang menemukan catatannya, [Case Board](https://phishdestroy.github.io/TgWitness/id/docs/case-board/) menatanya, [Report studio](https://phishdestroy.github.io/TgWitness/id/docs/reports/) menyajikannya.

KASUS YANG TELAH DITANGANI / TUJUAN PEMBAYARAN YANG BERUBAH

### Satu insiden. Empat percakapan. Jejak yang perlu direkonstruksi.

Sebuah postingan kanal mengarah ke bot. Sebuah grup membicarakan tautan pembayaran baru dan bot menampilkannya. Postingan disunting, obrolan pribadi mengulang tautannya, pesan grup menghilang.

Siapa yang memposting setiap versi?Di mana tautan tersebut muncul?File mana yang disimpan?Apa yang berubah, dan kapan?

Memuat riwayat, AI, MCP, OCR, dan webhook: [Mengolah arsip](https://phishdestroy.github.io/TgWitness/id/docs/archive/).

## 1. Menjangkau seluruh akun

Cakupan seluruh akun hanya di akun khusus. Akun utama memakai obrolan pilihan atau satu folder.

1. [Sambungkan akunnya](https://phishdestroy.github.io/TgWitness/id/docs/accounts/) di ruang kerja sendiri. Catat referensi kasus, ID akun, ruang kerja, dan sidik jari kunci.
2. **Sumber → Cakupan pengamatan → Mode investigasi**: **Seluruh akun**, keempat jenis sumber, **Tindakan sendiri**. Setiap obrolan baru disimpan profilnya dan **200 pesan terlihat** terakhirnya. **Simpan cakupan** lalu konfirmasi.
3. **Muat obrolan** dan bandingkan dengan daftar obrolan akun. Batasnya 1.000 dialog (hingga 20.000 di **Parameter → Obrolan yang dibaca dari daftar akun**); yang melebihi batas muncul begitu aktif.
4. **Pengaturan perekaman** → **Semua aktivitas terlihat**, periksa batas lampiran dan ruang disk. Mulai, lalu uji dengan satu pesan, satu suntingan, dan satu penghapusan.

SaluranGrupObrolan pribadiBot

SATU AKUN / SATU KUNCI PENANDATANGANAN**Semua aktivitas yang terlihat di akun yang dipilih → satu jurnal**

Pesan · pengeditan · pemberitahuan penghapusan · reaksi yang terlihat · peristiwa keanggotaan · tindakan sendiri

"Seluruh akun" berarti setiap obrolan yang bisa dibuka akun ini, dikurangi pengecualian. Tanpa obrolan rahasia. Obrolan baru bergabung saat muncul; riwayat lama tidak diunduh otomatis.

## 2. Mengumpulkan riwayat dan menyimpan berkas-berkas tersebut

Buat koleksi Case Board dan tandai yang penting. Simpan daftar sumber: ID obrolan, judul, akun, peran, awal penangkapan langsung, hasil riwayat, hasil media, celah.

| Kebutuhan | Tindakan di panel | Fitur yang disediakan |
| --- | --- | --- |
| Riwayat di seluruh obrolan yang diaktifkan | Sumber → Muat riwayat lengkap | Pesan-pesan lama yang tersedia dimasukkan ke dalam jurnal ruang kerja, dilengkapi dengan fitur jeda/lanjutkan serta laporan kemajuan yang telah ditandatangani. [Panduan riwayat](https://phishdestroy.github.io/TgWitness/id/docs/reference/history/). |
| Konteks obrolan yang ada dalam jurnal | Sumber → Pengaturan perekaman → Cuplikan riwayat | Pesan terbaru sebagai catatan bertanda tangan. Bawaan 500, hingga 10.000 di **Parameter → Snapshot riwayat terbesar**. |
| Riwayat lengkap dari satu obrolan yang saat ini terlihat | Ekspor obrolan lengkap → Ekspor obrolan lengkap, atau Obrolan → Ekspor obrolan | Paket bertanda tangan terpisah dengan `chat.json` dan `chat.html`, satu per obrolan. |
| Konteks saat obrolan baru muncul | Ruang lingkup pengamatan → Saat obrolan atau bot baru muncul | Profilnya dan hingga 1.000 pesan terbaru (200 dalam mode investigasi). Tidak berlaku untuk obrolan yang sudah ada. |
| Ukuran lampiran | Unduh lampiran yang terlihat + batas per jenis | Cari `media.saved` dengan SHA-256 dan ukuran. Dalam antrean, dilewati, atau gagal berarti tidak tersimpan. |

Ekspor obrolan tidak masuk ke jurnal atau profil orang. Untuk mencari riwayat lama di dalam TgWitness, gunakan **Muat seluruh riwayat** atau snapshot.

Di sini: kanal, grup, obrolan bot, dan obrolan pribadi, ditambah berkas faktur dan hash-nya. Yang dihapus sebelum penangkapan sudah hilang.

## 3. Catat percakapan yang terus berkembang dan tindakan Anda sendiri

Biarkan berjalan. Beri bintang pada obrolan panas sebagai prioritas, atur pemeriksaan ulang di **Pengaturan perekaman → Periksa ulang**, dan pantau `recheck.completed`, FloodWait, serta hasil media.

**Obrolan → Profil → Simpan profil sekarang** menyimpan deskripsi obrolan, perintah bot, dan metadata lain.

**Mengikuti bot atau undangan sebagai bagian dari kasus**

1. **Obrolan → Buka tautan Telegram**, simpan pratinjaunya dulu. Tautan dan pratinjau menjadi catatan bertanda tangan.
2. Jika perlu, **Gabung / buka dan amati** bergabung ke obrolan atau memulai bot dengan parameter mulainya.
3. Untuk mendokumentasikan tindakan, balas atau gunakan **Tekan tombol** dari panel. Anda mendapat `interaction.requested` dan `interaction.result` beserta jawaban bot.

Ini tindakan sungguhan. Tombol yang ditekan di aplikasi lain tidak terlihat, hanya jawaban bot. Tanpa aplikasi web, pembayaran, atau telepon/lokasi.

## 4. Melacak orang, tautan, dan berkas di seluruh obrolan

1. **Jurnal**, **Semua sumber**, cari frasa, domain, atau nama pengguna. Buka hasilnya dan kirim **Ke papan**.
2. **Obrolan → Orang → Aktifkan profil**, pilih seseorang: riwayat nama, balasan, aktivitas, **Juga di…**, tautan, dompet, telepon. Buka catatan yang dikutip.
3. Ikuti ID pengguna numerik yang sama ke obrolan lain. Nama, dompet, atau avatar yang cocok adalah petunjuk, bukan bukti.
4. Bandingkan hash berkas. SHA-256 sama = byte sama. Siapa yang membagikannya adalah soal lain.

PETA KASUS / IKUTI REFERENSIKasus fiktif · bukan grafik aktual

SALURAN / PENGUMUMAN**Asli → tujuan yang telah diedit**

Catatan #101, #188 Pesan #84 · pengirim tidak diketahui

KELOMPOK / OPERASI**Pengguna 71001 memposting tautan baru**

Catatan #146 · pesan #309 Bukti penyimpanan berkas #151

BOT / PERCAKAPAN PEMESANAN**Sebuah tombol mengarah ke tujuan tersebut**

Catatan #173 · pesan #12 Metadata tombol "Kembali"

PRIVAT / TINDAK LANJUT**Pengguna 71001 mengulangi tujuan**

Catatan #205 · pesan #922 Tanda terima file yang disimpan #209

Empat obrolan memberikan pengamatan yang berbeda-beda. Ikuti catatan sumber untuk setiap koneksi; postingan saluran tersebut tidak mencantumkan pengirimnya.

ID numerik dan referensi catatan dibuat khusus untuk panduan ini. Peta penjelasan ini menunjukkan cara menghubungkan hasil pencarian, profil, dan catatan yang diperiksa; Case Board menyimpan kartu dan referensi sumber yang sesuai.

| Koneksi | Pengamatan pendukung | Kesimpulan yang perlu dipertahankan |
| --- | --- | --- |
| Akun Telegram yang sama | ID Pengguna 71001 di grup #146 dan obrolan pribadi #205 | ID pengirim yang sama di kedua obrolan. Siapa dia di dunia nyata adalah soal lain. |
| Tujuan yang diulang | `pay.example.invalid/new` di #146, metadata tombol #173, postingan yang diedit #188 dan #205 | Tautan yang sama di empat tempat. Siapa yang mengendalikannya butuh sumber lain. |
| Ukuran file yang sama | Nilai SHA-256 yang sama persis pada tanda terima media yang telah selesai #151 dan #209 | Kedua berkas identik byte demi byte. |

Profil hanya mencakup orang yang menulis sesuatu di *ruang kerja ini*, bukan daftar anggota. Kutipan per fakta: **Parameter → Catatan dikutip per fakta**.

## 5. Rekonstruksi urutan dan tandai celah-celahnya

Versi di **Obrolan**, lalu **Jurnal** dengan **Semua sumber** + **Suntingan**, **Penghapusan**, **Cakupan**. Masukkan kedua waktu ke lini masa: tanggal Telegram dan saat diamati.

1. 09:00 · #101**Postingan saluran yang direkam**

   Tujuan asli tetap dipertahankan.
2. 09:12 · #146 / #151**Grup memperkenalkan tautan yang berbeda**

   Pengguna 71001 mempostingnya; unduhan lampiran selesai.
3. 09:16 · #173**Bot menampilkan tujuan yang sama**

   Metadata keyboard yang disimpan berisi tautan tersebut.
4. 09:20 · #188**Perubahan pengumuman saluran**

   Baik pengamatan asli maupun yang telah diedit tetap dipertahankan.
5. 09:24 · #205 / #209**Tindak lanjut pribadi mengulanginya**

   Lampiran yang disimpan memiliki nilai SHA-256 lengkap yang sama dengan #151.
6. 09:28 · #231**Pemberitahuan penghapusan grup telah diterima**

   Pengamatan sebelumnya tetap berlaku; baik pihak yang menghapus maupun waktu penghapusan yang tepat tidak disebutkan.

Contoh waktu pengamatan dan referensi. Catatan jurnal lainnya terdapat di antara entri-entri ini.

Urutan jurnal adalah urutan kedatangan, belum tentu urutan kejadian. Pisahkan catatan langsung, snapshot, pesan yang dipulihkan, penghapusan, dan "tidak ditemukan saat periksa ulang", dan tandai setiap celah sebagai tidak diketahui.

## 6. Perluas penerapan ke akun pengumpul lainnya

Satu ruang kerja per akun, langkah yang sama. Catat peran dan sidik jari masing-masing. Nomor pesan berlaku per akun, jadi selalu sebutkan ruang kerja dan obrolannya.

[Grup akun](https://phishdestroy.github.io/TgWitness/id/docs/groups/) menampilkan status, berbagi pengaturan, dan mengekspor semuanya bersama, masing-masing dengan jurnal dan kuncinya sendiri. Lini masa lintas akun Anda susun di catatan Anda.

Kasus panjang? Tambahkan [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/witness/) dan uji apa yang benar-benar ditangkap setiap akun.

## 7. Serahkan paket kasus yang dapat diverifikasi

ZIP bertanda tangan dari setiap ruang kerja (selalu seluruh jurnal, filter tidak berpengaruh), ditambah profil orang, ekspor obrolan, dan berkas.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Kirim sidik jari secara terpisah. Verifikasi semuanya terhadap ruang kerjanya sendiri:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan keluaran verifikator, berkas asli, cakupan, dan catatan serah terima bersama temuan Anda. Tulis semuanya di Report studio. Jika penerima butuh lebih sedikit, siapkan [serah terima ringkas](https://phishdestroy.github.io/TgWitness/id/docs/handover/).
