# Panduan panel

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/

Setiap skrin panel: sembang, jurnal, sumber, eksport, Ekstra, mod perlindungan dan pemeriksaan kod.

[Pendaftaran awal dan tetapan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/settings/) · [Akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/) · [Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/) · [Laporan kes](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/)

Apa fungsi setiap skrin, apa yang ditulisnya ke jurnal yang disahkan dan di mana panduan terperinci berada. Panel memaparkan satu ruang kerja pada satu masa: satu akaun Telegram dengan sumber, jurnal dan kunci tandatangan tersendiri. Pemilih di bahagian atas bar sisi menukar ruang kerja. Alamat membawa ruang kerja (`?ws=…`); selagi alamat, pemilih dan akaun yang dimuat tidak sehaluan, tindakan kekal dihalang.

## Temui jalan anda

Bahagian harian terletak di bahagian atas bar sisi, **Akaun** berada di bawah **Ruang Kerja** , dan segala-galanya yang lain berada di bawah **Alat & Tetapan Lain** . Suis **aras Antara Muka** di bar atas menentukan berapa banyak bahagian yang dipaparkan:

| Tahap | Bahagian dalam bar sisi |
| --- | --- |
| Mudah | Home, Chats, Changes, Archives dan Settings |
| Standard | Juga Case Board, Akaun dan Akses |
| Pakar | Juga Sumber, Ekstra, Tanya arkib, Parameter, Akaun, Log Sistem dan Integrasi |

Panggilan mudah Mulai di sini, Jurnal dan Eksport **Utama**, **Perubahan** dan **Arkib**. Satu tahap hanya menyembunyikan bahagian. Ciri tersembunyi terus berfungsi, dan pelayan menyemak setiap kebenaran secara sendiri. Tahap, bahasa, tema dan zon waktu disimpan bagi setiap pengendali dan ruang kerja; lihat [tetapan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/settings/).

Bar atas juga mempunyai:

