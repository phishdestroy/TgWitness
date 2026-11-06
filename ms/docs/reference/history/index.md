# Muat sejarah sumber

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/

Muat mesej lepas daripada sumber yang diaktifkan, berehat dan sambung semula, serta sahkan laporan kemajuan yang ditandatangani.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Koleksi](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Koleksi](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

Dalam **Sumber**, semak sembang yang diaktifkan, hentikan pemerhatian, pilih API Standard atau eksport Takeout, kemudian pilih **Muat Sejarah Penuh**. Jalannya menetapkan senarai sumber tersebut dan membaca mesej laluan mereka yang tersedia ke dalam Sembang dan jurnal pemerhatian yang ditandatangani. Media menggunakan tetapan lampiran sedia ada dan barisan muat turun tahan lama. Ini berasingan daripada eksport JSON/HTML yang ditandatangani bagi setiap sembang.

Untuk pengumpulan merentas akaun, pilih **Whole account**, mulakan pemerhatian untuk memuatkan senarai sumbernya, dan semak senarai tersebut sebelum memulakan sejarah. Had senarai dialog masih terpakai (1,000 secara lalai, boleh dilaras dalam Parameter). Pelaksanaan yang berjaya tidak membuktikan bahawa setiap dialog akaun telah disenaraikan. Perbualan yang ditemui atau diaktifkan kemudian memerlukan pelaksanaan semula. Hentikan pemerhatian sebelum memulakan sejarah; satu pengambilan hanya boleh memiliki satu akaun pada satu-satu masa.

Pilih satu hingga lima pekerja lampiran dan sama ada untuk mengekalkan Tindakan Baru yang tersedia dan membandingkan versi yang disimpan sebelum ini. Takeout mungkin memerlukan kelulusan di Telegram dan tempoh menunggu yang ditetapkan oleh pelayan. Pilihan ini kekal tetap apabila disambung semula. Lihat [tingkah laku Backfill dan kontrak bukti](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) untuk butiran pengangkutan, percubaan semula dan kepercayaan.

## Pause, mula semula dan keputusan separa

- **Sejarah rehat** menghentikan pembacaan. **Sambung sejarah** akan diteruskan dari mesej terakhir yang disimpan dalam setiap sumber; memulakan semula aplikasi juga akan mengekalkan pelaksanaan dalam keadaan rehat sehingga disambung semula. Untuk menyambung semula, akaun Telegram yang tidak aktif yang sama diperlukan.
- Pengamatan mesej, pemprosesan lampiran dan komitmen penunjuk dalam satu transaksi. Jalankan semula tidak akan mengulangi pengamatan yang telah dikomit. Rakaman langsung atau jalankan berasingan yang dimulakan secara eksplisit boleh memerhati mesej yang sama secara bebas.
- Setiap sumber (setiap julat pecahan Telegram dalam Takeout) menetapkan ID mesej teratas pada bacaan pertamanya. Mesej yang lebih baru tergolong dalam pemerhatian langsung, bukan pada halaman bersejarah sumber tersebut yang tinggal.
- Sumber yang tidak dapat diakses dan sumber yang dilumpuhkan semasa pengambilan kekal kelihatan sebagai gagal atau dilangkau. Sumber lain diteruskan; keputusan keseluruhan tidak lengkap.
- Penangguhan FloodWait menghormati selang menunggu semula akaun yang disimpan. Kegagalan sementara mencuba semula sehingga lima kali; apabila habis atau ruang cakera rendah, ia berehat dengan penunjuk kekal utuh.
- **Menamatkan larian sejarah ini** mengekalkan pemerhatian yang disimpan. Ia tidak memadamnya atau membatalkan tugas lampiran API standard. Menamatkan Takeout menandakan fail Takeout yang tinggal sebagai dilangkau; menghentikan mengekalkan kebolehterusan semula. Larian baru membaca sumber yang diaktifkan semula.

Penyempurnaan sejarah menerangkan bacaan sejarah sahaja. Lampiran mungkin kekal menunggu, gagal, atau dikecualikan oleh dasar yang dikonfigurasikan. Semak resit media dalam jurnal dan barisan menunggu lampiran; hanya resit yang disempurnakan dengan bait yang terpelihara dianggap sebagai lampiran yang disimpan. Operasi sejarah adalah permintaan snapshot eksplisit dan berasingan daripada suis yang memilih kategori acara langsung akan datang.

## Pindahkan dan sahkan

Simpan **laporan kemajuan yang ditandatangani**, kemudian gunakan **Eksport bukti** untuk memuat turun jurnal dan lampiran yang disimpan. Eksport bukti kemudian mungkin termasuk rekod tambahan; laporan ini mengikat pengiraannya kepada awalan jurnal pada masa ia dibuat. Jalankan pengesah daripada tarikan semak yang dipercayai bagi versi ini:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Simpan cap jari kunci tandatangan yang dijangka secara berasingan. Pengesah memeriksa tandatangan laporan, arkib bukti, titik pemeriksaan laporan, pelan sumber, akaun dan kiraan mesej yang disimpan/tidak tersedia. Jalankan baharu juga mengikat kemajuan sumber dan pilihan kepada acara penunjuk yang ditandatangani. Tanpa `--evidence`, ia hanya memeriksa laporan yang ditandatangani dan keserasian dalamannya. Medan kemajuan warisan dan ringkasan lampiran kekal sebagai kenyataan pengumpul yang ditandatangani. Pengesah bukti memeriksa bait media yang diarkibkan.

Memerak atau menamatkan sejarah yang tersedia tidak membuktikan asal Telegram, snapshot atomik, atau kelengkapan sejarah. Mesej boleh berubah semasa dibaca; mesej yang dipadam dan suntingan pertengahan di luar Tindakan Baru-baru Ini yang tersedia dan Perbualan Rahsia tidak dapat dipulihkan. Seorang pengendali yang mengawal kunci penandatanganan boleh mencipta jurnal sebelum komitmen luaran wujud. Gunakan titik pemeriksaan yang disimpan secara berasingan atau saksi bebas untuk sifat pengesanan pengubahsuaian yang didokumenkan.

Penunjuk pemerolehan adalah status ruang kerja tempatan. Memulihkan ZIP bukti sahaja tidak memulihkan kerja pemerolehan yang tertangguh atau sesi Telegram. Simpan sandaran ruang kerja jika sambungan kerja asal diperlukan.
