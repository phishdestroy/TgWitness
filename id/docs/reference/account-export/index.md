# Ekspor akun

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/account-export/

Ekspor apa yang dapat dibaca oleh suatu akun saat ini: cakupan, tugas yang dapat dilanjutkan, arsip yang telah ditandatangani, dan salinan berbagi yang telah diminimalkan.

Ekspor akun mencadangkan akun itu secara eksklusif. Jeda pemantauan atau pengambilan data lain secara eksplisit sebelum memulai atau melanjutkan; aplikasi tidak pernah menghentikannya otomatis.

Sebagai administrator instalasi, pilih **Mulai di sini → Ekspor akun saya**, atau **Ekspor → Akun Telegram → Konfigurasi ekspor akun**. Masuk jika diperlukan, tinjau cakupan, dan mulai ekspor secara eksplisit. Pengamatan berkelanjutan tidak diperlukan. **"Pengamatan yang disimpan**" adalah ekspor terpisah dari jurnal yang ada; ZIP-nya mencakup semua sumber terlepas dari filter jurnal. Setiap ruang kerja memiliki tugas, identitas penandatanganan, dan penyimpanan sendiri. Akses panel yang diberikan, termasuk izin ekspor biasa tanpa batasan, tidak dapat membuka rute-rute yang berlaku untuk seluruh akun ini.

Filter pengirim dan teks dapat diperluas di bawah **"Filter berdasarkan pengirim atau teks pesan**". Bagian "**Data akun & metode koneksi"** berisi kategori akun opsional dan pilihan "Takeout" atau "sesi reguler"; ringkasannya menampilkan pilihan yang aktif meskipun panel tersebut ditutup. Menutup bagian-bagian ini akan mempertahankan pengaturannya. Draf ekspor dan laporan tetap ada di sesi panel saat ini saat berpindah tampilan; draf tersebut tidak disimpan saat browser dimuat ulang. Pekerjaan yang sudah ada tetap dapat diakses dari kedua pilihan ekspor tersebut.

