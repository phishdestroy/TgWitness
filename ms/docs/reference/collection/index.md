# Bagaimana pengumpulan berfungsi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/

Skop pemerhatian, kemas kini langsung, semakan semula, lampiran, tindakan sendiri dan maksud jurang, rekod demi rekod.

TgWitness merekod apa yang diperhatikan oleh akaun Telegram yang disambungkan. Jurnal ini memelihara pemerhatian tersebut, urutannya, dan konteks yang disertakan. Ia tidak membuat inferens tentang tindakan yang tidak dilihat daripada mesej yang hilang atau daripada akaun yang disambungkan.

## Dari log masuk ke jurnal

Diyagram aliran · Memberi kebenaran kepada akaun pengguna → Pilih kumpulan dan saluran yang boleh diakses; Pilih kumpulan dan saluran yang boleh diakses → Simpan tetapan acara dan lampiran; Simpan tetapan acara dan lampiran → Mulakan pemerhatian; Mulakan pemerhatian → Terima kemas kini daripada klien aktif; Terima kemas kini daripada klien aktif → Terapkan dasar sumber dan peristiwa; Terapkan dasar sumber dan peristiwa → Lampirkan pemerhatian yang disahkan; Lampirkan pemerhatian yang disahkan → Semak atau eksport jurnal; Lampirkan pemerhatian yang disahkan → Proses sebarang lampiran yang beratur; Proses sebarang lampiran yang beratur → Lampirkan hasil muat turun · Memberi kebenarankepada akaun pengguna · Pilih kumpulan dansaluran yang bolehdiakses · Simpan tetapan acaradan lampiran · Mulakan pemerhatian · Terima kemas kinidaripada klien aktif · Terapkan dasar sumberdan peristiwa · Lampirkan pemerhatianyang disahkan · Semak atau eksportjurnal · Proses sebaranglampiran yang beratur · Lampirkan hasil muatturun

**Diagram sebagai teks**

1. Memberi kebenaran kepada akaun pengguna → Pilih kumpulan dan saluran yang boleh diakses
2. Pilih kumpulan dan saluran yang boleh diakses → Simpan tetapan acara dan lampiran
3. Simpan tetapan acara dan lampiran → Mulakan pemerhatian
4. Mulakan pemerhatian → Terima kemas kini daripada klien aktif
5. Terima kemas kini daripada klien aktif → Terapkan dasar sumber dan peristiwa
6. Terapkan dasar sumber dan peristiwa → Lampirkan pemerhatian yang disahkan
7. Lampirkan pemerhatian yang disahkan → Semak atau eksport jurnal
8. Lampirkan pemerhatian yang disahkan → Proses sebarang lampiran yang beratur
9. Proses sebarang lampiran yang beratur → Lampirkan hasil muat turun

Pengesahan, akses kepada sumber, pengumpul yang sedang berjalan, dan penghantaran lengkap adalah persoalan yang berbeza. Log masuk yang berjaya tidak memberi akses kepada setiap kumpulan. Pengangkutan yang bersambung tidak menjamin bahawa setiap kemas kini berkaitan telah tiba.

## Skop pemerhatian: sembang terpilih, satu folder atau keseluruhan akaun

Sumber → **Skop pemerhatian** menentukan sembang mana yang direkodkan oleh ruang kerja.

| Mod | Merekod | Sembang baharu |
| --- | --- | --- |
| Perbualan terpilih (laluan lalai) | Hanya sembang yang anda tambah secara manual | Tidak pernah ditambah secara automatik |
| folder Telegram | Perbualan dalam salah satu folder akaun: perbualan yang disertakan mengikut nama, ditambah kategori folder (kenalan, bukan kenalan, kumpulan, saluran, bot), tolak perbualan yang dikecualikan dan, jika folder menyatakannya, perbualan yang diarkibkan | Perbualan yang sepadan ditambah sebaik sahaja ia menjadi aktif; perbualan yang anda tambahkan ke dalam folder di Telegram akan dikesan dalam masa sejam |
| Keseluruhan akaun | Setiap sembang yang dilihat oleh akaun | Setiap sembang baru, kumpulan, sembang peribadi atau bot ditambah sebaik sahaja kemas kini pertamanya tiba |

