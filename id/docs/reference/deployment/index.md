# Penerapan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/

Jalankan TgWitness sebagai layanan di Windows, Linux, macOS, atau Docker, melalui HTTPS, dengan fitur pencadangan dan pembaruan.

**Bahasa Inggris** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ukraina](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Bahasa Turki](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Bahasa Vietnam](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Bahasa Mandarin (Sederhana)](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Pilih metode instalasi

Untuk paket portabel, ekstrak `TgWitness-<version>-windows-amd64-portable.zip` dari GitHub Releases. Untuk metode lainnya, unduh dan ekstrak berkas ZIP sumber atau kloning repositori, lalu jalankan perintah berikut dari direktori proyek:

| Instalasi | Mulai | Berjalan di latar belakang? |
| --- | --- | --- |
| Paket portabel untuk Windows | `TgWitness.cmd` | Tidak; biarkan jendela tetap terbuka. |
| Aplikasi asli Windows | `Start.cmd` | Tidak; gunakan tugas masuk opsional untuk penggunaan di latar belakang. |
| Dukungan asli untuk Linux/macOS | `sh start.sh` | Tidak; gunakan systemd/launchd untuk penggunaan di latar belakang. |
| Docker di host apa pun yang didukung | `docker compose up -d --build --wait` | Ya, selama daemon Docker sedang berjalan. |
| Pembantu Docker di Windows | `scripts\Docker.cmd` | Ya; program bantu tersebut menunggu status kesehatan server web. |
| Pembantu Docker di Linux/macOS | `sh scripts/docker-start.sh` | Ya; program bantu tersebut menunggu status kesehatan server web. |

Untuk server cloud yang dapat diperiksa oleh pihak ketiga — dibuat melalui API penyedia layanan, tanpa SSH, dan hanya dapat diakses melalui Cloudflare Tunnel — lihat [penerapan dengan jaminan tinggi](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md).

Proses startup asli membuat `.venv` pribadi dan menginstal dependensi yang disematkan. Docker membangunnya di dalam gambar, tanpa memerlukan Python host. Pengaturan pertama kali memerlukan akses internet. Jika Python 3.11+ tidak ditemukan, `Start.cmd` akan meminta izin sebelum menginstal Python 3.12 untuk pengguna Windows saat ini (menggunakan winget, atau jika tidak, penginstal python.org setelah memeriksa tanda tangan Python Software Foundation-nya); alat ini tidak pernah meminta hak akses administrator. Docker dan layanan sistem operasi tetap menjadi prasyarat.

Instalasi native dan portabel menggunakan `data/live` di dalam foldernya. Docker menggunakan volume bernama `tgwitness-data` di `/data`. Ini adalah instalasi terpisah hingga Anda secara sengaja memigrasikan direktori data secara keseluruhan. Jangan berharap kontainer Docker baru akan mendeteksi akun native secara otomatis.

## Persyaratan instalasi

Instalasi asli memerlukan Python 3.11 atau yang lebih baru dengan `venv` dan `ensurepip`, akses internet untuk instalasi dependensi pertama, serta direktori proyek yang dapat ditulis untuk `.venv`. Panel yang disertakan tidak memerlukan Node.js atau build frontend. Jalankan peluncur dari akun OS biasa Anda; TgWitness tidak memerlukan hak akses administrator/root.

- **Windows:** `Start.cmd` memeriksa `py -3`, lalu `python`, kemudian folder instalasi default per-pengguna dan Program Files, serta memerlukan versi 3.11 atau yang lebih baru. Jika tidak ada yang berhasil, maka akan ditawarkan instalasi otomatis per-pengguna seperti yang dijelaskan di atas. `py -3 start.py` juga berfungsi. Paket portabel sama sekali tidak memerlukan Python.
- **Linux:** `start.sh` mencoba `python3.13`, `python3.12`, `python3.11`, `python3`, dan `python`, serta menampilkan perintah instalasi untuk apt, dnf, pacman, zypper, apk, atau Homebrew jika tidak ada yang memenuhi syarat. Instalasi Debian/Ubuntu mungkin memerlukan paket `python3-venv` yang sesuai dengan interpreter yang dipilih. Python bawaan versi lama pada suatu distribusi harus diganti atau dilengkapi dengan Python 3.11+.
- **macOS:** instal distribusi Python 3.11+ terbaru; jangan berasumsi bahwa interpreter yang disediakan sistem operasi sudah memenuhi persyaratan. Gunakan `python3 start.py` dari direktori proyek.
- **Docker:** gunakan Docker Engine/Desktop dengan Compose v2.20 atau yang lebih baru. Docker Desktop harus menggunakan kontainer Linux di Windows. Kontainer tersebut menginstal ketergantungan Python-nya sendiri; host tidak memerlukan instalasi Python terpisah.

Gunakan penyimpanan lokal yang persisten untuk direktori data. Rencanakan kapasitas berdasarkan pesan, media, pertumbuhan WAL, ekspor, dan cadangan; tidak ada spesifikasi minimum disk/RAM universal berdasarkan bukti untuk setiap beban kerja. Arsitektur CPU dan versi Python yang tidak memiliki roda dependensi yang kompatibel mungkin memerlukan alat pembangunan tambahan dan kualifikasi tersendiri. "Portabel" bukanlah klaim dukungan universal terhadap sistem operasi atau perangkat keras.

Windows 11/Python 3.12 telah diverifikasi secara lokal. Definisi untuk Linux/macOS/kontainer serta CI telah disediakan, namun belum dijalankan di host pengembangan ini. Lihat [berkas VERIFICATION.md](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/) untuk cakupan yang tepat.

## Komputer lokal

Gunakan `Start.cmd` di Windows atau `sh start.sh` di Linux/macOS. `scripts\Setup.cmd` atau `sh start.sh --setup-only` mempersiapkan lingkungan. Peluncur akan menginstal dependensi pada penggunaan pertama; peluncuran selanjutnya akan menggunakan kembali lingkungan tersebut. Akses internet diperlukan untuk pengaturan dan pengumpulan pesan Telegram, namun penelusuran catatan yang ada dan pembuatan ekspor dapat dilakukan secara offline.

Jalankan `python start.py --check` setelah pengaturan untuk memeriksa dependensi lokal, Ed25519, penyimpanan, konfigurasi kunci, dan alamat pendengar tanpa memulai pengumpul. Gunakan `--json` untuk keluaran terstruktur. Jalankan `--data-dir`, `--host`, dan `--port` sesuai kebutuhan. Pemeriksaan ini tidak menginstal paket, membuat jurnal, atau menghubungkan Telegram; ini bukan penilaian integritas atau cakupan. Proses startup memverifikasi secara terpisah jurnal yang sudah ada. `python start.py --help` juga menghindari instalasi.

Opsi:

Setelah menjalankan start.py, jalankan perintah tambahan dengan `.venv\Scripts\python.exe` di Windows atau `.venv/bin/python` di Linux/macOS, atau aktifkan lingkungan tersebut terlebih dahulu. Contoh `python -m ...` di bawah ini mengasumsikan bahwa lingkungan tersebut sudah aktif.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Variabel lingkungan: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE memilih mode kunci eksternal untuk instalasi baru; lihat di bawah. TGWITNESS_TOKEN, jika disediakan, harus berisi setidaknya 24 karakter; gunakan nilai acak yang dihasilkan secara kriptografis. Tanpa itu, aplikasi akan menghasilkan token acak 256-bit di file panel-token.txt. Penggantian variabel lingkungan tidak akan menimpa file tersebut. Mulai ulang untuk merotasi kredensial.

Tepat satu proses saja yang boleh mengelola direktori data. Kunci file lintas platform OS mencegah penulisan bersamaan yang tidak disengaja. Gunakan satu pekerja Uvicorn. Panel dapat mengelola sejumlah ruang kerja, dengan direktori ruang kerja tambahan di bawah profiles/<id>/. Untuk instance layanan yang terpisah, gunakan direktori dan port yang terpisah. File WAL SQLite harus disimpan di penyimpanan lokal yang persisten, bukan di sistem berkas jaringan. Jangan berbagi satu volume di antara replika.

## Paket portabel untuk Windows

Setiap Rilis GitHub menyertakan `TgWitness-<version>-windows-amd64-portable.zip` dan `.sha256`-nya. Rilis tersebut berisi runtime Python 3.12 resmi yang dapat disematkan dari python.org (checksum yang disematkan dalam `tools/build_portable.py`), TgWitness beserta dependensinya yang disematkan, serta tiga peluncur:

| Berkas | Tujuan |
| --- | --- |
| `TgWitness.cmd` | Jalankan panel; opsi tambahan diteruskan, misalnya `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Jalankan demo sintetis di `data\demo` |
| `TgWitness-Check.cmd` | Jalankan pemeriksaan kesiapan tanpa memulai |

Ekstrak seluruh arsip ke folder yang dapat ditulis seperti `Documents\TgWitness`; jangan jalankan dari dalam ZIP atau dari Program Files. Runtime menggunakan jalur modul yang terisolasi, sehingga instalasi Python lain dan `PYTHONPATH` tidak memengaruhinya. Data tetap berada di folder `data` dalam paket tersebut. Untuk memperbarui, hentikan TgWitness, ekstrak versi baru ke folder baru, lalu salin folder `data` ke sana.

Buat sendiri di Windows 64-bit dengan Python 3.12:

```
python tools/build_portable.py
```

Pembangun memverifikasi checksum saat runtime, menginstal dependensi yang dibatasi ke dalam paket, menjalankan pemeriksaan kesiapan dengan interpreter tertanam, dan menulis berkas ZIP serta checksum ke `dist/`.

## Kontainer

```
docker compose up -d --build --wait
```

Ini membuat volume persisten bernama untuk /data. Port web dipetakan ke 127.0.0.1:8787. Proses ini berjalan sebagai UID 10001 dengan kapabilitas yang diturunkan, sistem file root yang hanya dapat dibaca, serta /data dan /tmp yang dapat ditulis. `--wait` memeriksa kesehatan server web sebelum kembali; ia tidak melakukan otentikasi atau pengiriman Telegram. Pembantu yang disediakan menggunakan batas waktu kesiapan 180 detik setelah proses pembangunan. Pengunduhan dependensi awal mungkin memakan waktu lebih lama dari itu.

Kedua berkas Compose dasar menggunakan nama proyek `tgwitness`, sehingga mengekstrak rilis baru ke direktori lain tidak secara otomatis memilih volume data baru. Pertahankan hanya satu penyebaran yang aktif untuk proyek tersebut. Untuk instalasi independen, gunakan `docker compose -p NAME ...` yang unik dan port host yang berbeda, serta pertahankan keduanya saat pembaruan. Untuk penyebaran yang lebih lama yang menggunakan nama proyek berbeda, lanjutkan menggunakan nama aslinya dengan `-p`; `docker compose ls` mencantumkan proyek-proyek yang ada.

Salin `deploy/env.example` ke `.env` dan ubah `TGWITNESS_PORT` agar menggunakan port loopback yang berbeda. Misalnya, `TGWITNESS_PORT=8788` menampilkan panel di `http://127.0.0.1:8788`; kontainer tersebut tetap mendengarkan di port 8787. `.env` diabaikan oleh Git.

Ambil token awal:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Perintah yang berguna:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` akan memulai ulang pengumpul setelah terjadi crash atau daemon Docker dimulai ulang. Pada server Linux, aktifkan Docker saat boot menggunakan pengelola layanan distribusi Anda, umumnya `sudo systemctl enable --now docker`. Pada Windows/macOS, aktifkan pengaturan "start-at-sign-in" di Docker Desktop. Keluar dari desktop, mode tidur, atau Docker daemon yang dihentikan dapat mengganggu proses pengumpulan data. Kontainer yang dihentikan secara eksplisit akan tetap dihentikan hingga Anda menjalankannya kembali.

Volume /tmp dibatasi hingga 512 MiB dalam konfigurasi contoh. Proses ekspor menggunakan `temporary-exports/` dari setiap ruang kerja pada direktori /data yang persisten. Sediakan ruang di sana untuk ekspor simultan, pertumbuhan jurnal/WAL, media, dan cadangan. Peluncur menggunakan deploy/constraints.txt untuk mengunci versi dependensi runtime yang memenuhi syarat. Server Docker dan server dengan jaminan tinggi diinstal dari `deploy/requirements.lock` dan `deploy/build.lock` dengan perintah `pip --require-hashes`: setiap berkas paket harus cocok dengan SHA-256 yang tercatat dalam commit, sehingga berkas yang diganti di PyPI atau cermin akan ditolak. Gambar dasar Python dan paket sistem operasi masih memerlukan kualifikasi rilis yang independen.

Jangan gunakan perintah `docker compose down -v` kecuali Anda bermaksud menghancurkan jurnal dan kunci tersebut. Laporan kesehatan kontainer menunjukkan ketersediaan server web, bukan keberhasilan penangkapan pesan Telegram. Periksa status pengumpul, detak jantung, kesalahan, dan peristiwa cakupan pada panel.

### Profil saksi independen

Layanan opsional `witness` menjalankan [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/) di dalam kontainernya sendiri, dengan kunci dan jurnal tersendiri di volume `witness-data` serta hanya memiliki token saksi yang hanya dapat dibaca untuk pengumpul. Buat token tersebut di halaman **Saksi** pada panel, tambahkan bersama token bot dan saluran ke `.env`, lalu jalankan profil:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Layanan ini terhubung ke pengumpul di dalam jaringan Compose di `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` menggantikannya, misalnya `/profiles/<workspace ID>` untuk ruang kerja lain). Untuk saksi di server terpisah yang dijalankan oleh pihak lain, gunakan `deploy/compose/compose.witness.yaml` di sana dengan `TGWITNESS_WITNESS_COLLECTOR` disetel ke alamat HTTPS pengumpul; berkas tersebut hanya berisi saksi.

## Instal gambar yang telah dipublikasikan

Fitur ini tersedia setelah [alur kerja rilis](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/#automated-github-releases) berhasil diselesaikan dan konfigurasi paket GHCR publik selesai. Nama pemilik repositori tidak terkodekan secara permanen dalam pohon sumber ini. Gunakan gambar yang ditampilkan dalam ringkasan alur kerja rilis tersebut.

Salin `deploy/env.example` ke `.env`. Atur `TGWITNESS_IMAGE` ke versi yang telah dipublikasikan, dengan menggunakan jalur repositori **huruf kecil**, misalnya:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

Jalankan berkas ini secara mandiri, bukan `compose.yaml`:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Tidak diperlukan build sumber, Python, atau kompiler di host. Alur kerja rilis ditujukan untuk kontainer Linux AMD64 dan ARM64, termasuk VM Linux di Docker Desktop. Gunakan tag versi atau `ghcr.io/owner/repository@sha256:...` dari ringkasan alur kerja. Tidak ada konfigurasi untuk pemindahan tag `latest` atau pembaruan aplikasi tanpa pengawasan. Variasi gambar dan sumber menggunakan volume data yang sama jika nama proyeknya sama.

## HTTPS otomatis di server

Gunakan server dengan Docker, domain yang Anda kendalikan, dan penyimpanan lokal yang persisten. Arahkan catatan A/AAAA domain ke server; publikasikan AAAA hanya jika IPv6 menjangkau server tersebut. Izinkan lalu lintas masuk TCP 80 dan 443 serta lalu lintas keluar DNS/HTTPS untuk penerbitan sertifikat. Layanan lain tidak boleh sudah menggunakan port-port ini.

Salin `deploy/env.example` ke `.env` dan tetapkan nama host, tanpa skema atau jalur:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Mulai proses kompilasi sumber dengan overlay HTTPS:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Untuk gambar yang dipublikasikan, gunakan `deploy/compose/compose.image.yaml` sebagai file pertama. Pertahankan kedua argumen `-f` untuk perintah status, log, pembaruan, dan hentikan di kemudian hari.

Caddy memperoleh dan memperbarui sertifikat, mengalihkan HTTP ke HTTPS, serta meneruskan permintaan ke pengumpul di jaringan Compose pribadi. Status sertifikat memiliki volume persisten tersendiri. Port host langsung pengumpul tetap hanya untuk loopback. Konfigurasi Caddy yang disediakan tidak mengaktifkan pencatatan akses.

Buka `https://watch.your-domain.org` dan masukkan token panel. Kesiapan pembuatan tidak menjamin penerbitan sertifikat atau aksesibilitas eksternal. Jika HTTPS belum siap, periksa DNS, aturan firewall, dan:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Gambar Caddy yang disediakan mengikuti tag `2-alpine`-nya. Melakukan pull akan memperbarui gambar tersebut; sematkan ringkasan yang telah diuji dalam deployment Anda jika Anda memerlukan versi infrastruktur yang tetap.

## Pembaruan dan pencadangan

Pertahankan nama proyek Compose dan volume data di seluruh pembaruan. Pertama, hentikan pengumpul dan buat cadangan lengkap. Untuk penyebaran berbasis sumber default:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Gunakan tujuan cadangan baru setiap kali, di luar repositori, dan lindungi sebagai materi yang memerlukan akses akun. Jalur contoh hanya sebagai ilustrasi; gunakan lokasi cadangan pribadi Anda. Salin seluruh direktori, termasuk file tersembunyi, semua ruang kerja, kunci, jurnal, dan media. Cadangkan kunci utama brankas eksternal secara terpisah jika telah dikonfigurasi. File ZIP bukti bukanlah cadangan aplikasi yang dapat dipulihkan. Untuk HTTPS, simpan juga volume Caddy jika Anda perlu mempertahankan status sertifikat/akunnya.

Untuk penerapan sumber, unduh berkas rilis terbaru dan jalankan:

```
docker compose up -d --build --wait
```

Untuk penerapan gambar, ubah `TGWITNESS_IMAGE` menjadi versi yang diinginkan, lalu jalankan:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Gunakan berkas Compose pada instalasi Anda untuk perintah stop/copy di atas juga. Pertahankan `.env`, konfigurasi khusus, dan nama proyek yang sama. `down` mempertahankan volume yang diberi nama; **`down -v` menghapusnya**. Jangan menyalin `.venv` antar sistem operasi atau versi Python. Untuk pembaruan asli, hentikan TgWitness, buat cadangan direktori data lengkapnya , ganti berkas sumber, dan jalankan `python start.py --setup-only` sebelum meluncurkan.

Periksa akses panel, identitas akun, status pemantauan, dan cakupan setelah pembaruan. Memulai ulang tidak akan memulihkan pembaruan Telegram yang terlewat. Pengembalian ke versi sebelumnya mungkin memerlukan cadangan sebelum pembaruan jika versi mendatang mengubah format penyimpanan.

## Rilis otomatis di GitHub

[Alur kerja rilis](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) siap digunakan setelah proyek ini di-push ke repositori GitHub dengan Actions diaktifkan. Alur kerja ini berjalan saat Rilis GitHub **diterbitkan**, termasuk prarilis. Draf dan push tag saja tidak akan menerbitkan paket.

1. Tentukan versi paket dan catatan perubahan, lalu terbitkan rilis yang diberi tag `v` ditambah versi `pyproject.toml` yang tepat, seperti `v0.7.0`.
2. Alur kerja ini memvalidasi tag dan menjalankan pemeriksaan Python yang dapat digunakan di Windows/Linux/macOS, general/account-import/QR browser, paket sumber, dan Docker. Instalasi asli yang baru juga dilakukan pada ketiga sistem operasi tersebut menggunakan Python 3.12.
3. Setelah pemeriksaan tersebut lulus, sistem ini melakukan uji coba awal (smoke test) terhadap gambar ARM64 di bawah QEMU, mempublikasikan gambar AMD64/ARM64 ke `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, serta melampirkan berkas ZIP sumber, checksum, dan Python wheel ke dalam rilis. Sebuah tugas terpisah di Windows membangun dan melampirkan berkas ZIP portabel beserta checksum-nya.
4. Setelah publikasi pertama, buka pengaturan paket GHCR dan atur visibilitas menjadi **Publik** jika dimaksudkan untuk pengunduhan gambar secara anonim. Repositori sumber terbuka saja tidak menjamin paket kontainer yang terbuka. Kebijakan organisasi harus mengizinkan publikasi paket. Alur kerja ini menggunakan `GITHUB_TOKEN`; kata sandi registri atau kredensial VPS tidak boleh disimpan di repositori.

Keberhasilan alur kerja jarak jauh belum dapat dipastikan melalui persiapan lokal ini. Emulasi ARM64 hanyalah uji coba awal, bukan kualifikasi perangkat keras asli atau Telegram yang berjalan secara langsung. Ini mengotomatiskan pengemasan rilis; memulai server masih memerlukan perintah Compose serta prasyarat domain/host-nya. Server yang sudah ada tidak akan di-upgrade atau di-restart secara otomatis saat rilis diterbitkan.

## Server jarak jauh

Jaga agar layanan tetap terikat pada loopback dan gunakan terowongan SSH, atau hentikan HTTPS di proksi terbalik. Berkas Compose dasar hanya berlaku secara lokal; overlay `deploy/compose/compose.https.yaml` opsional menyediakan Caddy untuk domain yang telah dikonfigurasi. Jaga agar token bearer tidak muncul di URL dan log proxy. Proksi terbalik harus membatasi ukuran permintaan dan laju koneksi. Jangan mengekspos HTTP biasa ke Internet.

Contoh untuk systemd, tugas masuk Windows, agen pengguna macOS, dan Caddy disediakan di [folder deploy/.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Periksa/sesuaikan jalurnya sebelum instalasi. Ini adalah templat yang disediakan, bukan konfigurasi platform yang dijalankan secara lokal. Tidak ada layanan latar belakang atau tugas yang didaftarkan oleh peluncur standar.

Di Windows, peluncuran `pythonw.exe` tanpa jendela menyimpan diagnostik startup/server di `logs/server.log` di bawah direktori data (5 MiB per file, dua cadangan yang digilir). Peluncuran konsol tetap menyimpan log konsol. Pencatatan akses HTTP dinonaktifkan di kedua mode tersebut. Lindungi log dengan direktori data dan tinjau terlebih dahulu sebelum membagikannya.

## Mulai ulang dan celah

Status pengamatan terakhir yang diminta akan disimpan. Jika pengamatan sedang aktif, saat startup akan mencoba terhubung kembali dan melanjutkan sumber-sumber yang dipilih. Penundaan manual akan menghapus niat tersebut. Kegagalan restart akan dicatat dan ditampilkan di panel.

StringSession mempertahankan otorisasi tetapi tidak mempertahankan status pembaruan/entitas Telethon yang tahan lama. Dialog dimuat ulang saat dimulai. Telegram/Telethon dapat memulihkan beberapa gangguan transmisi saat berjalan, tetapi TgWitness tidak menjamin pemutaran ulang yang tahan lama setelah proses dimulai ulang. Setiap kali dimulai, sistem mencatat kepala jurnal sebelumnya dan batas offline. Monitor memeriksa konektivitas setiap 10 detik dan menambahkan sinyal detak jantung setiap menit (**Parameter → Liveness record every**). Gangguan singkat mungkin terlewatkan; koneksi transportasi yang terhubung tidak menjamin pengiriman pembaruan yang lengkap. Snapshot merupakan pengamatan riwayat terkini yang eksplisit, bukan perbaikan celah.

Antrian media disimpan dalam basis data SQLite masing-masing ruang kerja. Sebuah pesan dan tugasnya dikerjakan secara atomik. Tugas yang sedang berjalan dan terputus akan dipulihkan untuk dicoba kembali saat dimulai. Setiap unduhan memiliki batas waktu dasar 120 detik ditambah waktu sesuai kecepatan 256 KiB/s berdasarkan ukurannya, serta batas 1–2.000 MiB per jenis lampiran; batas waktu, kecepatan, dan upaya ulang diatur di **bagian Parameter**. Pengumpul melewati berkas yang ukurannya tidak diketahui. Menjeda akan mempertahankan pekerjaan yang sedang dalam antrian. Percobaan ulang menggunakan deskriptor berkas asli yang teramati, bukan versi terbaru dari pesan yang telah diedit setelahnya. Kegagalan sementara memiliki batasan percobaan ulang; jeda FloodWait media tetap berlaku setelah restart. Pemulihan media terpisah dari pemulihan pembaruan Telegram dan tidak dapat membuat ulang berkas yang hilang.

## Pencadangan, pemulihan, dan kapasitas

Hentikan proses sebelum menyalin **seluruh direktori data**, termasuk vault.key, signing.enc, credentials.enc, file basis data SQLite/WAL, media, token, titik pemeriksaan, serta semua profil/subdirektori. Kembalikan salinan lengkap tersebut saat layanan tujuan dalam keadaan berhenti. Kunci vault yang hilang atau ketidaksesuaian kunci penandatanganan akan menyebabkan kegagalan saat memulai; jangan membuat ulang kunci untuk memaksa akses.

Simpan cadangan rahasia dalam bentuk terenkripsi dan dengan kontrol akses. Berkas ZIP bukti bersifat portabel; tinjau artefak, bukan cadangan aplikasi atau cadangan sesi Telegram. Tidak ada penghapusan otomatis berdasarkan masa retensi. Rencanakan ruang disk untuk semua pesan, metadata mentah, media, ekspor sementara, dan cadangan.

Memulai verifikasi dan mengekspor catatan aliran alih-alih memuat seluruh jurnal. Ekspor mengunci snapshot yang telah dibaca sementara penulisan WAL baru dapat terus berlanjut; ekspor yang berlangsung lama dapat menyimpan halaman WAL, sehingga kapasitas disk tetap menjadi pertimbangan. Ukuran ZIP dibatasi hingga 4 GiB dalam bentuk tidak terkompresi agar sesuai dengan pengaturan default verifikator independen; **Parameter → ZIP Tertanda Terbesar** meningkatkan batas tersebut, dan arsip semacam itu diverifikasi dengan `verify.py --max-gib N`. Format lain tidak memiliki batas jumlah peristiwa. Browser yang didukung mengalirkan potongan respons ke berkas yang dipilih pengguna. Browser lain menyimpan dalam buffer maksimal 128 MiB dan mengarahkan transfer yang lebih besar ke CLI yang terotentikasi:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Gunakan `--profile ID` dari **Ekspor → ID Ruang Kerja** untuk ruang kerja lain, `--format zip|jsonl|csv|html`, `--url https://your-server` untuk server jarak jauh, atau `--max-mib` untuk mengubah batas transfer 5 GiB. HTTP biasa hanya diizinkan untuk loopback. Token dikirim melalui header, pengalihan ditolak, file yang sudah ada tidak ditimpa, dan unduhan yang belum selesai tidak dipublikasikan sebagai file yang sudah selesai. Jika TGWITNESS_TOKEN menggantikan token yang dihasilkan, gunakan berkas yang dilindungi secara terpisah yang berisi nilai aktif tersebut: panel-token.txt tidak akan ditimpa oleh penggantian tersebut. SHA-256 perintah ini hanyalah checksum transfer; verifikasi ZIP yang ditandatangani secara independen.

File ekspor server tetap berada di dalam direktori `temporary-exports/` pribadi masing-masing ruang kerja. Respons yang berhasil akan membersihkan berkas-berkasnya. Ekspor yang terputus akan dihapus pada pengaktifan ruang kerja berikutnya saat kunci instans eksklusifnya masih berlaku. Direktori ini merupakan bagian dari model ancaman/kapasitas penyimpanan; gunakan volume data terenkripsi. Transfer berskala produksi berukuran multi-gigabyte masih memerlukan pengujian pada sistem target Anda.

Panel menampilkan media yang sedang dalam antrian/gagal, media tertunda tertua, ruang disk kosong, jeda permintaan Telegram, dan sumber yang aksesnya belum dikonfirmasi. Diagnostik ini bukanlah pemantau pengiriman end-to-end yang lengkap. Ruang kerja berbagi proses; akun yang aktif masih dapat memengaruhi yang lain. Proses pekerja terpisah, retensi/rotasi, pemulihan pembaruan yang tahan lama, serta kualifikasi penerapan penuh tetap berlaku. Akses panel yang dibatasi didokumentasikan dalam [bagian akses dan izin](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/); titik pemeriksaan independen dijelaskan dalam [panduan saksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/).

## Opsi koneksi dan perlindungan

Rute koneksi ditentukan per ruang kerja dan harus dikonfigurasi sebelum otorisasi. SOCKS5/HTTP CONNECT menggunakan dependensi python-socks yang disematkan. MTProxy menggunakan transportasi perantara acak eksperimental dari Telethon; rahasia TLS palsu tidak didukung. Pengalihan langsung bergantung pada [mode IP](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/#ip-modes) yang dipilih: Mode "Hide IP" menolaknya; mode pengalihan eksplisit mengizinkannya setelah penundaan. Mode "Tunnel/VPN" mengizinkan rute langsung tetapi tidak membuat VPN. Ini bukanlah kebijakan jaringan yang berlaku secara sistem.

Untuk instalasi baru, TGWITNESS_VAULT_KEY_FILE mengarah ke berkas kunci utama acak yang dilindungi secara terpisah. Pasang berkas tersebut dalam mode baca-saja di luar direktori /data dalam sebuah kontainer. Simpan metadata salt publik vault.external.json secara terpisah untuk setiap ruang kerja dan kunci utama. Brankas lokal yang sudah ada memerlukan migrasi terencana; pengaturan variabel ini tidak akan mengonversinya secara otomatis. Penyimpanan pesan/media serta ekspornya tidak dienkripsi oleh aplikasi. Gunakan volume terenkripsi dan penyimpanan sementara pribadi yang memadai jika diperlukan.

Prosedur terperinci: [koneksi/keamanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) dan [mode operasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/operations/).