- **Pergi ke seksyen** (Ctrl+K, atau ⌘K pada Mac): cari sembang, parameter atau rekod jurnal oleh `#number`. Anak panah untuk bergerak, Enter untuk membuka, Esc untuk menutup.
- **Pemberitahuan**: masalah dan perubahan sembang yang diselesaikan daripada jurnal. **Tanda semua sebagai dibaca** akan membersihkan pengira dan membuka Peraturan **Pemberitahuan**. Penghantaran ke Telegram, Discord atau e-mel disediakan di [Tambahan → Pemberitahuan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#notifications).
- Penunjuk sambungan untuk ruang kerja ini. **Kesihatan pengumpul** di bawah bar atas membahagikannya kepada sambungan Telegram, kemasukan acara, sumber dan barisan lampiran.
- **Kunci**: menutup panel dalam pelayar ini. Koleksi terus berjalan pada pelayan.
- Mod perlindungan di sebelah nombor versi; lihat [mod perlindungan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#protection-modes).

Ruang kerja demo mengandungi mesej rekaan dan tidak pernah disambungkan ke Telegram. Tindakan yang boleh mengubah ruang kerja sebenar akan ditolak di sana.

## Mulakan di sini

Pilih tugasan. **Eksport akaun saya** memuat turun apa yang boleh dibaca oleh akaun sekarang. **Ikuti siasatan** merekod mesej baru, suntingan yang diperhatikan dan notis pemadaman daripada sembang yang anda pilih. Kad tetapan memaparkan tiga langkah: sambungkan akaun, pilih sumber, mulakan pemerhatian. Soalan matlamat kekal di halaman ini sehingga anda menjawab atau melangkauinya. Ruang kerja baru membuka [tetapan pertama](https://phishdestroy.github.io/TgWitness/ms/docs/reference/settings/) sebaliknya.

## Perbualan

Perbualan yang disimpan, secara lalai hanya untuk dibaca.

- Cari senarai mengikut nama atau ID. **Pilih** untuk menambah atau mengeluarkan sembang yang dipantau. **Pautan Telegram terbuka** mengambil nama pengguna atau pautan jemputan dan menyimpan pratonton ke jurnal. **Sertai / buka dan perhatikan** kemudian menyertai sembang dan menambahkannya ke sumber anda; membuka bot menghantarnya `/start`.
- Header sembang mengira mesej **yang dipadam, teks yang disimpan**, **mesej yang dipadam sebelum disimpan** dan mesej **yang tidak ditemui semasa semakan semula**. Senarai sembang dan pemberitahuan menggunakan definisi yang sama. Mesej yang dipadam berwarna merah dan mengekalkan teks yang disimpannya; mesej yang disunting mengekalkan setiap versi yang disimpan. Setiap pemadaman menyatakan apa yang diketahui: bila ia dilihat, bahawa Telegram tidak melaporkan siapa yang memadamnya, atau bahawa hanya notis yang diterima.
- **Muat sejarah** membawa 100, 250 atau 500 mesej terakhir ke dalam paparan ini dan jurnal. Untuk memuat semua sumber yang diaktifkan, gunakan [Sumber → Sejarah penuh](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#sources).
- **Eksport sembang** memuat turun keseluruhan sejarah yang boleh dilihat sebagai yang disahkan `chat.json` dan `chat.html`Beberapa akaun yang disambungkan boleh berkongsi kerja: setiap satu memuat turun julat nombor mesejnya sendiri dan menandatangani bahagiannya, dan akaun yang memulakan eksport menandatangani arkib tersebut. Lihat [eksport satu sembang](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- Senarai **Orang** memaparkan semua orang yang mempunyai mesej disimpan dalam sembang ini. Profil Orang dilumpuhkan secara lalai kerana ia adalah data peribadi mengenai pihak ketiga. Apabila diaktifkan untuk sembang, profil akan memaparkan sejarah nama dan nama pengguna, bendera Telegram, has rat avatar, aktiviti, siapa yang membalas kepada siapa, sembang lain yang diperhatikan, serta dompet, telefon, nama pengguna dan pautan yang disebut. Setiap fakta menunjuk kepada rekodnya. **Eksport profil** menyimpan fail yang disahkan, secara pilihan dalam kata laluan ZIP; mematikan profil akan memadam fail profil. Lihat [profil orang](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#people-profiles).
- **Simpan profil kini** merekodkan tangkapan profil sembang atau bot: deskripsi, ahli, pautan jemputan, arahan bot.

### Hanya baca, penghantaran dan rahsia

Dua suis di atas mesej melindungi akaun dan pembaca:

- **Hanya baca** dihidupkan apabila sembang dibuka. Matikan ia untuk menghantar mesej atau menekan butang bot. Setiap tindakan bertanya pada **Hantar sebagai @account?** atau **Tekan butang bot ini sebagai @account?**, memberitahu anda bahawa ahli sembang melihatnya dan ia dimasukkan ke dalam jurnal yang ditandatangani. **Jangan tanya lagi selama 10 minit dalam sembang ini** melangkau soalan itu untuk seketika. Penghantaran dimatikan untuk matlamat **Bukti untuk satu kes**, dalam panel dan dalam API.
- **Rahsia topeng** menyembunyikan apa yang kelihatan seperti kata laluan, kod log masuk, kunci API atau hash, token bot, rentetan sesi, kunci peribadi, JWT atau nombor kad pembayaran (nombor kad disemak dengan jumlah Luhn). **Tunjukkan** mendedahkan satu nilai; pendedahan itu direkodkan dalam jurnal. Menutup topeng untuk pelayar ini juga direkodkan. Hanya paparan yang berubah: rekod asal dan setiap eksport mengekalkan teks penuh.

## Jurnal

Setiap rekod yang telah ditandatangani oleh ruang kerja, terbarunya dahulu.

- **Ringkasan** mengira mesej yang diperhatikan, suntingan yang direkodkan, notis pemadaman dan sumber yang dipilih.
- **Garis masa acara** menapis mengikut jenis peristiwa (semua, suntingan, pemadaman, reaksi, keahlian, liputan), mengikut teks dan sumber. **Muat acara terdahulu** kembali ke halaman sebelumnya.
- Buka rekod untuk melihat butirannya, hash dan payload. **Pautan ke rekod ini** ialah alamat yang membuka rekod yang sama. Rahsia yang mungkin disembunyikan dalam pratonton ini; eksport mengekalkan versi asal.
- Jurnal bersifat hanya tambah: tiada apa-apa dalam panel yang menyunting atau memadam rekod. Semak ia dengan **Eksport → Sahkan jurnal** atau `python -m tgwitness.verify`; lihat [eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/).

## Sumber

Perbualan mana yang dirakam oleh ruang kerja ini, dan apa yang disimpannya daripada perbualan tersebut. Perubahan terpakai pada aktiviti akan datang; rekod yang disimpan kekal.

**Refresh senarai sembang** membaca sembang dan folder akaun. Ia tidak memuat turun mesej.

### Skop

- **Apa yang direkodkan oleh akaun ini** : **Perbualan terpilih** (hanya sembang yang anda tambahkan), **folder Telegram** (salah satu folder akaun, termasuk sembang yang ditambah kemudian) atau **Akaun keseluruhan** (setiap sembang, dan setiap sembang baru, kumpulan, sembang peribadi atau bot sebaik ia muncul). **Mod siasatan** adalah untuk akaun khusus: ia merekodkan segala yang dilihat oleh akaun itu, mesejnya sendiri dan butang yang ditekan, serta menyimpan profil setiap sembang baru dan mesej yang kelihatan sebelum ini dengan segera. [panduan akaun khusus](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) menerangkan mengapa anda tidak seharusnya menggunakan akaun utama anda.
- **Jenis sumber** mengehadkan mod folder dan akaun keseluruhan kepada saluran, kumpulan, sembang peribadi dan bot. **Tindakan sendiri** menambah mesej, suntingan dan ketikan papan kekunci balasan milik akaun tersebut.
- **Apabila sembang atau bot baru muncul**: simpan profilnya dan sehingga bilangan yang dipilih daripada mesej terbarunya yang boleh dilihat.

Had: sembang rahsia tidak pernah sampai ke TgWitness. Tiada apa yang direkodkan semasa TgWitness tidak berjalan; selepas dihidupkan semula ia hanya mengemas kini apa yang masih dikembalikan oleh Telegram, dan laporan menunjukkan jurangnya. Sembang melebihi had senarai sembang (1,000 dialog melainkan diubah dalam Parameter) akan ditambah apabila ia aktif semula. Butang bot dalam talian yang ditekan di aplikasi lain tidak kelihatan; balasan bot direkodkan.

### Perbualan yang termasuk dalam skop

Tapis mengikut status (**Diaktifkan**, **Digantung**, **Keutamaan**, **Dikecualikan**, **Akses belum disahkan**, **Diabaikan**) dan jenis, kemudian ambil tindakan ke atas pilihan: aktifkan, hentikan, tandakan atau buang keutamaan, kecualikan daripada skop atau buang. Lencana status hanya menunjukkan keadaan; tindakan terdapat dalam menu setiap baris dengan keterangan tentang fungsinya. Menangguhkan dan mengecualikan memerlukan pengesahan, juga secara pukal. Mengalih keluar sumber memerlukan nama sumber tersebut dan memadamkan profil orangnya; rekod simpanannya kekal dalam jurnal.

Sumber yang tidak dipaparkan dalam senarai sembang akaun sedang **menerima kemas kini, tidak dalam senarai sembang** sementara rekod terus tiba, jika tidak, **capaian tidak disahkan**. **Sembang tersedia** menambah sembang dengan **Pilih yang dipilih** atau **Tambah semua yang sepadan**.

### Sejarah penuh

Memuatkan sejarah yang tersedia bagi setiap sumber yang diaktifkan ke dalam Chats dan jurnal. Kemajuan dikekalkan selepas permulaan semula; lampiran mengikut tetapan media anda. Lihat [sejarah sumber](https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/).

### Perekodan

- **Pilih perubahan yang ingin disimpan**: mesej baru, suntingan, notis pemadaman, reaksi yang kelihatan, serta penyertaan dan pelepasan. Tetapan lalai menukar borang; **Simpan tetapan rakaman** menerapkannya. Mengaktifkan semula kategori tidak memulihkan acara yang terlepas.
- **Pelihara media apabila tersedia**: muat turun lampiran sehingga saiz per fail, tetapkan per jenis dari 1 hingga 2,000 MiB, dan hadkan panjang video dalam saat (0 bermaksud tiada had). Setiap percubaan muat turun mendapat keputusan yang direkodkan.
- **Semak Semula**: sembang keutamaan setiap beberapa minit, sembang lain jarang, jadi akaun kekal di bawah had FloodWait Telegram. 0 mematikan kumpulan. Tandakan sembang keutamaan dengan bintang dalam senarai; sembang setiap pusingan dan jeda antara sembang terdapat dalam Parameter. Lihat [koleksi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/).

## Eksport

**Muat turun** menyediakan fail; **Laporan bina** memilih rupa laporan.

| Apa | Gunakan untuk | Panduan |
| --- | --- | --- |
| Eksport akaun | Satu snapshot terkini tentang apa yang akaun boleh baca sekarang | [Eksport akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/account-export/) |
| Salinan untuk dikongsi | Derivatif yang diminiaturkan daripada eksport akaun yang telah selesai | [Pendedahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Tandatangan ZIP | Jurnal, laporan, lampiran dan alat pengesahan pada sempadan jurnal tetap | [Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/) |
| Laporan HTML, PDF, JSON | Laporan bermeter yang boleh dibaca | [Laporan kes](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/) |
| JSONL, CSV | Rekod asal dengan tandatangan; hamparan selamat formula | [Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/) |
| Petikan penyerahan | Hanya sembang, titik dan orang yang diperlukan oleh penerima | [Bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#investigation-handoff) |
| Eksport sembang | Satu sembang yang disahkan `chat.json` dan `chat.html` | [Eksport satu sembang](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Sulitkan muat turun di atas dengan kata laluan** (12 aksara atau lebih) menghasilkan ZIP AES-256 yang dibuka oleh 7-Zip atau WinRAR. Fail yang disahkan di dalamnya tidak berubah. Kata laluan tidak disimpan.
- **Eksport yang disediakan** mengekalkan sehingga 20 fail dalam 2 GiB, ditambah satu fail terkini, untuk muat turun semula, masing-masing dengan tanda airnyaSHA-256. Menyediakan fail tidak membuktikan penghantaran.
- Apabila pelayar menolak dialog simpanannya, panel beralih kepada muat turun biasa.
- **Identiti penandatangan anda** memaparkan cap jari kunci. **Simpan titik pemeriksaan** dan Muat turun **resit larian yang ditandatangani** memberikan anda rekod untuk disimpan di luar pengumpul. Sediakan **permintaan cap masa** membina permintaan RFC 3161 tanpa menghubungi mana-mana perkhidmatan.

## Tetapan, akaun dan sambungan

- **Tetapan**: matlamat, sambungan, apa yang hendak dirakam dan antara muka. Lihat [penyediaan pertama dan tetapan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/settings/).
- **Akaun**: setiap ruang kerja dengan statusnya, sumber, peristiwa dan barisan lampiran. Tapis mengikut **Perlukan perhatian**, **Mengumpul**, **Luar talian atau dihentikan** atau **Tidak berhubung**, hentikan atau sambung semula pilihan, import fail akaun secara pukal dan urus kumpulan. Lihat [akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/).
- **Akaun**: log masuk dan laluan sambungan akaun ini. Langsung, profil WireGuard, proksi anda sendiri, kolam MTProto awam atau WARP; sediakan dan periksa laluan, kemudian terapkan pada akaun ini, kumpulan atau semua akaun. Lihat [sambungan dan proksi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) dan [proksi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md).

## Tambahan

Pilihan: satu akaun dan sumber sudah mencukupi untuk mula mengumpul. Hanya pilihan yang anda pilih akan membuka tetapan, dan tiada apa-apa yang disambungkan secara automatik. Kad **Tahap Perlindungan** di bahagian atas memaparkan [mod perlindungan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#protection-modes).

| Kad | Apa yang ditambahkannya | Panduan |
| --- | --- | --- |
| Penyimpanan & ruang cakera | Sandaran, memindahkan fail lama ke awan anda, salinan bukti yang tidak boleh dipadam | [Penyimpanan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/) |
| Matlamat & tahap perlindungan | Tetapan yang dicadangkan untuk matlamat anda dan dua skala | [di bawah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#goal-and-protection-level) |
| Pemberitahuan | Masalah, mesej yang diubah dan ringkasan harian; bot kawalan anda sendiri | [di bawah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#notifications) |
| Bukti & sandaran | Cap masa, lebih banyak saksi dan salinan luar tapak yang disulitkan | [di bawah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#evidence-and-backups) |
| Pelayan 24/7 | Pelayan awan tanpa SSH, dicipta dan dipadam dari panel | [Jaminan tinggi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#from-the-panel) |
| Saksi bebas | Cek bertandatangan yang diposting ke saluran Telegram atau Discord anda | [Saksi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/) |
| Semak kod | Membandingkan program yang sedang berjalan dengan komit GitHub awam | [di bawah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#code-check) |

### Matlamat dan tahap perlindungan

Empat soalan:

1. **Untuk apa ia?** Rekod peribadi, siasatan, atau bukti untuk kes.
2. **Berapa banyak yang akan anda perhatikan?** Beberapa perbualan (sehingga kira-kira 50), banyak perbualan (sehingga kira-kira 500) atau keseluruhan akaun. Ini menetapkan had senarai perbualan kepada 1,000, 3,000 atau 20,000.
3. **Foto dan fail?** Teks sahaja, foto dan media pendek (foto 20 MB, video 100 MB), atau semuanya (video dan dokumen sehingga 1 GB setiap satu). Semua dengan akaun penuh juga mengekalkan 4 GiB ruang cakera kosong.
4. **Di mana ia akan dijalankan?** Komputer ini, atau pelayan yang sentiasa aktif.

Cadangan menyenaraikan cap masa bebas, drand dan senarai peranti Telegram, masing-masing dengan satu baris tentang apa yang ditambahkannya. Cap masa bermula setiap 60, 30 atau 10 minit untuk rekod peribadi, siasatan atau bukti; drand dan senarai peranti memerlukan cap masa. **Terapkan** perubahan hanya pada perkara-perkara ini, dasar lampiran dan dua parameter di atas. Setiap perubahan adalah rekod jurnal, ditambah `setup.applied`. Pemberitahuan, salinan luar tapak, pelayan, Gateway DNS, pemeriksaan kod dan saksi ditawarkan sebagai langkah seterusnya dengan borang masing-masing.

Dua skala dikira berdasarkan tetapan, bukan daripada matlamat:

| Skala | Titik |
| --- | --- |
| Kredibiliti | Jurnal bertandatangan 1, cap masa 3, drand 1, senarai peranti 1, pemeriksaan kod yang sepadan 1, pengundian saksi 1, pelayan disahkan 2, log DNS Gateway 1 |
| Kebolehpercayaan | Pelayan sentiasa aktif 3, salinan luar tapak 3, Object Lock 1, pemberitahuan masalah 1 |

80% atau lebih dianggap **maksimum**, 50% **tinggi**, 25% **sederhana**, di bawah itu **asas**. Kebolehpercayaan kini mengambil kira pelayan yang sentiasa aktif daripada jawapan kepada soalan 4, sebelum mana-mana pelayan diperiksa.

### Pemberitahuan

Notifikasi dihantar melalui Apprise ke Telegram, Discord, Slack, ntfy, e-mel, Matrix dan lebih 100 perkhidmatan lain. Pilih perkhidmatan, isi satu atau dua medan dan hantar ujian, atau tampal alamat Apprise terus.

- **Masalah**: cakera hampir penuh, akaun log keluar, pengumpulan, salinan atau cap masa ralat. Pada pelayan yang disegel, port SSH yang dibuka atau log masuk juga merupakan masalah.
- **Perubahan**: mesej yang dipadam, disunting dan hilang dalam sembang yang diperhatikan, dikumpulkan ke dalam satu pemberitahuan bagi setiap semakan (setiap minit melainkan diubah dalam Parameter).
- **Tugas yang telah diselesaikan**: sejarah, eksport dan salinan simpanan.
- **Ringkasan harian** pada waktu yang dipilih, waktu pelayan.

Notifikasi memaparkan nama sembang dan jumlah. Petikan mesej dimatikan secara lalai; apabila diaktifkan, teks mesej akan keluar dari mesin ini.

**Bot operator anda** ialah bot anda sendiri daripada @BotFather yang menjawab `/status` dan `/stats`, dan secara pilihan `/pause`, `/resume` dan `/copy`. Hanya ID sembang dan ID pengguna Telegram yang disenaraikan boleh menggunakannya; teks perbualan kekal di ruang kerja. Gunakan bot berasingan jika aplikasi lain sudah menerima arahan bot tersebut. Lihat [pemberitahuan](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) dan [bot pengendali](https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/#operator-bot-and-completion-notices).

### Bukti dan sandaran

- **Cap masa bebas** menghantar hanya tandatangan setiap titik pemeriksaan yangSHA-256 ditandatangani kepada pihak berkuasa RFC 3161 dan kalendar OpenTimestamps, setiap 5 hingga 1,440 minit. Anchor**kini** menjalankan satu pusingan. Lihat [cap masa](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/).
- **Lebih banyak saksi**, masing-masing tidak aktif sehingga dipilih: pusingan drand terbaru, senarai peranti yang log masuk Telegram tanpa alamat IP, dan log pertanyaan DNS pelayan Gateway Cloudflare. Lihat [rekod pilihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- Salinan **sandaran yang disulitkan** menyalin jurnal, fail, titik pemeriksaan dan eksport sembang ke penyimpanan serasi S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Segala-galanya disulitkan pada mesin ini terlebih dahulu. **Muat turun kunci penyulitan** dan simpan ia terpisah: tanpa ia, salinan tidak dapat dibaca. Kunci Objek dalam mod Tadbir Urus atau Pematuhan mencegah objek daripada dipadam untuk sejumlah hari yang ditetapkan. Lihat [salinan luar tapak](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Semak kod

Semak sama ada program yang dipasang sepadan dengan versi yang diterbitkan.

1. Masukkan repositori GitHub (yang rasmi telah diisi) dan tag, cabang atau komit.
2. **Check now** meminta API GitHub, melalui laluan ruang kerja ini untuk permintaan luar, untuk senarai fail bagi komit tersebut. Ia membandingkan ID blob git setiap fail program yang diukur dengan komit tersebut. Checkout Windows dengan hujung baris yang ditukar masih sepadan.
3. Hasilnya menyenaraikan fail yang diubah, tambahan dan yang hilang (sehingga 50 bagi setiap satu) dan disimpan sebagai a `source.checked` rekod jurnal.

Hasil hanya diiktiraf sebagai semasa selagi fail program yang sedang berjalan tidak berubah: semak semula selepas kemas kini. Tiada token diperlukan dan hanya repositori awam berfungsi; perbualan dan maklumat log masuk tidak dimuat naik. Padanan mengenal pasti kod pada cakera. Ia bukan pengesahan perkakasan; untuk itu, lihat [Phala Cloud](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Mod perlindungan

Penukar di sebelah nombor versi memaparkan mod yang dipilih dan berapa banyak daripada 18 lapisan perlindungan yang aktif, sebagai contoh `🟠 Witnessed 9/18`. **Tukar mod** di **Tambahan → Tahap Perlindungan** membuka pilihan. Satu mod menerangkan sasaran dan menyenaraikan apa yang masih kurang; rakaman, penandatanganan dan tetapan yang disimpan adalah sama dalam setiap mod.

| Mod | Untuk | Menambah |
| --- | --- | --- |
| 🟢 Mudah | Memantau sembang dan menyimpan salinan | Perbualan, jurnal dan eksport sembang; penandatanganan dijalankan di latar belakang |
| 🟡 Ditandatangani | Lapor kepada platform, hos atau meja penyalahgunaan | Arkib bermassa, semakan jurnal, titik pemeriksaan, ekstrak penyerahan |
| 🟠 Disaksikan | Kes di mana seseorang mungkin mendakwa rekod itu telah diubah | Saksi bebas yang menyiarkan tajuk jurnal yang ditandatangani |
| 🔴 Sedia untuk mahkamah | Bukti untuk peguam, polis atau mahkamah | Cap masa, salinan luar tapak yang disulitkan, butiran kes dalam laporan |
| 🟣 Disahkan GitHub | Rekod yang perisiannya mesti dapat disemak oleh sesiapa sahaja | Pemeriksaan kod dan tangkapan GitHub Actions |
| ⚫ Mossad | Kes berisiko tinggi menentang pihak lawan yang dibiayai dengan baik | Pelayan 24/7 yang disegel, alamat IP tersembunyi, semua 18 lapisan |

Lapisan-lapisan: setiap rekod ditandatangani dan diikat secara berantai; resit pelaksanaan yang ditandatangani; lampiran disimpan dengan SHA-256; titik pemeriksaan yang ditandatangani; semakan semula; amaran masalah; akses saksi baca sahaja; saksi memeriksa mengikut jadual; cap masa RFC 3161; bukti OpenTimestamps; cap masa terkini yang disahkan; salinan luar tapak yang disulitkan; butiran kes dalam laporan; semakan kod yang sepadan; Telegram tidak pernah melihat IP mesin ini; permintaan luar melalui proksi; Kunci Objek pada salinan; pelayan tersegel dengan rekod penyedia. Satu lapisan yang dimatikan ialah **Set Up**, yang membuka borangnya. Memilih mod yang lebih rendah meminta pengesahan dan tidak memadam apa-apa.

## Alat lain

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Tanya arkib**: cari pemerhatian yang disimpan, semak sumber, kemudian tentukan sama ada hendak menghantarnya ke model AI. Lihat [analisis arkib](https://phishdestroy.github.io/TgWitness/ms/docs/reference/analysis/) dan [OCR serta transkripsi tempatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/media-analysis/).
- **Parameter**: had dan kelajuan pengumpulan, semakan semula, muat turun, profil, pemberitahuan dan eksport. Cari mengikut nama, tunjukkan nilai **Hanya yang berubah** dan sediakan nilai lalai sebagai draf dengan **Pulihkan lalai…**. **Simpan parameter** menerapkan nilai daripada penggunaan seterusnya mereka, dan setiap perubahan adalah rekod jurnal.
- **Akses**: token berasingan untuk penilai, penganalisis dan pengendali, terhad kepada ruang kerja, sembang dan hak yang dipilih. Lihat [akses](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/).
- **Log sistem** : apa yang dilakukan oleh proses ini sejak ia bermula (pautan, perubahan proksi, log masuk, penolakan, perubahan tetapan) dengan alamat IP disembunyikan. **Ikuti baris baru** mengekalkan baris terbaru dalam paparan. Mesej hanya kekal dalam jurnal.
- **Integrasi**: penyedia AI, sambungan [MCP baca sahaja](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/) dan [webhook yang ditandatangani](https://phishdestroy.github.io/TgWitness/ms/docs/reference/webhooks/).
- **Case Board**: nota pasukan peribadi, penanda buku dan kepingan di sebelah bukti. Lihat [Case Board](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-board/).
- **GitHub Actions menangkap** dalam Eksport: satu sembang ditangkap daripada fork anda. Lihat [perekodan tersegel](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
