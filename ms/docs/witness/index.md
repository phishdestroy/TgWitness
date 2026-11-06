# Telegram · Menyediakan bot saksi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/witness/

Proses berasingan menyemak jurnal anda dan menyiarkan checkpoint bertandatangan ke saluran.

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

Buat bot dengan BotFather dan benarkan ia menyiar dalam saluran anda. Jalankan saksi di tempat lain: hos lain, sebaik-baiknya dikendalikan orang lain, jauh lebih bernilai daripada proses kedua di sebelah pengumpul.

## Tiga langkah dalam Extras

1. **Akses baca sahaja.** **Tambahan → Saksi Bebas**, cipta token, simpan fail. Ia membaca checkpoint dan kesihatan, tiada yang lain.
2. **Saluran dan selang.** Saluran Telegram atau webhook Discord, serta alamat pengumpul yang boleh dicapai saksi. Simpan fail tetapan.
3. **Lancar.** Letakkan `witness.json`, `witness-token.txt` dan `bot-token.txt` bersama pada hos saksi dan jalankan:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Tunggu hantaran bertandatangan pertama dalam saluran, kemudian simpan cap jari saksi di tempat selamat.

Discord pula? Simpan URL webhook sebagai `discord-webhook.txt`. Satu saksi menyiar ke satu tempat; semakan panjang tiba sebagai fail di Discord.

## Pilih kekerapan penerbitan

Menyiar setiap semakan memberi rekod luar yang tetap: setiap lima minit ialah kira-kira 288 hantaran sehari bagi setiap ruang kerja. Tetapan lanjutan boleh menyiar hanya apabila ada perubahan atau masalah, menggunakan proksi atau Bot API tersuai.

**Apa sebenarnya yang disahkan oleh bot ini?**

Ia meminta checkpoint bertandatangan daripada pengumpul, menyemaknya dengan kunci yang dijangka dan menyimpan jurnal bertandatangannya sendiri, termasuk jawapan yang terlepas dan ditolak.

Ia menyemak keadaan jurnal, ia tidak memerhati Telegram sendiri. Untuk itu, jalankan ujian penghantaran terkawal.

## Semak bukti kemudian

Simpan jurnal saksi, hantaran dan cap jari. [Cara menyemaknya](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#verify) terhadap eksport pengumpul.
