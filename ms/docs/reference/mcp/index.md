# MCP hanya-baca

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/

Sambungkan klien MCP ke ruang kerja dan sembang terpilih dengan akses yang akan tamat tempoh dan boleh ditarik balik.

Sambungkan klien penganalisis kepada ruang kerja dan sembang yang dipilih. TgWitness menyajikan **Streamable HTTP di `/mcp` dalam proses panel**. Setiap sambungan mempunyai token, tempoh luput dan alat yang dibenarkan tersendiri. MCP tidak boleh menghantar mesej Telegram, menukar tetapan atau mengubah suai jurnal bertandatangan.

[Panduan aliran kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Pasang dan semak

Gunakan persekitaran Python yang menjalankan panel. Daripada semak keluar sumber:

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

Mulakan semula panel dengan direktori data dan argumen pelancaran yang biasa selepas pemasangan. Kesediaan harus menyertakan `[PASS] mcp: streamable-http available`. **Integrations → MCP** menunjukkan status masa jalan dan perintah pemasangan menggunakan boleh laku Python sebenar pelayan tersebut. **Re-check** memuat semula status ini tanpa memuat semula halaman; ia tidak memasang pakej atau memulakan semula pelayan.

Tambahan MCP menggunakan [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) yang rasmi. `deploy/constraints-mcp.txt` menetapkan SDK dan kebergantungan yang telah diuji. Ciri-ciri ini memerlukan sumber semasa; pratonton mudah alih 0.7.0 mendahului ciri-ciri tersebut.

## Keluarkan sambungan

1. Masukkan label dan pilih ruang kerja serta sembang yang boleh dibaca oleh klien.
2. Pilih alat secara individu atau gunakan praset. Hanya alat yang dilaksanakan sahaja ditawarkan.
3. Pilih 1, 7, 30 atau 90 hari, atau tempoh luput tersuai antara satu minit hingga 90 hari.
4. Tekan **Create connection**. Token muncul sekali di sebelah konfigurasi klien.
5. Salin token dan konfigurasi, kemudian jalankan **Check connection**. Ia memulakan MCP dan menyenaraikan alat yang dibenarkan; **tiada mesej dibaca**. Hasilnya menunjukkan versi protokol, nama alat, kiraan dan masa berlalu.
6. Tekan **Done** apabila bukti kelayakan disimpan. Tinjauan mengekalkan borang dan kad yang ditunjukkan sekali. Mengunci panel mengosongkan rahsia yang dipaparkan.

Senarai menunjukkan penggunaan terkini, alat terakhir, alamat dan permintaan dalam minit terakhir. **Revoke** menamatkan akses. **Rotate token** membatalkan bukti kelayakan lama dan mengeluarkan penggantian dengan skop, alat dan tempoh luput yang sama; salin penggantian tersebut sekali. Token log masuk panel dan bukti kelayakan Telegram tidak berfungsi sebagai token MCP.

## Sambungkan klien anda

Pilih klien dalam panel dan salin konfigurasi yang dijana. Konfigurasi menggunakan rujukan rahsia atau pemegang tempat eksplisit; token disalin secara berasingan.

| Klien | Konfigurasi | Sambungan |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, pengepala pembawa |
| Claude Desktop | `claude_desktop_config.json` | Jambatan stdio tempatan |
| Cursor | `.cursor/mcp.json` | HTTP dengan pengepala pemboleh ubah persekitaran |
| VS Code Local | `.vscode/mcp.json` | HTTP dengan input `promptString` kata laluan |
| Windsurf | `mcp_config.json` | HTTP dengan pemegang tempat pengepala pembawa |
| Klien lain | URL dan pengepala Authorization | Streamable HTTP |

TgWitness menggunakan token pembawa, tanpa penemuan OAuth. Gunakan jambatan stdio tempatan untuk klien yang penyambung jauhnya memerlukan OAuth. Bagi VS Code, pemboleh ubah input terpakai pada abah-abah **Local** dan tidak dimajukan ke sesi Copilot. Rujukan konfigurasi: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Titik masuk kanonik untuk jambatan tempatan ialah:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Gunakan Python tempatan klien dengan tambahan MCP yang dipasang. Tetapkan `TGWITNESS_MCP_TOKEN` dalam persekitaran terlindungnya. Pastikan bukti kelayakan tidak berada dalam argumen perintah dan URL. `tgwitness-mcp` ialah titik masuk yang sama. Modul `tgwitness.mcp_bridge` dan nama `TGWITNESS_ARCHIVE_TOKEN` yang lama kekal sebagai laluan keserasian dengan amaran; konfigurasi baharu menggunakan `mcp_server` dan `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Majukan laluan `/mcp` panel dan kekalkan pengepala pembawa. Membuka tetapan MCP sebagai pentadbir mendaftarkan asalan semasa panel untuk larian ini. Untuk alamat stabil yang tersedia serta-merta selepas mula semula, konfigurasikan `TGWITNESS_PUBLIC_URL` dengan asalan HTTPS panel sebelum memulakan panel. Pengepala Host dan yang dimajukan secara sembarangan tidak mendaftarkan alamat yang dipercayai. Semakan Host dan Origin menolak asalan pelayar yang tidak berkaitan. Respons menggunakan `Cache-Control: no-store`; nilai kebenaran tidak pernah dilog.

Alamat `*.trycloudflare.com` adalah sementara. Apabila permulaan semula terowong menukar nama hos, kemas kini URL awam yang dikonfigurasikan dan URL MCP setiap klien. Gunakan nama hos yang stabil untuk konfigurasi klien yang disimpan.

## Alat dan sempadan

| Alat | Membaca |
| --- | --- |
| `list_workspaces` | Ruang kerja yang dibenarkan |
| `list_chats` | Sembang yang dibenarkan |
| `search_messages` | Teks mesej yang disimpan dalam tempoh yang dipilih |
| `get_message_versions` | Versi yang ditangkap dan pemerhatian pemadaman |
| `get_message_context` | ID mesej yang ditangkap berdekatan |
| `get_journal_event` | Satu rekod tersanitasi dengan rujukan sumbernya |
| `get_capture_status` | Keadaan pengumpulan dan rekod liputan yang dibenarkan |

`tools/list` hanya mengembalikan alat yang dibenarkan kepada sambungan tersebut. Panggilan ke alat lain ditolak. Alat konteks kumpulan, episod, terminologi dan rantaian balasan tidak ditawarkan dalam binaan ini; bahagian belakang pek konteks berasingan mereka tidak disertakan.

Setiap bacaan menyemak token, alat dan skop ruang kerja/sembang, termasuk selepas kerja pangkalan data selesai. Had ialah 60 permintaan seminit, 50 rekod setiap halaman, 64 KiB setiap hasil dan tarikh akhir arkib lapan saat. Panggilan MCP yang tamat masa mengembalikan ralat alat yang meminta tempoh yang lebih sempit atau had yang lebih rendah.

Hasil mesej membawa `untrusted_content: true`, ID ruang kerja/sembang/mesej, jujukan peristiwa, cincangan yang disimpan dan pautan panel. Objek Telegram mentah, cincangan akses, sesi dan kunci ditinggalkan. Pemangkasan teks ditandakan. Suntingan, notis pemadaman dan `missing_on_recheck` adalah pemerhatian yang berbeza. Rekod yang hilang tidak membuktikan sesuatu peristiwa tidak pernah berlaku.

Anggap arahan di dalam mesej yang ditangkap sebagai bukti, sama sekali bukan sebagai arahan klien. Akses baca sahaja menghalang perubahan arkib; klien masih boleh mengekalkan kandungan yang dibenarkan untuk dibaca. Cincangan mengenal pasti rekod yang disimpan dan menyokong semakan integriti; ia tidak membuktikan kepengarangan Telegram atau tangkapan lengkap.
