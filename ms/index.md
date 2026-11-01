# Mesej boleh berubah. Simpan apa yang anda lihat.

Canonical page: https://phishdestroy.github.io/TgWitness/ms/

[Sumber terbuka / v0.7.1](https://phishdestroy.github.io/TgWitness/ms/docs/reference/changelog/)

Rekod mesej Telegram, pelihara perubahan mereka, dan eksport rekod yang disahkan.

[Buka demo](https://phishdestroy.github.io/TgWitness/demo/?lang=ms)[Panduan pemasangan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms)

Demonstrasi ini menggunakan data fiksyen. Tiada log masuk Telegram diperlukan.

 [Pengumpulan melalui GitHub Actions (pratonton)](https://phishdestroy.github.io/TgWitness/ms/docs/capture/) [Salinan luar tapak S3: pemasangan dan pemulihan](https://phishdestroy.github.io/TgWitness/ms/#s3)

SATU PESANAN, MELALUI WAKTU#0042

Northstar · PenyelidikanSumber fiksyen / mesej 42

1. **Mesej diperhatikan**09:41:02

   Taklimat bermula di 14:00.
2. **Suntingan dipelihara**09:43:18

   Taklimat bermula di 15:00.

   Versi sebelumnya dikekalkan
3. **Notis pemadaman**10:06:45

   Kandungan yang dirakam kekal dalam jurnal anda.

Tiga pemerhatian. Satu sejarah. CONTOH

Mesej itu hilang. Sejarah yang dirakam kekal.

## Setiap perubahan yang dirakam. Tepat di mana anda memerlukannya.

Layari antara muka dengan data demonstrasi rekaan.

TgWitness / Perbualan yang disimpanRUANG KERJA PERHATIAN ANDA

![Perbualan Telegram yang disimpan dalam tema gelap, dengan suntingan dan mesej yang dipadam disimpan dalam konteks](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Perbualan yang disimpan Tampilan perbualan yang biasa, dengan suntingan yang dirakam dan notis pemadaman di sebelah mesej.

TgWitness / JurnalRUANG KERJA TEMPATAN

![Jurnal dengan mesej yang diperhatikan, suntingan, notis pemadaman dan peristiwa liputan](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Jurnal Satu garis masa yang boleh dicari mengenai apa yang diperhatikan oleh akaun anda, termasuk gangguan.

TgWitness / Sejarah suntinganRUANG KERJA TEMPATAN

![Tirai perincian membandingkan versi terdahulu yang dirakam dan versi yang disunting bagi sesuatu mesej](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Sejarah suntingan  Bandingkan versi yang dirakam tanpa menimpa pemerhatian terdahulu.

TgWitness / Eksport BerperakRUANG KERJA TEMPATAN

![Eksport ruang kerja yang menawarkan fail ZIP yang ditandatangani, JSONL, CSV dan laporan HTML luar talian](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Eksport yang disahkan Bawa jurnal ini bersama anda, dengan manifes dan pengesah bebas.

01 / CAPTURE

### Anda memilih skop.

Perbualan terpilih, satu folder Telegram atau keseluruhan akaun. Ruang kerja berasingan untuk setiap akaun.

[Bandingkan mod pengumpulan](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#scope)

02 / PELIHAR

### Perubahan menambah kepada cerita.

Versi yang dirakam, notis pemadaman dan jurang pemerhatian kekal dalam jurnal.

[Lihat matriks acara](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#events)

03 / SERAH TERIMA

### Rekod yang bergerak.

Fail ZIP yang disahkan, fail yang dipelihara dan laporan luar talian. Perlindungan kata laluan pilihan.

[Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/)

## Ubah satu bait. Rantaian akan memberitahu anda.

Setiap peristiwa memautkan kepada hash sebelumnya dan membawa tandatangan Ed25519.

![Acara yang dirakam dipautkan kepada hash sebelumnya, membawa tandatangan dan dihantar dalam eksport yang boleh disahkan.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Mengubah rekod yang dirakam akan menukar hashnya dan memecahkan pengesahan rekod yang berkaitan.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Satu checkpoint yang disimpan secara berasingan membolehkan penerima membandingkan jurnal yang dieksport dengan pemerhatian terdahulu.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Lihat apa yang ditetapkan oleh setiap mekanisme pengesahan, dan di mana hadnya terletak.

[Terokai lapan tahap bukti](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#levels)

## Sedia untuk pandangan mata lain.

Serahkan pemerhatian, fail dan laporan HTML luar talian dalam satu bundel yang disahkan.

[Baca model bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

tgwitness-evidence.zipBUNDEL TANDATANGAN

- 01

  Perhatian asalRekod JSONL + jadual CSV
- 02

  Kontext yang boleh dibacaLaporan HTML luar talian + media yang dipelihara
- 03

  Pengesahan bebasManifest yang ditandatangani + pengesah berdiri sendiri

Tandatangan mengesan pengubahsuaian berbanding kunci yang dipercayai. Ia tidak membuktikan asal Telegram atau menjamin tangkapan lengkap. Kandungan jurnal dan media memerlukan penyimpanan yang disulitkan yang disediakan oleh anda.

## Salinan S3. Semakan luaran.

Simpan salinan yang disulitkan dan tambah pemeriksaan bebas.

Dimatikan secara lalai

### Salin semuanya ke storan serasi S3

Jurnal, fail, titik pemeriksaan bercap masa dan eksport sembang — disulitkan sebelum dimuat naik ke AWS S3 atau storan serasi.

**Tetapan penyimpanan dan pemulihan**

Sulitan di pihak klien

`AES-256-GCM` menyulitkan objek pada mesin ini. Penyedia menerima objek yang disulitkan.

Salinan terjadual atau manual

Salin sekarang, atau pilih selang masa antara 1 hingga 1,440 minit. Semak kemajuan di panel.

Kunci Objek

Pilih hari penyimpanan dan mod apabila baldi menyokongnya. Panel melaporkan sama ada penyimpanan telah disahkan pada objek yang dimuat naik.

Pemulihan disahkan

Muat turun kunci penyulitan dan simpan secara berasingan. Pulihkan pada mesin lain; fail hanya diterbitkan selepas pengesahan.

![Panel salinan luar tapak lengkap: hujung, rantau, baldi, kunci akses, jadual, kawalan Kunci Objek dan kunci pemulihan](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Panel lengkap dengan pilihan lanjutan dibuka. Tiada kelayakan storan dipaparkan.

Jurnal dan media`AES-256-GCM`Simpanan serasi S3

[Konfigurasikan S3 dan pulihkan salinan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3)[Baca butiran pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Tidak melakukannya.** Ia tidak memulihkan tanpa kunci dekripsi yang dieksport atau menggantikan saksi bebas.

### Pemberitahuan · Apprise

Amaran masalah, perubahan sembang dan ringkasan harian melalui Apprise: pesanan segera, e-mel atau webhook JSON anda sendiri.

**Tidak melakukannya.** Ia tidak menghantar teks mesej melainkan anda mengaktifkan petikan.

 [Konfigurasikan destinasi pemberitahuan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/operations/#notifications)

### Cap masa luaran

Hash titik pemeriksaan cap masa menggunakan RFC 3161 dan OpenTimestamps.

**Tidak melakukannya.** Ia tidak menganggap resit kalendar yang belum diselesaikan sebagai cap masa Bitcoin yang disahkan.

 [Semak bukti cap masa](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/)

### Saksi bebas

Host berasingan menyimpan pemerhatian yang disahkan dan boleh menerbitkan titik pemeriksaan`TGW1`.

**Tidak melakukannya.** Ia tidak menjadikan dua ruang kerja pada satu hos pengumpul sebagai saksi bebas.

 [Menyediakan saksi](https://phishdestroy.github.io/TgWitness/ms/docs/witness/)

### Pemulihan dan jurang yang kelihatan

Sambung semula selepas memulakan semula. Semakan semula dan `coverage.json` memaparkan mesej yang dipulihkan dan kekosongan.

**Tidak melakukannya.** Ia tidak membina semula setiap suntingan yang terlepas atau mesej yang hilang.

 [Periksa kesinambungan dan kekosongan](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#continuity)

## Ruang kerja pertama anda bermula di sini.

Terokai demo terlebih dahulu. Sambungkan akaun khusus apabila anda bersedia. Windows, Linux, macOS, atau Docker.

[Baca panduan pemasangan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms)

**Satu sesi diimport, satu klien sedang berjalan.**

Jangan jalankan kunci TData/session yang diimport dalam Telegram Desktop dan TgWitness pada masa yang sama. Telegram boleh membatalkan kebenaran yang dikongsi (AUTH_KEY_DUPLICATED). Untuk penggunaan serentak, buat log masuk TgWitness berasingan melalui telefon atau QR.

[Baca amaran import sesi](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms#session-warning)

**Lihat dahulu sebelum anda menyambung.**

Cuba ruang kerja fiksyen tanpa akaun Telegram.

[Buka demo dalam talian →](https://phishdestroy.github.io/TgWitness/demo/?lang=ms)

`scripts\Demo.cmd` WindowsLinux / macOS `sh start.sh --demo`

**Arahan pemasangan tempatan**

LANGKAH 01

### Dapatkan sumber.

[Muat turun fail sumber ZIP](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) dan ekstraknya, atau klon repositori:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Pelancaran sumber memerlukan Python 3.11+. Pelancar Windows menawarkan pemasangan jika Python tiada.

[Layari keluaran](https://github.com/phishdestroy/TgWitness/releases)

Tiada Python pada Windows? [Muat turun pakej mudah alih](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.1/TgWitness-0.7.1-windows-amd64-portable.zip), ekstrak dan klik dua kali `TgWitness.cmd`.

LANGKAH 02

### Pilih cara untuk menjalankan.

Klik dua kali `Start.cmd`, atau jalankan dalam PowerShell:

```
.\Start.cmd
```

Hanya ingin meneroka? Klik dua kali `scripts\Demo.cmd` untuk demo terasing. Tidak perlu log masuk Telegram.

Dengan Python 3.11+ dan `venv` tersedia:

```
sh start.sh
```

Untuk membuka jurnal fiksyen sebaliknya, jalankan `sh start.sh --demo`.

Dengan Docker berjalan dan Compose 2.20+ dipasang:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Perintah kedua memaparkan token panel peribadi anda. Simpan ia pada mesin anda.

Buka [127.0.0.1:8787](http://127.0.0.1:8787) selepas pelancaran.

Untuk pemasangan sumber, token berada di `data/live/panel-token.txt`. Log masuk Telegram boleh menggunakan tetapan API terbina dalam atau pasangan anda sendiri dari [my.telegram.org](https://my.telegram.org). [Panduan penyediaan penuh ↗](https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/)

**TgWitness 0.7.1** [Apa yang baru →](https://phishdestroy.github.io/TgWitness/ms/docs/reference/changelog/) · [Ciri-ciri dan had yang diketahui →](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/)

## Arahan yang jelas. Langkah seterusnya yang berguna.

[Terokai panduan ↗](https://phishdestroy.github.io/TgWitness/ms/docs/)

[### Mod, senario dan tahap bukti Empat mod pengumpulan. Lapan tahap pengesahan. Temui aliran kerja untuk kes anda.](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html)

[01 ### Sambungkan akaun Telefon, QR, dan import sesi yang disokong.](https://phishdestroy.github.io/TgWitness/ms/docs/accounts/)[02 ### Pilih proksi Senarai awam MTProxy atau laluan anda sendiri.](https://phishdestroy.github.io/TgWitness/ms/docs/proxies/)[03 ### Menyediakan bot saksi Titik pemeriksaan bermasa dalam saluran Telegram anda.](https://phishdestroy.github.io/TgWitness/ms/docs/witness/)[04 ### Eksport dan sahkan Berkongsi sejarah yang dirakam dan menyemak integritinya.](https://phishdestroy.github.io/TgWitness/ms/docs/exports/)

## Kerjakan arkib.

Muat sejarah, semak sumber AI, sambungkan klien MCP, kenal pasti media yang disimpan dan hantar webhook yang disahkan.

[Terokai aliran kerja](https://phishdestroy.github.io/TgWitness/ms/docs/archive/)

## Sebelum anda bermula.

**Adakah halaman ini berhubung dengan Telegram?**

Tidak. Ini adalah halaman projek statik dengan contoh fiksyen dan tangkapan skrin. Aplikasi sebenar berjalan pada komputer atau pelayan anda; log masuk berlaku di sana.

**Bolehkah ia memulihkan mesej yang dipadam sebelum rakaman?**

Tidak. TgWitness mengekalkan kandungan yang diperhatikan oleh akaun anda semasa pengumpulan dijalankan. Snek sejarah kemudian tidak dapat membina semula suntingan yang terlepas atau mesej yang dipadam.

**Adakah keseluruhan jurnal saya disulitkan?**

Butiran akaun dan rahsia penandatanganan disimpan dalam peti besi yang disulitkan. Mesej tempatan dan lampiran memerlukan cakera atau volum yang disulitkan. Eksport secara pilihan boleh menggunakan fail ZIP AES-256 yang dilindungi kata laluan.

**Adakah ini berafiliasi dengan Telegram?**

Tidak. TgWitness adalah projek bebas yang menggunakan Telethon, diedarkan di bawah Lesen MIT. Anda mengautorisasi akaun anda sendiri, menggunakan tetapan API terbina dalam atau pasangan API anda sendiri.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Terokai dahulu. Sediakan apabila sudah bersedia.

[Buka demo](https://phishdestroy.github.io/TgWitness/demo/?lang=ms)[Panduan pemasangan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms)
