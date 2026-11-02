# Pasang, sahkan dan kemas kini

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/installation/

Pasang dengan satu arahan, semak tandatangan dan hash, kemas kini dan nyahpasang pemasangan.

[Projek](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Permulaan pantas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/) · [Penyebaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/)

## Pasang dengan satu arahan

Pemasang berpandu merangkumi persekitaran runtime Python peribadi. Gunakan alamat yang sama untuk pemasangan akan datang: setiap penerbitan mengemas kini pemasang, hash, tandatangan dan maklumat pembinaan secara serentak.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Pada pelayan Ubuntu, jalankan sebagai root untuk memasang perkhidmatan latar belakang. Pada desktop, jalankan sebagai pengguna biasa anda.

**Windows (PowerShell atau Command Prompt):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Tiada pentadbir diperlukan pada Windows. Proses PowerShell anak meninggalkan terminal anda terbuka dengan hasilnya. Python dan kebergantungan kekal dalam pemasangan.

Pada Ubuntu, pilih **Komputer ini**, **Pautan HTTPS sementara** atau **Domain sendiri**. Pemuat turun mencetak alamat panel dan kunci capaian. Untuk pautan sementara, buka alamat HTTPS itu dalam pelayar anda dan masukkan kunci tersebut. Dengan capaian tempatan pada pelayan jauh, gunakan penghalaan SSH dari komputer anda (`ssh -L 8787:127.0.0.1:8787 user@server`) dan buka `http://127.0.0.1:8787`. Pada macOS dan Windows, panel tempatan dibuka dalam pelayar anda; biarkan terminalnya terus berjalan.

Log masuk ke Telegram dalam panel dan pilih apa yang hendak dikumpul. Pemasangan sahaja tidak memulakan pengumpulan Telegram.

## Di mana semuanya berjalan

`get.destroy.tools` ialah **Cloudflare Worker yang menyajikan muat turun statik**. Ia tidak mempunyai panel TgWitness, sesi Telegram atau pangkalan data bukti pengguna. Ia tidak dialihkan ke VPS projek. Aplikasi ini berjalan pada mesin di mana anda menjalankan arahan.

| Pemasangan | Program | Data |
| --- | --- | --- |
| Ubuntu sebagai root | `/opt/tgwitness` | Perkhidmatan sistem: `/var/lib/tgwitness-<installation ID>`; gunakan `tgwitness paths` untuk laluan tepat. |
| Pengguna Linux / macOS | `~/.local/share/tgwitness` | `data/live` di bawah pemasangan itu. |
| Pengguna Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` di bawah pemasangan itu. |

Tetapkan `TGWITNESS_INSTALL_DIR` untuk memilih folder lain. Versi terpasang dan data adalah berasingan. Pemuat turun tidak memuat naik akaun, mesej atau kunci anda ke laman muat turun. Memilih terowong Cloudflare menghantar trafik panel melalui Cloudflare; menggunakan domain anda sendiri menunjuk ke pelayan anda sendiri.

Setiap pemasangan termasuk **START-HERE.html** dan **START-HERE.txt**, dengan laluan tempatan, arahan dan pautan ke repositori. Jalankan `tgwitness guide` untuk membuka panduan. Pada Windows, gunakan `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` dalam PowerShell.

## Sahkan sebelum menjalankan

Perintah satu baris mempercayai HTTPS untuk skrip permulaannya. Skrip itu memeriksa SHA-256 dan tandatangan RSA projek pada aplikasi dan sekatan sebelum pemasangan. Anda juga boleh memuat turun dan mengesahkan skrip permulaan terlebih dahulu.

Kunci keluaran awam ialah [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). SHA-256nya ialah:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Simpan cap jari ini daripada semakan repositori yang anda percayai. Checksum daripada pelayan muat turun yang sama mengesan ketidakpadanan; kunci awam yang dipercayai secara bebas itulah yang mengesahkan tandatangan keluaran.

Gunakan direktori baru yang kosong untuk muat turun pengesahan di bawah.

**Linux / macOS — jalankan dalam direktori muat turun baru yang kosong** (perlu curl dan OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

The `&&` rantaian akan berhenti sebelum pelaksanaan jika semakan muat turun, cap jari kunci atau tandatangan gagal. Jika penerbitan berlaku antara memuat turun skrip dan tandatangan nya, muat turun kedua-duanya semula. Pemuat turun lama mengekalkan URL pakej tidak berubah mereka.

**Windows — periksa SHA-256 sebelum menjalankan:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Bandingkan hash dengan `install.ps1` baris. Untuk pemeriksaan tandatangan secara bebas, gunakan OpenSSL (contohnya, dari Git Bash) dan cap jari kunci awam yang sama di atas:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Pemasangan Windows sendiri mengesahkan tandatangan pakej dengan .NET dan tidak memerlukan OpenSSL. Ini adalah tandatangan RSA-3072 / SHA-256 berasingan, bukan Authenticode. [Manifesto](https://get.destroy.tools/manifest.json) merekodkan versi perisian, komit Git tepat, ID keluaran yang tidak berubah dan SHA-256 setiap artifak. Halaman ini memautkan kepada sumber yang sepadan. Manifesto dan senarai checksum juga mempunyai tandatangan berasingan (`manifest.json.sig` dan `SHA256SUMS.txt.sig`).

## Kemas kini pemasangan sedia ada

**Penerbitan baru mengemas kini laman muat turun; program yang dipasang dikemas kini apabila anda menjalankan pemasang sekali lagi.** Tiada pengemas kini tanpa pengawasan atau permulaan semula automatik untuk koleksi yang sedang berjalan. Saluran pemasang semasa adalah **pratonton**; ia mengikuti bina yang diterbitkan dan diperiksa daripada `main`, yang komitnya boleh lebih baru daripada keluaran GitHub bernombor terakhir. Versi halaman ini berasal daripada `pyproject.toml`; komit dan ID binaannya membezakan kemas kini dalam versi pratonton yang sama.

Gunakan folder pemasangan dan pengguna OS yang sama seperti sebelum ini. Sediakan sandaran direktori data lengkap dengan pengumpulan dihentikan; `tgwitness paths` mengidentifikasinya. Eksport yang ditandatangani bukan sandaran pemasangan yang lengkap.

**Pemasangan root Ubuntu di `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Selepas pemasangan yang berjaya:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Untuk pemasangan pengguna Linux/macOS, gunakan yang asal `TGWITNESS_INSTALL_DIR` atau yang lalai dan jalankan semula arahan pemasangan pertama. Tutup panel latar hadapan sebelum mengemas kini dan mulakan semula selepas itu. Untuk perkhidmatan pengguna Linux yang telah dikonfigurasikan, jalankan `tgwitness restart` perintah.

