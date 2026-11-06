# Konfigurasi dan verifikasi laporan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/

Filter laporan, delapan desain, preset konten, riwayat perubahan yang disimpan, dan penilaian yang disertakan dalam ekspor yang telah ditandatangani.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/id/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Ubah pengamatan yang dipilih menjadi laporan kasus yang mudah dibaca: pertanyaannya, ruang lingkupnya, perubahan yang disimpan, bagan, temuan, dan referensi sumber. Setiap laporan memberikan penerima cara untuk memeriksa materi yang dikirimkan dan meninjau cakupan pengumpulannya.

Bagian **Dasar Kepercayaan dan Batasan** muncul dalam laporan jurnal, serah terima, obrolan, akun, dan berbagi. PDF jurnal dan serah terima menggunakan penilaian yang sama dengan `report.json` yang telah ditandatangani. Manifest ZIP menyertakan `case_assessment` dalam manifest yang telah ditandatangani. Penilaian ini disertakan bersama materi yang diekspor. Pengamatan asli tetap mempertahankan tanda tangan yang ada.

## Format dokumen dan urutan pembacaan

### Studio Laporan

Buka **Ekspor → Konfigurasi dan pratinjau**. Lanjutkan ke **Data → Desain & konten → Pratinjau**:

1. Gunakan seluruh ruang kerja atau pilih obrolan, penulis, termasuk tanggal pengamatan UTC dan jenis peristiwa. Muat katalog untuk mencari obrolan dan penulis, atau masukkan ID Telegram mereka. Filter penulis mencocokkan ID pengirim yang terekam; pemberitahuan penghapusan tanpa pengirim tidak cocok dengan filter penulis.
2. Pilih desain halaman, lalu pilih bagan, label peserta, transkrip, dan temuan tertulis Anda. Mengubah desain akan mempertahankan pilihan-pilihan ini.
3. Buat pratinjau. Pratinjau ini menampilkan jumlah aktual, aktivitas, peserta, contoh catatan, perubahan yang disimpan, dan rentang nomor pesan yang hilang. Mengubah pilihan akan membuat pratinjau menjadi kedaluwarsa. Simpan sebelum mengunduh HTML, PDF yang ditandatangani, JSON yang ditandatangani, atau ZIP bukti.

Pratinjau data menghitung prefiks jurnal stabil secara lengkap, bukan sampel awal. Hanya baris sampel yang ditampilkan dan daftar panjang yang dibatasi; jumlah yang dihilangkan ditampilkan. Ekspor selanjutnya akan mengambil snapshot stabil yang baru, sehingga pengumpulan yang sedang berlangsung dapat meningkatkan angka-angka tersebut. Cakupan, jumlah, dan identitas sumber disertakan dalam laporan yang ditandatangani. Membuka atau melihat pratinjau formulir tidak akan menyimpannya.

**Jurisdiction guidance.** Under Document details, open **Jurisdiction guidance · optional** to choose a jurisdiction and civil/commercial or criminal procedure. The appendix carries the legal basis, source links, preparation notes and research status. Local-language summaries and explanations of collection safeguards are optional. No jurisdiction is selected by default. These choices belong to the workspace, and are excluded from saved layout configurations and implicit sharing-copy defaults. See [defaults, supported reports and research limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md).

