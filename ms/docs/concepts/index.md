# Lihat bagaimana bukti berfungsi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/concepts/

Mesej berubah. Rekod anda tentang apa yang anda lihat tidak sepatutnya berubah, dan sesiapa sahaja sepatutnya boleh menyemaknya.

Dua eksperimen kecil di bawah. Mesej palsu, semuanya berjalan dalam pelayar anda, tiada apa yang dihantar ke Telegram.

## Dari eksport sembang ke rekod yang boleh disahkan

[Eksport Telegram Desktop](https://telegram.org/blog/export-and-more) menyimpan sejarah yang boleh anda lihat sekarang sebagai HTML atau JSON. TgWitness menambah jurnal perubahan yang berterusan, tandatangan pada setiap rekod dan checkpoint yang boleh dibandingkan oleh orang lain.

| Tugas | Eksport Telegram Desktop | TgWitness |
| --- | --- | --- |
| Baca perbualan yang disimpan | HTML atau JSON dengan media terpilih | Perbualan yang disimpan, jurnal boleh dicari dan laporan luar talian |
| Ikuti perubahan dari masa ke masa | Sejarah yang tersedia apabila dieksport | Versi lama, suntingan kemudian dan pemadaman, semuanya disimpan |
| Semak fail selepas penyerahan | Fail eksport HTML/JSON standard tidak ditandatangani | Manifes bertandatangan, rekod bertandatangan dan laporan bermeterai, disemak dengan kunci yang dipercayai |
| Bandingkan dengan keadaan terdahulu yang disimpan | Simpan salinan rujukan berasingan atau hash | Pemeriksaan bermasa yang ditandatangani, saksi berasingan dan cap masa luaran pilihan |

Perbandingan ini berdasarkan [kod eksport Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) setakat 2 November 2026.

## Satu mesej, tiga pemerhatian

Mesej baharu, suntingan dan pemadaman menjadi tiga rekod berasingan. Suntingan tidak menimpa yang pertama, dan pemadaman tidak menghapuskannya.

01 / PERJALANAN PESANANUrutan ilustratif

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Pengumpul · Jurnal · kemas kini → · sambung →

PAPARAN PERBualan Semasa Mesej #42

Mesej telah dipadam

Mesej itu telah hilang daripada paparan sembang.

JURNAL PERMATAHAN 3 rekod

1. 01

   `message.new`

   Bertemu pada pukul 10:00

   ✓
2. 02

   `message.edited`

   Bertemu pada pukul 11:00

   ✓
3. 03

   `message.deleted`

   Notis pemadaman untuk #42

   ✓

Ketiga-tiga pemerhatian yang diterima kekal dalam jurnal.

Laluan ringkas untuk satu sumber yang telah dipilih. Rekod operasi juga berkongsi jurnal sebenar. Rakaman bergantung pada apa yang akaun boleh lihat dan apa yang Telegram sampaikan.

Telegram tidak memberitahu siapa yang memadam mesej atau bila tepatnya. TgWitness membiarkan medan itu kosong dan bukannya meneka.

## Ubah rekod. Ikuti hash.

Setiap rekod mengandungi hash rekod sebelumnya. Checkpoint yang disimpan di tempat lain mengunci panjang jurnal dan hash terakhir.

02 / HASH-CHAIN SANDBOXSHA-256 sebenar · rekod sampel

RAKAMAN 01**Mesej diterima**`h₁ = SHA-256(e₁)`Pautan ke 64 sifar

RAKAMAN 02**Bertemu pada pukul 11:00**`h₂ = SHA-256(e₂)`Termasuk h₁

RAKAMAN 03**Pembuangan diperhatikan**`h₃ = SHA-256(e₃)`Termasuk h₂

DISIMPAN DI TEMPAT LAIN**3 rekod · kepala `h₃`**Bandingkan sempadan tetap ini dengan jurnal yang disediakan.

Mengubah suatu peristiwa akan mengubah hashnya. Membina semula rantaian akan mengubah kepalanya. Menghilangkan ekor menjadikannya lebih pendek daripada checkpoint yang disimpan.

**Periksa rekod 2 dan semua hash sepenuhnya**

Ini adalah JSON UTF-8 tepat yang di-hash dalam contoh ini. Nilai adalah rekaan; sembilan medan dan serialisasi sepadan dengan format jurnal.

```

```

Rekod simpanan hash 2

``

Hash rekod 2 dikira semula

``

Sandbox ini mengira hash, bukan tandatangan. Pemeriksa sebenar juga menyemak tandatangan Ed25519 setiap peristiwa, urutan dan pautan. Membina semula hash sahaja tidak dapat menghasilkan tandatangan sah di bawah kunci yang dipercayai.

## Peraturan sebenar, dalam beberapa baris

HASH + TANDATANGAN

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** ialah sembilan medan peristiwa sebagai JSON UTF-8: kunci diisih, tiada ruang kosong tambahan, tiada escape ASCII, tiada NaN/infiniti. `previous_hash` ialah hi−1, h0 ialah 64 sifar, tandatangan meliputi 32 bait mentah digest.

Medan: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Spesifikasi penuh: [pengekodan peristiwa](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#event-canonicalization).

Pemeriksa Disimpan

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Semak tandatangan checkpoint dengan kunci yang dipin, kemudian bandingkan dengan jurnal. Eksport kemudian boleh lebih panjang, tetapi mesti sepadan pada checkpoint.

## Tiga soalan, tiga pemeriksaan berbeza

[01 / INTEGRITI**Adakah rekod ini berubah?** Hash dan tandatangan terhadap kunci yang anda percayai.](https://phishdestroy.github.io/TgWitness/ms/docs/exports/)[02 / KELANJUTAN**Apa yang telah disimpan sebelum ini?** Bandingkan eksport dengan checkpoint yang disimpan saksi.](https://phishdestroy.github.io/TgWitness/ms/docs/witness/)[03 / PENYAMPAIAN**Adakah acara ujian ini tiba?** Hantar, sunting dan padam mesej ujian, dan lihat apa yang ditangkap setiap akaun.](https://phishdestroy.github.io/TgWitness/ms/docs/cases/)

Tandatangan menjawab "adakah ia diubah", checkpoint menjawab "adakah ia sepadan dengan yang ada sebelum ini", mesej ujian menjawab "adakah kita menangkap semuanya". [Apa yang dibuktikan oleh pengesahan dan apa yang tidak.](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope)

Seterusnya: [siasatan seluruh akaun](https://phishdestroy.github.io/TgWitness/ms/docs/cases/) dari mula hingga pakej kes.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
