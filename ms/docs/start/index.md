# Mulakan dalam beberapa minit

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/start/

Pertama, teliti contoh yang berfungsi. Kemudian sambungkan akaun anda sendiri.

## Lihat sekeliling tanpa akaun

Muat turun atau klon projek ini, pasang **Python 3.11 atau yang lebih baru**, dan jalankan demo. Pelancar akan mencipta persekitaran tempatan dan memasang kebergantungan yang dipin.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

Pelayar membuka ruang kerja dengan mesej rekaan. Buka perbualan, bandingkan suntingan dan periksa eksport. Mod demo tidak menyambung ke Telegram.

![Paparan perbualan TgWitness dengan contoh mesej](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Ruang kerja contoh. Jurnal anda sendiri bermula secara berasingan.

## Mulakan ruang kerja anda sendiri

Tutup proses demo, kemudian gunakan pelancar biasa:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Buka alamat tempatan yang dipaparkan oleh pelancar. Jika diminta, masukkan **token akses panel** daripada fail tempatan yang dinamakan dalam terminal. Ini membuka kunci TgWitness; ia berasingan daripada log masuk Telegram.

## Rekod mesej pertama anda

1. [Sambungkan akaun Telegram khusus.](https://phishdestroy.github.io/TgWitness/ms/docs/accounts/)
2. Pilih kumpulan atau saluran yang boleh diakses oleh akaun, kemudian mulakan pemerhatian.
3. Hantar mesej baru dalam kumpulan ujian yang anda kendalikan dan semak bahawa ia muncul dalam jurnal.

Untuk pemasangan pelayan, ikuti [Keep it running](https://phishdestroy.github.io/TgWitness/ms/docs/server/).
