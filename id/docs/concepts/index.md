# Telegram · Lihat cara kerja bukti ini

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/concepts/

Pesan berubah. Catatan Anda tentang apa yang Anda lihat seharusnya tidak, dan siapa pun seharusnya bisa memeriksanya.

Di bawah ada dua eksperimen kecil. Pesan fiktif, semuanya berjalan di browser Anda, tidak ada yang dikirim ke Telegram.

## Dari ekspor obrolan menjadi catatan yang dapat diverifikasi

[Ekspor Telegram Desktop](https://telegram.org/blog/export-and-more) menyimpan riwayat yang terlihat saat ini sebagai HTML atau JSON. TgWitness menambahkan jurnal perubahan yang terus berjalan, tanda tangan di setiap catatan, dan checkpoint yang bisa dibandingkan orang lain.

| Tugas | Ekspor Telegram Desktop | TgWitness |
| --- | --- | --- |
| Baca percakapan yang disimpan | HTML atau JSON dengan media yang dipilih | Obrolan yang disimpan, jurnal yang dapat dicari, dan laporan offline |
| Ikuti perubahan dari waktu ke waktu | Riwayat yang tersedia saat diekspor | Versi lama, suntingan berikutnya, dan penghapusan, semuanya disimpan |
| Periksa berkas setelah penyerahan | Berkas ekspor HTML/JSON standar tidak ditandatangani | Manifes bertanda tangan, catatan bertanda tangan, dan laporan bersegel, diperiksa dengan kunci tepercaya |
| Bandingkan dengan status yang disimpan sebelumnya | Simpan salinan referensi terpisah atau hash | Titik pemeriksaan yang ditandatangani, saksi terpisah, dan cap waktu eksternal opsional |

Perbandingan ini berdasarkan [kode ekspor Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) per 2 November 2026.

## Satu pesan, tiga pengamatan

Pesan baru, suntingan, dan penghapusan menjadi tiga catatan terpisah. Suntingan tidak menimpa yang pertama, dan penghapusan tidak menghilangkannya.

01 / PERJALANAN PESANUrutan ilustratif

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Pengumpul · Jurnal · perbarui → · tambahkan →

TAMPILAN OBrolan SAAT INI Pesan #42

Pesan telah dihapus

Pesan tersebut telah menghilang dari tampilan obrolan.

JURNAL PENGAMATAN 3 catatan

1. 01

   `message.new`

   Bertemu pukul 10.00

   ✓
2. 02

   `message.edited`

   Bertemu pukul 11.00

   ✓
3. 03

   `message.deleted`

   Pemberitahuan penghapusan untuk #42

   ✓

Ketiga pengamatan yang diterima tetap tersimpan dalam jurnal tersebut.

Jalur yang disederhanakan untuk satu sumber yang telah dipilih. Catatan operasional juga mencakup jurnal asli. Pencatatan bergantung pada apa yang dapat dilihat oleh akun tersebut dan apa yang disediakan oleh Telegram.

Telegram tidak memberi tahu siapa yang menghapus pesan atau kapan tepatnya. TgWitness membiarkan kolom itu kosong alih-alih menebak.

## Ubah catatan. Ikuti hash-nya.

Setiap catatan berisi hash catatan sebelumnya. Checkpoint yang disimpan di tempat lain mengunci panjang jurnal dan hash terakhir.

02 / HASH-CHAIN SANDBOXSHA-256 asli · contoh catatan

CATATAN 01**Pesan diterima**`h₁ = SHA-256(e₁)`Tautan ke 64 nol

CATATAN 02**Bertemu pukul 11.00**`h₂ = SHA-256(e₂)`Termasuk h₁

CATATAN 03**Penghapusan terdeteksi**`h₃ = SHA-256(e₃)`Termasuk h₂

DISIMPAN DI TEMPAT LAIN**3 catatan · kepala `h₃`**Bandingkan batas yang telah diperbaiki ini dengan jurnal yang disediakan.

Mengubah suatu peristiwa akan mengubah hash-nya. Membangun ulang rantai akan mengubah bagian awalnya. Menghapus bagian akhir akan membuatnya lebih pendek daripada titik pemeriksaan yang disimpan.

**Periksa catatan 2 dan hash lengkapnya**

Ini adalah JSON UTF-8 yang telah di-hash persis seperti pada contoh ini. Nilai-nilainya fiktif; sembilan bidang dan serialisasinya sesuai dengan format jurnal.

```

```

Catatan yang disimpan 2 hash

``

Hash catatan 2 yang dihitung ulang

``

Sandbox ini menghitung hash, bukan tanda tangan. Verifikator yang sebenarnya juga memeriksa tanda tangan Ed25519, urutan, dan tautan setiap peristiwa. Membangun ulang hash saja tidak dapat menghasilkan tanda tangan yang valid di bawah kunci tepercaya.

## Aturan sebenarnya, dalam beberapa baris

HASH + TANDA TANGAN

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** adalah sembilan kolom peristiwa sebagai JSON UTF-8: kunci terurut, tanpa spasi tambahan, tanpa escape ASCII, tanpa NaN/tak hingga. `previous_hash` adalah hi−1, h0 adalah 64 nol, dan tanda tangan mencakup 32 byte mentah digest.

Kolomnya: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Spesifikasi lengkap: [pengodean peristiwa](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#event-canonicalization).

TITIK PERIKSA YANG DISIMPAN

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Periksa tanda tangan checkpoint dengan kunci yang dipatok, lalu bandingkan dengan jurnal. Ekspor yang lebih baru boleh lebih panjang, tetapi harus cocok di checkpoint.

## Tiga pertanyaan, tiga pemeriksaan yang berbeda

[01 / INTEGRITAS**Apakah catatan ini berubah?** Hash dan tanda tangan terhadap kunci yang Anda percayai.](https://phishdestroy.github.io/TgWitness/id/docs/exports/)[02 / KONTINUITAS**Apa yang telah disimpan sebelumnya?** Bandingkan ekspor dengan checkpoint yang disimpan saksi.](https://phishdestroy.github.io/TgWitness/id/docs/witness/)[03 / PENYAMPAIAN**Apakah peristiwa uji coba ini telah diterima?** Kirim, sunting, dan hapus pesan uji, lalu lihat apa yang ditangkap setiap akun.](https://phishdestroy.github.io/TgWitness/id/docs/cases/)

Tanda tangan menjawab "apakah diubah?", checkpoint menjawab "apakah cocok dengan yang ada sebelumnya?", pesan uji menjawab "apakah kita menangkap semuanya?". [Apa yang dibuktikan verifikasi dan apa yang tidak.](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#verification-scope)

Berikutnya: [investigasi seluruh akun](https://phishdestroy.github.io/TgWitness/id/docs/cases/) dari awal hingga paket kasus.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
