# Penyimpanan dan pemulihan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/

Sandaran, memindahkan fail lama ke awan anda, salinan di bawah Object Lock dan pemulihan pada mesin baru.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penyebaran dan pemulihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/)

![Penyebaran & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Panel memisahkan tiga tugas:

| Tugas | Apa yang dilakukannya |
| --- | --- |
| Simpan sandaran | Salin jurnal yang ditandatangani, titik pemeriksaan, fail yang dipelihara dan eksport yang sedang menunggu ke destinasi S3 yang dikonfigurasikan. |
| Ruang tempatan percuma | Salin lampiran lama terpilih ke S3 atau ke jauh awan rclone, baca semula sepenuhnya, sahkan bait yang disulitkan, kemudian padamkan salinan tempatan yang disahkan. |
| Simpan salinan bukti | Konfigurasikan S3 Object Lock dan semak status pengekalan yang dikembalikan. Perkhidmatan mesti mengesahkan mod dan tarikh yang diminta. |

Membersihkan ruang tidak pernah memadam atau menulis semula jurnal yang disahkan. Setiap lampiran mengekalkan tandatangan asalnya dan resit pemulihan.SHA-256 Pemampatan gzip pilihan dilakukan sebelum penyulitan berotentikasi. Nama fail awan tidak mengandungi nama Telegram, ID sembang atau nama lampiran asal. Satu lampiran boleh sehingga 32 GiB.

Respon muat naik sahaja tidak memberi kebenaran untuk memadam fail. TgWitness memuat turun objek disulit sepenuhnya dan mengesahkan saiz serta SHA-256, menyimpan resit, kemudian menyemak bait tempatan sekali lagi sejurus sebelum pemadaman. Kegagalan muat naik, bacaan semula berbeza atau pemindahan dibatalkan mengekalkan fail tempatan di tempatnya. Jika sandaran bukti yang diaktifkan belum menyalin fail tersebut, pemadaman juga akan menunggu sehingga ia disalin.

**Pada halaman ini**

- [Apabila cakera hampir penuh](https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/#when-the-disk-is-filling-up)
- [Sambungkan destinasi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/#connect-a-destination)
- [Simpan fail pemulihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/#keep-the-recovery-file)
- [Pemulihan selepas kehilangan pemasangan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/#recover-after-losing-the-installation)
- [Bot pengendali dan notis penyempurnaan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/storage/#operator-bot-and-completion-notices)

## Apabila cakera semakin penuh

Muat turun lampiran dijeda apabila ruang kosong di bawah nilai **Parameter → Lampiran → ruang cakera kosong** (lalai 1 GiB), dengan giliran dikekalkan. Pemerhatian teks diteruskan. Ini tidak bergantung pada pemberitahuan: mematikannya tidak mematikan rizab muat turun atau perlindungan storan.

Untuk bertindak lebih awal, aktifkan **Jalankan secara automatik**, pilih **Buang fail setempat untuk mengosongkan ruang** dan aktifkan **Mulakan pemindahan tambahan apabila ruang cakera rendah**. Secara lalai, peraturan pilihan bermula di bawah 5120 MiB kosong dan memproses kelompok sehingga 10240 MiB tersedia. Kedua-dua ambang boleh ditetapkan. Destinasi, usia minimum fail, had kelompok, pengesahan bacaan semula penuh dan prasyarat sandaran bukti sama seperti proses manual. Destinasi tidak diaktifkan sendiri. Semakan dibuat setiap 30 saat; ralat atau tiada kemajuan menangguhkan cubaan berikutnya lima minit. Keadaan dan masa cubaan semula kekal selepas mula semula. Ketika peraturan tidak aktif, proses berjadual mengekalkan sela biasa.

Panel menunjukkan ruang kosong, rizab pembungkusan, kesiapsiagaan peraturan dan fail yang dilangkau kerana ruang sementara tidak cukup. Pembungkusan dan pemulihan menyemak keperluan ruang sementara puncak sebelum bermula serta ruang tersedia semasa menulis. Rizab mengikut tetapan muat turun, dengan minimum 64 MiB untuk operasi storan. Semakan ini bukan kuota sistem fail: proses lain masih boleh menggunakan ruang antara semakan.

Gzip memampatkan objek jauh tanpa kehilangan data; ia tidak mengecilkan jurnal aktif atau mencipta arkib setempat. JPEG, video dan ZIP mungkin hampir tidak mengecil atau sedikit membesar. Dengan pemampatan, pembungkusan mungkin memerlukan ruang sementara kira-kira dua kali saiz lampiran ditambah rizab. Pilih ambang mula cukup awal untuk fail terbesar. Fail terlalu besar dikekalkan dan dilaporkan; fail kecil serta salinan jauh yang telah disahkan masih boleh mengosongkan ruang. Salinan disahkan membolehkan fail setempat dibuang tanpa fail pembungkusan baharu. Pemulihan juga memerlukan ruang sementara dan boleh ditolak sehingga ruang tersedia.

Jika tiada fail layak dipindahkan atau destinasi belum ditetapkan, TgWitness tidak boleh mengosongkan ruang secara automatik. Pengurusan storan tidak pernah memangkas atau menulis semula jurnal bertandatangan. Ia masih memerlukan ruang untuk pemerhatian teks baharu.

## Sambungkan destinasi

Di **Ekstra → Penyimpanan & ruang cakera → Kelola penyimpanan**, pilih tugas dan destinasi, simpannya, kemudian pilih **Uji muat naik & muat turun**. Ujian ini memuat naik probe rawak kecil dan membacanya semula. Ia tidak menggunakan kandungan Telegram.

Untuk S3, gunakan titik akhir, rantau dan baldi sebenar penyedia. Wasabi, Backblaze, Cloudflare R2 dan perkhidmatan serasi lain menggunakan tetapan S3 yang sama. API serasi sahaja tidak bermakna menyokong Object Lock. Mod tadbir urus mungkin membolehkan pentadbir yang dibenarkan memintas tempoh penyimpanan; Mod pematuhan mempunyai sekatan berbeza. Baca status Object Lock yang dikembalikan sebelum bergantung pada tempoh penyimpanan.

Untuk destinasi rclone, cipta satu remote menggunakan penyediaan penyedia rclone dan tampal remote tersebut `[name]` seksyen ke dalam panel. Helper yang dipasang menyokong MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud dan penyedia lain yang ditunjukkan dalam pemilih. Butiran log masuk disimpan dalam peti besi disulitkan ruang kerja ini. Pembaharuan OAuth disimpan semula ke dalam peti besi. Butiran log masuk tidak ditambah ke acara jurnal atau disertakan dalam muat turun pemulihan.

Helper dipasang dalam ruang kerja, dengan versi yang dipin dan SHA-256. Ia tidak ditambah ke dalam PATH sistem. Fail konfigurasi dan fail kerja adalah fail sementara dalam ruang kerja tersebut. Remot berasaskan arahan dan remot fail tempatan ditolak. rclone pada masa ini memerlukan laluan **Langsung** yang dipilih secara eksplisit untuk permintaan luaran. Gunakan storan S3 asli untuk laluan SOCKS5 atau HTTP ruang kerja; rclone tidak akan secara senyap memintas laluan yang tidak tersedia.

## Simpan fail pemulihan

Pilih **Simpan fail pemulihan** selepas menyalin fail dan simpan ia di tempat yang berasingan daripada pemasangan. Ia mengandungi kunci penyahsulitan dan resit objek yang ditandatangani, jadi anggap ia sebagai sandaran kunci peribadi. Simpan konfigurasi jauh asal dan kelayakan destinasi secara berasingan juga. Fail pemulihan yang diambil sebelum salinan kemudian tidak mengandungi resit bagi fail tersebut.

Cap jari kunci tandatangan sepatutnya telah direkodkan secara berasingan. Tandatangan yang hanya disemak menentang kunci yang disediakan dalam fail yang sama tidak dapat menentukan milik siapa fail pemulihan itu.

Untuk membaiki resit storan yang hilang dalam ruang kerja sedia ada, buka **Pulih fail daripada fail pemulihan yang disimpan** dan pilih fail tersebut. Panel memeriksa tandatangan dan memerlukan kunci penandatanganan ruang kerja yang sama. Ia menolak untuk menggantikan kunci storan yang berbeza. Kemudian pilih **Pulihkan semua fail**. Pemulihan menangguhkan peraturan storan automatik supaya pusingan terjadual seterusnya tidak dapat segera memadam semula fail yang dipulihkan. Aktifkan semula peraturan apabila selesai dengan salinan tempatan.

Pemulihan mengesahkan teks sesar, mengautentikasi penyahsulitan, menyahmampat jika perlu dan memeriksa teks biasa asal SHA-256 sebelum meletakkan fail dalam `media/`Objek jauh yang rosak tidak akan menggantikan fail tempatan. Fail tempatan sedia ada dengan bait berbeza akan disimpan untuk semakan semula dan bukannya dioverwrite.

## Pemulihan selepas kehilangan pemasangan

Pasang TgWitness pada mesin lain. Gunakan fail pemulihan peribadi, cap jari yang dirakam secara berasingan dan kelayakan destinasi asal:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

Untuk S3, `--credentials` menunjuk kepada fail JSON peribadi dengan `access_key` dan `secret_key`; fail pemulihan yang disahkan menyediakan tetapan destinasi. Perintah ini menggunakan sambungan luaran terus dan memuat turun pembantu yang dilampirkan apabila rclone jauh memerlukannya. Ia menolak direktori output yang sedia ada.

Bait asal yang dipulihkan ditulis ke `recovered-attachments/media/`, dinamakan oleh SHA-256 mereka. `recovery-log.jsonl` ialah rekod tanpa tandatangan bagi operasi pemulihan. Perintah ini tidak mencipta semula jurnal bertandatangan yang hilang atau kunci penandatanganannya. Simpan sandaran penuh ruang kerja untuk perkara-perkara tersebut. Fail pemulihan storan bukan merupakan sandaran penuh ruang kerja.

## Bot pengendali dan notis penyempurnaan

Bot Telegram milik pengendali. Buat ia melalui BotFather dan tetapkan token, sembang destinasi dan ID pengguna Telegram yang dibenarkan secara eksplisit dalam panel. Baik penghantar mahupun sembang mesti sepadan. Mesej dan arahan yang diteruskan daripada bot lain diabaikan.

`/status` dan `/stats` tersedia dalam mod lalai hanya status. Mod kawalan pilihan menambah `/pause`, `/resume` dan `/copy`. `/copy` meminta tugas storan yang dikonfigurasikan; ia tidak bermakna bahawa muat naik jauh telah selesai. Perintah tidak boleh membekalkan URL, fail atau program shell sewenang-wenangnya.

Gunakan tetapan pemberitahuan berasingan untuk amaran dan pemberitahuan penyempurnaan tugas. Pemberitahuan penyempurnaan membezakan eksport akaun yang terputus-putus daripada eksport lengkap, dan memaparkan sejarah serta jumlah storan. Petikan mesej tidak disertakan melainkan diaktifkan secara berasingan dalam tetapan pemberitahuan. Pemilih perkhidmatan dijana daripada katalog Apprise yang dipasang sebenar dan bukannya set contoh penyedia yang tetap.
