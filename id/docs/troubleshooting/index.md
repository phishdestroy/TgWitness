# Temukan apa yang salah

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/troubleshooting/

Mulai dari gejalanya, periksa satu hal setiap kali.

## Panel meminta token

Yang diminta adalah token panel dari berkas yang disebut peluncur. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Bukan kode Telegram, bukan token bot, bukan token saksi.

## Telegram tidak terhubung

Jalankan pemeriksaan koneksi. Di proxy publik, pilih yang lain dan simpan. Periksa jenis proxy dan format rahasianya. Memperbarui daftar tidak mengganti rute dengan sendirinya.

## Terhubung, tetapi tidak ada pesan baru

1. Apakah pengamatan berjalan, di ruang kerja yang benar?
2. Apakah sumbernya dipilih dan terlihat oleh akun itu?
3. Kirim pesan unik di grup uji Anda lalu cari pesan itu.
4. Cari gangguan atau galat Telegram di jurnal.

Obrolan yang sepi memang tidak punya hal baru. Jika kelengkapan penting, lakukan uji pengiriman terkendali.

## FloodWait atau jeda setelah restart

FloodWait adalah Telegram berkata "pelan-pelan". Tunggu sampai lewat dan kurangi beban; menyambung ulang tidak membantu. Setelah restart, TgWitness mengejar apa yang masih dimiliki Telegram; sisanya adalah celah, jadi catat.

## Bot ini telah dikonfigurasi tetapi tidak memposting apa pun

Apakah saksi berjalan, bisakah bot memposting di kanal, bisakah ia menjangkau kolektor dan Bot API? Cari postingan yang gagal di jurnalnya. Kueri di sisi kolektor tidak berarti postingan terkirim.

## Di mana integrasi token GitHub?

**Sedang direncanakan.** Bagian "Extras" menjelaskan alur kerja verifikasi fork dan build yang diusulkan. Saat ini belum ada formulir token GitHub atau verifikasi otomatis yang memastikan bahwa instalasi yang berjalan sesuai dengan repositori. Lihat [status fitur saat ini](https://phishdestroy.github.io/TgWitness/id/docs/reference/features/).

Melaporkan bug? Versi, sistem operasi, langkah, dan galat tanpa data pribadi. Jangan pernah menaruh sesi, token, pesan pribadi, atau direktori data di issue publik.
