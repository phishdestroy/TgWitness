# Bukti dan kepercayaan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence-trust/

Apa yang dapat dibuktikan oleh ekspor, video, arsip web, dan catatan yang ditandatangani, serta bagaimana perangkat pengumpul memengaruhi keandalannya.

Ekspor, tangkapan layar, atau rekaman dapat menjadi bukti yang berguna. Keandalannya bergantung pada cara pengumpulan, penyimpanan, dan verifikasinya. **Hash atau tanda tangan yang valid memverifikasi materi yang disimpan; hal tersebut tidak secara independen membuktikan bahwa perangkat pengumpul menerima konten sumber yang sebenarnya.** Batasan ini juga berlaku untuk TgWitness.

Panduan ini memisahkan verifikasi teknis dari penilaian hukum. Dokumentasi produk dan ketentuan hukum di bawah ini telah ditinjau pada 1 November 2026; perbandingan Hunchly menggambarkan dokumentasi yang telah diterbitkan, bukan audit produk baru.

## Di mana kepercayaan berperan dalam proses penangkapan

Diagram alur · Akun dan layanan Telegram → Klien, peramban, dan sistem operasi; Klien, peramban, dan sistem operasi → Ekspor, perekaman video, atau tangkapan layar; Ekspor, perekaman video, atau tangkapan layar → Hash dan tanda tangan pengumpul; Hash dan tanda tangan pengumpul → Hash yang disimpan oleh pihak independen · Akun dan layananTelegram · Klien, peramban, dansistem operasi · Ekspor, perekamanvideo, atau tangkapanlayar · Hash dan tanda tanganpengumpul · Hash yang disimpanoleh pihak independen

**Diagram dalam bentuk teks**

1. Akun dan layanan Telegram → Klien, peramban, dan sistem operasi
2. Klien, peramban, dan sistem operasi → Ekspor, perekaman video, atau tangkapan layar
3. Ekspor, perekaman video, atau tangkapan layar → Hash dan tanda tangan pengumpul
4. Hash dan tanda tangan pengumpul → Hash yang disimpan oleh pihak independen

Model ancaman di sini mengasumsikan bahwa penyerang atau operator dapat mengubah lingkungan pengumpulan sebelum bukti disimpan. Ini adalah analisis bersyarat, bukan klaim bahwa perangkat atau produk tertentu telah disusupi.

Klien resmi dan koneksi terenkripsi membantu melindungi penggunaan normal. Keduanya tidak membuat sistem operasi, peramban, atau tampilan di sekitarnya secara mandiri dapat dipercaya. Jika konten diganti setelah dekripsi tetapi sebelum penangkapan, pengirim dapat menyimpannya secara akurat dan penandatangan dapat menandatanganinya dengan benar. Tidak ada operasi yang memerlukan algoritma hash yang rusak atau tanda tangan palsu.

Sebuah video yang dibuat pada perangkat yang sama dapat merekam tampilan yang telah diganti tersebut. Kamera terpisah dapat mengonfirmasi apa yang ditampilkan layar, tetapi layar itu sendiri tidak mengautentikasi apa yang disediakan Telegram. Demikian pula, HTML, JSON, tangkapan layar, dan log browser yang cocok dari satu lingkungan terkendali mungkin memiliki kesalahan yang sama. Kesesuaian di antara mereka merupakan konteks yang berguna; hal ini tidak secara otomatis menjadi penguatan yang independen.

## Kontribusi masing-masing bentuk bukti

