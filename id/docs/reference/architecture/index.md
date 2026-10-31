# Arsitektur

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/architecture/

Komponen-komponen kolektor, panel, jurnal, pekerja, dan saksi, serta bagaimana data berpindah di antara komponen-komponen tersebut.

Satu proses Python menjalankan panel FastAPI dan sejumlah ruang kerja yang terisolasi, masing-masing dilengkapi dengan klien akun pengguna Telethon. SQLite menyimpan jurnal peristiwa yang ditandatangani dan hanya dapat ditambahkan, serta pengaturan operasional yang dapat diubah. Sebuah brankas terenkripsi menyimpan kredensial API, StringSession, dan kunci penandatanganan. Frontend berupa paket HTML/CSS/JavaScript biasa: tidak diperlukan proses kompilasi Node, CDN, atau pengunduhan frontend saat runtime.

| Modul | Tanggung Jawab |
| --- | --- |
| collector.py | Otorisasi, pemilihan dialog, pembaruan, tangkapan layar, antrian media, pemantauan koneksi |
| interactions.py / telegram_client.py | Tindakan panel yang eksplisit, tanda terima yang ditandatangani, ID permintaan yang tetap, serta kebijakan percobaan ulang panggilan balik/bergabung yang disesuaikan dengan tugas |
| message_content.py | Perbandingan pesan yang dapat diamati, tidak termasuk metadata akses transportasi |
| workers.py | Tunggu hingga proses ekspor file selesai sebelum melakukan pembersihan setelah pembatalan |
| store.py | Transaksi WAL, rantai peristiwa terurut, filter kueri, pengaturan operasional |
| security.py | Pembuatan berkas pribadi, brankas terenkripsi, penandatanganan Ed25519, penguncian proses tunggal |
| evidence.py | Ekspor jurnal lengkap, turunan, titik pemeriksaan, verifikasi lampiran |
| verify.py | Verifikator mandiri dan hanya baca (perpustakaan standar + kriptografi): arsip, cakupan, jurnal saksi, dan posting saluran, serta berkas profil |
| app.py | API terotentikasi, siklus hidup, validasi permintaan, panel statis |
| profiles.py | Pengumpul akun ganda, pengontrol akses bersama, siklus hidup per ruang kerja |
| access.py | Hibah yang dibatasi cakupannya, pemeriksaan izin, pembatasan IP, batas sesi, dan konsol administrator |
| proxy_catalog.py | Cuplikan umpan publik, pemeriksaan transportasi, kumpulan proxy bersama, dan pemilihan berdasarkan kondisi kesehatan |
| provenance.py | Pengukuran identitas, kode, dan ketergantungan yang ditandatangani selama proses akuisisi |
| network.py | Rute yang telah divalidasi per ruang kerja; status dan bukti yang disunting; opsi pengiriman Telethon |
| sessions.py | Konversi skema SQLite Telethon yang telah ditinjau menjadi format offline yang hanya dapat dibaca |
| account_import.py | Deteksi dan normalisasi dalam memori terhadap berkas akun yang didukung dan JSON |
| tdata.py | Pembaca ZIP TData modern yang terbatas, validasi checksum/dekripsi, tanpa ekstraksi |
| doctor.py | Pemeriksaan kesiapan lokal tanpa pengumpulan data, login, atau instalasi paket |
| download.py | Unduhan ekspor streaming terotentikasi dengan pembatasan pembacaan dan tanpa penimpaan |
| monitoring.py | Kebijakan peristiwa yang divalidasi per ruang kerja dan aturan lampiran per jenis, dibagikan oleh pengelola, status, dan tanda terima yang ditandatangani |
| scope.py | Cakupan pemantauan (obrolan yang dipilih, folder Telegram, seluruh akun), jenis sumber, pengecualian, tingkatan pemeriksaan ulang |
| dossier.py | Profil pengguna per obrolan yang dibuat berdasarkan catatan yang disimpan: fakta dengan referensi catatan, SHA-256/pHash avatar, serta ekstraksi sebutan |
| witness_api.py | Token saksi yang hanya dapat dibaca dan bagian awal jurnal yang telah ditandatangani yang dapat mereka ambil |
| witness.py | Proses saksi independen: kunci dan jurnal milik sendiri, pemeriksaan kepala, posting saluran yang ditandatangani, ekspor |
| alerts.py | Pemberitahuan Apprise dan daftar pemberitahuan panel |
| logging_config.py | Pencatatan konsol dan diagnostik server bergilir untuk peluncuran tanpa jendela |
| static/ | Antarmuka responsif, gerbang akses lokal, filter, detail, ekspor, pengaturan akun |
| demo.py | Jurnal sintetis yang diberi label dengan jelas, terpisah dari data asli yang dikumpulkan |

