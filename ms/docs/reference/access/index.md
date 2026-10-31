# Akses dan kebenaran

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/

Keluarkan akses terhad kepada akaun dan sembang, pilih kebenaran, hadkan sesi dan alamat IP, dan tarik balik akses.

Beri seorang penilai akses kepada satu sembang, seorang penganalisis kebenaran untuk mengeksport satu kes, atau seorang pengendali kawalan ke atas akaun terpilih. Setiap orang mendapat token mereka sendiri. Token panel utama kekal dengan pentadbir.

[Pengesetan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/) · [Laluan sambungan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) · [Model keselamatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/security/)

## Dua skop, dua tugas berbeza

**Skop pengumpulan** menentukan apa yang direkodkan oleh akaun: sembang terpilih, folder Telegram atau keseluruhan akaun. **Skop capaian** menentukan mana-mana akaun dan sembang yang direkodkan boleh dilihat dan digunakan oleh orang lain. Memberi capaian tidak menyertai sembang Telegram, memulakan pengumpulan atau memberi kebenaran akaun Telegram.

Akses boleh membuka ruang kerja terpilih, sembang terpilih di dalamnya, atau semua ruang kerja. **Semua ruang kerja, termasuk yang ditambah kemudian**, juga merangkumi akaun masa depan. Pilih ruang kerja secara eksplisit apabila kes hendak dihadkan kepada ruang tersebut.

## Memberi seseorang akses

1. Log masuk sebagai pentadbir utama dan buka **Akses**.
2. Di bawah **'Beri seseorang akses**', masukkan nama yang akan anda kenali dalam log.
3. Pilih ruang kerja dan, jika perlu, sembang individu.
4. Pilih apa yang mungkin dilakukan oleh orang ini. **Lihat** sentiasa disertakan.
5. Tetapkan tarikh luput, had log masuk/sesi dan alamat yang dibenarkan mengikut keperluan.
6. Tekan **'Create access**'. Salin token sekarang: ia hanya dipaparkan sekali.
7. Hantar alamat panel dan token secara peribadi. Penerima memasukkan token itu pada halaman log masuk biasa; mereka tidak memerlukan token panel utama anda atau sesi Telegram.

Buka panel dengan token yang dikeluarkan dalam sesi pelayar berasingan dan periksa sembang yang boleh dilihat serta tindakan yang dibenarkan sebelum menyerahkannya.

## Pilih kebenaran

| Kebenaran | Apa yang dibenarkan |
| --- | --- |
| `view` | Baca sembang yang dibenarkan, mesej yang dirakam, profil, fail dan rekod jurnal yang ditapis. Sentiasa disertakan. |
| `export` | Eksport sejarah sembang dan dosie yang dibenarkan. Eksport bukti seluruh ruang kerja memerlukan akses ke seluruh ruang kerja. |
| `sources` | Urus sumber, tangkapan skrin dan cap profil. Akses terhad sembang hanya boleh bertindak pada sembang yang dibenarkan; penemuan sumber dan tetapan skop merentas akaun kekal tertutup. |
| `collect` | Mulakan atau hentikan pengumpul. Memerlukan akses ke seluruh ruang kerja kerana pengumpulan menjejaskan akaun. |
| `interact` | Lakukan interaksi Telegram yang disokong dalam skop capaian. Akses terhad sembang tidak boleh menggunakan pratonton pautan untuk seluruh akaun. |
| `settings` | Ubah tetapan pengumpulan, cap masa, pemberitahuan, salinan luar tapak dan parameter. Memerlukan akses penuh ke ruang kerja. |
| `account` | Masuk atau log keluar Telegram dan urus laluan sambungan. Memerlukan akses penuh ke ruang kerja. |

Kebenaran dan skop disemak serentak. Menandakan kebenaran tidak akan membuka sembang lain atau membuka operasi merentas ruang kerja untuk capaian terhad pada sembang. Untuk eksport selari, capaian mesti merangkumi sembang yang dieksport dalam setiap akaun yang dipilih. Capaian yang dikeluarkan tidak boleh mencipta capaian baru, mengurus sesi orang lain atau membuka konsol pentadbir.

### Tiga susunan berguna

