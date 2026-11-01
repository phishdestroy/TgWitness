# OCR dan transkripsi lokal

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/media-analysis/

Kenali gambar dan audio yang direkam menggunakan worker lokal; jaga agar teks yang dihasilkan tetap tertaut ke berkas asalnya.

[Panduan alur kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Buka catatan jurnal `media.saved`, pilih "**Kenali lampiran**", lalu pilih OCR atau transkripsi di bawah **"Tanyakan ke arsip**". Pemrosesan dilakukan secara manual dan lokal. Tidak ada mode media cloud atau unggahan otomatis. Byte lampiran asli dan `media_sha256` tetap tidak berubah; teks yang dikenali ditandai secara eksplisit sebagai hasil pengenalan mesin dan disimpan terpisah bersama hash sumber, versi mesin/model, bahasa, parameter, dan waktu penyelesaian. Transkrip mempertahankan cap waktu yang dikembalikan.

Cari hasil ini menggunakan **fitur "Cari teks yang dikenali**" dan filter OCR/transkrip. Ini adalah pencarian data turunan yang terpisah; fitur ini tidak secara otomatis mengubah hasil pengenalan mesin menjadi teks Telegram asli atau menambahkannya ke peristiwa yang ditandatangani.

## Siapkan worker opsional

Versi 1 memerlukan host Linux dengan daemon Docker lokal. Instalasi Windows dapat menjalankan TgWitness di dalam lingkungan VM Linux/WSL dengan daemon lokalnya sendiri. Panel ini tidak pernah mendekode lampiran yang tidak tepercaya secara langsung.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Atur variabel-variabel ini di lingkungan layanan TgWitness dan mulai ulang layanannya. Soket daemon secara default adalah `/var/run/docker.sock`; untuk penerapan tanpa hak root, dapat diatur menjadi `TGWITNESS_DOCKER_SOCKET`. Worker secara eksplisit menggunakan soket Unix tersebut, bukan konteks Docker jarak jauh. Jangan mengekspos API Docker kepada pengguna panel atau memasang soketnya di dalam kontainer pengenalan.

Untuk transkripsi, instal secara terpisah model Whisper yang kompatibel dengan CTranslate2, lalu atur `TGWITNESS_WHISPER_MODEL_DIR` ke direktori model tersebut. Worker memuatnya dengan `local_files_only=True`; model yang dipilih dan input dipasang dalam mode baca-saja. Lihat [dokumentasi pemuatan model](https://github.com/SYSTRAN/faster-whisper) pada mesin tersebut. Gambar OCR yang disediakan mencakup data pelatihan dalam bahasa Inggris dan Rusia. Tambahkan bahasa lain ke dalam gambar Anda jika diperlukan; kode bahasa mengikuti [CLI Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Tidak ada model yang diambil selama pemrosesan. Proses pembuatan/pengunduhan pengaturan mungkin menggunakan jaringan; setiap wadah pengenalan yang sebenarnya memiliki jaringan yang dinonaktifkan. Instal gambar sebelum mengaktifkannya; runtime menggunakan `--pull=never`.

## Batasan dan pemulihan

Kontainer ini berjalan sebagai pengguna tanpa hak istimewa dengan root hanya baca, kemampuan yang dibatasi, `no-new-privileges` , satu CPU, memori 2 GiB, batas PID, dan sistem berkas sementara yang dibatasi. Hanya salinan terverifikasi dari berkas yang dipilih dan direktori model opsional yang dipasang. Basis data, vault, dan sesi pengumpul tidak dipasang. [Bendera runtime Docker](https://docs.docker.com/reference/cli/docker/container/run/) memberlakukan batasan-batasan ini; ini tetap merupakan batas kontainer, bukan enklave perangkat keras.

Ukuran file dibatasi hingga 50 MiB, gambar hingga 20 juta piksel, audio hingga 30 menit dengan durasi yang diketahui, dan pemrosesan hingga lima menit. Hanya satu pekerja yang berjalan pada satu waktu, dengan maksimal 20 pekerjaan yang mengantri/sedang berjalan dan 100 pekerjaan yang disimpan per ruang kerja. Perintah "Cancel" menghentikan kontainer; perintah "retry" membuat pekerjaan baru yang terhubung dengan upaya sebelumnya. Pekerjaan yang terputus akan ditandai setelah dimulai ulang. Pemrosesan dapat gagal jika model tidak dapat memenuhi batas yang dikonfigurasi; model tidak akan berjalan secara diam-diam tanpa isolasi.
