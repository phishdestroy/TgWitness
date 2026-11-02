# Panduan panel

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/

Setiap layar pada panel: obrolan, jurnal, sumber, ekspor, Ekstra, mode perlindungan, dan pemeriksaan kode.

[Pengaturan awal dan konfigurasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/settings/) · [Akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/) · [Ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/) · [Laporan kasus](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/)

Fungsi setiap layar, apa yang ditulis ke jurnal yang ditandatangani, dan di mana panduan terperinci tersedia. Panel menampilkan satu ruang kerja pada satu waktu: satu akun Telegram dengan sumber, jurnal, dan kunci penandatanganan miliknya sendiri. Pemilih di bagian atas bilah samping digunakan untuk berganti ruang kerja. Alamat membawa informasi ruang kerja (`?ws=…`); selama alamat, pemilih, dan akun yang dimuat tidak sesuai, tindakan akan tetap diblokir.

## Temukan jalannya

Bagian harian terletak di bagian atas bilah samping, **"Akun"** berada di bawah **"Ruang Kerja"** , dan semua yang lain berada di bawah **"Alat & pengaturan lainnya"** . Tombol pengalih **tingkat antarmuka** di bilah atas menentukan berapa banyak bagian yang ditampilkan:

| Level | Bagian-bagian di bilah samping |
| --- | --- |
| Sederhana | Beranda, Obrolan, Perubahan, Arsip, dan Pengaturan |
| Standar | Lihat juga Case Board, Akun dan Akses |
| Ahli | Selain itu, terdapat bagian Sumber, Ekstra, Tanya Arsip, Parameter, Akun, Log Sistem, dan Integrasi |

