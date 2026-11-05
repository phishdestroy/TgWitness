# Mesej boleh berubah． Simpan apa yang anda lihat．

Canonical page: https://phishdestroy.github.io/TgWitness/ms/

[Sumber terbuka ／ v0.9.0](https://phishdestroy.github.io/TgWitness/ms/docs/reference/changelog/)

Simpan sembang Telegram bersama setiap suntingan dan pemadaman， kemudian serahkan rekod yang boleh disemak oleh sesiapa sahaja．

[Buka demo](https://phishdestroy.github.io/TgWitness/demo/?lang=ms)[Panduan pemasangan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms)

Data palsu， tanpa log masuk Telegram．

 [Pengumpulan melalui GitHub Actions （pratonton）](https://phishdestroy.github.io/TgWitness/ms/docs/capture/) [Salinan luar tapak S3： pemasangan dan pemulihan](https://phishdestroy.github.io/TgWitness/ms/#s3)

SATU PESANAN， MELALUI WAKTU＃0042

Northstar · PenyelidikanSumber fiksyen ／ mesej 42

1. **Mesej diperhatikan**09：41：02

   Taklimat bermula di 14：00．
2. **Suntingan dipelihara**09：43：18

   Taklimat bermula di 15：00．

   Versi sebelumnya dikekalkan
3. **Notis pemadaman**10：06：45

   Kandungan yang dirakam kekal dalam jurnal anda．

Tiga pemerhatian． Satu sejarah． CONTOH

Mesej itu hilang． Sejarah yang dirakam kekal．

## Setiap perubahan yang dirakam． Tepat di mana anda memerlukannya．

Antara muka sebenar， dengan data rekaan．

TgWitness ／ Perbualan yang disimpanRUANG KERJA PERHATIAN ANDA

![Perbualan Telegram yang disimpan dalam tema gelap， dengan suntingan dan mesej yang dipadam disimpan dalam konteks](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Sembang tersimpan Kelihatan seperti sembang biasa， dengan suntingan dan pemadaman betul－betul di sebelah mesej．

TgWitness ／ JurnalRUANG KERJA TEMPATAN

![Jurnal dengan mesej yang diperhatikan， suntingan， notis pemadaman dan peristiwa liputan](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Jurnal Semua yang dilihat akaun anda， boleh dicari， termasuk jurang．

TgWitness ／ Sejarah suntinganRUANG KERJA TEMPATAN

![Tirai perincian membandingkan versi terdahulu yang dirakam dan versi yang disunting bagi sesuatu mesej](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Sejarah suntingan Versi lama dan baharu bersebelahan， tiada yang ditimpa．

TgWitness ／ Eksport BerperakRUANG KERJA TEMPATAN

![Eksport ruang kerja yang menawarkan fail ZIP yang ditandatangani， JSONL， CSV dan laporan HTML luar talian](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Eksport bertandatangan Bawa jurnal bersama anda， bertandatangan， dengan pengesahnya sendiri．

Ikuti rekod yang disimpan melalui [Papan Kes](https://phishdestroy.github.io/TgWitness/ms/docs/case-board/)， [reka bentuk laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reports/) dan [salinan](https://phishdestroy.github.io/TgWitness/ms/docs/handover/) [perkongsian](https://phishdestroy.github.io/TgWitness/ms/docs/handover/)． [Semak semula kumpulan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/groups/) bersama－sama．

01 ／ CAPTURE

### Anda memilih skop．

Beberapa sembang， satu folder atau seluruh akaun． Setiap akaun mendapat ruang kerjanya sendiri．

[Bandingkan mod pengumpulan](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#scope)

02 ／ PELIHAR

### Perubahan menambah kepada cerita．

Versi， pemadaman dan jurang semuanya kekal dalam jurnal．

[Lihat matriks acara](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#events)

03 ／ SERAH TERIMA

### Rekod yang bergerak．

ZIP bertandatangan， fail dan laporan luar talian． Kata laluan pilihan．

[Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/)

## Ubah satu bait．
Pengesahan akan memberitahu anda．

Setiap peristiwa memautkan kepada hash sebelumnya dan membawa tandatangan Ed25519．

![Acara yang dirakam dipautkan kepada hash sebelumnya， membawa tandatangan dan dihantar dalam eksport yang boleh disahkan．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Mengubah rekod yang dirakam akan menukar hashnya dan memecahkan pengesahan rekod yang berkaitan．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Satu checkpoint yang disimpan secara berasingan membolehkan penerima membandingkan jurnal yang dieksport dengan pemerhatian terdahulu．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Ikuti pemeriksaan dari hash fail ke checkpoint yang disimpan secara berasingan．

[Terokai lapan tahap bukti](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#levels)

## Sedia untuk pandangan mata lain．

Mesej， fail dan laporan luar talian dalam satu berkas bertandatangan．

[Baca model bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

tgwitness-evidence.zipBUNDEL TANDATANGAN

- 01

  Perhatian asalRekod JSONL ＋ jadual CSV
- 02

  Kontext yang boleh dibacaLaporan HTML luar talian ＋ media yang dipelihara
- 03

  Pengesahan bebasManifest yang ditandatangani ＋ pengesah berdiri sendiri

Penerima menyemak segala－galanya dengan kunci anda， dan checkpoint yang disimpan di tempat lain menunjukkan tiada apa yang ditulis semula sejak itu． [Cara semakan berfungsi．](https://phishdestroy.github.io/TgWitness/ms/docs/concepts/#layers)

## Salinan S3． Semakan luaran．

Simpan salinan yang disulitkan dan tambah pemeriksaan bebas．

Dimatikan secara lalai

### Salin semuanya ke storan serasi S3

Jurnal， fail， checkpoint dan eksport sembang， disulitkan sebelum dihantar ke S3．

**Tetapan penyimpanan dan pemulihan**

Sulitan di pihak klien

`AES-256-GCM` pada mesin anda． Penyedia hanya melihat teks sifer．

Salinan terjadual atau manual

Salin sekarang atau setiap 1 hingga 1，440 minit， kemajuan dipaparkan dalam panel．

Kunci Objek

Pilih bilangan hari dan mod pengekalan， panel menyemak sama ada ia benar－benar berkuat kuasa．

Pemulihan disahkan

Simpan kunci secara berasingan． Pulihkan di mana－mana， fail hanya dikeluarkan selepas pengesahan．

![Panel salinan luar tapak lengkap： hujung， rantau， baldi， kunci akses， jadual， kawalan Kunci Objek dan kunci pemulihan](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Panel lengkap dengan pilihan lanjutan dibuka． Tiada kelayakan storan dipaparkan．

Jurnal dan media`AES-256-GCM`Simpanan serasi S3

[Konfigurasikan S3 dan pulihkan salinan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3)[Baca butiran pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Kunci pemulihan** Simpan secara berasingan， tanpanya salinan tidak boleh dibaca．

### Pemberitahuan · Apprise

Masalah， perubahan sembang dan ringkasan harian ke aplikasi pesanan， e－mel atau webhook anda sendiri．

**Pilih apa yang dikongsi** Tiada teks mesej melainkan anda menghidupkannya．

 [Konfigurasikan destinasi pemberitahuan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/operations/#notifications)

### Cap masa luaran

Hash titik pemeriksaan cap masa menggunakan RFC 3161 dan OpenTimestamps．

**Ikuti hasilnya** Semak jawapan TSA atau naik taraf resit OpenTimestamps kepada bukti Bitcoin．

 [Semak bukti cap masa](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/)

### Saksi bebas

Host berasingan menyimpan pemerhatian yang disahkan dan boleh menerbitkan titik pemeriksaan`TGW1`．

**Asingkan rujukan** Jalankan pada hos lain， dengan kunci dan jurnalnya sendiri．

 [Menyediakan saksi](https://phishdestroy.github.io/TgWitness/ms/docs/witness/)

### Pemulihan dan jurang yang kelihatan

Sambung semula selepas memulakan semula． Semakan semula dan `coverage.json` memaparkan mesej yang dipulihkan dan kekosongan．

**Semak selang masa** Mesej yang dipulihkan dan jurang yang direkodkan bersebelahan．

 [Periksa kesinambungan dan kekosongan](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#continuity)

## Ruang kerja pertama anda bermula di sini．

Cuba demo dahulu， sambungkan akaun ganti apabila anda bersedia．
Windows， Linux， macOS atau Docker．

[Baca panduan pemasangan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms)

**Satu sesi diimport， satu klien sedang berjalan．**

Jangan jalankan TData atau sesi yang diimport dalam Telegram Desktop dan TgWitness serentak， Telegram boleh mematikan kedua－duanya （AUTH_KEY_DUPLICATED）． Perlukan kedua－duanya？ Log masuk ke TgWitness secara berasingan melalui telefon atau QR．

[Baca amaran import sesi](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms#session-warning)

**Lihat dahulu sebelum anda menyambung．**

Cuba ruang kerja fiksyen tanpa akaun Telegram．

[Buka demo dalam talian →](https://phishdestroy.github.io/TgWitness/demo/?lang=ms)

`scripts\Demo.cmd` WindowsLinux ／ macOS `sh start.sh --demo`

**Arahan pemasangan tempatan**

LANGKAH 01

### Dapatkan sumber．

[Muat turun fail sumber ZIP](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) dan ekstraknya， atau klon repositori：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Memerlukan Python 3.11+． Di Windows， pelancar menawarkan untuk memasangnya．

[Layari keluaran](https://github.com/phishdestroy/TgWitness/releases)

LANGKAH 02

### Pilih cara untuk menjalankan．

Klik dua kali `Start.cmd`， atau jalankan dalam PowerShell：

```
.\Start.cmd
```

Hanya ingin meneroka？ Klik dua kali `scripts\Demo.cmd` untuk demo terasing． Tidak perlu log masuk Telegram．

Dengan Python 3.11+ dan `venv` tersedia：

```
sh start.sh
```

Untuk membuka jurnal fiksyen sebaliknya， jalankan `sh start.sh --demo`．

Dengan Docker berjalan dan Compose 2.20+ dipasang：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Perintah kedua memaparkan token panel peribadi anda． Simpan ia pada mesin anda．

Buka [127.0.0.1:8787](http://127.0.0.1:8787) selepas pelancaran．

Pemasangan daripada sumber menyimpan token dalam `data/live/panel-token.txt`． Pasangan API anda sendiri daripada [my.telegram.org](https://my.telegram.org) adalah pilihan． [Panduan persediaan penuh ↗](https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/)

**TgWitness 0.9.0** [Apa yang baru →](https://phishdestroy.github.io/TgWitness/ms/docs/reference/changelog/) · [Ciri－ciri dan had yang diketahui →](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/)

## Arahan yang jelas． Langkah seterusnya yang berguna．

[Terokai panduan ↗](https://phishdestroy.github.io/TgWitness/ms/docs/)

[### Mod， senario dan tahap bukti Empat mod pengumpulan． Lapan tahap pengesahan． Temui aliran kerja untuk kes anda．](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html)

[01 ### Sambungkan akaun Telefon， QR， dan import sesi yang disokong．](https://phishdestroy.github.io/TgWitness/ms/docs/accounts/)[02 ### Pilih proksi Senarai awam MTProxy atau laluan anda sendiri．](https://phishdestroy.github.io/TgWitness/ms/docs/proxies/)[03 ### Menyediakan bot saksi Titik pemeriksaan bermasa dalam saluran Telegram anda．](https://phishdestroy.github.io/TgWitness/ms/docs/witness/)[04 ### Eksport dan sahkan Berkongsi sejarah yang dirakam dan menyemak integritinya．](https://phishdestroy.github.io/TgWitness/ms/docs/exports/)

## Kerjakan arkib．

Sejarah， AI dengan sumber， MCP， OCR dan webhook bertandatangan．

[Terokai aliran kerja](https://phishdestroy.github.io/TgWitness/ms/docs/archive/)

## Sebelum anda bermula．

**Adakah halaman ini berhubung dengan Telegram？**

Tidak． Ini halaman statik dengan contoh palsu． Aplikasi berjalan pada mesin anda sendiri dan anda log masuk di sana．

**Bolehkah ia memulihkan mesej yang dipadam sebelum rakaman？**

Tidak． Ia menyimpan apa yang dilihat akaun anda semasa ia berjalan． Snapshot kemudian tidak dapat membina semula suntingan yang terlepas atau mesej yang dipadam．

**Adakah keseluruhan jurnal saya disulitkan？**

Sesi dan kunci， ya． Mesej dan fail， tidak， gunakan penyulitan cakera． Eksport boleh diberi kata laluan AES－256．

**Adakah ini berafiliasi dengan Telegram？**

Tidak． Ini projek bebas berlesen MIT yang dibina di atas Telethon． Anda log masuk dengan akaun anda sendiri．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Terokai dahulu． Sediakan apabila sudah bersedia．

[Buka demo](https://phishdestroy.github.io/TgWitness/demo/?lang=ms)[Panduan pemasangan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms)
