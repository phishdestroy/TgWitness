# Format bukti

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/

Kandungan ZIP yang disahkan, jenis rekod, resit proses, profil orang, salinan luar tapak dan pengesahan luar talian.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Bukti & pengesahan](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

TgWitness memelihara pemerhatian Telegram yang boleh dilihat oleh akaun dalam jurnal yang disahkan. Penerima boleh mengesahkan rekod yang disimpan, lampiran dan laporan dengan kunci pengumpul yang dipercayai, kemudian membandingkan jurnal dengan titik pemeriksaan yang disimpan secara bebas. Halaman ini menerangkan format, pemeriksaan dan bahan yang perlu disimpan untuk penyerahan.

Penerima boleh memulakan dengan **VERIFY.cmd** pada Windows: ia meminta ZIP asal dan cap jari kunci yang diperoleh secara bebas, memaparkan keputusan yang dijelaskan, dan menyimpan transkrip pengesahan berasingan. Lihat [pelancar pengesahan dan persekitaran larian mudah alih](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) untuk penyediaan dan had kepercayaan.

**Pada halaman ini**

- [Apa yang ditandatangani](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#what-is-signed)
- [Membandingkan eksport sembang](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#comparing-chat-exports)
- [Serahan siasatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#investigation-handoff)
- [Petikan penyerahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#handover-extract)
- [Laporan yang boleh dibaca](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#readable-reports)
- [Kanonalisasi acara](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#event-canonicalization)
- [Semantik pelaku](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#actor-semantics)
- [Liputan: kesinambungan, jurang dan ID yang tidak diperhatikan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)
- [Pengeluar](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#producer)
- [Profil orang](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#people-profiles)
- [Saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#independent-witness)
- [Manifest dan checkpoint](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#manifest-and-checkpoints)
- [Skop pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope)
- [Lampiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#attachments)
- [Koleksi dan resit proses tahan lama (0.2)](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#durable-collection-and-process-receipts-02)
- [Persiapan RFC 3161 dan pengesahan respons (0.2)](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)
- [Rekod pilihan dalam mod bukti: drand dan peranti Telegram](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)

## Apa itu ditandatangani

| Bahan | Perlindungan | Apa yang perlu disimpan |
| --- | --- | --- |
| Setiap pemerhatian jurnal, termasuk peristiwa operasi | Rantaian SHA-256 dan tandatangan Ed25519 bagi setiap peristiwa | `events.jsonl` asal, cap jari kunci yang dipercayai, dan checkpoint yang dikekalkan |
| Kandungan ZIP bukti | `manifest.sig` menandatangani manif kanonik, yang menyenaraikan hash fail kandungan | Fail ZIP lengkap, termasuk manifes dan tandatangan |
| Lampiran yang disimpan | SHA-256 dan kiraan bait dalam acara `media.saved` yang ditandatangani; hash fail dalam manifes ZIP yang ditandatangani | Byte asal di dalam ZIP yang disahkan |
| Pemeriksaan | Tandatangan Ed25519 merangkumi keseluruhan jurnal, hash kepala, kunci awam, dan masa penciptaan | Salinan bebas yang disimpan sebelum perubahan yang dipertikaikan |
| Resit pelaksanaan | Rekod berasingan versi pengumpul, hash fail sumber dan tetapan permulaan, juga disertakan dalam `process.started` | Resit, jurnal berkaitan dan bukti persekitaran untuk mod pengesahan yang dipilih |
| Laporan yang boleh dibaca: `report.html` dan bahagian-bahagiannya, `report.json`, `report.pdf`, `chat.pdf` | Setiap fail disegel dengan cap Ed25519; PDF juga membawa tandatangan piawai PDF (lihat [Laporan boleh dibaca](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#readable-reports)) | Fail seperti yang diterima dan cap jari kunci dipercayai; ZIP yang diterangkan |
| CSV berdiri sendiri | Tiada tandatangan kriptografi berdiri sendiri; hash peristiwa sahaja tidak mencukupi | Gunakan salinan tepat di dalam fail ZIP yang disahkan untuk pemeriksaan integriti |
| Skrinshot, cetakan, atau PDF yang dihasilkan oleh pelayar | Tiada tandatangan TgWitness pada derivatif | Simpan pakej asal yang disahkan dan dokumentasikan bagaimana derivatif itu dibuat |

Pengumpul mengesahkan tandatangan jurnal sebelum menjana setiap format eksport. Laporan HTML dan PDF yang boleh dibaca mempunyai meterai masing-masing; CSV berdiri sendiri diperiksa sebagai sebahagian daripada ZIP yang ditandatangani. Simpan ZIP untuk mengekalkan bait lampiran dan manifes, serta titik pemeriksaan berasingan untuk menyemak jurnal dengan sempadan terdahulu.

## Membandingkan eksport sembang

Sahkan dan bandingkan dua ZIP eksport sembang yang ditandatangani dengan cap jari penandatangan yang disimpan secara berasingan:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

Apabila kedua-dua arkib merekodkan ID akaun dan sembang numerik yang sama, rekod dipadankan oleh ID mesej. **Tidak berubah** bermaksud kesamaan rekod JSON yang disimpan sepenuhnya: teks penuh, pengarang, tarikh, sasaran balasan, metadata bersarang dan medan tidak diketahui semuanya disertakan. Susunan kunci objek JSON tidak penting; medan yang tiada, nilai null, jenis nilai dan susunan senarai adalah penting. Pratonton 300 aksara hanya untuk paparan. Kemasukan yang diubah dinamakan `changed_fields` aras atas yang berbeza, termasuk perubahan yang tidak kelihatan dalam pratonton tersebut. ID mesej ganda ditolak dan bukannya saling menimpa semasa padanan.

Perbezaan boleh berupa nama paparan yang diubah, bilangan tontonan, anotasi koleksi atau metadata pemerhatian lain. Ia sendiri tidak menetapkan penyuntingan Telegram, mengenal pasti siapa yang membuat perubahan, atau membuktikan arkib bertentangan yang tepat. Rekod yang belum diparsing kekal dalam perbandingan; kesaksamaan representasi yang disimpannya tidak bermakna muatan Telegram mereka telah didekod.

Untuk identiti akaun/perbualan yang berbeza atau hilang, alat ini hanya mencari padanan yang mungkin menggunakan penghantar, teks lengkap, hash fail, jenis media dan toleransi masa lima saat. Ia melaporkan **'Matched'**, bukan **'Unchanged**'. Calon-calon ini tidak menetapkan identiti mesej atau kesetaraan semua metadata. Rekod yang tidak diparsekalkan kekal tidak dipadankan. Perbezaan dalam rekod berpasangan kekal disenaraikan dalam `changed`, termasuk dalam mod kandungan; perbezaan ini tidak membuktikan pengeditan pada mesej yang sama. Dengan `--json`, `matched` mengira pasangan dan `unchanged` mengira pasangan yang rekod simpanannya lengkap dan sama. Tiada satu pun kiraan ini membuktikan identiti mesej dalam mod kandungan. Keluaran `changed_fields` dan integer `unchanged` sedia ada kekal serasi dengan keputusan perbandingan terdahulu. Format arkib dan pengesahan tandatangan tidak berubah.

## Penyerahan siasatan

1. Rakam rujukan kes, pengendali, ID akaun Telegram berangka yang dipilih, dasar pengumpulan, dan tempoh pengumpulan dalam nota kes anda. TgWitness memelihara pemerhatian dan menyokong nota serta koleksi yang dipautkan kepada sumber dalam [Case Board](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-board/). Simpan rekod pemindahan dan pemilikan bersama bahan kes anda. Semak tetapan pengumpulan yang dimaksudkan dengan [prosedur penerimaan secara langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Simpan cap jari kunci awam ruang kerja secara bebas sebelum bergantung kepada eksportnya. Simpan titik pemeriksaan yang ditandatangani di luar pengumpul semasa pengumpulan. Catatkan gangguan dan had keterlihatan akaun.
3. Eksport **ZIP** yang **ditandatangani** dan simpan resit pelaksanaan yang ditandatangani. Gunakan titik pemeriksaan pada atau sebelum sempadan jurnal yang dieksport. Titik pemeriksaan kemudian boleh menolak dengan betul eksport sebelumnya sebagai terlalu pendek. Eksport merangkumi keseluruhan jurnal ruang kerja, tanpa mengira penapis panel; semak bahan sebelum berkongsi.
4. Minta penerima mengesahkan ZIP dengan salinan verifier yang dipercayai dan cap jari/titik pemeriksaan yang dibekalkan secara bebas. Daripada pemeriksaan yang dipercayai dengan persekitaran Python aktif:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Laporan output yang berjaya mengembalikan `key_pinned: true` dan `checkpoint_checked: true` apabila kedua-dua input dibekalkan dan diterima. Pelihara keputusan pengesahan.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Rekod SHA-256 arkib, sempadan eksport, tarikh pemindahan, penghantar, dan penerima dalam rekod pemilikan anda. Biarkan pakej asal utuh dan kerjakan salinan. Kongsi fail bukti dan bukannya direktori data peribadi aplikasi, yang juga mengandungi sesi akaun dan rahsia tandatangan. Untuk pemindahan, eksport boleh dimasukkan ke dalam fail ZIP AES-256 yang dilindungi kata laluan. Kata laluan hanya melindungi kerahsiaan dan tidak disimpan; penerima mengekstrak arkib tersebut dan mengesahkan eksport yang ditandatangani di dalamnya, yang tidak berubah.
   2. Jika penambatan masa bebas diperlukan, ikuti [prosedur RFC 3161](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/) dan simpan permintaan, checkpoint, maklumat CA dipercayai, dan respons pihak berkuasa yang disahkan. Menyediakan permintaan sahaja tidak memperoleh cap masa.

Pengesahan yang berjaya menetapkan integriti berbanding kunci pengumpul yang dipercayai dan sempadan yang dikekalkan. Lihat [skop pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) untuk andaian kepercayaan dan [keputusan pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) bagi semakan yang dijalankan.

## Petikan penyerahan

Fail ZIP yang disahkan memuatkan keseluruhan jurnal ruang kerja. Apabila mahkamah, peguam atau meja penyalahgunaan hanya memerlukan beberapa perbualan, tempoh tertentu atau individu tertentu, **Eksport → Ekstrak Penyerahan** menyediakan salinan minimum (`tgwitness-handover-v1`) mengikut peraturan pendedahan yang dipilih. Pengendali menyatakan tujuan dan memilih sembang, tempoh pilihan (UTC), orang yang berkaitan dengan ekstrak, apa yang berlaku kepada orang lain (dipaparkan, digantikan dengan nama palsu P01, P02… atau diabaikan), teks mesej mana yang kekal, lampiran dan foto profil mana yang disertakan, dan sama ada nombor telefon dan alamat e-mel dalam teks disamarkan. Tujuan dan peraturan ini terdapat dalam manifes yang ditandatangani dan dalam laporan; jurnal merekodkan `handover.exported` dengan akses yang menyediakan ia dan SHA-256 fail, bukan kandungannya.

`verify.py` memeriksa petikan dengan dua cara. Rekod yang ditunjukkan tidak berubah disahkan sepenuhnya: kandungannya dibandingkan dengan hash-nya, tandatangan Ed25519-nya dan pautannya kepada rekod sebelumnya yang disertakan. Rekod yang diminiaturkan mengekalkan hash dan tandatangan asal, jadi tandatangan masih boleh disahkan, tetapi medan yang disembunyikan tidak dapat dikira semula daripadanya; rekod tersebut menyatakan apa yang disembunyikan dan laporan menandakannya. Manifest menyatakan panjang jurnal dan tajuk dengan tandatangan pengumpul di atas tajuk tersebut, dan mengira rekod yang tertinggal; `coverage.json` menerangkan sembang yang dipilih. Nama di dalam nama fail tidak dikesan. Semak fail akhir sebelum berkongsi: teks bebas, nama fail dan lampiran terpilih masih boleh mengenal pasti orang. Simpan ZIP penuh yang disahkan: ekstrak itu adalah pendedahan, bukan pengganti.

## Laporan yang boleh dibaca

Bukti bertandatangan, handover dan fail ZIP sembang mengandungi laporan HTML dan JSON yang boleh dibaca, serta PDF apabila fon yang diperlukan tersedia, dalam bahasa laporan yang dipilih. Setiap laporan disegel dengan kunci Ed25519 ruang kerja dan boleh disahkan secara berasingan: `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]`.

- `report.html` / `chat.html`: pernyataan meterai (`tgwitness-report-seal-v1`) menutup fail dan menandatangani SHA-256 bagi setiap bait sebelumnya. Jurnal dan sembang panjang dibahagikan kepada bahagian bersaiz boleh laras (Tetapan Laporan, 500 hingga 100,000 rekod; 5,000 secara lalai): `records/records-0001.html` atau `messages/messages-0001.html`, masing-masing disegel dengan nombornya, julat dan jumlahnya, serta disenaraikan bersama SHA-256 dalam manifes yang ditandatangani. Susunan degupan jantung pengumpul dipaparkan sebagai satu baris melainkan tetapan Laporan menyenaraikannya satu per satu.
- `report.json` (`tgwitness-report-json-v1`, kunci `format`, `report`, `seal`): meterai menandatangani SHA-256 bagi JSON kanonik `report`, supaya fakta boleh dibaca oleh sistem kes dan skrip dan pilihan untuk perlindungan data boleh dibuat daripadanya sementara fail yang disahkan kekal utuh.
- `report.pdf` / `chat.pdf`: dokumen formal untuk cetakan dan pemfailan, ditandatangani dua kali ke atas bytes yang sama, keseluruhan fail kecuali nilai tandatangan (`/ByteRange`). Tandatangan piawai PDF (`adbe.pkcs7.detached`, CMS dengan SHA-256 dan ECDSA P-256) menggunakan dokumen tandatangan kendiri-terbitan sijil disimpan dalam peti besi ruang kerja; nombor siri subjeknya ialah cap jari kunci Ed25519. Segel Ed25519 dibawa di dalam CMS sebagai atribut tidak ditandatangani `2.25.240684792623320047764573196045913242332` dan menamakan SHA-256 sijil dengan `"content": "pdf-byte-range"`, jadi kunci Ed25519 menjamin sijil itu. Pembaca PDF memaparkan sama ada fail telah diubah selepas ditandatangani dan menganggap penandatangan tidak diketahui sehingga sijil dipercayai; sebaliknya bandingkan cap jari Ed25519. PDF Cina, Jepun dan Korea memerlukan fon pada pelayan (atau dalam `TGWITNESS_FONT_DIR`); tanpa fon tersebut, ZIP hanya mengandungi laporan HTML dan JSON.

Dalam saluran atau superkumpulan, Telegram menyusun nombor mesej 1, 2, 3… mengikut urutan. Eksport sembang menyenaraikan nombor pertama dan terakhir, berapa banyak yang hadir dan setiap siri nombor yang tiada dalam `message-ids.json` , manifes dan tajuk `chat.json` , serta menandakan setiap jurang di mana ia terletak dalam transkrip. `verify.py` menyenaraikannya semula daripada `chat.json` . Nombor yang tiada ialah mesej yang tidak dikembalikan oleh Telegram (dihapuskan sebelum eksport, atau tidak dapat dilihat oleh akaun); dalam sembang peribadi dan kumpulan asas, nombor dikongsi oleh semua sembang dalam akaun dan jurang tidak dikira.

Selepas membaca sejarah, eksport meminta semula setiap nombor yang tiada daripada Telegram, mengikut nombor (`channels.getMessages`, sehingga 10,000 nombor). Keputusannya terdapat dalam `message-ids.json` dan laporan. Jawapan kosong merekodkan bahawa nombor tersebut tidak tersedia untuk akaun ini pada masa semakan semula; ia tidak menyatakan puncanya. Sebarang mesej yang dikembalikan semasa semakan semula akan ditambah ke dalam eksport dan ditandakan dengan `found_on_recheck`.

Setiap laporan dibuka dengan **Secara ringkas**: satu perenggan, kemudian apa yang ditunjukkan oleh bahan tersebut dan apa yang tidak (siapa di sebalik akaun, kelengkapan penghantaran, pemadaman sebelum pemerhatian, masa jam tanpa cap masa). Cop meterai pada halaman itu sendiri bertukar menjadi amber apabila pelayar mengesahkan tandatangan meterai, bukan halaman: pelayar tidak memberikan halaman itu baitnya sendiri. Ia bertukar hijau hanya apabila pembaca meletakkan fail ke dalam pemeriksaan di hujung halaman dan setiap bait sepadan, dan hanya jika halaman yang dipaparkan adalah fail tersebut; jika tidak, ia bertukar merah.

Setiap laporan menamakan program dengan tepat: komit git apabila pengumpul dijalankan daripada checkout atau pemasang menetapkan `TGWITNESS_COMMIT`, dan SHA-256 bagi fail sumbernya (`source_tree_sha256`, JSON kanonik bagi laluan → SHA-256 setiap `.py`, `.js`, `.css`, `.html` dan `.svg` dalam pakej), yang dihasilkan semula oleh checkout komit tersebut melainkan fail telah diubah. Klien Telegram dinamakan mengikut perpustakaan, lapisan API dan pusat datanya. Apabila pemerhatian bermula dan apabila eksport sembang bermula dan berakhir, pengumpul meminta masa daripada Telegram (`updates.getState`, saat penuh) dan merekod masa Telegram tolak jam pengumpul, dengan ketidakpastian daripada perjalanan pergi dan balik; laporan menunjukkan ukuran ini di bawah Rantaian Pemilikan. Eksport sembang juga merekodkan bila ia membaca sejarah, selain tarikh mesej-mesej.

### Pemapar laporan luar talian dan panduan arkib

Ekstrak keseluruhan fail ZIP sebelum membuka `chat.html` atau `report.html`. Pemapar menyediakan carian, penapis, peserta, penunjuk, butiran rekod dan pilihan JSON/CSV tanpa pelayan. Simpan `viewer/` dan `media/` di sebelah laporan. Pilihan adalah turunan: gunakan `verify.py SELECTION.json
--evidence ARCHIVE.zip` untuk membandingkannya dengan arkib yang ditandatangani. Pemverifikasi memeriksa ID laporan, kunci penandatanganan, sempadan arkib dan setiap item yang dipilih; item yang disunting, hilang dan berganda akan gagal. Nota pemilihan dan masa penciptaan kekal sebagai metadata tanpa tandatangan.

Jurang nombor mesej hanya dipaparkan untuk aliran sembang menaik yang lengkap dan tidak disaring. Menyembunyikan kategori atau kegagalan memuatkan ketulan data tidak boleh menjadikan baris yang diabaikan sebagai bukti mesej yang hilang. Sorotan carian dijalankan pada teks biasa sebelum pelarian HTML, mengekalkan penandaan literal.

Pelayar memeriksa tandatangan manifest, ID dan kunci laporan, serta semua has ratus fail yang disenaraikan. Ia menolak struktur ZIP yang samar atau cacat, nama berganda dan laluan tidak selamat, serta mengehadkan saiz fail kepada 256 MiB dan jumlah keseluruhan kandungan kepada 4 GiB. Gunakan pengesah berdiri sendiri untuk arkib yang lebih besar. Semakan pelayar ini melengkapi semakan pengesah terhadap rantaian jurnal dan semantik data.

`README.txt` mengandungi panduan permulaan, inventori fail yang diselaraskan, arahan pengesahan dan nota format data dalam bahasa laporan, diikuti dengan panduan lengkap Bahasa Inggeris. `SHA256SUMS` merangkumi fail-fail yang disenaraikan di dalamnya, kecuali dirinya sendiri, `manifest.json` dan `manifest.sig`; manif tersurat juga merangkumi `SHA256SUMS`. Kekalkan ZIP asal tanpa diubah dan simpan fail kerja di luar folder yang diekstrak. Laporan PDF termasuk penanda buku seksyen dan pengecaman kes/laporan pada halaman kemudian.

### Perbualan pada masa eksport

Eksport sembang merekodkan apa yang dikatakan oleh Telegram tentang sembang apabila eksport bermula: label Telegram sendiri (`scam`, `fake`, `restricted` dengan sebabnya, `verified`), nama pengguna, keterangan, bilangan ahli dan pentadbir, perbincangan yang dipautkan, perlindungan kandungan, sama ada ahli baru melihat mesej terdahulu dan dari mesej mana dalam akaun ini melihat sejarah (`available_min_id`), tarikh mesej 1 apabila ia adalah penciptaan sembang, dan SHA-256 gambar sembang (disimpan dalam `media/`). Ia merekodkan kedudukan akaun yang mengeksport dalam sembang: peranan, tarikh sertai, siapa yang menjemputnya dan, untuk pentadbir, haknya. Sebarang permintaan yang ditolak oleh Telegram dinamakan sebaliknya.

Apabila akaun yang mengeksport adalah pentadbir, eksport membaca log pentadbir sembang (Telegram menyimpan selama kira-kira 48 jam) ke dalam `admin-log.json`: pemadaman dan suntingan beserta kandungan dan akaun yang bertindak. Ia adalah satu-satunya rekod pemadaman yang menyatakan siapa yang memadam.

### Petunjuk

Laporan menyenaraikan, dan arkib menyimpan sebagai `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) dan `indicators.misp.json` (peristiwa MISP ), apa yang boleh diambil tindakan oleh meja penyalahgunaan dalam mesej yang dirakam: pautan dan domain (juga disembunyikan di sebalik teks, dalam butang dan dalam pratonton pautan), alamat mata wang kripto, nama pengguna Telegram dan pautan jemputan, nombor telefon, alamat e-mel dan gambar yang disimpan. Alamat Bitcoin, Litecoin, Dogecoin dan TRON disenaraikan hanya apabila checksum base58 mereka sah, alamat segwit apabila checksum bech32 atau bech32m mereka sah dan alamat TON apabila CRC mereka sah; alamat EVM dan Solana ditandakan sebagai tidak disemak. Gambar mempunyai hash persepsi SHA-256 (dHash, 64 bit) yang kekal hampir tidak berubah pada salinan yang dimampatkan semula atau diubah saiznya. Laporan menulis penunjuk supaya ia tidak terbuka secara tidak sengaja (`hxxps[://]example[.]com` ); fail mengekalkan nilai seperti sediakala. Setiap penunjuk ditandakan sebagai tidak diketahui dan bukan untuk pengesanan automatik (STIX `indicator_types: unknown` , MISP `to_ids: false` , pengedaran kepada organisasi sendiri): disenaraikan menunjukkan bahawa mesej itu mengandungkannya, bukan bahawa ia berniat jahat. Pautan yang teksnya menunjukkan alamat berbeza daripada yang dibuka akan ditandakan dalam laporan.

Laporan PDF diakhiri dengan deklarasi pemeriksa untuk ditandatangani dengan tangan, senarai semak untuk notari atau pakar mahkamah, dan kod QR (juga pada halaman pertama) dengan ID laporan, cap jari kunci dan SHA-256 data berkuasa, supaya cetakan boleh menjejak kembali ke arkibnya.

## Kanonalisasi acara

Input hash terdiri daripada tepatnya medan-medan ini:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Memerialisasikan menggunakan JSON serasi Python dengan UTF-8, kunci objek disusun, tiada pelarian ASCII, tiada ruang kosong tidak penting, dan tiada NaN/infiniti:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

SHA-256 bagi bait-bait tersebut menjadi hash peristiwa. Tandatangan adalah Ed25519 ke atas 32 bait hash mentah, kemudian disulitkan dalam base64. previous_hash pertama ialah 64 sifar. Nombor urutan bermula pada 1 dan bertambah 1. Semua peristiwa, termasuk peristiwa operasi, berkongsi satu rantaian. Tiada penindasan penghantaran dwi: pemerhatian berulang adalah resit berasingan, bukan tuntutan tindakan Telegram berasingan.

Tarikh mentah Telegram adalah rentetan ISO; medan binari menjadi objek yang mengandungi bytes_base64. Teks mesej, entiti, penerang media, metadata balasan, reaksi, dan tindakan perkhidmatan dikekalkan dalam metadata mesej mentah apabila dibekalkan.

observed_at ialah jam dinding UTC pengumpul. source_at ialah tarikh Telegram yang dibekalkan apabila tersedia. Pemberitahuan pemadaman tidak membekalkan masa pemadaman yang tepat, jadi source_at kekal kosong. Susunan penerimaan penghantaran tidak semestinya mengikut susunan peristiwa sumber. Snek sejarah menggunakan tarikh sumber yang lebih lama tetapi masa pemerhatian semasa.

## Semantik pelaku

message.new actor_id ialah penghantar mesej. message.edited tiada penyunting yang dijangka; payload.sender_id merekod penghantar mesej yang diperhatikan. Pembuangan actor_id kekal sifar. Mesej perkhidmatan keahlian mengekalkan penghantar dan jenis tindakan, tanpa menukar setiap pemindahan menjadi peletakan jawatan sukarela. Kemas kini peserta mentah mengekalkan actor_id seperti yang diberikan. Snapshot reaksi tidak mencipta pelaku perubahan.

Notifikasi pemadaman untuk sembang peribadi dan kumpulan biasa hanya mengandungi ID mesej. Sembang-sembang tersebut berkongsi satu urutan ID untuk seluruh akaun, jadi satu ID mengenal pasti satu mesej tunggal bagi akaun ini. Apabila mesej dengan ID tersebut disimpan sebelum ini dalam jurnal ini, pemadaman itu direkodkan dalam sembang tersebut sebagai message.deleted dengan payload.chat_resolution yang menamakan kaedah tersebut. ID yang tidak pernah disimpan disimpan sebagai deletion.unscoped tanpa chat_id; tiada apa-apa yang diandaikan. Saluran dan superkumpulan mengira bilangan mesej bagi setiap sembang dan tidak pernah dipadankan dengan cara ini. Apabila mesej yang dipadam dihantar oleh akaun yang diperhatikan, payload.deleted_message_was_outgoing adalah benar; pemadam masih tidak disertakan.

Notis tanpa skop tidak menetapkan bahawa mesej tidak pernah disimpan: sembang yang sepadan mungkin berada di luar skop pemerhatian semasa, atau padanan unik mungkin tidak tersedia. Semakan semula ketiadaan kekal sebagai pemerhatian berasingan daripada pemberitahuan pemadaman dalam kiraan laporan, penapis dan label. Pemulihan kemudian membersihkan status hilang semasa sambil mengekalkan semakan tidak berjaya terdahulu dalam sejarah yang disahkan; tiada satu pun pemerhatian menetapkan pemberitahuan pemadaman.

Beberapa ID yang diselesaikan ke sembang yang sama daripada satu pemberitahuan digolongkan sebagai `deletion.batch`, tanpa mengira bilangannya. Pemberitahuan itu tidak menyatakan bahawa keseluruhan sejarah telah dipadamkan, siapa yang melakukan pemadaman, atau sama ada ia terpakai kepada semua peserta. Mesej keluar yang disimpan tidak mengubah had ini. Jurnal lama mungkin mengandungi acara `history.cleared` yang disimpulkan daripada kelompok sepuluh atau lebih ID, dengan teks penjelasan yang menyabitkan pemadaman itu kepada peserta lain. Kesimpulan tersebut tidak disokong oleh kemas kini ini. Pelihara rekod tandatangan asal tersebut, tetapi anggap ia sebagai pemberitahuan pemadaman berkumpulan; antara muka semasa menandanya dengan sewajarnya.

## Liputan: kesinambungan, jurang dan ID yang tidak diperhatikan

Setiap fail ZIP yang disahkan mengandungi `coverage.json`; laporan HTML dibuka dengan ringkasan yang sama, dan `verify.py` mengira semula ia daripada `events.jsonl` dan bukannya mempercayai fail tersebut:

- **Dipantau secara berterusan dari X hingga Y.** Satu tempoh bermula dengan `observation.started` dan berakhir pada jeda, pemberhentian, kehilangan sambungan Telegram, log keluar, permulaan proses tanpa pemberhentian yang teratur, atau lebih daripada tiga minit tanpa sebarang rekod semasa memantau (denyutan jantung direkodkan setiap minit, jadi kesunyian bermakna proses berhenti, beku atau komputer berehat). Apabila selang denyutan jantung diubah dalam **Parameter**, setiap denyutan jantung direkodkan dan kesunyian yang dibenarkan menjadi tiga selang, tidak pernah kurang daripada tiga minit.
- **Kekosongan** menyenaraikan masa antara tempoh beserta sebab. Kekosongan yang masih terbuka pada rekod terakhir ditandakan sebagai`not_resumed_by_last_record`.
- **ID mesej yang tidak diperhatikan.** Bagi saluran dan superkumpulan, yang menyenaraikan bilangan mesej bagi setiap sembang, ID yang hilang di antara mesej yang diperhatikan disenaraikan sebagai julat. Mereka dilaporkan sebagai tidak*diperhatikan* — dipadam, tidak pernah dihantar, atau di luar sejarah yang disimpan — tetapi tidak pernah dilaporkan sebagai dipadam. Sembang peribadi dan kumpulan biasa berkongsi urutan di seluruh akaun, jadi jurang dalam salah satu sembang tersebut tidak bermakna apa-apa dan tidak disenaraikan di situ.
- Notis jurang pada peringkat sembang (contohnya Telegram meminta pemulihan perbezaan dalam satu saluran) dikira sebagai nota; ia tidak mengganggu liputan global.

### Nombor mesej yang hilang (`gap_summary`)

**Pratinjau.** `coverage.json` → `gap_summary` mengukur nombor yang diberikan oleh Telegram dan yang tidak pernah dilihat oleh pengumpul ini. Telegram menombor mesej sekali bagi setiap saluran atau superkumpulan, dan sekali bagi setiap akaun merentasi sembang peribadi, bot dan kumpulan biasa. Nombor antara dua mesej yang diperhatikan sama ada diperhatikan atau hilang; julat bersebelahan adalah kenyataan positif bahawa setiap mesej yang bernombor di dalamnya telah diperhatikan. Kelompongan tidak menyatakan sebarang pelaku atau sebab.

| Medan | Maksud |
| --- | --- |
| `status` | `on`, atau `off` apabila dilumpuhkan dalam **Parameter → Analisis jurang** |
| `parameters` | Parameter yang menghasilkan keputusan, supaya ia boleh diulang |
| `chats[]` | Satu entri bagi setiap saluran atau superkumpulan, masing-masing bernombor sendiri |
| `account` | Susunan merentas akaun bagi sembang peribadi, bot dan kumpulan biasa |
| `status` (per urutan) | `applicable`, atau `not_applicable` dengan `reason` |
| `observed_from`, `observed_to`, `span` | Nombor pertama dan terakhir yang diperhatikan dan saiz julat |
| `observed`, `observed_without_content` | Nombor yang diperhatikan; nombor yang hanya diketahui melalui rekod pemadaman atau semakan semula |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Nombor yang tidak pernah diperhatikan, bahagian mereka dalam julat, berapa banyak larian, larian terpanjang |
| `clusters[]` | Jurang yang disenaraikan: `low`, `high`, `missing`, dan nombor jiran yang diperhatikan `after` / `before` dengan masa pemerhatian mereka |
| `service_estimate` | Hanya apabila diaktifkan: berapa banyak nombor yang hilang akan menjadi mesej perkhidmatan pada bahagian yang diperhatikan. Tidak pernah ditolak daripada `missing` |

Kesahihan diperoleh daripada jurnal, tidak pernah diandaikan:

- **Saluran dan superkumpulan** diukur bagi setiap sembang, juga dalam eksport sembang terpilih. Rekod yang dipilih oleh penghantar membentuk ukuran `not_applicable`.
- **Susunan peringkat akaun** diukur hanya dari mesej pertama hingga mesej terakhir yang telah diterima semasa pengumpulan seluruh akaun diaktifkan dan merangkumi sembang peribadi, bot, kumpulan biasa serta mesej akaun itu sendiri, tanpa sebarang sembang dikecualikan (`scope.changed`). Nombor yang dinamakan oleh `deletion.unscoped` dikira sebagai diperhatikan tanpa kandungan. Eksport atau penyerahan sembang terpilih tidak dapat mengukurnya. Jika pengumpulan seluruh akaun dipadamkan dan dihidupkan semula, satu nota menyatakan bahawa nombor yang digunakan dalam tempoh tersebut akan muncul sebagai jurang.
- Mesej perkhidmatan adalah rekod jurnal dengan nombor mereka sendiri, jadi ia menutup jurangnya sendiri; anggaran pilihan hanyalah konteks.

`verify.py` mengira semula `gap_summary` daripada `events.jsonl` dengan parameter dalam jurnal yang ditandatangani `coverage.json` ahli (tetapan lalai untuk arkib lama) dan mencetak baris merentas akaun dalam ringkasan liputannya. Arkib tersebut `get_capture_status`(MCP dan baris perintah) mengembalikan ukuran yang sama untuk sembang yang boleh dibaca oleh capaian; urutan merentas akaun hanya untuk capaian yang merangkumi keseluruhan ruang kerja.

Pengamatan berulang bagi satu mesej perkhidmatan dikira sekali, dan anggaran perkhidmatan akaun hanya menggunakan nombor dalam julat yang diukur. Skop yang digunakan mesti mengekalkan mesej akaun itu sendiri secara eksplisit sebelum pengukuran merentas akaun diaktifkan; rekod lama tanpa maklumat tersebut tidak dapat menetapkan syarat ini. Pengamatan yang dihentikan tidak memanjangkan julat yang diukur, dan memulakannya semula dicatatkan. Permintaan arkib langsung mempunyai bajet masa, termasuk imbasan pangkalan data, dan menandakan pengukuran yang belum selesai sebagai separa.

Telegram mendokumenkan [urutan ID mesej yang berasingan](https://core.telegram.org/api/updates#message-id-sequences). Nombor-nombor ini menerangkan pemerhatian; ia tidak mengenal pasti pelaku pemadaman atau menentukan mengapa sesuatu nombor tiada.

Apabila Telegram berhenti menerima akaun, rekod `coverage.gap` yang menamatkan pemerhatian membawa `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` atau `not_authorized`) dan ralat Telegram; `verify.py` menamakan punca di mana tempoh itu berakhir.

Liputan menggabungkan tempoh pemerhatian yang direkodkan, gangguan dan hasil mesej. Nilai ia bersama sembang terpilih, tempoh dan dasar lampiran; operasi berterusan sahaja tidak mengesahkan penghantaran penuh kemas kini Telegram.

## Pengeluar

Manifester berasingan ZIP bukti, eksport sembang, jurnal saksi dan kenyataan fail profil-orang mengandungi `producer` : perisian, versi, projek (PhishDestroy), laman utama dan repositori sumber. Laporan HTML memaparkan baris yang sama, dan `verify.py` mencetaknya sebagai sebahagian daripada apa yang disahkannya. Arkib yang dibuat sebelum medan ini wujud disahkan sebagai sebelum dan dilaporkan tidak menamakan pengeluar.

Setiap rekod `observation.started` juga menamakan klien Telegram yang memerhati: `api_id` nya (bukan hash), sama ada ia pasangan awam terbina dalam atau aplikasi pengendali sendiri, deskripsi klien yang dihantar dalam permintaan sambungan Telegram, dan jenis laluan sambungan dengan mod IP (tiada alamat proksi atau rahsia). Laporan dan `custody.json` menyenaraikan setiap klien dan laluan berbeza beserta masa ia direkodkan, dan masa di mana tiada proksi yang disenaraikan memberi respons dan Telegram melihat alamat pelayan. Jurnal yang direkodkan sebelum ini menyatakan demikian.

## Profil orang

Fail profil (`tgwitness-dossier-v1`, JSON) dibina atas permintaan daripada rekod yang sudah ada dalam jurnal untuk satu sembang; tiada apa-apa dimuat daripada Telegram dan kandungan profil tidak pernah ditulis ke dalam jurnal (pengaktifan dan pematikan profil direkodkan sebagai `dossier.changed`). Untuk setiap individu yang mempunyai mesej yang disimpan, ia menyenaraikan nama dan sejarah nama pengguna, penanda aras Telegram (bot, penipuan, palsu, premium, disahkan, terhad, dipadam) seperti yang dilihat semasa penyimpanan, profil ID foto, SHA-256 dan hash persepsi (pHash, serasi dengan `imagehash.phash`) avatar daripada cache avatar tempatan dengan avatar serupa, aktiviti (mesej pertama dan terakhir, bilangan, perkongsian yang disunting dan dipadam, mesej mengikut jam UTC), siapa yang membalas kepada siapa, sembang lain dalam jurnal ini di mana orang tersebut menulis, dan menyebut dompet (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; alamat Base58Check disahkan checksum), nombor telefon, nama pengguna dan pautan, termasuk pautan yang disembunyikan di sebalik teks.

Setiap fakta menyenaraikan rekod jurnal (`seq`) yang menjadi sumbernya, dan `record_hashes` menyimpan hash bagi setiap rekod yang dirujuk. Pernyataan itu ditandatangani dengan kunci ruang kerja:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

memeriksa tandatangan, mengesahkan eksport bukti itu sendiri (tandatangan, rantaian hash dan fail) dan bahawa setiap rekod yang dirujuk wujud tanpa diubah dalam eksport yang sama daripada ruang kerja tersebut. Hash avatar dilabel sebagai berasal daripada cache tempatan (bukan rekod jurnal). Kemenyan adalah padanan corak — petunjuk untuk disemak, bukan fakta yang disahkan. Profil diaktifkan bagi setiap sembang, boleh dieksport sebagai fail ZIP AES-256 dengan kata laluan, dan dihapuskan apabila dilumpuhkan atau apabila sembang dikeluarkan daripada sumber.

## Saksi bebas

Jurnal saksi (`tgwitness-witness-v1`) dan kiriman saluran beliau disemak menentang eksport bukti dengan `verify.py --witness … --channel …`; lihat [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/).

## Manifest dan checkpoint

manifest.json merangkumi format, masa eksport, kunci awam, cap jari, panjang jurnal, hash kepala, skop, pengeluar, had, dan SHA-256 bagi setiap ahli kandungan selain `manifest.json` dan `manifest.sig` itu sendiri. manifest.sig ialah tandatangan Ed25519 base64 ke atas JSON manifest kanonik. Pemverifikasi menolak ahli yang tidak dijangka/hilang, nama duplikat, fail rosak, urutan/rantaian terputus, tandatangan tidak sah, dan ketidakpadanan dengan checkpoint yang disediakan. Ia tidak pernah mengekstrak laluan arkib. Ia mengehadkan saiz keseluruhan yang diisytiharkan tanpa mampatan kepada 4 GiB; `--max-gib N` membenarkan arkib yang lebih besar yang dibuat dengan had **Parameter** yang ditingkatkan.

Jalankan pengesahan daripada versi TgWitness yang dipasang atau keluaran semakan. Salinan yang disertakan dalam arkib menyokong penggunaan mudah alih; semak salinan itu dengan pemasangan anda yang dipercayai sebelum menjalankannya.

Satu checkpoint menandatangani kenyataan yang mengandungi kunci awam, panjang jurnal, hash kepala, dan masa penciptaan. Pengesah boleh memeriksa bahawa arkib kemudian mengandungi pendahuluan yang sama. Kekalkan checkpoint di luar pengumpul, supaya pengesahan kemudian membandingkan arkib dengan rujukan yang disimpan secara berasingan daripadanya.

## Skop pengesahan

Pengesahan memeriksa arkib dan mod pengumpulan yang digunakan untuk menjana ia. Pilih mod yang sempadan kepercayaannya sepadan dengan kes, kemudian simpan input pengesahannya.

| Mod pengumpulan | Apa yang diperiksa oleh pengesah | Input pengesahan dan sempadan kepercayaan |
| --- | --- | --- |
| Ruang kerja tempatan | Rekod tandatangan, rantaian hash, manifes dan bait lampiran | Cap jari pengumpul yang disimpan secara bebas; pentadbir hos mengawal kunci tandatangan tempatan |
| Ruang kerja tempatan dengan saksi bebas | Arkib memeriksa dan memadankan dengan awalan jurnal terdahulu yang disimpan oleh saksi | Pisahkan kunci saksi dipercayai dan rekod; titik pemeriksaan mengikat awalan yang telah diperhatikan |
| [Tangkapan GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | Pengesahan GitHub bagi digest arkib, aliran kerja yang diluluskan dan komit pengumpul, pelaksana hos, asal sesi/kunci baharu dan integriti arkib dalaman | Dasar pengesah dipercayai, repositori penelefon dan bundel pengesahan GitHub; pengumpulan dijalankan di bawah aliran kerja yang dipin |
| [Penyebaran awan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/) | Kitar hayat penyedia dan rekod akses, status firewall dan Cloudflare, serta rekod larian berasingan pengumpul yang disahkan | Permintaan baca sahaja kepada penyedia dan Cloudflare; ketersediaan pemeriksaan individu bergantung pada penyedia |
| [VM sulit Intel TDX](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Petik tandatangan dan status platform, pengikatan kepada pernyataan pengumpul, susun dan pengukuran OS | Rantaian kepercayaan Intel dan ukuran penyebaran yang dijangka; kekalkan keputusan setiap pemeriksaan TDX yang diperlukan |

Dalam pemerolehan bermeterai, pengumpul yang diluluskan menerima data melalui sambungan Telegram yang disahkan dalam persekitaran yang disahkan. Pengesahan mengikat arkib kepada pelaksanaan tersebut, jadi pengesahan merangkumi pemerolehan serta integriti fail kemudian. Ini bergantung pada kod yang diluluskan dan rantaian kepercayaan platform yang disenaraikan di atas. Pengesahan tangkapan GitHub memerlukan sesi yang dibuat dalam pelaksanaan dan menolak tangkapan sesi yang diimport.

Resit pelaksanaan merekodkan versi pengumpul, hash fail dan tetapan permulaan. Provenans GitHub dan pengukuran TDX menyediakan semakan persekitaran; [rekod pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) mengenal pasti konfigurasi yang diuji.

TgWitness menandatangani pemerhatian yang dikumpulkannya; Telegram dan pengarang mesej tidak mengeluarkan tandatangan ini. Dalam ruang kerja tempatan, bahan yang dihasilkan sebelum titik pemeriksaan bebas pertama masih bergantung kepada pengumpul dan pemegang kuncinya. Rekod liputan menerangkan skop yang dipilih dan hasil pengumpulan, manakala cap masa luaran yang disahkan menetapkan sempadan arkib atau jurnal yang telah disimpan pada masa tertentu.

## Lampiran

Fail dialamatkan oleh SHA-256 di bawah media/. Acara media.saved memautkan hash dan panjang bait kepada peristiwa mesej tertentu. Nama fail mentah adalah metadata, bukan laluan tempatan. Bait media dimuat turun secara asinkron, jadi pemadaman segera mungkin menghalang perekodan. Pengumpulan dilumpuhkan, fail bersaiz besar/saiz tidak diketahui, kegagalan muat turun, dan muat turun yang terganggu akan dipaparkan sebagai hasil. Kegagalan proses boleh meninggalkan fail separa yang tidak dirujuk; ia tidak disertakan dalam eksport.

Pengeksport ZIP mengesahkan media yang disimpan mengikut nama mereka. Eksport JSONL, CSV, dan HTML mengesahkan tandatangan peristiwa tetapi tidak mengandungi bait media. Laporan turunan disediakan untuk kemudahan; events.jsonl adalah representasi peristiwa yang sah.

Eksport sembang penuh menyimpan lampiran dalam tetapan lampiran ruang kerja ke dalam media/, dinamakan oleh SHA-256. Setiap rekod mesej dalam chat.json menamakan failnya (`file`, `file_sha256`) atau sebab ia tiada (`file_status`), bersama apa yang dilihat pembaca di sekeliling teks: pautan di belakang teks, asal penghantaran, butang bot, tandatangan, jumlah tontonan dan pemasa padam automatik. `verify.py` memeriksa bahawa setiap fail yang dinamakan terdapat dalam manifes berasingan di bawah hash tersebut.

## Koleksi tahan lama dan resit proses (0.2)

Satu job media dan acara pesannya disimpan dalam satu transaksi. Tugas ini menyimpan deskriptor mesej TL asal; pemerhatian yang disahkan mengikat SHA-256, akaun, dan dasar saiznya. Pemulihan mengesahkan ikatan tersebut sebelum memuat turun. Ia tidak pernah mengambil mesej semasa dan secara senyap menggantikan lampiran yang lebih baru. Tugas yang terhenti akan dicuba semula, manakala kegagalan kekal kekal sebagai hasil yang nyata.

Setiap ruang kerja mempunyai jurnal dan identiti tandatangan tersendiri. Peristiwa process.started merangkumi ID larian, jam tempatan, versi kebergantungan, has ratah sumber, akaun/skop awal, dan tetapan rakaman. Denyutan jantung merangkumi ID larian, masa monotonik, dan status barisan. Risit pelaksanaan juga boleh dimuat turun sebagai kenyataan yang ditandatangani secara berasingan. Untuk pengesahan persekitaran pelaksanaan, padankan ia dengan pengesahan GitHub atau semakan TDX yang diterangkan dalam [Skop Pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope).

Titik pemeriksaan automatik disimpan secara tempatan semasa permulaan, setiap lima minit semasa memerhati (**Parameter → Titik pemeriksaan berasingan setiap**), dan semasa pemberhentian yang teratur. Pengesahan permulaan dan eksport membandingkan jurnal dengan titik pemeriksaan tempatan terkini yang disimpan. Ini boleh mengesan pengunduran pangkalan data apabila titik pemeriksaan masih wujud. Penyimpanan bebas memastikan rujukan tersebut tersedia di luar ruang kerja; cap masa luaran yang disahkan juga mengukuhkan kedudukannya dari segi masa.

Selepas dihidupkan semula, kedudukan kemas kini Telegram yang disimpan akan disambung semula (`catch_up_from` dalam `observation.started`) dan kemas kini yang terlepas akan diminta. Semakan semula berkala merekod `message.recovered` untuk mesej yang terlepas dan `message.missing_on_recheck` apabila Telegram tidak lagi memulangkan mesej yang disimpan; yang terakhir bukan notis pemadaman dan tidak menyatakan nama pemadam atau masa.

### Salinan dan pemulihan luar tapak (S3)

Salinan luar tapak (Eksport, lalai dimatikan) memuat naik segmen jurnal, fail yang disimpan, titik pemeriksaan dengan cop masanya dan eksport sembang yang selesai ke storan serasi S3, disulitkan dengan AES-256-GCM sebelum dimuat naik di bawah kunci yang disimpan dalam peti besi ruang kerja; Penahanan Object Lock terpakai apabila baldi menyokongnya. Tanpa kunci yang dimuat turun, salinan tersebut tidak dapat dibaca. Pulihkan dan sahkan dengan `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Pemulihan memerlukan direktori biasa yang kosong. Fail yang dimuat turun dan objek yang telah disahsulit kekal dalam storan sementara peribadi sehingga keseluruhan jurnal dan setiap penanda aras yang disimpan disahkan. Laluan objek yang tidak selamat, julat segmen yang tidak konsisten dan jurnal yang lebih pendek daripada satu penanda aras akan ditolak; pengesahan yang gagal tidak menerbitkan sebarang fail yang dipulihkan. Semakan pengekalan membandingkan mod dan tarikh Kunci Objek yang dikembalikan dengan tarikh akhir yang dihantar semasa pemunggahan (toleransi pemutaran satu saat). Tarikh akhir yang telah tamat tempoh, tidak sah atau dipendekkan tidak dikira sebagai disahkan. Status melaporkan objek sampel yang pengekalanannya dibaca balik untuk pas pemunggahan tersebut.

Media tempatan yang hilang atau rosak dilaporkan sebagai ralat pada pusingan tersebut dan mengekalkan penunjuk media di hadapannya, supaya fail itu dicuba semula pada pusingan seterusnya; fail, titik pemeriksaan dan eksport selepasnya masih disalin. Pemulihan menyemak semua rujukan media yang dipelihara menentang hashes yang telah didekripsi dan saiz yang direkodkan. Segmen jurnal yang bertindih dan identik daripada muat naik yang terhenti akan dipadankan; tumpang tindih yang bercanggah ditolak. Titik pemeriksaan yang dibuat semasa muat naik ditangguhkan sehingga rekod jurnal yang diliputinya disalin, jadi satu pusingan yang selesai tidak menerbitkan titik pemeriksaan di hadapan jurnalnya.

### Snapshot eksport penstriman

Eksport penstriman menggunakan snapshot baca SQLite yang stabil. Snapshot ini mungkin lebih lama daripada jurnal langsung semasa apabila muat turun selesai. Titik pemeriksaan yang dibuat selepas snapshot tersebut boleh melaporkan dengan betul bahawa arkib itu lebih pendek; bandingkan dengan titik pemeriksaan pada atau sebelum awalan yang dieksport, bukan titik pemeriksaan sewenang-wenang yang kemudian.

## Persiapan RFC 3161 dan pengesahan respons (0.2)

Mod bukti (dimatikan secara lalai) hanya menghantar SHA-256 setiap checkpoint yang ditandatangani kepada pihak berkuasa RFC 3161 yang disenaraikan dan kalendar OpenTimestamps, melalui laluan ruang kerja dan tidak pernah melalui MTProxy. Jawapan disimpan dalam `checkpoints/anchors/`, dieksport, dan diperiksa oleh `verify.py` (`--tsa-ca` memeriksa tandatangan TSA; mengesahkan bukti OpenTimestamps dengan `ots upgrade` dan `ots verify`).

Panel menyediakan arkib permintaan yang mengandungi bait checkpoint.json kanonik, cap pesan SHA-256 dan nonse rawak dalam timestamp.tsq, checksum, dan arahan. Tiada permintaan rangkaian dibuat. Persediaan bukan cap masa dipercayai.

`python -m tgwitness.anchor verify` memanggil OpenSSL ts dua kali: sekali terhadap bait checkpoint dan sekali terhadap permintaan asal. Fail CA yang dipercayai diperlukan secara eksplisit; sijil yang disertakan tidak dipercayai secara automatik. Semakan permintaan adalah pilihan di CLI, jadi simpan dan gunakan --request untuk menyemak nonce. Keputusan menyatakan sama ada ia telah disemak. Tandatangan dan jurnal titik pemeriksaan pengumpul masih perlu disahkan secara berasingan dengan cap jari pengumpul yang dipercayai.

Pengesahan memeriksa tandatangan respons, bait penanda aras dan, apabila disediakan, permintaan asal di bawah kepercayaan CA yang dinyatakan. Semakan pembatalan dan pengesahan arkib jangka panjang selepas tamat tempoh sijil berada di luar pengesah semasa. Lihat [prosedur](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/) dan [keputusan pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/).

## Rekod pilihan dalam mod bukti: peranti drand dan Telegram

Dua rekod lagi boleh dijalankan pada pas yang sama seperti cap masa. Kedua-duanya dimatikan secara lalai dan hanya berkuat kuasa semasa mod bukti dihidupkan: Tambahan → Bukti & sandaran → **Lebih ramai saksi · pilihan**, atau `"drand": true` dan `"devices": true` dalam `POST /api/evidence`. Satu kegagalan tidak menghentikan yang lain atau cap masa; panel menunjukkan keputusan terkini bagi setiap satu di bawah borang.

**drand** (`beacon.drand` ). Setiap pusingan menulis pusingan terkini drand quicknet, kebolehubahan rawak awam Liga Entropi (sepusingan setiap 3 saat), ke dalam jurnal: `chain` , `round` , `randomness` , `signature` , `round_time` dan `relay` yang menjawab. Pusingan yang disahkan dan tidak dapat diramalkan menyediakan rujukan masa bawah untuk bahan pautan-hash seterusnya. Cap masa yang disahkan pada titik pemeriksaan kemudian menyediakan rujukan masa atas. Semakan ini mengehadkan bahan yang dipautkan; liputan pengumpulan dinilai secara berasingan. Pengumpul bertanya kepada `drand.cloudflare.com` terlebih dahulu, kemudian kepada relai Protocol Labs, melalui laluan ruang kerja, satu permintaan setiap pusingan.

`verify.py` memeriksa bahawa setiap kebetulan adalah SHA-256 tandatanganannya dan bahawa masa pusingan adalah tepat, dan melaporkan pusingan-pusingan, rentetan terpanjang tanpa satu dan sejauh mana jam kolektor ketinggalan di belakang drand. Ia tidak memeriksa tandatangan BLS. `--check-drand` membandingkan pusingan dengan relai Cloudflare dan relai Protocol Labs, kesemuanya atau sampel rawak seratus dalam jurnal panjang; pusingan yang berbeza akan gagal pengesahan.

**Peranti Telegram** (`account.devices`). Setiap pusingan membaca sesi akaun dengan `account.getAuthorizations`, senarai yang dipaparkan oleh Telegram dalam Tetapan → Peranti, dan merekamnya: secara penuh apabila ia berubah sejak pusingan sebelumnya, dengan `added` dan `removed` hash sesi, jika tidak hanya kiraannya dan SHA-256. Model peranti, platform, aplikasi dan versi, penciptaan dan aktiviti terakhir, negara dan rantau disimpan; alamat IP tidak, kerana pembuangan bukti keluar dari tangan anda. Sesi pengumpul sendiri sentiasa aktif, jadi hanya aktiviti sesi lain dikira sebagai perubahan. `verify.py` melaporkan berapa kerap senarai itu direkodkan dan setiap sesi baharu dan yang berakhir. Ia membaca senarai hanya semasa pemerhatian dijalankan.

Apa yang mereka tidak tunjukkan: drand membuktikan tidak lebih daripada susunan rekod berbanding masa awam, dan senarai peranti adalah pernyataan Telegram melalui pengumpul, ditandatangani oleh pengumpul seperti setiap rekod lain.

Log Gateway **Cloudflare** (`cloudflare.gateway_dns`). Untuk pelayan yang menyelesaikan melalui Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), setiap salinan menyalin apa yang direkodkan oleh Gateway sejak salinan sebelumnya: satu rekod bagi setiap tingkap maksimum tiga jam dengan `from`, `until`, `location_id`, `address` pelayan apabila ditetapkan, dan `queries` sebagai `[at, name, type, rcode, decision, colo]`, juga apabila tiada. Aturkannya di bawah log Gateway Cloudflare ****: akaun, lokasi, alamat pilihan dan token baca sahaja (Akaun Analitik Dibaca; PII Amanah Sifar Dibaca untuk menyimpan satu alamat lokasi kongsi). Panel memeriksa mereka dengan satu permintaan sebelum menyimpan; token kekal disulitkan dan tidak pernah dimasukkan ke dalam jurnal. `verify.py` menyenaraikan tetingkap, nama yang paling kerap dicari dan sebarang masa tiada salinan merangkumi; rekod yang bilangannya tidak sepadan dengan cariannya akan gagal. Sebuah tetingkap yang memuat lebih daripada satu halaman pertanyaan dalam satu saat akan menyimpan halaman tersebut dan menyatakan baki pertanyaan yang hilang. Salinan itu ialah jawapan Cloudflare melalui pengumpul, yang ditandatangani oleh pengumpul; dalam masa 24 jam, sesiapa sahaja yang mempunyai token baca sahaja boleh membandingkannya dengan Cloudflare.
