# Jaga agar tetap berjalan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/server/

Jaga kolektor tetap berjalan dan data aman melewati restart.

## Pilih metode peluncuran

Native: [peluncur](https://phishdestroy.github.io/TgWitness/id/docs/start/) ditambah templat layanan di [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, dari folder proyek:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Panel mendengarkan di localhost:8787. Buka secara lokal atau lewat tunnel SSH, dengan token dari perintah kedua.

## Pertahankan seluruh direktori data

Native: `data/live`. Docker: volume `tgwitness-data`. Jurnal, sesi, dan kunci harus bersama. Ekspor bertanda tangan adalah bukti, bukan cadangan.

1. Hentikan pengumpulan dulu.
2. Salin seluruh direktori data ke tempat aman di luar host.
3. Coba pulihkan di instalasi terpisah sebelum Anda mempercayainya.

## Periksa kembali setelah restart

Periksa ruang kerja dan kunci, koneksi, sumber, dan apakah pesan baru masuk. TgWitness mengejar apa yang masih dimiliki Telegram, bukan semua yang terjadi selama ia mati.

Kontainer "sehat" berarti server web menjawab. Apakah pengumpulan berjalan, pesan uji dan saksi yang akan memberi tahu.

## Hanya publikasikan apa yang Anda maksudkan

HTTPS, volume, pembaruan, dan pemulihan ada di referensi deployment. Yang benar-benar diuji: [catatan validasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/).
