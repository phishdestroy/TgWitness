# Selidiki seluruh obrolan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/cases/

Tangani seluruh kasus di berbagai saluran, grup, obrolan pribadi, dan bot: kumpulkan, hubungkan, rekonstruksi, dan serahkan bukti tersebut.

Panduan ini mengikuti satu insiden fiktif dari awal hingga akhir. Panduan ini menggunakan fitur pengumpulan, pencarian, profil pengguna, dan ekspor yang sebenarnya. Peta kasus hanyalah contoh dokumentasi; kesimpulan dan daftar kasus Anda disimpan di luar aplikasi.

KASUS YANG TELAH DITANGANI / TUJUAN PEMBAYARAN YANG BERUBAH

### Satu insiden. Empat percakapan. Jejak yang perlu direkonstruksi.

Sebuah pengumuman di saluran mengarah ke sebuah bot. Sebuah grup operasional mendiskusikan tautan pembayaran baru. Sebuah pesan tindak lanjut di saluran pribadi mengulanginya. Kemudian, pengumuman tersebut diedit dan pesan grup tersebut menghilang.

Siapa yang memposting setiap versi?Di mana tautan tersebut muncul?File mana yang disimpan?Apa yang berubah, dan kapan?

Untuk pemuatan riwayat, tinjauan sumber AI opsional, MCP, OCR, dan webhook keluar, lihat "[Work the archive](https://phishdestroy.github.io/TgWitness/id/docs/archive/)".

## 1. Menjangkau seluruh akun

