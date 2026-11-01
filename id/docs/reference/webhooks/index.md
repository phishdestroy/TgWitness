# Webhook keluar

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/webhooks/

Mengirimkan peristiwa yang telah difilter ke penerima HTTPS dengan tanda tangan HMAC, upaya pengiriman ulang, dan status pengiriman.

[Panduan alur kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Buka **Integrasi → Webhook keluar** di ruang kerja yang dipilih. Tambahkan penerima HTTPS, pilih peristiwa pengumpul/media/ekspor, dan secara opsional pilih obrolan untuk pengamatan baru dan perubahan. Teks pesan dinonaktifkan secara default. Mengaktifkan kutipan akan menambahkan maksimal 1.000 karakter ke peristiwa perubahan pesan; bidang Telegram mentah dan kredensial tidak pernah dikirim.

Salin rahasia HMAC satu kali ke konfigurasi terlindungi penerima. Rahasia ini dienkripsi di brankas TgWitness dan tidak dapat diambil dari panel. Hapus dan buat ulang tujuan untuk merotasi kunci. **Kirim** antrian **uji sintetis** sebuah uji tanpa konten obrolan; segarkan status pengiriman untuk melihat hasilnya.

Pengiriman ini memperluas siklus pemberitahuan yang sudah ada bersama Apprise. Fitur ini menggunakan rute luar ruang kerja dan batasan tujuan pribadi yang sudah ada. Tidak ada fallback atau pengalihan langsung setelahnya. URL tidak boleh berisi kredensial, string kueri, atau fragmen; alamat pribadi memerlukan persetujuan jaringan tingkat server, bukan pengaturan yang dapat dilewati oleh pengguna panel.

## Payload dan tanda tangan

Skema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Setiap muatan berisi `event_id`, `timestamp`, `workspace`, `type`, `synthetic`, dan penghitung. Peristiwa berbasis jurnal mencakup urutan dan hash-nya. Penyelesaian ekspor penuh dan uji sintetis merupakan peristiwa pengiriman, tanpa referensi jurnal yang ditandatangani yang dibuat-buat. Pemberitahuan penghapusan Telegram dan `missing_on_recheck` tetap merupakan jenis yang berbeda.

Header `X-TgWitness-Signature` adalah `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Hitung HMAC atas byte yang tepat `timestamp + "." + raw_request_body`, menggunakan rahasia yang ditampilkan sebagai byte UTF-8. Bandingkan tanda tangan dalam waktu konstan sebelum menganalisis atau memproses isi pesan. Tolak cap waktu yang selisihnya lebih dari lima menit dari jam Anda. Cap waktu diperbarui pada setiap upaya pengiriman.

Gunakan `event_id` sebagai kunci idempotensi dalam penyimpanan tahan lama, dengan batasan unik atomik sebelum efek samping. Tanda tangan yang valid saja tidak mencegah permintaan terbaru diputar ulang. Simpan ID yang telah diproses setidaknya selama seluruh jendela percobaan ulang; simpan lebih lama jika penerima dapat memproses ulang peristiwa yang tersimpan.

## Mencoba lagi

Pengiriman diantrekan secara permanen sebelum permintaan HTTP. Sistem ini menggunakan semantik "setidaknya sekali": pengakuan yang hilang atau restart dapat menyebabkan suatu peristiwa dikirim ulang dengan ID yang sama. Terdapat delapan upaya dengan penundaan eksponensial, dimulai dari 15 detik dan dibatasi hingga satu jam. Keberhasilan memerlukan respons 2xx. Pekerjaan yang habis akan meninggalkan pesan kesalahan yang terlihat; pengiriman tidak dijamin setelah upaya ulang berakhir.

Antrian menampung 1.000 pengiriman. Saat penuh, pemindaian peristiwa jurnal akan berhenti sementara dan dilanjutkan kembali setelah ada ruang yang tersedia. Penyelesaian ekspor penuh yang tidak dapat dimasukkan ke antrian akan memicu kesalahan antrian yang terlihat. Hingga lima upaya pengiriman dicoba per siklus notifikasi, dan 100 catatan upaya terbaru disimpan. Menghapus tujuan juga akan menghapus pengiriman yang tertunda.

## Contoh n8n

Impor [alur kerja contoh](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Alur kerja ini tidak aktif dan tidak mengandung rahasia atau tindakan lanjutan. Tetapkan `TGWITNESS_WEBHOOK_SECRET` di lingkungan pekerja n8n, izinkan akses ke lingkungan tersebut, dan izinkan fungsi bawaan `crypto` untuk node Code. Contoh ini menggunakan opsi raw-body pada node Webhook, memverifikasi tanda tangan/keabsahan, dan mengonfirmasi peristiwa yang telah diverifikasi. Hal ini sesuai dengan [implementasi yang didokumentasikan](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) pada node tersebut.

Sebelum menambahkan penulisan atau pemberitahuan SIEM, tambahkan penyimpanan idempotensi yang tahan lama yang diindeks menggunakan `event_id`. Batasi pengeditan alur kerja n8n dan penyimpanan log eksekusi sesuai dengan data yang Anda pilih untuk dikirim. TgWitness tidak menambahkan perintah masuk apa pun.
