# Penyebaran

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/

Jalankan TgWitness sebagai perkhidmatan pada Windows, Linux, macOS atau Docker, di sebalik HTTPS, dengan sandaran dan kemas kini.

**Inggeris** · [Bahasa Rusia](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Bahasa Ukraine](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Sepanyol](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Portugis (Brazil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Bahasa Turki](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [Bahasa Arab](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [Bahasa Parsi](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Bahasa Vietnam](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Teks ringkas Cina](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Pilih pemasangan

Untuk pakej mudah alih, ekstrak `TgWitness-<version>-windows-amd64-portable.zip` daripada GitHub Releases. Untuk kaedah lain, muat turun dan ekstrak fail ZIP sumber atau klon repositori, kemudian jalankan arahan berikut dari direktori projek:

| Pemasangan | Mula | Berjalan di latar belakang? |
| --- | --- | --- |
| Pakej mudah alih Windows | `TgWitness.cmd` | Tidak; biarkan tetingkap terbuka. |
| Windows asli | `Start.cmd` | Tidak; gunakan tugas logon pilihan untuk penggunaan latar belakang. |
| Bawaan Linux/macOS | `sh start.sh` | Tidak; gunakan systemd/launchd untuk kegunaan latar belakang. |
| Docker pada mana-mana hos yang disokong | `docker compose up -d --build --wait` | Ya, selagi daemon Docker berjalan. |
| Pembantu Docker di Windows | `scripts\Docker.cmd` | Ya; pembantu menunggu kesihatan pelayan web. |
| Pembantu Docker pada Linux/macOS | `sh scripts/docker-start.sh` | Ya; pembantu menunggu kesihatan pelayan web. |

Untuk pelayan awan yang boleh disemak oleh pihak ketiga — dicipta melalui API penyedia, tanpa SSH, hanya boleh diakses melalui Terowong Cloudflare — lihat [penyebaran jaminan tinggi](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md).

Perisian asli mencipta `.venv` peribadi dan memasang kebergantungan yang dilampirkan. Docker membinanya di dalam imej, tanpa memerlukan Python hos. Persediaan kali pertama perlu akses Internet. Apabila tiada Python 3.11+ ditemui, `Start.cmd` akan bertanya sebelum memasang Python 3.12 untuk pengguna Windows semasa (winget, jika tidak, pemuat turun python.org selepas memeriksa tandatangan Python Software Foundation); ia tidak pernah meminta keistimewaan pentadbir. Docker dan perkhidmatan OS kekal sebagai prasyarat.

Pemasangan asli dan mudah alih menggunakan `data/live` di dalam folder mereka. Docker menggunakan volum bernama `tgwitness-data` di `/data`. Ini adalah pemasangan berasingan sehingga anda secara sengaja memindahkan direktori data lengkap. Jangan jangkakan kontena Docker baru akan menemui akaun asli secara automatik.

## Keperluan pemasangan

Pemasangan asli memerlukan Python 3.11 atau yang lebih baru dengan `venv` dan `ensurepip`, capaian Internet untuk pemasangan kebergantungan pertama, dan direktori projek yang boleh ditulis untuk `.venv`. Panel terbungkus tidak memerlukan Node.js atau pembinaan frontend. Jalankan pelancar dari akaun OS biasa anda; keistimewaan pentadbir/root tidak diperlukan oleh TgWitness.

- **Windows:** `Start.cmd` memeriksa `py -3`, kemudian `python`, kemudian folder pemasangan lalai bagi setiap pengguna dan Program Files, dan memerlukan versi 3.11 atau lebih baru. Jika tiada satu pun berfungsi, ia menawarkan pemasangan automatik bagi setiap pengguna seperti yang diterangkan di atas. `py -3 start.py` juga berfungsi. Pakej mudah alih tidak memerlukan Python langsung.
- **Linux:** `start.sh` mencuba `python3.13`, `python3.12`, `python3.11`, `python3` dan `python`, dan mencetak arahan pemasangan untuk apt, dnf, pacman, zypper, apk atau Homebrew apabila tiada yang sesuai. Pemasangan Debian/Ubuntu mungkin memerlukan pakej `python3-venv` yang sepadan dengan penafsir yang dipilih. Python lalai yang lebih lama pada sesuatu pengedaran perlu digantikan atau dilengkapi dengan Python 3.11+.
- **macOS:** pasang pengedaran Python 3.11+ terkini; jangan anggap penyahkod yang disediakan oleh OS memenuhi keperluan. Gunakan `python3 start.py` daripada direktori projek.
- **Docker:** gunakan Docker Engine/Desktop dengan Compose v2.20 atau lebih baru. Docker Desktop mesti menggunakan kontena Linux pada Windows. Kontena ini memasang kebergantungan Pythonnya sendiri; hos tidak memerlukan pemasangan Python berasingan.

Gunakan storan tempatan berterusan untuk direktori data. Rancang kapasiti berdasarkan mesej, media, pertumbuhan WAL, eksport dan sandaran; tiada spesifikasi minimum universal berasaskan bukti untuk cakera/RAM bagi setiap beban kerja. Seni bina CPU dan versi Python tanpa roda kebergantungan yang serasi mungkin memerlukan alat pembinaan tambahan dan kelayakan tersendiri. "Portable" bukan tuntutan sokongan OS atau perkakasan sejagat.

Windows 11/Python 3.12 telah disahkan secara tempatan. Definisi Linux/macOS/kontena dan CI disediakan tetapi belum dijalankan pada hos pembangunan ini. Lihat [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) untuk skop yang tepat.

## Komputer tempatan

Gunakan `Start.cmd` pada Windows atau `sh start.sh` pada Linux/macOS. `scripts\Setup.cmd` atau `sh start.sh --setup-only` menyediakan persekitaran. Pelancar memasang kebergantungan pada penggunaan pertama; pelancaran kemudian menggunakan semula persekitaran tersebut. Akses internet diperlukan untuk penyediaan dan pengumpulan Telegram, tetapi melayari rekod sedia ada dan mencipta eksport berfungsi secara luar talian.

Jalankan `python start.py --check` selepas pemasangan untuk memeriksa kebergantungan tempatan, Ed25519, penyimpanan, konfigurasi kunci dan alamat pendengar tanpa memulakan pengumpul. Gunakan `--json` untuk keluaran berstruktur. Jalankan `--data-dir`, `--host` dan `--port` yang dimaksudkan. Semakan ini tidak memasang pakej, mencipta jurnal atau menyambung ke Telegram; ia bukan kelayakan integriti atau liputan. Permulaan secara berasingan mengesahkan jurnal sedia ada. `python start.py --help` juga mengelakkan pemasangan.

Pilihan:

Selepas menggunakan start.py, jalankan arahan sampingan dengan `.venv\Scripts\python.exe` pada Windows atau `.venv/bin/python` pada Linux/macOS, atau aktifkan persekitaran tersebut terlebih dahulu. Contoh `python -m ...` di bawah menganggap persekitaran tersebut sudah aktif.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Pembolehubah persekitaran: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE memilih mod kunci luaran untuk pemasangan baru; lihat di bawah. TGWITNESS_TOKEN, jika disediakan, mesti mengandungi sekurang-kurangnya 24 aksara; gunakan nilai rawak kriptografi. Tanpa ia, aplikasi akan menjana token rawak 256-bit dalam panel-token.txt. Penimpaan persekitaran tidak menulis semula fail tersebut. Mulakan semula untuk menukar kelayakan.

Persis satu proses sahaja boleh memiliki direktori data. Kunci fail sistem operasi rentas platform menghalang penulis serentak secara tidak sengaja. Gunakan satu pekerja Uvicorn. Panel boleh mengurus sebarang bilangan ruang kerja, dengan direktori ruang kerja tambahan di bawah profiles/<id>/. Untuk instans perkhidmatan berasingan, gunakan direktori dan port berasingan. Fail WAL SQLite harus disimpan pada storan kekal tempatan, bukan pada sistem fail rangkaian. Jangan kongsi satu volum antara replika.

## Pakej mudah alih Windows

Setiap Pelepasan GitHub mengandungi `TgWitness-<version>-windows-amd64-portable.zip` dan `.sha256`. Ia mengandungi runtime Python 3.12 rasmi yang boleh disematkan daripada python.org (checksum dipaku dalam `tools/build_portable.py`), TgWitness dan kebergantungannya yang dipaku, dan tiga pelancar:

| Fail | Tujuan |
| --- | --- |
| `TgWitness.cmd` | Mulakan panel; pilihan tambahan dihantar, contohnya `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Mulakan demo sintetik di `data\demo` |
| `TgWitness-Check.cmd` | Jalankan pemeriksaan kesiapsiagaan tanpa memulakan |

Ekstrak keseluruhan arkib ke dalam folder yang boleh ditulis seperti `Documents\TgWitness`; jangan jalankan ia dari dalam ZIP atau dari Program Files. Runtime menggunakan laluan modul terasing, jadi pemasangan Python lain dan `PYTHONPATH` tidak menjejaskannya. Data kekal dalam folder `data` pada pakej ini. Untuk mengemas kini, hentikan TgWitness, ekstrak versi baru ke dalam folder baru dan salin folder `data`.

Bina sendiri pada Windows 64-bit dengan Python 3.12:

```
python tools/build_portable.py
```

Pembina mengesahkan checksum masa larian, memasang kebergantungan terhad ke dalam pakej, menjalankan pemeriksaan kesiapsiagaan dengan penafsir terbina dalam dan menulis fail ZIP serta checksum ke dalam `dist/`.

## Kontena

```
docker compose up -d --build --wait
```

Ini mencipta volum kekal bernama untuk /data. Pintu web dipetakan ke 127.0.0.1:8787. Proses ini dijalankan sebagai UID 10001 dengan keupayaan yang dikurangkan, sistem fail root hanya-baca, dan /data serta /tmp yang boleh ditulis. `--wait` memeriksa kesihatan pelayan web sebelum memulangkan; ia tidak menubuhkan kebenaran atau penghantaran Telegram. Pemacu bantuan yang disediakan menggunakan had masa kesiapsiagaan 180 saat selepas pembinaan. Muat turun kebergantungan awal mungkin mengambil masa lebih lama daripada itu.

Kedua-dua fail asas Compose menggunakan nama projek `tgwitness`, jadi mengekstrak keluaran baru ke direktori lain tidak akan secara senyap memilih volum data baru. Pastikan hanya satu penyebaran aktif untuk projek tersebut. Untuk pemasangan bebas, gunakan `docker compose -p NAME ...` yang unik dan port hos yang berbeza, serta kekalkan kedua-duanya semasa kemas kini. Untuk penyebaran lama yang menggunakan nama projek berbeza, teruskan menggunakan nama asal nya dengan `-p`; `docker compose ls` menyenaraikan projek sedia ada.

Salin `deploy/env.example` ke `.env` dan ubah `TGWITNESS_PORT` untuk menggunakan port loopback yang berbeza. Sebagai contoh, `TGWITNESS_PORT=8788` mendedahkan panel di `http://127.0.0.1:8788`; kontena masih mendengar di 8787. `.env` diabaikan oleh Git.

Dapatkan token awal:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Perintah berguna:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` memulakan semula pengumpul selepas kerosakan atau permulaan semula Docker daemon. Pada pelayan Linux, aktifkan Docker semasa but menggunakan pengurus perkhidmatan pengedaran anda, biasanya `sudo systemctl enable --now docker`. Pada Windows/macOS, aktifkan tetapan mulakan-semasa-log-masuk Docker Desktop. Log keluar desktop, tidur, atau pemberhentian daemon Docker boleh mengganggu pengumpulan. Kontena yang dihentikan secara eksplisit kekal berhenti sehingga anda memulakannya semula.

Volum /tmp dihadkan pada 512 MiB dalam konfigurasi contoh. Pembinaan eksport sebaliknya menggunakan `temporary-exports/` setiap ruang kerja pada /data berterusan. Tempah ruang di sana untuk eksport serentak, pertumbuhan jurnal/WAL, media dan sandaran. Pelancar menggunakan deploy/constraints.txt untuk menetapkan versi kebergantungan runtime yang layak. Docker dan pelayan jaminan tinggi dipasang daripada deploy/requirements.lock dan deploy/build.lock dengan pip --require-hashes: setiap fail pakej mesti sepadan dengan rekod SHA-256 yang direkodkan dalam komit, jadi fail yang digantikan di PyPI atau cerminan akan ditolak. Imej asas Python dan pek operasi sistem masih memerlukan kelayakan keluaran bebas.

Jangan gunakan docker compose down -v melainkan anda berniat memusnahkan jurnal dan kunci. Laporan kesihatan kontena melaporkan ketersediaan pelayan web, bukan perekodan Telegram yang berjaya. Periksa status pengumpul panel, degupan jantung, ralat, dan peristiwa liputan.

### Profil saksi bebas

Perkhidmatan pilihan `witness` menjalankan [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/) dalam kontena tersendiri, dengan kunci dan jurnal tersendiri dalam jilid `witness-data` dan hanya token saksi baca sahaja untuk pengumpul. Buat token pada halaman **Saksi** panel, tambahkan ia dengan token bot dan saluran ke `.env`, kemudian mulakan profil:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Perkhidmatan ini mencapai pengumpul di dalam rangkaian Compose di `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` mengutamakannya, contohnya `/profiles/<workspace ID>` untuk ruang kerja lain). Untuk saksi di pelayan berasingan yang diuruskan oleh orang lain, gunakan `deploy/compose/compose.witness.yaml` di sana dengan `TGWITNESS_WITNESS_COLLECTOR` ditetapkan kepada alamat HTTPS pengumpul; fail itu mengandungi saksi sahaja.

## Pasang imej yang diterbitkan

Ini akan tersedia selepas [aliran kerja pelepasan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/#automated-github-releases) berjaya dan konfigurasi pakej GHCR awam. Pemilik/nama repositori tidak di-hardcode ke dalam pokok sumber ini. Gunakan imej yang ditunjukkan dalam ringkasan aliran kerja pelepasan tersebut.

Salin `deploy/env.example` ke `.env`. Tetapkan `TGWITNESS_IMAGE` ke versi terbitan, menggunakan laluan repositori **huruf kecil**, contohnya:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

Jalankan fail ini sendiri, bukannya `compose.yaml`:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Tiada pembinaan sumber, Python, atau penyusun diperlukan pada hos. Aliran kerja pelepasan menyasarkan kontena Linux AMD64 dan ARM64, termasuk VM Linux Docker Desktop. Gunakan tag versi atau `ghcr.io/owner/repository@sha256:...` daripada ringkasan aliran kerja. Tiada tag `latest` yang bergerak atau peningkatan aplikasi tanpa pengawasan yang dikonfigurasikan. Imej dan varian sumber menggunakan volum data yang sama apabila nama projek mereka sepadan.

## HTTPS automatik pada pelayan

Gunakan pelayan dengan Docker, domain yang anda kawal, dan storan tempatan berterusan. Arahkan rekod A/AAAA domain ke pelayan; terbitkan AAAA hanya jika IPv6 sampai kepadanya. Benarkan masuk TCP 80 dan 443 serta keluar DNS/HTTPS untuk penerbitan sijil. Perkhidmatan lain tidak boleh sudah menggunakan port ini.

Salin `deploy/env.example` ke `.env` dan tetapkan nama hos, tanpa skema atau laluan:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Mulakan pembinaan sumber dengan lapisan HTTPS:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Untuk imej yang diterbitkan, gunakan `deploy/compose/compose.image.yaml` sebagai fail pertama sebaliknya. Simpan kedua-dua argumen `-f` untuk status, log, kemas kini, dan arahan henti kemudian.

Caddy memperoleh dan memperbaharui sijil, mengalihkan HTTP ke HTTPS, dan meneruskan permintaan kepada pengumpul di rangkaian Compose persendirian. Status sijil mempunyai volum kekal tersendiri. Port hos langsung pengumpul kekal hanya untuk loopback. Konfigurasi Caddy yang disediakan tidak mengaktifkan log akses.

Buka `https://watch.your-domain.org` dan masukkan token panel. Keadaan sedia tidak mengesahkan penerbitan sijil atau kebolehcapaian luaran. Jika HTTPS tidak sedia, periksa DNS, peraturan tembok api, dan:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Imej Caddy yang disediakan mengikuti tag `2-alpine`. Tarikan akan menyegarkan semula imej tersebut; pasangkan digest yang telah diuji dalam penyebaran anda jika anda memerlukan versi infrastruktur tetap.

## Kemas kini dan sandaran

Memelihara nama projek Compose dan volum data merentas kemas kini. Pertama, hentikan pengumpul dan buat sandaran lengkap. Untuk penyebaran berasaskan sumber lalai:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Gunakan destinasi sandaran baharu setiap kali, di luar repositori, dan lindungi ia sebagai bahan capaian akaun. Laluan contoh adalah untuk ilustrasi; gunakan lokasi sandaran peribadi anda. Salin keseluruhan direktori, termasuk fail tersembunyi, semua ruang kerja, kunci, jurnal, dan media. Sandarkan kunci induk peti keselamatan luaran secara berasingan jika dikonfigurasikan. Fail ZIP bukti bukan sandaran aplikasi yang boleh dipulihkan. Untuk HTTPS, juga pelihara jumlah Caddy jika anda perlu mengekalkan status sijil/akaunnya.

Untuk penyebaran sumber, peroleh fail keluaran baru dan jalankan:

```
docker compose up -d --build --wait
```

Untuk penyebaran imej, ubah `TGWITNESS_IMAGE` kepada versi yang diingini, kemudian jalankan:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Gunakan fail Compose pemasangan anda juga untuk arahan stop/copy sebelumnya. Pastikan `.env`, konfigurasi tersuai, dan nama projek yang sama. `down` mengekalkan volum bernama; **`down -v` memadamkannya**. Jangan salin `.venv` antara sistem operasi atau versi Python. Untuk kemas kini asli, hentikan TgWitness, buat sandaran direktori data penuhnya, gantikan fail sumber, dan jalankan `python start.py --setup-only` sebelum pelancaran.

Semak akses panel, identiti akaun, status pemerhatian, dan liputan selepas kemas kini. Memulakan semula tidak akan membina semula kemas kini Telegram yang terlepas. Rollback mungkin memerlukan sandaran pra-kemas kini jika versi akan datang mengubah format storan.

## Pelepasan GitHub automatik

[Aliran kerja pelepasan](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) sedia untuk digunakan selepas projek ini dihantar ke repositori GitHub dengan Actions diaktifkan. Ia berjalan apabila GitHub Release **diterbitkan**, termasuk prapelepasan. Draf dan penghantaran tag sahaja tidak menerbitkan pakej.

1. Aturkan versi pakej dan log perubahan, kemudian terbitkan rilisan yang ditandakan dengan `v` ditambah versi `pyproject.toml` yang tepat, seperti `v0.7.0`.
2. Aliran kerja mengesahkan tag dan menjalankan pemeriksaan Python yang dikongsi untuk Windows/Linux/macOS, pelayar umum/import akaun/QR, pakej sumber, dan Docker. Pemasangan asli baharu juga dijalankan pada ketiga-tiga sistem pengendalian menggunakan Python 3.12.
3. Selepas pemeriksaan tersebut lulus, ia menjalankan ujian asap pada imej ARM64 di bawah QEMU, menerbitkan imej AMD64/ARM64 ke `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, dan melampirkan fail ZIP sumber, checksum, dan roda Python pada keluaran. Satu tugas berasingan untuk Windows membina dan melampirkan ZIP mudah alih serta checksumnya.
4. Selepas penerbitan pertama, buka tetapan pakej GHCR dan tetapkan keterlihatan kepada **Awam** jika muat turun imej tanpa nama dimaksudkan. Repositori sumber awam sahaja tidak menjamin pakej kontena awam. Dasar organisasi mesti membenarkan penerbitan pakej. Aliran kerja ini menggunakan `GITHUB_TOKEN`; tiada kata laluan pendaftaran atau kelayakan VPS yang perlu dimasukkan ke dalam repositori.

Kejayaan aliran kerja jauh tidak dapat dipastikan melalui penyediaan tempatan ini. Emulasi ARM64 adalah pemeriksaan asap, bukan kelayakan perkakasan asli atau Telegram secara langsung. Ini mengautomasikan pembungkusan keluaran; memulakan pelayan masih memerlukan arahan Compose dan prasyarat domain/hosnya. Pelayan sedia ada tidak dinaik taraf atau dihidupkan semula secara senyap apabila keluaran diterbitkan.

## Pelayan jauh

Pastikan perkhidmatan terikat pada loopback dan gunakan terowong SSH, atau akhiri HTTPS pada proksi songsang. Fail Compose asas hanya untuk tempatan; lapisan tambahan pilihan `deploy/compose/compose.https.yaml` menyediakan Caddy untuk domain yang dikonfigurasikan. Pastikan token pembawa tidak termasuk dalam URL dan log proksi. Proksi songsang harus mengehadkan saiz permintaan dan kadar sambungan. Jangan dedahkan HTTP biasa kepada Internet.

Contoh untuk systemd, tugas logon Windows, ejen pengguna macOS dan Caddy disediakan dalam [deploy/.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Semak/sesuaikan laluan mereka sebelum pemasangan. Mereka adalah templat yang disediakan, bukan kualifikasi platform yang dijalankan secara tempatan. Tiada perkhidmatan atau tugas latar belakang didaftarkan oleh pelancar biasa.

Pada Windows, pelancaran `pythonw.exe` tanpa tetingkap menyimpan diagnostik permulaan/pelayan dalam `logs/server.log` di bawah direktori data (5 MiB setiap fail, dua sandaran berputar). Pelancaran konsol mengekalkan log konsol. Log akses HTTP dilumpuhkan dalam kedua-dua mod. Lindungi log dengan direktori data dan semak mereka sebelum dikongsi.

## Mula semula dan jurang

Negeri pemerhatian terakhir yang diminta dikekalkan. Jika pemerhatian aktif, permulaan cuba menyambung semula dan meneruskan sumber terpilih. Menangguhkan secara manual membatalkan niat tersebut. Permulaan semula yang gagal direkodkan dan dipaparkan di panel.

StringSession mengekalkan kebenaran tetapi bukan status entiti/kemas kini berterusan Telethon. Dialog dimuat semula semasa permulaan. Telegram/Telethon boleh memulihkan beberapa gangguan penghantaran semasa berjalan, tetapi TgWitness tidak mendakwa keupayaan main balik berterusan merentas permulaan semula proses. Setiap permulaan merekodkan kepala jurnal sebelumnya dan sempadan luar talian. Pemantau memeriksa sambungan setiap 10 saat dan menambah isyarat degupan jantung setiap minit (**Parameter → Rakam kelangsungan hidup setiap**). Gangguan ringkas mungkin terlepas; penghantaran yang bersambung tidak menjamin penghantaran kemas kini yang lengkap. Snapshot adalah pemerhatian sejarah semasa yang eksplisit, bukan pembaikan jurang.

Barisan media disimpan dalam pangkalan data SQLite setiap ruang kerja. Satu mesej dan tugasnya dikomit secara atomik. Tugas yang sedang berjalan dan terganggu akan dipulihkan untuk dicuba semula semasa permulaan. Setiap muat turun mempunyai masa tamat asas 120 saat ditambah masa pada kadar 256 KiB/s mengikut saiznya, dan had 1–2,000 MiB bagi setiap jenis lampiran; masa tamat, kelajuan dan percubaan semula berada di bawah **Parameter**. Pengumpul akan melangkau fail yang saiznya tidak diketahui. Menangguhkan mengekalkan kerja yang beratur. Cubaan semula menggunakan penerang fail asal yang diperhatikan, bukan versi terkini bagi mesej yang disunting kemudian. Kegagalan sementara mempunyai cubaan semula yang terhad; jeda FloodWait media akan terus berfungsi walaupun dimulakan semula. Pemulihan media adalah berasingan daripada pemulihan kemas kini Telegram dan tidak dapat mencipta semula fail yang hilang.

## Sandaran, pemulihan, dan kapasiti

Hentikan proses sebelum menyalin **keseluruhan direktori data**, termasuk vault.key, signing.enc, credentials.enc, fail pangkalan data SQLite/WAL, media, token, titik pemeriksaan, dan semua profil/subdirektori. Pulihkan salinan lengkap sementara perkhidmatan destinasi dihentikan. Ketiadaan kunci vault atau ketidakpadanan kunci penandatangan menyebabkan permulaan gagal; jangan menjana semula kunci untuk memaksa akses.

Simpan sandaran rahsia yang disulitkan dan dikawal capaian. Fail ZIP bukti adalah mudah alih semak artifak, bukan sandaran aplikasi atau sandaran sesi Telegram. Tiada pemadaman pengekalan automatik. Rancang ruang cakera untuk semua mesej, metadata mentah, media, eksport sementara, dan sandaran.

Pengesahan permulaan dan aliran rekod eksport, bukannya memuatkan keseluruhan jurnal. Eksport menetapkan tangkapan baca sementara penulisan WAL baru boleh diteruskan; eksport jangka panjang boleh mengekalkan halaman WAL, jadi kapasiti cakera masih penting. ZIP dihadkan kepada 4 GiB tanpa mampat untuk menyamai lalai pemeriksa bebas; **Parameter → Saiz ZIP terbesar yang ditandatangani** meningkatkan had, dan arkib seperti ini disahkan dengan `verify.py --max-gib N`. Format lain tiada had bilangan acara. Pelayar yang disokong menstrim ketulan respons ke fail pilihan pengguna. Pelayar lain menampan sehingga 128 MiB dan mengarahkan pemindahan yang lebih besar ke CLI yang disahkan:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Gunakan `--profile ID` daripada **Eksport → ID Ruang Kerja** untuk ruang kerja lain, `--format zip|jsonl|csv|html`, `--url https://your-server` untuk pelayan jauh, atau `--max-mib` untuk menukar had pemindahan 5 GiB. HTTP Biasa dibenarkan hanya untuk loopback. Token dihantar dalam pengepala, penalaan semula ditolak, fail sedia ada tidak ditimpa, dan muat turun yang tidak lengkap tidak diterbitkan sebagai fail siap. Jika TGWITNESS_TOKEN menimpa token yang dijana, gunakan fail yang dilindungi berasingan yang mengandungi nilai aktif tersebut: panel-token.txt tidak diubah semula oleh penimpaan. SHA-256 arahan hanyalah checksum pemindahan; sahkan sendiri ZIP yang ditandatangani.

Fail eksport pelayan kekal di dalam `temporary-exports/` peribadi setiap ruang kerja. Tindak balas yang berjaya akan membersihkan fail mereka. Eksport yang terhenti akan dialih keluar pada permulaan ruang kerja seterusnya dengan kunci instans eksklusifnya dipegang. Direktori ini adalah sebahagian daripada model ancaman/kapasiti penyimpanan; gunakan volum data yang disulitkan. Pemindahan berskala pengeluaran berbilang gigabait masih memerlukan kelayakan pada sistem sasaran anda.

Panel memaparkan media yang sedang menunggu/gagal, media tertua yang menunggu, ruang cakera kosong, jeda permintaan Telegram, dan sumber yang aksesnya belum disahkan. Diagnostik ini bukan pemantau penghantaran hujung-ke-hujung yang lengkap. Ruang kerja berkongsi proses; akaun yang bising masih boleh menjejaskan yang lain. Proses pekerja berasingan, pengekalan/pusingan, pemulihan kemas kini tahan lama dan kelayakan penyebaran penuh kekal. Akses panel terhad didokumenkan dalam [akses dan kebenaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/); checkpoint bebas dilindungi oleh [panduan saksi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/).

## Pilihan sambungan dan perlindungan

Rute sambungan adalah bagi setiap ruang kerja dan perlu dikonfigurasikan sebelum kebenaran. SOCKS5/HTTP CONNECT menggunakan kebergantungan python-socks yang dipasang. MTProxy menggunakan pengangkutan perantaraan rawak eksperimental Telethon; rahsia TLS palsu tidak disokong. Fallback langsung bergantung pada [mod IP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes) yang dipilih: Sembunyikan IP menolaknya; mod fallback eksplisit membenarkannya selepas kelewatan. Mod Terowong/VPN membenarkan laluan langsung tetapi tidak mewujudkan VPN. Ini bukan dasar rangkaian untuk seluruh sistem.

Untuk pemasangan baharu, TGWITNESS_VAULT_KEY_FILE menunjuk kepada fail kunci induk rawak yang dilindungi secara berasingan. Pasangkannya secara baca sahaja di luar /data dalam sebuah kontena. Peliharalah metadata garam vault.external.json awam bersama setiap ruang kerja dan kunci induk secara berasingan. Vault tempatan sedia ada memerlukan migrasi yang dirancang; menetapkan pembolehubah ini tidak akan menukarnya secara senyap. Penyimpanan dan eksport mesej/media tidak disulitkan oleh aplikasi. Gunakan volum yang disulitkan dan storan sementara peribadi yang mencukupi di mana diperlukan.

Prosedur terperinci: [sambungan/keselamatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) dan [mod operasi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/operations/).
