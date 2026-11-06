# Konfigurasi dan pengesahan laporan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/

Penapis laporan, lapan reka bentuk, pratetap kandungan, sejarah perubahan yang disimpan dan penilaian yang disertakan dalam eksport yang ditandatangani.

Ubah pemerhatian terpilih menjadi satu akaun kes yang mudah dibaca: persoalannya, skopnya, perubahan yang disimpan, carta, penemuan dan rujukan sumber. Setiap laporan memberi penerima cara untuk menyemak bahan yang dihantar dan memeriksa liputan pengumpulannya.

Bahagian **Asas kepercayaan dan had** muncul dalam laporan jurnal, penyerahan, sembang, akaun dan perkongsian. PDF jurnal dan penyerahan menggunakan penilaian yang sama seperti `report.json` yang ditandatangani. Manifest ZIP membawa `case_assessment` dalam manifest yang ditandatangani. Penilaian ini dibawa bersama bahan yang dieksport. Pengamatan asal mengekalkan tandatangan sedia ada mereka.

## Format dokumen dan susunan pembacaan

### Studio Laporan

Buka **Eksport → Konfigurasi dan pratonton**. Lalui **Data → Reka bentuk & kandungan → Pratonton**:

1. Gunakan keseluruhan ruang kerja atau pilih sembang, pengarang, tarikh pemerhatian UTC termasuk dan jenis acara. Muatkan katalog untuk mencari sembang dan pengarang, atau masukkan ID Telegram mereka. Penapis pengarang sepadan dengan ID penghantar yang direkodkan; notis pemadaman tanpa penghantar tidak sepadan dengan penapis pengarang.
2. Pilih reka bentuk halaman, kemudian pilih carta, label peserta, transkrip dan penemuan bertulis anda. Mengubah reka bentuk mengekalkan pilihan-pilihan ini.
3. Bina pratonton. Ia memaparkan kiraan sebenar, aktiviti, peserta, rekod sampel, perubahan yang disimpan dan julat nombor mesej yang hilang. Mengubah pilihan menandakan pratonton sudah lapuk. Simpan sebelum memuat turun HTML, PDF yang ditandatangani, JSON yang ditandatangani atau ZIP bukti.

Pratinjau data mengira keseluruhan awalan jurnal yang stabil, bukan sampel awal. Hanya baris sampel yang dipaparkan dan senarai panjang yang dihadkan; bilangan yang terlepas dipaparkan. Eksport kemudian mengambil tangkapan stabil baharu, jadi pengumpulan berterusan mungkin meningkatkan angka. Skop, bilangan dan identiti sumber disertakan dalam laporan yang ditandatangani. Membuka atau pratonton borang tidak menyimpannya.

