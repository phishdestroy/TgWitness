# Satu jurnal. Empat mod pengumpulan. Lapan tahap pengesahan.

Canonical page: https://phishdestroy.github.io/TgWitness/ms/guides/modes.html

Mod, senario dan tahap bukti

TgWitness merekodkan apa yang diperhatikan oleh akaun yang disambungkan. Pihak ketiga boleh mengesahkan integriti rekod tersebut berbanding kunci yang dipercayai secara bebas.

[Mod pengumpulan](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#scope)[Senario](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#scenarios)[Tahap bukti](https://phishdestroy.github.io/TgWitness/ms/guides/modes.html#levels)

3–5 minit gambaran keseluruhan · contoh rekaan · pelaksanaan semasa

1. **Telegram**

   Kemas kini yang boleh dilihat oleh akaun
2. **Pengumpul**

   Rekod yang dipautkan, setiap satu ditandatangani
3. **Pengesah**

   Kunci dipercayai + sempadan terpelihara

`h₁ → h₂ → h₃ · Ed25519`Integriti disemak. Asal Telegram dan kebenaran mesej kekal sebagai persoalan berasingan.

## Pilih skop pemerhatian

Tiga skop dan satu tetapan siasatan. Pengecualian dan jenis sumber yang diaktifkan masih terpakai.

Lalai**Perbualan terpilih**

Rekod

Hanya sumber yang dipilih secara manual.

Sembang baru

Tidak ditambah secara automatik.

Pilih untuk

Sekumpulan saluran atau kumpulan yang diketahui. Tiada kapasiti sembang tetap telah ditetapkan.

**Tidak melakukan** Ia tidak menemui sembang lain atau mengisi semula sejarah terdahulu.

Folder akaun**folder Telegram**

Rekod

Inklusi folder dan kategori, pengecualian minus dan sembang yang diarkibkan apabila dikonfigurasikan.

Sembang baru

Perlawanan sembang aktif; perubahan folder dalam masa sejam.

Pilih untuk

Seorang penganalisis sudah mengekalkan folder kes. Sahkan pengumpulan pada akaun khusus.

**Tidak melakukan** Ia tidak menerapkan perubahan folder muted/read keadaan.

Sahkan skop**Keseluruhan akaun**

Rekod

Perbualan yang boleh dilihat oleh akaun, termasuk perbualan peribadi dan bot, dalam jenis terpilih.

Sembang baru

Ditambah apabila kemas kini pertama tiba.

Pilih untuk

Akaun pemerhatian khusus, termasuk akaun yang mengambil bahagian dalam sesuatu kes.

**Tidak melakukan** Ia tidak menyertai sembang secara automatik atau memintas akses sumber.

Pra-tetapan akaun keseluruhan**Mod siasatan**

Rekod

Semua jenis sumber, tindakan sendiri, profil sumber dan 200 mesej terpapar terkini daripada sumber yang baru ditemui.

Sembang baru

Sembang atau bot baru mendapat profil dan potret sejarah.

Pilih untuk

Sertailah pasukan atau berinteraksilah dengan bot melalui panel. Semak dan simpan pratetap.

**Tidak melakukan** Ia tidak mengambil snapshot setiap sembang sedia ada atau callback pemerhatian yang ditekan dalam klien lain.

Kad-kad ini adalah perbandingan tempatan, bukan kawalan pengumpul langsung. Ia tidak mengubah akaun.

**Tidak melakukan** Tiada mod membaca sembang rahsia, merekod semasa proses dihentikan, menyambung sumber secara sendiri atau mendapatkan sejarah terdahulu melebihi yang diminta snapshot/export.

[Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/)

## Pengumpulan melalui GitHub Actions (pratonton)

Log masuk Telegram baharu, satu sembang, arkib disulitkan dan bukti asal GitHub.

[Buka pembantu pengumpulan](https://phishdestroy.github.io/TgWitness/ms/docs/capture/)

## Apa yang direkodkan

Hanya pemerhatian yang dihantar atau diminta secara eksplisit dimasukkan ke dalam rekod. Atribusi yang tidak diketahui kekal tidak diketahui.

 Rekod suis · ilustrasi tempatanMesej baruSuntinganPembuanganReaksiKeahlian

Panel menerapkan suis ini bagi setiap ruang kerja. Mengaktifkannya mengekalkan rekod sedia ada; menyahtandanya tidak memulihkan semula peristiwa yang terlepas.

**Matriks peristiwa: bahan yang disimpan dan perkara yang masih tidak diketahui**

| Kategori | Disimpan | Tetap tidak diketahui |
| --- | --- | --- |
| Mesej | Teks, ID, metadata penghantar, konteks balasan dan sampul kemas kini asal. | Tiada tandatangan Telegram yang boleh disahkan oleh pihak ketiga. |
| Sunting | Setiap versi yang diperhatikan, tanpa menimpa versi-versi sebelumnya. | Suntingan pertengahan mungkin terlepas; penghantar tidak semestinya penyunting. |
| Pembuangan | Notis serta teks yang telah disimpan sebelum ini, jika tersedia. | Penghapus dan masa tindakan tepat tidak disertakan. |
| Pembuangan tanpa skop | Notis peringkat akaun; rakan sebaya yang tidak diketahui kekal nyata. | Tiada sembang yang diandaikan. Korelasi menggunakan ID skop akaun yang disimpan sebelum ini apabila boleh. |
| Reaksi | Pengira yang dihantar dan identiti terkini yang kelihatan. | Tidak semua reaktor boleh dilihat; senarai penuh yang tersedia memerlukan pertanyaan berasingan. |
| Keahlian | Mesej perkhidmatan dan kemas kini peserta dihantar. | Peranan dan jenis sembang mengehadkan keterlihatan; kesunyian tidak membuktikan ketiadaan. |
| Lampiran | Penerang versi asal, bait yang disimpan, SHA-256 dan hasil percubaan. | Fail yang hilang mungkin tidak tersedia; versi yang lebih baru tidak menggantikannya. |
| Siaran sejarah | Mesej yang kini kelihatan, ditandakan sebagai pemerhatian sejarah. | Suntingan terdahulu dan kandungan yang hilang tidak akan dibina semula. |
| Tindakan sendiri | Keluar messages/edits dan papan kekunci balasan yang sepadan button_press metadata. | Callback yang ditekan dalam klien Telegram lain tidak dapat dilihat. |
| Butang bot | Callback, URL, aplikasi web dan metadata permintaan disimpan bersama mesej. | URL dan phone/location permintaan adalah teks, tidak dibuka atau dijalankan secara automatik. |

### Had lampiran lalai

Foto

20 MiB

Video

100 MiB

Fail

50 MiB

Animasi

20 MiB

Nota video

50 MiB

Suara

20 MiB

Audio

50 MiB

Pegunaman

5 MiB

**Tidak melakukan** Suwayt tidak menyembunyikan metadata tersemat atau menyahaktifkan rekod operasi. Rakaman tidak mengenal pasti pelaku yang tidak dibekalkan oleh Telegram.

[Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/)

## Gunakan kebenaran yang anda ada

Setiap akaun mempunyai ruang kerja, jurnal, kunci penandatanganan, laluan dan barisan sendiri.

### Telefon + kod

Masukkan 2FA apabila diaktifkan.

### QR kod

Imbas daripada peranti yang dibenarkan; 2FA mungkin masih diperlukan.

### Telethon .session

Import fail sesi akaun.

### Pyrogram .session

Import yang disokong Pyrogram format sesi.

### TData ZIP

Satu akaun Desktop disokong; kod laluan tempatan jika ditetapkan.

### StringSession teks

Tempelkan a Telethon StringSession.

### .session + .json

Pilih sesi dan metadata rakan yang sepadan.

### KunciAuth HEX + DC ID

Import kebenaran akaun dengan pengecam pusat data-nya.

**API pasangan**

Anda sendiri API pasangan adalah pilihan. Tanpa satu, TgWitness menggunakan kolam pasangan awam, termasuk pasangan daripada Telegram Desktop rasmi.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy adalah eksperimental; terbina dalam awam MTProxy senarai tersedia. Laluan proksi yang gagal tidak beralih semula kepada sambungan terus.

Dua ruang kerja pada satu mesin bukanlah dua saksi bebas.

**Tidak melakukan** Import tidak memintas kebenaran Telegram, 2FA atau format sesi yang tidak disokong. Akaun masih berkongsi proses aplikasi.

[Format akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/)

## Tindakan daripada panel

Hantar atau balas, tekan butang bot semasa, simpan pratonton pautan, kemudian sertai sembang secara eksplisit atau mulakan bot dengan parameter permulaannya.

`interaction.preview``interaction.requested``interaction.result`

Kuitans preview, permintaan dan hasil ditandatangani. Sebelum butang ditekan, pelayan memuat semula mesej dan menolak papan kekunci yang diubah. Teks dan URL callback yang dikembalikan kekal sebagai konteks yang direkodkan.

**Tidak melakukan** Tiada aplikasi web, pembayaran, phone/location kongsi atau pertanyaan dalam talian. Memaparkan URL tidak membukanya.

[Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/)

## Pemulihan dan kesinambungan

Jurang ditunjukkan, bukan disembunyikan.

### Sambung semula kedudukan yang disimpan

Selepas dihidupkan semula, Telegram akan meminta kemas kini yang terlepas. Penyimpanan terhad dan perbezaan yang tamat tempoh boleh menyebabkan terdapat jurang.

### Semak semula mesej yang kelihatan

Lalai: memuat sumber keutamaan setiap 15 minit, yang lain setiap 6 jam. Keputusan termasuk message.recovered dan message.missing_on_recheck.

### Bacalah coverage.json

Tempoh pemerhatian, jurang dengan sebab dan ID yang tidak diperhatikan disertakan bersama eksport yang disahkan. Rekod hilang semasa semakan semula bukan notis pemadaman.

**Tidak melakukan** Snapshot sejarah kemudian tidak memadamkan masa henti atau memulihkan setiap versi yang hilang. Penunjuk yang disimpan bukan pengesahan tanpa kehilangan bagi penerimaan jurnal.

[Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

## Tujuh tahap. Soalan berbeza.

Setiap mekanisme menjawab soalan terhad. Konfigurasikan perkhidmatan luaran secara berasingan dan simpan titik rujukan kepercayaan mereka di luar pengumpul.

1. ### Rakam

   SHA-256 rantaian + Ed25519 per acara; yang pertama previous_hash adalah 64 sifar.

   **Semakan pihak ketiga** Pengesanan dan tandatangan di bawah kunci pengumpul yang dipaku.

   **Tidak melakukan** Ia tidak membuktikan asal Telegram atau kelengkapannya.

   **Perintah pengesahan**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Kontena

   manifest.json menyenaraikan hash fail; manifest.sig menandatangani. media.saved mengikat bait lampiran kepada suatu peristiwa.

   **Semakan pihak ketiga** Fail yang disediakan sepadan dengan manif yang ditandatangani dan resit media.

   **Tidak melakukan** Ia tidak menandatangani yang dimuat turun secara berasingan CSV, HTML atau tangkapan skrin.

   **Perintah pengesahan**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Batas yang dikekalkan

   Titik pemeriksaan semasa permulaan, setiap 5 minit secara lalai, dan pemberhentian teratur. Simpan salinan di tempat lain.

   **Semakan pihak ketiga** Eksport kemudian sepadan dengan panjang dan kepala yang disimpan sebelum ini; rollback boleh dikesan.

   **Tidak melakukan** Ia tidak mengesan penggantian kedua-dua jurnal dan semua titik pemeriksaan yang disimpan.

   **Perintah pengesahan**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Masa luaran

   Mod bukti menghantar titik pemeriksaan SHA-256 kepada RFC 3161 pihak berkuasa (FreeTSA, DigiCert) dan OpenTimestamps kalendar.

   **Semakan pihak ketiga** Tindak balas TSA yang disahkan menetapkan tarikh bait-bait tersebut; yang disahkan OpenTimestamps bukti mengikatkannya kepada Bitcoin.

   **Tidak melakukan** Ia tidak menganggap permintaan yang telah disediakan atau resit kalendar yang sedang menunggu sebagai cap masa yang disahkan.

   **Perintah pengesahan**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Saksi bebas

   Host berasingan, hujung bacaan sahaja berbeza skop, cabaran baharu, miliknya sendiri key/journal dan TGW1 pos saluran.

   **Semakan pihak ketiga** Kepala yang diterima sebelum ini; status ok, key_changed, rollback, fork, tidak sah dan no_response.

   **Tidak melakukan** Ia tidak menjadikan dua ruang kerja pada satu hos pengumpul sebagai saksi bebas.

   **Perintah pengesahan**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Salinan luar tapak

   S3 salinan serasi disulitkan dengan AES-256-GCM; Object Lock apabila baldi menyokongnya.

   **Semakan pihak ketiga** Restore hanya menerbitkan fail selepas pengesahan jurnal, titik pemeriksaan dan media terpelihara berjaya.

   **Tidak melakukan** Ia tidak memulihkan tanpa kunci yang dieksport atau menganggap penyimpanan tanpa memeriksa respons penyimpanan.

   **Perintah pengesahan**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Jalankan asal-usul

   Resit pelaksanaan yang disahkan: hash sumber, versi kebergantungan dan konteks proses. Dilaporkan sendiri.

   **Semakan pihak ketiga** Apa yang dilaporkan oleh pengumpul tandatangan mengenai pelaksanaan sendiri.

   **Tidak melakukan** Ia tidak menyediakan pengesahan proses bebas atau mengecualikan pengkomproman sebelum rakaman.

   **Perintah pengesahan**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Apa yang tiada tahap dapat buktikan

Penyampaian setiap kemas kini Telegram; kebenaran teks; bahawa ID penghantar mengenal pasti orang sebenar; ketiadaan kompromi pengumpul sebelum rakaman; kebolehterimaan di mahkamah.

[Saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/)

Tempatan SHA-256 eksperimen

### Cuba ubah rekod 2

Rekod seterusnya mengekalkan pautan yang disimpan sebelum ini. Mengubah teks mengubah hash yang dikira bagi rekod 2.

Teks rekod 2

Rekod 1`h1`Bermula dengan 64 sifar

Rekod 2`h2`Termasuk yang disimpan h1

Rekod 3`h3`Termasuk yang disimpan h2

Contoh statik: h2 menutup "Bertemu pada pukul 11:00". Mengubah teks itu mengubah h2; rekod 3 masih merujuk kepada yang disimpan h2.

**Periksa semua digest sepenuhnya**

Rekod 2 hash disimpan

`SHA-256(e₂)`

Hash rekod 2 dikira semula

`SHA-256(e₂)`

Contoh ini mengira hash, bukan tandatangan. Pengesah sebenar menyemak setiap tandatangan dan pautan dengan kunci yang dipercayai.

 [Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/how-it-works/)

## Pilih laluan melalui bukti

Situasi rekaan. Mulakan pengumpulan sebelum peristiwa yang berkaitan; pelihara sempadan dan jurang bersama kandungan.

### Saluran menukar butiran pembayaran

Mod → peristiwa

Perbualan terpilih → mesej, suntingan, pemadaman.

Keluaran

Versi pos dan lampiran yang diperhatikan mengikut hash.

Pengesahan

Ditandatangani ZIP + checkpoint disimpan + respons TSA disahkan.

**Tidak melakukan** Ia tidak memulihkan asal yang tidak pernah dirakam.

### Mesej akan hilang selepas suatu insiden

Mod → peristiwa

Folder atau keseluruhan akaun → semua kategori peristiwa.

Keluaran

Salinan asal yang disimpan, notis pemadaman dan liputan dengan jurang.

Pengesahan

Ditandatangani ZIP + jurnal saksi bebas.

**Tidak melakukan** Ia tidak mengenal pasti penghapus daripada pemberitahuan yang tidak menyenaraikan sebarang pelaku.

### Siasat bot kedai

Mod → peristiwa

Prset siasatan → butang, pratonton pautan dan permulaan bot secara eksplisit.

Keluaran

Resit interaksi yang disahkan, callback yang dikembalikan dan profil yang disimpan.

Pengesahan

Ditandatangani ZIP; sahkan mana-mana draf terhadap ZIP.

**Tidak melakukan** Ia tidak membuka aplikasi web bot, membuat pembayaran atau merekodkan callback klien lain.

### Seorang peserta menukar nama merentasi sembang

Mod → peristiwa

Sebarang skop → diperhatikan sender/profile metadata.

Keluaran

Sejarah nama/nama pengguna mengikut ID numerik, pautan "juga dalam" dan petunjuk yang diekstrak.

Pengesahan

Dossier JSON diperiksa menentang yang ditandatangani ZIP.

**Tidak melakukan** Ia tidak menjadikan dompet, rentetan seperti telefon atau nama pengguna sebagai identiti yang terbukti.

### Pengamatan jangka panjang dengan salinan luar tapak

Mod → peristiwa

Sebarang skop → Mod bukti dan satu S3 replika dengan sokongan Object Lock.

Keluaran

Salinan disulitkan, titik pemeriksaan disimpan dan tindak balas cop masa.

Pengesahan

Pulihkan dengan kunci yang dieksport, kemudian sahkan tanpa pelayan asal.

**Tidak melakukan** Ia tidak menggantikan saksi bebas atau kunci penyahsulitan yang disimpan secara berasingan.

[Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/investigation/)

## Serahkan pakej yang boleh disemak

Sediakan asal yang ditandatangani, cap jari kunci yang disimpan secara bebas, checkpoint yang berkaitan dan hasil pengesahan.

- Ditandatangani ZIP
- JSONL
- CSV
- HTML
- Titik pemeriksaan
- Jalankan resit
- Eksport sembang: chat.json / chat.html
- Dossier JSON
- Dilindungi kata laluan AES-256 ZIP
- Eksport berasingan untuk beberapa akaun
- CLI penstriman: 5 GiB had lalai

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Dapatkan pengesah daripada salinan yang dipercayai, bukan daripada arkib yang sedang diperiksa.

**Tidak melakukan** Boleh berdiri sendiri CSV dan HTML bukan bekas yang ditandatangani. Kata laluan melindungi kerahsiaan pemindahan, bukan kesahihan. Eksport berbilang tidak menggabungkan jurnal akaun.

[Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

## Bandingkan artifak yang dihantar

Artifak asas tanpa penandatanganan, cap masa atau sistem saksi tambahan. Skrip dan pencatat berbeza mengikut pelaksanaan; "sebahagian" bermaksud terhad kepada bahan yang dirakam atau dapat dilihat.

| Pendekatan | Suntingan / pemadaman | Rakam tandatangan | Masa luaran | Saksi bebas | Liputan / jurang | Pengesahan tanpa pengarang |
| --- | --- | --- | --- | --- | --- | --- |
| Eksport Telegram Desktop | Sebahagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| Telethon skrip snapshot | Sebahagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| Pencatat log pemadaman: log teks | Sebahagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| Skrinshot / tangkapan web | Sebahagian | Tidak | Tidak | Tidak | Tidak | Tidak |
| TgWitness dengan tambahan yang dikonfigurasikan | Sebahagian | Ya | Ya | Ya | Sebahagian | Ya |

**Tidak melakukan** Jadual ini tidak menilai setiap skrip atau produk log. Semakan masa dan saksi pilihan memerlukan perkhidmatan dan jangkar kepercayaan mereka sendiri; tiada yang menetapkan kebenaran sumber.

[Bacalah butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

## Pastikan had selari dengan bukti

Pengesahan berguna apabila skopnya kekal jelas.

- Perbualan rahsia tidak tersedia.
- Tiada apa yang direkodkan semasa proses dihentikan; pemulihan adalah terhad.
- Rekod yang disahkan bukan bukti bahawa kandungannya benar.
- Seorang pengendali dengan kunci boleh menandatangani kandungan sewenang-wenangnya. Saksi bebas dan cap masa mengehadkan penggantian kemudian, bukan tangkapan awal yang tidak jujur.
- Gunakan akaun khusus, bukan akaun utama anda.
- Telegram boleh mengehadkan akaun kerana jumlah permintaan.

**Tidak melakukan** Tiada mod atau tahap bukti menetapkan kebolehterimaan undang-undang, penghantaran Telegram yang lengkap atau identiti dunia sebenar.

[Panduan pemasangan](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms)[Akaun khusus](https://phishdestroy.github.io/TgWitness/ms/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)[INVESTIGASI.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/investigation/)
