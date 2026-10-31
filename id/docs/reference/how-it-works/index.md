# Cara kerja bukti tersebut

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/how-it-works/

Penjelasan mengenai rantai hash, tanda tangan, titik pemeriksaan, dan saksi, disertai rumus-rumus tepat yang digunakan oleh verifikator.

TgWitness menyimpan apa yang diamati oleh akun pengumpul, menghubungkan pengamatan tersebut ke dalam jurnal yang ditandatangani, dan memungkinkan orang lain memverifikasi ekspor tersebut dengan menggunakan kunci tepercaya serta titik pemeriksaan yang disimpan sebelumnya.

[Situs web dokumentasi lokal](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) ini menambahkan contoh interaktif di `/docs/concepts/`, serta penjelajah keputusan checkpoint di `/docs/witness/`. Semua pesan contoh, jumlah, dan penundaan bersifat fiktif. Hash dalam sandbox rantai dihitung menggunakan SHA-256 di browser. Tidak ada data yang dikirim ke Telegram.

## Sebuah pesan berubah; pengamatan terus bertambah

Diagram urutan · Telegram → Pengumpul: Pesan baru: Bertemu pukul 10:00; Pengumpul → Jurnal yang ditandatangani: Tambahkan pesan.baru; Telegram → Pengumpul: Edit: Bertemu pukul 11:00; Pengumpul → Jurnal yang ditandatangani: Tambahkan pesan.edited; Telegram → Pengumpul: Pemberitahuan penghapusan; Pengumpul → Jurnal yang ditandatangani: Tambahkan pesan.dihapus; Catatan tentang Jurnal yang ditandatangani: Pengamatan terhadap pesan asli, yang diedit, dan yang dihapus tetap dipertahankan · Telegram · Pengumpul · Jurnal yang ditandatangani · Pesan baru: Bertemu pukul 10:00 · Tambahkan pesan.baru · Edit: Bertemu pukul 11:00 · Tambahkan pesan.edited · Pemberitahuan penghapusan · Tambahkan pesan.dihapus · Pengamatan terhadap pesan asli, yang diedit, danyang dihapus tetap dipertahankan

**Diagram dalam bentuk teks**

1. Telegram → Pengumpul: Pesan baru: Bertemu pukul 10:00
2. Pengumpul → Jurnal yang ditandatangani: Tambahkan pesan.baru
3. Telegram → Pengumpul: Edit: Bertemu pukul 11:00
4. Pengumpul → Jurnal yang ditandatangani: Tambahkan pesan.edited
5. Telegram → Pengumpul: Pemberitahuan penghapusan
6. Pengumpul → Jurnal yang ditandatangani: Tambahkan pesan.dihapus
7. Catatan tentang Jurnal yang ditandatangani: Pengamatan terhadap pesan asli, yang diedit, dan yang dihapus tetap dipertahankan

Urutan yang disederhanakan ini mengasumsikan bahwa Telegram telah mengirimkan setiap pembaruan dan akun yang dipilih dapat melihatnya. Peristiwa operasional juga tercatat dalam jurnal. Pemberitahuan penghapusan tidak mencantumkan pengirim penghapusan atau waktu penghapusan yang tepat. Pengiriman berulang merupakan pengamatan terpisah; tidak ada penindasan duplikat secara menyeluruh di jurnal.

## Apa yang dicakup oleh hash