Penanganan pengamatan didaftarkan sebelum terhubung. Pengumpulan data secara langsung dibatasi oleh identitas klien yang aktif, status berjalan yang eksplisit, sumber yang diaktifkan, atau cakupan pengamatan (mode folder atau seluruh akun menambahkan obrolan baru sebagai sumber pada pembaruan pertamanya), serta kebijakan peristiwa. Klien yang ditolak dan digantikan tidak dapat berkontribusi pada pembaruan langsung. Reaksi mentah dan pembaruan keanggotaan mempertahankan batasan visibilitas. Isi pesan masuk dan tugas media tahan lama-nya disimpan bersama-sama. Tugas-tugas tersebut mempertahankan deskriptor TL asli dan mengikat hash-nya ke pengamatan pesan yang ditandatangani. Semantik pengirim/editor/penghapus dipisahkan.

Setiap ruang kerja hanya menerima satu akun dan memiliki direktori serta identitas penandatanganan tersendiri. Ruang kerja utama tetap berada di direktori akar demi kompatibilitas; ruang kerja tambahan berada di profiles/<id>/. Satu token bearer mengendalikan seluruh instalasi; ruang kerja bukanlah entitas otorisasi yang terpisah. Kunci proses melindungi direktori; kunci basis data menserialisasikan penyisipan peristiwa. Setiap penambahan disimpan secara sinkron ke WAL SQLite dengan mode sinkron PENUH. Pemicu pembaruan/penghapusan peristiwa mencegah pengeditan aplikasi biasa; administrator sistem berkas tetap berada di dalam batas kepercayaan.

Otorisasi API menggunakan token bearer. Operasi login diserialisasikan dan dibatasi waktu. Unggahan akun menggunakan batas khusus 12 MiB untuk badan terenkripsi dan batas 8 MiB untuk file terdekodasi; permintaan API biasa tetap menggunakan batas 16 KiB. Konversi berjalan di benang pekerja (worker thread), menyimpan unggahan di memori, dan mengembalikan input yang dinormalisasi ke browser yang terotentikasi. Masuk melalui QR memiliki kandidat per ruang kerja, pengenal berumur pendek, tugas penunggu, dan pembatalan eksplisit. Hanya otorisasi yang diterima yang menjadi klien aktif. Telegram FloodWait dikembalikan dengan nilai Retry-After; kredensial dan pesan kesalahan RPC mentah tidak ditampilkan dalam kesalahan API. Ekspor berjalan di luar loop peristiwa asinkron dan diserialisasikan per ruang kerja. Ekspor ini mengalirkan snapshot baca yang stabil, dan dapat berjalan bersamaan dengan penulisan WAL yang sedang berlangsung. Pengumpul ruang kerja berbagi proses/loop peristiwa.

Cuplikan riwayat terkini dan pembaruan langsung dapat tumpang tindih. Keduanya merupakan pengamatan terpisah, yang diberi label berdasarkan sumber; duplikat tidak disembunyikan secara otomatis. Tidak ada inferensi yang dilakukan berdasarkan ID yang hilang, teks terhapus yang dipalsukan, penghitungan anggota yang dipaksakan, atau bergabungnya ke grup secara otomatis yang diterapkan.

Untuk penjelasan yang ditujukan kepada operator, lihat [cara kerja pengumpulan data](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/) serta [format akun dan sesi](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/).

Konfigurasi jaringan disimpan di dalam brankas terenkripsi. Menerapkan rute akan menutup klien lama dan membatalkan proses login yang belum selesai; koneksi selanjutnya menggunakan rute tersebut tanpa fallback langsung. Instalasi kunci eksternal baru menghasilkan kunci Fernet setiap ruang kerja dengan HKDF-SHA256 dari berkas kunci utama dan garam acak yang tersimpan. Hal ini melindungi rahasia secara terpisah dari direktori data, bukan isi jurnal/media dalam teks biasa.

Entri demo lokal menggunakan kemampuan proses yang dihasilkan secara terpisah, bukan token panel yang dikonfigurasi. Penerbitan dan penerimaan memerlukan mode demo eksplisit, root sintetis tanpa ruang kerja tambahan atau sesi yang diotorisasi, peer/Host loopback, tanpa header penerusan proxy, dan tanpa permintaan browser lintas asal. API langsung mempertahankan otentikasi pembawa dan menolak perubahan pengumpulan data dalam mode demo.