| Materi | Kontribusi yang bermanfaat | Pertanyaan yang tersisa |
| --- | --- | --- |
| Ekspor Telegram Desktop | Percakapan yang dapat dibaca manusia atau mesin serta media yang dipilih | Siapa yang mengontrol file klien dan file ekspor, serta apa saja yang tersedia atau dikecualikan? |
| Tangkapan layar atau rekaman layar | Konteks yang terlihat, urutan tindakan, dan penyajian | Apakah presentasi ini mencerminkan sumber dengan setia, dan apa yang terjadi di luar rekaman? |
| Arsip web lokal, termasuk MHTML | Konten halaman dan sumber daya terkait untuk pemeriksaan selanjutnya | Apa yang disediakan oleh peramban kepada pengarsip, dan siapa yang mengendalikan peramban tersebut? |
| Arsip yang ditandatangani oleh pengumpul | Perubahan pada byte yang ditandatangani dapat dideteksi relatif terhadap kunci tepercaya dan referensi yang dipertahankan | Siapa yang mengendalikan kunci penandatanganan dan input sebelum penandatanganan? |
| Titik pemeriksaan yang disimpan secara independen atau cap waktu yang terverifikasi | Hash atau titik pemeriksaan yang dipertahankan untuk perbandingan dengan pengiriman berikutnya | Byte dan batas mana yang dicakup, dan apa yang sebenarnya disertifikasi oleh pihak independen? |

