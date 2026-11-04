# Format bukti

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/

Isi berkas ZIP yang telah ditandatangani, jenis catatan, tanda terima proses, profil pengguna, salinan di luar lokasi, dan verifikasi offline.

TgWitness melestarikan pengamatan Telegram yang terlihat di akun dalam jurnal yang ditandatangani. Penerima dapat memverifikasi catatan, lampiran, dan laporan yang disimpan dengan membandingkannya terhadap kunci pengumpul tepercaya, kemudian membandingkan jurnal tersebut dengan titik pemeriksaan yang disimpan secara independen. Halaman ini menjelaskan format, pemeriksaan, dan materi yang harus disimpan untuk penyerahan.

## Apa itu "ditandatangani"?

| Materi | Perlindungan | Apa yang perlu disimpan |
| --- | --- | --- |
| Setiap catatan dalam jurnal, termasuk peristiwa operasional | Rantai SHA-256 dan tanda tangan Ed25519 per peristiwa | `events.jsonl` asli, sidik jari kunci tepercaya, dan titik pemeriksaan yang disimpan |
| Isi berkas ZIP bukti | `manifest.sig` menandatangani manifes kanonik, yang mencantumkan hash dari berkas-berkas konten | File ZIP lengkap, termasuk manifes dan tanda tangannya |
| Lampiran yang disimpan | SHA-256 dan jumlah byte dalam peristiwa `media.saved` yang ditandatangani; hash berkas dalam manifes ZIP yang ditandatangani | Byte asli di dalam berkas ZIP yang telah diverifikasi |
| Checkpoint | Tanda tangan Ed25519 atas panjang jurnal, hash header, kunci publik, dan waktu pembuatan | Salinan independen yang disimpan sebelum adanya perubahan yang diperdebatkan |
| Bukti transaksi | Pengukuran pengumpul yang ditandatangani secara terpisah; juga disertakan dalam peristiwa `process.started` yang ditandatangani | Bukti penerimaan dan jurnal terkait; pengukuran dilaporkan sendiri |
| Laporan yang mudah dibaca: `report.html` dan bagian-bagiannya, `report.json`, `report.pdf`, `chat.pdf` | Satu segel Ed25519 per berkas pada isinya; PDF juga dilengkapi dengan tanda tangan standar PDF (lihat [Laporan yang dapat dibaca](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#readable-reports)) | Berkas sebagaimana diterima dan sidik jari kunci tepercaya; berkas ZIP yang dijelaskan di dalamnya |
| CSV mandiri | Tidak ada tanda tangan kriptografis yang berdiri sendiri; hash peristiwa saja tidak cukup | Gunakan salinan persis yang terdapat di dalam berkas ZIP yang telah diverifikasi untuk pemeriksaan integritas |
| Tangkapan layar, cetakan, atau berkas PDF yang dihasilkan oleh peramban | Tidak ada tanda tangan TgWitness pada hasil turunan | Simpan paket asli yang telah diverifikasi dan dokumentasikan bagaimana turunan tersebut dibuat |

Pengumpul memverifikasi tanda tangan jurnal sebelum menghasilkan setiap format ekspor. Laporan HTML dan PDF yang dapat dibaca memiliki segelnya sendiri; CSV mandiri diperiksa sebagai bagian dari ZIP yang ditandatangani. Pertahankan ZIP untuk mempertahankan byte lampiran dan manifest, serta titik pemeriksaan terpisah untuk membandingkan jurnal dengan batas waktu sebelumnya.

## Serah terima penyelidikan

1. Catat referensi kasus, operator, ID akun Telegram numerik, sumber yang dipilih, kebijakan pengumpulan, dan periode pengumpulan dalam catatan kasus Anda. TgWitness melestarikan pengamatan dan mendukung catatan serta pengumpulan yang tertaut ke sumber di [Case Board](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-board/). Simpan catatan transfer dan penyimpanan bersama materi kasus Anda. Periksa pengaturan pengumpulan yang dimaksud dengan [prosedur penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

Verifikasi yang berhasil menetapkan integritas relatif terhadap kunci pengumpul tepercaya dan batas yang dipertahankan. Lihat [ruang lingkup verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope) untuk asumsi kepercayaan dan [hasil validasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/) dari pemeriksaan yang dilakukan.

## Cuplikan serah terima

Sebuah berkas ZIP yang ditandatangani berisi seluruh jurnal ruang kerja. Ketika pengadilan, pengacara, atau unit penanganan pelanggaran hanya memerlukan beberapa obrolan, periode tertentu, atau orang-orang tertentu, **menu Ekspor → Ekstrak Serah Terima** akan menyiapkan salinan yang dipersempit (`tgwitness-handover-v1`) sesuai dengan aturan pengungkapan yang dipilih. Operator menyatakan tujuannya dan memilih obrolan, periode opsional (UTC), orang-orang yang terkait dengan ekstrak tersebut, apa yang terjadi pada orang lain (ditampilkan, diganti dengan nama samaran P01, P02… atau diabaikan ), teks pesan mana yang dipertahankan, lampiran dan foto profil mana yang disertakan, serta apakah nomor telepon dan alamat email dalam teks disamarkan. Tujuan dan aturan-aturan ini tercantum dalam manifes yang ditandatangani dan dalam laporan; jurnal mencatat "`handover.exported`" beserta akses yang menyiapkannya serta SHA-256 berkas tersebut, bukan isinya.

`verify.py` memeriksa ekstrak dengan dua cara. Rekaman yang ditampilkan tidak berubah diverifikasi sepenuhnya: isinya dibandingkan dengan hash-nya, tanda tangan Ed25519-nya, dan tautannya ke pendahulunya yang disertakan. Sebuah rekaman yang dipersingkat tetap mempertahankan hash dan tanda tangan aslinya, sehingga tanda tangan tersebut masih dapat diverifikasi, tetapi bidang-bidang yang disembunyikan tidak dapat dihitung ulang darinya; rekaman tersebut menyebutkan apa yang disembunyikan dan laporan menandainya. Manifes menyebutkan panjang jurnal dan bagian awal dengan tanda tangan pengumpul di atas bagian awal tersebut, serta menghitung jumlah rekaman yang dihilangkan; `coverage.json` menjelaskan obrolan yang dipilih. Nama-nama di dalam nama file tidak terdeteksi. Periksa kembali file akhir sebelum membagikannya: teks bebas, nama file, dan lampiran yang dipilih masih dapat mengidentifikasi orang. Simpan ZIP lengkap yang telah ditandatangani: ekstraknya merupakan pengungkapan, bukan pengganti.

## Laporan yang mudah dibaca

Bukti yang ditandatangani, serah terima, dan file ZIP obrolan berisi laporan HTML dan JSON yang dapat dibaca, serta PDF jika font yang diperlukan tersedia, dalam bahasa laporan yang dipilih. Setiap laporan disegel dengan kunci Ed25519 ruang kerja dan dapat diverifikasi secara terpisah: ` `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]``.

- `report.html` / `chat.html`: pernyataan penyegelan (`tgwitness-report-seal-v1`) menutup berkas dan menandatangani SHA-256 untuk setiap byte di depannya. Jurnal dan obrolan yang panjang dibagi menjadi bagian-bagian dengan ukuran yang dapat dikonfigurasi (Pengaturan Laporan, 500 hingga 100.000 catatan; 5.000 secara default): `records/records-0001.html` atau `messages/messages-0001.html`, masing-masing disegel dengan nomor, rentang, dan totalnya, serta dicantumkan bersama SHA-256-nya dalam manifes yang ditandatangani. Rangkaian sinyal detak jantung pengumpul ditampilkan sebagai satu baris kecuali jika Pengaturan Laporan mencantumkannya satu per satu.
- `report.json` (`tgwitness-report-json-v1`, kunci `format`, `report`, `seal`): segel tersebut menandatangani SHA-256 dari JSON kanonik dari `report`, sehingga fakta-fakta tersebut dapat dibaca oleh sistem dan skrip kasus dan pemilihan untuk perlindungan data dapat dilakukan darinya sementara berkas yang ditandatangani tetap utuh.
- `report.pdf` / `chat.pdf`: dokumen resmi untuk dicetak dan diarsipkan, ditandatangani dua kali pada byte yang sama, seluruh berkas kecuali nilai tanda tangan (`/ByteRange`). Tanda tangan standar PDF (`adbe.pkcs7.detached`, CMS dengan SHA-256 dan ECDSA P-256) menggunakan sertifikat penandatanganan dokumen yang diterbitkan sendiri yang disimpan di brankas ruang kerja; nomor seri subjeknya adalah sidik jari kunci Ed25519 . Segel Ed25519 terdapat di dalam CMS sebagai atribut yang tidak ditandatangani `2.25.240684792623320047764573196045913242332` dan menyebutkan sertifikat SHA-256 dengan `"content": "pdf-byte-range"`, sehingga kunci Ed25519 menjamin keaslian sertifikat tersebut. Pembaca PDF menunjukkan apakah berkas tersebut berubah setelah ditandatangani dan menganggap penandatangan tidak dikenal hingga sertifikat tersebut dipercaya; bandingkan sidik jari Ed25519 sebagai gantinya. PDF berbahasa Mandarin, Jepang, dan Korea memerlukan font di server (atau di `TGWITNESS_FONT_DIR`); tanpa font tersebut, berkas ZIP hanya berisi laporan HTML dan JSON saja.

Dalam saluran atau supergrup, Telegram menomori pesan 1, 2, 3… secara berurutan. Ekspor obrolan mencantumkan nomor pertama dan terakhir, jumlah yang ada, serta setiap rentetan nomor yang tidak ada dalam `message-ids.json` , manifes, dan header `chat.json` , serta menandai setiap celah di mana celah tersebut berada dalam transkrip. `verify.py` menghitung ulang nomor-nomor tersebut mulai dari `chat.json` . Nomor yang hilang adalah pesan yang tidak dikembalikan oleh Telegram (dihapus sebelum ekspor, atau tidak terlihat oleh akun); dalam obrolan pribadi dan grup dasar, nomor-nomor tersebut dibagikan di semua obrolan akun tersebut dan celah tidak dihitung.

Setelah membaca riwayat, ekspor tersebut meminta Telegram untuk setiap nomor yang tidak ada lagi, berdasarkan nomor (`channels.getMessages`, hingga 10.000 nomor). Hasilnya terdapat di `message-ids.json` dan dalam laporan. Jawaban kosong berarti Telegram tidak memiliki pesan dengan nomor tersebut untuk akun ini; hal ini tidak menunjukkan apakah pesan tersebut telah dihapus atau memang tidak pernah terlihat oleh akun tersebut. Pesan Telegram yang dikembalikan berarti terlewatkan saat pembacaan dan ditambahkan ke ekspor, ditandai sebagai `found_on_recheck`.

Setiap laporan diawali dengan **. Singkatnya**: satu paragraf, kemudian apa yang ditunjukkan oleh materi tersebut dan apa yang tidak ditunjukkan (siapa di balik suatu akun, kelengkapan pengiriman, penghapusan sebelum pemantauan, waktu tanpa cap waktu). Stempel segel pada halaman tersebut berubah menjadi kuning ketika browser telah memeriksa tanda tangan segel tersebut, bukan halaman itu sendiri: browser tidak memberikan byte-nya sendiri kepada halaman. Stempel tersebut berubah menjadi hijau hanya ketika pembaca memasukkan berkas ke dalam pemeriksaan di bagian akhir halaman dan setiap byte cocok, serta hanya jika halaman yang ditampilkan adalah berkas tersebut; jika tidak, stempel berubah menjadi merah.

Setiap laporan menyebutkan nama program secara tepat: commit Git saat pengumpul berjalan dari checkout atau penginstal menetapkan `TGWITNESS_COMMIT`, serta SHA-256 dari berkas sumbernya (`source_tree_sha256`, JSON kanonik dari jalur → SHA-256 dari setiap berkas `.py`, `.js`, `.css`, `.html`, dan `.svg` dalam paket), yang direproduksi oleh checkout dari commit tersebut kecuali jika berkas-berkas tersebut telah diubah. Telegram klien dinamai berdasarkan perpustakaannya, lapisan API, dan pusat datanya. Saat pemantauan dimulai dan saat ekspor obrolan dimulai serta diakhiri, pengumpul meminta waktu dari Telegram (`updates.getState`, dalam detik penuh) dan mencatat waktu Telegram dikurangi waktu jam pengumpul, dengan ketidakpastian akibat perjalanan bolak-balik; laporan menampilkan pengukuran ini di bawah Rantai Pengawasan. Ekspor obrolan juga mencatat waktu saat riwayat dibaca, selain tanggal pesan-pesan tersebut.

### Panduan penampil laporan dan arsip offline

Ekstrak ZIP secara lengkap sebelum membuka `chat.html` atau `report.html`. Penampil menyediakan fitur pencarian, filter, peserta, indikator, detail rekaman, serta pilihan JSON/CSV tanpa memerlukan server. Simpan `viewer/` dan `media/` di samping laporan. Pilihan-pilihan tersebut merupakan turunan: gunakan `verify.py SELECTION.json
--evidence ARCHIVE.zip` untuk membandingkannya dengan arsip yang ditandatangani. Verifikator memeriksa ID laporan, kunci penandatanganan, batas arsip, dan setiap item yang dipilih; item yang diedit, hilang, dan duplikat akan ditolak. Catatan pemilihan dan waktu pembuatan tetap menjadi metadata yang tidak ditandatangani.

Kesenjangan nomor pesan hanya ditampilkan untuk umpan obrolan yang lengkap, tidak difilter, dan disusun secara ascending. Menyembunyikan suatu kategori atau kegagalan memuat potongan data tidak boleh mengubah baris yang dihilangkan menjadi bukti adanya pesan yang hilang . Penyorotan pencarian diterapkan pada teks biasa sebelum proses escaping HTML, dengan mempertahankan markup literal.

Browser ini memeriksa tanda tangan manifest, ID laporan dan kuncinya, serta semua hash file yang tercantum. Browser ini menolak struktur ZIP yang ambigu atau tidak valid, nama yang duplikat, dan jalur yang tidak aman, serta membatasi ukuran file hingga 256 MiB dan total isi yang dinyatakan hingga 4 GiB. Gunakan verifikator mandiri untuk arsip yang lebih besar. Pemeriksaan browser ini melengkapi pemeriksaan verifikator terhadap rantai jurnal dan semantik data.

`README.txt` berisi panduan awal, inventaris berkas yang disesuaikan, petunjuk verifikasi, dan catatan format data dalam bahasa laporan, diikuti dengan panduan lengkap dalam bahasa Inggris. `SHA256SUMS` mencakup file-file yang tercantum di dalamnya, tidak termasuk file itu sendiri, `manifest.json`, dan `manifest.sig`; manifest yang ditandatangani juga mencakup `SHA256SUMS`. Pertahankan ZIP asli tanpa perubahan dan simpan file kerja di luar folder yang diekstrak. Laporan PDF mencakup penanda bagian dan identifikasi kasus/laporan pada halaman-halaman selanjutnya.

### Percakapan pada saat ekspor

Ekspor obrolan mencatat apa yang dikatakan Telegram tentang obrolan tersebut saat ekspor dimulai: label milik Telegram sendiri (`scam`, `fake`, `restricted` beserta alasannya, `verified`), nama pengguna, deskripsi, jumlah anggota dan admin, diskusi yang tertaut, perlindungan konten, apakah anggota baru dapat melihat pesan sebelumnya dan mulai dari pesan mana akun ini dapat melihat riwayat (`available_min_id`), tanggal pesan pertama saat obrolan tersebut dibuat, dan SHA-256 foto obrolan (disimpan di `media/`). Data ini mencatat posisi akun yang mengekspor dalam obrolan: peran, tanggal bergabung, siapa yang mengundangnya, dan, bagi seorang admin, hak aksesnya. Permintaan yang ditolak oleh Telegram akan disebutkan sebagai gantinya.

Jika akun yang melakukan ekspor adalah admin, ekspor tersebut akan membaca log admin obrolan (Telegram menyimpan data selama sekitar 48 jam) ke dalam `admin-log.json`: penghapusan dan pengeditan beserta isinya serta akun yang melakukannya. Ini adalah satu-satunya catatan penghapusan yang menyebutkan siapa yang menghapusnya.

### Indikator

Daftar laporan, dan arsip tersebut berisi `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) serta `indicators.misp.json` (peristiwa MISP ), yang dapat ditindaklanjuti oleh bagian penanganan penyalahgunaan dalam pesan yang terekam: tautan dan domain (termasuk yang tersembunyi di balik teks, di tombol, dan di pratinjau tautan), alamat mata uang kripto, nama pengguna dan tautan undangan Telegram , nomor telepon, alamat email, serta gambar yang disimpan. Alamat Bitcoin, Litecoin, Dogecoin, dan TRON hanya dicantumkan jika checksum base58-nya valid, alamat SegWit jika checksum bech32 atau bech32m-nya valid, dan alamat TON jika CRC-nya valid; alamat EVM dan Solana ditandai sebagai belum diperiksa. Gambar disertai SHA-256 dan hash perseptual (dHash, 64 bit) yang tetap hampir tidak berubah pada salinan yang dikompres ulang atau diubah ukurannya. Laporan mencatat indikator agar tidak terbuka secara tidak sengaja (`hxxps[://]example[.]com` ); berkas-berkas tersebut mempertahankan nilai-nilai sebagaimana adanya. Setiap indikator ditandai sebagai tidak dikenal dan tidak untuk deteksi otomatis (STIX , `indicator_types: unknown` , MISP , `to_ids: false` , distribusi ke organisasi sendiri): tercantumnya indikator tersebut menunjukkan bahwa pesan tersebut mengandung indikator tersebut, bukan berarti indikator tersebut berbahaya. Tautan yang teksnya menampilkan alamat yang berbeda dari yang sebenarnya dibuka ditandai dalam laporan.

Laporan PDF diakhiri dengan pernyataan pemeriksa yang harus ditandatangani secara manual, daftar periksa untuk notaris atau ahli pengadilan, serta kode QR (juga terdapat di halaman pertama) yang berisi ID laporan, sidik jari kunci, dan SHA-256 dari data otoritatif, sehingga cetakan laporan tersebut dapat dilacak kembali ke arsipnya.

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

Ketika Telegram berhenti menerima akun tersebut, catatan `coverage.gap` yang mengakhiri pemantauan mengandung `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended`, atau `not_authorized`) dan Telegram kesalahan; `verify.py` menyebutkan penyebab di mana periode tersebut berakhir.

Cakupan menjelaskan apa yang direkam oleh pengumpul ini. Hal ini bukan bukti bahwa Telegram mengirimkan setiap pembaruan selama periode yang berkelanjutan.

## Produser

Manifest yang ditandatangani dari berkas ZIP bukti, ekspor obrolan, jurnal saksi, dan pernyataan berkas profil pengguna berisi `producer` : perangkat lunak, versi, proyek (PhishDestroy), halaman utama, dan repositori sumber. Laporan HTML menampilkan baris yang sama, dan `verify.py` mencantumkannya sebagai bagian dari apa yang telah diverifikasi. Arsip yang dibuat sebelum bidang ini ada diverifikasi seperti sebelumnya dan dilaporkan sebagai tidak mencantumkan nama pembuat.

Setiap catatan `observation.started` juga menyebutkan klien Telegram yang melakukan pemantauan: `api_id`-nya (bukan hash-nya), apakah itu pasangan publik bawaan atau aplikasi milik operator, deskripsi klien yang dikirim dalam permintaan koneksi Telegram, serta jenis rute koneksi dengan mode IP (tanpa alamat proxy atau rahasia). Laporan dan `custody.json` mencantumkan setiap klien dan rute yang berbeda beserta waktu perekamannya, serta waktu-waktu ketika tidak ada proxy yang terdaftar yang merespons dan Telegram mendeteksi alamat server. Jurnal yang direkam sebelum ini menyatakan hal tersebut.

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

## Ruang lingkup verifikasi

Tanda tangan tersebut mengidentifikasi kunci pengumpul dan melindungi materi yang disimpan. Tetapkan sidik jarinya secara independen untuk mengaitkan kunci tersebut dengan pengumpul yang diharapkan. Pembaruan Telegram merupakan masukan untuk pengumpulan; TgWitness menandatangani pengamatannya terhadap pembaruan tersebut. Tanda tangan tersebut bukanlah tanda tangan yang dikeluarkan oleh Telegram atau oleh penulis pesan.

Titik pemeriksaan yang disimpan atau catatan saksi mendeteksi perubahan awalan jurnal sebelumnya, termasuk penggantian yang ditandatangani dengan kunci pengumpul yang disalin. Catatan yang dibuat sebelum titik pemeriksaan independen pertama mereka memerlukan penguatan sumber: pemegang kunci pengumpul dapat menandatangani materi baru. Jaga agar akses kunci penandatanganan tetap terkendali dan simpan referensi secara terpisah.

Nilai visibilitas akun dan pengiriman menggunakan catatan cakupan dan pengujian terkontrol. Gunakan cap waktu eksternal yang terverifikasi untuk penandaan waktu independen. ID pengirim mengidentifikasi akun Telegram; hubungkan ID tersebut dengan seseorang melalui penyelidikan Anda. Tanda terima program dan pemeriksaan cloud menjelaskan pengukuran yang dilaporkan oleh pengumpul serta konfigurasi penerapan. Lihat [hasil validasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/) untuk perilaku yang diukur dan cakupannya.

## Lampiran

File-file diidentifikasi berdasarkan SHA-256 di dalam direktori media/. Sebuah entri media.saved menghubungkan nilai hash dan panjang byte ke peristiwa pesan tertentu. Nama file mentah merupakan metadata, bukan jalur lokal. Byte media diunduh secara asinkron, sehingga penghapusan seketika dapat mencegah proses penangkapan data. Pengumpulan yang dinonaktifkan, berkas berukuran berlebihan/tidak diketahui, kegagalan unduhan, dan unduhan yang terputus akan ditampilkan sebagai hasil. Kerusakan proses dapat meninggalkan berkas parsial yang tidak terreferensikan; berkas-berkas tersebut tidak disertakan dalam ekspor.

Eksportir ZIP memverifikasi media yang disimpan berdasarkan namanya. Ekspor dalam format JSONL, CSV, dan HTML memverifikasi tanda tangan peristiwa tetapi tidak menyertakan byte media. Laporan turunan hanya sebagai kemudahan; events.jsonl adalah representasi peristiwa yang sah.

Ekspor obrolan lengkap menyimpan lampiran sesuai pengaturan lampiran ruang kerja ke dalam media/, dengan nama SHA-256. Setiap catatan pesan dalam chat.json mencantumkan nama berkasnya (`file`, `file_sha256`) atau alasan ketidakhadirannya (`file_status`), beserta apa yang dilihat pembaca di sekitar teks: tautan di balik teks, asal penerusan, tombol bot, tanda tangan, jumlah tampilan, dan pengatur waktu penghapusan otomatis. `verify.py` memeriksa apakah setiap berkas yang disebutkan terdapat dalam manifes yang ditandatangani di bawah hash tersebut.

## Penyimpanan yang tahan lama dan tanda terima proses (0.2)

Sebuah tugas media dan pencatatan peristiwa pesannya dilakukan dalam satu transaksi. Tugas tersebut menyimpan deskriptor pesan TL asli; pengamatan yang ditandatangani mengikat SHA-256, akun, dan kebijakan ukurannya. Pemulihan memverifikasi pengikatan tersebut sebelum mengunduh. Tugas ini tidak pernah mengambil pesan saat ini dan secara diam-diam menggantinya dengan lampiran yang lebih baru. Tugas yang terputus akan dicoba ulang, sementara kegagalan permanen tetap menjadi hasil yang eksplisit.

Setiap ruang kerja memiliki jurnal dan identitas penandatanganan tersendiri. Peristiwa `process.started` mencakup ID eksekusi, waktu lokal, versi dependensi, hash berkas sumber, akun/ruang lingkup awal, serta pengaturan penangkapan. Sinyal detak jantung mencakup ID eksekusi, waktu monotonik, dan status antrian. Tanda terima proses juga dapat diunduh sebagai pernyataan yang ditandatangani secara terpisah. Pengukuran berkas dilaporkan sendiri dan bukan merupakan pengesahan perangkat keras yang tepercaya.

Titik pemeriksaan otomatis disimpan secara lokal saat startup, setiap lima menit selama proses pemantauan (**Parameter → Titik pemeriksaan yang ditandatangani setiap**), dan saat penghentian yang teratur. Verifikasi saat startup dan ekspor membandingkan jurnal dengan titik pemeriksaan lokal terbaru yang disimpan. Hal ini dapat mendeteksi rollback basis data jika titik pemeriksaan tersebut masih ada; seorang operator yang mengendalikan keduanya masih dapat mengganti keduanya. Penyimpanan independen dan cap waktu tepercaya eksternal tetap menjadi persyaratan terpisah.

Setelah restart, posisi pembaruan Telegram yang tersimpan dilanjutkan (`catch_up_from` di `observation.started`) dan pembaruan yang terlewat diminta. Pemeriksaan ulang berkala mencatat `message.recovered` untuk pesan yang terlewat dan `message.missing_on_recheck` ketika Telegram tidak lagi mengembalikan pesan yang tersimpan; yang terakhir ini bukan pemberitahuan penghapusan dan tidak menyebutkan nama penghapus atau waktunya.

### Penyalinan dan pemulihan di luar situs (S3)

Salinan di luar situs (Ekspor, dinonaktifkan secara default) mengunggah segmen jurnal, file yang disimpan, titik pemeriksaan bersama dengan cap waktunya, serta ekspor obrolan yang telah selesai ke penyimpanan yang kompatibel dengan S3, dienkripsi dengan AES-256-GCM sebelum diunggah menggunakan kunci yang disimpan di brankas ruang kerja; retensi Object Lock berlaku jika bucket mendukungnya. Tanpa kunci yang diunduh, salinan tersebut tidak dapat dibaca. Pulihkan dan verifikasi dengan `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Pemulihan memerlukan direktori biasa yang kosong. Unduhan dan objek yang telah didekripsi tetap berada di penyimpanan sementara pribadi hingga seluruh jurnal dan setiap titik pemeriksaan yang disimpan terverifikasi. Jalur objek yang tidak aman, rentang segmen yang tidak konsisten, dan jurnal yang lebih pendek dari titik pemeriksaan akan ditolak; verifikasi yang gagal tidak akan mempublikasikan file yang dipulihkan. Pemeriksaan retensi membandingkan mode Object Lock yang dikembalikan dan tanggalnya dengan batas waktu yang dikirim saat pengunggahan (toleransi pembulatan satu detik). Batas waktu yang telah kedaluwarsa, tidak valid, atau dipersingkat tidak dianggap terverifikasi. Status tersebut melaporkan objek yang diambil sampelnya yang retensinya dibaca kembali untuk proses pengunggahan tersebut.

Media lokal yang hilang atau rusak dilaporkan sebagai kesalahan pada tahap tersebut dan kursor media tetap berada di depan media tersebut, sehingga file tersebut akan dicoba lagi pada tahap berikutnya; file, titik pemeriksaan, dan ekspor setelahnya tetap disalin. Pemeriksaan pemulihan memverifikasi semua referensi media yang disimpan terhadap hash yang telah didekripsi dan ukuran yang tercatat. Segmen jurnal yang tumpang tindih dan identik dari unggahan yang terputus akan dihilangkan duplikatnya; tumpang tindih yang bertentangan akan ditolak. Titik pemeriksaan yang dibuat selama unggahan ditunda hingga catatan jurnal yang dicakupnya telah disalin, sehingga satu putaran yang telah selesai tidak akan menerbitkan titik pemeriksaan sebelum jurnalnya.

### Ekspor snapshot streaming

Ekspor streaming menggunakan snapshot baca SQLite yang stabil. Bagian awalnya mungkin lebih lama daripada jurnal langsung saat ini ketika pengunduhan selesai. Titik pemeriksaan yang dibuat setelah snapshot tersebut dapat melaporkan dengan benar bahwa arsip tersebut lebih pendek; bandingkan dengan titik pemeriksaan pada atau sebelum awalan yang diekspor, bukan titik pemeriksaan sembarang yang lebih baru.

## Persiapan RFC 3161 dan verifikasi respons (0.2)

Mode bukti (dinonaktifkan secara default) hanya mengirimkan SHA-256 dari setiap titik pemeriksaan yang ditandatangani ke otoritas RFC 3161 dan kalender OpenTimestamps yang terdaftar, melalui rute ruang kerja dan tidak pernah melalui MTProxy. Jawaban disimpan dalam `checkpoints/anchors/`, diekspor, dan diperiksa oleh `verify.py` (`--tsa-ca` memeriksa tanda tangan TSA; konfirmasi bukti OpenTimestamps dengan `ots upgrade` dan `ots verify`).

Panel ini menyiapkan arsip permintaan yang berisi byte checkpoint.json kanonik, jejak pesan SHA-256 dan nonce acak dalam timestamp.tsq, checksum, serta petunjuk. Tidak ada permintaan jaringan yang dilakukan. Persiapan ini bukanlah cap waktu yang tepercaya.

`python -m tgwitness.anchor verify` memanggil OpenSSL dua kali: sekali terhadap byte checkpoint dan sekali terhadap permintaan asli. File CA tepercaya diperlukan secara eksplisit; sertifikat yang disertakan tidak secara otomatis dipercaya. Pemeriksaan permintaan bersifat opsional di CLI, jadi pertahankan dan berikan opsi --request untuk memeriksa nonce. Hasilnya menyatakan apakah pemeriksaan telah dilakukan. Tanda tangan titik pemeriksaan pengumpul dan jurnal tetap harus diverifikasi secara terpisah dengan sidik jari pengumpul yang tepercaya.

Verifikasi memeriksa tanda tangan respons, byte titik pemeriksaan, dan, jika disediakan, permintaan asli di bawah kepercayaan CA yang ditentukan. Pemeriksaan pencabutan dan validasi pengarsipan jangka panjang setelah sertifikat kedaluwarsa berada di luar cakupan verifikator saat ini. Lihat [prosedur](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/) dan [hasil validasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/).

## Catatan opsional dalam mode bukti: perangkat drand dan Telegram

Dua catatan tambahan dapat dijalankan pada proses yang sama dengan cap waktu. Keduanya dinonaktifkan secara default dan hanya berlaku saat mode bukti diaktifkan: Ekstra → Bukti & cadangan → **Saksi tambahan · opsional**, atau `"drand": true` dan `"devices": true` di `POST /api/evidence`. Kegagalan pada salah satunya tidak menghentikan yang lain atau penanda waktu; panel menampilkan hasil terbaru masing-masing di bawah formulir.

**drand** (`beacon.drand` ). Setiap putaran menulis putaran terbaru drand quicknet, yaitu keacakan publik dari League of Entropy (satu putaran setiap 3 detik), ke dalam jurnal: `chain` , `round` , `randomness` , `signature` , `round_time` , dan `relay` yang merespons. Putaran yang terverifikasi dan tidak dapat diprediksi menyediakan referensi waktu bawah untuk materi yang tertaut melalui hash berikutnya. Cap waktu terverifikasi pada titik pemeriksaan berikutnya memberikan referensi waktu atas. Pemeriksaan ini membatasi materi yang tertaut; cakupan pengumpulan dinilai secara terpisah. Pengumpul meminta `drand.cloudflare.com` terlebih dahulu, kemudian relai Protocol Labs, melalui rute ruang kerja, satu permintaan per putaran.

`verify.py` memeriksa apakah setiap nilai acak merupakan SHA-256 dari tanda tangannya dan apakah waktu putaran sudah tepat, serta melaporkan jumlah putaran, rentang terpanjang tanpa putaran, dan seberapa jauh ketinggalan jam pengumpul dari drand. Alat ini tidak memeriksa tanda tangan BLS. `--check-drand` membandingkan putaran dengan relai Cloudflare dan relai Protocol Labs, baik semuanya maupun sampel acak sebanyak 100 dalam jurnal panjang; putaran yang berbeda akan gagal dalam verifikasi.

Perangkat **, Telegram,**, dan `account.devices`. Setiap proses membaca sesi akun dengan `account.getAuthorizations`, daftar yang ditampilkan Telegram di Pengaturan → Perangkat, dan mencatatnya: secara lengkap jika terjadi perubahan sejak putaran sebelumnya, beserta hash sesi `added` dan `removed`, jika tidak, hanya jumlahnya dan SHA-256 yang dicatat. Model perangkat, platform, aplikasi, dan versi, waktu pembuatan dan aktivitas terakhir, negara, serta wilayah disimpan; alamat IP tidak disimpan, karena ekspor bukti berada di luar kendali Anda. Sesi pengumpul itu sendiri aktif sepanjang waktu, sehingga hanya aktivitas sesi lain yang dihitung sebagai perubahan. `verify.py` melaporkan seberapa sering daftar tersebut direkam serta setiap sesi baru dan yang telah berakhir. Ia hanya membaca daftar tersebut selama proses pengamatan berlangsung.

Apa yang tidak mereka tunjukkan: drand hanya membuktikan urutan catatan berdasarkan waktu publik, dan daftar perangkat merupakan pernyataan Telegram melalui pengumpul, yang ditandatangani oleh pengumpul seperti halnya setiap catatan lainnya.

**Log Cloudflare Gateway** (`cloudflare.gateway_dns`). Untuk server yang melakukan resolusi melalui Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), setiap salinan menyalin apa yang dicatat Gateway sejak salinan sebelumnya: satu catatan per jendela waktu maksimal tiga jam dengan `from`, `until`, `location_id`, `address` server jika ada, dan `queries` sebagai `[at, name, type, rcode, decision, colo]`, bahkan jika tidak ada. Atur di bawah **(log Cloudflare Gateway)**: akun, lokasi, alamat opsional, dan token baca-saja (Pembacaan Analytics Read; Zero Trust PII Read untuk menyimpan satu alamat dari lokasi bersama). Panel ini memeriksa data tersebut dengan satu permintaan sebelum menyimpannya; token tetap terenkripsi dan tidak pernah masuk ke jurnal. `verify.py` mencantumkan jendela, nama yang paling sering dicari, dan waktu apa pun yang tidak tercakup oleh salinan; catatan yang jumlahnya tidak sesuai dengan kuerinya akan gagal. Jendela yang menampung lebih dari satu halaman kueri dalam satu detik akan menyimpan halaman tersebut dan menyatakan sisanya hilang. Salinan tersebut merupakan tanggapan Cloudflare melalui pengumpul, yang ditandatangani oleh pengumpul; dalam waktu 24 jam, siapa pun yang memiliki token baca-saja dapat membandingkannya dengan Cloudflare.
