# Bagaimana bukti berfungsi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/how-it-works/

Rantaian hash, tandatangan, titik pemeriksaan dan saksi dijelaskan dengan formula tepat yang digunakan oleh pengesah.

TgWitness mengekalkan apa yang diperhatikan oleh akaun pengumpul, memautkan pemerhatian tersebut ke dalam jurnal yang ditandatangani dan membolehkan pihak lain mengesahkan eksport tersebut terhadap kunci yang dipercayai dan checkpoint yang telah disimpan sebelum ini.

[Laman web dokumentasi tempatan](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) menambah contoh interaktif di `/docs/concepts/`, penjelajah keputusan checkpoint di `/docs/witness/`. Semua mesej contoh, kiraan dan kelewatan adalah rekaan. Hashes dalam kotak pasir rantaian dikira menggunakan SHA-256 dalam pelayar. Tiada apa-apa yang dihantar ke Telegram.

## Satu mesej berubah; pemerhatian terkumpul

Diagram urutan · Telegram → Pengumpul: Mesej baru: Bertemu pada pukul 10:00; Pengumpul → Jurnal yang disahkan: Lampirkan message.new; Telegram → Pengumpul: Sunting: Bertemu pada pukul 11:00; Pengumpul → Jurnal yang disahkan: Sertakan mesej.disunting; Telegram → Pengumpul: Notis pemadaman; Pengumpul → Jurnal yang disahkan: Tambah message.deleted; Nota mengenai Jurnal yang disahkan: Perhatian terhadap asal + suntingan + pemadaman kekal · Telegram · Pengumpul · Jurnal yang disahkan · Mesej baru: Bertemu pada pukul 10:00 · Lampirkan message.new · Sunting: Bertemu pada pukul 11:00 · Sertakan mesej.disunting · Notis pemadaman · Tambah message.deleted · Perhatian terhadap asal + suntingan + pemadamankekal

**Diagram sebagai teks**

1. Telegram → Pengumpul: Mesej baru: Bertemu pada pukul 10:00
2. Pengumpul → Jurnal yang disahkan: Lampirkan message.new
3. Telegram → Pengumpul: Sunting: Bertemu pada pukul 11:00
4. Pengumpul → Jurnal yang disahkan: Sertakan mesej.disunting
5. Telegram → Pengumpul: Notis pemadaman
6. Pengumpul → Jurnal yang disahkan: Tambah message.deleted
7. Nota mengenai Jurnal yang disahkan: Perhatian terhadap asal + suntingan + pemadaman kekal

Susunan ringkas ini menganggap Telegram telah menyampaikan setiap kemas kini dan akaun terpilih dapat melihatnya. Acara operasi juga berkongsi jurnal tersebut. Notis pemadaman tidak memberikan maklumat tentang pemadam atau masa pemadaman yang tepat. Penghantaran berulang merupakan pemerhatian berasingan; tiada penindasan duplikat di seluruh jurnal.

## Apa yang dilindungi oleh hash