1. [Hubungkan akun pengumpul](https://phishdestroy.github.io/TgWitness/id/docs/accounts/) ke ruang kerja tersendiri. Catat nomor referensi kasus, ID akun, nama ruang kerja, dan sidik jari kunci penandatanganan dalam catatan kasus Anda.
2. **Sumber** Terbuka **→ Cakupan pengamatan → Mode investigasi**. Tinjau **seluruh akun**, keempat jenis sumber, dan **tindakan sendiri**. Pengaturan awal ini memungkinkan penyimpanan profil sumber baru beserta **200 pesan** terbarunya **yang terlihat**. Tekan **Simpan cakupan** dan selesaikan konfirmasi cakupan.
3. Tekan **"Muat obrolan**". Bandingkan sumber-sumber tersebut dengan daftar percakapan akun dan tinjau pengecualian. Di bawah **Parameter → Obrolan yang dibaca dari daftar akun**, sesuaikan batas daftar awal jika diperlukan: nilai defaultnya adalah 1.000 percakapan, dapat dikonfigurasi hingga 20.000. Percakapan yang melebihi batas tersebut akan terdeteksi saat menjadi aktif.
4. Di **pengaturan Perekaman**, pilih dan simpan **Semua aktivitas yang terlihat**. Periksa jenis lampiran, batas ukuran, dan ruang disk kosong. Mulai pemantauan dan validasi pesan, pengeditan, serta penghapusan yang dikendalikan sebelum mengandalkan pengaturan tersebut.

SaluranGrupObrolan pribadiBot

SATU AKUN / SATU KUNCI PENANDATANGANAN**Semua aktivitas yang terlihat di akun yang dipilih → satu jurnal**

Pesan · pengeditan · pemberitahuan penghapusan · reaksi yang terlihat · peristiwa keanggotaan · tindakan sendiri

“Seluruh akun” mencakup obrolan yang dapat diakses oleh akun ini, beserta jenis sumber dan pengecualian yang telah dikonfigurasi. Obrolan rahasia tidak tersedia. Dialog baru ditambahkan seiring dengan kedatangan pembaruan; mengaktifkan mode ini tidak secara otomatis mengunduh riwayat lama lengkap dari setiap obrolan yang ada.

## 2. Mengumpulkan riwayat dan menyimpan berkas-berkas tersebut

Buatlah daftar sumber untuk seluruh penyelidikan. Berikan setiap obrolan satu baris yang berisi ID numerik, judul, akun, akses/peran, waktu mulai real-time, perolehan riwayat, hasil media, dan celah yang diketahui. Tandai sumber sebagai telah diperoleh hanya setelah memeriksa hasil yang relevan.

| Kebutuhan | Tindakan di panel | Fitur yang disediakan |
| --- | --- | --- |
| Riwayat di seluruh obrolan yang diaktifkan | Sumber → Muat riwayat lengkap | Fitur utama saat ini: pesan-pesan lama yang tersedia dimasukkan ke dalam jurnal ruang kerja, dilengkapi dengan fitur jeda/lanjutkan serta laporan kemajuan yang ditandatangani. [Panduan riwayat](https://phishdestroy.github.io/TgWitness/id/docs/reference/history/). |
| Konteks obrolan yang ada dalam jurnal | Sumber → Pengaturan perekaman → Cuplikan riwayat | Pesan-pesan terbaru yang terlihat sebagai catatan yang telah ditandatangani. Batas maksimum default 500; **Parameter → "Largest history snapshot"** dapat menaikkan batas tersebut hingga 10.000. |
| Riwayat lengkap dari satu obrolan yang saat ini terlihat | Ekspor obrolan lengkap → Ekspor obrolan lengkap, atau Obrolan → Ekspor obrolan | Sebuah bundel terpisah yang ditandatangani dengan `chat.json` dan `chat.html`. Ulangi untuk setiap sumber; simpan hasil keberhasilan/kegagalan. |
| Konteks saat obrolan baru muncul | Ruang lingkup pengamatan → Saat obrolan atau bot baru muncul | Profil sumber dan hingga 1.000 pesan terbaru yang terlihat; Mode penyelidikan memilih 200 pesan. Obrolan yang sudah ada tidak akan dimasukkan ke dalam catatan ini secara retroaktif. |
| Ukuran lampiran | Unduh lampiran yang terlihat + batas per jenis | Periksa kode `media.saved`, nilai SHA-256, dan jumlah byte-nya. Unduhan yang sedang dalam antrean, dilewati, atau gagal bukanlah berkas yang tersimpan. |

Ekspor obrolan lengkap merupakan snapshot terpisah; ekspor ini tidak mengimpor seluruh riwayat obrolan ke dalam jurnal atau profil pengguna. Gunakan opsi "**Muat riwayat lengkap** dari semua sumber yang diaktifkan" atau "snapshot jurnal terbatas" untuk materi historis yang perlu Anda telusuri di dalam TgWitness. Periksa daftar sumber sebelum memulai proses.

Dalam kasus yang dianalisis, peroleh saluran pengumuman, grup operasional, percakapan bot, dan tindak lanjut pribadi. Simpan byte dan hash lampiran faktur. Riwayat yang tersedia saat ini tidak dapat merekonstruksi pesan yang dihapus sebelum penangkapan atau pengeditan sementara yang tidak lagi ditampilkan oleh Telegram.

## 3. Catat percakapan yang terus berkembang dan tindakan Anda sendiri

Pertahankan pemantauan agar tetap berjalan seiring perkembangan kasus. Tandai obrolan kasus yang aktif sebagai sumber prioritas; konfigurasikan pemeriksaan ulang prioritas dan sumber lain di bawah **Pengaturan Perekaman → Pemeriksaan Ulang**. Tinjau `recheck.completed`, kelanjutan penyesuaian, FloodWait, dan hasil media seiring berjalannya pekerjaan.

Gunakan **Obrolan → Profil → Simpan profil sekarang** untuk menyimpan deskripsi sumber saat ini, perintah bot, dan metadata lain yang dikembalikan oleh Telegram. Profil sumber ini terpisah dari profil orang yang dibuat berdasarkan pesan dalam jurnal.

**Mengikuti bot atau undangan sebagai bagian dari kasus**

1. Di **bagian Chats → Buka tautan Telegram**, simpan pratinjau terlebih dahulu. Tautan asli dan pratinjau yang ditampilkan akan menjadi catatan yang ditandatangani.
2. Jika diperlukan dalam penyelidikan, perintah "**Join / open**" **akan** membuka sumber dan menjalankan bot dengan parameter awal yang disediakan. Permintaan bergabung yang tertunda tetap tercatat sebagai tertunda dalam catatan.
3. Untuk tindakan yang perlu Anda dokumentasikan, gunakan balasan teks pada panel atau kontrol **tombol "Press"** yang didukung. Jurnal ini menyimpan `interaction.requested` dan `interaction.result`, termasuk teks atau URL callback yang dikembalikan.

Kontrol-kontrol ini melakukan tindakan Telegram yang sebenarnya. Tombol callback yang ditekan di aplikasi Telegram lain tidak terlihat oleh pengumpul; pesan atau pengeditan bot selanjutnya mungkin terlihat. Aplikasi web, pembayaran, dan permintaan nomor telepon/lokasi berada di luar cakupan mini-client.

## 4. Melacak orang, tautan, dan berkas di seluruh obrolan

1. Buka **Jurnal**, biarkan filter sumber pada "**Semua sumber"** dan cari frasa, domain, nama pengguna, atau pengenal yang tersimpan yang khas. Buka setiap catatan yang cocok dan catat obrolannya, ID pesan, serta nomor urut jurnal.
2. Untuk obrolan yang relevan, buka **Obrolan → Orang → Aktifkan profil**, lalu pilih seseorang. Tinjau riwayat nama/nama pengguna, hubungan balasan, aktivitas, **serta "Juga di..."** obrolan lain yang diamati dan tautan, dompet, atau nomor telepon yang diekstraksi. Buka catatan jurnal yang dikutip.
3. Ikuti ID pengguna Telegram numerik yang sama ke obrolan lain di ruang kerja ini. Anggap nama yang cocok, penyebutan dompet, atau avatar yang serupa sebagai petunjuk yang perlu diperiksa. Alamat yang disebutkan tidak membuktikan kepemilikan; avatar yang serupa tidak membuktikan bahwa itu adalah orang yang sama.
4. Bandingkan nilai SHA-256 lampiran yang disimpan di seluruh catatan. Nilai hash yang sama mendukung identitas byte dari file yang disimpan. Periksa catatan pesan dan pengirim yang terkait sebelum menarik kesimpulan tentang siapa yang membagikannya.

PETA KASUS / IKUTI REFERENSIKasus fiktif · bukan grafik aktual

SALURAN / PENGUMUMAN**Asli → tujuan yang telah diedit**

Catatan #101, #188 Pesan #84 · pengirim tidak diketahui

KELOMPOK / OPERASI**Pengguna 71001 memposting tautan baru**

Catatan #146 · pesan #309 Bukti penyimpanan berkas #151

BOT / PERCAKAPAN PEMESANAN**Sebuah tombol mengarah ke tujuan tersebut**

Catatan #173 · pesan #12 Metadata tombol "Kembali"

PRIVAT / TINDAK LANJUT**Pengguna 71001 mengulangi tujuan**

Catatan #205 · pesan #922 Tanda terima file yang disimpan #209

Empat obrolan memberikan pengamatan yang berbeda-beda. Ikuti catatan sumber untuk setiap koneksi; jangan mengaitkan posting saluran tersebut dengan pengguna 71001 tanpa pengirim yang teridentifikasi.

ID numerik dan referensi catatan yang digunakan dalam panduan ini adalah fiktif. Peta ini menjelaskan alur kerja seorang analis dalam menggunakan fitur pencarian, profil, dan pemeriksaan catatan; aplikasi ini tidak menghasilkan grafik investigasi global.

| Koneksi | Pengamatan pendukung | Kesimpulan yang perlu dipertahankan |
| --- | --- | --- |
| Akun Telegram yang sama | ID Pengguna 71001 di grup #146 dan obrolan pribadi #205 | ID pengirim yang sama tercantum di kedua obrolan tersebut. Identitas di dunia nyata tetap menjadi pertanyaan terpisah. |
| Tujuan yang diulang | `pay.example.invalid/new` di #146, metadata tombol #173, postingan yang diedit #188 dan #205 | Tujuan yang sama muncul dalam empat konteks yang diamati. Hal ini saja tidak cukup untuk menentukan siapa yang mengendalikannya. |
| Ukuran file yang sama | Nilai SHA-256 yang sama persis pada tanda terima media yang telah selesai #151 dan #209 | Kedua lampiran yang disimpan tersebut identik secara byte. Nama file atau thumbnail saja tidak cukup untuk membuktikannya. |

Profil pengguna mencakup penulis yang memiliki pesan tersimpan dalam obrolan tersebut dan menghubungkannya dengan obrolan lain dalam *jurnal ruang kerja* yang *sama*. Profil ini bukanlah direktori keanggotaan yang lengkap. Nilai hash avatar berasal dari cache lokal terpisah; kutipan profil memiliki batas yang dapat dikonfigurasi di bawah **Parameter → Catatan yang dikutip per fakta**.

## 5. Rekonstruksi urutan dan tandai celah-celahnya

Di **bagian Chats**, periksa versi yang disimpan beserta tautan **catatan Jurnal #…** yang menyertainya. Di **bagian Jurnal**, gunakan opsi **Semua sumber** ditambah **Pengeditan**, **Penghapusan**, dan **Cakupan**. Buat garis waktu kasus dengan menggunakan tanggal Telegram yang disediakan serta waktu pengamatan pengumpul data.

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

Urutan jurnal mengikuti urutan penerimaan, bukan urutan tindakan asli di Telegram. Cuplikan riwayat yang lebih lama dapat muncul setelah pesan langsung yang lebih baru. Pastikan untuk membedakan antara pengamatan langsung, cuplikan, pesan yang dipulihkan, pemberitahuan penghapusan, dan “tidak ditemukan saat diperiksa ulang”. Tambahkan interval “tidak diketahui” secara eksplisit di mana pun terdapat celah dalam cakupan; cuplikan yang lebih baru tidak akan menghapus celah tersebut.

## 6. Perluas penerapan ke akun pengumpul lainnya

Tambahkan ruang kerja untuk setiap akun yang berbeda dan ulangi inventarisasi cakupan serta riwayat. Catat keanggotaan/peran dan sidik jari kunci penandatanganan untuk masing-masing akun. Pastikan pengidentifikasi dikualifikasikan berdasarkan ruang kerja dan obrolan: nomor pesan yang sama bukanlah pengidentifikasi lintas akun secara global.

Bandingkan pengamatan yang relevan dalam catatan kasus atau alat analisis Anda, dengan tetap mencantumkan referensi akun dan jurnal untuk setiap baris. Saat ini, TgWitness belum menyediakan fitur pencarian global tunggal, garis waktu gabungan, grafik kontak, atau arsip kasus yang mencakup seluruh ruang kerja. Ekspor lengkap multi-akun dari satu saluran atau supergrup merupakan fitur terpisah; ini bukanlah penggabungan dari semua jurnal akun.

Selama proses kerja yang lebih lama, tambahkan [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/witness/) untuk mempertahankan batasan-batasan sebelumnya. Gunakan uji coba pengiriman terkontrol untuk memverifikasi jalur penangkapan dan visibilitas akun-akun tersebut.

## 7. Menyediakan paket kasus yang lengkap dan dapat diverifikasi

Ekspor berkas ZIP jurnal yang telah ditandatangani dari setiap ruang kerja. Berkas tersebut berisi jurnal lengkap yang terekam, terlepas dari filter pencarian panel. Ekspor profil orang-orang yang relevan secara terpisah, pertahankan setiap bundel riwayat obrolan lengkap, dan simpan bukti lampiran yang telah lengkap.

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

Simpan sidik jari tepercaya melalui saluran terpisah. Dari instalasi tepercaya, verifikasi setiap artefak berdasarkan identitas ruang kerjanya sendiri:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Periksa hasil verifikasi yang sebenarnya, simpan salinan asli, dan pertahankan laporan cakupan, kegagalan akuisisi, serta catatan transfer bersama temuan Anda. Folder kasus tingkat atas dan kesimpulan analis disusun secara eksternal; setiap artefak TgWitness memiliki tanda tangan tersendiri.

## Gunakan metode yang sama untuk penyelidikan lainnya

**Sengketa pesanan atau pembayaran yang dipicu oleh bot**

**Pertanyaan:** Apa yang dijanjikan oleh bot tersebut, tombol mana yang disediakan, dan apa yang berubah setelahnya?

**Jejak:** postingan masuk saluran → pratinjau tautan bot yang disimpan → parameter awal bot → pesan dan versi keyboard → tanda terima panggilan balik yang dikeluarkan panel → tindak lanjut grup/pribadi. Cocokkan setiap tujuan dengan catatan sumbernya; pertahankan deskripsi profil dan media yang lengkap.

**Hasil yang disajikan:** garis waktu penawaran dan tanggapan yang teramati, referensi sumber, serta ekspor data yang telah diverifikasi. Tautan pembayaran yang ditampilkan bukanlah bukti bahwa pembayaran telah terjadi.

**Pesan yang dihapus setelah insiden lintas obrolan**

**Pertanyaan:** apa yang telah diamati sebelum pesan-pesan yang relevan menghilang?

**Jejak:** semua obrolan yang terpengaruh → pesan asli → pengeditan yang terkirim → pemberitahuan penghapusan atau hasil "hilang saat diperiksa ulang" → lampiran yang disimpan → cakupan seputar insiden tersebut. Bandingkan pengamatan dari akun independen dengan tingkat visibilitas yang disebutkan.

**Hasil:** urutan versi yang disimpan dan interval yang tidak diketahui secara eksplisit. Jangan jadikan riwayat pesan yang tidak ada sebagai bukti bahwa seseorang telah menghapusnya.

**Seorang peserta mengganti nama di beberapa obrolan**

**Pertanyaan:** aktivitas mana yang teramati berasal dari akun Telegram yang sama meskipun namanya telah berubah?

**Jejak:** ID pengirim numerik → riwayat nama/nama pengguna yang disimpan → balasan → obrolan lain di ruang kerja → tujuan yang disebutkan dan file yang disimpan. Periksa catatan sumber untuk setiap koneksi yang diklaim; pisahkan akun yang mirip.

**Hasil yang diberikan:** garis waktu aktivitas akun yang disertai sumber rujukan dan hipotesis terpisah mengenai hubungan antar akun. Kesamaan nama dan pHash avatar hanyalah petunjuk, bukan bukti identitas.
