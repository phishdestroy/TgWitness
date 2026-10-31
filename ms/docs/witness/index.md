# Menyediakan bot saksi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/witness/

Biarkan proses berasingan memeriksa jurnal dan menerbitkan titik pemeriksaan yang disahkan ke saluran anda.

## Dua hos, dua kunci tandatangan

HOST A / PENGUMPUL**Akaun + jurnal**

Kunci tandatangan Pengumpul sesi Telegram

Titik akhir checkpoint baca sahaja

← minta jawapan bertandatangan →

HOST B / WITNESS**Sahkan + simpan**

Cap capai pengeksah terpaku Kunci tandatangan saksi berasingan

Jurnal sendiri + token bot

Saksi → API Bot Telegram →**Saluran anda · kiriman bertandatangan TGW1**

Saksi memuat turun semak sendiri. Akses pengumpul adalah baca sahaja. Penerbitan bot menggunakan sambungan dan token saksi; tiada sesi akaun diberikan kepada saksi.

03 / KEPUTUSAN CHECKPOINTJawapan ilustratif

DITERIMA TERAKHIR**120 rekod**`head 9c7d…`

JAWAPAN SETERUSNYA**128 rekod**`head a4f2…`

Diterima: bilangan meningkat, tandatangan disahkan dan kunci sepadan. Saksi mengekalkan sempadan baharu ini.

Semua contoh jawapan menganggap tandatangan sah dan kunci yang dipaku. Hashes di sini adalah ilustrasi ringkas. Bilangan yang lebih besar sahaja tidak dapat membuktikan bahawa keseluruhan awalan lama tidak berubah; bandingkan eksport dengan checkpoint yang dikekalkan.

## Sediakan bot dan saluran

Buat bot dengan BotFather dan benarkan ia menyiarkan dalam saluran yang anda kawal. Pilih komputer atau pelayan untuk saksi. Host dan pengendali berasingan menyediakan kebebasan yang lebih kukuh berbanding proses kedua pada pelayan pengumpul.

## Tiga langkah dalam Extras

1. **Akses baca sahaja.** Buka **Extras → Bot dalam saluran anda**, cipta token saksi dan simpan fail akses. Ia membolehkan membaca titik pemeriksaan dan status kesihatan, bukan perbualan atau kawalan pengumpul.
2. **Saluran dan selang.** Masukkan saluran dan alamat pengumpul yang boleh dihubungi oleh saksi. Simpan fail tetapan.
3. **Pelancaran.** Letakkan `witness.json`, `witness-token.txt` dan `bot-token.txt` yang dicipta pada hos saksi bersama-sama. Jalankan arahan di bawah dalam persekitaran projek yang dipasang.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Muat turun fail tidak memulakan saksi. Semak bahawa pos pertama yang ditandatangani muncul dalam saluran, kemudian simpan cap jari kunci awam saksi secara berasingan.

## Pilih kekerapan penerbitan

Menerbitkan setiap pemeriksaan mewujudkan rekod luaran berkala. Pada selang lima minit, iaitu kira-kira 288 siaran setiap ruang kerja setiap hari. Tetapan lanjutan juga menawarkan penerbitan untuk perubahan atau masalah, proksi dan alamat Bot API tersuai.

**Apa sebenarnya yang disahkan oleh bot ini?**

Saksi meminta pengumpul untuk titik pemeriksaan yang ditandatangani, mengesahkannya dengan kunci yang dijangka dan menyimpan jurnal berasingan yang ditandatangani. Ia merekodkan respons yang hilang dan jawapan yang ditolak serta pemeriksaan yang berjaya. Penerbitan masih bergantung pada saksi yang dijalankan dan mencapai Bot API Telegram.

Ia memeriksa status jurnal yang dilaporkan oleh pengumpul. Ia tidak memerhati secara bebas setiap mesej Telegram. Untuk itu, tambahkan ujian penghantaran terkawal.

## Semak bukti kemudian

Simpan jurnal saksi, pos saluran dan cap jari yang disimpan secara bebas. [Prosedur pengesahan penuh](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#verify) membandingkannya dengan eksport berasingan pengumpul yang ditandatangani.
