# Keselamatan dan pengendalian data

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/

Model ancaman, model capaian, rahsia semasa rehat, pendedahan rangkaian, import sesi dan cara melaporkan kerentanan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| Kawasan | Ringkasnya |
| --- | --- |
| Akses | Kunci pentadbir serta akses terhad ke akaun/perbualan, tujuh kebenaran dan sesi yang boleh ditarik balik; localhost secara lalai |
| Rahsia yang disimpan | Sesi, pasangan API, kunci penandatanganan dan tetapan proksi disulitkan dengan Fernet |
| Mesej dan media | Disimpan tanpa penyulitan: gunakan penyulitan cakera dan kebenaran yang ketat |
| Integriti | Rantaian hash SHA-256 dan tandatangan Ed25519 pada setiap rekod |
| Batas kepercayaan tempatan | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

Untuk laporan kerentanan, lihat [dasar keselamatan](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

**On this page**

- [Access model](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#access-model)
- [Panel content and exports](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#panel-content-and-exports)
- [Secrets at rest](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#secrets-at-rest)
- [Proxies and network routes](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#proxies-and-network-routes)
- [Sign-in and session imports](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#sign-in-and-session-imports)
- [Logs and transport](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#logs-and-transport)
- [Integrity limits](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#integrity-limits)
- [If you suspect a problem](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/#if-you-suspect-a-problem)

## Model akses

Token panel utama memberikan kawalan penuh. Orang lain boleh menerima [akses terhad](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/) mereka sendiri: ruang kerja dan sembang terpilih, kebenaran, tamat tempoh, sekatan IP, had log masuk dan sesi yang boleh ditarik balik. Akses terhad sembang tidak dapat menjalankan operasi seluruh ruang kerja walaupun kebenaran mereka telah dicentang. Ruang kerja berkongsi satu proses dan tidak mengasingkan data daripada pentadbir hos.

Panel mendengar pada localhost secara lalai. Log masuk pelayar menukar token akses untuk kelayakan sesi; pelayar menghantarnya sebagai token pembawa. Ia disimpan dalam sessionStorage dan bukannya kuki pengesahan. Kunci/keluar log membersihkan sesi pelayar. Menutup pelayar atau menamatkan sesi tidak menghentikan pengumpulan.

Token yang dikeluarkan dan kelayakan sesi disimpan sebagai hash dalam peti besi yang disulitkan. Pencabutan menamatkan sesi yang berkaitan; perubahan kebenaran menjejaskan permintaan seterusnya. Fail yang dimuat turun tidak dapat ditarik balik. Pentadbir juga boleh mengehadkan sesi pelayar mereka sendiri, tetapi skrip yang menggunakan token panel utama secara langsung mengekalkan akses penuh dan memintas had sesi pelayar tersebut.

Pengesahan gagal dihadkan kadar mengikut alamat klien. Sekatan IP menggunakan alamat yang dilihat oleh aplikasi; semak tingkah laku proksi songsang sebelum bergantung padanya. Kredensial Witness kekal berasingan sebagai kredensial titik pemeriksaan/kesihatan baca sahaja.

### Akses demo

`/api/demo-access` adalah bootstrap yang sengaja tidak diautentikasi untuk demo sintetik yang dimulakan secara eksplisit dan terasing. Ia mengeluarkan keupayaan tempoh-proses yang berasingan, tidak pernah token panel sebenar atau penimpaan TGWITNESS_TOKEN. Penerbitan dan penggunaan memerlukan rakan sebaya loopback dan Host, tiada pengepala yang diteruskan, dan tiada permintaan rentas asal. Ruang kerja tambahan atau sesi yang dibenarkan menyahaktifkan laluan ini. Ruang kerja langsung tidak pernah mengeluarkan keupayaan ini. Demo ini tidak boleh menghubungkan akaun atau menukar tetapan pengumpulan.

## Kandungan panel dan eksport

Panel ini tidak menggunakan fon luaran, analitik, sumber CDN, atau media jauh yang disemat. Teks yang diperoleh daripada Telegram disisipkan sebagai teks, bukan HTML. Lampiran yang dimuat turun dihidangkan sebagai lampiran binari. Eksport JSONL mengekalkan rentetan asal; HTML melarikan mereka; sel CSV yang boleh menjadi formula diberi awalan tanda petik.

Eksport mengecualikan rahsia pengesahan dan penandatanganan, tetapi sengaja mengandungi metadata sumber yang dikumpul, pengecam, dan mungkin kandungan peribadi atau sensitif. Hash akses Telegram dan rujukan fail boleh muncul dalam metadata sumber mentah.

## Rahsia yang disimpan

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### Kunci induk luaran

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) for setup details.

## Proksi dan laluan rangkaian

Konfigurasi proksi disulitkan dalam peti besi. Kata laluan dan rahsia MTProxy tidak dikembalikan oleh API atau ditulis ke dalam rekod bukti. Setiap ruang kerja memilih laluan Telegram dan [mod IP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes) masing-masing.

**Sembunyikan alamat** menolak fallback Telegram langsung dan memerlukan proksi untuk permintaan HTTP luaran. Mod fallback yang dipilih secara eksplisit membenarkan akses Telegram langsung selepas kelewatannya; mod terowong/VPN membenarkan laluan langsung. Memilih mod terowong tidak memasang atau mengesahkan VPN. Tetapan ini tidak mengawal semua trafik mesin, pelayar, pengurus pakej atau penyelesaian DNS hos proksi tempatan.

MTProxy hanya membawa trafik Telegram. Permintaan luaran boleh menggunakan proksi SOCKS5/HTTP berasingan, laluan SOCKS5/HTTP ruang kerja, atau laluan terus yang dibenarkan; ia juga boleh dilumpuhkan. Saksi bebas mempunyai tetapan pengangkutan tersendiri. Pengesahan CONNECT SOCKS5/HTTP biasa tidak disulitkan oleh protokol proksi tersebut itu sendiri. Rahsia MTProxy TLS palsu masih tidak disokong.

## Log masuk dan import sesi

Fail .tgwitness-session yang diubah suai mengandungi rahsia kebenaran teks biasa sehingga dimuat dan disimpan dalam peti besi. CLI luar talian menerima skema Telethon yang telah disemak. Panel import juga menerima Pyrogram SQLite, TData ZIP akaun tunggal moden, dan input JSON yang didokumenkan. Ia disahkan, terhad kepada empat fail / 8 MiB, dan memproses muat naik dalam memori tanpa mengekstrak arkib atau menyimpan fail asal. Butiran pengesahan yang telah dinormalisasi hanya dikembalikan kepada pelayar yang disahkan yang membuat permintaan; ia disimpan dalam peti besi yang disulitkan selepas pengesahan Telegram berjaya. Lindungi fail asal dan fail yang telah ditukar, dan elakkan klien serentak menyalin kebenaran.

Pemprosesan TData mengesahkan checksum kontena, has rat pengekodan semula tempatan, dan panjang struktur. Kod laluan tempatan Desktop yang dibekalkan digunakan secara sementara dan tidak disimpan. Penganalisis terhad ini tidak menyatakan bahawa setiap versi Desktop adalah serasi. Imej QR dijana secara tempatan, mengandungi token log masuk Telegram yang singkat tempohnya, dan tidak pernah dihantar ke perkhidmatan paparan luaran. Kunci, pertukaran ruang kerja, log masuk baru, dan perubahan laluan membatalkan percubaan QR yang tertangguh. Memuat semula/menutup tab mungkin menyebabkan percubaan masih tertangguh sehingga tamat tempoh. Log masuk QR yang berjaya masih menguatkuasakan pengikatan akaun. Badan API biasa kekal terhad kepada 16 KiB; laluan import yang disahkan menerima sehingga 12 MiB JSON yang disulit, dengan menguatkuasakan had fail terdekod yang lebih kecil secara berasingan.

Kod log masuk dan kata laluan pengesahan dua langkah Telegram tidak disimpan. Status nombor telefon/kod-hash disimpan dalam memori semasa kebenaran. Sesi Telegram memberikan akses akaun; jangan sekali-kali memuat naik direktori data, sesi, token, kunci peti, atau kunci tandatangan peribadi ke GitHub.

## Logs dan penghantaran

Tindak balas pengesahan API lalai diganti supaya ia tidak memantulkan nilai kelayakan. Log akses aplikasi dilumpuhkan. Jangan tetapkan proksi terbalik untuk melogkan tajuk Autentikasi atau badan permintaan. HTTP membawa token dan rahsia log masuk dalam teks biasa: gunakan HTTPS atau terowong SSH setiap kali meninggalkan localhost.

## Had integriti

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## Jika anda mengesyaki terdapat masalah

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
