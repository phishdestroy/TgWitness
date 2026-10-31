# Teruskan menjalankannya

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/server/

Pastikan pengumpul sentiasa tersedia dan datanya kekal utuh selepas dimulakan semula.

## Pilih kaedah pelancaran

Untuk pemasangan asli, gunakan [pelancar](https://phishdestroy.github.io/TgWitness/ms/docs/start/) dan contoh perkhidmatan dalam [deploy/.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Untuk Docker, pasang Docker dengan Compose dan jalankan dari direktori projek:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Panel lalai mendengar pada alamat loopback hos, port 8787. Buka secara tempatan atau melalui terowong SSH. Gunakan token daripada arahan kedua untuk membuka kunci panel.

## Simpan keseluruhan direktori data

Pemasangan asli menggunakan `data/live`. Docker menggunakan volum `tgwitness-data` yang berterusan. Menyimpan jurnal, sesi akaun, kunci dan keadaan operasi bersama-sama. Eksport yang ditandatangani adalah bukti yang berguna, tetapi ia bukan sandaran penuh pemasangan.

1. Hentikan pengumpulan sebelum membuat sandaran yang konsisten.
2. Salin keseluruhan direktori data peribadi ke storan terlindung di luar hos.
3. Uji pemulihan ke dalam pemasangan terasing sebelum bergantung pada sandaran.

## Semak selepas memulakan semula

Sahkan ruang kerja dan kunci yang dijangka, sambungan Telegram, sumber terpilih dan tangkapan mesej baru. Status MTProto yang disimpan dan bantuan catch-up membantu memulihkan kemas kini yang masih disimpan oleh Telegram. Mereka tidak dapat membina semula setiap kemas kini yang telah tamat tempoh atau suntingan yang dipadam sebelum tangkapan.

Kesihatan kontena bermaksud pelayan web memberi respons. Gunakan mesej terkawal dan pemeriksaan saksi untuk menilai pengumpulan dan penerbitan luaran.

## Terbitkan hanya apa yang anda niatkan

Rujukan penyebaran merangkumi contoh HTTPS, arahan volum kekal, langkah kemas kini dan pemulihan. Arahan Docker disediakan untuk penyebaran; [rekod pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) semasa mengenal pasti persekitaran yang benar-benar diuji.
