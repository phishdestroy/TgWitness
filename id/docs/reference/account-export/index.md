# Ekspor akun

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/account-export/

Ekspor apa yang dapat dibaca oleh suatu akun saat ini: cakupan, tugas yang dapat dilanjutkan, arsip yang telah ditandatangani, dan salinan berbagi yang telah diminimalkan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bukti dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/)

![Bukti & verifikasi](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

Ekspor akun mencadangkan akun itu secara eksklusif. Jeda pemantauan atau pengambilan data lain secara eksplisit sebelum memulai atau melanjutkan; aplikasi tidak pernah menghentikannya otomatis.

Sebagai administrator instalasi, pilih **Mulai di sini → Ekspor akun saya**, atau **Ekspor → Akun Telegram → Konfigurasi ekspor akun**. Masuk jika diperlukan, tinjau cakupan, dan mulai ekspor secara eksplisit. Pengamatan berkelanjutan tidak diperlukan. **"Pengamatan yang disimpan**" adalah ekspor terpisah dari jurnal yang ada; ZIP-nya mencakup semua sumber terlepas dari filter jurnal. Setiap ruang kerja memiliki tugas, identitas penandatanganan, dan penyimpanan sendiri. Akses panel yang diberikan, termasuk izin ekspor biasa tanpa batasan, tidak dapat membuka rute-rute yang berlaku untuk seluruh akun ini.

Filter pengirim dan teks dapat diperluas di bawah **"Filter berdasarkan pengirim atau teks pesan**". Bagian "**Data akun & metode koneksi"** berisi kategori akun opsional dan pilihan "Takeout" atau "sesi reguler"; ringkasannya menampilkan pilihan yang aktif meskipun panel tersebut ditutup. Menutup bagian-bagian ini akan mempertahankan pengaturannya. Draf ekspor dan laporan tetap ada di sesi panel saat ini saat berpindah tampilan; draf tersebut tidak disimpan saat browser dimuat ulang. Pekerjaan yang sudah ada tetap dapat diakses dari kedua pilihan ekspor tersebut.

Alur kerja ini mengekspor data yang saat ini dapat diakses oleh akun yang terhubung. Pengaturan default menggunakan [Telegram Takeout](https://core.telegram.org/api/takeout); ini bukanlah cadangan data Telegram yang tidak tersedia atau telah dihapus. Obrolan Rahasia, riwayat yang tidak dapat diakses, dan suntingan sebelumnya tidak dapat dipulihkan. Telegram dapat memberlakukan masa tunggu sebelum Takeout dimulai. Panel menampilkan masa tunggu tersebut; panel tidak secara diam-diam mengganti metode pengiriman data. Opsi API reguler eksplisit memiliki cakupan yang berbeda dan merekam kategori yang tidak didukung.

Takeout adalah API ekspor resmi yang juga digunakan oleh Telegram Desktop. TgWitness dapat menulis JSON yang kompatibel dengan Desktop langsung dari akuisisi sendiri; mengimpor arsip orang lain tidak diperlukan. ID obrolan dan pesan tersedia melalui kedua saluran tersebut. Obrolan publik atau izin untuk meneruskan tidak menjamin ekspor yang lebih cepat atau menghilangkan penundaan persetujuan Takeout. Ukur cakupan dan pengaturan media yang sama sebelum membandingkan kecepatan.

Untuk hingga 20 ID obrolan yang dipilih secara eksplisit, ekspor API reguler menyelesaikan rekan-rekan tersebut secara langsung sebelum mempertimbangkan inventaris dialog lengkap akun tersebut. Saluran publik yang dapat dibaca karenanya dapat diekspor tanpa harus bergabung dengannya, bahkan ketika saluran tersebut tidak ada dalam daftar dialog. Mitra yang tidak tersimpan dalam cache akan kembali ke inventaris biasa. Filter arsip tetap diberlakukan: jika Telegram tidak mengembalikan dialog dan obrolan yang diarsipkan dikecualikan, status arsip yang tidak diketahui dicatat sebagai kelalaian. Takeout mempertahankan prosedur inventaris rentang terpisah. Kedua jalur tersebut tidak bergabung dengan obrolan atau mengubah izin penerusan. Dalam format JSON yang kompatibel dengan Desktop, saluran yang ditandai Telegram sebagai `left` muncul di bawah `left_chats`, termasuk saluran publik yang dapat dibaca yang belum diikuti oleh akun tersebut.

Baik permintaan jeda `FLOOD_WAIT` maupun `FLOOD_PREMIUM_WAIT` berlaku selama seluruh periode yang diminta server. Batas waktu akun tetap berlaku meskipun terjadi koneksi ulang dan restart; waktu tunggu yang lebih singkat di kemudian hari tidak dapat memperpendeknya. Upaya ulang dibatasi, pembatalan mempertahankan halaman yang disegel, dan kredensial API tidak diganti untuk menghindari batasan laju. Tidak ada pembelian Premium yang dilakukan.

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

Payload foto menggunakan varian gambar diam yang diidentifikasi dalam metadata dan manifest hash-nya, termasuk foto dengan varian avatar animasi. Animasi tersebut tidak digantikan oleh gambar diam yang dipilih. Payload yang lebih pendek atau lebih panjang dari ukuran yang diamati akan dicatat sebagai lampiran yang gagal, dan representasi yang berubah selama pembaruan referensi file akan ditolak. Kegagalan ini membuat arsip menjadi tidak lengkap namun tetap mempertahankan catatan pesan. Verifikasi independen juga menolak lampiran yang disimpan yang panjang tanda tangannya bertentangan dengan ukuran atau representasi yang diamati, termasuk dalam arsip yang lebih lama.

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

### Pesan yang tidak termasuk dalam pemilihan

**Pratinjau.** Sebuah pengungkapan tidak terlihat lengkap jika memang belum lengkap. Di dalam setiap obrolan yang menyimpan setidaknya satu pesan yang telah diungkapkan, pesan-pesan yang tidak termasuk dalam pilihan akan muncul sebagai penanda, `[withheld by selection — rule: sender]` (atau `text`, `period`). Pilih **"Pesan yang tidak termasuk dalam pilihan**": satu penanda untuk setiap rangkaian pesan yang ditahan secara berurutan (default) atau satu penanda untuk setiap pesan. Penanda hanya menampilkan aturan dan jumlah, tidak pernah menampilkan teks, pengirim, tanggal, atau file. Obrolan yang tidak memiliki pesan yang diungkapkan akan diabaikan sepenuhnya, sehingga paket ini tidak mengungkapkan keberadaan obrolan tersebut.

Balasan yang diungkapkan menunjukkan apa yang dijawabnya: pesan yang termasuk dalam salinan ini, pesan yang ditahan oleh seleksi, atau pesan yang tidak ada dalam ekspor sumber (dihapus sebelum ekspor atau tidak pernah diekspor; ekspor tidak dapat membedakan mana yang mana). Pesan yang ditahan yang dijawab oleh balasan yang diungkapkan selalu diberi penanda tersendiri, sehingga balasan tersebut mengarah ke catatan yang menjelaskan mengapa pesan tersebut kosong. Ketiga status ini berbeda dari penghapusan dan celah koleksi, yang merupakan bagian dari ekspor sumber.

Dalam `messages.jsonl` (format `tgwitness-account-disclosure-v2`) setiap pesan memiliki `state`: `disclosed`, atau `withheld` dengan `rules` dan `count`. Balasan yang diungkapkan memiliki `reply_to` bersama dengan target `id` dan `state` (`disclosed`, `withheld`, `not_in_source`). Manifest tersebut menghitung pesan, obrolan, media, dan `withheld` pesan. `verify.py` menolak penanda yang membawa konten dan balasan yang mengarah ke catatan yang tidak terdapat dalam paket; paket versi 1 diverifikasi seperti sebelumnya.

Format yang dipersingkat ini mengabaikan profil akun terstruktur, kontak, avatar, sesi, cerita, objek Telegram mentah, header penerusan, kutipan balasan, kartu kontak, dan metadata lokasi. Format ini juga tidak menyertakan berkas JSONL asli, pengaturan filter pribadi, kunci pseudonim, dan peta identitas. Teks yang dipilih, identitas yang secara eksplisit dipertahankan, dan berkas yang disertakan masih dapat mengandung nama, ID, atau frasa yang sama dengan yang digunakan dalam filter tersebut; hal-hal tersebut memerlukan tinjauan terpisah. Kebijakan pribadi dan kunci pseudonim disimpan dalam bentuk terenkripsi di brankas lokal untuk pekerjaan tersebut; menghapus pekerjaan akan menghapus catatan pengungkapan pribadi yang terkait. Catatan kebijakan publik mencatat jumlah filter, bukan nilai filter. Tujuan yang dinyatakan bersifat publik dalam manifest dan HTML: kriteria pribadi yang eksplisit dan, dalam mode pseudonim, identitas tersembunyi yang diketahui juga disamarkan di sana, termasuk saat teks pesan dihilangkan. Jaga agar tujuan tetap bebas dari detail pribadi yang tidak perlu; konteks identifikasi yang tidak diketahui dapat tetap ada.

Manifestnya mengikat berkas-berkas turunan, kebijakan publik, dan hash dari ZIP asli. Verifikasi dapat memastikan integritas dan, jika sumber disediakan secara lokal, kesesuaian tautan sumber:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Tautan sumber tidak secara mandiri membuktikan bahwa transformasi tersebut telah memilih setiap item yang diperlukan atau menghapus setiap detail yang dapat mengidentifikasi. Teks asli tidak disertakan sebagai bukti. Diperlukan tinjauan baru untuk penilaian tersebut.

## Berbagi dan penangkapan yang dihosting

Pilih pesan dan berkas yang dibutuhkan penerima, tinjau salinan lengkap yang dibagikan, dan simpan sumbernya secara terpisah. Catat hash ZIP yang telah dikirim agar penerima dapat mengidentifikasi dan memverifikasi salinan yang tepat tersebut. Pseudonimisasi menggantikan pengenal yang dipilih; teks yang disertakan dan berkas asli tetap menjadi bagian dari tinjauan.

GitHub Actions mendukung ekspor seluruh akun dan obrolan terpilih melalui Takeout atau API biasa, serta jurnal peristiwa satu obrolan. Panduan penangkapan yang dihosting  menjelaskan verifikasi pengaturan dan batas waktu 120 menit. Untuk memverifikasi salinan berbagi yang berasal dari penangkapan yang dihosting, bandingkan hash sumbernya dengan arsip asli dan verifikasi pengesahan arsip tersebut dengan pemeriksaan khusus mode .

[Format bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/) · [Laporan kasus](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/)
