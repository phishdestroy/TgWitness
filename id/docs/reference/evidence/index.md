# Format bukti

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/

Isi berkas ZIP yang telah ditandatangani, jenis catatan, tanda terima proses, profil pengguna, salinan di luar lokasi, dan verifikasi offline.

Sebuah pengamatan bukanlah kesimpulan. ID pengirim bukanlah identitas di dunia nyata. Pembaruan layanan yang terlihat di akun adalah sumbernya; Telegram tidak menandatangani secara kriptografis catatan yang disimpan ini untuk penyelidik pihak ketiga.

## Apa itu "ditandatangani"?

| Materi | Perlindungan | Apa yang perlu disimpan |
| --- | --- | --- |
| Setiap catatan dalam jurnal, termasuk peristiwa operasional | Rantai SHA-256 dan tanda tangan Ed25519 per peristiwa | `events.jsonl` asli, sidik jari kunci tepercaya, dan titik pemeriksaan yang disimpan |
| Isi berkas ZIP bukti | `manifest.sig` menandatangani manifes kanonik, yang mencantumkan hash dari berkas-berkas konten | File ZIP lengkap, termasuk manifes dan tanda tangannya |
| Lampiran yang disimpan | SHA-256 dan jumlah byte dalam peristiwa `media.saved` yang ditandatangani; hash berkas dalam manifes ZIP yang ditandatangani | Byte asli di dalam berkas ZIP yang telah diverifikasi |
| Checkpoint | Tanda tangan Ed25519 atas panjang jurnal, hash header, kunci publik, dan waktu pembuatan | Salinan independen yang disimpan sebelum adanya perubahan yang diperdebatkan |
| Bukti transaksi | Pengukuran pengumpul yang ditandatangani secara terpisah; juga disertakan dalam peristiwa `process.started` yang ditandatangani | Bukti penerimaan dan jurnal terkait; pengukuran dilaporkan sendiri |
| Berkas CSV atau HTML mandiri | Tidak ada tanda tangan kriptografis yang berdiri sendiri; hash peristiwa saja tidak cukup | Gunakan salinan persis yang terdapat di dalam berkas ZIP yang telah diverifikasi untuk pemeriksaan integritas |
| Tangkapan layar, cetakan, atau berkas PDF yang dihasilkan oleh peramban | Tidak ada tanda tangan TgWitness pada hasil turunan | Simpan paket asli yang telah diverifikasi dan dokumentasikan bagaimana turunan tersebut dibuat |

Pengumpul memverifikasi tanda tangan jurnal sebelum menghasilkan setiap format ekspor. Pemeriksaan sumber tersebut tidak menghasilkan tanda tangan pada file CSV atau HTML yang diunduh secara terpisah. Tanda tangan peristiwa JSONL yang valid juga tidak menyediakan byte lampiran atau secara independen memastikan bahwa seluruh jurnal yang diamati telah disediakan.

## Serah terima penyelidikan

