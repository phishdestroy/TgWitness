# Referensi Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/case-board/

Bookmark, sorotan tepat, potongan tindakan, diskusi, akses terbatas, dan riwayat anotasi yang ditandatangani yang digunakan oleh Case Board.

Case Board memberikan tim investigasi tampilan kerja bersama atas materi yang disimpan. Tandai sebuah pengamatan, sorot bagian tertentu, simpan serangkaian tindakan, dan diskusikan dengan rekan kerja. Kartu-kartu tersebut mempertahankan referensi sumber dan riwayat revisi yang ditandatangani. Anotasi tim tetap berada di ruang kerja, dan dapat dibedakan secara terpisah dari pengamatan Telegram asli.

[Model bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/) · [Akses](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) · [Laporan](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/) · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/CASE-BOARD.md)

![Umpan investigasi sintetis](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Bekerja dengan suatu kasus

Buka **Investigasi → Case Board** dalam mode Standar atau Ahli. Bahasa yang digunakan mengikuti panel. Gunakan **tombol** **"To board"** di samping catatan jurnal atau pesan obrolan yang disimpan, atau sorot dan tekan **B**. Penanda akan ditambahkan ke Kotak Masuk dengan satu klik. Edit judul, label, dan catatannya, atau pindahkan ke koleksi. Kartu yang diubah akan menyertakan revisi yang ditandatangani; menghapusnya akan mempertahankan riwayatnya.

Untuk kasus pertama, pilih pengumpulan data dan tambahkan catatan yang menjawab satu pertanyaan. Gunakan komentar untuk meninjau interpretasi, lalu gunakan **Presentation** untuk menelusuri kartu dan konteks sumber. Pilih materi Case Board secara terpisah di [Report Studio](https://phishdestroy.github.io/TgWitness/id/docs/reference/case-reports/) saat menyiapkan hasil akhir. Menyimpan potongan data tidak secara otomatis mengonfigurasi filter data laporan.

Pilih teks di dalam pesan obrolan yang disimpan untuk menampilkan **Highlight → board**. Pilih warnanya dan tambahkan catatan. Server memeriksa kutipan yang tepat dan versi yang disimpan, termasuk emoji, teks RTL, dan tanda penggabungan. Antarmuka tidak memetakan pilihan melalui teks yang disamarkan atau diubah.

Tekan Shift sambil mengklik dua catatan dalam satu obrolan untuk **memotong (Slice) di antara keduanya**, gunakan **Slice berdasarkan waktu**, atau simpan filter obrolan saat ini, periode, dan jenis peristiwa di Journal. Potongan yang disimpan memiliki predikat otoritatif sendiri: membukanya di Journal juga menerapkan filter obrolan ganda, batas jumlah pesan, dan filter aktor. **Tampilkan catatan yang ditambahkan sejak penanda** mengisolasi penambahan-penambahan selanjutnya. Mengubah filter Journal akan keluar dari potongan tersebut. Dari People, **Potong tindakan orang ini** menggunakan ID pelaku yang tercatat; fitur ini tidak mengasumsikan bahwa penulis pesan telah mengedit, menghapus, atau bereaksi terhadap sebuah pesan.

Kotak dialog "slice" menampilkan pratinjau jumlah sebelum mengizinkan pembuatan. "`all`" mencakup semua jenis data yang direkam, termasuk tangkapan layar, pengeditan, penghapusan, reaksi, pembaruan keanggotaan/layanan, tindakan sendiri, tombol, hasil media, pesan yang dipulihkan, dan jenis peristiwa di masa depan. Pilihan ini menggambarkan pengamatan yang disimpan. Pemberitahuan penghapusan obrolan yang tidak dikenal merupakan konteks terpisah, hanya tersedia bagi pengguna dengan akses ke seluruh ruang kerja, dan tidak pernah dikaitkan dengan salah satu obrolan yang dipilih.

Koleksi memiliki cakupan obrolan yang ditentukan. Cakupan kosong berarti seluruh ruang kerja. Sebuah koleksi tidak dapat berisi kartu di luar cakupannya; peserta yang dibatasi obrolan tidak dapat membaca koleksi yang lebih luas. Kotak masuk adalah koleksi virtual untuk kartu yang belum ditugaskan. Pencarian dan filter hanya mencakup kartu yang terlihat; utas dan sebutan mewarisi akses dari kartu induknya. Komentar yang dihapus memiliki tanda penghapusan dalam diskusi. Riwayat penampil tidak dicatat.

**Presentasi** membuka semua kartu dalam koleksi yang dipilih, dengan tampilan Kartu, Konteks Sumber, dan Komentar Tim, serta kontrol keyboard Sebelumnya/Berikutnya. Fitur ini tidak menyediakan kontrol pengeditan. Umpan biasa dibagi menjadi beberapa halaman; presentasi memuat daftarnya per halaman dan menampilkan detail satu kartu pada satu waktu.

## Izin

Semua operasi memerlukan akses ke `view`, ruang kerja/ruang obrolan, dan `board.read`. `board.write` menambahkan kartu, komentar, memindahkan, serta mengubah status menjadi "terbuka" atau "telah ditinjau". `board.manage` memungkinkan pengelolaan koleksi, status "dikonfirmasi" atau "ditolak", serta revisi atau penghapusan kartu milik orang lain. Status merupakan keputusan tim, bukan hasil verifikasi kriptografis.

Akses preset formulir: Peninjau = baca; Analis = baca/tulis; Operator = baca/tulis/kelola, selain izin yang sudah ada. Pemberian izin yang sudah ada tidak secara otomatis memperoleh hak baru. Administrator utama memiliki semua hak akses, dan memposting sebagai **Administrator Utama**. Gunakan pemberian hak akses berlabel untuk atribusi. Daftar penyebutan hanya mencakup akses saat ini yang dapat membaca kartu induk secara lengkap.

Sebuah izin untuk obrolan A tidak dapat memperoleh kartu atau potongan untuk A+B, bahkan dengan menebak ID-nya atau memberikan `target.chat_id` palsu. Metadata target diselesaikan dari hash peristiwa yang ditandatangani di server. Koleksi, jumlah diskusi, kartu terkait, dan pemberitahuan langsung disaring sebelum respons. exportasi memerlukan izin `export` serta `board.read`; eksportir yang sudah ada tanpa akses ke papan akan mendapatkan arsip bukti biasa tanpa catatan tim. SSE memeriksa kembali izin yang berlaku sebelum setiap batch.

## Kontrak yang disimpan

Seperti pengamatan, anotasi ditulis secara transaksional ke tabel SQLite yang hanya dapat ditambahkan (append-only) di ruang kerja. `annotations.jsonl` adalah ekspor kanonik persisnya dari snapshot baca yang sama dengan `events.jsonl`. Tidak ada penyimpanan anotasi lain yang bersaing dan tidak ada peristiwa jurnal `board.activity`.

Setiap baris harus berisi tepat:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

Contoh singkat di atas menggambarkan "envelope"; muatan sebenarnya mencakup nilai default model mereka dan bidang target yang diselesaikan oleh server. Skema permintaan API terdapat di [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), dihasilkan dari model Pydantic waktu berjalan oleh skrip `python tools/build_board_schemas.py`. Bidang permintaan tambahan akan ditolak. ID dihasilkan di sisi server jika diabaikan. Keterangan penulis, waktu, snapshot, dan tanda tangan tidak dapat disediakan oleh pemanggil. ID pemberian yang diberi nama mengikuti format 16-heksadesimal yang sudah ada di Access; ID kartu berformat 32-heksadesimal.

JSON kanonik menggunakan UTF-8, kunci objek diurutkan, tanpa spasi di antara token, Unicode tanpa escaping, dan tanpa NaN/tak terhingga. Hash anotasi adalah SHA-256 dari objek kanonik yang berisi `format: "tgwitness-annotations-v1"` dan ketujuh bidang envelope hingga `previous_hash`. Tag format ini memisahkan domain hash-nya dari pengamatan. Tanda tangan menggunakan Ed25519 atas 32 byte hash mentah. Urutan dimulai dari 1. Revisi mempertahankan ID kartu dan menyebutkan hash anotasi sebelumnya dalam "`supersedes`"; revisi tidak dapat mengubah cakupan obrolan. Pemindahan, status, dan penghapusan merupakan catatan terpisah. Tabel SQLite menolak perintah UPDATE dan DELETE.

`case-board.json` berisi `{statement, signature}`. Pernyataan kanonik ditandatangani oleh kunci ruang kerja dan berisi `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning`, dan `state`. State adalah replay deterministik: `annotations_head`, sebuah array `items` yang terurut (koleksi, kartu, komentar termasuk tombstone), dan `status_history`. Item-item mempertahankan hash anotasi terakhir, urutan, penulis, dan waktunya, serta pencipta asli dan waktu pembuatan di seluruh revisi. Pemutaran ulang memeriksa revisi, induk, referensi koleksi, dan ID tindakan duplikat. ``manifest.json`` dan titik pemeriksaan baru juga mengikat ``annotations_head``. Simpan titik pemeriksaan secara terpisah untuk mendeteksi pemotongan atau penulisan ulang dengan kunci penandatanganan yang disalin.

### Versi teks

`range.start` adalah offset titik kode Unicode berbasis nol, `length` adalah jumlah titik kode positif, dan `quote` harus sama persis dengan substring dari `payload.text` atau `payload.caption` pada peristiwa target. Tidak diterapkan NFC/NFKC, case folding, atau normalisasi grafem. Potongan string Python dan `Array.from(text)` JavaScript menerapkan pengindeksan yang sama. Kombinasi tanda dan emoji ZWJ mungkin menempati beberapa titik kode. ``range.version`` adalah hash peristiwa target, bukan versi pesan saat ini atau offset entitas UTF-16 Telegram. Pengeditan selanjutnya tidak pernah memindahkan sorotan secara otomatis.

### Identitas dan waktu potongan

`query` menerima tepat satu `chat_id` atau `chat_ids` yang tidak kosong, rentang `from`/`to` inklusif opsional, batas ID pesan inklusif (hanya satu obrolan), `kinds: "all"` atau jenis wildcard eksak/awalan, `actors` eksplisit, `search`, `hide_system`, dan `include_unscoped`. Kelompok jenis jurnal diperluas menjadi predikatnya yang tepat. Pencarian menggunakan pencarian muatan jurnal yang di-NFC/case-folded tanpa mengubah teks sumber yang ditandatangani. Tanggal memerlukan zona waktu dan dinormalisasi ke UTC. Tanggal menyaring **`observed_at`**. ``source_at`` dari Telegram ditampilkan secara terpisah. Penghapusan tanpa cap waktu sumber tidak memiliki waktu penghapusan yang dibuat-buat. Catatan terlambat yang diamati di luar interval waktu tidak dimasukkan ke dalamnya; potongan `message-ID` dapat mencakup penghapusan yang lebih baru untuk `message-ID` tersebut.

`snapshot` menetapkan waktu pembuatan, batas urutan/hash jurnal, jumlah kecocokan, urutan pertama/terakhir, dan `result_hash`. Yang terakhir ini adalah SHA-256 dari array JSON kanonik UTF-8 dari hash peristiwa yang cocok yang diurutkan secara leksikografis, termasuk `[]` untuk potongan kosong. Snapshot ini juga memuat jumlah jenis yang tepat dan miniatur waktu pengamatan dengan 24 bin. Sebuah potongan (slice) menyimpan kueri, bukan catatan sumber duplikat. Saat diekspor, `board/slices/<id>.json` mencantumkan hash saat ini serta urutan yang ditambahkan/dihapus. Verifikator merekonstruksi hasil asli pada batas pembuatan, kemudian hasil saat ini. Catatan yang ditambahkan dilaporkan sebagai fakta perubahan. Menghapus peristiwa asli akan memutus rantai bukti yang tidak dapat diubah; hal ini tidak diterima secara diam-diam sebagai penghapusan biasa dari sebuah slice.

Cuplikan reaksi memiliki daftar aktor terbaru yang tidak lengkap. Penjelajah membandingkan cuplikan yang berdekatan dari obrolan/pesan yang sama, termasuk pendahulu di luar potongan, dan melaporkan selisih jumlah agregat **antara pengamatan**. Aktor terbaru yang hilang tidak dianggap telah menghapus reaksi. Cuplikan pertama tidak memiliki status sebelumnya yang disimpulkan. Pengamatan aktor tetap dikaitkan dengan cuplikan tempat pengamatan tersebut disediakan, bukan dengan waktu tindakan yang dibuat-buat.

## API dan ekspor

`GET /api/board`menerima collection/chat/author/label/state/from/to/q/kind/comments, offset/limit dan urutan terbaru/terlama. `GET /api/board/card/{id}`mengembalikan kartu, pratinjau sumber, utas, riwayat status, dan kartu terkait. Subrute peserta mengembalikan pilihan sebutan yang memenuhi syarat. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` menambahkan catatan. `POST /api/board/slice-preview` menghitung kueri. Catatan slice dipaginasikan di `GET /api/board/slice/{id}/records`; perhitungan ulang selalu menggunakan snapshot baca stabil terkini. `/api/stream` yang aktif mengirimkan pemberitahuan `board` tanpa muatan, terpisah dari kursor jurnal.

`GET /api/board/export` mengembalikan dokumen yang ditandatangani. Akses terbatas obrolan menerima **pengungkapan** yang ditandatangani dan diberi label dengan jelas, bukan anotasi obrolan lain atau rantai lengkap. File ZIP bukti lengkap berisi `annotations.jsonl`, `case-board.json` yang ditandatangani, dan lampiran JSON potongan. Pengaturan laporan HTML/PDF/JSON memungkinkan pemilihan tanpa papan, penanda/potongan tanpa diskusi, atau kartu dengan komentar. Bagian tersebut secara eksplisit memisahkan pendapat tim dari pengamatan. Filter data laporan juga membatasi catatan yang dapat dibaca; file sumber lengkap yang ditandatangani dalam ZIP bukti tetap utuh.

`GET /api/board/slice/{id}/export` menghasilkan cuplikan JSON `tgwitness-board-selection-v1` yang telah ditandatangani; `?format=csv` menghasilkan tabel yang praktis tanpa tanda tangan terpisah. Pertahankan format JSON dan ZIP:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Pemeriksaan seleksi mengautentikasi pernyataan yang ditandatangani, catatan sumber yang tepat, dan kelengkapan kueri pada batas yang ditentukan. File ZIP bukti mungkin lebih baru tetapi harus mengandung awalan tersebut. Target yang terputus dilaporkan secara eksplisit. Snapshot potongan asli yang berbeda, anotasi yang diubah, status pemutaran ulang yang tidak cocok, atau sumber yang diubah akan gagal. Arsip lama tanpa anotasi tetap mempertahankan perilaku verifikasi yang ada.

Pengalihan secara default diatur ke **"Jangan sertakan"**. Penyertakan eksplisit menampilkan kartu proyek melalui catatan yang telah diminimalkan, mengabaikan target yang tidak dapat diakses/dilewati, menyembunyikan sorotan yang teks sumbernya telah diminimalkan, membersihkan teks tim dengan aturan penyebutan/kontak yang sama, dan secara opsional mengganti label penyelidik dengan R01, R02… dalam metadata dan kemunculan yang diketahui dalam catatan. Tidak ada berkas ` `annotations.jsonl`` asli yang diungkapkan. Sidecar ``tgwitness-case-board-handover-v1`` yang ditandatangani dan laporan berisi materi yang disembunyikan yang sama. Jumlah potongan hanya menggambarkan catatan yang diungkapkan, dengan detail aktor snapshot/kueri asli yang disembunyikan. Nama-nama dalam teks bebas yang tidak dikenal oleh alat minimisasi masih memerlukan peninjauan, seperti halnya dalam proses penyerahan biasa. Turunan ini tidak mengklaim mempertahankan tanda tangan anotasi asli setelah penyuntingan.

## Batasan operasional

Parameter mencakup batas lunak sebanyak 10.000 kartu dan 50.000 komentar, halaman potongan hingga 5.000 catatan, serta kontrol pratinjau media. Batas lunak memberikan peringatan tanpa menghapus riwayat. Halaman umpan memuat maksimal 200 kartu. Kutipan potongan JSON mandiri dibatasi hingga 64 MiB; persempit kueri atau gunakan ZIP yang ditandatangani untuk materi yang lebih besar. Verifikator mandiri membatasi pemutaran ulang anotasi hingga 256 MiB. Pemberitahuan komentar eksternal tidak diaktifkan atau diimplementasikan oleh Case Board.

Proses penerimaan otomatis fitur ini menggunakan data fiktif dan transportasi Telegram yang disimulasikan untuk memverifikasi penyimpanan, akses, penayangan, dan ekspor. Lihat [ruang lingkup verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope) untuk mengetahui cakupan pemeriksaan bukti.
