# Baris perintah

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/cli/

Cari, baca konteks, kira aktiviti dan eksport mesej yang disimpan daripada skrip dan ejen, dengan keluaran --json, kod keluar stabil dan token baca sahaja yang terhad skop.

[MCP hanya baca](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/) · [Carian teks penuh](https://phishdestroy.github.io/TgWitness/ms/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Praperintian.** `tgwitness search`, `context`, `messages`, `stats` dan `export` baca pemerhatian yang disimpan untuk skrip dan ejen AI. Mereka tidak boleh menghantar apa-apa ke Telegram, menukar tetapan atau mengubah jurnal yang disahkan.

Dengan `--json`, stdout membawa tepat satu dokumen JSON (`export` menulis JSON Lines). Kemajuan, petunjuk dan ralat dihantar ke stderr. Kod keluar kekal:

| Kod | Maksud |
| --- | --- |
| `0` | Jaya, termasuk hasil kosong |
| `1` | Kegagalan: panel tidak dapat diakses, data tidak dapat dibaca, eksport terganggu |
| `2` | Ralat penggunaan atau permintaan tidak sah: tarikh salah, pilihan tidak diketahui, indeks carian tidak sah |
| `3` | Tidak tersedia sekarang: ruang kerja dibuka dalam panel yang sedang berjalan, atau panel meminta mencuba semula kemudian (had kadar, tamat masa) |
| `4` | Akses ditolak: token hilang, tamat tempoh atau dibatalkan, sembang di luar skopnya, alat yang tidak dibenarkan |

## Dua cara untuk membaca

**Melalui panel (`--url`).** Perintah ini menggunakan API arkib berlingkup yang sama seperti MCP. Buat sambungan di **Integrasi → MCP**: pilih ruang kerja dan sembang, alat dan tempoh luput, kemudian salin token sekali sahaja. Sambungan ini hanya untuk bacaan, terhad kepada sembang tersebut, dihadkan kadar kepada 60 permintaan seminit dan boleh ditarik balik atau dipulihkan pada bila-bila masa. Token log masuk panel dan kelayakan Telegram tidak berfungsi di sini.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Panel jauh memerlukan HTTPS; HTTP biasa hanya diterima untuk `127.0.0.1`, `localhost` dan `::1`. Pembolehubah persekitaran proksi diabaikan dan penalaan semula ditolak, jadi token hanya sampai ke alamat yang anda berikan.

**Langsung daripada ruang kerja yang dihentikan (`--data-dir`).** Membaca direktori data dengan akses tempatan penuh, tanpa token. Gunakan pada salinan direktori data atau semasa pengumpulan dihentikan. Rekod yang disahkan tidak pernah diubah; seperti panel, membuka ruang kerja mungkin mengemas kini indeks terbitannya. Apabila panel membuka ruang kerja, arahan akan keluar dengan kod `3`; baca melalui panel sebaliknya. Tanpa `--data-dir`, `TGWITNESS_DATA`, `./data/live` atau direktori data pemasangan yang menjalankan arahan digunakan.

`--workspace ID` memilih ruang kerja (laluan lalai `default`). `tgwitness messages
--workspaces` menyenaraikan ruang kerja yang boleh anda baca.

## Perintah

| Perintah | Keputusan |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Padanan terbaik diutamakan, dengan bentuk kata, frasa tepat dalam tanda petik, domain dan `@username` ([sintaksis](https://phishdestroy.github.io/TgWitness/ms/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Teks tepat, terkini dahulu, tanpa indeks |
| `tgwitness context CHAT_ID MESSAGE_ID` | Mesej yang disimpan dalam sepuluh ID mesej di kedua-dua belah |
| `tgwitness messages` | Perbualan yang boleh anda baca |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Mesej yang disimpan dalam sembang, yang terbaru dahulu |
| `tgwitness messages CHAT_ID --message ID` | Setiap versi yang disimpan dan rekod pemadaman bagi satu mesej |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Statistik aktiviti di bawah |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Pemerhatian disimpan sebagai JSON Lines mengikut susunan jurnal |

Tarikh adalah `2026-10-01` (tengah malam UTC) atau masa ISO dengan zon waktu, `2026-10-01T09:00+03:00`. Untuk `search`, `messages` dan `export` mereka memilih masa pemerhatian. Halaman memuat sehingga 50 rekod: ikuti `next_offset` (`--offset`) untuk carian berperingkat dan `next_before` (`--before`) di tempat lain.

Ranked search stops at 1，000 results．The final page may be shorter than `--limit`；narrow the query，chat or period when more matching observations exist．

Setiap keputusan mesej membawa `untrusted_content: true`, ruang kerja, sembang dan ID mesej, urutan jurnal, hash rekod yang disimpan dan pautan panel. Suntingan, notis pemadaman dan `missing_on_recheck` adalah rekod berasingan. Ketiadaan rekod tidak membuktikan bahawa sesuatu peristiwa tidak pernah berlaku.

### Statistik aktiviti

`stats` mengira pemerhatian yang disimpan untuk satu sembang, satu penghantar, atau setiap sembang dalam skop:

- mesej mengikut jam UTC dan hari dalam minggu (Isnin pertama), jam dan hari paling sibuk;
- disunting, dipadam dan `missing_on_recheck` kongsi;
- pengirim dengan bilangan mesej dan masa mesej pertama dan terakhir;
- domain yang paling kerap dan `@handles`, dikira sekali setiap mesej merentasi versi yang disimpannya;
- liputan: `coverage.gap` merekod dan, untuk akses ke seluruh ruang kerja, tempoh tanpa denyutan jantung pengumpul yang disambungkan (`collector_liveness`).

Tempoh memilih **masa mesej yang dilaporkan oleh Telegram**. Kiraan jam dan hari dalam minggu boleh membantu menganggarkan zon waktu penghantar; ia tidak menetapkannya. Angka dikira atas permintaan daripada jurnal dan tidak disimpan. Setiap keputusan menamakan tajuk jurnal yang diliputinya apabila capaian anda merentasi ruang kerja. Bacaan berhenti selepas lima saat melalui panel, atau `--timeout` saat secara tempatan (laluan lalai 30); kemudian `complete` adalah palsu dan `partial` menamakan rekod pertama yang tidak dibaca. Hanya rekod terkini yang dikira dalam kes itu.

### Eksport

`export` menulis satu objek JSON bagi setiap pemerhatian yang disimpan (mesej baharu, snapshot, suntingan, mesej dipulihkan, notis pemadaman, `missing_on_recheck` dan rakaman media yang disimpan dalam urutan jurnal. Setiap baris mempunyai medan yang sama seperti keputusan lain, dengan teks penuh. Dengan `--output`, fail itu ditulis di bawah `.partial` nama dan dinamakan semula hanya selepas rekod penyiapan panel; eksport yang terganggu tidak meninggalkan sebarang fail dan keluar dengan kod `1`. `--output` tidak pernah menulis ke atas fail yang sedia ada. Dengan `--output` dan `--json`, stdout memaparkan ringkasan: bilangan rekod, urutan jurnal terakhir dan, untuk capaian seluruh ruang kerja, tajuk jurnal.

Pengeksportan melalui panel memerlukan sambungan yang membenarkan **Eksport mesej (baris arahan sahaja)**; ia tidak dipilih secara lalai. Fail ini adalah salinan kerja, bukan bukti: untuk penyerahan yang boleh disahkan gunakan eksport yang disahkan dalam **Eksport**, yang `python -m tgwitness.verify`semak.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Kemahiran ejen

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) memberitahu ejen cara menggunakan arahan ini, cara memetik rekod dan cara mengendalikan teks yang dirakam. Ejen yang membaca `.agents/skills` memuatnya daripada simpanan checkout. Untuk Claude Code, salin `tgwitness-cli` folder ke `.claude/skills/` dalam projek anda atau `~/.claude/skills/`.

## MCP dan baris perintah

Kedua-duanya menggunakan sambungan, pemeriksaan skop dan had yang sama. Keputusan MCP terhad kepada satu halaman 64 KiB, jadi MCP tidak menawarkan eksport pukal; ia disalurkan melalui baris perintah. `get_activity_stats` tersedia untuk kedua-duanya.
