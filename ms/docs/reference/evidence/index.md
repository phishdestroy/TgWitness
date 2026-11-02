# Format bukti

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/

Kandungan ZIP yang disahkan, jenis rekod, resit proses, profil orang, salinan luar tapak dan pengesahan luar talian.

Perhatian bukanlah kesimpulan. ID penghantar bukanlah identiti sebenar di dunia nyata. Kemas kini perkhidmatan yang boleh dilihat oleh akaun adalah sumbernya; Telegram tidak menandatangani secara kriptografi rekod yang disimpan ini untuk penyiasat pihak ketiga.

## Apa itu ditandatangani

| Bahan | Perlindungan | Apa yang perlu disimpan |
| --- | --- | --- |
| Setiap pemerhatian jurnal, termasuk peristiwa operasi | Rantaian SHA-256 dan tandatangan Ed25519 bagi setiap peristiwa | `events.jsonl` asal, cap jari kunci yang dipercayai, dan checkpoint yang dikekalkan |
| Kandungan ZIP bukti | `manifest.sig` menandatangani manif kanonik, yang menyenaraikan hash fail kandungan | Fail ZIP lengkap, termasuk manifes dan tandatangan |
| Lampiran yang disimpan | SHA-256 dan kiraan bait dalam acara `media.saved` yang ditandatangani; hash fail dalam manifes ZIP yang ditandatangani | Byte asal di dalam ZIP yang disahkan |
| Pemeriksaan | Tandatangan Ed25519 merangkumi keseluruhan jurnal, hash kepala, kunci awam, dan masa penciptaan | Salinan bebas yang disimpan sebelum perubahan yang dipertikaikan |
| Resit pelaksanaan | Pengukuran kolektor yang ditandatangani secara berasingan; juga disertakan dalam peristiwa `process.started` yang ditandatangani | Resit dan jurnal berkaitan; ukuran dilaporkan sendiri |
| CSV atau HTML berdiri sendiri | Tiada tandatangan kriptografi berdiri sendiri; hash peristiwa sahaja tidak mencukupi | Gunakan salinan tepat di dalam fail ZIP yang disahkan untuk pemeriksaan integriti |
| Skrinshot, cetakan, atau PDF yang dihasilkan oleh pelayar | Tiada tandatangan TgWitness pada derivatif | Simpan pakej asal yang disahkan dan dokumentasikan bagaimana derivatif itu dibuat |

Pengumpul mengesahkan tandatangan jurnal sebelum menjana setiap format eksport. Semakan sumber itu tidak menghasilkan tandatangan pada fail CSV atau HTML yang dimuat turun secara berasingan. Tandatangan acara JSONL yang sah juga tidak menyediakan bait lampiran atau mengesahkan secara berasingan bahawa keseluruhan jurnal yang diperhatikan telah dibekalkan.

## Penyerahan siasatan