![Amati, enkripsi, hash, dan tandatangani: setiap peristiwa baru menyertakan hash dari peristiwa sebelumnya.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Baca rumusnya dari dalam ke luar: **C** mengubah sembilan bidang menjadi byte yang tepat; **SHA-256** menghasilkan ringkasannya; **hex** adalah cara penyimpanan ringkasan tersebut. Hash sebelumnya sudah ada di dalam peristiwa. **unhex** mengubah hash yang disimpan kembali menjadi 32 byte yang ditandatangani oleh Ed25519.

[Diagram rantai statis](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Misalkan C(ei) adalah JSON UTF-8 kanonik dari sembilan bidang peristiwa. Yang pertama, `previous_hash`, terdiri dari 64 karakter nol. Setiap catatan berikutnya menyertakan hash heksadesimal dari catatan sebelumnya:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

Tanda tangan mencakup 32 byte digest mentah. Masukan hash berisi tepat `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, dan `previous_hash`. Kunci objek diurutkan; spasi kosong dan kode pelarian ASCII dihilangkan; NaN dan tak terhingga ditolak. Lihat [pengkodean yang tepat](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#event-canonicalization).

Diagram alur · 64 karakter nol → Catatan 1 / hash h1; Catatan 1 / hash h1 → Catatan 2 mencakup h1 / hash h2; Catatan 2 mencakup h1 / hash h2 → Catatan 3 mencakup h2 / hash h3; Catatan 3 mencakup h2 / hash h3 → Titik pemeriksaan yang ditandatangani: hitungan 3, judul h3 (simpan di tempat lain) · 64 karakter nol · Catatan 1 / hash h1 · Catatan 2 mencakup h1/ hash h2 · Catatan 3 mencakup h2/ hash h3 · Titik pemeriksaan yangditandatangani:hitungan 3, judul h3 · simpan di tempat lain

**Diagram dalam bentuk teks**

1. 64 karakter nol → Catatan 1 / hash h1
2. Catatan 1 / hash h1 → Catatan 2 mencakup h1 / hash h2
3. Catatan 2 mencakup h1 / hash h2 → Catatan 3 mencakup h2 / hash h3
4. Catatan 3 mencakup h2 / hash h3 → Titik pemeriksaan yang ditandatangani: hitungan 3, judul h3 (simpan di tempat lain)

| Ubah menjadi jurnal yang disediakan | Apa yang mendeteksinya |
| --- | --- |
| Ubah catatan 2 sambil mempertahankan hash yang telah disimpan | Hash peristiwa yang dihitung ulang berbeda; tanda tangannya tidak lagi mencakup peristiwa yang telah diubah |
| Merekonstruksi catatan yang telah diubah dan setiap hash berikutnya | Tanda tangan asli gagal; titik pemeriksaan yang disimpan di batas yang terpengaruh juga tidak sesuai |
| Hapus bagian akhir tetapi pertahankan awalan yang tersisa tetap utuh | Titik pemeriksaan yang disimpan sebelumnya di luar awalan yang diberikan menunjukkan bahwa ekspor tersebut terlalu pendek |
| Menandatangani ulang jurnal pengganti dengan kunci lain | Jejak kunci tepercaya yang terpisah menolak identitas pengganti |

![Mengubah bidang yang telah disimpan akan mengubah ringkasannya; menghitung ulang hash tidak akan memulihkan tanda tangan asli.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Coba logika pada catatan 2:** ubah `Meet at 11:00` menjadi `Meet at 12:00` dalam peristiwa yang disimpan. Hash yang dihitung ulang tidak lagi cocok. Menghitung ulang rantai selanjutnya dapat memperbaiki tautannya, tetapi tidak dapat membuat tanda tangan asli mencakup ringkasan baru. Sebaliknya, pengeditan Telegram yang teramati akan menjadi catatan jurnal baru.

[Diagram perubahan statis](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Tautan hash saja tidak mencegah seseorang untuk menghitung ulang rantai pengganti. Kepercayaan berasal dari pemeriksaan tanda tangan menggunakan kunci yang dipercaya secara independen dan perbandingan dengan referensi yang disimpan di luar pengumpul.

## Apa yang ditambahkan oleh titik pemeriksaan sebelumnya

![Pertahankan jumlah 3 dan judul h3; ekspor selanjutnya yang berisi 4 catatan diperiksa pada posisi 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Referensi tetap tidak berubah meskipun jurnal terus bertambah.** Jika titik pemeriksaan menyatakan “3 catatan, header h3”, ekspor empat catatan dapat lolos dengan mencocokkan h3 pada posisi ke-3. Header terbarunya adalah h4, yang diperkirakan akan berbeda. Ekspor yang hanya berisi dua catatan akan gagal.

[Diagram titik pemeriksaan statis](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Setelah memverifikasi tanda tangan titik pemeriksaan, wajibkan:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Ekspor mungkin melampaui titik pemeriksaan. Ekspor tersebut harus sesuai pada batas yang dipertahankan. Verifikator sebenarnya juga memeriksa urutan setiap peristiwa, tautan sebelumnya, hash, dan tanda tangan. Membandingkan hanya bagian awal yang disimpan akan melewatkan catatan bagian dalam yang diubah yang hash-nya tidak diperbarui.

## Tempat yang tepat bagi seorang saksi

Diagram alur · Pengumpul / sesi akun / kunci A → Titik akhir checkpoint yang hanya dapat dibaca; Witness / kunci pengumpul yang disematkan / kunci sendiri B → Jurnal saksi terverifikasi yang terpisah; Witness / kunci pengumpul yang disematkan / kunci sendiri B → Titik akhir checkpoint yang hanya dapat dibaca (Ajukan permintaan pemeriksaan); Titik akhir checkpoint yang hanya dapat dibaca → Witness / kunci pengumpul yang disematkan / kunci sendiri B (Jawaban yang ditandatangani); Witness / kunci pengumpul yang disematkan / kunci sendiri B → Saluran dengan postingan TGW1 yang ditandatangani (API Bot / token sendiri) · Host A · Host B · Pengumpul / sesi akun /kunci A · Titik akhir checkpointyang hanya dapat dibaca · Witness / kunci pengumpulyang disematkan / kuncisendiri B · Jurnal saksi terverifikasiyang terpisah · Saluran dengan postinganTGW1 yang ditandatangani · Ajukan permintaan · pemeriksaan · Jawaban yang ditandatangani · API Bot / token sendiri

**Diagram dalam bentuk teks**

1. Pengumpul / sesi akun / kunci A → Titik akhir checkpoint yang hanya dapat dibaca
2. Witness / kunci pengumpul yang disematkan / kunci sendiri B → Jurnal saksi terverifikasi yang terpisah
3. Witness / kunci pengumpul yang disematkan / kunci sendiri B → Titik akhir checkpoint yang hanya dapat dibaca (Ajukan permintaan pemeriksaan)
4. Titik akhir checkpoint yang hanya dapat dibaca → Witness / kunci pengumpul yang disematkan / kunci sendiri B (Jawaban yang ditandatangani)
5. Witness / kunci pengumpul yang disematkan / kunci sendiri B → Saluran dengan postingan TGW1 yang ditandatangani (API Bot / token sendiri)

Witness mencatat rollback, nilai head yang berbeda pada hitungan yang sama, kunci yang diubah, jawaban yang tidak valid, dan respons yang hilang. Hitungan yang lebih besar saja tidak menjamin bahwa setiap catatan sebelumnya tetap tidak berubah; bandingkan ekspor dengan titik pemeriksaan yang disimpan. Witness di host lain menghindari dampak gangguan pada host pengumpul; operator terpisah memberikan kemandirian tambahan.

Witness memverifikasi status jurnal yang dilaporkan oleh pengumpul. Alat ini tidak secara independen memantau semua pesan Telegram. Lihat [pengaturan Witness](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/).

## Pengujian pengiriman terhadap tindakan yang diketahui

Gunakan kelompok terkontrol, akun pengumpul yang terpisah, dan penanda baru. Kirim, edit, dan hapus secara sengaja, sambil memeriksa hasil pencatatan di antara setiap tahap. Tentukan tindakan yang diharapkan serta batas waktu sebelum memeriksa hasilnya.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Hanya tindakan yang sesuai dengan yang diharapkan yang dihitung; tanda terima ganda tidak menambah pembilang. Penyebut harus bukan nol. Tanda terima yang hilang tidak memiliki penundaan yang terukur. Dokumentasikan ketidakpastian waktu; gunakan waktu tindakan penghapusan terkontrol Anda sendiri, karena Telegram tidak menyediakan waktu penghapusan yang tepat. Hasil seperti 5/6 (83,3%) menggambarkan tindakan pengujian, bukan kelengkapan seluruh lalu lintas Telegram.

## Pilih alur kerja

[Panduan penyelidikan lengkap](https://phishdestroy.github.io/TgWitness/id/docs/reference/investigation/) berikut ini menguraikan alur kejadian yang terjadi di saluran, grup, bot, dan obrolan pribadi:

1. Aktifkan mode Investigasi seluruh akun dan inventarisasi setiap obrolan yang dapat diakses.
2. Peroleh cuplikan jurnal, riwayat lengkap per obrolan, dan lampiran yang disimpan.
3. Simpan perubahan secara real-time dan setiap interaksi panel yang disengaja beserta bukti transaksinya.
4. Lacak ID pengirim numerik, hubungan balasan, tujuan yang berulang, dan hash file melalui catatan yang dikutip serta profil pengguna.
5. Merekonstruksi garis waktu lintas obrolan dengan cap waktu dan celah yang jelas.
6. Bandingkan ruang kerja akun lain sambil tetap memisahkan asal-usul dan kuncinya.
7. Kumpulkan dan verifikasi jurnal yang telah ditandatangani, profil, serta ekspor riwayat bersama dengan catatan kasus.

Panduan `/docs/cases/` di situs web ini mencakup peta kasus interaktif dan varian-variannya untuk sengketa bot, pesan yang dihapus, dan peserta yang mengganti nama. Catatan kasus serta analisis lintas ruang kerja bersifat eksternal; aplikasi ini tidak secara otomatis menghasilkan grafik investigasi global atau arsip kasus gabungan.

[Validasi yang telah diselesaikan dan pekerjaan yang masih harus dilakukan](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/) · [Ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#investigation-handoff) · [Mulailah dengan satu akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/quickstart/)
