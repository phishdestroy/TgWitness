# MCP hanya-baca

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/

Sambungkan klien MCP ke ruang kerja dan sembang terpilih dengan akses yang akan tamat tempoh dan boleh ditarik balik.

**Utama semasa:** gunakan checkout sumber; pratonton mudah alih 0.7.0 wujud sebelum ciri ini.

[Panduan aliran kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Pasang pelayan pilihan daripada direktori projek TgWitness:

```
python -m pip install '.[mcp]'
```

Di panel, buka **Integrasi → MCP**. Namakan sambungan, pilih ruang kerja dan sembangnya, dan pilih tarikh luput. Salin token arkib sekali sahaja; ia tidak dapat dipulihkan kemudian. Batalkan token yang hilang dan keluarkan pengganti. Token panel dan kelayakan Telegram bukan kelayakan MCP.

## Sambungkan klien

Panel menjana token `.vscode/mcp.json` untuk **harness VS Code Local** menggunakan [konfigurasi yang didokumentasikannya](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Simpan fail yang dimuat turun di lokasi tersebut, jalankan **MCP: List Servers**, dan mulakan TgWitness. VS Code meminta token melalui masukan kata laluan. JSON yang dimuat turun mengandungi rujukan permintaan, bukan token itu sendiri. Gunakan fail boleh laji Python dari persekitaran di mana MCP extra dipasang.

Untuk klien stdio lain, jalankan:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Setingkan `TGWITNESS_ARCHIVE_TOKEN` dalam persekitaran terlindung klien. Jangan masukkan ia dalam argumen perintah atau URL. Jambatan ini membaca melalui API arkib bertauliah panel; ia tidak mempunyai akses langsung ke pangkalan data. Stdout hanya mengandungi mesej MCP.

Untuk klien jauh, jalankan perkhidmatan di sebelah panel:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Alihkan `/mcp` melalui proksi terbalik HTTPS ke `127.0.0.1:8766/mcp`, sambil mengekalkan header `Authorization: Bearer …`. Matikan log header kebenaran dan badan permintaan/jawapan. Ikatan melangkaui loopback hanya apabila diperlukan, menggunakan `--host` dan `--public-url`. Titik akhir ini menggunakan Streamable HTTP daripada [SDK Python MCP](https://github.com/modelcontextprotocol/python-sdk) rasmi. Ia menyokong kelayakan pembawa yang dikonfigurasikan secara eksplisit, bukan penemuan OAuth; klien yang hanya memerlukan OAuth tidak disokong.

**Periksa protokol dan akses** memulakan klien MCP sebenar dan menyenaraikan alat. Ia tidak memuat turun mesej. Untuk pemeriksaan jauh, pelayan MCP terpilih menerima token arkib. Konfigurasikan hanya pelayan yang anda kendalikan atau percayai dengan skop tersebut.

## Skop dan keputusan

Alat yang tersedia: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event`, dan `get_capture_status`. Tiada tindakan Telegram, perubahan konfigurasi, atau alat eksport pukal. Setiap kali dibaca, ia menyemak semula akses ruang kerja/perbualan; kelayakan yang telah tamat tempoh dan dibatalkan berhenti berfungsi. Hadnya ialah 60 permintaan API seminit bagi setiap kelayakan, 50 rekod setiap halaman, respons 64 KiB, dan tempoh akhir API lapan saat.

Hasil mesej termasuk ruang kerja, ID sembang/mesej, urutan peristiwa, hash yang disimpan, dan pautan panel. Pemapar yang membuka pautan mesti mempunyai sesi panel bertauliah sendiri. Objek Telegram mentah, hash akses, rujukan fail, bahan sesi, dan kunci diabaikan. Carian memeriksa teks mesej, bukan medan mentah. Teks dihadkan dan pemotongan ditandakan. Suntingan, notis pemadaman Telegram, dan `missing_on_recheck` kekal sebagai pemerhatian berasingan. Akses skop sembang tidak dapat melihat peristiwa operasi di seluruh ruang kerja; status tangkapan menandakan had ini secara eksplisit.

Teks arkib adalah input yang tidak dipercayai. Arahan di dalam mesej tidak memberikan sebarang skop tambahan dan tidak boleh dianggap sebagai arahan klien. Model AI luaran mungkin menerima apa sahaja kandungan yang diminta oleh klien MCPnya. Akses baca sahaja menghalang perubahan arkib; ia tidak menghalang klien daripada menyimpan data yang dibacanya.

Hash mengenal pasti rekod yang disimpan dan menyokong pemeriksaan integriti. Ia tidak secara bebas membuktikan pengarang Telegram atau bahawa setiap mesej telah dirakam.