Alur kerja ini mengekspor data yang saat ini dapat diakses oleh akun yang terhubung. Pengaturan default menggunakan [Telegram Takeout](https://core.telegram.org/api/takeout); ini bukanlah cadangan data Telegram yang tidak tersedia atau telah dihapus. Obrolan Rahasia, riwayat yang tidak dapat diakses, dan suntingan sebelumnya tidak dapat dipulihkan. Telegram dapat memberlakukan masa tunggu sebelum Takeout dimulai. Panel menampilkan masa tunggu tersebut; panel tidak secara diam-diam mengganti metode pengiriman data. Opsi API reguler eksplisit memiliki cakupan yang berbeda dan merekam kategori yang tidak didukung.

## Pilih apa yang akan dikumpulkan

| Pengaturan | Arti |
| --- | --- |
| Tujuan | Catat alasan mengapa akuisisi ini diperlukan. Jangan cantumkan nama yang tidak perlu atau detail kasus yang sensitif di sini. |
| Bahasa laporan | Pilih bahasa untuk label pada laporan yang dapat dibaca. Teks pesan asli tetap tidak berubah; label templat yang belum diterjemahkan menggunakan bahasa Inggris. Bahasa tersebut ditetapkan melalui opsi pekerjaan yang telah ditandatangani. |
| Jenis obrolan / ID obrolan | Semua jenis yang dipilih, atau hanya obrolan yang tercantum; Pesan yang Disimpan termasuk dalam obrolan pribadi. Obrolan yang diarsipkan dapat dipilih secara terpisah. |
| Tanggal | UTC. Tanggal kalender "Dari" dan "Sampai" pada panel tersebut keduanya disertakan. API ini menggunakan rentang waktu inklusif `from_utc` dan eksklusif `to_utc`; panel ini mengirimkan awal hari setelah tanggal "Through". Batas yang kosong berarti sisi tersebut tidak dibatasi. |
| ID Pengirim | Hanya pesan dari pengirim yang tercantum; daftar kosong mencakup semua pengirim. |
| Teks berisi | Frasa literal yang tidak membedakan huruf besar-kecil, dicocokkan dengan operator OR. Kondisi pengirim/tanggal/pesan sendiri digabungkan dengan operator AND. |
| Pesan sendiri | Simpan hanya pesan yang dikirim. |
| Jenis media | Pilih kategori lampiran, atau hapus semuanya untuk menghindari pengunduhan berkas pesan. |
| Batas file / total media | Ukuran per file dalam MiB dan total media yang diunduh dalam GiB. Teks, tanda terima, laporan yang dapat dibaca, dan overhead ZIP memerlukan ruang disk tambahan. |
| Kategori akun | Profil, kontak, foto profil, cerita, metadata sesi, dan data Takeout lainnya memiliki pengaturan terpisah. |

Preset **koleksi "Minimize**" menonaktifkan file dan metadata akun. Filter pengirim/konten diterapkan sebelum halaman pesan yang disimpan dan unduhan media. Telegram tetap mengirimkan halaman riwayat API yang berisi pesan yang diperlukan untuk mengevaluasi filter tersebut: penyaringan bukanlah jaminan bahwa pesan yang tidak dipilih tidak akan pernah masuk ke memori proses. Pengamatan lain yang sedang berlangsung di ruang kerja memiliki cakupan dan pengaturan penyimpanan tersendiri.

Riwayat foto profil dan cerita tidak dipilih secara default. Nonaktifkan juga profil dan kontak jika kasus tersebut hanya memerlukan pesan. Jika lampiran atau metadata tidak diperlukan, mengesampingkannya selama proses pengambilan data akan mencegah penyimpanan salinan pribadi tambahan dalam ekspor ini.

## Ringkasan, cakupan, dan verifikasi

Setiap tugas membekukan opsi dan identitas akunnya. Inventaris dan halaman yang ditangkap ditandatangani; catatan tanda terima halaman mencatat hash, kursor, waktu, hasil lampiran, dan tanda terima sebelumnya. Hanya halaman yang telah dikonfirmasi yang meningkatkan kemajuan. Fitur restart/resume memeriksa catatan-catatan tersebut sebelum melanjutkan. Akun yang diubah, halaman yang ditandatangani yang diubah, atau rantai tanda terima yang tidak konsisten akan ditolak. Opsi tidak dapat diedit di tengah proses akuisisi: mulailah tugas lain untuk cakupan yang berbeda.

Tombol "Pause" menghentikan operasi akun yang sedang berjalan. Memulai ulang aplikasi akan membuat pekerjaan yang belum selesai tetap tersedia untuk dilanjutkan secara eksplisit. Sesi Takeout yang telah kedaluwarsa memerlukan dilanjutkan secara eksplisit; mengubah rentang pemotongan Telegram mungkin memerlukan akuisisi baru. Fitur "Resume" mempertahankan pengamatan sebelumnya, sehingga ekspor yang berjalan lama bukanlah satu snapshot atomik. Operasi perubahan akun lainnya dan ekspor yang bertentangan diblokir selama proses akuisisi. Tunggu hingga pengemasan selesai sebelum menghapus ruang kerja.

Fitur "Resume" memverifikasi konten yang telah direkam sebelum melanjutkan. Arsip besar pada penyimpanan lambat dapat melebihi batas waktu yang dikonfigurasi **Parameter → Batas waktu tindakan panel** (120 detik secara default). Tingkatkan pengaturan tersebut sebelum mencoba lagi; pembatalan atau gangguan penyimpanan akan meninggalkan tugas yang ditangguhkan, sedangkan kegagalan pemeriksaan integritas akan meninggalkan tugas yang gagal beserta penjelasannya. Verifikasi harus selesai atau dihentikan dengan aman sebelum berkas-berkasnya dapat ditutup. Belum ada klaim mengenai throughput akun besar yang telah diverifikasi oleh pemeriksaan sintetis.

Panel ini membedakan cakupan yang telah dipilih dan selesai dari arsip parsial, serta mencatat kelalaian dan pembacaan yang gagal. File yang sengaja dikecualikan berbeda dari file yang gagal atau tidak tersedia. Periksa cakupan bahkan ketika verifikasi integritas berhasil. Tidak ada pembaca lokal yang dapat membuktikan bahwa Telegram telah mengembalikan setiap pesan yang pernah ada.

ZIP yang telah selesai tetap tersedia untuk diunduh berulang kali dan melalui HTTP-range. Arsip akun berisi `manifest.json`, `manifest.sig`, yang telah ditandatangani `job.json`, `inventory.json`, `receipts/`, dan resmi `data/*.jsonl`, dipilih `media/`, HTML yang dapat dibaca, dan verifikator. Sematkan sidik jari pengumpul melalui saluran independen, lalu verifikasi menggunakan instalasi tepercaya:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Untuk arsip yang isi terperluasnya melebihi 4 GiB, tetapkan ukuran yang memadai secara eksplisit `--max-gib`. Panel ini memverifikasi arsip lokalnya yang telah diautentikasi dan selesai menggunakan ukuran yang dinyatakan setelah diekspansi serta ringkasan (ZIP) yang dipublikasikan; CLI eksternal mempertahankan batas ukurannya sendiri. Lakukan verifikasi sebelum membuka HTML yang dapat dibaca. Verifikator bawaan arsip memang praktis, tetapi verifikator yang diperoleh secara independen menghindari ketergantungan pada kode yang dapat dieksekusi yang disertakan bersama bukti tersebut.

Tanda tangan Ed25519 dan hash SHA-256 mendeteksi perubahan setelah pengumpul menyimpan byte yang relevan. Hal ini **tidak** membuktikan bahwa Telegram menandatangani pesan-pesan tersebut, bahwa operator pengumpul jujur, bahwa riwayat akun lengkap, atau bahwa pengadilan akan menerima materi tersebut. Waktu penangkapan menggunakan jam pengumpul. Cap waktu independen dan asal-usul akuisisi independen harus dievaluasi secara terpisah.

## Siapkan pengungkapan informasi untuk pengacara atau penerima lainnya

Setelah mengunduh ekspor yang sudah selesai, simpan gambar asli ZIP dan buka `index.html` dari salinan yang telah diekstrak. Laporan ini menjelaskan cakupan, jangkauan yang tersedia, dan batasannya. Referensi catatannya menggabungkan referensi arsip, jalur dokumen, dan nomor catatan, sehingga penerima dapat menemukan entri yang sama dalam HTML atau hasil cetakan. Untuk contoh yang sudah diterapkan, lihat [buka laporan fiktif](https://phishdestroy.github.io/TgWitness/demo/report/).

Dari ekspor akun yang sudah selesai, pilih **"Siapkan salinan untuk dibagikan**". Ini akan membuat turunan terpisah yang telah ditandatangani. Sumber ZIP tetap tidak berubah dan bersifat pribadi; jangan mengirimkannya bersama dengan turunan yang telah dipersingkat kecuali penerima berwenang untuk menerima seluruh isinya. Pilih bahasa laporannya secara terpisah. Mengubah bahasa atau pengaturan pilihan apa pun memerlukan pratinjau lain sebelum pembuatan.

1. Masukkan tujuan pengungkapan dan pilih tanggal, ID pengirim, serta kriteria teks literal.
2. Pilih apakah akan mempertahankan identitas asli, hanya menampilkan peserta yang terdaftar, atau menyamarkan identitas semua orang. Dalam mode penyamaran apa pun, ID/judul obrolan dan ID pesan juga diganti. Nama samaran tetap konsisten di dalam satu pengungkapan dan berubah antar pengungkapan yang disiapkan secara terpisah.
3. Simpan teks pesan, hilangkan seluruhnya, atau tambahkan nama/frasa literal untuk disamarkan. Dalam mode pribadi, alat ini juga menyamarkan nama pengirim tersembunyi yang diketahui dan nama pengguna alternatif, ID pengirim token lengkap, nama obrolan langsung, tautan, alamat email, dan string yang menyerupai nomor telepon. Pencocokan nama yang diketahui menangani konversi huruf besar-kecil Unicode, termasuk `Straße`/`STRASSE`. Judul grup/saluran umum tidak secara otomatis dihapus dari teks pesan. Jika batas penyamaran identitas yang diketahui terlampaui, persempit ekspor sumber atau hilangkan teks; alat ini menolak untuk secara diam-diam melewati nama-nama berikutnya. Ini adalah aturan yang dilakukan semaksimal mungkin, bukan anonimisasi umum.
4. Jangan sertakan berkas kecuali jika penerima membutuhkannya. Berkas asli yang disertakan tetap mempertahankan piksel, audio, teks, dan metadatanya. Berkas-berkas tersebut **tidak** dianonimkan oleh alat ini.
5. Lihat pratinjau jumlah, peringatan, dan contoh pesan yang telah diubah, lalu konfirmasikan pembuatan secara eksplisit. Contoh dibatasi hingga 12 pesan dan masing-masing 2.000 karakter teks. Ini hanyalah contoh, bukan tinjauan lengkap atas hasilnya. Mengubah pengaturan memerlukan pratinjau baru. Pratinjau kedaluwarsa setelah 15 menit dan terikat pada sesi administrator tersebut serta ZIP asli yang tepat; pratinjau tidak dapat digunakan kembali setelah dibuat. Pratinjau baru akan membatalkan pratinjau sebelumnya untuk pekerjaan dan sesi yang sama.
6. Periksa hasil lengkapnya `index.html` dan `messages.jsonl` secara lokal sebelum menyerahkannya. Jika ternyata terdapat informasi yang tidak perlu, buat pengungkapan baru dengan pengecualian yang lebih ketat. Jangan mengedit ZIP yang telah ditandatangani di tempat.

Format yang dipersingkat ini mengabaikan profil akun terstruktur, kontak, avatar, sesi, cerita, objek Telegram mentah, header penerusan, kutipan balasan, kartu kontak, dan metadata lokasi. Format ini juga tidak menyertakan berkas JSONL asli, pengaturan filter pribadi, kunci pseudonim, dan peta identitas. Teks yang dipilih, identitas yang secara eksplisit dipertahankan, dan berkas yang disertakan masih dapat mengandung nama, ID, atau frasa yang sama dengan yang digunakan dalam filter tersebut; hal-hal tersebut memerlukan tinjauan terpisah. Kebijakan pribadi dan kunci pseudonim disimpan dalam bentuk terenkripsi di brankas lokal untuk pekerjaan tersebut; menghapus pekerjaan akan menghapus catatan pengungkapan pribadi yang terkait. Catatan kebijakan publik mencatat jumlah filter, bukan nilai filter. Tujuan yang dinyatakan bersifat publik dalam manifest dan HTML: kriteria pribadi yang eksplisit dan, dalam mode pseudonim, identitas tersembunyi yang diketahui juga disamarkan di sana, termasuk saat teks pesan dihilangkan. Jaga agar tujuan tetap bebas dari detail pribadi yang tidak perlu; konteks identifikasi yang tidak diketahui dapat tetap ada.

Manifestnya mengikat berkas-berkas turunan, kebijakan publik, dan hash dari ZIP asli. Verifikasi dapat memastikan integritas dan, jika sumber disediakan secara lokal, kesesuaian tautan sumber:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Tautan sumber tidak secara mandiri membuktikan bahwa transformasi tersebut telah memilih setiap item yang diperlukan atau menghapus setiap detail yang dapat mengidentifikasi. Teks asli tidak disertakan sebagai bukti. Diperlukan tinjauan baru untuk penilaian tersebut.

## Perlindungan data dan pratinjau Capture yang dihosting

Kontrol-kontrol ini mendukung prinsip pembatasan tujuan dan minimalisasi data; namun, kontrol-kontrol ini bukanlah pemeriksaan kepatuhan hukum otomatis. [Pasal 5 dan 25 GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) mengatur prinsip-prinsip tersebut serta perlindungan sejak awal/secara default. Dasar hukum, keharusan, syarat kategori khusus jika berlaku, penyimpanan, keamanan, dan akses penerima tetap memerlukan keputusan yang sesuai dengan kasusnya. Tujuan litigasi saja tidak membuat setiap pengungkapan menjadi sah. Data yang dipseudonimkan umumnya tetap merupakan data pribadi; lihat [penjelasan EDPB](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).

Teks bebas, tanggal, peristiwa langka, dan kombinasi fakta dapat mengidentifikasi seseorang bahkan setelah nama dihapus. Prioritaskan penghilangan teks jika isi pesan tidak diperlukan; periksa salinan lengkapnya jika diperlukan. Lindungi sumber dan brankas, sepakati masa penyimpanan dan pembagian dengan pihak yang bertanggung jawab, serta catat ZIP mana yang tepat telah diserahkan.

Fitur ini berjalan di panel lokal. Elemen [Pratinjau tangkapan layar yang dihosting](https://phishdestroy.github.io/TgWitness/docs/capture/) yang diterbitkan secara terpisah menggunakan runner sekali pakai yang disematkan dan kebijakan attestation-nya sendiri. Tanda tangan pengumpul lokal tidak mewarisi asal-usul runner tersebut. Perubahan di sini tidak memperbarui alur kerja jarak jauh yang telah disetujui atau pin kepercayaannya; penangkapan akun lengkap yang dihosting memerlukan pasangan pengumpul/alur kerja yang ditinjau dan diterbitkan secara terpisah serta penerimaan runner aktif. Uji sintetik lokal tidak mengklaim adanya penyebaran yang dihosting atau perolehan akun Telegram yang sebenarnya.

[Format bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/) · [Laporan kasus](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/)
