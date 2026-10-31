# MCP hanya baca

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/

Hubungkan klien MCP ke ruang kerja dan obrolan yang dipilih dengan akses yang memiliki batas waktu dan dapat dicabut.

**Versi utama saat ini:** gunakan checkout sumber; pratinjau portabel 0.7.0 dirilis sebelum fitur ini tersedia.

[Panduan alur kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Instal server opsional dari direktori proyek TgWitness:

```
python -m pip install '.[mcp]'
```

Di panel, buka **Integrasi → MCP**. Beri nama koneksi, pilih ruang kerja dan obrolannya, serta tentukan masa berlaku. Salin token arsip sekali saja; token ini tidak dapat diambil kembali nanti. Cabut token yang hilang dan terbitkan penggantinya. Token panel dan kredensial Telegram bukanlah kredensial MCP.

## Hubungkan klien

Panel tersebut menghasilkan `.vscode/mcp.json` untuk **harness Lokal VS Code** menggunakan [konfigurasi yang terdokumentasi](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Simpan berkas yang diunduh di lokasi tersebut, jalankan **MCP: List Servers**, dan mulai TgWitness. VS Code akan meminta token melalui kolom masukan kata sandi. Berkas JSON yang diunduh berisi referensi prompt, bukan token itu sendiri. Gunakan berkas eksekusi Python dari lingkungan tempat ekstensi MCP diinstal.

Untuk klien stdio lainnya, jalankan:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Tetapkan `TGWITNESS_ARCHIVE_TOKEN` di lingkungan terlindungi klien. Jangan memasukkannya ke dalam argumen perintah atau URL. Jembatan ini membaca melalui API arsip yang diotorisasi panel; jembatan ini tidak memiliki akses langsung ke basis data. Stdout hanya mentransmisikan pesan MCP.

Untuk klien jarak jauh, jalankan layanan ini di samping panel:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Teruskan `/mcp` melalui proxy terbalik HTTPS ke `127.0.0.1:8766/mcp`, dengan tetap mempertahankan header `Authorization: Bearer …`. Nonaktifkan pencatatan header otorisasi serta isi permintaan/respons. Lakukan pengikatan di luar loopback hanya jika diperlukan, menggunakan `--host` dan `--public-url`. Titik akhir ini menggunakan Streamable HTTP dari [SDK Python MCP](https://github.com/modelcontextprotocol/python-sdk) resmi. Endpoint ini mendukung kredensial bearer yang dikonfigurasi secara eksplisit, bukan penemuan OAuth; klien yang hanya memerlukan OAuth tidak didukung.

**Proses pemeriksaan protokol dan akses** akan menginisialisasi klien MCP yang sebenarnya serta menampilkan daftar alat. Proses ini tidak mengambil pesan. Untuk pemeriksaan jarak jauh, server MCP yang dipilih akan menerima token arsip. Konfigurasikan hanya server yang Anda kelola atau percayai dengan cakupan tersebut.

## Ruang lingkup dan hasil

Alat yang tersedia: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event`, dan `get_capture_status`. Tidak ada tindakan Telegram, perubahan konfigurasi, atau alat ekspor massal. Setiap kali dibaca, akses ruang kerja/obrolan diperiksa ulang; kredensial yang kedaluwarsa dan dicabut tidak lagi berfungsi. Batasannya adalah 60 permintaan API per menit per kredensial, 50 catatan per halaman, respons sebesar 64 KiB, dan batas waktu API delapan detik.

Hasil pesan mencakup ruang kerja, ID obrolan/pesan, urutan peristiwa, hash yang disimpan, dan tautan panel. Pengguna yang membuka tautan harus memiliki sesi panel yang terotorisasi sendiri. Objek Telegram mentah, hash akses, referensi file, materi sesi, dan kunci dihilangkan. Pencarian memeriksa teks pesan, bukan bidang mentah. Teks dibatasi dan pemotongan ditandai. Pengeditan, pemberitahuan penghapusan Telegram, dan `missing_on_recheck` tetap menjadi pengamatan terpisah. Akses dalam lingkup obrolan tidak dapat melihat peristiwa operasional di seluruh ruang kerja; status penangkapan secara eksplisit menandai batasan ini.

Teks arsip merupakan masukan yang tidak dapat dipercaya. Instruksi di dalam pesan tidak memberikan ruang lingkup tambahan dan tidak boleh diperlakukan sebagai instruksi klien. Model AI eksternal dapat menerima konten apa pun yang diminta oleh klien MCP-nya. Akses baca-saja mencegah perubahan pada arsip; hal ini tidak mencegah klien untuk menyimpan data yang dibacanya.

Hashes tersebut mengidentifikasi catatan yang disimpan dan mendukung pemeriksaan integritas. Hashes tersebut tidak secara mandiri membuktikan keaslian pengirim di Telegram atau bahwa setiap pesan telah terekam.