![Perhatikan, enkod, hashi dan tandatangani: setiap peristiwa baharu merangkumi hash sebelumnya.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Baca formula dari dalam ke luar: **C** menukarkan sembilan medan menjadi bait tepat; **SHA-256** menghasilkan digest mereka; **hex** ialah cara digest itu disimpan. Hash sebelumnya sudah berada dalam acara. **unhex** menukarkan semula hash yang disimpan menjadi 32 bait yang ditandatangani oleh Ed25519.

[Diagram rantaian statik](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Biarkan C(ei) menjadi JSON UTF-8 kanonik bagi sembilan medan peristiwa. Yang pertama `previous_hash` ialah 64 aksara sifar. Setiap rekod kemudian merangkumi hash heksadesimal rekod sebelumnya:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

Tandatangan merangkumi 32 bait digest mentah. Masukan hash mengandungi tepat `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` dan `previous_hash`. Kunci objek disusun; ruang putih dan pelarian ASCII diabaikan; NaN dan infiniti ditolak. Lihat [pengekodan tepat](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#event-canonicalization).

Diyagram aliran · 64 watak sifar → Rekod 1 / hash h1; Rekod 1 / hash h1 → Rekod 2 merangkumi h1 / hash h2; Rekod 2 merangkumi h1 / hash h2 → Rekod 3 merangkumi h2 / hash h3; Rekod 3 merangkumi h2 / hash h3 → Pemeriksaan titik bertandatangan: kira 3, tajuk h3 (simpan di tempat lain) · 64 watak sifar · Rekod 1 / hash h1 · Rekod 2 merangkumi h1/ hash h2 · Rekod 3 merangkumi h2/ hash h3 · Pemeriksaan titikbertandatangan: kira3, tajuk h3 · simpan di tempat lain

**Diagram sebagai teks**

1. 64 watak sifar → Rekod 1 / hash h1
2. Rekod 1 / hash h1 → Rekod 2 merangkumi h1 / hash h2
3. Rekod 2 merangkumi h1 / hash h2 → Rekod 3 merangkumi h2 / hash h3
4. Rekod 3 merangkumi h2 / hash h3 → Pemeriksaan titik bertandatangan: kira 3, tajuk h3 (simpan di tempat lain)

| Tukar ke jurnal yang disediakan | Apa yang mengdeteksinya |
| --- | --- |
| Ubah rekod 2 sambil mengekalkan hash yang disimpannya | Hash peristiwa yang dikira semula berbeza; tandatanganannya tidak lagi merangkumi peristiwa yang diubah |
| Bina semula rekod yang diubah dan setiap hash kemudian | Tandatangan asal gagal; titik pemeriksaan yang dikekalkan di sempadan terjejas juga tidak sepadan |
| Buang ekor tetapi biarkan prefiks yang tinggal utuh | Satu titik pemeriksaan yang disimpan lebih awal di luar awalan yang diberikan mendedahkan bahawa eksport itu terlalu pendek |
| Menandatangani semula jurnal pengganti dengan kunci lain | Cap cap jari kunci yang dipercayai secara berasingan menolak identiti pengganti |

![Mengubah medan yang disimpan akan mengubah digestnya; membina semula has tidak memulihkan tandatangan asal.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Cuba logik pada rekod 2:** ubah `Meet at 11:00` kepada `Meet at 12:00` dalam acara yang disimpan. Hash yang dikira semula itu tidak lagi sepadan. Mengira semula rantaian kemudian boleh membaiki pautannya, tetapi tidak dapat menjadikan tandatangan asal merangkumi digest baru. Sebaliknya, suntingan Telegram yang diperhatikan menjadi rekod jurnal baru.

[Diagram perubahan statik](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Pautan hash sahaja tidak menghalang seseorang daripada mengira semula rantaian pengganti. Kepercayaan datang daripada memeriksa tandatangan di bawah kunci yang dipercayai secara bebas dan membandingkannya dengan rujukan yang disimpan di luar pengumpul.

## Apa yang ditambah oleh titik pemeriksaan awal

![Menyimpan kiraan 3 dan tajuk h3; eksport kemudian 4 rekod diperiksa pada kedudukan 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Rujukan kekal tidak berubah sementara jurnal berkembang.** Jika penanda aras menyatakan "3 rekod, kepala h3", eksport empat rekod boleh melalui dengan memadankan h3 pada kedudukan 3. Kepala terbarunya ialah h4, yang dijangka berbeza. Eksport hanya dua rekod akan gagal.

[Diagram checkpoint statik](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Selepas mengesahkan tandatangan checkpoint, kehendaki:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Keluaran mungkin melangkaui titik pemeriksaan. Ia mesti sepadan pada sempadan yang dikekalkan. Pengesah sebenar juga memeriksa urutan setiap peristiwa, pautan sebelumnya, suai ukur dan tandatangan. Membandingkan hanya kepala simpanan akhir akan terlepas rekod dalaman yang diubah tetapi suai ukur simpanannya tidak dikemas kini.

## Di mana seorang saksi sepatutnya berada

Diyagram aliran · Pengumpul / sesi akaun / kunci A → Titik akhir checkpoint baca sahaja; Saksi / kunci pengumpul yang dipin / kunci sendiri B → Jurnal saksi berasingan yang disahkan; Saksi / kunci pengumpul yang dipin / kunci sendiri B → Titik akhir checkpoint baca sahaja (Minta semakan); Titik akhir checkpoint baca sahaja → Saksi / kunci pengumpul yang dipin / kunci sendiri B (Jawapan yang disahkan); Saksi / kunci pengumpul yang dipin / kunci sendiri B → Saluran dengan pos TGW1 yang disahkan (Bot API / token sendiri) · Host A · Host B · Pengumpul / sesi akaun /kunci A · Titik akhir checkpointbaca sahaja · Saksi / kunci pengumpulyang dipin / kunci sendiriB · Jurnal saksi berasinganyang disahkan · Saluran dengan pos TGW1yang disahkan · Minta semakan · Jawapan yang disahkan · Bot API / token sendiri

**Diagram sebagai teks**

1. Pengumpul / sesi akaun / kunci A → Titik akhir checkpoint baca sahaja
2. Saksi / kunci pengumpul yang dipin / kunci sendiri B → Jurnal saksi berasingan yang disahkan
3. Saksi / kunci pengumpul yang dipin / kunci sendiri B → Titik akhir checkpoint baca sahaja (Minta semakan)
4. Titik akhir checkpoint baca sahaja → Saksi / kunci pengumpul yang dipin / kunci sendiri B (Jawapan yang disahkan)
5. Saksi / kunci pengumpul yang dipin / kunci sendiri B → Saluran dengan pos TGW1 yang disahkan (Bot API / token sendiri)

Saksi merekodkan rollback, kepala berbeza pada kiraan yang sama, kunci yang diubah, jawapan tidak sah dan respons yang hilang. Kiraan yang lebih besar sahaja tidak membuktikan bahawa setiap rekod terdahulu kekal tidak berubah; bandingkan eksport dengan checkpoint yang disimpan. Saksi pada hos lain mengelakkan perkongsian gangguan hos pengumpul; seorang pengendali berasingan memberikan kebebasan tambahan.

Saksi mengesahkan keadaan jurnal yang dilaporkan oleh pengumpul. Ia tidak memerhati semua mesej Telegram secara bebas. Lihat [tetapan saksi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/).

## Uji penghantaran terhadap tindakan yang diketahui

Gunakan kumpulan terkawal, akaun pengumpulan berasingan dan penanda baharu. Hantar, sunting dan padam secara sengaja, menyemak tangkapan antara peringkat. Tetapkan tindakan yang dijangka dan had masa sebelum memeriksa keputusan.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Hanya tindakan yang sepadan dengan jangkaan dikira; resit gandaan tidak meningkatkan penyebut atas. Penyebut bawah mesti tidak sifar. Resit yang hilang tiada kelewatan yang diukur. Dokumen ketidakpastian masa; gunakan masa tindakan pemadaman terkawal anda sendiri, kerana Telegram tidak menyediakan masa pemadaman yang tepat. Hasil seperti 5/6 (83.3%) menerangkan tindakan ujian, bukan kelengkapan semua trafik Telegram.

## Pilih aliran kerja

[Panduan lengkap penyiasatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/investigation/) ini mengikuti satu insiden merentasi saluran, kumpulan, bot dan sembang peribadi:

1. Aktifkan mod siasatan akaun sepenuhnya dan inventori semua sembang yang boleh diakses.
2. Dapatkan snapshot jurnal, sejarah penuh setiap sembang dan lampiran yang disimpan.
3. Simpan perubahan secara langsung dan sebarang interaksi panel yang disengajakan beserta resitnya.
4. Ikuti ID penghantar numerik, hubungan balasan, destinasi berulang dan hash fail melalui rekod yang dirujuk dan profil individu.
5. Membina semula garis masa sembang silang dengan cap masa dan jurang yang jelas.
6. Bandingkan ruang kerja akaun lain sambil memisahkan asal usul dan kunci mereka.
7. Himpunkan dan sahkan jurnal yang ditandatangani, profil dan eksport sejarah dengan nota kes.

Panduan `/docs/cases/` di laman web ini merangkumi peta kes interaktif dan varian untuk pertikaian bot, mesej yang dipadam dan peserta yang menukar nama. Nota kes dan analisis merentas ruang kerja adalah luaran; aplikasi ini tidak secara automatik menjana graf siasatan global atau arkib kes gabungan.

[Pengesahan yang telah diselesaikan dan kerja yang masih tinggal](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) · [Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#investigation-handoff) · [Mulakan dengan satu akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/)