| Orang | Skop | Kebenaran |
| --- | --- | --- |
| Penilai | Perbualan rakaman satu kes | `view` |
| Penganalisis menyediakan penyerahan tugas | Perbualan untuk disiasat dan dieksport | `view`, `export`; tambahkan `interact` hanya jika mereka perlu bertindak melalui Telegram |
| Pengendali pengumpulan | Ruang kerja keseluruhan yang dipilih | `view`, `sources`, `collect`; tambahkan `settings` atau `account` hanya apabila diperlukan |

Ini adalah contoh yang anda konfigurasi dengan kotak semak kebenaran, bukan peranan tetap.

## Had dan sesi

| Persetelan | Bagaimana ia berfungsi |
| --- | --- |
| Sesi selari | Hadkan sesi serentak kepada 1–100. Apabila mencapai had, tolak log masuk seterusnya atau tamatkan sesi tertua. |
| Log masuk dibenarkan | Hadkan penggunaan token yang berjaya hanya untuk memulakan sesi. Sesi sedia ada tidak akan ditamatkan semata-mata kerana log masuk terakhir yang dibenarkan telah digunakan. |
| Bersahaja sehingga | Tamat akses secara mutlak. Akses yang telah tamat tidak dapat log masuk atau terus membuat permintaan. |
| Minit tanpa aktiviti | Tamat masa tidak aktif sesi, dari 5 minit hingga 30 hari. Permintaan yang berjaya akan memanjangkannya; panel terbuka boleh kekal aktif dengan membuat semakan berkala. |
| Alamat yang dibenarkan | Terima alamat IP tertentu atau subnet CIDR. Biarkan kosong untuk membenarkan sebarang alamat melainkan pengikatan log masuk pertama diaktifkan. |
| Ikatan pada log masuk pertama | Log masuk pertama yang berjaya menetapkan alamat yang dibenarkan untuk capaian tersebut. |

IP ialah alamat klien yang dilihat oleh aplikasi. Di sebalik proksi songsang atau terowong, semak alamat yang dipaparkan dalam **Sesi Terbuka** sebelum bergantung pada peraturan IP: jika tidak, beberapa pengguna mungkin kelihatan berkongsi alamat proksi tersebut.

## Ubah atau tarik balik akses

Sunting entri di bawah **Akses** untuk mengubah skop, kebenaran atau hadnya. Perubahan skop dan kebenaran disemak pada permintaan seterusnya, termasuk permintaan daripada sesi yang sudah terbuka. Membatalkan akses akan menamatkan sesinya dan menjadikan token yang dikeluarkan tidak boleh digunakan. **Sesi terbuka** juga membolehkan pentadbir menamatkan sesi individu tanpa membatalkan keseluruhan akses.

Pencabutan tidak dapat memulihkan semula fail yang telah dimuat turun oleh seseorang. Log keluar, mengunci panel atau menamatkan sesi tidak menghentikan pengumpul yang sedang berjalan.

## Apa yang boleh dilihat oleh pentadbir

**Log sejak permulaan ini** menggabungkan log proses dengan aktiviti jurnal dari setiap ruang kerja: log masuk, penolakan, perubahan laluan dan tindakan pengendali. Ia adalah konsol dalam memori untuk proses semasa, bukan salinan kekal bagi setiap mesej. Acara mesej yang kerap kekal dalam jurnal dan bukannya memenuhi konsol.

Penerbitan, perubahan dan pembatalan akses, serta permulaan atau penamatan sesi, juga menghasilkan rekod jurnal `access.*` yang disahkan. Token tidak disertakan dalam rekod tersebut. Token yang dikeluarkan dan kelayakan sesi disimpan sebagai hash dalam peti besi yang disulitkan.

****Pentadbir utama dan sempadan kepercayaan**** Token panel utama kekal tidak terhad. Log masuk pelayar dengannya mewujudkan sesi yang tertakluk kepada had sesi yang dikonfigurasikan oleh pentadbir. Skrip yang menghantar token utama secara langsung mengekalkan akses penuh dan tidak dikira sebagai sesi pelayar. Ini adalah kawalan capaian peringkat aplikasi dalam satu pemasangan. Semua ruang kerja berkongsi proses pelayan; ini bukan pengasingan daripada pentadbir hos. Jaga token utama, sesi Telegram, kunci penandatanganan dan direktori data supaya kekal peribadi. Token saksi adalah titik pemeriksaan/kredensial kesihatan yang berasingan, bukan token capaian panel.
