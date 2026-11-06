# Instal, verifikasi, dan perbarui

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/

Instal dengan satu perintah, periksa tanda tangan dan hash, perbarui, dan hapus instalasi.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Proyek](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Panduan cepat](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/) · [Penerapan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/)

**On this page**

- [Install with one command](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#install-with-one-command)
- [Where everything runs](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#where-everything-runs)
- [Full-text search settings](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#full-text-search-settings)
- [Command-line access](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#command-line-access)
- [Verify before running](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#verify-before-running)
- [Update an existing installation](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#update-an-existing-installation)
- [Everyday commands on Ubuntu](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#everyday-commands-on-ubuntu)
- [Remove TgWitness](https://phishdestroy.github.io/TgWitness/id/docs/reference/installation/#remove-tgwitness)

## Instal dengan satu perintah

Penginstal terpandu ini mencakup runtime Python pribadi. Gunakan alamat yang sama untuk penginstalan di masa mendatang: setiap publikasi memperbarui penginstal, hash, tanda tangan, dan informasi build secara bersamaan.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Di server Ubuntu, jalankan sebagai root untuk menginstal layanan latar belakang. Di desktop, jalankan sebagai pengguna biasa.

**Windows (PowerShell atau Command Prompt):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Tidak diperlukan administrator di Windows. Proses PowerShell anak akan membiarkan terminal Anda tetap terbuka dengan hasilnya. Python dan dependensinya tetap berada di dalam instalasi.

Di Ubuntu, pilih **"Komputer ini**", **"Tautan HTTPS sementara"**, atau "**Domain sendiri**". Penginstal akan menampilkan alamat panel dan kunci akses. Untuk tautan sementara, buka alamat HTTPS tersebut di browser Anda dan masukkan kuncinya. Untuk akses lokal pada server jarak jauh, gunakan pengalihan SSH dari komputer Anda (`ssh -L 8787:127.0.0.1:8787 user@server`) dan buka `http://127.0.0.1:8787`. Di macOS dan Windows, panel lokal akan terbuka di browser Anda; biarkan terminalnya tetap berjalan.

Masuk ke Telegram di panel dan pilih apa yang ingin dikumpulkan. Instalasi saja tidak akan memulai pengumpulan data Telegram.

## Tempat semuanya berjalan

`get.destroy.tools` adalah **Cloudflare Worker yang melayani unduhan statis**. Alat ini tidak memiliki panel TgWitness, sesi Telegram, atau basis data bukti pengguna. Alat ini tidak diarahkan ke VPS proyek. Aplikasi ini berjalan di mesin tempat Anda menjalankan perintah tersebut.

| Instalasi | Program | Data |
| --- | --- | --- |
| Ubuntu sebagai root | `/opt/tgwitness` | Layanan sistem: `/var/lib/tgwitness-<installation ID>`; gunakan `tgwitness paths` untuk jalur yang tepat. |
| Pengguna Linux / macOS | `~/.local/share/tgwitness` | `data/live` di bawah instalasi tersebut. |
| Pengguna Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` di bawah instalasi tersebut. |

Pilih `TGWITNESS_INSTALL_DIR` untuk memilih folder lain. Versi yang terinstal dan datanya terpisah. Penginstal tidak mengunggah akun, pesan, atau kunci Anda ke situs unduhan. Memilih terowongan Cloudflare akan mengarahkan lalu lintas panel melalui Cloudflare; menggunakan domain Anda sendiri akan mengarahkannya ke server Anda sendiri.

Setiap instalasi mencakup berkas **START-HERE.html** dan **START-HERE.txt**, yang berisi jalur lokal, perintah, dan tautan ke repositori. Jalankan `tgwitness guide` untuk membuka panduan. Di Windows, gunakan `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` di PowerShell.

## Pengaturan pencarian teks lengkap

[Pencarian teks lengkap](https://phishdestroy.github.io/TgWitness/id/docs/reference/search/) (pratinjau) tidak memerlukan pengaturan. Indeksnya dibangun di latar belakang setelah pembaruan.

| Variabel atau perintah | Efek |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Secara default: indeks disimpan di `search/fulltext.sqlite3` setiap ruang kerja |
| `TGWITNESS_FULLTEXT=memory` | Tidak ada berkas indeks; indeks dibangun ulang setiap kali aplikasi dimulai |
| `TGWITNESS_FULLTEXT=off` | Tanpa indeks; hanya pencarian teks persis |
| `tgwitness index status` | Indeks status setiap ruang kerja |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Bangun ulang setiap indeks dari jurnal yang ditandatangani |

Pilihan administrator di **Jurnal → Filter → Indeks Pencarian** akan menggantikan variabel untuk ruang kerja tersebut. Perintah akan mencari direktori data dari instalasi yang menjalankannya; di tempat lain, tambahkan `--data-dir` dengan jalur dari `tgwitness paths`. Untuk kamus bahasa Ukraina lengkap (data GPL-3.0), instal `pymorphy3-dicts-uk` di lingkungan Python instalasi tersebut.

## Akses baris perintah

[Baris](https://phishdestroy.github.io/TgWitness/id/docs/reference/cli/) [perintah](https://phishdestroy.github.io/TgWitness/id/docs/reference/cli/) (pratinjau) membaca arsip untuk skrip dan agen.

| Variabel | Efek |
| --- | --- |
| `TGWITNESS_URL` | Alamat panel untuk `tgwitness search`, `context`, `messages`, `stats` dan `export`; default `http://127.0.0.1:8787` ketika token telah ditetapkan |
| `TGWITNESS_MCP_TOKEN` | Arsipkan token koneksi dari **Integrasi → MCP**, yang dibagikan dengan klien MCP; `--token-file` membacanya dari berkas sebagai gantinya |
| `TGWITNESS_DATA` | Direktori data dibaca secara langsung jika tidak `--data-dir`, URL, atau token yang diberikan |

## Verifikasi sebelum dijalankan

Perintah satu baris ini mempercayai HTTPS untuk skrip awalnya. Skrip tersebut memeriksa SHA-256 serta tanda tangan RSA proyek pada aplikasi dan batasan-batasan sebelum pemasangan. Anda juga dapat mengunduh dan memverifikasi skrip awal tersebut terlebih dahulu.

Kunci rilis publiknya adalah [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). SHA-256-nya adalah:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Simpan sidik jari ini dari revisi repositori yang Anda percayai. Checksum dari server unduhan yang sama akan mendeteksi ketidaksesuaian; kunci publik yang tepercaya secara independen adalah yang mengautentikasi tanda tangan rilis.

Gunakan direktori baru yang kosong untuk mengunduh berkas verifikasi di bawah ini.

**Linux / macOS — jalankan di direktori unduhan baru yang kosong** (memerlukan curl dan OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

Rantai `&&` rantai akan berhenti sebelum eksekusi jika unduhan, sidik jari kunci, atau pemeriksaan tanda tangan gagal. Jika terjadi publikasi baru antara saat mengunduh skrip dan tanda tangannya, unduh keduanya kembali. Penginstal lama tetap mempertahankan URL paketnya yang tidak dapat diubah.

**Windows — periksa SHA-256 sebelum menjalankannya:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Bandingkan hash tersebut dengan `install.ps1` baris tersebut. Untuk pemeriksaan tanda tangan secara independen, gunakan OpenSSL (misalnya, dari Git Bash) dan sidik jari kunci publik yang sama di atas:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Instalasi Windows sendiri memverifikasi tanda tangan paket dengan .NET dan tidak memerlukan OpenSSL. Ini adalah tanda tangan RSA-3072 / SHA-256 yang terpisah, bukan Authenticode. [Manifest](https://get.destroy.tools/manifest.json) mencatat versi perangkat lunak, komit Git yang tepat, ID rilis yang tidak dapat diubah, dan SHA-256 setiap artefak. Halaman tersebut menautkan ke sumber yang sesuai. Manifest dan daftar checksum juga memiliki tanda tangan yang terpisah (`manifest.json.sig` dan `SHA256SUMS.txt.sig`).

## Perbarui instalasi yang sudah ada

**Publikasi baru memperbarui situs unduhan; program yang sudah terinstal akan diperbarui saat Anda menjalankan penginstal lagi.** Tidak ada pembaruan tanpa pengawasan atau restart otomatis pada koleksi yang sedang berjalan. Saluran penginstal saat ini adalah **pratinjau**; saluran ini mengikuti build yang telah diterbitkan dan diperiksa dari `main`, yang commit-nya bisa lebih baru daripada rilis GitHub bernomor terakhir. Versi halaman ini berasal dari `pyproject.toml`; commit dan ID build-nya membedakan pembaruan dalam versi pratinjau yang sama.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

Gunakan folder instalasi dan pengguna OS yang sama seperti sebelumnya. Cadangkan seluruh direktori data dengan menghentikan pengumpulan data; `tgwitness paths` mengidentifikasinya. Ekspor yang ditandatangani bukanlah cadangan instalasi yang lengkap.

**Instalasi root Ubuntu di `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Setelah instalasi berhasil:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Untuk instalasi pengguna Linux/macOS, gunakan `TGWITNESS_INSTALL_DIR` atau pengaturan default, lalu jalankan perintah instalasi pertama sekali lagi. Tutup panel yang sedang aktif sebelum melakukan pembaruan, lalu buka kembali setelahnya. Untuk layanan pengguna Linux yang telah dikonfigurasi , jalankan perintah `tgwitness restart` perintahnya.

**Windows:** tutup panel yang sedang berjalan, jalankan perintah instalasi Windows lagi, lalu buka `bin\tgwitness.cmd` di instalasi yang sama. Penginstal menyimpan data, sesi, pengaturan akses, dan kunci penandatanganan. Penginstal hanya akan mengganti peluncur setelah lingkungan baru lulus pemeriksaan; jika instalasi gagal, peluncur sebelumnya akan tetap ada. Simpan cadangan sebelum peningkatan untuk perubahan format penyimpanan.

## Perintah sehari-hari di Ubuntu

| Perintah | Hasil |
| --- | --- |
| `tgwitness open` | URL panel saat ini dan kunci akses. |
| `tgwitness paths` | Jalur program, data, dan panduan yang tepat. |
| `tgwitness guide --print` | Petunjuk penggunaan dalam mode offline. |
| `tgwitness status` / `tgwitness logs` | Ketersediaan / log layanan. |
| `tgwitness stop` / `tgwitness start` | Hentikan / lanjutkan layanan; simpan data. |
| `tgwitness token rotate` | Ganti kunci administrator dan akhiri sesi browser. |
| `tgwitness tunnel off` | Nonaktifkan terowongan cepat publik; pertahankan panel lokal. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Buat tautan terowongan cepat / ganti alamatnya. |

Lihat [bagian Akses](https://phishdestroy.github.io/TgWitness/id/docs/reference/access/) untuk token rekan kerja, sesi, dan pembatasan IP, serta [publikasi penginstal](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) untuk alur kerja rilis dari GitHub ke Cloudflare.

## Hapus TgWitness

Tidak ada program penghapus instalasi: Anda cukup menghentikan panel dan menghapus foldernya. Menghapus folder data akan menghapus jurnal, kunci penandatanganan, sesi Telegram, dan file yang disimpan secara permanen. Sebelum itu:

1. Ekspor apa yang Anda butuhkan (**Ekspor → Unduh ZIP yang telah ditandatangani**) dan simpan sidik jari kunci penandatanganan serta titik pemeriksaan di luar mesin ini. Untuk menyimpan ruang kerja itu sendiri, salin seluruh folder data setelah pengumpulan data dihentikan.
2. Hapus server yang dibuat di bawah **Extras → Server 24/7** dari "**Server Anda"** atau dengan `python -m tgwitness.cloud destroy`; penyedia layanan akan menagih biaya untuk server tersebut hingga dihapus.
3. Akhiri sesi setiap akun di Telegram melalui **Pengaturan → Perangkat**. Menghapus file-file tersebut tidak akan membuat sesi tersebut keluar di sisi Telegram.

**Instalasi root di Ubuntu.** Perhatikan folder data, hentikan layanan, lalu hapus layanan, folder, dan pintasan:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Instalasi untuk pengguna Linux atau macOS.** Tutup panel. Layanan pengguna Linux yang telah dikonfigurasi dihentikan dengan `systemctl --user disable --now tgwitness-<ID>`; unitnya berada di `~/.config/systemd/user/`. Kemudian hapus `~/.local/share/tgwitness` (atau `TGWITNESS_INSTALL_DIR`) serta `~/.local/bin/tgwitness` pintasan.

**Windows.** Tutup panel dan hapus `%LOCALAPPDATA%\TgWitness` (atau `TGWITNESS_INSTALL_DIR`). Penginstal tidak menambahkan layanan, tugas terjadwal, atau pintasan apa pun.