Telegram mendokumentasikan ekspor Desktop-nya sebagai salinan HTML/JSON offline dan API Takeout-nya sebagai cara untuk mengambil data akun yang dipilih. Deskripsi ini tidak menyediakan tanda tangan Telegram pada arsip akhir yang diekspor agar dapat diverifikasi oleh penerima. Kesimpulan kami terbatas pada mekanisme ekspor yang didokumentasikan tersebut; ini bukanlah klaim bahwa bukti Telegram tidak memiliki nilai hukum.[Ekspor Telegram Desktop](https://telegram.org/blog/export-and-more),[API Takeout](https://core.telegram.org/api/takeout).

Perbedaan yang sama berlaku untuk permintaan latar belakang, entri cache, dan log jaringan. Hal-hal tersebut mungkin mengungkapkan ketidakkonsistenan dan membantu menguatkan suatu pengumpulan. Kompleksitasnya saja tidak menentukan siapa yang menghasilkannya. Arsip yang dioperasikan secara independen atau catatan layanan yang diperoleh secara terpisah memperkenalkan sumber yang berbeda untuk dibandingkan, dengan tunduk pada batasan pengumpulan dan penyimpanannya sendiri.

## Hunchly menggambarkan batas yang sama

Dokumentasi Hunchly menjelaskan hashing SHA-256 untuk tangkapan MHTML, foto, dan lampiran, dengan verifikasi hash independen. Dokumentasi tersebut juga menjelaskan mengapa file yang diubah yang disertai dengan hash yang baru dihitung dapat lolos perbandingan tersebut, serta menunjuk pada tanda tangan dan verifikasi sumber sebagai pemeriksaan tambahan.[Hunchly: hashing konten, foto, dan lampiran](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

*Panduan Bukti* yang diterbitkannya, revisi 1.0 tanggal 17 Oktober 2018, menjelaskan kunci GPG dan tanda tangan yang dihasilkan secara lokal untuk penangkapan MHTML. Panduan tersebut secara eksplisit mengidentifikasi akses ke kunci pribadi lokal sebagai cara untuk menandatangani kembali materi yang dimodifikasi. Ini adalah batasan kepercayaan yang terdokumentasi, bukan bukti adanya eksploitasi saat ini yang tidak diungkapkan. Panduan tersebut juga menyebutkan bahwa Chrome melakukan penangkapan MHTML. Menggambarkan Hunchly sebagai hanya mengandalkan reputasi penyelidik akan mengabaikan kontrol teknis ini.[Panduan Bukti Hunchly, bagian 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

Apakah materi yang dikumpulkan dengan produk tertentu telah diterima dalam suatu kasus tergantung pada keputusan dan keadaan yang relevan. Kami tidak membuat klaim apa pun di sini mengenai seberapa sering pengadilan menerima Hunchly atau TgWitness, atau mengenai apakah salah satu produk tersebut memiliki persetujuan umum dari pengadilan.

## Apa yang ditambahkan oleh TgWitness, dan di mana batas perlindungannya

TgWitness mencatat pengamatan dalam jurnal yang ditandatangani dan tertaut serta menyediakan ekspor yang dapat diverifikasi oleh penerima. Titik pemeriksaan yang disimpan, cap waktu, dan saksi terpisah memberikan referensi kepada peninjau di luar berkas-berkas pengumpul saat ini. Hal ini membantu mengungkap perubahan pada catatan yang telah disimpan sebelumnya. Catatan cakupan dan hasil pengumpulan yang eksplisit membantu menjelaskan apa yang terekam dan apa yang tidak.[Format bukti dan penyerahan](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/), [ruang lingkup pengumpulan](https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/).

Waktu penggantian yang mungkin dilakukan sangat penting:

1. **Setelah penandatanganan, tanpa akses ke kunci penandatanganan:** mengubah catatan yang telah ditandatangani atau berkas yang terikat pada manifes akan gagal verifikasi dengan verifikator tepercaya dan kunci.
2. **Dengan kunci pengumpul, setelah titik pemeriksaan independen disimpan:** sebuah jurnal pengganti dapat memiliki tanda tangan baru yang valid, tetapi awalan yang diubah akan gagal dibandingkan dengan titik pemeriksaan sebelumnya. Titik pemeriksaan yang hanya disimpan pada perangkat terkontrol yang sama dapat diganti bersamaan dengan jurnal tersebut. Catatan di luar batas yang disimpan memerlukan cakupan tersendiri.
3. **Sebelum titik pemeriksaan yang mencakup suatu pengamatan disimpan secara independen:**input yang salah dapat ditandatangani dan diikat dengan sukses, termasuk catatan baru yang ditambahkan setelah titik pemeriksaan sebelumnya. Titik pemeriksaan atau cap waktu yang dihasilkan masih mencakup catatan-catatan yang salah tersebut; hal itu tidak membuktikan kebenarannya.

Seorang saksi TgWitness menerima titik pemeriksaan yang ditandatangani oleh pengumpul; ia tidak secara mandiri membaca percakapan Telegram yang mendasarinya. Kunci dan catatan yang disimpannya harus dipercaya secara terpisah. Ketika seluruh jurnal yang dikirimkan harus disaksikan, gunakan[prosedur serah terima yang mensyaratkan batas ekspor akhir](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/#require-a-witnessed-export-boundary). Proses integritas biasa masih dapat melaporkan bagian akhir yang tidak disaksikan.

Respons RFC 3161 yang terverifikasi dapat mendukung bahwa titik pemeriksaan (checkpoint) telah ada pada waktu yang dinyatakan oleh otoritas. Hal ini tidak membuktikan kapan pesan Telegram dikirim atau apakah isinya benar. Permintaan yang disiapkan atau berkas respons yang disertakan saja tidak cukup. Saat memverifikasi ekspor dengan `tgwitness.verify`, memeriksa tanda tangan TSA yang disertakan memerlukan CA yang secara eksplisit tepercaya melalui `--tsa-ca`. Bukti OpenTimestamps memerlukan verifikasi independen `ots verify`, dengan peningkatan bukti jika diperlukan. [Prosedur cap waktu](https://phishdestroy.github.io/TgWitness/id/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

Dalam [penangkapan GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), sebuah runner yang dihosting sementara mengumpulkan pesan-pesan tersebut. Attestation mengikat arsip ke alur kerja yang disetujui. Mode ini masih mempercayai GitHub, perangkat lunak dan dependensi yang disetujui, helper/browser, serta terowongan. Ini bukanlah perangkat keras rahasia, tanda tangan Telegram, atau bukti bahwa tidak ada yang mengakses host. Tanda terima eksekusi yang ditandatangani secara lokal juga merupakan pengukuran yang dilaporkan sendiri, bukan attestation perangkat keras.

## Bobot hukum bergantung pada landasannya

Empat pertanyaan harus tetap dibedakan: apakah item tersebut sesuai dengan yang diklaim, apakah byte yang dikirimkan cocok dengan catatan yang disimpan, apakah kontennya mendukung fakta yang diklaim, dan apakah aturan yang berlaku mengizinkan penggunaannya. Pemeriksaan kriptografi hanya mencakup sebagian dari dasar tersebut.

Dalam proses hukum federal AS, Aturan 901 mengatur cara-cara untuk mengautentikasi bukti, termasuk kesaksian saksi yang berpengalaman dan bukti mengenai suatu proses atau sistem. Aturan 902(13) dan 902(14) menyediakan jalur sertifikasi untuk catatan elektronik dan salinan tertentu, dengan persyaratan prosedural. Catatan komite mereka membedakan otentikasi dari masalah seperti kabar angin, relevansi, dan atribusi. Tanda tangan perangkat lunak saja bukanlah sertifikasi dari pihak yang berkualifikasi sebagaimana dijelaskan di sana.[Aturan Bukti Federal 901](https://www.law.cornell.edu/rules/fre/rule_901),[Aturan Bukti Federal 902](https://www.law.cornell.edu/rules/fre/rule_902).

Di mana Undang-Undang Bukti Kanada berlaku, pasal 31.1 mengatur otentikasi dokumen elektronik. Pasal 31.2 mengaitkan aturan bukti terbaik dengan integritas sistem atau anggapan yang berlaku; pasal 31.3 menetapkan keadaan untuk anggapan integritas. Ini adalah ketentuan pembuktian yang didefinisikan, bukan anggapan umum bahwa setiap penyelidik berlisensi atau produk komersial tidak pernah salah. [Undang-Undang Bukti Kanada, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Contoh-contoh ini tidak menentukan kelayakan di yurisdiksi lain atau kasus tertentu. Pemeriksaan teknis harus diterapkan secara konsisten terhadap materi yang mendukung atau menentang suatu tuduhan. Panduan ini tidak menyatakan bahwa bukti penuntutan secara umum lebih mudah diterima daripada bukti pembelaan.

## Siapkan catatan yang dapat dievaluasi oleh orang lain

- Jelaskan akun, perangkat pengumpulan, operator, versi perangkat lunak, hak akses, ruang lingkup yang dipilih, dan periode pengumpulan. Catat gangguan dan kemungkinan kompromi, alih-alih menganggap pemeriksaan tanda tangan yang berhasil sebagai uji perangkat yang bersih.
- Pertahankan paket asli dan catat transfer, hash, serta sumber waktu. Pertahankan sidik jari kunci dan titik pemeriksaan melalui saluran tepercaya yang terpisah. Verifikasi saksi aktual atau cakupan cap waktu sebelum menjelaskannya dalam laporan.
- Carilah pembuktian independen yang sesuai dengan klaim tersebut: catatan peserta lain, rekaman independen, atau catatan layanan yang diperoleh secara sah. Jelaskan kemandirian dan keterbatasannya; kesesuaian antara salinan saja tidak cukup.
- Pertahankan konteks yang relevan. Identifikasi berkas yang dihilangkan, riwayat yang tidak tersedia, dan bagian yang disunting. Siapkan [pengungkapan terpisah yang disederhanakan](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)jika diperlukan, dan jelaskan transformasinya tanpa menyajikannya sebagai versi asli yang lengkap.
- Berikan petunjuk verifikasi kepada penerima serta materi yang diperlukan untuk pemeriksaan tersebut. Pastikan pengamatan, temuan teknis, dan kesimpulan analis dapat dibedakan dengan jelas.

Untuk serah terima tertentu, sebutkan hash arsip, kunci tepercaya, hasil verifikasi, dan batas eksternal yang tercakup secara tepat. Jelaskan keaslian sumber, atribusi akun, kelengkapan, dan kesimpulan hukum secara terpisah. Hal ini memberikan klaim spesifik kepada peninjau berikutnya untuk diperiksa.
