# MCP hanya baca

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/

Hubungkan klien MCP ke ruang kerja dan obrolan yang dipilih dengan akses yang memiliki batas waktu dan dapat dicabut.

Hubungkan klien analis ke ruang kerja dan obrolan yang dipilih. TgWitness menyajikan **Streamable HTTP di `/mcp` dalam proses panel**. Setiap koneksi memiliki token, masa berlaku, dan alat yang diizinkan sendiri. MCP tidak dapat mengirim pesan Telegram, mengubah pengaturan, atau memodifikasi jurnal bertanda tangan.

[Panduan alur kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Instal dan periksa

Gunakan lingkungan Python yang menjalankan panel. Dari checkout sumber:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Mulai ulang panel dengan direktori data dan argumen peluncuran biasanya setelah instalasi. Pemeriksaan kesiapan harus menyertakan `[PASS] mcp: streamable-http available`. **Integrations → MCP** menampilkan status runtime dan perintah instalasi yang menggunakan eksekutabel Python aktual server tersebut. **Re-check** menyegarkan status ini tanpa memuat ulang halaman; tindakan ini tidak menginstal paket atau memulai ulang server.

MCP extra menggunakan [SDK Python resmi MCP](https://github.com/modelcontextprotocol/python-sdk).`deploy/constraints-mcp.txt` mengunci versi SDK dan dependensi yang telah diuji.

## Terbitkan koneksi

1. Masukkan label dan pilih ruang kerja serta obrolan yang boleh dibaca oleh klien.
2. Pilih alat satu per satu atau gunakan preset. Hanya alat yang telah diimplementasikan yang ditawarkan.
3. Pilih 1, 7, 30, atau 90 hari, atau masa berlaku khusus antara satu menit hingga 90 hari.
4. Tekan **Create connection**. Token muncul satu kali di samping konfigurasi klien.
5. Salin token dan konfigurasi, lalu jalankan **Check connection**. Tindakan ini menginisialisasi MCP dan mencantumkan alat yang diizinkan; **tidak ada pesan yang dibaca**. Hasilnya menampilkan versi protokol, nama alat, jumlah, dan waktu yang berlalu.
6. Tekan **Done** setelah kredensial disimpan. Polling mempertahankan formulir dan kartu yang hanya ditampilkan sekali. Mengunci panel akan menghapus rahasia yang ditampilkan.

Daftar tersebut menampilkan penggunaan terkini, alat terakhir, alamat, dan permintaan dalam satu menit terakhir. **Revoke** mengakhiri akses. **Rotate token** mencabut kredensial lama dan menerbitkan pengganti dengan cakupan, alat, dan masa berlaku yang sama; salin pengganti tersebut satu kali. Token login panel dan kredensial Telegram tidak berfungsi sebagai token MCP.

## Hubungkan klien Anda

Pilih klien di panel dan salin konfigurasi yang dihasilkan. Konfigurasi menggunakan referensi rahasia atau placeholder eksplisit; token disalin secara terpisah.

| Klien | Konfigurasi | Koneksi |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, header bearer |
| Claude Desktop | `claude_desktop_config.json` | Jembatan stdio lokal |
| Cursor | `.cursor/mcp.json` | HTTP dengan header variabel lingkungan |
| VS Code Local | `.vscode/mcp.json` | HTTP dengan input kata sandi `promptString` |
| Windsurf | `mcp_config.json` | HTTP dengan placeholder header bearer |
| Klien lainnya | URL dan header Authorization | Streamable HTTP |

TgWitness menggunakan token bearer, tanpa penemuan OAuth. Gunakan jembatan stdio lokal untuk klien yang konektor jarak jauhnya memerlukan OAuth. Untuk VS Code, variabel input berlaku pada harness **Local** dan tidak diteruskan ke sesi Copilot. Referensi konfigurasi: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Titik masuk kanonis untuk jembatan lokal adalah:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Gunakan Python lokal klien yang sudah terinstal ekstra MCP. Atur `TGWITNESS_MCP_TOKEN` di lingkungan yang dilindunginya. Jauhkan kredensial dari argumen perintah dan URL. `tgwitness-mcp` adalah titik masuk yang sama. Modul lama `tgwitness.mcp_bridge` dan nama `TGWITNESS_ARCHIVE_TOKEN` tetap menjadi jalur kompatibilitas dengan peringatan; konfigurasi baru menggunakan `mcp_server` dan `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Teruskan rute `/mcp` panel dan pertahankan header bearer. Membuka pengaturan MCP sebagai administrator akan mendaftarkan origin panel saat ini untuk proses yang sedang berjalan ini. Untuk alamat stabil yang langsung tersedia setelah mulai ulang, konfigurasikan `TGWITNESS_PUBLIC_URL` dengan origin HTTPS panel sebelum memulai panel. Header Host dan forwarded yang sembarang tidak akan mendaftarkan alamat tepercaya. Pemeriksaan Host dan Origin menolak origin browser yang tidak terkait. Respons menggunakan `Cache-Control: no-store`; nilai otorisasi tidak pernah dicatat ke dalam log.

Alamat `*.trycloudflare.com` bersifat sementara. Ketika mulai ulang tunnel mengubah nama host, perbarui URL publik yang dikonfigurasi dan URL MCP setiap klien. Gunakan nama host yang stabil untuk konfigurasi klien yang disimpan.

## Alat dan batasan

| Alat | Yang dibaca |
| --- | --- |
| `list_workspaces` | Ruang kerja yang diizinkan |
| `list_chats` | Obrolan yang diizinkan |
| `search_messages` | Teks pesan tersimpan dalam periode yang dipilih |
| `get_message_versions` | Versi yang tertangkap dan pengamatan penghapusan |
| `get_message_context` | ID pesan sekitar yang tertangkap |
| `get_journal_event` | Satu catatan yang telah disanitasi beserta referensi sumbernya |
| `get_capture_status` | Status pengumpulan dan catatan cakupan yang diizinkan |

`tools/list` hanya mengembalikan alat yang diizinkan untuk koneksi tersebut. Pemanggilan ke alat lain akan ditolak. Alat konteks grup, episode, terminologi, dan rantai balasan tidak ditawarkan dalam build ini; backend paket konteks terpisahnya tidak disertakan.

Setiap pembacaan memeriksa token, alat, dan cakupan ruang kerja/obrolan, termasuk setelah pekerjaan database selesai. Batasannya adalah 60 permintaan per menit, 50 catatan per halaman, 64 KiB per hasil, dan batas waktu arsip delapan detik. Pemanggilan MCP yang kehabisan waktu mengembalikan kesalahan alat yang meminta periode yang lebih sempit atau batas yang lebih rendah.

Hasil pesan memuat `untrusted_content: true`, ID ruang kerja/obrolan/pesan, urutan peristiwa, hash tersimpan, dan tautan panel. Objek Telegram mentah, hash akses, sesi, dan kunci dihilangkan. Pemotongan teks ditandai. Suntingan, pemberitahuan penghapusan, dan `missing_on_recheck` adalah pengamatan yang berbeda. Catatan yang hilang tidak membuktikan bahwa suatu peristiwa tidak pernah terjadi.

Perlakukan instruksi di dalam pesan yang tertangkap sebagai bukti, jangan pernah sebagai instruksi klien. Akses baca-saja mencegah perubahan arsip; klien masih dapat menyimpan konten yang diizinkan untuk dibacanya. Hash mengidentifikasi catatan yang disimpan dan mendukung pemeriksaan integritas; hash tidak membuktikan kepengarangan Telegram atau penangkapan yang lengkap.