**Pilih salinan penerima.** Carta dan transkrip menggunakan rekod yang dipilih. Integriti, pemilikan dan liputan menerangkan jurnal sumber penuh. ZIP bukti mengandungi rekod asal dan lampirannya. Gunakan [penyerahan minimum](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#handover-extract) apabila penerima hanya perlu menerima data terpilih yang dibenarkan.

### Bacakan suntingan, pemadaman dan ID yang hilang

Suntingan memaparkan teks **Sebelum** dan **Selepas** yang disimpan dan menyerlahkan perkataan yang diubah. Pemadaman memaparkan versi terakhir yang disimpan sebelum pemberitahuan. Jika tiada kandungan terdahulu dirakam, laporan akan menyatakan demikian. Apabila anda memilih hanya suntingan atau pemadaman, versi sebelumnya kekal tersedia sebagai konteks yang dilabelkan secara eksplisit di luar penapis. Mesej yang tidak berkaitan tidak ditambah ke dalam sejarah ini.

**ID mesej yang tidak diperhatikan** adalah jurang antara nombor yang diketahui dalam sembang terpilih dan julat ID yang diperoleh daripada tarikh. Setiap rekod sumber yang diketahui diperiksa sebelum mengisytiharkan sesuatu nombor sebagai tidak diperhatikan: menapis pengarang lain, jenis peristiwa atau tarikh tidak boleh menghasilkan jurang palsu. Mesej yang disimpan bersebelahan dilabel sebagai konteks. Nombor yang hilang tidak membuktikan bahawa mesej itu wujud atau telah dipadam; notis pemadaman dan semakan semula yang tidak berjaya kekal sebagai jenis peristiwa yang berasingan.

### Pilih reka bentuk

Lapan reka bentuk halaman tersedia untuk laporan jurnal dan HTML sembang tunggal serta PDF yang ditandatangani. Mereka menggunakan rekod dan pengiraan yang sama, dengan muka depan, tipografi, tajuk bab, jadual dan jarak yang berbeza.

| Reka bentuk | Gaya pembacaan |
| --- | --- |
| Klasik | Dossier tradisional dengan kulit gelap dan bahagian bernombor. |
| Suntingan | Halaman tajuk serif berbingkai, margin lebar dan jalur bab sempit. |
| Taklimat | Sampul padat dengan tulang belakang biru laut, tajuk pendek dan jadual berpenyusunan rapat. |
| Analitik | Sampul gaya tinjauan, plat carta modular dan figura berruang sama. |
| Teknikal | Daftar bergaris, rel rujukan bernombor dan jadual perbandingan tepat. |
| Rangkuman | Sampul panoramik, jarak yang lapang dan figura ringkasan yang menonjol. |
| Siri bacaan | Rel seksyen dan bab yang dikelompokkan untuk penemuan, skop, perubahan dan jurnal pemerhatian. |
| Ledger & margin | Bab bernombor dengan margin luas, carta jadual yang tepat dan transkrip mesej berasingan. |

Reka bentuk disimpan bagi setiap ruang kerja dan direkodkan dalam manif eksport yang ditandatangani. HTML berfungsi secara luar talian, menyokong tema cerah dan gelap, dan menyesuaikan diri dengan skrin sempit serta bahasa dari kanan ke kiri. PDF asli menggunakan fon terbungkus; reka bentuk Editorial termasuk Noto Serif di bawah Lesen Fon Terbuka SIL yang dibundel. Siri bacaan dan Ledger & margin juga terpakai pada gambaran keseluruhan akaun, sembang akaun dan salinan perkongsian.

PDF Bahasa Cina, Jepun dan Korea juga memerlukan fon yang sesuai pada pelayan, seperti Noto Sans CJK, dipasang di seluruh sistem atau diletakkan di `TGWITNESS_FONT_DIR`. Apabila ia tidak tersedia, ZIP mengekalkan laporan HTML dan JSON.

Kedua-dua reka bentuk ini merangkumi jurnal yang boleh dibaca tanpa JavaScript. Untuk eksport besar, paparan ini mengandungi sehingga 500 rekod penuh dalam bajet input 8 MiB; laporan menandakan had dan memautkan kepada pemapar lengkap serta rekod sumber. Direktori akaun dan indeks hubungan menerangkan sampel bacaan yang sama itu, bukan semua peserta. Carta jurnal penuh mengekalkan skop mereka yang dinyatakan secara berasingan.

### Pilih kandungan

| Aisyen pratetap | Disertakan secara lalai |
| --- | --- |
| Dossier kes | Aktiviti, masa pemerhatian, peserta, sembang dan transkrip rekod. |
| Taklimat | Garis besar aktiviti tanpa kedudukan peserta atau transkrip. |
| Semakan aktiviti | Aktiviti, masa pemerhatian, peserta, sembang dan komposisi, dengan rujukan sumber dan angka tepat. |
| Laporan tersuai | Gabungan anda sendiri carta, transkrip dan pratonton. |

Menukar tetapan awalan mengekalkan reka bentuk anda, butiran kes dan analisis bertulis. Semakan integriti, liputan, had dan arahan pengesahan kekal dalam setiap reka bentuk. Rekod sumber dalam ZIP kekal tidak berubah apabila carta atau transkrip disembunyikan.

**Nota Pemeriksaan** pilihan mengandungi soalan, kaedah, penemuan dan kesimpulan yang ditulis oleh pengarang laporan. Petik fail sumber dan nombor rekod dalam penemuan. Tandatangan mengekalkan kenyataan yang ditulis ini bersama laporan; pemerhatian sumber dan tafsiran pengarang kekal boleh dikenal pasti. Penyerahan yang dimimumkan mengabaikan nota peribadi ini dan carta jurnal penuh. Pilihan carta dan pemeriksaan terpakai pada laporan jurnal.

Pilih aktiviti mengikut masa, peta haba hari/jam UTC, kedudukan peserta, kedudukan sembang dan komposisi rekod. Pilih 5–30 kumpulan berperingkat dan nama samaran atau ID akaun peserta neutral. Pengirim tidak dikenali dan peserta selebihnya berada dalam baris berasingan. Nama samaran hanya mempengaruhi carta; rekod sumber masih mengandungi identiti mereka.

Pratonton reka bentuk dikemas kini daripada draf yang belum disimpan menggunakan komponen muka depan, pemeriksaan dan carta pengeluaran, terhad kepada padanan dalam 50,000 rekod sumber pertama. Pratonton data di bawah mengira keseluruhan pilihan. Ia secara eksplisit tidak ditandatangani dan tidak mengekalkan suntingan. Butang Muka Depan dan Carta menukar seksyennya. Ini bukan pratonton PDF yang lengkap. **Simpan tetapan laporan** menerapkan pilihan pada eksport akan datang; fail yang telah ditandatangani sedia ada tidak boleh diubah. PDF menggunakan muka depan, tipografi, susun atur bab yang dipilih dan agregat terpilih yang sama seperti HTML dan JSON yang ditandatangani.

Penilaian kepercayaan, had liputan dan arahan pengesahan kekal wujud. Menyembunyikan carta atau transkrip boleh dibaca tidak membuang baris sumber berkuasa daripada ZIP. Siri carta yang dilumpuhkan diabaikan dalam JSON analitik; gunakan eksport yang diminimumkan untuk mengehadkan pendedahan rekod sumber.

Penapis pemilihan data terpakai pada laporan jurnal; eksport akaun dan perkongsian mengekalkan skop pemerolehan dan pendedahan mereka sendiri.

Keutamaan reka bentuk/grafik yang dikongsi dibekukan ke dalam eksport sembang/akaun baharu dan pratonton perkongsian akaun. Bahasa akaun/perkongsian dan tetapan privasi kekal berasingan; nota kes peribadi dan pemeriksaan tidak disalin ke dalam eksport ini. Laporan akaun dan perkongsian kekal dilindungi HTML oleh manifester arkib yang ditandatangani. Jurnal, penyerahan jurnal yang dimimumkan dan kit sembang tunggal juga menyediakan PDF yang disahkan.

### Apa yang dikira oleh carta

Aktiviti jurnal dan peta haba mengira **pemerhatian** baru, bersejarah, pulih, disunting, dipadam dan hilang semasa semakan semula, mengikut masa pemerhatian pengumpul dalam UTC. Denyutan jantung dan resit lampiran dikecualikan. Peringkat peserta hanya mengira pemerhatian mesej baharu, bersejarah dan pulih: penghantar tidak diisytiharkan sebagai penyunting atau pemadam. Pemerhatian berulang boleh menerangkan mesej Telegram yang sama.

Analitik jurnal mengekalkan kiraan mengikut jenis, rujukan rekod pertama/terakhir dan SHA-256 sumber `events.jsonl`. Rajah termasuk nilai tepat dalam HTML dan PDF. Bakul harian beralih kepada bulan melebihi 366 hari yang direkodkan; graf menggabungkan ini ke dalam paling banyak 36 selang lebar sama. Lebih daripada 100,000 pengecam unik atau 1,200 bulan menandakan carta yang terjejas tidak tersedia, manakala kiraan keseluruhan tepat kekal tersedia.

Grafik tangkapan skrin dan perkongsian akaun hanya mengira baris mesej bukan perkhidmatan yang disertakan, menggunakan masa mesej yang direkodkan. Pengagregatan perkongsian dikira selepas penyensoran dan penapisan. Grafik ini menggunakan paling banyak 90 selang tarikh UTC lebar sama dan mengekalkan sehingga 10,000 nilai pengelompokan; kiraan berlebihan dinyatakan secara eksplisit dan diselesaikan. Interval terakhir mungkin lebih pendek. Tarikh yang tidak diketahui atau tidak sah tidak dimasukkan ke dalam carta masa.

Selang kosong bermaksud tiada pemerhatian disertakan; semak liputan untuk mengetahui jurang. Carta-carta ini menerangkan aktiviti yang disimpan. Pengirim tidak dikenali kekal sebagai kategori berasingan, dan setiap semakan dilaporkan secara berasingan.

Apabila disertakan, `analytics.json` dilindungi oleh hash fail berasingan yang ditandatangani. Jurnal `report.json` menyelitkan agregat terpilih yang sama. Pengesahan tandatangan mengesan bait yang telah diubah. Untuk menyemak angka, kira semula agregat jurnal dengan `report_analytics.Analytics` dan `selected`, atau ambil gambaran agregat dengan `snapshot_analytics.collect` dan `project`.

Daripada checkout sumber, bina semua lapan reka bentuk yang disenaraikan di atas daripada jurnal fiksyen yang sama:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Buka `index.html` yang terhasil untuk membandingkan laporan HTML lengkap, PDF yang ditandatangani dan fail ZIP. Setiap reka bentuk menggunakan jurnal sumber yang sama. Gunakan direktori output baharu untuk setiap pelaksanaan supaya contoh yang telah ditandatangani sebelum ini terpelihara.

![Dossier HTML fiksyen](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

HTML dibuka dengan muka depan kes dan tokoh utama. Peta bukti bernombor memautkan kepada setiap penemuan, fakta sokongan, had dan semakan bebas. Rekod yang boleh dicari dan rujukan rekod stabil kekal tersedia dalam pemapar luar talian. Reka bentuk menyesuaikan diri dengan skrin sempit, kedua-dua tema dan pelayar tanpa JavaScript.

PDF yang ditandatangani mempunyai muka depan A4 khusus, rujukan laporan dan QR, ringkasan eksekutif, peta bukti, penemuan bernombor dan penanda halaman dokumen. Header dan footer halaman mengenal pasti laporan. QR mengenal pasti bahan; ia bukan keputusan pengesahan bebas. Cetakan pelayar adalah berasingan daripada PDF yang ditandatangani secara kriptografi ini.

Garis masa pemerhatian meletakkan tempoh pemerhatian yang direkodkan dan gangguan pada paksi UTC yang sama. Ruang kosong tidak dianggap sebagai liputan; jadual terperinci mengekalkan selang yang tepat. Fail ZIP mengandungi laporan yang boleh dibaca, JSON yang ditandatangani, rekod sumber dan arahan pengesahan.

Jana draf baharu fiksyen Bahasa Inggeris/Rusia/Jerman dengan persekitaran pembangunan dipasang:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Setiap direktori bahasa mengandungi `report.html`, `report.pdf`, `report.json` dan `dossier.zip`. Direktori sampel sedia ada tidak pernah dioverwrite. Tiada akaun Telegram, perkhidmatan cap masa luaran atau sambungan rangkaian digunakan untuk menciptanya.

![Tiga muka surat pertama PDF rekaan yang ditandatangani](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Membaca kes konkrit

Untuk jurnal dengan 1,200 entri dan cap masa disahkan pada entri ke-1,000, laporan mengenal pasti 200 entri kemudian yang berada di luar had cap masa tersebut. Ini adalah had atas kewujudan titik pemeriksaan, bukan bukti masa penghantaran setiap mesej. Jika tiga fail cap masa lain gagal pengesahan atau tidak dapat disahkan, ia dikira secara berasingan dan tidak dapat memberikan kesimpulan positif.

Cap masa yang boleh digunakan mesti memenuhi semua semakan ini: jejaknya sepadan dengan titik pemeriksaan, tandatanganannya berantai kepada akar TSA yang dipercayai pada masa dicap, dan tandatangan, kunci, kiraan dan kepala titik pemeriksaan sepadan dengan awalan jurnal yang tepat. Hanya menganalisis cap masa atau mempunyai resit OTS tidak mencukupi. Pembaca mesti memilih akar TSA yang dipercayai secara bebas dan mengulangi pengesahan. OTS memerlukan pemeriksaan pengesahan Bitcoinnya sendiri.

| Status laporan | Maksud |
| --- | --- |
| Disemak semasa eksport | Pengeksport telah menjalankan pemeriksaan yang dinyatakan; pengulangan bebas masih diperlukan. |
| Direkod; semakan diperlukan | Perhatian asas atau pernyataan pengendali direkodkan; ia bukan pengesahan bebas. |
| Tidak disertakan dalam salinan ini | Salinan ini tidak mempunyai artifak sokongan untuk dakwaan ini. Ia tidak menyatakan tiada wujud di tempat lain. |
| Tidak diperiksa secara bebas | Laporan ini tidak menyediakan keputusan pengesahan bebas. |
| Tidak lengkap atau tidak tersedia | Bahan atau pemeriksaan yang diperlukan hilang, tidak lengkap atau tidak berjaya. |

Semak setiap semakan secara berasingan, bersama liputan pengumpulan yang direkodkan.

## Apa yang mesti dipelihara oleh konfigurasi yang kukuh

1. Sebelum bergantung pada pengumpulan, simpan cap jari kunci pengumpul melalui saluran dipercayai berasingan. Bandingkan rujukan itu dengan kunci penandatangan eksport.
2. Pelihara titik pemeriksaan yang dicop waktunya secara bebas dan, jika digunakan, jurnal saksi di luar kawalan pentadbiran pengumpul. Bandingkan dengan jurnal yang dieksport untuk memeriksa sempadannya yang lebih awal.
3. Skop pemerolehan rekod, jurang, penapis, had dan perubahan dalam pengumpulan. Terangkan tempoh yang hilang yang berkaitan dengan tuntutan sebenar, sambil mengekalkan ID mesej yang tidak diperhatikan, notis pemadaman dan semakan semula yang tidak berjaya berasingan.
4. Pelihara ZIP asal dan hash mereka. Catatkan setiap pemegang, pemindahan, tarikh dan tujuan. Simpan kenyataan pengendali yang dikaitkan dan nota kes bersamanya.
5. Untuk VM sulit, pelihara dan sahkan secara bebas petikan, cabaran, rantaian sijil Intel, ukuran, sumber tepat dan syarat pengendalian kunci. Simpan keputusan pengesahan pengakuan bersama artifak yang telah disemak.

See [verification scope](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) for the checks of acquisition， archive integrity，time and collection coverage in each mode．

## Semakan penerima

Gunakan pemasangan TgWitness yang dipercayai dan cap jari yang diperoleh secara bebas:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Fail ZIP saksi mesti diperoleh daripada sumber yang dipercayai secara bebas; pelihara juga kunci dan asal usulnya. Kekalkan arahan, versi alat, keluaran, hashes input yang telah disemak dan soalan yang belum diselesaikan. Pengesahan Beacon adalah pemeriksaan dalam talian yang berasingan; penyaji laporan tidak pernah menghubungi perkhidmatan semata-mata untuk memaparkan laporan.

Untuk pertikaian mengenai mesej tertentu, nyatakan rujukan arkib, fail berkuasa dan rujukan rekod, kemudian terangkan tempoh masa berkaitan, jurang liputan, pemilihan dan bahan pengesahan. Untuk salinan perkongsian, juga semak transformasi yang direkodkan dan rujukannya kepada arkib sumber. Penapis peribadi dan pemetaan identiti kekal di luar penilaian awamnya.

Pengesahan PDF yang ditandatangani mengesan perubahan pada bait yang dilindungi. Simpan fail digital asal dan keputusan pengesahan bersama sebarang tangkapan skrin atau salinan cetak untuk bacaan.
