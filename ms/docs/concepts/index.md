# Lihat bagaimana bukti berfungsi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/concepts/

Satu mesej boleh berubah. Rekod apa yang anda perhatikan harus kekal boleh disemak.

Terokai dua eksperimen kecil di bawah. Mereka menggunakan mesej rekaan, kekal di pelayar anda dan tidak pernah menyambung ke Telegram.

## Satu mesej, tiga pemerhatian

Apabila Telegram menghantar mesej baru, suntingan dan pemberitahuan pemadaman, pengumpul menambah tiga pemerhatian berasingan. Suntingan tidak menggantikan rekod pertama. Pemberitahuan pemadaman tidak memadamkannya.

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

Notis pemadaman tidak memberikan masa pemadaman yang boleh dipercayai mahupun individu yang memadam mesej. Menjaga nilai-nilai tersebut tidak diketahui mengekalkan perbezaan antara pemerhatian dan andaian.

## Ubah rekod. Ikuti hash.

Setiap rekod mengandungi hash rekod sebelumnya. Hashnya sendiri merangkumi medan peristiwa, termasuk pautan tersebut. Titik pemeriksaan yang disimpan secara luaran menetapkan panjang jurnal tertentu dan hash kepala.

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

**C** menyirialisasikan sembilan medan peristiwa sebagai JSON UTF-8: kunci disusun, tiada ruang tambahan, tiada pelarian ASCII dan tiada NaN/infinity. `previous_hash` bagi peristiwa ialah hi−1. h0 yang dipaparkan bermaksud 64 aksara sifar; tandatangan merangkumi 32 bait digest mentah.

Kesembilan medan ialah `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` dan `previous_hash`. Ini ialah [pengekodan JSON yang didokumenkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#event-canonicalization) oleh TgWitness; hash dan tandatangan itu sendiri bukan medan input hash.

Pemeriksa Disimpan

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Sahkan tandatangan checkpoint di bawah kunci pengumpul yang dipin, kemudian bandingkan sempadannya dengan jurnal yang disahkan. Eksport kemudian mungkin mengandungi lebih banyak rekod; ia masih mesti sepadan dengan checkpoint terdahulu.

## Tiga soalan, tiga pemeriksaan berbeza

[01 / INTEGRITI**Adakah rekod ini berubah?** Sahkan hash dan tandatangan terhadap kunci yang dipercayai secara berasingan.](https://phishdestroy.github.io/TgWitness/ms/docs/exports/)[02 / KELANJUTAN**Apa yang telah disimpan sebelum ini?** Bandingkan eksport yang disahkan dengan titik pemeriksaan yang disimpan oleh saksi berasingan.](https://phishdestroy.github.io/TgWitness/ms/docs/witness/)[03 / PENYAMPAIAN**Adakah acara ujian ini tiba?** Padankan tindakan hantar terkawal, sunting dan padam dengan jurnal setiap akaun.](https://phishdestroy.github.io/TgWitness/ms/docs/cases/)

Rantaian hash yang sepadan menjawab soalan integriti. Ia tidak menetapkan penghantaran Telegram yang lengkap, kebenaran mesej atau masa pemerhatian yang dipercayai secara bebas.

Ikuti [siasatan keseluruhan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/cases/) dari pemerolehan hingga pakej kes.