Panggilan sederhana: Mulai di sini, Jurnal dan Ekspor **Beranda**, **Perubahan,** serta **Arsip**. Tingkat hanya menyembunyikan bagian-bagian tertentu. Fitur yang disembunyikan tetap berfungsi, dan server memeriksa setiap izin secara mandiri. Tingkat, bahasa, tema, dan zona waktu disimpan per operator dan ruang kerja; lihat [pengaturan](https://phishdestroy.github.io/TgWitness/id/docs/reference/settings/).

Bilah atas juga memiliki:

- **Buka bagian** (Ctrl+K, atau ⌘K di Mac): temukan obrolan, parameter, atau catatan jurnal dengan `#number`. Tombol panah untuk berpindah, Enter untuk membuka, Esc untuk menutup.
- **Pemberitahuan**: masalah dan perubahan obrolan diproses dari jurnal. Opsi **“Tandai Semua sebagai Telah Dibaca”** menghapus hitungan, sedangkan **“Aturan Pemberitahuan”** membuka pengaturan aturan. Pengiriman ke Telegram, Discord, atau email diatur di [Ekstra → Pemberitahuan](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#notifications).
- Indikator koneksi untuk ruang kerja ini. **Status kesehatan Collector** di bawah bilah atas membaginya menjadi koneksi Telegram, penerimaan peristiwa, sumber, dan antrian lampiran.
- **Kunci**: menutup panel di browser ini. Koleksi tetap berjalan di server.
- Mode perlindungan yang terletak di sebelah nomor versi; lihat [mode perlindungan](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#protection-modes).

Ruang kerja demo berisi pesan fiktif dan tidak pernah terhubung ke Telegram. Tindakan yang dapat mengubah ruang kerja asli akan ditolak di sana.

## Mulailah dari sini

Pilih sebuah tugas. **“Ekspor akun saya”** mengunduh semua yang dapat dibaca oleh akun tersebut saat ini. **“Ikuti penyelidikan”** mencatat pesan baru, perubahan yang diamati, dan pemberitahuan penghapusan dari obrolan yang Anda pilih. Kartu pengaturan menampilkan tiga langkah: hubungkan akun, pilih sumber, mulai pemantauan. Pertanyaan tujuan akan tetap muncul di halaman ini hingga Anda menjawab atau melewatinya. Ruang kerja baru akan membuka [pengaturan awal](https://phishdestroy.github.io/TgWitness/id/docs/reference/settings/) sebagai gantinya.

## Obrolan

Percakapan yang disimpan, secara default hanya dapat dibaca.

- Cari daftar berdasarkan nama atau ID. **Pilih** menambahkan atau menghapus obrolan yang diawasi. **Buka tautan Telegram** menerima nama pengguna atau tautan undangan dan menyimpan pratinjau ke jurnal. **Gabung / buka dan amati** kemudian bergabung ke obrolan dan menambahkannya ke sumber Anda; membuka bot akan mengirimkannya `/start`.
- Header obrolan menghitung pesan **yang dihapus, teks yang disimpan**, pesan **yang dihapus sebelum disimpan**, dan **pesan yang tidak ditemukan saat diperiksa ulang**. Daftar obrolan dan notifikasi menggunakan definisi yang sama. Pesan yang dihapus berwarna merah dan tetap menyimpan teks yang telah disimpan; pesan yang diedit tetap menyimpan setiap versi yang telah disimpan. Setiap penghapusan menunjukkan informasi yang diketahui: kapan pesan tersebut dilihat, bahwa Telegram tidak melaporkan siapa yang menghapusnya, atau bahwa hanya pemberitahuan yang diterima.
- **Riwayat muat** menampilkan 100, 250, atau 500 pesan terakhir di tampilan ini dan di jurnal. Untuk memuat semua sumber yang diaktifkan, gunakan [Sumber → Riwayat lengkap](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#sources).
- **Fitur Ekspor Obrolan** mengunduh seluruh riwayat yang terlihat sebagai file yang ditandatangani `chat.json` dan `chat.html`. Beberapa akun yang terhubung dapat berbagi pekerjaan: masing-masing mengunduh rentang nomor pesan miliknya sendiri dan menandatangani bagiannya, sedangkan akun yang memulai proses ekspor menandatangani arsip tersebut. Lihat [cara mengekspor satu obrolan](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- Daftar **Orang** menampilkan semua orang yang memiliki pesan tersimpan di obrolan ini. Profil Orang dinonaktifkan secara default karena berisi data pribadi pihak ketiga. Saat diaktifkan untuk suatu obrolan, profil menampilkan nama dan riwayat nama pengguna, bendera Telegram, hash avatar, aktivitas, siapa yang membalas siapa, obrolan lain yang diamati, serta dompet, nomor telepon, nama pengguna, dan tautan yang disebutkan. Setiap fakta mengarah ke catatannya. **Mengekspor profil** akan menyimpan berkas yang ditandatangani, secara opsional dalam ZIP yang dilindungi kata sandi; menonaktifkan profil akan menghapus berkas profil tersebut. Lihat [profil pengguna](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#people-profiles).
- **Fitur "Simpan Profil" kini** merekam cuplikan profil obrolan atau bot: deskripsi, anggota, tautan undangan, dan perintah bot.

### Hanya baca, pengiriman, dan rahasia

Dua tombol di atas pesan berfungsi untuk melindungi akun dan pembaca:

- Mode **hanya baca** aktif saat obrolan dibuka. Matikan mode ini untuk mengirim pesan atau menekan tombol bot . Setiap tindakan akan menanyakan **"Kirim sebagai @akun?**" atau **"Tekan tombol bot ini sebagai @akun?**", yang memberi tahu Anda bahwa anggota obrolan akan melihatnya dan bahwa tindakan tersebut akan masuk ke dalam jurnal yang telah ditandatangani. **Pilihan "Jangan tanyakan lagi selama 10 menit dalam obrolan ini"** akan melewatkan pertanyaan tersebut untuk sementara waktu. Fitur pengiriman dinonaktifkan untuk tujuan "**Bukti untuk suatu kasus**", baik di panel maupun di API.
- **Fitur "Mask secrets"** menyembunyikan apa yang tampak seperti kata sandi, kode login, kunci API atau hash, token bot, string sesi, kunci pribadi, JWT, atau nomor kartu pembayaran (nomor kartu diperiksa dengan Luhn sum). **Fitur "Show"** menampilkan satu nilai; penampilan tersebut dicatat dalam jurnal. Menonaktifkan penyamaran untuk browser ini juga dicatat. Hanya tampilan yang berubah: catatan asli dan setiap ekspor tetap menyimpan teks lengkapnya.

## Jurnal

Setiap catatan yang telah ditandatangani oleh ruang kerja, ditampilkan mulai dari yang terbaru.

- **Ikhtisar** menghitung pesan yang diamati, pengeditan yang direkam, pemberitahuan penghapusan, dan sumber yang dipilih.
- **Garis waktu peristiwa** menyaring berdasarkan jenis peristiwa (semua, pengeditan, penghapusan, reaksi, keanggotaan, cakupan), berdasarkan teks, dan berdasarkan sumber. **Muat peristiwa sebelumnya** kembali ke halaman sebelumnya.
- Buka sebuah catatan untuk melihat detail, hash, dan muatannya. **Tautan ke catatan ini** adalah alamat yang membuka catatan yang sama. Informasi rahasia yang mungkin ada disamarkan dalam pratinjau ini; ekspor tetap mempertahankan versi aslinya.
- Jurnal ini bersifat hanya tambah: tidak ada yang di panel yang dapat mengedit atau menghapus catatan. Periksa dengan **Ekspor → Verifikasi jurnal** atau `python -m tgwitness.verify`; lihat [ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/).

## Sumber

Percakapan mana saja yang direkam oleh ruang kerja ini, dan apa saja yang disimpan darinya. Perubahan berlaku untuk aktivitas di masa mendatang; catatan yang telah disimpan tetap ada.

**Refresh daftar obrolan** membaca obrolan dan folder akun tersebut. Fitur ini tidak mengunduh pesan.

### Ruang Lingkup

- **Apa yang dicatat oleh akun ini** : **Obrolan yang dipilih** (hanya obrolan yang Anda tambahkan), **Folder Telegram** (salah satu folder akun, termasuk obrolan yang ditambahkan ke dalamnya kemudian) atau **Seluruh akun** (setiap obrolan, serta setiap obrolan baru, grup, obrolan pribadi, atau bot begitu muncul). **Mode penyelidikan** diperuntukkan bagi akun khusus: alat ini merekam segala sesuatu yang dilihat akun tersebut, pesan dan penekanan tombolnya sendiri, serta langsung menyimpan profil setiap obrolan baru beserta pesan-pesan yang sebelumnya terlihat. Gambar [panduan akun khusus](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) menjelaskan mengapa Anda tidak boleh menggunakan akun utama Anda.
- **Jenis sumber** membatasi mode folder dan seluruh akun hanya untuk saluran, grup, obrolan pribadi, dan bot. **Tindakan sendiri** menambahkan pesan, pengeditan, dan penekanan tombol balasan dari akun tersebut.
- **Saat obrolan atau bot baru muncul**: simpan profilnya dan hingga sejumlah pesan terbarunya yang terlihat.

Batasan: obrolan rahasia tidak pernah tercatat di TgWitness. Tidak ada yang direkam saat TgWitness tidak berjalan; setelah di-restart, alat ini hanya merekam apa yang masih dikembalikan oleh Telegram, dan laporan menunjukkan selisih tersebut. Obrolan yang melebihi batas daftar obrolan (1.000 percakapan kecuali diubah di Parameter) akan ditambahkan saat obrolan tersebut aktif kembali. Tombol bot yang ditekan di aplikasi lain tidak terlihat; balasan bot tetap direkam.

### Obrolan yang termasuk dalam cakupan

Saring berdasarkan status (**Diaktifkan**, **Dijeda**, **Prioritas**, **Dikecualikan**, **Akses Belum Dikonfirmasi**, **Diabaikan**) dan jenis, lalu lakukan tindakan pada pilihan: aktifkan, jeda, tandai atau hapus prioritas, kecualikan dari cakupan, atau hapus. Lencana status hanya menunjukkan keadaan; tindakan terdapat di menu setiap baris dengan penjelasan singkat tentang fungsinya. Menjeda dan mengecualikan memerlukan konfirmasi, termasuk untuk tindakan massal. Menghapus sumber akan meminta nama sumber tersebut dan menghapus profil orang-orangnya ; catatan yang disimpan tetap ada di jurnal.

Sumber yang tidak muncul dalam daftar obrolan akun sedang **menerima pembaruan, tidak ada dalam daftar obrolan**meskipun catatan terus masuk; jika tidak, **akses belum dikonfirmasi**. **Obrolan yang tersedia**menambahkan obrolan dengan **opsi “Tambahkan yang dipilih”** atau **“Tambahkan semua yang cocok**”.

### Riwayat lengkap

Memuat riwayat yang tersedia dari setiap sumber yang diaktifkan ke dalam Obrolan dan jurnal. Kemajuan tetap tersimpan setelah restart; lampiran mengikuti pengaturan media Anda. Lihat [riwayat sumber](https://phishdestroy.github.io/TgWitness/id/docs/reference/history/).

### Perekaman

- **Pilih perubahan mana yang ingin disimpan**: pesan baru, pengeditan, pemberitahuan penghapusan, reaksi yang terlihat, bergabung, dan keluar. Pengaturan awal mengubah formulir; **Simpan pengaturan rekaman** akan menerapkannya. Mengaktifkan kembali suatu kategori tidak akan memulihkan peristiwa yang terlewat.
- **Simpan media jika tersedia**: unduh lampiran hingga ukuran tertentu per file, atur per jenis dari 1 hingga 2.000 MiB, dan batasi durasi video dalam detik (0 berarti tidak ada batasan). Setiap upaya pengunduhan akan mencatat hasilnya.
- **Pemeriksaan ulang**: obrolan prioritas diperiksa setiap beberapa menit, obrolan lain jarang, sehingga akun tetap terhindar dari batas FloodWait Telegram. Nilai 0 menonaktifkan grup. Tandai obrolan prioritas dengan bintang di daftar; jumlah obrolan per putaran dan jeda antar obrolan terdapat di Parameter. Lihat [koleksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/).

## Ekspor

**Bagian Unduhan** menyiapkan berkas; **Laporan Pembuatan** menentukan tampilan laporan.

| Apa | Gunakan untuk | Panduan |
| --- | --- | --- |
| Ekspor akun | Cuplikan terbaru mengenai apa yang dapat dibaca oleh akun tersebut saat ini | [Ekspor akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/account-export/) |
| Berbagi salinan | Versi ringkas dari ekspor akun yang sudah selesai | [Pengungkapan](https://phishdestroy.github.io/TgWitness/id/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Tertanda ZIP | Jurnal, laporan, lampiran, dan alat verifikasi dalam batas jurnal yang tetap | [Ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/) |
| Laporan dalam format HTML, PDF, dan JSON | Laporan yang dapat dibaca dan disegel | [Laporan kasus](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/) |
| JSONL, CSV | Catatan asli yang telah ditandatangani; lembar kerja yang aman untuk rumus | [Ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/) |
| Cuplikan serah terima | Hanya obrolan, periode, dan orang-orang yang dibutuhkan oleh penerima | [Bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#investigation-handoff) |
| Ekspor obrolan | Satu obrolan yang telah ditandatangani `chat.json` dan `chat.html` | [Ekspor satu obrolan](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Mengenkripsi unduhan di atas dengan kata sandi** (12 karakter atau lebih) akan menyimpan berkas AES-256 ZIP yang dapat dibuka dengan 7-Zip atau WinRAR. Berkas yang ditandatangani di dalamnya tetap tidak berubah. Kata sandi tidak disimpan.
- **Ekspor yang telah disiapkan** menyimpan hingga 20 berkas dalam batas 2 GiB, ditambah berkas terbaru, untuk pengunduhan berulang, masing-masing dilengkapi dengan SHA-256. Menyiapkan berkas tidak menjamin pengiriman.
- Jika browser menolak dialog penyimpanan, panel akan beralih ke unduhan biasa.
- **Identitas penandatanganan Anda** menampilkan sidik jari kunci. **Simpan titik pemeriksaan** dan Unduh **tanda terima eksekusi yang ditandatangani** memberi Anda catatan untuk disimpan di luar pengumpul. Siapkan **permintaan cap waktu** membuat permintaan RFC 3161 tanpa menghubungi layanan apa pun.

## Pengaturan, akun, dan koneksi

- **Pengaturan**: tujuan, koneksi, apa yang akan direkam, dan antarmuka. Lihat [pengaturan awal dan pengaturan](https://phishdestroy.github.io/TgWitness/id/docs/reference/settings/).
- **Akun**: setiap ruang kerja beserta status, sumber, peristiwa, dan antrian lampirannya. Saring berdasarkan **Perlu Perhatian**, **Sedang Dikumpulkan**, **Offline atau Ditangguhkan**, atau **Tidak Terhubung**; tunda atau lanjutkan pilihan; impor berkas akun secara massal dan kelola grup. Lihat [akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/).
- **Akun**: masuk dan rute koneksi akun ini. Langsung, profil WireGuard, proksi Anda sendiri, kumpulan MTProto publik, atau WARP; siapkan dan periksa rute, lalu terapkan ke akun ini, sebuah grup, atau semua akun. Lihat [koneksi dan proksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) serta [proksi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md).

## Fitur Tambahan

Opsional: akun dan sumber saja sudah cukup untuk mulai mengumpulkan data. Hanya opsi yang Anda pilih yang akan membuka pengaturannya, dan tidak ada yang terhubung secara otomatis. Kartu **“Tingkat Perlindungan”** di bagian atas menunjukkan [mode perlindungan](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#protection-modes).

| Kartu | Fitur tambahan | Panduan |
| --- | --- | --- |
| Penyimpanan & ruang disk | Pencadangan, memindahkan file lama ke cloud Anda, serta salinan bukti yang tidak dapat dihapus | [Penyimpanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/) |
| Tujuan & tingkat perlindungan | Pengaturan yang disarankan untuk tujuan Anda dan dua skala | [di bawah ini](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#goal-and-protection-level) |
| Pemberitahuan | Masalah, pesan yang diubah, dan ringkasan harian; bot kontrol milik Anda sendiri | [di bawah ini](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#notifications) |
| Bukti & cadangan | Cap waktu, saksi tambahan, dan salinan terenkripsi di luar lokasi | [di bawah ini](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#evidence-and-backups) |
| Server beroperasi 24/7 | Server cloud tanpa SSH, yang dibuat dan dihapus melalui panel | [Jaminan tinggi](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#from-the-panel) |
| Saksi independen | Pemeriksaan yang telah ditandatangani diposting ke saluran Telegram atau Discord Anda | [Witness](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/) |
| Pemeriksaan kode | Membandingkan program yang sedang berjalan dengan commit GitHub publik | [di bawah ini](https://phishdestroy.github.io/TgWitness/id/docs/reference/panel/#code-check) |

### Tujuan dan tingkat perlindungan

Empat pertanyaan:

1. **Untuk apa ini? Sebagai** catatan pribadi, penyelidikan, atau bukti untuk suatu kasus.
2. **Seberapa banyak yang akan Anda pantau?** Beberapa obrolan (hingga sekitar 50), banyak obrolan (hingga sekitar 500), atau seluruh akun. Ini menetapkan batas daftar obrolan menjadi 1.000, 3.000, atau 20.000.
3. **Foto dan berkas?** Hanya teks, foto dan media pendek (foto 20 MB, video 100 MB), atau semuanya (video dan dokumen masing-masing hingga 1 GB). Opsi “semuanya” dengan akun lengkap juga menyisakan ruang disk kosong sebesar 4 GiB.
4. **Di mana alat ini akan dijalankan?** Di komputer ini, atau di server yang selalu aktif.

Saran tersebut mencantumkan cap waktu independen, drand, dan daftar perangkat Telegram, masing-masing dilengkapi dengan penjelasan singkat mengenai fungsinya. Cap waktu dimulai setiap 60, 30, atau 10 menit untuk catatan pribadi, penyelidikan, atau bukti; drand dan daftar perangkat memerlukan cap waktu. **Terapkan** perubahan hanya pada hal-hal ini, kebijakan lampiran, dan dua parameter di atas. Setiap perubahan merupakan catatan jurnal, ditambah `setup.applied`. Pemberitahuan, salinan di luar situs, server, Gateway DNS, pemeriksaan kode, dan saksi ditawarkan sebagai langkah selanjutnya dengan formulir masing-masing.

Dua skala dihitung berdasarkan pengaturan yang ada, bukan berdasarkan tujuan:

| Skala | Poin |
| --- | --- |
| Kredibilitas | Jurnal yang ditandatangani 1, cap waktu 3, drand 1, daftar perangkat 1, pemeriksaan kode yang cocok 1, polling saksi 1, server yang disertifikasi 2, log DNS Gateway 1 |
| Keandalan | Server yang selalu aktif 3, salinan di luar lokasi 3, Object Lock 1, pemberitahuan masalah 1 |

80% atau lebih dianggap **maksimal**, 50% **tinggi**, 25% **sedang**, di bawah itu **dianggap dasar**. Keandalan saat ini dihitung berdasarkan server yang selalu aktif sesuai jawaban pertanyaan 4, sebelum server mana pun diperiksa.

### Pemberitahuan

Pemberitahuan dikirim melalui Apprise ke Telegram, Discord, Slack, ntfy, email, Matrix, dan lebih dari 100 layanan lainnya. Pilih layanan, isi satu atau dua kolom, lalu kirim uji coba, atau tempelkan alamat Apprise secara langsung.

- **Masalah**: disk hampir penuh, akun terlogout, kesalahan koleksi, penyalinan, atau cap waktu . Pada server yang disegel, port SSH yang terbuka atau proses login juga menjadi masalah.
- **Perubahan**: pesan yang dihapus, diedit, dan hilang dalam obrolan yang dipantau, dikelompokkan menjadi satu pemberitahuan per pemeriksaan (setiap menit kecuali diubah di Parameter).
- **Tugas yang telah diselesaikan**: riwayat, ekspor, dan salinan penyimpanan.
- **Ringkasan harian** pada jam yang dipilih, sesuai waktu server.

Pemberitahuan menampilkan nama obrolan dan jumlah pesan. Kutipan pesan dinonaktifkan secara default; jika diaktifkan, teks pesan akan dikirimkan ke luar perangkat ini.

**Bot operator Anda** adalah bot milik Anda sendiri yang dibuat melalui @BotFather yang menjawab `/status` dan `/stats`, serta secara opsional `/pause`, `/resume` dan `/copy`. Hanya obrolan dan ID pengguna Telegram yang tercantum yang dapat menggunakannya; teks percakapan tetap berada di ruang kerja. Gunakan bot terpisah jika aplikasi lain sudah menerima perintahnya. Lihat [notifikasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) dan [bot operator](https://phishdestroy.github.io/TgWitness/id/docs/reference/storage/#operator-bot-and-completion-notices).

### Bukti dan cadangan

- **Stempel waktu independen** hanya mengirimkan SHA-256 dari setiap titik pemeriksaan yang ditandatangani ke otoritas RFC 3161 dan kalender OpenTimestamps, setiap 5 hingga 1.440 menit. **Anchor kini** menjalankan satu siklus. Lihat [stempel waktu](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/).
- **Saksi-saksi lainnya**, masing-masing dinonaktifkan hingga dipilih: putaran drand terbaru, daftar perangkat yang masuk ke Telegram tanpa alamat IP, dan log Cloudflare Gateway mengenai kueri DNS server. Lihat [catatan opsional](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **Pencadangan terenkripsi** menyalin jurnal, file, titik pemeriksaan, dan ekspor obrolan ke penyimpanan yang kompatibel dengan S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Semua data dienkripsi terlebih dahulu di mesin ini. **Unduh kunci enkripsi** dan simpanlah terpisah: tanpa kunci tersebut, salinan tersebut tidak dapat dibaca. Object Lock dalam mode Governance atau Compliance mencegah objek dihapus selama jumlah hari yang ditentukan. Lihat [salinan di luar lokasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Pemeriksaan kode

Memeriksa apakah program yang terinstal sesuai dengan versi yang telah diterbitkan.

1. Masukkan repositori GitHub (yang resmi sudah terisi) serta tag, cabang, atau commit.
2. **Fitur "Check now"** meminta daftar berkas dari commit tersebut melalui API GitHub, melalui rute ruang kerja ini untuk permintaan eksternal. Fitur ini membandingkan ID blob Git dari setiap berkas program yang diukur dengan commit tersebut. Hasil checkout di Windows dengan akhir baris yang telah dikonversi tetap cocok.
3. Hasilnya mencantumkan file yang berubah, tambahan, dan yang hilang (masing-masing hingga 50) dan disimpan sebagai catatan `source.checked` catatan jurnal.

Hasil ini hanya dianggap terkini selama berkas program yang sedang berjalan tidak diubah: periksa kembali setelah pembaruan. Tidak diperlukan token dan hanya repositori publik yang berfungsi; obrolan dan kredensial tidak diunggah. Pencocokan mengidentifikasi kode di disk. Ini bukan pengesahan perangkat keras; untuk itu, lihat [Phala Cloud](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Mode perlindungan

Tombol pengalih di sebelah nomor versi menunjukkan mode yang dipilih dan berapa banyak dari 18 lapisan perlindungan yang aktif, misalnya `🟠 Witnessed 9/18`. Untuk **mengubah mode**, pilih **"Extras" → "Tingkat Perlindungan"** untuk membuka menu pilihan. Setiap mode menggambarkan target tertentu dan mencantumkan apa saja yang masih belum tercakup; proses perekaman, penandatanganan, dan pengaturan yang disimpan tetap sama di setiap mode.

| Mode | Untuk | Menambahkan |
| --- | --- | --- |
| 🟢 Mudah | Memantau obrolan dan menyimpan salinannya | Obrolan, jurnal, dan ekspor obrolan; proses penandatanganan berjalan di latar belakang |
| 🟡 Ditandatangani | Melaporkan ke platform, host, atau bagian penanganan pelanggaran | Arsip yang ditandatangani, pemeriksaan jurnal, titik pemeriksaan, ekstrak serah terima |
| 🟠 Disaksikan | Kasus-kasus di mana seseorang mungkin mengklaim bahwa catatan tersebut telah diubah | Saksi independen yang memposting entri jurnal yang telah ditandatangani |
| 🔴 Siap untuk persidangan | Bukti untuk pengacara, kepolisian, atau pengadilan | Cap waktu, salinan terenkripsi di luar lokasi, serta rincian kasus dalam laporan |
| 🟣 Terverifikasi oleh GitHub | Catatan yang perangkat lunaknya harus dapat diperiksa oleh siapa pun | Pemeriksaan kode dan pencatatan GitHub Actions |
| ⚫ Mossad | Kasus-kasus berisiko tinggi melawan lawan yang memiliki dana besar | Server yang aman 24/7, alamat IP tersembunyi, serta seluruh 18 lapisan |

Lapisan-lapisan: setiap catatan ditandatangani dan dirantai; tanda terima eksekusi yang ditandatangani; lampiran disimpan dengan SHA-256; titik pemeriksaan yang ditandatangani; pemeriksaan ulang; peringatan masalah; akses saksi hanya-baca; saksi yang memeriksa sesuai jadwal; cap waktu RFC 3161; bukti OpenTimestamps; cap waktu terbaru yang terverifikasi; salinan terenkripsi di luar lokasi; detail kasus dalam laporan; pemeriksaan kode kesesuaian; Telegram tidak pernah melihat IP mesin ini; permintaan dari luar melalui proxy; Object Lock pada salinan; server yang disegel dengan catatan penyedia. Lapisan yang dinonaktifkan memiliki opsi **"Set up**", yang membuka formulirnya. Memilih mode yang lebih rendah akan meminta konfirmasi dan tidak menghapus apa pun.

## Alat lainnya

- **Tanyakan ke arsip**: cari pengamatan yang tersimpan, tinjau sumbernya, lalu putuskan apakah akan mengirimkannya ke model AI. Lihat [analisis arsip](https://phishdestroy.github.io/TgWitness/id/docs/reference/analysis/) serta [OCR dan transkripsi lokal](https://phishdestroy.github.io/TgWitness/id/docs/reference/media-analysis/).
- **Parameter**: batasan dan kecepatan pengumpulan data, pemeriksaan ulang, unduhan, profil, pemberitahuan, dan ekspor. Cari berdasarkan nama, tampilkan nilai **Hanya yang berubah**, dan siapkan pengaturan default sebagai draf dengan **Pulihkan default…**. **Simpan parameter** menerapkan nilai-nilai tersebut mulai dari penggunaan berikutnya, dan setiap perubahan dicatat dalam jurnal.
- **Akses**: token terpisah untuk peninjau, analis, dan operator, yang dibatasi pada ruang kerja, obrolan, dan hak akses tertentu. Lihat [bagian akses](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/).
- **Log sistem** : apa yang telah dilakukan proses ini sejak dimulai (koneksi, perubahan proxy, proses masuk, penolakan, perubahan pengaturan) dengan alamat IP disembunyikan. Fitur **“Ikuti Baris Baru”** menjaga baris terbaru tetap terlihat. Pesan hanya disimpan di jurnal.
- **Integrasi**: penyedia AI, koneksi [MCP yang hanya dapat dibaca,](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/) dan [webhook yang ditandatangani](https://phishdestroy.github.io/TgWitness/id/docs/reference/webhooks/).
- **Case Board**: catatan tim pribadi, bookmark, dan potongan di samping bukti. Lihat [Case Board](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-board/).
- **GitHub Actions menangkap data** dalam Ekspor: satu obrolan yang ditangkap dari fork Anda. Lihat [penangkapan yang disegel](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
