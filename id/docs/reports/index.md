# Rancang laporan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reports/

Berikan pembaca jalur yang jelas dari pertanyaan kasus hingga catatan yang disimpan.

Report Studio menggabungkan pemilihan data, riwayat perubahan yang mudah dibaca, bagan, dan temuan tertulis Anda. Delapan desain terintegrasi berlaku untuk keluaran HTML dan PDF asli yang didukung. Laporan HTML, PDF, dan JSON memiliki segel tanda tangan masing-masing; manifest ZIP juga mengikat file-file dalam paket tersebut. HTML dan PDF disegel setelah tata letak akhirnya selesai.

## Buat laporan dalam tiga langkah

1. Buka **Ekspor → Konfigurasi dan pratinjau → Data**. Gunakan seluruh ruang kerja atau pilih obrolan, penulis, tanggal pengamatan UTC yang mencakup, dan jenis catatan. Tanggal-tanggal tersebut menggambarkan kapan TgWitness mengamati catatan tersebut.
2. Di bagian **Desain & Konten**, pilih preset desain dan konten. Pilih bagan aktivitas, label peserta, transkrip, perubahan yang disimpan, dan materi Case Board opsional. Tambahkan detail kasus dan catatan pemeriksaan Anda.
3. Buka **Pratinjau** untuk meninjau jumlah, aktivitas, peserta, catatan yang diambil sampelnya, dan rentang ID yang hilang. Simpan pengaturan, lalu unduh format yang Anda butuhkan.

### Susun materi yang disimpan tersebut agar mudah dipahami oleh pembaca

Contoh sintetis · tata letak skematis, bukan laporan yang dihasilkan

1. **Pilih.** Pilih dua obrolan dan periode pengamatan untuk kasus tersebut.
2. **Tulis.** Pilih tata letak dan bagian-bagian yang menjawab pertanyaan tersebut.
3. **Pratinjau.** Periksa jumlah yang dipilih dan teks sebelum dan sesudah yang telah disimpan.
4. **Verifikasi.** Buat berkas akhir dan periksa tanda tangannya dengan sidik jari ruang kerja tepercaya.

#### Catatan terpilih

2 obrolan · 1 hari pengamatan

Pesan, pengeditan, dan pemberitahuan penghapusan

#### Struktur laporan

##### Perubahan tujuan pembayaran

Pertanyaan kasus → ruang lingkup → temuan → referensi catatan

**Konteks pesan**

Pengamatan #142: “Gunakan tautan pembayaran yang baru.”

**Perubahan yang disimpan**

Sebelum: old.example.invalid → Setelah: new.example.invalid

#### Tinjau pilihan tersebut

18 komentar · 2 suntingan yang disimpan

Waktu pengiriman, pengeditan, dan pemantauan memiliki label terpisah.

#### Hasil akhir

PDF yang ditandatangani + JSON yang ditandatangani, atau ZIP yang ditandatangani beserta laporannya yang dapat dibaca

Penerima memeriksa berkas dan sidik jari yang tepercaya.

## Pilih gaya penulisan

**Seri Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading, serta Ledger & margin** menyajikan catatan dasar yang sama dalam komposisi yang berbeda. Perubahan desain tetap mempertahankan pemilihan data dan catatan tertulis. Bahasa laporan dapat dipilih dari 25 bahasa yang didukung.

Seri bacaan mengelompokkan kasus, ruang lingkup, temuan, dan perubahan di sekitar rel bagian. Ledger & margin menggunakan bab bernomor dan margin lebar. Keduanya juga mendukung ikhtisar HTML akun dan berbagi salinan. PDF asli dihasilkan dengan font yang disertakan; mesin pengguna tidak memerlukan browser atau instalasi Node untuk pembuatan PDF. PDF dalam bahasa Mandarin, Jepang, dan Korea juga memerlukan font yang sesuai di server, seperti Noto Sans CJK, yang diinstal secara sistem atau ditempatkan di `TGWITNESS_FONT_DIR`. Tanpa font tersebut, ZIP akan menyimpan laporan HTML dan JSON.

## Baca perubahan beserta konteksnya

Perubahan yang disimpan ditampilkan dalam bentuk sebelum dan sesudah. Pemberitahuan penghapusan dapat disertai dengan versi terakhir yang terekam. Balasan, kutipan, penerusan, reaksi, tombol, dan metadata lampiran tetap mempertahankan referensi yang tersedia. SHA-256 file dan hash catatan jurnal diberi label secara terpisah.

Pratinjau desain menampilkan komponen sampul, pemeriksaan, dan bagan menggunakan catatan yang cocok di antara 50.000 catatan sumber pertama. Pratinjau data terpisah memindai snapshot jurnal stabil secara lengkap untuk menghitung jumlah pilihan yang tepat, dengan batas sampel yang ditampilkan diberi label. Buat PDF untuk memeriksa paginasi akhir. Ekspor akun lengkap dilengkapi dengan ikhtisar HTML; PDF obrolan individualnya menggunakan desain yang dipilih.

## Pilih salinan untuk penerima dengan cermat

Filter laporan membentuk laporan yang mudah dibaca. File ZIP bukti lengkap mempertahankan jurnal asli dan lampirannya. Gunakan [penyerahan data](https://phishdestroy.github.io/TgWitness/id/docs/handover/) [yang](https://phishdestroy.github.io/TgWitness/id/docs/handover/) [dipersingkat](https://phishdestroy.github.io/TgWitness/id/docs/handover/) jika penerima hanya perlu menerima data yang dipilih. Lihat [isi laporan dan verifikasi,](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/) atau [verifikasi ekspor yang telah selesai](https://phishdestroy.github.io/TgWitness/id/docs/exports/).
