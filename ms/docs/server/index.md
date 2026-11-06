# Teruskan menjalankannya

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/server/

Pastikan pengumpul terus berjalan dan data selamat melalui mula semula.

## Pilih kaedah pelancaran

Asli: [pelancar](https://phishdestroy.github.io/TgWitness/ms/docs/start/) serta templat perkhidmatan dalam [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, dari folder projek:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Panel mendengar pada localhost:8787. Bukanya secara setempat atau melalui terowong SSH, dengan token daripada arahan kedua.

## Simpan keseluruhan direktori data

Asli: `data/live`. Docker: volum `tgwitness-data`. Jurnal, sesi dan kunci mesti bersama. Eksport bertandatangan ialah bukti, bukan sandaran.

1. Hentikan pengumpulan dahulu.
2. Salin seluruh direktori data ke tempat selamat, di luar hos.
3. Cuba pulihkannya pada pemasangan berasingan sebelum anda mempercayainya.

## Semak selepas memulakan semula

Semak ruang kerja dan kunci, sambungan, sumber dan sama ada mesej baharu masuk. TgWitness mengejar apa yang Telegram masih ada, bukan segala yang berlaku semasa ia terhenti.

Bekas "healthy" bermaksud pelayan web menjawab. Sama ada pengumpulan berfungsi, mesej ujian dan saksi akan memberitahu.

## Terbitkan hanya apa yang anda niatkan

HTTPS, volum, kemas kini dan pemulihan ada dalam rujukan pengerahan. Apa yang benar-benar telah diuji: [rekod pengesahsahihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/).