1. Rekod rujukan kes, operator, ID akaun Telegram berangka yang dipilih, sumber yang dipilih, dasar pengumpulan, dan tempoh pengumpulan dalam nota kes anda. TgWitness mengekalkan pemerhatian; penugasan kes dan rekod tahanan diuruskan di luar aplikasi. Kenal pasti susunan pengumpulan yang dimaksudkan dengan [prosedur penerimaan secara langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

Pengesahan yang berjaya menetapkan integriti berbanding kunci pengumpul yang dipercayai dan sempadan yang dikekalkan. Kebenaran sumber, penghantaran Telegram yang lengkap, masa yang dipercayai, dan kebolehterimaan undang-undang memerlukan bukti berasingan. Versi ini belum melengkapkan kelayakan Telegram langsung atau penilaian forensik/keselamatan bebas.

Kunci pengumpul yang disalin boleh menandatangani jurnal pengganti palsu. Pengesahan terhadap checkpoint yang disimpan secara bebas atau rekod saksi mengesan prefiks awal yang telah diubah; pengesahan tandatangan sahaja tidak dapat melakukannya. Saksi menetapkan apa yang dibentangkan oleh pengumpul, jadi ia tidak menegakkan kebenaran rekod yang dicipta sebelum checkpoint luaran pertama mereka secara bebas. Laporan penyebaran awan memeriksa konfigurasi dan ukuran yang dilaporkan oleh pengumpul; ia tidak menetapkan bahawa kunci peribadi tidak pernah disalin semasa butstrap.

Notifikasi yang dihantar melalui Apprise mengandungi nama dan bilangan ruang kerja dan sembang; petikan ringkas mesej yang dipadam dan disunting hanya ditambah apabila pengendali mengaktifkannya (dimatikan secara lalai). Ia adalah isyarat kemudahan, bukan bukti: penghantaran tidak dijamin, dan hanya jurnal serta eksport yang disahkan merekodkan apa yang diperhatikan. Dengan proksi ruang kerja, pemberitahuan menggunakan laluan yang sama; perkhidmatan yang tidak dapat menggunakannya, dan laluan MTProxy, akan ditolak.

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

## Liputan: kesinambungan, jurang dan ID yang tidak diperhatikan

Setiap fail ZIP yang disahkan mengandungi `coverage.json`; laporan HTML dibuka dengan ringkasan yang sama, dan `verify.py` mengira semula ia daripada `events.jsonl` dan bukannya mempercayai fail tersebut:

- **Dipantau secara berterusan dari X hingga Y.** Satu tempoh bermula dengan `observation.started` dan berakhir pada jeda, pemberhentian, kehilangan sambungan Telegram, log keluar, permulaan proses tanpa pemberhentian yang teratur, atau lebih daripada tiga minit tanpa sebarang rekod semasa memantau (denyutan jantung direkodkan setiap minit, jadi kesunyian bermakna proses berhenti, beku atau komputer berehat). Apabila selang denyutan jantung diubah dalam **Parameter**, setiap denyutan jantung direkodkan dan kesunyian yang dibenarkan menjadi tiga selang, tidak pernah kurang daripada tiga minit.
- **Kekosongan** menyenaraikan masa antara tempoh beserta sebab. Kekosongan yang masih terbuka pada rekod terakhir ditandakan sebagai`not_resumed_by_last_record`.
- **ID mesej yang tidak diperhatikan.** Bagi saluran dan superkumpulan, yang menyenaraikan bilangan mesej setiap sembang, ID yang hilang antara yang diperhatikan disenaraikan sebagai julat. Ia dilaporkan sebagai tidak*diperhatikan* — dipadam, tidak pernah dihantar, atau di luar sejarah yang disimpan — tidak pernah sebagai dipadam. Perbualan peribadi dan kumpulan biasa berkongsi urutan merentas akaun, jadi jurang di situ tidak bermakna apa-apa dan tidak disenaraikan.
- Notis jurang pada peringkat sembang (contohnya Telegram meminta pemulihan perbezaan dalam satu saluran) dikira sebagai nota; ia tidak mengganggu liputan global.

Liputan menerangkan apa yang direkodkan oleh pengumpul ini. Ia bukan bukti bahawa Telegram telah menyampaikan setiap kemas kini sepanjang tempoh berterusan.

## Pengeluar

Manifester berasingan ZIP bukti, eksport sembang, jurnal saksi dan kenyataan fail profil-orang mengandungi `producer` : perisian, versi, projek (PhishDestroy), laman utama dan repositori sumber. Laporan HTML memaparkan baris yang sama, dan `verify.py` mencetaknya sebagai sebahagian daripada apa yang disahkannya. Arkib yang dibuat sebelum medan ini wujud disahkan sebagai sebelum dan dilaporkan tidak menamakan pengeluar.

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

Dapatkan kod pengesah daripada sumber yang dipercayai atau salinan bebas yang telah disemak. Pengesah dalam arkib yang tidak dipercayai adalah bahan boleh dilaksanakan yang dibekalkan oleh pengarang arkib tersebut; kehadirannya adalah kemudahan kebolehsusuran, bukan jangkar kepercayaan bebas.

Satu checkpoint menandatangani kenyataan yang mengandungi kunci awam, panjang jurnal, hash kepala, dan masa penciptaan. Pemeriksa boleh menyemak bahawa arkib kemudian mengandungi pendahuluan yang sama. Kekalkan checkpoint di luar pengumpul sebelum perubahan yang dipertikaikan: penyerang yang mengawal kedua-dua arkib dan checkpoint boleh menggantikan kedua-duanya.

Tandatangan sah daripada kunci yang tidak dipasang hanya menetapkan konsistensi dalaman. Malahan kunci yang dipasang pun tidak dapat membuktikan kandungan sumber yang benar jika pengumpul atau kunci telah dikompromi sebelum merekod. Pemeteraian masa luaran dan tangkapan dipercayai adalah keperluan berasingan. TgWitness tidak menjanjikan kebolehterimaan atau pensijilan forensik.

## Lampiran

Fail dialamatkan oleh SHA-256 di bawah media/. Acara media.saved memautkan hash dan panjang bait kepada peristiwa mesej tertentu. Nama fail mentah adalah metadata, bukan laluan tempatan. Bait media dimuat turun secara asinkron, jadi pemadaman segera mungkin menghalang perekodan. Pengumpulan dilumpuhkan, fail bersaiz besar/saiz tidak diketahui, kegagalan muat turun, dan muat turun yang terganggu akan dipaparkan sebagai hasil. Kegagalan proses boleh meninggalkan fail separa yang tidak dirujuk; ia tidak disertakan dalam eksport.

Pengeksport ZIP mengesahkan media yang disimpan mengikut nama mereka. Eksport JSONL, CSV, dan HTML mengesahkan tandatangan peristiwa tetapi tidak mengandungi bait media. Laporan turunan disediakan untuk kemudahan; events.jsonl adalah representasi peristiwa yang sah.

## Koleksi tahan lama dan resit proses (0.2)

Satu job media dan acara pesannya disimpan dalam satu transaksi. Tugas ini menyimpan deskriptor mesej TL asal; pemerhatian yang disahkan mengikat SHA-256, akaun, dan dasar saiznya. Pemulihan mengesahkan ikatan tersebut sebelum memuat turun. Ia tidak pernah mengambil mesej semasa dan secara senyap menggantikan lampiran yang lebih baru. Tugas yang terhenti akan dicuba semula, manakala kegagalan kekal kekal sebagai hasil yang nyata.

Setiap ruang kerja mempunyai jurnal dan identiti tandatangan sendiri. Peristiwa process.started merangkumi ID larian, jam tempatan, versi kebergantungan, has sumber fail, akaun/skop awal, dan tetapan tangkapan. Detak jantung merangkumi ID larian, masa monotonic, dan status barisan. Resit proses juga boleh dimuat turun sebagai kenyataan yang ditandatangani secara berasingan. Ukuran fail dilaporkan sendiri dan bukan pengesahan perkakasan yang dipercayai.

Pemeriksa automatik disimpan secara tempatan semasa permulaan, setiap lima minit semasa memantau (**Parameter → Pemeriksa berasingan setiap**), dan semasa pemberhentian yang teratur. Pengesahan permulaan dan eksport membandingkan jurnal dengan checkpoint tempatan terkini yang disimpan. Ini boleh mengesan pengunduran pangkalan data apabila checkpoint masih wujud; seorang pengendali yang mengawal kedua-duanya masih boleh menggantikan kedua-duanya. Penyimpanan bebas dan cap masa luaran yang dipercayai kekal sebagai keperluan berasingan.

Selepas dihidupkan semula, kedudukan kemas kini Telegram yang disimpan akan disambung semula (`catch_up_from` dalam `observation.started`) dan kemas kini yang terlepas akan diminta. Semakan semula berkala merekod `message.recovered` untuk mesej yang terlepas dan `message.missing_on_recheck` apabila Telegram tidak lagi memulangkan mesej yang disimpan; yang terakhir bukan notis pemadaman dan tidak menyatakan nama pemadam atau masa.

### Salinan dan pemulihan luar tapak (S3)

Salinan luar tapak (Eksport, lalai dimatikan) memuat naik segmen jurnal, fail yang disimpan, titik pemeriksaan dengan cop masanya dan eksport sembang yang selesai ke storan serasi S3, disulitkan dengan AES-256-GCM sebelum dimuat naik di bawah kunci yang disimpan dalam peti besi ruang kerja; Penahanan Object Lock terpakai apabila baldi menyokongnya. Tanpa kunci yang dimuat turun, salinan tersebut tidak dapat dibaca. Pulihkan dan sahkan dengan `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Pemulihan memerlukan direktori biasa yang kosong. Fail yang dimuat turun dan objek yang telah disahsulit kekal dalam storan sementara peribadi sehingga keseluruhan jurnal dan setiap penanda aras yang disimpan disahkan. Laluan objek yang tidak selamat, julat segmen yang tidak konsisten dan jurnal yang lebih pendek daripada satu penanda aras akan ditolak; pengesahan yang gagal tidak menerbitkan sebarang fail yang dipulihkan. Semakan pengekalan membandingkan mod dan tarikh Kunci Objek yang dikembalikan dengan tarikh akhir yang dihantar semasa pemunggahan (toleransi pemutaran satu saat). Tarikh akhir yang telah tamat tempoh, tidak sah atau dipendekkan tidak dikira sebagai disahkan. Status melaporkan objek sampel yang pengekalanannya dibaca balik untuk pas pemunggahan tersebut.

Kemajuan salinan terhad kepada destinasi dan kunci penyulitan. Menukar titik hujung, baldi atau awalan akan memulakan salinan lengkap jurnal, media dan titik pemeriksaan yang disimpan secara tempatan ke destinasi tersebut. Kemajuan lama yang tidak terhad akan dipelihara tetapi dimainkan semula sekali selepas peningkatan. Eksport sembang sejarah yang telah dialih keluar daripada peti keluar tempatan kekal di destinasi sebelumnya.

Media tempatan yang hilang atau rosak dilaporkan sebagai ralat pada pusingan tersebut dan mengekalkan penunjuk media di hadapannya, supaya fail itu dicuba semula pada pusingan seterusnya; fail, titik pemeriksaan dan eksport selepasnya masih disalin. Pemulihan menyemak semua rujukan media yang dipelihara menentang hashes yang telah didekripsi dan saiz yang direkodkan. Segmen jurnal yang bertindih dan identik daripada muat naik yang terhenti akan dipadankan; tumpang tindih yang bercanggah ditolak. Titik pemeriksaan yang dibuat semasa muat naik ditangguhkan sehingga rekod jurnal yang diliputinya disalin, jadi satu pusingan yang selesai tidak menerbitkan titik pemeriksaan di hadapan jurnalnya.

### Snapshot eksport penstriman

Eksport penstriman menggunakan snapshot baca SQLite yang stabil. Snapshot ini mungkin lebih lama daripada jurnal langsung semasa apabila muat turun selesai. Titik pemeriksaan yang dibuat selepas snapshot tersebut boleh melaporkan dengan betul bahawa arkib itu lebih pendek; bandingkan dengan titik pemeriksaan pada atau sebelum awalan yang dieksport, bukan titik pemeriksaan sewenang-wenang yang kemudian.

## Persiapan RFC 3161 dan pengesahan respons (0.2)

Mod bukti (dimatikan secara lalai) hanya menghantar SHA-256 setiap checkpoint yang ditandatangani kepada pihak berkuasa RFC 3161 yang disenaraikan dan kalendar OpenTimestamps, melalui laluan ruang kerja dan tidak pernah melalui MTProxy. Jawapan disimpan dalam `checkpoints/anchors/`, dieksport, dan diperiksa oleh `verify.py` (`--tsa-ca` memeriksa tandatangan TSA; mengesahkan bukti OpenTimestamps dengan `ots upgrade` dan `ots verify`).

Panel menyediakan arkib permintaan yang mengandungi bait checkpoint.json kanonik, cap pesan SHA-256 dan nonse rawak dalam timestamp.tsq, checksum, dan arahan. Tiada permintaan rangkaian dibuat. Persediaan bukan cap masa dipercayai.

`python -m tgwitness.anchor verify` memanggil OpenSSL ts dua kali: sekali terhadap bait checkpoint dan sekali terhadap permintaan asal. Fail CA yang dipercayai diperlukan secara eksplisit; sijil yang disertakan tidak dipercayai secara automatik. Semakan permintaan adalah pilihan di CLI, jadi simpan dan gunakan --request untuk menyemak nonce. Keputusan menyatakan sama ada ia telah disemak. Tandatangan dan jurnal titik pemeriksaan pengumpul masih perlu disahkan secara berasingan dengan cap jari pengumpul yang dipercayai.

Pemverifikasi semasa tidak mengambil maklumat penarikan balik atau melaksanakan pengesahan arkib jangka panjang selepas tamat tempoh sijil. Jangan samakan pengesahan tandatangan yang berjaya dengan cap masa bertauliah atau kebolehterimaan undang-undang. TSA bebas sebenar belum dihubungi semasa pembangunan. Lihat [prosedur](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/).
