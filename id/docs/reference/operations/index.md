# Alur kerja dan operasi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/operations/

Pengoperasian harian panel: mode, kategori pemantauan, parameter, pemberitahuan, ekspor, pencadangan, dan kapasitas.

Untuk koneksi pertama Anda, gunakan [akun dan format sesi](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/). Untuk penjelasan mengenai versi yang disimpan, kebijakan peristiwa, dan celah, lihat [cara kerja pengumpulan data](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/). Panduan ini mencakup operasi harian dan pemulihan.

## Alur kerja operator

Diagram alur · Pilih penyimpanan dan perlindungan kunci → Buka panel dengan tokennya; Buka panel dengan tokennya → Pilih ruang kerja; Pilih ruang kerja → Konfigurasikan rute langsung atau melalui proxy; Konfigurasikan rute langsung atau melalui proxy → Masukkan nomor telepon atau pilih berkas / QR; Masukkan nomor telepon atau pilih berkas / QR → Periksa identitas akun dan pilih grup yang dapat diakses; Periksa identitas akun dan pilih grup yang dapat diakses → Simpan kebijakan peristiwa dan lampiran, lalu mulailah pemantauan; Simpan kebijakan peristiwa dan lampiran, lalu mulailah pemantauan → Memantau kesalahan, akses, antrian, dan disk; Memantau kesalahan, akses, antrian, dan disk → Pertahankan titik pemeriksaan independen; Pertahankan titik pemeriksaan independen → Ekspor dan verifikasi materi · Pilih penyimpanan danperlindungan kunci · Buka panel dengantokennya · Pilih ruang kerja · Konfigurasikan rutelangsung atau melaluiproxy · Masukkan nomor teleponatau pilih berkas / QR · Periksa identitas akundan pilih grup yangdapat diakses · Simpan kebijakanperistiwa danlampiran, lalumulailah pemantauan · Memantau kesalahan,akses, antrian, dandisk · Pertahankan titikpemeriksaan independen · Ekspor dan verifikasimateri

**Diagram dalam bentuk teks**

1. Pilih penyimpanan dan perlindungan kunci → Buka panel dengan tokennya
2. Buka panel dengan tokennya → Pilih ruang kerja
3. Pilih ruang kerja → Konfigurasikan rute langsung atau melalui proxy
4. Konfigurasikan rute langsung atau melalui proxy → Masukkan nomor telepon atau pilih berkas / QR
5. Masukkan nomor telepon atau pilih berkas / QR → Periksa identitas akun dan pilih grup yang dapat diakses
6. Periksa identitas akun dan pilih grup yang dapat diakses → Simpan kebijakan peristiwa dan lampiran, lalu mulailah pemantauan
7. Simpan kebijakan peristiwa dan lampiran, lalu mulailah pemantauan → Memantau kesalahan, akses, antrian, dan disk
8. Memantau kesalahan, akses, antrian, dan disk → Pertahankan titik pemeriksaan independen
9. Pertahankan titik pemeriksaan independen → Ekspor dan verifikasi materi

Otorisasi, konektivitas jaringan, akses ke grup, dan kelengkapan pengiriman merupakan properti yang berbeda. Status koneksi berwarna hijau tidak berarti semua peristiwa telah terekam.

## Bagikan hasil kerja tanpa membagikan kunci utama

**Akses** Terbuka untuk memberikan token tersendiri kepada peninjau atau analis. Pilih akun dan obrolan yang dapat mereka buka, lalu izinkan tindakan melihat, mengekspor, atau tindakan operasional. Seorang operator yang memulai/menghentikan pengumpulan memerlukan akses ke seluruh ruang kerja; seorang peninjau dapat dibatasi hanya pada satu obrolan. Batasan sesi, masa berlaku, dan aturan IP terpisah dari otorisasi akun Telegram. Lihat [akses dan izin](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/).

Gunakan **"Open sessions"** untuk mengakhiri koneksi atau mencabut akses guna mengakhiri semua sesinya. Konsol administrator menggabungkan aktivitas proses saat ini di seluruh ruang kerja. Penutupan sesi tidak menghentikan proses pengumpulan data.

