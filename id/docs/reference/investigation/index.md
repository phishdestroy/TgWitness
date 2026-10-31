# Mode penyelidikan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/investigation/

Penyelidikan menyeluruh terhadap akun, mencakup saluran, grup, obrolan pribadi, dan bot, mulai dari lingkup penyelidikan hingga paket kasus yang terverifikasi.

Lacak sebuah kasus melintasi saluran, grup, obrolan pribadi, dan bot, mulai dari pengumpulan awal hingga garis waktu yang dirujuk dan penyerahan yang dapat diverifikasi. Versi situs web interaktif tersedia di `/docs/cases/`; [petunjuk pratinjau](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Contoh kasus: perubahan tujuan dalam empat percakapan

Sebuah pengumuman mengarah ke sebuah bot. Sebuah grup operasional mendiskusikan tujuan pembayaran baru, keyboard bot menampilkannya, dan pesan tindak lanjut pribadi mengulanginya. Pengumuman tersebut kemudian diedit dan pesan grup menghilang.

Pertanyaannya adalah: apa yang diamati sebelum dan sesudah perubahan, akun Telegram mana yang memposting setiap item, di mana tujuan tersebut muncul, byte lampiran mana yang dipertahankan, dan interval apa saja yang masih belum diketahui?

Semua nama, ID, waktu, dan referensi jurnal dalam contoh ini adalah fiktif. Alur kerja ini menggunakan fitur-fitur terkini; peta kasus hanyalah ilustrasi, bukan grafik otomatis yang dihasilkan oleh aplikasi.

Diagram alur · Saluran → Jurnal ruang kerja; Grup → Jurnal ruang kerja; Obrolan pribadi → Jurnal ruang kerja; Bot → Jurnal ruang kerja; Jurnal ruang kerja → Cari di semua sumber; Jurnal ruang kerja → Profil orang dengan referensi catatan; Jurnal ruang kerja → Versi yang disimpan dan tanda terima lampiran; Cari di semua sumber → Lini waktu analis dan daftar sumber; Profil orang dengan referensi catatan → Lini waktu analis dan daftar sumber; Versi yang disimpan dan tanda terima lampiran → Lini waktu analis dan daftar sumber; Jurnal ruang kerja → ZIP bukti yang ditandatangani; Lini waktu analis dan daftar sumber → Penyerahan kasus dengan bukti-bukti yang diverifikasi secara terpisah; ZIP bukti yang ditandatangani → Penyerahan kasus dengan bukti-bukti yang diverifikasi secara terpisah · Saluran · Grup · Obrolan pribadi · Bot · Jurnal ruang kerja · Cari di semua sumber · Profil orang denganreferensi catatan · Versi yang disimpan dantanda terima lampiran · ZIP bukti yangditandatangani · Lini waktu analis dandaftar sumber · Penyerahan kasus denganbukti-bukti yangdiverifikasi secaraterpisah

**Diagram dalam bentuk teks**

1. Saluran → Jurnal ruang kerja
2. Grup → Jurnal ruang kerja
3. Obrolan pribadi → Jurnal ruang kerja
4. Bot → Jurnal ruang kerja
5. Jurnal ruang kerja → Cari di semua sumber
6. Jurnal ruang kerja → Profil orang dengan referensi catatan
7. Jurnal ruang kerja → Versi yang disimpan dan tanda terima lampiran
8. Cari di semua sumber → Lini waktu analis dan daftar sumber
9. Profil orang dengan referensi catatan → Lini waktu analis dan daftar sumber
10. Versi yang disimpan dan tanda terima lampiran → Lini waktu analis dan daftar sumber
11. Jurnal ruang kerja → ZIP bukti yang ditandatangani
12. Lini waktu analis dan daftar sumber → Penyerahan kasus dengan bukti-bukti yang diverifikasi secara terpisah
13. ZIP bukti yang ditandatangani → Penyerahan kasus dengan bukti-bukti yang diverifikasi secara terpisah

## 1. Menjelaskan kasus dan mengumpulkan seluruh kronologi peristiwa

1. Hubungkan akun pengumpul ke ruang kerjanya sendiri. Dalam catatan kasus eksternal, catat referensi kasus, ID akun, ruang kerja, waktu mulai pengamatan, dan sidik jari kunci penandatanganan tepercaya.
2. **Sumber** Terbuka **→ Cakupan pengamatan → Mode investigasi**. Pengaturan default memilih **Seluruh akun**, saluran/grup/obrolan pribadi/bot, tindakan sendiri, profil sumber, serta 200 pesan terbaru yang terlihat untuk sumber yang baru ditemukan. Tinjau pengaturan tersebut, tekan **Simpan cakupan**, dan selesaikan konfirmasi cakupan.
3. **Muat obrolan** dan bandingkan sumber-sumber tersebut dengan daftar obrolan akun. Periksa pengecualian. **Parameter → Obrolan yang dibaca dari daftar akun** secara default berjumlah 1.000 dan memungkinkan hingga 20.000. Sumber di luar batas daftar akan ditambahkan saat mereka menjadi aktif. Catat apa yang sebenarnya terdaftar.
4. Di **pengaturan Perekaman**, pilih **Semua aktivitas yang terlihat** dan simpan pengaturan pemantauan. Periksa jenis lampiran/batasannya serta ruang disk yang tersedia.
5. Mulai pengamatan. Validasi pesan baru yang dikendalikan, pengeditan, dan penghapusan, kemudian simpan referensi pengujian dan segala kegagalan yang terjadi.

Cakupan seluruh akun merekam aktivitas yang terlihat oleh akun sesuai dengan pengaturan yang disimpan. Alat ini tidak mengakses obrolan rahasia atau secara otomatis bergabung dengan setiap grup yang tertaut. Alat ini juga tidak mengisi kembali setiap percakapan yang sudah ada. Lihat [cakupan pengumpulan](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Inventarisasi setiap sumber dan peroleh konteks historisnya

Buatlah daftar sumber dengan satu baris per obrolan:

| Bidang | Merekam |
| --- | --- |
| Identitas | Ruang kerja, ID akun, ID obrolan numerik, judul, dan jenis |
| Visibilitas | Keanggotaan/peran, akses yang telah dikonfirmasi atau belum dikonfirmasi, pengecualian |
| Perekaman langsung | Waktu mulai, jenis peristiwa yang dipilih, dan perubahan kebijakan selanjutnya |
| Riwayat jurnal | Permohonan/penyelesaian snapshot, batas, waktu, dan referensi catatan |
| Riwayat lengkap | Nama file ekspor per obrolan yang ditandatangani, batas, dan status keberhasilan/kegagalan |
| Lampiran | Tangkapan layar media yang telah diselesaikan, hash, ukuran, serta hasil yang dilewati/gagal |
| Cakupan | Gangguan layanan, pengambilan data yang tidak lengkap, FloodWait, pesan yang tidak tersedia, dan celah lainnya |

Gunakan metode pengumpulan data yang tepat untuk setiap sumber:

- **Memuat riwayat lengkap** di **Sumber** (`main` saat ini) memuat pesan-pesan masa lalu yang tersedia dari sumber yang diaktifkan ke dalam jurnal ruang kerja. Fitur ini mendukung jeda/lanjutkan serta laporan kemajuan yang ditandatangani. Lihat [perolehan riwayat](https://phishdestroy.github.io/TgWitness/id/docs/reference/history/).
- **Cuplikan riwayat** menyimpan pesan-pesan terbaru yang terlihat ke dalam jurnal pengamatan. Nilai maksimum defaultnya adalah 500; melalui menu **Parameter → Largest history snapshot,** nilai tersebut dapat ditingkatkan hingga 10.000. Ini adalah pengamatan riwayat terkini, bukan hasil rekonstruksi pengeditan.
- **Ekspor obrolan lengkap → Ekspor obrolan lengkap**, atau **Obrolan → Ekspor obrolan**, mengambil riwayat obrolan yang saat ini terlihat dari satu obrolan ke dalam bundel `chat.json` / `chat.html` terpisah yang telah ditandatangani. Ulangi untuk sumber-sumber kasus tersebut dan simpan setiap hasilnya.
- **Ketika obrolan atau bot baru muncul**, profilnya serta hingga 1.000 pesan terbaru dapat disimpan; mode penyelidikan memilih 200 pesan. Obrolan yang sudah ada tidak menerima pencatatan tersebut secara retroaktif saat mode tersebut diaktifkan.
- **Pengunduhan lampiran yang terlihat** akan menyimpan byte sesuai dengan kebijakan yang dikonfigurasi. Diperlukan tanda terima `media.saved` yang lengkap dengan SHA-256 dan jumlah byte. Pekerjaan yang sedang dalam antrian, gambar mini, atau nama file bukanlah lampiran yang disimpan.

Ekspor obrolan lengkap **tidak** akan mengisi jurnal atau profil pengguna dengan semua pesan yang ada. Gunakan opsi **"Muat riwayat lengkap"** atau "cuplikan jurnal terbatas" untuk riwayat yang perlu Anda analisis di dalam TgWitness. Periksa daftar sumber yang diaktifkan sebelum memulai proses pemuatan riwayat. Kedua metode tersebut tidak dapat memulihkan materi yang tidak lagi tersedia di Telegram.

## 3. Melestarikan perkembangan kasus dan interaksi yang disengaja

Tandai obrolan kasus aktif sebagai sumber prioritas. Tinjau interval pemeriksaan ulang, penyelesaian tunggakan, dan hasil media. Pastikan pengumpul data tetap aktif saat menggunakan akun. Gunakan **Obrolan → Profil → Simpan profil sekarang** untuk mempertahankan metadata sumber seperti deskripsi dan perintah bot. Hal ini terpisah dari profil pengguna yang dihasilkan dari pesan yang disimpan.

Jika kasus tersebut melibatkan pelacakan sumber atau interaksi dengan bot:

1. **Buka tautan Telegram → Simpan pratinjau** akan merekam tautan yang diberikan dan pratinjau yang ditampilkan sebelum tindakan dilakukan.
2. **Perintah "Join / open and observe"** melakukan tindakan join/open, dan mengirimkan parameter start bot jika disediakan. Permintaan join yang sedang menunggu persetujuan dicatat sebagai pending.
3. Balasan teks yang dikeluarkan panel dan penekanan tombol yang didukung mempertahankan `interaction.requested` dan `interaction.result`. Tanda terima callback dapat mempertahankan teks popup yang dikembalikan, status peringatan, dan URL.

Itu adalah tindakan akun yang sebenarnya. Penekanan tombol callback di aplikasi Telegram lain tidak terlihat oleh pengumpul, meskipun pesan atau pengeditan yang dihasilkan mungkin terlihat. Mini-client tidak menjalankan alur kerja aplikasi web, pembayaran, telepon, atau lokasi. Untuk perilaku yang tepat, lihat [interaksi panel](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/#act-from-the-panel).

## 4. Menghubungkan pengamatan di berbagai obrolan

Di **Jurnal**, pilih **Semua sumber** dan cari konten yang terekam. Buka catatan yang sesuai dan catat ruang kerja, obrolan, ID pesan, urutan, serta hash catatan.

Dalam obrolan yang relevan, buka **People → Aktifkan profil**, lalu periksa profil seseorang:

- Nama/nama pengguna yang teramati dari waktu ke waktu serta ID Telegram numerik.
- Hubungan balasan dengan referensi catatan sumber.
- **Juga terdapat di…** obrolan lain dalam jurnal ruang kerja ini di mana ID tersebut pernah menulis.
- Aktivitas, pengeditan/penghapusan, serta dompet, nomor telepon, nama pengguna, dan tautan yang disebutkan.
- Metadata avatar yang disimpan dan avatar serupa yang disimpan dalam cache, beserta asal masing-masing.

Buka catatan yang dikutip sebelum menggunakan profil yang dihasilkan dalam sebuah temuan. Profil mencakup orang-orang yang pesannya tersimpan, bukan setiap anggota grup. **Parameter → Catatan yang dikutip per fakta** membatasi daftar referensi, bukan jumlah aktivitas yang mendasarinya. Sebutan dan kemiripan avatar hanyalah petunjuk; keduanya tidak membuktikan kepemilikan atau identitas.

Dalam contoh yang telah disusun:

| Tautan | Merekam | Pengamatan yang didukung |
| --- | --- | --- |
| Akun pengirim yang sama | Grup #146 dan tindak lanjut pribadi #205 | Keduanya menyediakan ID pengirim Telegram 71001 |
| Tujuan yang sama | #146, bot keyboard #173, pengeditan saluran #188, pesan pribadi #205 | Semua berisi `pay.example.invalid/new`; kepemilikan/pengendalian belum ditetapkan |
| File yang disimpan sama | Telah diselesaikan: tanda terima media #151 dan #209 | Nilai SHA-256 lengkapnya cocok dengan byte yang disimpan |
| Sumber saluran | #101 dan #188 | Jangan mengaitkan postingan saluran kepada pengguna 71001 tanpa menyebutkan pengirimnya |

Bandingkan hash lampiran dan referensi pesan yang terkait. File yang identik tidak membuktikan adanya pembuat, pengirim ulang, atau operator yang sama. Nama yang sama dan avatar yang mirip saja tidak cukup untuk menggabungkan dua ID Telegram menjadi satu orang.

## 5. Membuat garis waktu lintas obrolan

Gunakan versi yang disimpan di **Obrolan** beserta tautan **catatan Jurnal #…**-nya. Di **Jurnal**, gabungkan **Semua sumber** dengan **Pengeditan**, **Penghapusan,** dan **Cakupan**. Simpan baik `source_at` (jika tersedia) maupun `observed_at`.

| Waktu pengamatan ilustratif | Referensi | Pengamatan |
| --- | --- | --- |
| 09:00 | Saluran #101 | Tujuan asli telah direkam |
| 09:12 | Grup #146; media #151 | Tujuan baru telah diposting; pengunduhan berkas telah selesai |
| 09:16 | Bot #173 | Tombol panah mengarah ke tujuan baru |
| 09:20 | Saluran #188 | Pengumuman telah diedit; kedua versi yang disimpan tetap ada |
| 09:24 | Pribadi #205; media #209 | ID pengirim yang sama mengulang alamat tujuan; byte file yang sama dipertahankan |
| 09:28 | Grup #231 | Pemberitahuan penghapusan telah diterima; pengirim penghapusan dan waktu penghapusan yang tepat tidak diketahui |

Catatan lain terjadi di antara referensi contoh ini. Nomor urut mengatur pengamatan; cuplikan riwayat dapat berisi tanggal sumber yang lebih lama dan tiba lebih lambat daripada peristiwa langsung. Bedakan antara cuplikan, pesan yang dipulihkan, pemberitahuan penghapusan, dan hasil "hilang saat diperiksa ulang". Tandai celah cakupan sebagai interval yang tidak diketahui. Akuisisi riwayat yang dilakukan kemudian tidak secara retroaktif menjamin pengamatan yang tidak terputus.

## 6. Tambahkan perspektif akun tanpa menghilangkan asal-usulnya

Gunakan ruang kerja terpisah untuk setiap akun yang berbeda dan ulangi inventarisasinya. Simpan ID akun, peran, sidik jari kunci penandatanganan, dan referensi sumber pada setiap perbandingan. Nomor pesan bukanlah pengenal global yang berlaku di seluruh obrolan/akun.

Korelasi lintas ruang kerja dilakukan dalam catatan kasus eksternal atau alat analisis. Saat ini, TgWitness belum memiliki fitur pencarian lintas ruang kerja secara global, garis waktu terpadu, grafik investigasi, atau arsip kasus gabungan. Ekspor multi-akun dari **satu** saluran/supergrup merupakan operasi yang berbeda, bukan penggabungan jurnal akun.

Untuk pekerjaan yang lebih panjang, pertahankan batasan dengan [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/). Gunakan pemeriksaan pengiriman terkontrol untuk memverifikasi jalur penangkapan dan visibilitas setiap akun.

## 7. Mengumpulkan dan memverifikasi serah terima kasus

Simpan semua ini dalam direktori kasus yang disusun oleh analis:

| Materi | Tujuan |
| --- | --- |
| Catatan kasus dan daftar sumber | Pertanyaan, kebijakan pengumpulan data, akses/peran, temuan, penjelasan alternatif, dan celah |
| Garis Waktu | Referensi waktu serta ruang kerja/obrolan/pesan/urutan untuk setiap entri |
| Berkas ZIP bukti yang ditandatangani per ruang kerja | Jurnal yang direkam secara lengkap, manifes, dan media yang disimpan; filter panel tidak membatasi ekspor jurnal |
| Berkas profil orang yang ditandatangani secara terpisah | Referensi yang diperoleh telah diverifikasi berdasarkan bukti di ruang kerja yang sesuai |
| Ekspor obrolan lengkap yang ditandatangani | Pengambilan riwayat yang terlihat saat ini, terpisah dari jurnal pengamatan |
| Jejak digital tepercaya dan titik pemeriksaan sebelumnya | Identitas utama dan batasan jurnal yang disimpan |
| Artefak Witness, jika dikonfigurasi | Jurnal terpisah, posting yang ditandatangani, dan sidik jari saksi |
| Hasil verifikasi dan hash berkas yang dikirimkan | Apa yang diperiksa, byte mana yang ditransfer, dan kepada siapa |

Dari instalasi tepercaya, dengan nama file dan sidik jari aktual setiap ruang kerja:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan hasil verifikasi aktual dan artefak asli. Direktori kasus tingkat atas, daftar sumber, dan kesimpulan analis disimpan secara eksternal; setiap artefak TgWitness memiliki tanda tangan dan prosedur verifikasi tersendiri.

## Sesuaikan penyelidikan

| Kasus | Lacak | Sampaikan |
| --- | --- | --- |
| Sengketa pesanan/pembayaran yang ditangani oleh bot | Pengumuman entri → pratinjau tautan yang disimpan → parameter awal bot → versi pesan dan keyboard → tanda terima panggilan balik panel → tindak lanjut pribadi/grup | Jadwal penawaran/tanggapan yang teramati dan sumber yang terverifikasi; tautan pembayaran saja tidak membuktikan adanya pembayaran |
| Pesan yang dihapus setelah terjadinya insiden | Semua obrolan yang terpengaruh → salinan asli/suntingan yang disimpan → hasil penghapusan atau tidak ditemukan saat diperiksa ulang → media yang disimpan → cakupan dan perspektif akun lainnya | Versi yang disimpan dan interval yang tidak diketahui secara eksplisit; tidak ada aktor penghapusan yang dibuat-buat |
| Seorang peserta mengganti nama di berbagai obrolan | ID pengirim numerik → riwayat nama/nama pengguna → balasan → obrolan lain yang teramati → tujuan/file yang disebutkan | Garis waktu aktivitas akun Telegram yang dikutip, dengan hipotesis identitas dan hubungan di dunia nyata yang dipisahkan |

[Referensi koleksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/) · [Verifikasi profil orang](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#people-profiles) · [Penyerahan bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#investigation-handoff) · [Validasi telah selesai](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/)