**Pilih salinan untuk penerima.** Bagan dan transkrip menggunakan catatan yang dipilih. Integritas, penyimpanan, dan cakupan menggambarkan jurnal sumber secara lengkap. File ZIP bukti berisi catatan asli dan lampirannya. Gunakan [serah terima yang dipersempit](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#handover-extract) jika penerima hanya perlu menerima data yang dipilih dan diizinkan.

### Baca perubahan, penghapusan, dan ID yang hilang

Pengeditan menampilkan teks **Sebelum** dan **Sesudah** yang disimpan serta menyoroti kata-kata yang diubah. Penghapusan menampilkan versi terakhir yang disimpan sebelum pemberitahuan. Jika tidak ada konten sebelumnya yang terekam, laporan akan mencantumkannya. Saat Anda memilih hanya pengeditan atau penghapusan, versi sebelumnya tetap tersedia sebagai konteks yang diberi label secara eksplisit di luar filter. Pesan yang tidak terkait tidak ditambahkan ke riwayat ini.

**ID pesan yang tidak teramati** adalah celah antara angka-angka yang diketahui dalam obrolan yang dipilih dan rentang ID yang diturunkan dari tanggal. Setiap catatan sumber yang diketahui diperiksa sebelum menyatakan suatu angka sebagai tidak teramati: menyaring penulis lain, jenis peristiwa, atau tanggal tidak dapat menciptakan celah palsu. Pesan-pesan yang disimpan di sekitarnya diberi label sebagai konteks. Angka yang hilang tidak membuktikan bahwa pesan tersebut pernah ada atau telah dihapus; pemberitahuan penghapusan dan pemeriksaan ulang yang gagal tetap merupakan jenis peristiwa yang terpisah.

### Pilih desain

Tersedia delapan desain halaman untuk laporan jurnal dan obrolan tunggal dalam format HTML serta PDF yang ditandatangani. Laporan-laporan tersebut menggunakan catatan dan perhitungan yang sama, dengan sampul, tipografi, judul bab, tabel, dan spasi yang berbeda.

| Desain | Gaya penulisan |
| --- | --- |
| Klasik | Sebuah berkas tradisional dengan sampul berwarna gelap dan bagian-bagian yang diberi nomor. |
| Editorial | Halaman judul berbingkai dengan huruf serif, margin lebar, dan daftar isi bab yang ramping. |
| Pengarahan | Sampul ringkas dengan punggung berwarna biru tua, judul-judul singkat, dan tabel dengan spasi yang rapat. |
| Analisis | Sampul bergaya survei, lembar bagan modular, dan gambar dengan spasi monospaced. |
| Teknis | Buku catatan bergaris, daftar referensi bernomor, dan tabel perbandingan yang akurat. |
| Gambaran Umum | Sampul panorama, spasi yang lapang, dan gambar ringkasan yang menonjol. |
| Seri bacaan | Sebuah bilah bagian dan bab-bab yang dikelompokkan untuk temuan, ruang lingkup, perubahan, dan jurnal pengamatan. |
| Buku besar & margin | Bab-bab bernomor dengan margin lebar, tabel dan bagan yang tepat, serta transkrip pesan terpisah. |

Desain disimpan per ruang kerja dan dicatat dalam manifes ekspor yang ditandatangani. HTML dapat berfungsi secara offline, mendukung tema terang dan gelap, serta beradaptasi dengan layar sempit dan bahasa yang ditulis dari kanan ke kiri. PDF asli menggunakan font yang disertakan; desain Editorial mencakup Noto Serif di bawah Lisensi Font Terbuka SIL yang disertakan. Seri bacaan serta Ledger & margin juga berlaku untuk ikhtisar akun, obrolan akun, dan salinan yang dibagikan.

PDF dalam bahasa Mandarin, Jepang, dan Korea juga memerlukan font yang sesuai di server, seperti Noto Sans CJK, yang diinstal secara sistem atau ditempatkan di `TGWITNESS_FONT_DIR`. Jika font tersebut tidak tersedia, berkas ZIP akan menyimpan laporan HTML dan JSON.

Kedua desain ini mencakup jurnal yang dapat dibaca tanpa JavaScript. Untuk ekspor berukuran besar, tampilan ini menampung hingga 500 catatan lengkap dalam batas input 8 MiB; laporan tersebut mencantumkan batas tersebut dan menautkan ke penampil lengkap serta catatan sumber. Direktori akun dan indeks hubungan menggambarkan sampel bacaan yang sama, bukan semua peserta. Bagan jurnal lengkap mempertahankan cakupan yang dinyatakan secara terpisah.

### Pilih kontennya

| Daftar isi yang telah ditentukan | Disertakan secara default |
| --- | --- |
| Berkas kasus | Aktivitas, waktu pengamatan, peserta, obrolan, dan transkrip rekaman. |
| Pengarahan | Gambaran umum aktivitas tanpa peringkat peserta atau transkrip. |
| Tinjauan aktivitas | Aktivitas, waktu pengamatan, peserta, obrolan, dan komposisinya, beserta referensi sumber dan angka yang tepat. |
| Laporan khusus | Kombinasi diagram, transkrip, dan pratinjau sesuai keinginan Anda. |

Mengubah preset akan mempertahankan desain, detail kasus, dan analisis tertulis Anda. Pemeriksaan integritas, cakupan, batasan, dan petunjuk verifikasi tetap ada di setiap desain. Catatan sumber dalam ZIP tetap tidak berubah saat bagan atau transkrip disembunyikan.

**Catatan Pemeriksaan** opsional berisi pertanyaan, metode, temuan, dan kesimpulan yang ditulis oleh penulis laporan. Cantumkan file sumber dan nomor catatan dalam temuan. Tanda tangan melestarikan pernyataan yang ditulis ini bersama dengan laporan; pengamatan sumber dan interpretasi penulis tetap dapat diidentifikasi. Serah terima yang dipersingkat menghilangkan catatan pribadi ini dan grafik jurnal lengkap. Pilihan grafik dan pemeriksaan berlaku untuk laporan jurnal.

Pilih aktivitas berdasarkan waktu, peta panas hari kerja/jam UTC, peringkat peserta, peringkat obrolan, dan komposisi catatan. Pilih 5–30 grup yang diurutkan dan alias peserta netral atau ID akun. Pengirim yang tidak dikenal dan peserta lainnya ditampilkan dalam baris terpisah. Alias hanya memengaruhi grafik; catatan sumber tetap berisi identitas asli mereka.

Pratinjau desain diperbarui dari draf yang belum disimpan menggunakan sampul produksi, pemeriksaan, dan komponen bagan, terbatas pada kecocokan dalam 50.000 catatan sumber pertama. Pratinjau data di bawah ini menghitung seluruh pilihan. Pratinjau ini secara eksplisit belum ditandatangani dan tidak menyimpan hasil pengeditan. Tombol Sampul dan Bagan berfungsi untuk mengganti bagiannya. Ini bukan pratinjau PDF yang lengkap. **Menyimpan pengaturan laporan** akan menerapkan pilihan tersebut ke ekspor di masa mendatang; file yang sudah ditandatangani tidak dapat diubah. PDF menggunakan sampul yang dipilih, tipografi, tata letak bab, dan agregat yang sama seperti yang dipilih untuk HTML dan JSON yang ditandatangani.

Penilaian kepercayaan, batasan cakupan, dan petunjuk verifikasi tetap ada. Menyembunyikan grafik atau transkrip yang dapat dibaca tidak menghapus baris sumber otoritatif dari ZIP. Seri grafik yang dinonaktifkan dihilangkan dari JSON analitis; gunakan ekspor yang diminimalkan untuk membatasi pengungkapan catatan sumber.

Filter pemilihan data berlaku untuk laporan jurnal; ekspor akun dan berbagi tetap memiliki cakupan akuisisi dan pengungkapan masing-masing.

Preferensi desain/bagan yang dibagikan dibekukan ke dalam ekspor obrolan/akun baru dan pratinjau pembagian akun. Pengaturan bahasa dan privasi akun/pembagian tetap independen; catatan kasus dan pemeriksaan pribadi tidak disalin ke dalam ekspor ini. Laporan akun dan pembagian tetap dalam format HTML yang dilindungi oleh manifes arsip yang telah ditandatangani. Jurnal, serah terima jurnal yang dipersingkat, dan paket obrolan tunggal juga menyediakan PDF yang ditandatangani.

### Apa yang dihitung oleh bagan-bagan tersebut

Aktivitas jurnal dan peta panas menghitung **pengamatan** baru, historis, yang dipulihkan, diedit, dihapus, dan yang hilang saat diperiksa ulang, berdasarkan waktu pengamatan pengumpul dalam UTC. Heartbeat dan tanda terima lampiran tidak termasuk. Peringkat peserta hanya menghitung pengamatan pesan baru, historis, dan yang dipulihkan: pengirim tidak dinyatakan sebagai pengedit atau penghapus. Pengamatan berulang dapat menggambarkan pesan Telegram yang sama.

Analisis jurnal menyimpan jumlah berdasarkan jenis, referensi catatan pertama/terakhir, dan SHA-256 sumber `events.jsonl`. Angka-angka mencakup nilai pasti dalam HTML dan PDF. Kelompok harian beralih ke bulan setelah 366 hari yang tercatat; grafik menggabungkannya menjadi maksimal 36 interval dengan lebar yang sama. Lebih dari 100.000 pengenal unik atau 1.200 tanda bulan menyebabkan grafik yang bersangkutan tidak tersedia, sementara jumlah keseluruhan yang tepat tetap tersedia.

Bagan snapshot dan berbagi akun hanya menghitung baris pesan non-layanan yang disertakan, dengan menggunakan waktu pesan yang tercatat. Agregat berbagi dihitung setelah penyuntingan dan penyaringan. Bagan-bagan ini menggunakan paling banyak 90 interval tanggal UTC dengan lebar yang sama dan menyimpan hingga 10.000 nilai pengelompokan; jumlah yang melebihi batas tersebut dinyatakan secara eksplisit dan direkonsiliasi. Interval terakhir mungkin lebih pendek. Tanggal yang tidak diketahui atau tidak valid tidak dimasukkan ke dalam grafik waktu.

Interval kosong berarti tidak ada pengamatan yang disertakan; periksa cakupan untuk mengetahui celah. Bagan-bagan ini menggambarkan aktivitas yang disimpan. Pengirim yang tidak dikenal tetap menjadi kategori terpisah, dan setiap pemeriksaan dilaporkan secara terpisah.

Jika disertakan, `analytics.json` dilindungi oleh hash file yang ditandatangani dari arsip. `report.json` jurnal menyematkan agregat terpilih yang sama. Verifikasi tanda tangan mendeteksi byte yang berubah. Untuk memeriksa angka-angka tersebut, hitung ulang agregat jurnal dengan `report_analytics.Analytics` dan `selected`, atau agregat snapshot dengan `snapshot_analytics.collect` dan `project`.

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | Apa yang ditampilkannya |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day. A flag requires at least five first-time posters and three times their median, with message volume at most 1.5 times its median. The baseline uses at least seven observed days within the previous 14 calendar days, after seven days of warm-up. |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows, including in filtered reports. Daily and monthly tables show recent rows, service-share tables rank chats by saved message count. Totals cover every row.

Dari checkout sumber, buatlah kedelapan desain yang tercantum di atas dari jurnal fiktif yang sama:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Buka berkas `index.html` yang dihasilkan untuk membandingkan laporan HTML lengkap, PDF yang telah ditandatangani, dan berkas ZIP. Setiap desain menggunakan jurnal sumber yang sama. Gunakan direktori keluaran baru untuk setiap proses agar contoh yang telah ditandatangani sebelumnya tetap terjaga.

![Dokumen HTML fiktif](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

Halaman HTML dibuka dengan sampul kasus dan angka-angka kunci. Peta bukti bernomor tertaut ke setiap temuan, fakta pendukungnya, batasan, dan tinjauan independen. Catatan yang dapat dicari serta referensi catatan yang stabil tetap tersedia di penampil offline. Desainnya dapat beradaptasi dengan layar sempit, baik tema maupun browser tanpa JavaScript.

PDF yang telah ditandatangani memiliki sampul A4 khusus, referensi laporan dan QR, ringkasan eksekutif, peta bukti, temuan bernomor, dan penanda dokumen. Header dan footer halamannya mengidentifikasi laporan tersebut. QR mengidentifikasi materi; ini bukan hasil verifikasi independen. Cetakan dari browser terpisah dari PDF yang ditandatangani secara kriptografis ini.

Garis waktu pengamatan menempatkan periode pengamatan yang terekam dan gangguan pada sumbu UTC yang sama. Ruang kosong tidak berarti cakupan yang disimpulkan; tabel terperinci mempertahankan interval yang tepat. File ZIP berisi laporan yang dapat dibaca, JSON yang ditandatangani, catatan sumber, dan petunjuk verifikasi.

Buatlah berkas baru yang fiktif dalam bahasa Inggris/Rusia/Jerman dengan lingkungan pengembangan yang telah terinstal:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Setiap direktori bahasa berisi `report.html`, `report.pdf`, `report.json`, dan `dossier.zip`. Direktori contoh yang sudah ada tidak akan pernah ditimpa. Tidak ada akun Telegram, layanan penanda waktu eksternal, atau koneksi jaringan yang digunakan untuk membuatnya.

![Tiga halaman pertama dari PDF fiktif yang telah ditandatangani](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Membaca kasus konkret

Untuk jurnal yang berisi 1.200 entri dengan cap waktu yang tervalidasi pada entri ke-1.000, laporan tersebut mengidentifikasi 200 entri selanjutnya yang berada di luar batas cap waktu tersebut. Ini merupakan batas atas keberadaan titik pemeriksaan, bukan bukti waktu pengiriman setiap pesan. Jika tiga berkas cap waktu lainnya gagal validasi atau tidak dapat divalidasi, mereka dihitung secara terpisah dan tidak dapat memberikan kesimpulan yang pasti.

Stempel waktu yang dapat digunakan harus memenuhi semua pemeriksaan berikut: jejaknya cocok dengan titik pemeriksaan, tanda tangannya terhubung ke akar TSA tepercaya pada waktu yang dicap, dan tanda tangan, kunci, hitungan, serta kepala titik pemeriksaan tersebut cocok dengan awalan jurnal yang tepat. Hanya mengurai cap waktu atau memiliki tanda terima OTS saja tidak cukup. Pembaca harus secara mandiri memilih akar TSA tepercaya dan mengulangi verifikasi. OTS memerlukan pemeriksaan konfirmasi Bitcoin-nya sendiri.

| Status laporan | Arti |
| --- | --- |
| Telah diperiksa selama proses ekspor | Eksportir telah melakukan pemeriksaan yang disebutkan; pengulangan secara independen masih diperlukan. |
| Telah direkam; perlu ditinjau | Pengamatan atau pernyataan operator yang mendasari dicatat; hal ini bukanlah konfirmasi independen. |
| Tidak termasuk dalam salinan ini | Teks tersebut tidak memiliki bukti pendukung untuk klaim ini. Teks tersebut juga tidak menyatakan bahwa tidak ada bukti serupa di tempat lain. |
| Belum diverifikasi secara independen | Laporan ini tidak memberikan hasil verifikasi independen. |
| Tidak lengkap atau tidak tersedia | Ada materi atau pemeriksaan yang diperlukan yang hilang, tidak lengkap, atau tidak berhasil. |

Tinjau setiap pemeriksaan secara terpisah, bersamaan dengan cakupan pengumpulan yang tercatat.

## Apa saja yang harus dipertahankan dalam konfigurasi yang kuat

1. Sebelum mengandalkan proses pengumpulan, simpan sidik jari kunci pengumpul melalui saluran tepercaya yang terpisah. Bandingkan referensi tersebut dengan kunci penandatanganan ekspor.
2. Pertahankan titik pemeriksaan yang diberi cap waktu secara independen dan, jika digunakan, jurnal saksi di luar kendali administratif pengumpul. Bandingkan dengan jurnal yang diekspor untuk memeriksa batas-batas sebelumnya.
3. Cakupan akuisisi catatan, celah, filter, batasan, dan perubahan dalam pengumpulan. Jelaskan periode yang hilang yang relevan dengan klaim yang sebenarnya, dengan tetap membedakan ID pesan yang tidak teramati, pemberitahuan penghapusan, dan pemeriksaan ulang yang gagal.
4. Pertahankan file ZIP asli beserta hash-nya. Catat setiap pemegang, transfer, tanggal, dan tujuan. Pertahankan pernyataan operator yang dikaitkan serta catatan kasus bersama dengan data tersebut.
5. Untuk VM rahasia, pertahankan dan verifikasi secara independen kutipan, tantangan, rantai sertifikat Intel, pengukuran, sumber yang tepat, dan kondisi penanganan kunci. Simpan hasil verifikasi attestation bersama artefak yang telah ditinjau.

See [verification scope](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope) for the checks of acquisition, archive integrity, time and collection coverage in each mode.

## Tinjauan penerima

Gunakan instalasi TgWitness yang tepercaya dan sidik jari yang diperoleh secara independen:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

File ZIP saksi harus berasal dari sumber tepercaya yang independen; pertahankan juga kuncinya dan asal-usulnya. Pertahankan perintah, versi alat, hasil, hash masukan yang telah ditinjau, serta pertanyaan yang belum terjawab. Verifikasi Beacon adalah pemeriksaan daring terpisah; pembuat laporan tidak pernah menghubungi layanan apa pun hanya untuk menampilkan laporan.

Untuk sengketa terkait pesan tertentu, cantumkan referensi arsip, referensi berkas dan catatan yang sah, lalu jelaskan rentang waktu yang relevan, celah cakupan, pemilihan, dan bahan pendukung. Untuk salinan yang dibagikan, tinjau juga transformasi yang tercatat beserta referensinya ke arsip sumber. Filter pribadi dan pemetaan identitas tidak termasuk dalam penilaian publik.

Verifikasi PDF yang ditandatangani mendeteksi perubahan pada byte yang tercakup. Simpan file digital asli dan hasil verifikasi bersama dengan tangkapan layar atau salinan cetak untuk dibaca.
