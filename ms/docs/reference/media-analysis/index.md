# OCR tempatan dan transkripsi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/media-analysis/

Kenal pasti imej dan audio yang dirakam dengan pekerja tempatan; pastikan teks terbitan dipautkan kepada fail sumbernya.

**Utama semasa:** gunakan checkout sumber; pratonton mudah alih 0.7.0 wujud sebelum ciri ini.

[Panduan aliran kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Buka rekod jurnal `media.saved`, pilih **Kenal pasti lampiran**, kemudian pilih OCR atau transkripsi di bawah **Tanya arkib**. Pemprosesan adalah secara manual dan tempatan. Tiada mod media awan atau muat naik automatik. Bait lampiran asal dan `media_sha256` kekal tidak berubah; teks yang diiktiraf ditandakan secara eksplisit sebagai pengiktirafan mesin dan disimpan secara berasingan dengan hash sumber, versi enjin/model, bahasa, parameter dan masa penyempurnaan. Transkrip mengekalkan cap masa yang dikembalikan.

Cari keputusan ini menggunakan **teks yang diiktiraf oleh Search** dan penapis OCR/transkrip. Ini adalah carian data terbitan yang berasingan; ia tidak secara senyap menukarkan pengiktirafan mesin kepada teks Telegram asal atau menambahkannya ke dalam acara yang disahkan.

## Menyiapkan pekerja pilihan

Versi 1 memerlukan hos Linux dengan daemon Docker tempatan. Pemasangan Windows boleh menjalankan TgWitness dalam persekitaran VM/WSL Linux dengan daemon tempatan tersendiri. Panel tidak pernah menyahsulit lampiran yang tidak dipercayai itu sendiri.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Atur pembolehubah ini dalam persekitaran perkhidmatan TgWitness dan mulakan semula. Soket daemon secara lalai ialah `/var/run/docker.sock`; penyebaran tanpa root boleh menetapkan `TGWITNESS_DOCKER_SOCKET`. Worker secara eksplisit menggunakan soket Unix tersebut daripada konteks Docker jauh. Jangan dedahkan API Docker kepada pengguna panel atau memasang soketnya di dalam kontena pengecaman.

Untuk transkripsi, pasang secara berasingan model Whisper yang serasi dengan CTranslate2, kemudian tetapkan `TGWITNESS_WHISPER_MODEL_DIR` ke direktori model tersebut. Worker memuatkannya dengan `local_files_only=True`; model terpilih dan input dipasang secara baca sahaja. Rujuk [dokumentasi pemuatan](https://github.com/SYSTRAN/faster-whisper) model enjin. Imej OCR yang disertakan merangkumi data latihan Bahasa Inggeris dan Rusia. Bina bahasa lain ke dalam imej anda apabila diperlukan; kod bahasa mengikut [CLI Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Tiada model dimuat semasa pemprosesan. Pembinaan/pamasan mungkin menggunakan rangkaian; setiap bekas pengecaman sebenar mempunyai rangkaian dilumpuhkan. Pasang imej sebelum mengaktifkannya; runtime menggunakan `--pull=never`.

## Batas dan pemulihan

Kontener dijalankan sebagai pengguna tanpa keistimewaan dengan root hanya-baca, keupayaan dikurangkan, `no-new-privileges` , satu CPU, 2 GiB memori, had PID dan sistem fail sementara terhad. Hanya salinan disahkan bagi fail yang dipilih dan direktori model pilihan dipasang. Pangkalan data, peti besi dan sesi pengumpul tidak dipasang. [Penanda aras runtime Docker](https://docs.docker.com/reference/cli/docker/container/run/) menguatkuasakan had ini; ini kekal sebagai sempadan kontena, bukan kawasan selamat perkakasan.

Fail dihadkan kepada 50 MiB, imej kepada 20 juta piksel, audio kepada 30 minit dengan tempoh yang diketahui, dan pemprosesan kepada lima minit. Satu pekerja berjalan pada satu-satu masa, dengan maksimum 20 kerja yang disusun/berjalan dan 100 kerja yang disimpan bagi setiap ruang kerja. Batal menghentikan kontena; cuba semula mencipta kerja baru yang dipautkan dengan percubaan sebelumnya. Kerja yang terhenti akan ditandakan selepas dihidupkan semula. Pemprosesan boleh gagal apabila model tidak dapat memenuhi had yang dikonfigurasikan; ia tidak akan berjalan secara senyap tanpa pengasingan.