## Mode runtime

| Mode | Tindakan | Perilaku |
| --- | --- | --- |
| Demo | scripts\Demo.cmd atau `--demo` | Data sintetis; koneksi akun asli dinonaktifkan |
| Pengamatan | Mulai pemantauan | Mencatat pembaruan yang telah dikirimkan untuk sumber-sumber yang dipilih |
| Cuplikan riwayat | Sumber → cuplikan riwayat | Maksimal 500 pesan terkini; tidak ada rekonstruksi atas semua perubahan di masa lalu |
| Jeda | Jeda pengamatan | Hentikan pengumpulan data sambil tetap menyimpan data dan pekerjaan yang sedang dalam antrian |
| Tinjauan/serah terima | Ekspor | ZIP, JSONL/CSV/HTML, titik pemeriksaan, tanda terima proses, dan permintaan cap waktu |
| Beberapa akun | Ruang kerja atau tombol **+** di bagian atas | Jumlah ruang kerja terpisah yang tidak terbatas dalam satu proses |

Akses demo lokal terbuka secara otomatis tanpa perlu memasukkan token secara manual. Fitur ini menggunakan kemampuan seumur proses yang hanya berlaku untuk akses loopback langsung ke demo sintetis yang terisolasi; token panel utama tidak diungkapkan. Ruang kerja nyata serta akses demo jarak jauh atau melalui proxy tetap memerlukan otentikasi token. Akses demo tidak memberikan otorisasi apa pun di Telegram.

## Kategori pemantauan