**Windows:** tutup panel yang sedang berjalan, jalankan semula arahan pemasangan Windows, kemudian buka `bin\tgwitness.cmd` dalam pemasangan yang sama. Pemuat turun mengekalkan data, sesi, tetapan capaian dan kunci tandatangan. Ia menukar pelancar hanya selepas persekitaran baru lulus semakan; pemasangan yang gagal mengekalkan pelancar sebelumnya. Simpan sandaran pra-peningkatan untuk perubahan format storan.

## Perintah harian di Ubuntu

| Perintah | Keputusan |
| --- | --- |
| `tgwitness open` | URL panel semasa dan kunci akses. |
| `tgwitness paths` | Jalur program, data dan panduan yang tepat. |
| `tgwitness guide --print` | Arahan operasi luar talian. |
| `tgwitness status` / `tgwitness logs` | Ketersediaan / log perkhidmatan. |
| `tgwitness stop` / `tgwitness start` | Hentikan / sambung semula perkhidmatan; kekal data. |
| `tgwitness token rotate` | Gantikan kunci pentadbir dan tamatkan sesi pelayar. |
| `tgwitness tunnel off` | Matikan terowong pantas awam; kekalkan panel tempatan. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Buat pautan terowong pantas / gantikan alamatnya. |

Lihat [Akses](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/) untuk token rakan sekerja, sesi dan sekatan IP, serta [penerbitan pemasang](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) untuk aliran kerja pelepasan GitHub-ke-Cloudflare.

## Hapus TgWitness

Tiada pemadam pemasang: anda menghentikan panel dan memadamkan folder-foldernya. Memadamkan folder data memusnahkan jurnal, kunci penandatanganan, sesi Telegram dan fail yang disimpan sepenuhnya. Sebelum itu:

1. Eksport apa yang anda perlukan (**Eksport → Muat turun ZIP yang ditandatangani**) dan simpan cap jari kunci penandatanganan serta titik pemeriksaan di luar mesin ini. Untuk mengekalkan ruang kerja itu sendiri, salin keseluruhan folder data dengan pengumpulan dihentikan.
2. Padamkan pelayan yang dibuat di bawah **Extras → Server 24/7** daripada **Pelayan anda** atau dengan `python -m tgwitness.cloud destroy`; penyedia akan mengenakan bil kepada mereka sehingga ia dipadam.
3. Akhirkan sesi setiap akaun di Telegram di bawah **Tetapan → Peranti**. Memadam fail tidak menamatkan sesi di pihak Telegram.

**Pemasangan root Ubuntu.** Perhatikan folder data, hentikan perkhidmatan, kemudian keluarkan perkhidmatan, folder-folder dan pintasan:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Pemasangan untuk pengguna Linux atau macOS.** Tutup panel. Perkhidmatan pengguna Linux yang dikonfigurasikan dihentikan dengan `systemctl --user disable --now tgwitness-<ID>`; unitnya berada di `~/.config/systemd/user/`. Kemudian padamkan `~/.local/share/tgwitness` (atau anda `TGWITNESS_INSTALL_DIR`) dan `~/.local/bin/tgwitness` pautan pintas.

**Windows.** Tutup panel dan padamkan `%LOCALAPPDATA%\TgWitness` (atau anda `TGWITNESS_INSTALL_DIR`). Pemasang tidak menambah sebarang perkhidmatan, tugas terjadual atau pintasan.
