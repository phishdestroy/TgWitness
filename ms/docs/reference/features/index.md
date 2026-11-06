# Telegram · Ciri dan had

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/

Model pengumpulan semasa, aliran kerja berbilang akaun, eksport dan sempadan operasi TgWitness.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Rujukan projek](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Rujukan projek](https://phishdestroy.github.io/TgWitness/assets/chapter-project.svg)

TgWitness mengekalkan perbualan Telegram yang boleh diakses oleh akaun yang disambungkan, merekod perubahan yang diperhatikan dan menyediakan eksport yang boleh disahkan. Rujukan ini menerangkan model pengumpulan, aliran kerja semasa dan sempadannya.

**Pada halaman ini**

- [Aplikasi berdiri sendiri](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#standalone-application)
- [Siasatan bersama](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#shared-investigations)
- [Alat arkib](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#archive-tools)
- [Tambahan pilihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#optional-extras)
- [Protokol dan sumber peribadi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#protocol-and-private-sources)
- [Beberapa akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#multiple-accounts)
- [Perekodan dan atribusi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#capture-and-attribution)
- [Kapasiti dan had Telegram](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#capacity-and-telegram-limits)
- [Kebolehpercayaan dan pemulihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#reliability-and-recovery)
- [Model bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#evidence-model)
- [Eksport, penyebaran dan penyerahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#export-deployment-and-handoff)
- [Kriteria keluaran stabil](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/#stable-release-criteria)

## Aplikasi berdiri sendiri

TgWitness mempunyai pemasangan, direktori data, dan kitaran hayat keluaran tersendiri. Antaramuka web terbina dalam mengendalikan penyediaan dan semakan; rekod yang dieksport boleh digunakan secara bebas.

Pengendali menyambungkan akaun mereka, memilih sumber yang boleh dilihat oleh setiap akaun, dan mendapatkan jurnal pemerhatian yang disimpan. Panel memaparkan kandungan, perubahan yang disimpan, asal-usul pemerhatian dan kekosongan yang diketahui. Penyiasat lain boleh mengesahkan bahan yang dieksport.

Panel membezakan pengesahan akaun, akses kepada sumber, aktiviti pengumpul dan liputan yang direkodkan. Semak keadaan-keadaan tersebut secara bersama apabila menilai selang dengan sedikit mesej atau masalah sambungan.

## Siasatan Bersama

Pentadbir boleh mengeluarkan [token akses](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/) yang terhad kepada ruang kerja dan sembang individu, dengan kebenaran bagi setiap tindakan, sekatan IP, tamat tempoh, had log masuk dan kawalan sesi. Pemeriksa baca sahaja boleh memeriksa kes tanpa menerima kebenaran Telegram atau kunci panel utama. Akses terhad kepada sembang kekal berasingan daripada tetapan seluruh akaun dan eksport jurnal penuh.

MTProxy automatik mengekalkan laluan Telegram berfungsi daripada empat sumber awam atau katalog pengendali. [Mod IP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes) menentukan sama ada kegagalan perlu menunggu proksi lain atau boleh menggunakan laluan terus yang dibenarkan secara eksplisit. Permintaan HTTP luaran mempunyai laluan berasingan dan suis mati.

## Alat arkib

[Pendapatan sejarah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/), [carian arkib dan analisis](https://phishdestroy.github.io/TgWitness/ms/docs/reference/analysis/), [MCP baca sahaja](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/), [OCR/transkripsi tempatan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/media-analysis/) dan [webhook keluaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/webhooks/) disertakan dalam 0.7.1. Laporan analitik dan teks yang diiktiraf kekal berasingan daripada peristiwa yang dirakam.

[Case Board](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-board/) menambah penanda buku, petikan, nota dan koleksi yang dipautkan kepada sumber dalam ruang kerja. [Pembina](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/) [laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/) memilih bahan, seksyen dan salah satu daripada lapan reka bentuk untuk eksport HTML/PDF yang disokong.

## Tambahan pilihan

Setup harian ialah akaun → sumber → pemerhatian. **Ekstra** ialah destinasi berasingan dengan bot saksi Telegram dan pratonton tangkapan GitHub. Setiap satunya menyatakan ketersediaan dan keperluan sebelum memaparkan tetapan. Memilih kad membuka arahan; ia tidak mendaftar atau memulakan perkhidmatan.

Pengesanan bot mempunyai tiga langkah: cipta akses baca sahaja, pilih tetapan penerbitan, dan lancarkan pada hos saksi. Pilihan rangkaian dan penerbitan, sambungan sedia ada dan perintah pengesahan didedahkan atas permintaan. Konfigurasi yang dimuat turun berbeza daripada saksi yang sedang berjalan. Menukar extras mengekalkan draf; perubahan akaun dan penguncian membersihkan token dan borang sementara. Panduan terbina dalam merangkumi arahan pelancaran. [GitHub Actions menangkap](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) pelancaran pengumpul yang dipin dari fork anda, menangkap satu sembang dan menghasilkan penyerahan terenkripsi dengan asal usul aliran kerja.

## Protokol dan sumber peribadi

**MTProto ialah protokol Telegram; Telethon ialah perpustakaan Python yang digunakan oleh TgWitness untuk berkomunikasi dengan MTProto.** Mereka bukan kaedah sambungan alternatif. Pengumpulan menggunakan MTProto; saksi pilihan menerbitkan semakan berasingan yang disahkan melalui Bot API.

Setiap ruang kerja mempunyai aliran kemas kini klien dan akaun yang dibenarkan sendiri. TgWitness memilih pemerhatian daripada sumber yang dikonfigurasikan dan membuat permintaan eksplisit berasingan untuk fungsi seperti potret sejarah dan muat turun media.

Sumber peribadi tidak memerlukan nama pengguna awam. Jenis rakan Telegram dan ID numerik adalah pengecam; tajuk dan nama pengguna boleh berubah. Akses bergantung pada keahlian dan kebenaran sedia ada. TgWitness tidak secara automatik menyertai sumber atau memintas kelulusan penyertaan. Hash akses daripada akaun lain bukan token akses sejagat.

Model pengumpulan mesti mengambil kira sejarah tersembunyi sebelum menyertai, peranan peserta/pentadbir, pembatalan sesi, penghapusan atau perubahan kebenaran, migrasi daripada kumpulan ke superkumpulan, topik/forum, perbincangan yang dipautkan, identiti saluran dan lampiran yang tidak tersedia. Tidak semua kombinasi telah diuji secara langsung.

Visibiliti sumber diperiksa semasa permulaan pengumpul. Ketiadaan sumber daripada dialog terhad bermakna **akses tidak disahkan**, bukan pembuangan yang terbukti. Satu sumber yang tidak tersedia tidak menghalang pemerhatian terhadap sumber lain yang boleh diakses. Jangan sekali-kali meletakkan pautan jemputan atau sesi sebenar dalam infrastruktur awam.

## Beberapa akaun

Panel ini menyokong sebarang bilangan **ruang kerja**, setiap satu dengan:

- Autorisasi, peti besi disulit dan laluan sambungan.
- Jurnal SQLite dan identiti tandatangan Ed25519.
- Sumber terpilih, barisan media dan tetapan tangkapan.
- Status pemerhatian, ralat, titik pemeriksaan dan eksport.

Menukar ruang kerja yang dipaparkan tidak menghentikan pengumpul lain. Pengesahan akaun dwi di merentasi ruang kerja ditolak. Jurnal yang sudah diikat dengan satu akaun Telegram tidak boleh ditugaskan semula kepada akaun lain; menyambung semula akaun yang sama dibenarkan. Ini mengekalkan identiti akaun dan skop ID-mesej yang berkaitan.

Aplikasi ini tidak menetapkan bilangan ruang kerja tetap. Setiap ruang kerja menjalankan tugas pengumpulnya sendiri untuk pemantauan sambungan, muat turun media, semakan semula dan pengambilan sembang baru dalam proses Python dan gelung acara yang dikongsi. Kelajuan pemprosesan bergantung pada beban kerja. Untuk pengasingan proses, gunakan pemasangan, port dan direktori data yang berasingan.

Tugaskan setiap akaun sumber yang boleh diaksesnya. Akaun yang berbeza mungkin memerhati kumpulan yang sama, tetapi pemerhatian mereka kekal berasingan dan mengekalkan asal usulnya. Dua akaun pada satu mesin yang dikawal oleh pengendali bukanlah dua saksi bebas. **Eksport kumpulan** membundelkan ZIP ruang kerja yang ditandatangani secara berasingan dengan senarai fail yang ditandatangani yang mengandungi ID ruang kerja, hash dan cap jari kunci penandatanganan mereka. Setiap jurnal mengekalkan sempadannya sendiri. Bina garis masa merentas ruang kerja gabungan dalam nota kes atau alat analisis, sambil mengekalkan rujukan sumber tersebut.

## Perekodan dan atribusi

Sumber menyediakan suis bagi setiap akaun untuk mesej baru, suntingan, pemadaman, reaksi dan keahlian. Tetapan lalai mengekalkan sama ada semua kategori atau mesej/suntingan/pemadaman. Dasar ini terpakai kepada kumpulan terpilih di ruang kerja, kekal selepas mula semula, dan disahkan dengan perubahan sebelum/selepas. Lalai mengekalkan semua kategori. Memadam kategori tidak akan membuang rekod lama; mengaktifkannya semula tidak akan membina semula peristiwa yang terlepas. Rekod operasi, peristiwa perkhidmatan kumpulan lain dan potret sejarah eksplisit adalah berasingan. Objek Telegram yang dirakam mungkin mengekalkan metadata terbenam tanpa mengira suis kemas kini berasingan. Belum ada keutamaan kategori mengikut kumpulan.

| Bahan | Direkod sekarang | Batas |
| --- | --- | --- |
| Mesej | Teks, ID rakan/mesej, metadata penghantar, balasan dan sampul kemas kini asal | Dipelihara sebagai pemerhatian yang boleh dilihat oleh akaun dan ditandatangani oleh pengumpul |
| Sunting | Versi baharu yang diperhatikan dan mana-mana versi yang telah disimpan sebelum ini | Suntingan pertengahan semasa waktu henti boleh hilang; penghantar tidak semestinya penyunting |
| Pembuangan | Notifikasi dan kandungan yang telah dirakam sebelum ini, jika ada | Biasanya tiada maklumat tentang penghapus atau masa tindakan tepat |
| Notis pemadaman peringkat akaun | Notis asal; rekod yang diselesaikan merangkumi sembang yang disimpan dan kaedah korelasi | Memerlukan tepat satu padanan sembang peribadi atau kumpulan biasa yang telah disimpan sebelum ini dalam skop; ID lain kekal `deletion.unscoped`. ID saluran dan superkumpulan dikecualikan daripada korelasi ini |
| Reaksi | Pengira semula yang dihantar dan identiti terkini yang dapat dilihat | Senarai reaktor lengkap yang tersedia memerlukan pertanyaan berasingan; saluran mungkin menyembunyikan identiti |
| Keahlian | Mesej perkhidmatan dan kemas kini peserta yang dihantar | Kelihatan bergantung pada peranan dan jenis sembang; peristiwa yang hilang tidak membuktikan ketiadaan |
| Tindakan pentadbir | Kemas kini yang berkaitan telah disampaikan dan snapshot log pentadbir dalam eksport sembang saluran/superkumpulan | Eksport membaca log apabila tersedia untuk akaun pentadbir yang mengeksport; pemantauan log pentadbir secara berterusan berada di luar aliran kerja ini |
| Lampiran | Deskriptor versi asal, bait yang dimuat turun/SHA-256 dan keputusan percubaan | Fail yang hilang mungkin tidak dapat dipulihkan; versi terkini tidak digantikan |
| Sejarah | Sneak peek eksplisit mesej yang kini kelihatan | Tidak membina semula semua suntingan atau kandungan yang dipadam |
| Proses pengumpul | Mula/henti, degupan jantung, ralat, tetapan, skop dan resit larian bertandatangan | Inventori tempatan; GitHub dan TDX menambah [pemeriksaan persekitaran bebas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) |

Antaramuka menamakan akaun yang dibekalkan dalam peristiwa sumber dan mengekalkan nama pemerhatian dan nama pengguna. Apabila peristiwa itu tidak menyertakan pelakunya, laporan tersebut membiarkan medan itu tidak ditentukan.

## Kapasiti dan had Telegram

Tiada bilangan sembang sejagat yang boleh dipantau dengan kualiti terjamin. Kapasiti bergantung pada acara puncak per saat, volum dan saiz lampiran, RPC tambahan, akaun aktif, kelewatan/ruang kosong cakera, keadaan rangkaian, had Telegram, kelewatan yang boleh diterima dan kedalaman barisan.

Telegram membezakan penghantaran pasif daripada tinjauan pendek aktif. Dokumentasi kemas kini menerangkan panggilan tambahan `updates.getChannelDifference` untuk saluran terbuka/superkumpulan dan mengesyorkan paling banyak **sepuluh sumber yang ditinjau pendek serentak**. Ini bukan had sepuluh kumpulan terpilih atau jaminan kelengkapan.

| Mod | Tujuan | Status |
| --- | --- | --- |
| Pemerhatian standard | Merekod kemas kini yang disampaikan daripada sumber terpilih | Dipelaksanaan |
| Semakan semula keutamaan | Sumber yang diberi bintang menggunakan selang yang boleh dikonfigurasi sendiri dan diutamakan dalam setiap kitaran semakan semula terhad | Dilaksanakan dengan pertanyaan sejarah dan mesej |

Bintang keutamaan mengawal semakan semula ini. Pemanggilan pantas tambahan `updates.getChannelDifference` tidak didedahkan sebagai mod pengguna berasingan.

Pemeriksaan kekerapan tinggi sewenang-wenangnya, mengabaikan FloodWait atau menganggap kapasiti linear daripada akaun tambahan bukanlah model saiz yang sah. Had lalai ialah 1,000 dialog yang disenaraikan pertama, sehingga 500 mesej setiap potret sejarah, 1–2,000 MiB bagi setiap fail yang dikumpul mengikut jenis, dan 4 GiB kandungan ZIP yang ditandatangani tanpa pemampatan; setiap satu diubah mengikut ruang kerja di bawah **Parameter**. Eksport tiada had tetap bilangan acara. Fallback pelayar terhad kepada 128 MiB secara lalai; CLI penstriman mempunyai had pemindahan yang boleh dikonfigurasi, iaitu 5 GiB secara lalai.

## Kebolehpercayaan dan pemulihan

Perilaku yang dilaksanakan merangkumi transaksi SQLite WAL/sinkron; penulisan atomik mesej dan tugas media; tugas berterusan dan kelewatan percubaan semula; deskriptor versi asal; cubaan semula terhad; FloodWait media yang disimpan; muat turun media di luar masa tunggu rangkaian acara teks; eksport awalan-tetap sementara penulisan kemudian diteruskan; tetapan atom dan rekod audit; pemeliharaan kebenaran bekerja selepas log masuk penggantian yang gagal; penyusunan ruang kerja tambahan yang rosak; percubaan penyambungan semula secara eksplisit; pelaporan kehilangan kebenaran yang berasingan; dan pengesanan perubahan masa dinding menggunakan jam monotonik.

Posisipts/qts/seq akaun dan saluran disimpan dan disambung semula selepas but semula, dan sembang yang diperhatikan disemak semula secara berkala; lihat [format bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#durable-collection-and-process-receipts-02). Penyimpanan posisi secara berkala bukanlah pengesahan atomik tanpa kehilangan yang menjamin penerimaan jurnal.

Setiap permulaan proses merekodkan kepala sebelumnya dan sempadan luar talian. Sejarah semasa tidak dianggap sebagai pembaikan jurang. Penahanan perbezaan Telegram adalah terhad; `differenceTooLong` tidak dapat membina semula semua kandungan yang hilang. Jurang yang tidak dapat dipulihkan mesti kekal nyata walaupun potret sejarah kemudian berjaya.

## Model bukti

Setiap peristiwa merekodkan urutan, masa pemerhatian tempatan UTC, masa sumber jika disediakan, jenis, sumber, pelaku jika disediakan, muatan asal, hash sebelumnya dan tandatangan. Pemerhatian mesej juga mengekalkan konteks akaun/jalanan pengumpul.

Resit proses yang disahkan mengandungi ID larian rawak; versi TgWitness/Python/OS/kebergantungan; nilai SHA-256 fail sumber dan cap jari agregat; akaun awal, skop dan tetapan; bacaan UTC/monotonik; dan kepala jurnal sebelumnya. Perubahan tetapan, permulaan/pemberhentian dan ralat dimasukkan ke dalam jurnal yang sama. Titik pemeriksaan dikekalkan semasa permulaan, setiap lima minit semasa pemerhatian (boleh diubah), dan semasa pemberhentian yang teratur. Titik pemeriksaan tempatan yang dikekalkan boleh mengesan pengunduran ke prefiks jurnal yang lebih awal.

| Mekanisme | Apa yang ditetapkan |
| --- | --- |
| Fail SHA-256 | Byte-byte sepadan dengan digest yang diketahui |
| Rantaian hash acara | Perekodan pengurutan/pautan berbanding sempadan yang diketahui |
| Ed25519 | Tandatangan di bawah kunci tertentu |
| Pemeriksa bebas yang disimpan secara berasingan | Bahan kemudian selari dengan sempadan yang dikekalkan |
| Pengukuran fail program | Laporan kendiri pengumpul mengenai fail yang diukur |
| Tindak balas TSA bebas yang sah | Wujudnya bait tertentu pada masa TSA di bawah andaian kepercayaan eksplisit |

Persiapan permintaan RFC 3161 dan pengesahan respons OpenSSL telah dilaksanakan. Mod bukti juga menghantar hashes titik pemeriksaan kepada perkhidmatan cop masa yang dikonfigurasikan. Simpan dan sahkan respons pihak berkuasa untuk menetapkan penanda masa bebas. Lihat [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/).

Simpan titik pemeriksaan secara berasingan, kawal akses kepada kunci penandatanganan, simpan rekod pemindahan dan sahkan eksport dengan perisian yang dipercayai. [Skop](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) [pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) menerangkan bagaimana pemeriksaan tersebut saling melengkapi dan andaian kepercayaan yang terpakai.

## Eksport, penyebaran dan penyerahan

Fail ZIP yang disahkan mengandungi JSONL asal, CSV, HTML, lampiran yang dipelihara, hash, manifes yang disahkan dan pengesah ringkas. Ia merangkumi satu ruang kerja dan awalan jurnal penuh yang tetap. Penapis carian panel tidak membuang rekod secara senyap. Kunci rahsia, token dan sesi Telegram dikecualikan; pemerhatian asal masih boleh mengandungi maklumat peribadi dan metadata Telegram.

Simpan digest ZIP, cap jari dipercayai, titik pemeriksaan, resit proses dan rekod penyerahan secara berasingan. Gunakan pengesah daripada pemasangan yang dipercayai, bukannya mempercayai kod boleh lajak semata-mata kerana ia terdapat dalam ZIP yang diperiksa.

Antaramuka pelayar dipasang secara tempatan tanpa Node.js, CDN atau fon luaran. Satu token pengendali mengawal pemasangan. Akses jauh memerlukan HTTPS atau terowong SSH. Definisi Python asli dan kontena disediakan, dengan contoh perkhidmatan di bawah [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); pemeriksaan platform yang dijalankan disenaraikan secara berasingan.

Ruang kerja lalai menggunakan akar data; ruang kerja tambahan menggunakan `profiles/<id>/`. Sandaran memerlukan proses yang dihentikan dan set data/kunci lengkap. ZIP bukti bukan sandaran aplikasi. Rahsia boleh menggunakan kunci induk luaran untuk direktori data baru; penyulitan jurnal/media disediakan oleh cakera/jumlah operator. Lihat [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) dan [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/operations/).

## Kriteria keluaran stabil

Sebelum pelepasan stabil, nyatakan:

1. Kumpulan peribadi sebenar, superkumpulan, forum dan saluran dengan peranan ahli/pentadbir dan sejarah tersembunyi/terlihat, termasuk log masuk/2FA, pembatalan dan kehilangan akses.
2. Suntingan terkawal, pemadaman, reaksi, keahlian dan media terhadap tindakan yang diketahui.
3. Kegagalan proses/hos, kegagalan cakera/cakera penuh, rujukan fail tamat tempoh, FloodWait, kehilangan rangkaian, fail rosak dan rollback pangkalan data.
4. Penggunaan berbilang akaun berterusan dengan kelewatan terkawal, barisan, memori dan cakera, termasuk sumber senyap dan bising bersama-sama.
5. Gangguan antara kemajuan status MTProto dan penerimaan jurnal.
6. Pemasangan bersih pada matriks OS/kontena yang dimaksudkan dan pemulihan sandaran yang disahkan.
7. Pemeriksaan bebas terhadap keselamatan, tandatangan dan dakwaan atribusi/bukti.

Akses panel terhad diterangkan dalam [Akses dan Kebenaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/). Versi 0.6 menyokong TData akaun tunggal terhad dan import fail-akaun yang diterangkan dalam [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/). Semak terma API Telegram sebelum penerbitan. Rujukan penyelidikan dan penemuan platform terdapat dalam [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