![Pengaturan pemantauan per akun dengan data sumber sintetis](https://phishdestroy.github.io/TgWitness/assets/sources.png)

Di **Sumber → Pengaturan penangkapan → Pilih perubahan mana yang akan disimpan**, pilih pesan baru, pengeditan, pemberitahuan penghapusan, pembaruan reaksi, dan peristiwa keanggotaan secara terpisah. Pengaturan default menyimpan semua kategori. **Pesan, pengeditan, & penghapusan** mempertahankan konteks asli sambil menonaktifkan pembaruan reaksi/keanggotaan terpisah. **Semua aktivitas yang terlihat** memulihkan kelima kategori tersebut. Pengaturan awal mengubah formatnya; tekan **Simpan pengaturan pemantauan** untuk menerapkannya.

Kebijakan yang disimpan berlaku untuk semua sumber yang dipilih di ruang kerja tersebut. Ruang kerja lainnya mempertahankan pengaturannya masing-masing. Setiap perubahan aktual mencatat nilai sebelum/sesudah yang telah ditandatangani; kebijakan saat ini juga disertakan dalam tanda terima proses dan catatan awal pengamatan. Menonaktifkan suatu kategori tidak menghapus pengamatan sebelumnya. Mengaktifkan kembali tidak akan memulihkan perubahan yang terlewatkan. Tidak ada penggantian kategori per-kelompok dalam versi ini.

Biarkan opsi "pesan baru" tetap aktif jika konten sebelumnya penting: pemberitahuan penghapusan tidak dapat memulihkan teks yang tidak pernah direkam. Catatan operasional/cakupan dan peristiwa layanan grup lainnya selalu disimpan. Cuplikan riwayat eksplisit terpisah dari pemilihan kategori langsung dan mungkin mencakup pesan layanan. Opsi-opsi ini tidak menyensor metadata reaksi/anggota yang tertanam dalam objek Telegram yang telah direkam.

Cuplikan riwayat mungkin mengantrekan lampiran saat dalam keadaan dijeda. Mulailah pemantauan untuk memproses lampiran tersebut. Berada dalam antrean tidak berarti telah diunduh. File asli yang tidak tersedia tidak diganti dengan versi yang lebih baru yang telah diedit; hasilnya dicatat secara terpisah.

**Mengunci** akan menghapus akses browser dan bidang rahasia, tetapi tetap membiarkan proses pengumpulan data berjalan. Menutup tab juga akan membiarkan proses tetap berjalan. Menghentikan proses Python atau layanan akan menghentikan pengumpulan data terlepas dari status browser.

Menghapus ruang kerja tambahan akan menghentikan pengumpulnya dan menghapus data lokalnya. Jika file terkunci atau kesalahan sistem berkas mengganggu proses penghapusan, panel akan melaporkan kegagalan tersebut dan tetap mencantumkan ruang kerja tersebut sebagai tidak tersedia (`DeletionPending`). Tutup program yang menyimpan file-file tersebut dan coba lagi dengan opsi **Hapus**. Memulai ulang TgWitness akan membuat ruang kerja tersebut tetap dalam status terhenti dan tidak akan membuat ulang jurnal atau kunci yang telah dihapus sebagian. Penghapusan yang berhasil dicatat hanya setelah direktori tersebut dihapus; salinan yang diekspor atau dicadangkan secara terpisah tetap berlaku sesuai kebijakan penyimpanan masing-masing.

## Pemberitahuan

Buka **Sumber → Pemberitahuan → Peringatan dan ringkasan harian**. TgWitness menggunakan Apprise untuk mengirim peringatan ke Matrix, Telegram, Discord, Slack, ntfy, email, dan layanan lain yang didukung. Anda dapat menambahkan beberapa tujuan ke satu ruang kerja.

1. Masukkan satu URL tujuan Apprise per baris. Gunakan [katalog layanan dan format URL](https://appriseit.com/services/) yang sesuai untuk layanan Anda.
2. Aktifkan "**Kirim pemberitahuan**", lalu pilih peringatan masalah, perubahan dalam obrolan yang dipantau, dan ringkasan harian. Jam dalam ringkasan menggunakan waktu server.
3. Aktifkan "**Sertakan kutipan singkat"** jika Anda ingin teks yang disimpan dari pesan yang dihapus dan diedit muncul dalam pemberitahuan.
4. Tekan **Simpan pemberitahuan**, lalu **Kirim uji coba** untuk memeriksa pengiriman.

Untuk penerima Anda sendiri, gunakan [webhook JSON](https://appriseit.com/services/json/) Apprise. Misalnya, `jsons://notify.example.org/tgwitness` mengirim JSON melalui HTTPS ke titik akhir tersebut. Ini adalah contoh fiktif; gantilah dengan tujuan Anda sendiri.

Tujuan dan pengaturan merupakan bagian dari ruang kerja yang dipilih. Pemberitahuan perubahan mencakup sumber-sumber yang dipantau, termasuk obrolan yang baru ditambahkan. Lonceng di bilah atas juga mencantumkan masalah terbaru dan perubahan obrolan.

Dalam demo, kontrol notifikasi terlihat tetapi pengiriman dinonaktifkan. Konfigurasikan pengiriman di ruang kerja yang sebenarnya. Notifikasi menggunakan rute Direct, SOCKS5, atau HTTP dari ruang kerja tersebut; MTProxy tidak dapat mengantarkannya. Tujuan non-HTTP seperti SMTP memerlukan rute langsung.

## Tata letak panel

![Ruang kerja koneksi menggunakan data sintetis](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Jurnal** menampilkan pengamatan, pencarian, dan filter. Pengeditan akan menampilkan versi yang terekam; penghapusan akan menampilkan konten sebelumnya jika tersedia. Sumber yang tidak diketahui tetap disebutkan secara eksplisit. Jumlah tersedia di bagian **Ikhtisar**; rincian akuisisi tetap ada di panduan lokal.

**Sumber** mencakup cakupan pengamatan (obrolan yang dipilih, folder Telegram, atau seluruh akun), obrolan yang dapat diakses dari segala jenis, sumber terpilih dengan bintang prioritas, pengaturan lampiran dan pemeriksaan ulang, serta cuplikan riwayat. Sumber pribadi dipilih berdasarkan dialog/ID tanpa tautan publik. Status akses menggambarkan pemeriksaan terbaru, bukan izin permanen.

**Obrolan → Daftar Kontak** menampilkan semua orang yang pesannya telah disimpan; jika profil kontak diaktifkan untuk obrolan tersebut, satu klik akan membuka profil orang tersebut beserta tautan ke catatan jurnal.

**Witness** membuat token saksi yang hanya dapat dibaca, menampilkan kapan setiap saksi terakhir kali diperiksa, dan menyediakan perintah serta opsi untuk menjalankan satu [saksi (saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/)).

**Parameter** mencakup setiap batasan dan kecepatan ruang kerja yang tidak tercantum di halaman lain: berapa banyak percakapan yang dibaca, seberapa sering daftar obrolan dibaca ulang, interval heartbeat dan checkpoint , buffer saat startup, bagaimana pemeriksaan ulang mendistribusikan permintaannya (penundaan awal, jumlah obrolan per putaran, jeda antar obrolan, pesan yang dipulihkan dan diminta ulang), cadangan disk, batas waktu dan upaya ulang unduhan, apa yang dicari oleh profil pengguna (termasuk ekspresi reguler Anda sendiri), ukuran dan frekuensi notifikasi, batas snapshot, ZIP, dan unduhan browser, serta batas waktu dan upaya ulang klien Telegram. Setiap bidang menampilkan rentang dan nilainya secara default; bidang yang diubah ditandai dan dapat dikembalikan satu per satu atau sekaligus. Setiap perubahan dicatat sebagai "`parameters.changed`" beserta nilai sebelum dan sesudahnya, sedangkan catatan awal pemantauan mencantumkan nilai yang berlaku. Nilai-nilai berlaku mulai dari penggunaan berikutnya; batas waktu klien dan upaya ulang berlaku mulai dari koneksi berikutnya. Interval pemeriksaan ulang, jenis dan ukuran lampiran, bukti, serta interval salinan di luar situs tetap berada di halaman masing-masing dan dapat diatur ke nilai apa pun dalam rentangnya, tidak hanya pengaturan bawaan.

Lonceng di bilah atas mencantumkan masalah dan perubahan terbaru dalam obrolan yang dipantau; pesan yang belum dibaca akan dihitung hingga ditandai sebagai telah dibaca. Perubahan dikelompokkan per obrolan dan per jam ("12 dihapus, 1 diedit, 0 tidak ditemukan"), dan masalah seperti logout atau disk penuh tetap ada dalam daftar terlepas seberapa sibuknya obrolan tersebut.

**Pembuatan akun** dimulai dari kolom nomor telepon. **Lanjutkan** akan langsung mengarah ke halaman memasukkan kode, dan hanya meminta kredensial API jika belum ada. QR dan impor file adalah tab alternatif. Kredensial API yang disimpan hanya digunakan kembali di dalam ruang kerja masing-masing. Layar masuk tidak memiliki bilah samping, statistik, atau paragraf pengaturan. Ikon **Pengaturan** membuka kontrol API, proxy, penyimpanan, dan akun tambahan. Instalasi baru dimulai dari sini; akun yang terhubung tanpa sumber yang dipilih dimulai dari **Pilih obrolan**. Mengubah rute memerlukan penghentian sementara pengamatan dan membatalkan proses login yang belum selesai. Jurnal yang sudah ada tidak dapat dihubungkan kembali secara diam-diam ke akun Telegram yang berbeda.

**Fitur ekspor** memeriksa integritas jurnal dan menghasilkan berkas yang portabel. ID ruang kerja dapat disertakan ke dalam perintah baris perintah (CLI) unduhan. Setiap ekspor menetapkan awalan jurnal lengkap; peristiwa selanjutnya akan dimasukkan ke dalam ekspor berikutnya. Filter pencarian tidak mengubah cakupan paket. Informasi terperinci mengenai penandatanganan dan cakupan terdapat di bagian **Verifikasi & batasan**.

Panel ini melaporkan status pengumpul, media yang antri/gagal, media tertunda tertua, ruang disk kosong, jeda permintaan, dan sumber yang aksesnya belum dikonfirmasi di bawah **kesehatan Pengumpul**. Detail-detail ini awalnya ditutup dan disembunyikan di halaman Akun. Kartu pengaturan menunjukkan langkah selanjutnya: hubungkan akun, pilih sumber, atau mulai pemantauan. Daftar akun merupakan cuplikan pada saat dimuat; ruang kerja yang dipilih diperbarui secara berkala. Ini bukanlah pemantau SLA multiproses.

Antarmuka pengguna (UI) menggunakan aset lokal dan rendering teks untuk konten sumber. Tata letak desktop dan tata letak Chromium yang sempit telah diuji. Ini bukanlah sertifikasi aksesibilitas yang lengkap; evaluasi kegunaan bagi pembaca layar dan pengguna manusia tetap menjadi pekerjaan terpisah.

## Lingkungan penerapan

| Lingkungan | Instalasi | Status verifikasi |
| --- | --- | --- |
| PC/server Windows | Python 3.11+, scripts\Setup.cmd/Start.cmd, direktori data pribadi | Telah diuji secara lokal pada Windows/Python 3.12 |
| Server Linux/VPS | Python venv, pengguna layanan khusus, HTTPS/SSH | Contoh kode, CI, dan systemd disertakan; tidak dijalankan di host ini |
| macOS | Python venv, proses latar depan, atau agen pengguna | Contoh launchd disertakan; diperlukan pemeriksaan instalasi terpisah |
| Docker/Compose | Volume yang konsisten, satu pekerja | Definisi dan pemeriksaan runtime CI disediakan; Docker tidak tersedia secara lokal |
| Browser ponsel | Masuk ke panel yang dilindungi pada server yang sedang berjalan | Tata letak Chromium yang disempurnakan telah diuji; pengumpul data tidak berjalan di iOS/Android |

Portabilitas berarti tidak ada layanan cloud atau pembangunan frontend yang wajib. Setiap target tetap memerlukan dependensi Python/kripto yang kompatibel, disk lokal, dan akses jaringan. Lihat [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/) dan [templat layanan](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Ruang kerja berbagi CPU, memori, dan loop peristiwa. Untuk isolasi proses, gunakan instansi, port, direktori data, dan otorisasi akun yang berbeda. Tidak ada panel terpadu di antara instansi yang terpisah. Jangan pernah mengarahkan beberapa pekerja ke satu basis data.

## Pemeriksaan awal dan ekspor

Jalankan perintah `python start.py --check` sebelum memulai lingkungan yang telah disiapkan. Tambahkan `--json` untuk pemeriksaan yang dapat dibaca mesin atau masukkan nilai `--data-dir`, `--host`, dan `--port` yang diinginkan. Perintah ini memeriksa prasyarat tanpa perlu login ke Telegram atau membuat jurnal. Perintah ini tidak memverifikasi jurnal atau membuktikan kesiapan penangkapan; verifikasi jurnal dilakukan saat aplikasi dimulai. Port yang sudah terpakai mungkin hanya merupakan instance yang sudah ada.

Browser yang mendukung File System Access API menyimpan ekspor melalui aliran yang dapat ditulis (writable stream). Browser lain menyimpan data dalam buffer maksimal 128 MiB. Gunakan CLI streaming untuk ekspor berukuran lebih besar atau browser yang tidak mendukung streaming file:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Tambahkan `--profile ID` dari Ekspor untuk ruang kerja anak. Gunakan `--url https://server` untuk akses jarak jauh. HTTP biasa hanya diterima untuk tujuan loopback. Token dibaca dari file dan dikirim dalam header, tidak dicetak atau dimasukkan ke dalam URL. Pengalihan ditolak. Tujuan yang sudah ada tidak akan ditimpa. Transfer yang gagal akan menghapus file bagian sementara mereka. SHA-256 yang dilaporkan adalah checksum transfer; verifikasi ZIP yang ditandatangani secara terpisah dengan sidik jari/titik pemeriksaan tepercaya.

## Pencadangan, pemulihan, dan gangguan

1. Jeda pengamatan dan hentikan proses dengan rapi.
2. Salin seluruh direktori data: database, WAL/SHM jika ada, media, `credentials.enc`, `signing.enc`, `network.enc`, kunci/metadata vault, token, titik pemeriksaan, dan setiap direktori `profiles/`.
3. Untuk mode kunci eksternal, simpan kunci utama secara terpisah dan pertahankan setiap `vault.external.json`. Pembuatan kunci baru tidak dapat memulihkan rahasia lama.
4. Pulihkan saat tujuan sedang dihentikan; konfigurasikan kunci asli, batasi akses, dan verifikasi integritas sebelum melanjutkan.
5. Catat waktu henti dan hasil verifikasi. Cuplikan riwayat tidak dapat membuktikan bahwa tidak ada penghapusan yang terjadi selama gangguan tersebut.

Berkas ZIP bukti tidak menyertakan sesi/kunci pribadi dan bukan merupakan cadangan layanan lengkap. Empat hal dilindungi dengan cara yang berbeda:

| Apa | Perlindungan |
| --- | --- |
| Berkas ekspor tanpa kata sandi (bawaan) | Tidak dienkripsi. Ditandatangani, sehingga perubahan dapat dideteksi, tetapi siapa pun yang memiliki berkas tersebut dapat membacanya |
| Berkas ekspor dengan kata sandi | Jika Anda menetapkan kata sandi, hasil ekspor yang sudah jadi akan disimpan tanpa perubahan ke dalam berkas ZIP WinZip yang dienkripsi dengan AES-256 dan dapat dibuka dengan 7-Zip serta WinRAR; kata sandi tersebut tidak disimpan ([penanganan bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)) |
| Basis data jurnal dan lampiran yang disimpan di disk | Tidak dienkripsi oleh TgWitness; gunakan disk atau volume yang dienkripsi |
| Sesi Telegram dan kunci penandatanganan | Terenkripsi di direktori data (`credentials.enc`, `signing.enc`, `network.enc`) |

Cadangan layanan penuh adalah direktori data yang dihentikan seperti yang dijelaskan di atas, bukan ekspor. Gunakan penyimpanan yang dilindungi dan mekanisme transfer yang terencana untuk keduanya. Ekspor server sementara disimpan di `temporary-exports/` masing-masing ruang kerja; respons yang telah selesai dibersihkan, dan file ekspor yang terputus dihapus pada saat startup berikutnya saat kunci instance ruang kerja tersebut masih berlaku.

Peristiwa pemulihan koneksi tidak menjamin pemulihan perubahan yang terjadi di antara waktu tersebut. Tugas media yang persisten dan posisi pembaruan Telegram tetap ada setelah restart; lihat [format bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Kapasitas dan masa penyimpanan

Batas default, semuanya dapat diubah di bawah **Parameter**: 1.000 percakapan pertama, 500 pesan per snapshot, 4 GiB konten ZIP yang ditandatangani dan tidak terkompresi (arsip yang lebih besar memerlukan `verify.py --max-gib N`), serta cadangan browser sebesar 128 MiB. Lampiran memakan ruang 1–2.000 MiB per jenis di bawah **Sumber → Lampiran**. CLI unduhan secara default mentransfer 5 GiB. Ruang disk yang tersedia dapat menjadi batas bawah. Sediakan ruang untuk jurnal, media, WAL, ekspor sementara, dan cadangan. Ekspor menggunakan volume data, bukan `/tmp` sebesar 512 MiB dari Compose.

Ukur peristiwa per detik, usia antrian, byte media, dan latensi disk, bukan hanya menghitung jumlah grup. Uji kinerja lokal sintetis tidak menjamin pengiriman pesan Telegram. Tidak ada penghapusan retensi otomatis. Menghapus bagian akhir jurnal akan membatalkan hubungan jurnal tersebut dengan titik pemeriksaan yang disimpan.

Pemeriksaan ulang prioritas sudah tersedia: sumber yang ditandai bintang diperiksa ulang setiap 15 menit secara default, sumber lainnya setiap 6 jam (lihat [tingkatan pemeriksaan ulang](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/#recheck-tiers)). Ekspor yang dilindungi kata sandi tersedia seperti yang dijelaskan di atas. Penerimaan Telegram/proksi secara langsung, pemutaran ulang yang tahan lama, log admin dan pemantauan reaksi, pekerja terisolasi, enkripsi jurnal lokal dan media oleh TgWitness sendiri, serta tinjauan independen tetap menjadi pekerjaan terpisah. Akses yang dibatasi didokumentasikan dalam [akses dan izin](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/). Lihat [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md,](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) dan [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/).