1. Catat nomor referensi kasus, operator, ID akun Telegram numerik, sumber yang dipilih, kebijakan pengumpulan, dan periode pengumpulan dalam catatan kasus Anda. TgWitness menyimpan hasil pengamatan; penugasan kasus dan catatan penyimpanan dikelola di luar aplikasi. Sesuaikan pengaturan pengumpulan yang dimaksud dengan [prosedur penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Simpan sidik jari kunci publik ruang kerja secara terpisah sebelum mengandalkan ekspornya. Simpan titik pemeriksaan yang ditandatangani di luar pengumpul selama proses pengumpulan. Catat gangguan dan batasan visibilitas akun.
3. Ekspor berkas **ZIP yang telah ditandatangani** dan simpan tanda terima eksekusi yang telah ditandatangani. Gunakan titik pemeriksaan pada atau sebelum batas jurnal yang diekspor. Titik pemeriksaan yang lebih baru dapat dengan benar menolak ekspor sebelumnya karena terlalu pendek. Ekspor mencakup jurnal ruang kerja secara lengkap, terlepas dari filter panel; tinjau materi tersebut sebelum membagikannya.
4. Mintalah penerima untuk memverifikasi berkas ZIP tersebut menggunakan salinan verifier yang tepercaya dan sidik jari/titik pemeriksaan yang disediakan secara terpisah. Dari lingkungan checkout yang tepercaya dengan lingkungan Python-nya aktif:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Laporan keluaran yang berhasil menampilkan kode `key_pinned: true` dan `checkpoint_checked: true` ketika kedua masukan disediakan dan diterima. Pertahankan hasil verifikasi.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Catat SHA-256 arsip, batas ekspor, tanggal transfer, pengirim, dan penerima dalam catatan penyimpanan Anda. Jaga agar paket asli tetap utuh dan kerjakan dari salinan. Bagikan berkas bukti, bukan direktori data pribadi aplikasi yang juga berisi sesi akun dan rahasia penandatanganan. Untuk transfer, ekspor dapat dimasukkan ke dalam ZIP AES-256 yang dilindungi kata sandi. Kata sandi hanya melindungi kerahasiaan dan tidak disimpan; penerima mengekstrak arsip dan memverifikasi ekspor yang ditandatangani di dalamnya, yang tidak berubah.
   2. Jika diperlukan penandaan waktu independen, ikuti [prosedur RFC 3161](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/) dan simpan permintaan, titik pemeriksaan, informasi CA tepercaya, serta respons otoritas yang terverifikasi. Hanya menyiapkan permintaan saja tidak akan menghasilkan cap waktu.

Verifikasi yang berhasil membuktikan integritas relatif terhadap kunci pengumpul tepercaya dan batas yang dipertahankan. Kebenaran sumber, pengiriman Telegram yang lengkap, waktu yang tepercaya, dan kelayakan hukum memerlukan bukti terpisah. Versi ini belum menyelesaikan kualifikasi Telegram langsung atau penilaian forensik/keamanan independen.

Kunci pengumpul yang disalin dapat menandatangani jurnal pengganti yang dipalsukan. Verifikasi terhadap titik pemeriksaan atau catatan saksi yang disimpan secara independen dapat mendeteksi perubahan pada awalan sebelumnya; verifikasi tanda tangan saja tidak dapat melakukannya. Saksi memperbaiki apa yang disajikan oleh pengumpul, sehingga tidak secara independen menetapkan kebenaran catatan yang dipalsukan sebelum titik pemeriksaan eksternal pertama mereka. Laporan penerapan cloud memeriksa konfigurasi dan pengukuran yang dilaporkan pengumpul; laporan tersebut tidak menetapkan bahwa kunci pribadi tidak pernah disalin selama proses bootstrap.

Pemberitahuan yang dikirim melalui Apprise berisi nama ruang kerja dan obrolan serta jumlahnya; kutipan singkat dari pesan yang dihapus dan diedit hanya ditambahkan jika operator mengaktifkannya (secara default dinonaktifkan). Pemberitahuan ini merupakan sinyal kemudahan, bukan bukti: pengiriman tidak dijamin, dan hanya jurnal serta ekspornya yang ditandatangani yang mencatat apa yang diamati. Dengan proksi ruang kerja, pemberitahuan menggunakan rute yang sama; layanan yang tidak dapat menggunakannya, serta rute MTProxy, akan ditolak.

## Kanonikalisasi peristiwa

Masukan hash terdiri dari bidang-bidang berikut ini:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Serialisasikan menggunakan JSON yang kompatibel dengan Python dengan UTF-8, kunci objek yang diurutkan, tanpa escaping ASCII, tanpa spasi kosong yang tidak signifikan, dan tanpa NaN/infinity:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

SHA-256 dari byte-byte tersebut menjadi hash peristiwa. Tanda tangan menggunakan Ed25519 atas 32 byte hash mentah, kemudian dikodekan dengan base64. Previous_hash pertama adalah 64 angka nol. Nomor urut dimulai dari 1 dan bertambah 1 setiap kali. Semua peristiwa, termasuk peristiwa operasional, berada dalam satu rantai. Tidak ada penekanan pengiriman ganda: pengamatan yang berulang merupakan bukti terpisah, bukan klaim adanya tindakan Telegram yang berbeda.

Tanggal Telegram mentah berupa string ISO; bidang biner diubah menjadi objek yang berisi bytes_base64. Teks pesan, entitas, deskriptor media, metadata balasan, reaksi, dan tindakan layanan disimpan dalam metadata pesan mentah jika disediakan.

observed_at adalah waktu UTC pada jam sistem pengumpul. source_at adalah tanggal Telegram yang disediakan jika tersedia. Pemberitahuan penghapusan tidak menyertakan waktu penghapusan yang tepat, sehingga source_at tetap bernilai null. Urutan penerimaan data tidak selalu sama dengan urutan peristiwa sumber. Cuplikan riwayat menggunakan tanggal sumber yang lebih lama tetapi waktu pengamatan terkini.

## Semantik aktor

message.new actor_id adalah pengirim pesan. message.edited tidak memiliki editor yang disimpulkan; payload.sender_id mencatat pengirim dari pesan yang diamati. Penghapusan actor_id tetap null. Pesan layanan keanggotaan mempertahankan pengirim dan jenis tindakan, tanpa mengonversi setiap penghapusan menjadi pengunduran diri sukarela. Pembaruan peserta mentah mempertahankan actor_id sebagaimana disediakan. Cuplikan reaksi tidak menciptakan aktor perubahan.

Pemberitahuan penghapusan untuk obrolan pribadi dan grup biasa hanya berisi ID pesan. Obrolan-obrolan tersebut berbagi satu urutan ID yang berlaku untuk seluruh akun, sehingga sebuah ID mengidentifikasi satu pesan dari akun ini. Jika pesan dengan ID tersebut telah disimpan sebelumnya dalam jurnal ini, penghapusan tersebut dicatat dalam obrolan tersebut sebagai message.deleted dengan payload.chat_resolution sebagai nama metodenya. ID yang tidak pernah disimpan disimpan sebagai deletion.unscoped tanpa chat_id; tidak ada yang diperkirakan. Saluran dan supergrup menomori pesan per obrolan dan tidak pernah dicocokkan dengan cara ini. Ketika pesan yang dihapus dikirim oleh akun yang diamati, payload.deleted_message_was_outgoing bernilai true; pengirim pesan yang dihapus tetap tidak disebutkan.

## Cakupan: kontinuitas, celah, dan ID yang tidak terdeteksi

Setiap berkas ZIP yang ditandatangani berisi `coverage.json`, laporan HTML dibuka dengan ringkasan yang sama, dan `verify.py` menghitung ulang ringkasan tersebut dari `events.jsonl` alih-alih mempercayai berkas tersebut:

- **Terus diamati dari X hingga Y.** Sebuah periode dimulai dengan `observation.started` dan berakhir pada jeda, penghentian, koneksi Telegram terputus, logout, dimulainya proses tanpa penghentian yang teratur, atau lebih dari tiga menit tanpa catatan apa pun selama pengamatan (detak jantung dicatat setiap menit, sehingga keheningan berarti proses berhenti, macet, atau komputer dalam mode tidur). Ketika interval detak jantung diubah di **bagian Parameter**, setiap detak jantung akan mencatatnya dan durasi keheningan yang diperbolehkan menjadi tiga interval, tidak pernah kurang dari tiga menit.
- **Daftar celah** mencantumkan selang waktu antar periode beserta alasannya. Celah yang masih terbuka pada catatan terakhir ditandai dengan kode `not_resumed_by_last_record`.
- **ID pesan tidak terdeteksi.** Untuk saluran dan supergrup, yang menghitung jumlah pesan per obrolan, ID yang hilang di antara ID yang terdeteksi dicantumkan sebagai rentang. ID tersebut dilaporkan sebagai tidak*terdeteksi* — dihapus, tidak pernah terkirim, atau berada di luar riwayat yang tersimpan — bukan sebagai dihapus. Obrolan pribadi dan grup biasa menggunakan urutan ID yang sama untuk seluruh akun, sehingga celah di sana tidak berarti apa-apa dan tidak dicantumkan.
- Pemberitahuan celah pada tingkat obrolan (misalnya, Telegram meminta pemulihan perbedaan di satu saluran) dihitung sebagai catatan; pemberitahuan tersebut tidak mengganggu cakupan global.

Cakupan menjelaskan apa yang direkam oleh pengumpul ini. Hal ini bukan bukti bahwa Telegram mengirimkan setiap pembaruan selama periode yang berkelanjutan.

## Produser

Manifest yang ditandatangani dari berkas ZIP bukti, ekspor obrolan, jurnal saksi, dan pernyataan berkas profil pengguna berisi `producer` : perangkat lunak, versi, proyek (PhishDestroy), halaman utama, dan repositori sumber. Laporan HTML menampilkan baris yang sama, dan `verify.py` mencantumkannya sebagai bagian dari apa yang telah diverifikasi. Arsip yang dibuat sebelum bidang ini ada diverifikasi seperti sebelumnya dan dilaporkan sebagai tidak mencantumkan nama pembuat.

## Profil orang

File profil (`tgwitness-dossier-v1`, JSON) dibuat berdasarkan permintaan dari catatan yang sudah ada di jurnal untuk satu obrolan; tidak ada data yang diambil dari Telegram dan isi profil tidak pernah ditulis ke jurnal (mengaktifkan dan menonaktifkan profil dicatat sebagai `dossier.changed`). Untuk setiap orang dengan pesan yang disimpan, alat ini mencantumkan nama dan riwayat nama pengguna, status Telegram (bot, penipuan, palsu, premium, terverifikasi, dibatasi, dihapus) sebagaimana terlihat pada saat penyimpanan, foto identitas, SHA-256, dan hash perseptual (pHash, kompatibel dengan `imagehash.phash`) dari avatar yang diambil dari cache avatar lokal beserta avatar serupa, aktivitas (pesan pertama dan terakhir, jumlah, berbagi yang diedit dan dihapus, pesan per jam UTC), siapa yang membalas siapa, obrolan lain dalam jurnal ini di mana orang tersebut menulis, serta dompet yang disebutkan (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; alamat Base58Check telah diverifikasi checksum-nya), nomor telepon, nama pengguna, dan tautan, termasuk tautan yang tersembunyi di balik teks.

Setiap fakta mencantumkan catatan jurnal (`seq`) asalnya, dan `record_hashes` menyimpan hash dari setiap catatan yang dirujuk. Pernyataan tersebut ditandatangani dengan kunci ruang kerja:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

memeriksa tanda tangan, memverifikasi ekspor bukti itu sendiri (tanda tangan, rantai hash, dan berkas) serta memastikan setiap catatan yang dirujuk tetap ada tanpa perubahan dalam ekspor ruang kerja yang sama tersebut. Hash avatar diberi label sebagai berasal dari cache lokal (bukan catatan jurnal). Sebutan merupakan pencocokan pola — petunjuk untuk diperiksa, bukan fakta yang terverifikasi. Profil diaktifkan per obrolan, dapat diekspor sebagai ZIP AES-256 dengan kata sandi, dan dihapus saat dinonaktifkan atau saat obrolan dihapus dari sumber.

## Saksi independen

Jurnal saksi (`tgwitness-witness-v1`) dan postingan salurannya dicocokkan dengan ekspor bukti menggunakan `verify.py --witness … --channel …`; lihat [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/).

## Manifest dan titik pemeriksaan

manifest.json mencakup format, waktu ekspor, kunci publik, sidik jari, panjang jurnal, hash awal, cakupan, produsen, batasan, dan SHA-256 dari setiap anggota konten selain `manifest.json` dan `manifest.sig` itu sendiri. manifest.sig adalah tanda tangan base64 Ed25519 atas manifest JSON kanonik. Verifikator akan menolak anggota yang tidak terduga/hilang, nama yang duplikat, berkas yang rusak, urutan/rantai yang terputus, tanda tangan yang tidak valid, dan ketidaksesuaian dengan titik pemeriksaan yang disediakan. Verifikator tidak pernah mengekstrak jalur arsip. Verifikator membatasi ukuran total yang dinyatakan dalam keadaan tidak terkompresi hingga 4 GiB; ``--max-gib N`` memungkinkan arsip yang lebih besar yang dibuat dengan batas **Parameter** yang ditingkatkan.

Peroleh kode verifikator dari salinan yang telah diperiksa atau salinan independen yang telah ditinjau. Kode verifikator di dalam arsip yang tidak tepercaya merupakan materi yang dapat dieksekusi yang disediakan oleh pembuat arsip tersebut; keberadaannya hanya untuk kemudahan portabilitas, bukan sebagai jangkar kepercayaan independen.

Sebuah titik pemeriksaan (checkpoint) menandatangani pernyataan yang berisi kunci publik, panjang jurnal, hash awal, dan waktu pembuatan. Pihak verifikator dapat memeriksa apakah arsip yang dibuat kemudian mengandung awalan yang sama. Simpan titik pemeriksaan di luar pengumpul (collector) sebelum terjadi perubahan yang dipermasalahkan: seorang penyerang yang mengendalikan baik arsip maupun titik pemeriksaan dapat mengganti keduanya.

Tanda tangan yang valid dari kunci yang tidak disematkan hanya menjamin konsistensi internal. Bahkan kunci yang disematkan pun tidak dapat membuktikan kebenaran konten sumber jika pengumpul atau kuncinya telah disusupi sebelum perekaman. Penandaan waktu eksternal dan penangkapan data yang tepercaya merupakan persyaratan terpisah. TgWitness tidak menjamin kelayakan sebagai bukti atau sertifikasi forensik.

## Lampiran

File-file diidentifikasi berdasarkan SHA-256 di dalam direktori media/. Sebuah entri media.saved menghubungkan nilai hash dan panjang byte ke peristiwa pesan tertentu. Nama file mentah merupakan metadata, bukan jalur lokal. Byte media diunduh secara asinkron, sehingga penghapusan seketika dapat mencegah proses penangkapan data. Pengumpulan yang dinonaktifkan, berkas berukuran berlebihan/tidak diketahui, kegagalan unduhan, dan unduhan yang terputus akan ditampilkan sebagai hasil. Kerusakan proses dapat meninggalkan berkas parsial yang tidak terreferensikan; berkas-berkas tersebut tidak disertakan dalam ekspor.

Eksportir ZIP memverifikasi media yang disimpan berdasarkan namanya. Ekspor dalam format JSONL, CSV, dan HTML memverifikasi tanda tangan peristiwa tetapi tidak menyertakan byte media. Laporan turunan hanya sebagai kemudahan; events.jsonl adalah representasi peristiwa yang sah.

## Penyimpanan yang tahan lama dan tanda terima proses (0.2)

Sebuah tugas media dan pencatatan peristiwa pesannya dilakukan dalam satu transaksi. Tugas tersebut menyimpan deskriptor pesan TL asli; pengamatan yang ditandatangani mengikat SHA-256, akun, dan kebijakan ukurannya. Pemulihan memverifikasi pengikatan tersebut sebelum mengunduh. Tugas ini tidak pernah mengambil pesan saat ini dan secara diam-diam menggantinya dengan lampiran yang lebih baru. Tugas yang terputus akan dicoba ulang, sementara kegagalan permanen tetap menjadi hasil yang eksplisit.

Setiap ruang kerja memiliki jurnal dan identitas penandatanganan tersendiri. Peristiwa `process.started` mencakup ID eksekusi, waktu lokal, versi dependensi, hash berkas sumber, akun/ruang lingkup awal, serta pengaturan penangkapan. Sinyal detak jantung mencakup ID eksekusi, waktu monotonik, dan status antrian. Tanda terima proses juga dapat diunduh sebagai pernyataan yang ditandatangani secara terpisah. Pengukuran berkas dilaporkan sendiri dan bukan merupakan pengesahan perangkat keras yang tepercaya.

Titik pemeriksaan otomatis disimpan secara lokal saat startup, setiap lima menit selama proses pemantauan (**Parameter → Titik pemeriksaan yang ditandatangani setiap**), dan saat penghentian yang teratur. Verifikasi saat startup dan ekspor membandingkan jurnal dengan titik pemeriksaan lokal terbaru yang disimpan. Hal ini dapat mendeteksi rollback basis data jika titik pemeriksaan tersebut masih ada; seorang operator yang mengendalikan keduanya masih dapat mengganti keduanya. Penyimpanan independen dan cap waktu tepercaya eksternal tetap menjadi persyaratan terpisah.

Setelah restart, posisi pembaruan Telegram yang tersimpan dilanjutkan (`catch_up_from` di `observation.started`) dan pembaruan yang terlewat diminta. Pemeriksaan ulang berkala mencatat `message.recovered` untuk pesan yang terlewat dan `message.missing_on_recheck` ketika Telegram tidak lagi mengembalikan pesan yang tersimpan; yang terakhir ini bukan pemberitahuan penghapusan dan tidak menyebutkan nama penghapus atau waktunya.

### Penyalinan dan pemulihan di luar situs (S3)

Salinan di luar situs (Ekspor, dinonaktifkan secara default) mengunggah segmen jurnal, file yang disimpan, titik pemeriksaan bersama dengan cap waktunya, serta ekspor obrolan yang telah selesai ke penyimpanan yang kompatibel dengan S3, dienkripsi dengan AES-256-GCM sebelum diunggah menggunakan kunci yang disimpan di brankas ruang kerja; retensi Object Lock berlaku jika bucket mendukungnya. Tanpa kunci yang diunduh, salinan tersebut tidak dapat dibaca. Pulihkan dan verifikasi dengan `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Pemulihan memerlukan direktori biasa yang kosong. Unduhan dan objek yang telah didekripsi tetap berada di penyimpanan sementara pribadi hingga seluruh jurnal dan setiap titik pemeriksaan yang disimpan terverifikasi. Jalur objek yang tidak aman, rentang segmen yang tidak konsisten, dan jurnal yang lebih pendek dari titik pemeriksaan akan ditolak; verifikasi yang gagal tidak akan mempublikasikan file yang dipulihkan. Pemeriksaan retensi membandingkan mode Object Lock yang dikembalikan dan tanggalnya dengan batas waktu yang dikirim saat pengunggahan (toleransi pembulatan satu detik). Batas waktu yang telah kedaluwarsa, tidak valid, atau dipersingkat tidak dianggap terverifikasi. Status tersebut melaporkan objek yang diambil sampelnya yang retensinya dibaca kembali untuk proses pengunggahan tersebut.

Kemajuan penyalinan terbatas pada tujuan dan kunci enkripsi. Mengubah titik akhir, bucket, atau awalan akan memulai penyalinan lengkap jurnal, media, dan titik pemeriksaan yang disimpan secara lokal ke tujuan tersebut. Kemajuan lama yang tidak termasuk dalam cakupan tetap dipertahankan tetapi akan diputar ulang satu kali setelah pemutakhiran. Ekspor riwayat obrolan yang telah dihapus dari kotak keluar lokal tetap berada di tujuan sebelumnya.

Media lokal yang hilang atau rusak dilaporkan sebagai kesalahan pada tahap tersebut dan kursor media tetap berada di depan media tersebut, sehingga file tersebut akan dicoba lagi pada tahap berikutnya; file, titik pemeriksaan, dan ekspor setelahnya tetap disalin. Pemeriksaan pemulihan memverifikasi semua referensi media yang disimpan terhadap hash yang telah didekripsi dan ukuran yang tercatat. Segmen jurnal yang tumpang tindih dan identik dari unggahan yang terputus akan dihilangkan duplikatnya; tumpang tindih yang bertentangan akan ditolak. Titik pemeriksaan yang dibuat selama unggahan ditunda hingga catatan jurnal yang dicakupnya telah disalin, sehingga satu putaran yang telah selesai tidak akan menerbitkan titik pemeriksaan sebelum jurnalnya.

### Ekspor snapshot streaming

Ekspor streaming menggunakan snapshot baca SQLite yang stabil. Bagian awalnya mungkin lebih lama daripada jurnal langsung saat ini ketika pengunduhan selesai. Titik pemeriksaan yang dibuat setelah snapshot tersebut dapat melaporkan dengan benar bahwa arsip tersebut lebih pendek; bandingkan dengan titik pemeriksaan pada atau sebelum awalan yang diekspor, bukan titik pemeriksaan sembarang yang lebih baru.

## Persiapan RFC 3161 dan verifikasi respons (0.2)

Mode bukti (dinonaktifkan secara default) hanya mengirimkan SHA-256 dari setiap titik pemeriksaan yang ditandatangani ke otoritas RFC 3161 dan kalender OpenTimestamps yang terdaftar, melalui rute ruang kerja dan tidak pernah melalui MTProxy. Jawaban disimpan dalam `checkpoints/anchors/`, diekspor, dan diperiksa oleh `verify.py` (`--tsa-ca` memeriksa tanda tangan TSA; konfirmasi bukti OpenTimestamps dengan `ots upgrade` dan `ots verify`).

Panel ini menyiapkan arsip permintaan yang berisi byte checkpoint.json kanonik, jejak pesan SHA-256 dan nonce acak dalam timestamp.tsq, checksum, serta petunjuk. Tidak ada permintaan jaringan yang dilakukan. Persiapan ini bukanlah cap waktu yang tepercaya.

`python -m tgwitness.anchor verify` memanggil OpenSSL dua kali: sekali terhadap byte checkpoint dan sekali terhadap permintaan asli. File CA tepercaya diperlukan secara eksplisit; sertifikat yang disertakan tidak secara otomatis dipercaya. Pemeriksaan permintaan bersifat opsional di CLI, jadi pertahankan dan berikan opsi --request untuk memeriksa nonce. Hasilnya menyatakan apakah pemeriksaan telah dilakukan. Tanda tangan titik pemeriksaan pengumpul dan jurnal tetap harus diverifikasi secara terpisah dengan sidik jari pengumpul yang tepercaya.

Verifikator saat ini tidak mengambil informasi pencabutan atau menerapkan validasi arsip jangka panjang setelah sertifikat kedaluwarsa. Jangan menyamakan verifikasi tanda tangan yang berhasil dengan cap waktu yang memenuhi syarat atau kelayakan hukum. Sebuah TSA independen yang sesungguhnya belum dihubungi selama pengembangan. Lihat [prosedur](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/).