- **Jenis sumber** (saluran, kumpulan, sembang peribadi, bot) mengehadkan folder dan mod akaun keseluruhan. Sembang terpilih boleh sebarang jenis, termasuk sembang peribadi dan bot.
- **Perbualan yang dikecualikan** tidak pernah dirakam, dalam apa jua mod. Dalam mod folder dan akaun keseluruhan, *Mengecualikan* dan *Mengalihkan* pada sumber meletakkannya dalam senarai ini, supaya skop tidak menambahkannya semula. Memilih semula sembang secara manual (dalam Sumber atau dari Sembang) akan mengeluarkan sembang tersebut daripada senarai. Senarai boleh memuat sehingga 5,000 sembang; melebihi had itu, *permintaan Mengalihkan* akan ditolak dan sembang tersebut boleh ditangguhkan sebaliknya.
- **Tindakan sendiri** (diaktifkan secara lalai): mesej yang dihantar oleh akaun ini, suntingannya dan tekanan butang papan kekunci balasan. Apabila dimatikan, mesej keluar dan suntingan akan diabaikan.
- Menukar ke folder atau keseluruhan akaun memerlukan pengesahan: mod-mod ini merekodkan sembang peribadi dan mesej pihak ketiga dan hanya sesuai untuk akaun khusus. Pengesahan dan setiap perubahan skop ditandatangani sebagai rekod `scope.changed`.
- Perbualan yang ditambah oleh skop muncul sebagai sumber yang ditandakan *auto*, direkodkan sebagai `scope.applied` (pada permulaan dan setiap jam) atau `source.discovered` (perbualan baru semasa memerhati). Beralih kembali ke perbualan yang dipilih akan menghentikan semua sumber yang ditambah secara automatik.

Apa yang mod-mod ini tidak dapat lakukan:

- **Perbualan rahsia** disulitkan hujung ke hujung antara dua peranti dan tidak pernah sampai ke TgWitness, dalam apa jua mod.
- **Tiada apa yang dirakam selagi TgWitness tidak berjalan.** Selepas dihidupkan semula, ia meminta kemas kini yang terlepas daripada Telegram dan menyemak semula sembang, tetapi Telegram tidak memulangkan semuanya selepas gangguan panjang. Laporan dan `verify.py` menunjukkan tempoh sedemikian sebagai jurang (lihat [liputan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Hanya 1,000 dialog pertama disenaraikan pada permulaan (hadnya berada di bawah **Parameter**); sembang yang lebih lama akan ditambah apabila ia menjadi aktif semula. Sejarah awal sembang yang ditambah tidak dimuat — ambil tangkapan sejarah atau eksport sembang penuh apabila diperlukan.
- Kondisi folder yang berubah-ubah (dibisukan, dibaca) tidak diterapkan: sembang seperti ini tetap dipantau.
- **Butang bot inline (callback)** yang ditekan dalam aplikasi lain tidak kelihatan kepada sesi kedua; balasan atau suntingan bot direkodkan. Tekanan kekunci papan kekunci balasan tiba sebagai mesej keluar dan dilabelkan `button_press`.
- Lebih banyak sembang bermakna lebih banyak permintaan. Telegram mengehadkan akaun untuk jumlah yang dianggap berlebihan, yang merupakan satu lagi sebab untuk menggunakan akaun khusus.

## Skop dan pemilihan acara

Setiap ruang kerja mempunyai sumbernya sendiri. TgWitness tidak menyertai kumpulan, menerima jemputan, atau menyenaraikan setiap ahli secara automatik. Sumber mesti sudah boleh diakses oleh akaun. Semasa permulaan, pengumpul menyemak sumber terpilih dengan dialog yang boleh dilihat oleh akaun; 1,000 dialog pertama akan diperiksa melainkan **Parameter → Perbualan yang dibaca daripada senarai akaun** menyatakan sebaliknya. Sumber yang tiada akan ditandakan **sebagai akses belum disahkan**, bukan dianggap telah menyingkirkan anda.

| Persetelan | Mengumpul | Kesan apabila dilumpuhkan |
| --- | --- | --- |
| Mesej baru | Mesej biasa yang dihantar | Suntingan/pembuangan kemudian mungkin tidak mempunyai teks yang dirakam sebelum ini untuk dibandingkan. |
| Suntingan | Menyampaikan versi mesej yang telah disunting | Perubahan pertengahan tidak direkonstruksi kemudian. |
| Pembuangan | Notis pemadaman berskop dan notis peringkat akaun tanpa skop | Notis pemadaman tidak dimasukkan ke dalam jurnal. |
| Reaksi | Siaran tangkapan reaksi | Kemas kini reaksi berasingan tidak ditambah. |
| Keahlian | Mesej perkhidmatan keahlian dan kemas kini peserta disampaikan | Perhatian keahlian tersebut tidak ditambah. |

Tetapan terpakai kepada semua sumber yang dipilih dalam ruang kerja. Simpan borang untuk menerapkan perubahan; perubahan direkodkan dengan nilai sebelum/selepas yang disahkan. Mematikan sesuatu kategori tidak akan memadam rekod terdahulu. Mengaktifkannya semula tidak akan mengisi semula kemas kini yang terlepas.

Rekod operasi dan acara perkhidmatan kumpulan lain kekal berasingan daripada suis ini. Mesej perkhidmatan keahlian boleh mencipta rekod mesej apabila keahlian diaktifkan walaupun tangkapan mesej biasa dimatikan. Objek Telegram yang dirakam mengekalkan metadata terbenam; suis bukan peraturan redaksi.

**Pembuangan dalam sembang peribadi dan kumpulan biasa** muncul sebagai ID mesej tanpa sembang. Sembang-sembang ini berkongsi satu urutan ID mesej untuk seluruh akaun, jadi apabila mesej dengan ID itu disimpan lebih awal, sembangnya diketahui: pembuangan itu direkodkan dalam sembang itu dengan `chat_resolution` menerangkan bagaimana. ID yang tidak pernah disimpan kekal sebagai **pemadaman tanpa skop** dengan sumber yang secara eksplisit tidak diketahui; pengumpul tidak meneka. Telegram tidak pernah menyatakan siapa yang memadam mesej; apabila mesej yang dipadam dihantar oleh akaun ini, rekodnya menyatakan demikian (`deleted_message_was_outgoing`) tanpa menamakan pihak yang memadam.

## Tindakan sendiri

Mesej yang dihantar oleh akaun yang diperhatikan dilabelkan `outgoing`. Suntingan pada mesej keluar mencatat bahawa dalam sembang peribadi dan kumpulan hanya penulisnya boleh menyuntingnya, manakala pos saluran boleh disunting oleh pentadbir lain. Apabila mesej keluar mengulangi teks butang daripada papan kekunci balasan tersimpan terbaru dalam sembang itu, ia membawa `button_press` dengan pautan ke rekod papan kekunci tersebut.

Pengecualian tindakan sendiri juga terpakai pada semakan semula latar belakang dan sejarah sembang baru secara automatik. Mesej keluar yang dilangkau akan memajukan kedudukan semakan semula supaya ia tidak dapat menyekat mesej masuk kemudian. Tindakan panel yang jelas dan potret sejarah yang diminta secara manual kekal direkodkan.

## Mod siasatan: menyertai pasukan dan bercakap dengan bot

**Sumber → Skop pemerhatian → Mod siasatan** menyediakan skop untuk akaun khusus yang menyertai sembang pasukan, memulakan bot dan menulis kepada mereka: keseluruhan akaun, setiap jenis sumber, tindakan sendiri, dan untuk setiap sembang atau bot yang muncul, profilnya dan 200 mesej terbarunya yang boleh dilihat. Semak borang dan tekan **Simpan skop**; suis ke seluruh akaun meminta pengesahan biasa.

- **Butang.** Butang di bawah mesej disimpan bersamanya dan dipaparkan dalam **Perbualan**: pautan, aplikasi web, pautan log masuk, teks untuk disalin, data callback, pertanyaan dalam talian, permintaan nombor telefon atau lokasi. Pautan dipaparkan sebagai teks dan tidak pernah dibuka oleh panel. Apabila bot menukar hanya butang (contohnya pautan pembayaran baru), itu adalah versi baru mesej tersebut, sama ada daripada kemas kini langsung atau semakan semula.
- **Sembang dan bot baru.** Dalam mod folder dan akaun keseluruhan, **apabila sembang atau bot baru muncul**, disimpan, sejurus selepas ia muncul:

  - profilnya sebagai rekod `source.profile`: bot description and commands, teks tentang pengguna, kumpulan atau saluran, ahli, chat yang dipautkan dan pautan jemputan apabila Telegram memulangkan satu;
  - mesej terkini yang kelihatan (sehingga 1,000) sebagai potret sejarah yang ditandakan `new_chat`: mesej-mesej awal dalam sembang pasukan yang baru disertai, atau apa yang dikatakan oleh bot sebelum pemerhatian menyedari sembang itu. Mesej yang telah disimpan secara langsung tidak diulang.

  Perbualan yang sudah ada dalam senarai apabila mod diaktifkan akan ditambah tanpa imej skrin. FloodWait akan menangguhkan kerja ini dan ia akan disambung semula selepas itu; kegagalan direkodkan dan rakaman langsung perbualan diteruskan. - **Profil atas permintaan. Perbualan → Profil → Simpan profil kini** menyimpan profil semasa mana-mana sumber; yang terbaru dipaparkan di atas mesej. - **Tidak kelihatan.** Butang dalam talian (callback) yang ditekan di aplikasi Telegram lain, pop timbul atau pautan yang dijawab oleh bot, dan pautan jemputan yang digunakan di aplikasi lain tidak sampai ke TgWitness. Apa yang dihantar atau disunting oleh bot selepas itu akan direkodkan.

### Tindakan daripada panel

**Perbualan** kini merangkumi klien mini yang menggunakan akaun Telegram ruang kerja yang dipilih:

- Tulis mesej teks biasa atau pilih **Balas** di bawah mesej yang disimpan. Mesej keluar yang dihantar akan direkodkan walaupun skop mengecualikan kemas kini keluar.
- Tekan**butang** di bawah callback semasa atau butang teks. Pelayan memuat semula mesej itu dan menolak tindakan jika papan kekunci berbeza daripada versi yang disimpan. Resit callback mengekalkan teks pop timbul Telegram, bendera amaran dan URL; jawapan juga dipaparkan di bawah perbualan. URL kekal sebagai teks yang boleh dipilih dan tidak dibuka secara automatik.
- Perluas **pautan Telegram Terbuka**, masukkan `@username`, pautan `https://t.me/name` awam, `https://t.me/+invite` / `joinchat/invite`, atau pautan bot dengan `?start=parameter`, dan tekan **Simpan pratonton**. Pautan asal dan pratonton Telegram ditandatangani sebelum menyertai. **Sertailah / buka dan perhatikan** kemudian menyertai kumpulan/saluran atau membuka pengguna/bot, menambah sembang itu sebagai sumber yang diaktifkan, dan menghantar `/start` kepada bot, termasuk parameter permulaannya. Permintaan penyertaan yang menunggu kelulusan pentadbir direkodkan sebagai tertangguh, bukan sebagai keahlian.

Dayakan **Mula Pengamatan** untuk merakam balasan yang diterima secara langsung. Tindakan panel berfungsi semasa pengamatan dihentikan seketika, tetapi hanya tindak balas langsung mereka yang dijamin akan disimpan. Sumber yang baru ditambah menggunakan pengambilan profil/sejarah yang dikonfigurasikan apabila pengamatan sedang dijalankan. Apabila sesuatu sumber dihentikan seketika, aktifkan ia dalam **Sumber** sebelum menghantar atau menekan butangnya.

`interaction.preview`, `interaction.requested` dan `interaction.result` adalah acara jurnal berasingan biasa yang disertakan dalam eksport bukti. Permintaan mengenal pasti akaun, mesej/butang atau rekod pratonton dan sama ada pemerhatian sedang dijalankan. Resit membezakan antara kejayaan, penolakan, kelulusan menunggu dan keputusan yang tidak diketahui. Permintaan yang terganggu mungkin telah sampai ke Telegram: semak sembang sebelum memulakan tindakan baru. Menggunakan semula ID permintaan akan memulihkan resit yang disimpannya tanpa mengulangi tindakan, termasuk selepas memulakan semula. Panel mengekalkan ID itu selepas respons yang samar untuk tindakan yang sama semasa sesi halaman semasa. Ia juga mengekalkan ID tersebut apabila menyegarkan paparan gagal selepas tindakan yang berjaya: resit kekal kelihatan, dan mengklik sekali lagi akan memulihkannya. Callback dan RPC sertai mempunyai satu percubaan aplikasi; bacaan yang boleh dicuba semula mengekalkan dasar percubaan semula yang dikonfigurasikan. Menukar sembang segera membersihkan draf dan sasaran balasan dan menyekat penghantaran sehingga perbualan baru dimuat.

Mini-klien ini mengendalikan butang teks dan callback. Aplikasi web, permintaan log masuk/telefon/lokasi, pembayaran, pertanyaan dalam talian dan lampiran masih memerlukan klien Telegram; metadata butang yang disimpan kekal dapat dilihat. Kawalan baru menggunakan teks Bahasa Inggeris.

## Semak semula peringkat

Semakan semula meminta semula Telegram untuk mesej yang terlepas, suntingan dan mesej yang tidak lagi dipaparkan. Sumber yang ditandakan dengan bintang adalah sumber **keutamaan**, disemak semula setiap 15 minit secara lalai; semua sumber lain setiap 6 jam. Perbualan yang dipilih bermula sebagai sumber keutamaan, manakala perbualan yang ditambah melalui folder atau keseluruhan akaun dikira sebagai perbualan biasa. Sebanyak 30 sumber paling banyak akan diperiksa semula setiap pusingan dan baki akan menunggu sehingga minit seterusnya; selepas disambungkan semula, sumber keutamaan akan diutamakan. Kedua-dua selang masa ditetapkan di bawah Sumber → Tetapan Rakaman → Semak Semula (0 mematikan peringkat) dan direkodkan sebagai `recheck.changed`.

Mesej yang terlepas diambil semula dari tempat kitaran sebelumnya berhenti, paling banyak **Mesej baharu setiap semakan semula** (1,000 secara lalai) setiap kitaran. Selepas hentian panjang, semakan semula oleh itu akan mengisi keseluruhan jurang, walaupun mesej langsung yang lebih baru daripada jurang telah disimpan terlebih dahulu. Sembang yang masih mengejar ketinggalan akan disemak semula pada minit berikutnya, bukannya menunggu selang lapisan; `recheck.completed` memaparkan `continues_after` sehingga ia selesai.

Perbandingan merangkumi teks mesej, entiti, papan kekunci (termasuk penyingkiran), dan kandungan/identiti lampiran. Mengubah suai hash capaian fail atau rujukan fail sahaja tidak mencipta suntingan, begitu juga apa yang diisi secara automatik oleh Telegram: pratonton pautan yang dimuat, paparan cerita, media berbayar yang dibuka oleh akaun ini, resit invois. Setiap versi yang disimpan dalam Chats memautkan kepada rekod jurnal penuh, termasuk metadata media.

## Sejarah mesej dan atribusi

Andai pengumpul memerhati "Mesyuarat pada pukul 10:00," kemudian melihat "Mesyuarat pada pukul 11:00," dan seterusnya menerima notis pemadaman. Ia menyelitkan tiga pemerhatian berbeza. Teks asal kekal, suntingan adalah versi berasingan, dan notis merekodkan bahawa pemadaman telah diperhatikan.

Jika pengumpulan bermula selepas versi pertama hilang, teks tersebut tidak tersedia. Jika beberapa suntingan berlaku semasa proses tidak dalam talian, hanya versi yang diperhatikan kemudian boleh disimpan. Notis pemadaman tidak dapat memulihkan kandungan yang tidak pernah dirakam.

Pengirim mesej tidak secara automatik menjadi penyunting. Telegram biasanya tidak menyediakan maklumat tentang individu yang memadam mesej atau masa pemadaman yang tepat. Pelaku yang tidak diketahui tetap tidak diketahui. Snapshot reaksi dan kemas kini peserta hanya mengandungi bilangan dan identiti yang Telegram paparkan kepada akaun tersebut.

Nombor urutan menyatakan susunan pemerhatian. Cap masa UTC pengumpul adalah jam tempatan; cap masa sumber Telegram disimpan secara berasingan apabila disediakan. Tiada satu pun yang merupakan cap masa dipercayai yang bebas.

## Snapshot sejarah

Satu snapshot meminta mesej terkini yang boleh dilihat daripada sumber yang diaktifkan, sehingga 500 setiap permintaan. Keputusan dilabel sebagai pemerhatian sejarah. Ia boleh tumpang tindih dengan tangkapan langsung, dan pemerhatian berulang disimpan sebagai rekod berasingan.

Snapshot mematuhi dasar lampiran tetapi kekal berasingan daripada suis acara langsung. Ia tidak membina semula mesej yang telah dipadam atau versi perantaraan yang terlepas. Anda boleh meminta satu semasa berehat; sebarang lampiran yang ia susun menunggu sehingga pemerhatian bermula dan pekerja muat turun berjalan.

## Pengendalian lampiran

Muat turun lampiran diaktifkan secara lalai dan akan terhenti apabila ruang cakera bebas turun di bawah 1 GiB. Pengumpul melaksanakan pemerhatian mesej dan kerja muat turun serentak. Kerja tersebut mengekalkan penderia media asal dan dasar saiz, jadi lampiran yang disunting kemudian tidak akan digantikan secara senyap.

Muat turun dijalankan selepas tangkapan mesej. Muat turun yang lengkap mencipta rekod `media.saved` dengan SHA-256 dan kiraan baitnya. Kerja yang dilangkau, gagal, dicuba semula, dan terganggu mempunyai hasil yang berasingan. Tugas yang dibariskan bukan bukti bahawa fail itu telah dipelihara. Fail yang lengkap juga mesti sepadan dengan kiraan bait dalam penderia lampiran asal yang diperhatikan. Tindak balas yang pendek atau panjang secara tidak dijangka tidak direkodkan sebagai media yang dipelihara.

Had ditetapkan **mengikut jenis**: foto, video, GIF dan animasi, mesej video bulat, mesej suara, muzik dan audio, pelekat, dan fail. Setiap jenis boleh dimatikan dan mempunyai had saiz tersendiri dari 1 hingga 2,000 MiB; ruang kerja baru bermula dengan 20 MiB untuk foto, 100 MiB untuk video, 50 MiB untuk fail, audio dan video bulat, 20 MiB untuk mesej suara dan GIF dan 5 MiB untuk pelekat. *Saiz fail maksimum* menetapkan setiap jenis sekaligus. Dasar yang disimpan sebelum had bagi setiap jenis mengekalkan had tunggal mereka untuk setiap jenis. Jenis yang dilumpuhkan menghasilkan rekod `media.skipped`; fail bersaiz tidak diketahui atau terlalu besar tidak akan dimuat turun. Fail besar mendapat masa muat turun sekurang-kurangnya 256 KiB/s. Tugas bertahan selepas mula semula, tetapi rujukan yang tamat tempoh, kehilangan capaian, atau fail yang dipadam masih boleh menghalang pemulihan. Tugas sedia ada mengekalkan dasar yang disimpan bersamanya.

## Pause, kunci, putuskan sambungan, dan mulakan semula

| Tindakan atau keadaan | Kesan |
| --- | --- |
| Tukar ruang kerja | Menukar paparan panel; pengumpul lain mengekalkan keadaan mereka. |
| Kunci panel atau tutup tab | Membiarkan pelayan dan pemantauan terus berjalan. |
| Jeda pemerhatian | Menghentikan pengumpul tersebut dan memelihara kerja lampiran yang sedang menunggu. |
| Lumpuhkan sumber | Menghentikan tangkapan skop masa depan; kerja media yang beratur untuknya menunggu sementara ia dilumpuhkan. |
| Hapus sumber | Melupakannya sebagai sumber dan memadam profil orangnya; rekod yang telah disimpan kekal dalam jurnal hanya-tambah. Lampirannya yang masih menunggu direkod sebagai gagal (`source_removed`). Dalam mod folder dan akaun keseluruhan, ia juga dikecualikan. |
| Ubah laluan sambungan | Memerlukan jeda, menutup klien lama, dan membatalkan log masuk yang belum selesai. |
| Hentikan proses Python | Menhentikan semua ruang kerja; tiada pemerhatian dibuat semasa ia tidak dalam talian. |
| Mulakan semula selepas pemerhatian aktif | Cubaan untuk menyambung semula skop yang disimpan menggunakan sesi yang disimpan. Paus manual membatalkan niat tersebut. |

Pengumpul merekodkan putusnya sambungan yang dikesan, percubaan semula, ralat, permulaan/pemberhentian, dan denyutan jantung. Gangguan pendek mungkin terlepas oleh pemeriksaan sambungan berkala. Selepas dihidupkan semula, kemas kini yang terlepas akan diminta daripada kedudukan kemas kini yang disimpan dan sembang yang diperhatikan akan disemak semula secara berkala; lihat [format bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#durable-collection-and-process-receipts-02). Snekapskrin menyediakan konteks; ia tidak membuktikan bahawa jurang telah diperbaiki.

## Pengasingan dan pengesahan akaun

Setiap ruang kerja mempunyai jurnal, kebenaran, kunci penandatangan, dasar, dan barisan tunggu tersendiri. Hanya klien aktifnya boleh menyumbang pemerhatian secara langsung. Klien yang ditolak, menunggu, digantikan, dan ujian sambungan tidak dapat menulis kemas kini langsung ke dalam jurnalnya. Akaun yang berbeza boleh memerhati kumpulan yang sama, tetapi jurnal mereka kekal berasingan.

Setiap peristiwa merangkumi hash sebelumnya dan tandatangan Ed25519. Eksport merangkumi keseluruhan jurnal ruang kerja melalui nombor urutan tetap. Penapis panel tidak menapis eksport; pengumpulan mungkin diteruskan melebihi sempadannya semasa ia sedang disediakan.

**Semak jurnal** memeriksa rantaian peristiwa dan tandatangan melalui sempadan yang dipaparkan. Keputusannya dipadamkan apabila ruang kerja berubah, dan panel mengenal pasti rekod baharu yang ditambah selepas pemeriksaan. Eksport ZIP juga mengesahkan media yang dikumpul.

Tandatangan sah menetapkan integriti berbanding kunci yang dipercayai, bukan asal Telegram atau kandungan yang benar. Simpan cap jari dan titik pemeriksaan secara berasingan. Lihat [model bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/), [operasi harian](https://phishdestroy.github.io/TgWitness/ms/docs/reference/operations/), dan [prosedur penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk keperluan kepercayaan dan penghantaran.
