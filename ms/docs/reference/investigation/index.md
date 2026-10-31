# Mod siasatan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/investigation/

Siasatan keseluruhan akaun merentas saluran, kumpulan, sembang peribadi dan bot, daripada skop hingga pakej kes yang disahkan.

Ikuti satu kes merentasi saluran, kumpulan, sembang peribadi dan bot, daripada pemerolehan awal hingga garis masa yang dirujuk dan penyerahan yang boleh disahkan. Versi laman web interaktif boleh diakses di `/docs/cases/`; [arahan pratonton](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Kes yang dikaji: destinasi berubah merentasi empat perbualan

Sebuah pengumuman merujuk kepada bot. Kumpulan operasi membincangkan destinasi pembayaran baharu, papan kekunci bot memaparkannya, dan susulan peribadi mengulanginya. Pengumuman itu kemudian disunting dan mesej kumpulan hilang.

Soalan-soalannya ialah: apa yang diperhatikan sebelum dan selepas perubahan, akaun Telegram mana yang menyiarkan setiap item, di mana destinasi muncul, bait lampiran mana yang terpelihara, dan selang masa mana yang masih tidak diketahui?

Semua nama, ID, masa dan rujukan jurnal dalam contoh ini adalah rekaan. Aliran kerja menggunakan ciri semasa; peta kes adalah ilustrasi, bukan graf automatik yang dijana oleh aplikasi.

Diyagram aliran · Saluran → Jurnal ruang kerja; Kumpulan → Jurnal ruang kerja; Perbualan peribadi → Jurnal ruang kerja; Bot → Jurnal ruang kerja; Jurnal ruang kerja → Cari semua sumber; Jurnal ruang kerja → Profil individu dengan rujukan rekod; Jurnal ruang kerja → Versi yang disimpan dan resit lampiran; Cari semua sumber → Garis masa penganalisis dan pendaftaran sumber; Profil individu dengan rujukan rekod → Garis masa penganalisis dan pendaftaran sumber; Versi yang disimpan dan resit lampiran → Garis masa penganalisis dan pendaftaran sumber; Jurnal ruang kerja → ZIP bukti yang disahkan; Garis masa penganalisis dan pendaftaran sumber → Penyerahan kes dengan artifak yang disahkan secara berasingan; ZIP bukti yang disahkan → Penyerahan kes dengan artifak yang disahkan secara berasingan · Saluran · Kumpulan · Perbualan peribadi · Bot · Jurnal ruang kerja · Cari semua sumber · Profil individu denganrujukan rekod · Versi yang disimpan danresit lampiran · ZIP bukti yang disahkan · Garis masa penganalisisdan pendaftaran sumber · Penyerahan kes denganartifak yang disahkansecara berasingan

**Diagram sebagai teks**

1. Saluran → Jurnal ruang kerja
2. Kumpulan → Jurnal ruang kerja
3. Perbualan peribadi → Jurnal ruang kerja
4. Bot → Jurnal ruang kerja
5. Jurnal ruang kerja → Cari semua sumber
6. Jurnal ruang kerja → Profil individu dengan rujukan rekod
7. Jurnal ruang kerja → Versi yang disimpan dan resit lampiran
8. Cari semua sumber → Garis masa penganalisis dan pendaftaran sumber
9. Profil individu dengan rujukan rekod → Garis masa penganalisis dan pendaftaran sumber
10. Versi yang disimpan dan resit lampiran → Garis masa penganalisis dan pendaftaran sumber
11. Jurnal ruang kerja → ZIP bukti yang disahkan
12. Garis masa penganalisis dan pendaftaran sumber → Penyerahan kes dengan artifak yang disahkan secara berasingan
13. ZIP bukti yang disahkan → Penyerahan kes dengan artifak yang disahkan secara berasingan

## 1. Takrifkan kes dan kumpulkan keseluruhan keterangan

1. Sambungkan akaun pengumpulan ke ruang kerjanya sendiri. Dalam nota kes luaran, catatkan rujukan kes, ID akaun, ruang kerja, permulaan pemerhatian dan cap jari kunci penandatanganan yang dipercayai.
2. **Sumber** Terbuka **→ Skop Pengamatan → Mod Siasatan**. Preset memilih **keseluruhan akaun**, saluran/kumpulan/perbualan peribadi/bot, tindakan sendiri, profil sumber dan 200 mesej terkini yang boleh dilihat untuk sumber yang baru ditemui. Semak ia, tekan **Simpan Skop**, dan lengkapkan pengesahan skop.
3. **Muat sembang** dan bandingkan sumber dengan senarai dialog akaun. Semak pengecualian. **Parameter → Perbualan yang dibaca daripada senarai akaun** secara lalai adalah 1,000 dan membenarkan sehingga 20,000. Sumber yang melebihi had senarai akan ditambah apabila mereka menjadi aktif. Rekod apa yang sebenarnya disenaraikan.
4. Dalam **Tetapan Rakaman**, pilih **Semua aktiviti yang kelihatan** dan simpan tetapan pemantauan. Semak jenis/had lampiran dan ruang cakera kosong.
5. Mulakan pemerhatian. Sahkan mesej baru terkawal, suntingan dan pemadaman, kemudian simpan rujukan ujian dan sebarang kegagalan.

Skop keseluruhan akaun merekodkan aktiviti yang boleh dilihat dalam akaun mengikut tetapan yang disimpan. Ia tidak mengakses sembang rahsia atau menyertai secara automatik setiap kumpulan yang dipautkan. Ia juga tidak merekod semula setiap perbualan sedia ada. Lihat [skop pengumpulan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Daftarkan setiap sumber dan peroleh konteks sejarah

Simpan daftar sumber dengan satu baris bagi setiap sembang:

| Medan | Rakam |
| --- | --- |
| Identiti | Ruang kerja, ID akaun, ID sembang numerik, tajuk dan jenis |
| Kelihatan | Kehahlian/peranan, akses disahkan atau tidak disahkan, pengecualian |
| Rakaman langsung | Masa permulaan, jenis peristiwa yang dipilih dan perubahan dasar kemudian |
| Sejarah jurnal | Siaran tangkapan diminta/disiapkan, had, masa dan rujukan rekod |
| Sejarah penuh | Nama fail eksport per-bual bicara yang ditandatangani, sempadan dan penyempurnaan/kegagalan |
| Lampiran | Resit media yang diselesaikan, hash, saiz dan keputusan yang dilangkau/gagal |
| Liputan | Kegagalan perkhidmatan, kemasukan tidak lengkap, FloodWait, mesej tidak tersedia dan jurang lain |

Gunakan kaedah pemerolehan yang sesuai untuk setiap sumber:

- **Muat sejarah penuh** dalam **Sumber** (`main` semasa) memuatkan mesej lalu yang tersedia daripada sumber yang diaktifkan ke dalam jurnal ruang kerja. Ia menyokong hentikan/lanjutan dan laporan kemajuan yang disahkan. Lihat [pemerolehan sejarah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/).
- **Snepaduan sejarah** menyimpan mesej yang baru-baru ini kelihatan ke dalam jurnal pemerhatian. Had maksima lalai ialah 500; **Parameter → Snepaduan sejarah terbesar** boleh meningkatkannya kepada 10,000. Ini adalah pemerhatian sejarah semasa, bukan suntingan yang dibina semula.
- **Eksport sembang penuh → Eksport sembang penuh**, atau **Sembang → Eksport sembang**, memuat turun sejarah yang kini kelihatan bagi satu sembang ke dalam bundel berasingan yang ditandatangani `chat.json`/`chat.html`. Ulang untuk sumber kes dan simpan setiap hasil.
- **Apabila sembang atau bot baru muncul,** ia boleh menyimpan profilnya dan sehingga 1,000 mesej terkini; mod siasatan memilih 200. Sembang sedia ada tidak menerima pengambilan semula secara retroaktif apabila mod ini diaktifkan.
- **Muat turun lampiran yang kelihatan** mengekalkan bait di bawah dasar yang dikonfigurasikan. Meminta resit `media.saved` yang lengkap dengan SHA-256 dan kiraan bait. Tugas yang dibariskan, thumbnail atau nama fail bukan lampiran yang dipelihara.

Eksport sembang penuh **tidak** mengisi jurnal atau profil orang dengan semua pesannya. Gunakan **Muat Sejarah Penuh** atau snapshot jurnal terhad untuk sejarah yang anda perlukan untuk dianalisis dalam TgWitness. Semak senarai sumber yang diaktifkan sebelum memulakan larian sejarah. Tiada satu pun laluan yang memulihkan bahan yang Telegram tidak lagi kembalikan.

## 3. Pelihara kes yang sedang berkembang dan interaksi yang disengajakan

Tandakan sembang kes aktif sebagai sumber keutamaan. Semak selang semakan semula, pengejaran berterusan dan hasil media. Biarkan pengumpul memerhati semasa menggunakan akaun. Gunakan **Sembang → Profil → Simpan profil sekarang** untuk mengekalkan metadata sumber seperti keterangan dan arahan bot. Ini berasingan daripada profil orang yang diperoleh daripada mesej yang disimpan.

Apabila kes melibatkan pengikutan sumber atau interaksi dengan bot:

1. **Buka pautan Telegram → Simpan** rakaman **pratonton** merekod pautan yang diberikan dan pratonton yang dikembalikan sebelum sesuatu tindakan.
2. **Serah / buka dan perhatikan** melaksanakan serah/buka, dan menghantar parameter permulaan bot apabila dibekalkan. Permintaan serah yang menunggu kelulusan direkodkan sebagai tertangguh.
3. Balasan teks yang dikeluarkan oleh panel dan butang yang disokong mengekalkan `interaction.requested` dan `interaction.result`. Resit panggilan balik boleh mengekalkan teks pop timbul yang dikembalikan, keadaan amaran dan URL.

Itu adalah tindakan akaun sebenar. Tekanan callback dalam aplikasi Telegram lain tidak dapat dilihat oleh pengumpul, walaupun mesej atau suntingan yang terhasil mungkin dapat dilihat. Mini-klien tidak menjalankan aliran kerja web-app, pembayaran, telefon atau lokasi. Untuk tingkah laku tepat, lihat [interaksi panel](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/#act-from-the-panel).

## 4. Menghubungkan pemerhatian merentas sembang

Dalam **Journal**, pilih **Semua sumber** dan cari kandungan yang dirakam. Buka rekod yang sepadan dan simpan ruang kerja, sembang, ID mesej, urutan dan hash rekod.

Dalam sembang yang berkaitan, buka **Orang → Hidupkan profil** dan periksa seseorang:

- Nama/nama pengguna yang diperhatikan dari masa ke masa dan ID Telegram numerik.
- Balas dengan hubungan kepada rujukan rekod sumber.
- **Juga dalam…** sembang lain dalam jurnal ruang kerja ini di mana ID itu menulis.
- Aktiviti, suntingan/pembuangan dan dompet, telefon, nama pengguna serta pautan yang disebut.
- Metadata avatar yang disimpan dan avatar cache serupa, dengan asal usul masing-masing.

Buka rekod yang dirujuk sebelum menggunakan profil terbitan dalam penemuan. Profil merangkumi orang yang mempunyai mesej disimpan, bukan setiap ahli kumpulan. **Parameter → Rekod yang dirujuk bagi setiap fakta** mengehadkan senarai rujukan, bukan bilangan aktiviti asas. Kesesuaian sebutan dan avatar adalah petunjuk; ia tidak menetapkan pemilikan atau identiti.

Dalam contoh terperinci:

| Pautan | Merekod | Pemerhatian disokong |
| --- | --- | --- |
| Akaun penghantar yang sama | Kumpulan #146 dan susulan peribadi #205 | Kedua-duanya menyediakan ID penghantar Telegram 71001 |
| Tujuan yang sama | #146, bot papan kekunci #173, suntingan saluran #188, mesej peribadi #205 | Semua mengandungi `pay.example.invalid/new`; pemilikan/kawalan tidak ditetapkan |
| Fail yang sama disimpan | Resit media yang diselesaikan #151 dan #209 | Nilai SHA-256 penuh adalah serasi untuk bait yang dipelihara |
| Penetapan saluran | #101 dan #188 | Jangan kaitkan kiriman saluran kepada pengguna 71001 tanpa pengirim yang disahkan |

Bandingkan hash lampiran dan rujukan mesej yang berkaitan. Fail yang sama tidak menentukan pencipta, penghantar atau pengendali bersama. Nama yang sama dan avatar yang serupa sahaja tidak menyatukan dua ID Telegram menjadi satu individu.

## 5. Membina garis masa rentas sembang

Gunakan versi yang disimpan dalam Perbualan dan rekod Jurnal mereka pautan #… . Dalam Jurnal, gabungkan Semua sumber dengan Suntingan, Pemadaman dan Liputan. Simpan kedua-dua `source_at`, jika disediakan, dan `observed_at`.

| Masa pemerhatian ilustratif | Rujukan | Perhatian |
| --- | --- | --- |
| 09:00 | Saluran #101 | Tujuan asal dirakam |
| 09:12 | Kumpulan #146; media #151 | Destinasi baharu telah dipaparkan; muat turun fail telah selesai |
| 09:16 | Bot #173 | Papan kekunci menunjukkan ke destinasi baru |
| 09:20 | Saluran #188 | Pengumuman telah disunting; kedua-dua versi yang disimpan kekal |
| 09:24 | Peribadi #205; media #209 | ID penghantar yang sama berulang ke destinasi; bait fail yang sama dikekalkan |
| 09:28 | Kumpulan #231 | Notis pemadaman diterima; pengpadam dan masa pemadaman tepat tidak diketahui |

Rekod lain berlaku di antara rujukan contoh ini. Nombor urutan menyusun pemerhatian; snapshot sejarah boleh mengandungi tarikh sumber yang lebih lama dan tiba kemudian daripada peristiwa langsung. Bezakan snapshot, mesej yang dipulihkan, notis pemadaman dan hasil tiada pada semakan semula. Tandakan jurang liputan sebagai selang tidak diketahui. Pengambilan sejarah kemudian tidak secara retrospektif menetapkan pemerhatian tanpa gangguan.

## 6. Tambah perspektif akaun tanpa kehilangan asal usulnya

Gunakan ruang kerja berasingan untuk setiap akaun berbeza dan ulangi inventori akaun tersebut. Simpan ID akaun, peranan, cap jari kunci tandatangan dan rujukan sumber pada setiap perbandingan. Nombor mesej bukan pengecam global merentas sembang/akaun.

Korelasi merentas ruang kerja dilakukan dalam nota kes luaran atau alat analisis. TgWitness pada masa ini tidak mempunyai carian merentas ruang kerja global, garis masa gabungan, graf penyiasatan atau arkib kes gabungan. Eksport berbilang akaun untuk **satu** saluran/superkumpulan adalah operasi yang berbeza, bukan penggabungan jurnal akaun.

Untuk kerja yang lebih panjang, kekalkan batasan dengan [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/). Gunakan pemeriksaan penghantaran terkawal untuk menilai jejak tangkapan dan keterlihatan setiap akaun.

## 7. Mengumpul dan mengesahkan penyerahan kes

Simpan semua ini bersama dalam direktori kes yang disusun oleh penganalisis:

| Bahan | Tujuan |
| --- | --- |
| Nota kes dan daftar sumber | Soalan, dasar pengumpulan, akses/peranan, penemuan, penjelasan alternatif dan kekosongan |
| Garis Masa | Kedua-dua masa dan rujukan ruang kerja/perbualan/mesej/urutan bagi setiap entri |
| ZIP bukti yang ditandatangani bagi setiap ruang kerja | Jurnal rakaman lengkap, manifes dan media terpelihara yang disertakan; penapis panel tidak mengehadkan eksport jurnal |
| Fail profil orang yang ditandatangani secara berasingan | Rujukan terbitan disemak menentang bukti ruang kerja yang sepadan |
| Eksport sembang penuh yang disahkan | Perolehan sejarah yang kelihatan semasa, berasingan daripada jurnal pemerhatian |
| Cap jari dipercayai dan titik pemeriksaan awal | Identiti utama dan sempadan jurnal yang disimpan |
| Artifak saksi, jika dikonfigurasikan | Jurnal berasingan, kiriman yang ditandatangani dan cap jari saksi |
| Keputusan pengesahan dan hash fail yang dihantar | Apa yang diperiksa, bait mana yang dipindahkan dan kepada siapa |

Daripada pemasangan yang dipercayai, dengan nama fail dan cap jari sebenar setiap ruang kerja:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan keputusan pengesahan sebenar dan artifak asal. Direktori kes peringkat tertinggi, daftar sumber dan kesimpulan penganalisis diselenggara secara luaran; setiap artifak TgWitness mempunyai tandatangan dan prosedur pengesahan tersendiri.

## Sesuaikan siasatan

| Kes | Jejak | Serahkan |
| --- | --- | --- |
| Pertikaian pesanan/pembayaran yang diuruskan oleh bot | Pengumuman entri → pratonton pautan yang disimpan → parameter permulaan bot → versi mesej dan papan kekunci → resit panggilan balik panel → susulan peribadi/kumpulan | Garis masa tawaran/tindak balas yang diperhatikan dan sumber yang disahkan; pautan pembayaran sahaja tidak membuktikan pembayaran |
| Mesej yang dipadam selepas insiden | Semua sembang terjejas → asal/suntingan yang disimpan → hasil pemadaman atau ketiadaan semasa semakan semula → media yang dipelihara → liputan dan perspektif akaun lain | Versi yang disimpan dan selang masa tidak diketahui secara eksplisit; tiada pelaku pemadaman rekaan |
| Seorang peserta menukar nama di merata sembang | ID penghantar numerik → sejarah nama/nama pengguna → balasan → sembang lain yang diperhatikan → destinasi/fail yang dirujuk | Garis masa aktiviti akaun Telegram yang dirujuk, dengan identiti sebenar dan hipotesis hubungan dipisahkan |

[Rujukan pengumpulan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/) · [Pengesahan profil orang](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#people-profiles) · [Penyerahan bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#investigation-handoff) · [Pengesahan selesai](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/)
