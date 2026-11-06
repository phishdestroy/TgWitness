# Baris perintah

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/cli/

Cari, baca konteks, hitung aktivitas, dan ekspor pesan yang disimpan dari skrip dan agen, dengan output --json, kode keluar yang stabil, dan token baca-saja yang terbatas cakupannya.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Archive integrations](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[MCP hanya baca](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/) · [Pencarian teks lengkap](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Pratinjau.** `tgwitness search`, `context`, `messages`, `stats` dan `export` membaca pengamatan yang disimpan untuk skrip dan agen AI. Mereka tidak dapat mengirim apa pun ke Telegram, mengubah pengaturan, atau memodifikasi jurnal yang ditandatangani.

Dengan `--json`, stdout menampilkan tepat satu dokumen JSON (`export` menulis baris JSON). Kemajuan, petunjuk, dan kesalahan dikirim ke stderr. Kode keluar bersifat stabil:

| Kode | Arti |
| --- | --- |
| `0` | Keberhasilan, termasuk hasil kosong |
| `1` | Kegagalan: panel tidak dapat diakses, data tidak dapat dibaca, ekspor terputus |
| `2` | Kesalahan penggunaan atau permintaan tidak valid: tanggal salah, opsi tidak dikenal, indeks pencarian tidak aktif |
| `3` | Saat ini tidak tersedia: ruang kerja sedang terbuka di panel yang sedang berjalan, atau panel meminta untuk mencoba lagi nanti (batasan frekuensi, waktu habis) |
| `4` | Akses ditolak: token hilang, kedaluwarsa, atau dicabut; obrolan di luar cakupan; atau alat yang tidak mengizinkannya |

## Dua cara untuk membacanya

**Melalui panel (`--url`).** Perintah ini menggunakan API arsip berskala yang sama dengan MCP. Buat koneksi di **Integrasi → MCP**: pilih ruang kerja dan obrolan, alat, serta masa berlaku, lalu salin token sekali saja. Koneksi ini bersifat baca-saja, terbatas pada obrolan-obrolan tersebut, dibatasi hingga 60 permintaan per menit, dan dapat dicabut atau diganti kapan saja. Token login panel dan kredensial Telegram tidak berfungsi di sini.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Panel jarak jauh memerlukan HTTPS; HTTP biasa hanya diterima untuk `127.0.0.1`, `localhost` dan `::1`. Variabel lingkungan proxy diabaikan dan pengalihan ditolak, sehingga token hanya akan sampai ke alamat yang Anda tentukan.

**Langsung dari ruang kerja yang dihentikan (`--data-dir`).** Membaca direktori data dengan akses lokal penuh, tanpa token. Gunakan pada salinan direktori data atau saat proses pengumpulan data dihentikan. Catatan yang ditandatangani tidak pernah diubah; seperti pada panel, membuka ruang kerja dapat memperbarui indeks yang diturunkan darinya. Saat panel membuka ruang kerja, perintah akan keluar dengan kode `3`; bacalah melalui panel sebagai gantinya. Tanpa `--data-dir`, `TGWITNESS_DATA`, `./data/live` atau direktori data dari instalasi yang menjalankan perintah tersebut.

`--workspace ID` memilih ruang kerja (daftar default `default`). `tgwitness messages
--workspaces` menampilkan daftar ruang kerja yang dapat Anda baca.

## Perintah

| Perintah | Hasil |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Hasil yang paling sesuai ditampilkan terlebih dahulu, termasuk bentuk kata, frasa persis dalam tanda kutip, domain, dan `@username` ([sintaksis](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Teks persis, yang terbaru terlebih dahulu, tanpa indeks |
| `tgwitness context CHAT_ID MESSAGE_ID` | Pesan yang disimpan dalam rentang sepuluh ID pesan di kedua sisi |
| `tgwitness messages` | Obrolan yang dapat Anda baca |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Pesan obrolan yang disimpan, dimulai dari yang terbaru |
| `tgwitness messages CHAT_ID --message ID` | Setiap versi yang disimpan dan catatan penghapusan dari satu pesan |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Statistik aktivitas, di bawah ini |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Pengamatan yang disimpan sebagai baris JSON sesuai urutan jurnal |

Tanggalnya adalah `2026-10-01` (pukul 00.00 UTC) atau waktu ISO dengan zona waktu, `2026-10-01T09:00+03:00`. Untuk `search`, `messages` dan `export` mereka memilih waktu pengamatan. Setiap halaman menampung hingga 50 catatan: ikuti `next_offset` (`--offset`) untuk pencarian berdasarkan peringkat dan `next_before` (`--before`) di tempat lain.

Ranked search stops at 1,000 results. The final page may be shorter than `--limit`; narrow the query, chat or period when more matching observations exist.

Setiap hasil pesan memuat `untrusted_content: true`ID ruang kerja, obrolan, dan pesan, urutan jurnal, hash catatan yang disimpan, serta tautan panel. Pengeditan, pemberitahuan penghapusan, dan `missing_on_recheck` merupakan catatan terpisah. Tidak adanya suatu catatan tidak membuktikan bahwa suatu peristiwa tidak pernah terjadi.

### Statistik aktivitas

`stats` menghitung pengamatan yang disimpan untuk satu obrolan, satu pengirim, atau semua obrolan dalam cakupan:

- pesan berdasarkan jam UTC dan hari dalam seminggu (dimulai dari Senin), jam dan hari tersibuk;
- yang telah diedit, dihapus, dan `missing_on_recheck` berbagi;
- pengirim beserta jumlah pesan serta waktu pesan pertama dan terakhir;
- domain yang paling sering muncul dan `@handles`, dihitung satu kali per pesan di seluruh versi yang disimpan;
- cakupan: `coverage.gap` catatan dan, untuk mengakses seluruh ruang kerja, periode tanpa detak jantung pengumpul yang terhubung (`collector_liveness`).

Periode ini memilih **waktu pesan yang dilaporkan oleh Telegram**. Jumlah jam dan hari kerja dapat membantu memperkirakan zona waktu pengirim; namun, hal tersebut tidak menentukan zona waktunya secara pasti. Angka-angka dihitung berdasarkan permintaan dari jurnal dan tidak disimpan. Setiap hasil mencantumkan nama kepala jurnal yang dicakupnya ketika akses Anda mencakup ruang kerja tersebut. Pembacaan akan berhenti setelah lima detik melalui panel, atau `--timeout` detik secara lokal (default 30); kemudian `complete` bernilai false dan `partial` menyebutkan catatan pertama yang belum dibaca. Hanya catatan terbaru yang dihitung dalam kasus tersebut.

### Ekspor

`export` Menulis satu objek JSON per pengamatan yang disimpan (pesan baru, tangkapan layar, pengeditan, pesan yang dipulihkan, pemberitahuan penghapusan, `missing_on_recheck` dan rekaman media yang disimpan) sesuai urutan jurnal. Setiap baris memiliki bidang yang sama dengan hasil lainnya, beserta teks lengkapnya. Dengan `--output`, berkas ditulis dengan `.partial` nama dan hanya diganti namanya setelah catatan penyelesaian panel; ekspor yang terputus tidak meninggalkan file apa pun dan keluar dengan kode `1`. `--output` tidak akan pernah menimpa berkas yang sudah ada. Dengan `--output` dan `--json`, stdout menampilkan ringkasan: jumlah catatan, urutan jurnal terakhir, dan, untuk akses seluruh ruang kerja, kepala jurnal.

Ekspor melalui panel memerlukan koneksi yang memungkinkan **ekspor pesan (hanya melalui baris perintah)**; opsi ini tidak dipilih secara default. Berkas ini adalah salinan kerja, bukan bukti: untuk penyerahan yang dapat diverifikasi, gunakan ekspor yang ditandatangani di **bagian** **Ekspor**, yang `python -m tgwitness.verify`melakukan verifikasi.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Keterampilan agen

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) menjelaskan kepada agen cara menggunakan perintah-perintah ini, cara mengutip catatan, dan cara menangani teks yang ditangkap. Agen yang membaca `.agents/skills` memuatnya dari hasil checkout repositori . Untuk Claude Code, salin `tgwitness-cli` folder tersebut ke `.claude/skills/` di proyek Anda atau `~/.claude/skills/`.

## MCP dan baris perintah

Keduanya menggunakan koneksi, pemeriksaan cakupan, dan batasan yang sama. Hasil MCP dibatasi hingga satu halaman berukuran 64 KiB, sehingga MCP tidak menawarkan ekspor massal; baris perintah mengalirkannya. `get_activity_stats` tersedia untuk keduanya.
