# Muat sejarah sumber

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/

Muat mesej lepas daripada sumber yang diaktifkan, berehat dan sambung semula, serta sahkan laporan kemajuan yang ditandatangani.

**Utama semasa:** tersedia dari sumber; tidak disertakan dalam pratonton mudah alih 0.7.0.

Dalam **Sumber**, semak sembang yang diaktifkan, mulakan pemerhatian, kemudian pilih **Muat Sejarah Penuh**. Proses ini menetapkan senarai sumber tersebut dan membaca mesej laluan mereka yang tersedia ke dalam Sembang dan jurnal pemerhatian yang ditandatangani. Media menggunakan tetapan lampiran sedia ada dan barisan muat turun tahan lama. Ini berasingan daripada eksport JSON/HTML yang ditandatangani bagi setiap sembang.

Untuk pengumpulan seluruh akaun, pilih **Keseluruhan akaun**, mulakan pemerhatian untuk memuatkan senarai sumbernya, dan semak senarai tersebut sebelum memulakan sejarah. Had senarai dialog masih terpakai (1,000 secara lalai, boleh dilaras dalam Parameter). Jalankan yang berjaya tidak membuktikan bahawa setiap dialog akaun telah disenaraikan. Perbualan yang ditemui atau diaktifkan kemudian memerlukan pelaksanaan lain.

## Pause, mula semula dan keputusan separa

- **Sejarah jeda** menghentikan pembacaan. **Sambung sejarah** akan meneruskan dari mesej terakhir yang disimpan dalam setiap sumber; memulakan semula aplikasi juga akan membiarkan jalannya jeda sehingga disambung semula. Mulakan semula pemerhatian terlebih dahulu. Menyambung semula memerlukan akaun Telegram yang sama.
- Pengamatan mesej, pemprosesan lampiran dan komitmen penunjuk dalam satu transaksi. Jalankan semula tidak akan mengulangi pengamatan yang telah dikomit. Rakaman langsung atau jalankan berasingan yang dimulakan secara eksplisit boleh memerhati mesej yang sama secara bebas.
- Setiap sumber menetapkan ID mesej tertinggi pada bacaan pertama. Mesej yang lebih baru tergolong dalam pemerhatian langsung, bukan pada halaman sejarah yang masih ada bagi sumber tersebut.
- Sumber yang tidak dapat diakses dan sumber yang dilumpuhkan semasa pengambilan kekal kelihatan sebagai gagal atau dilangkau. Sumber lain diteruskan; keputusan keseluruhan tidak lengkap.
- Penangguhan FloodWait menghormati selang menunggu semula yang disimpan. Masa tamat penghantaran dan ruang cakera rendah menghentikan pelaksanaan dengan penunjuk kekal. Sambung semula selepas menyelesaikan puncanya.
- **Menamatkan larian sejarah ini** mengekalkan pemerhatian yang disimpan. Ia tidak memadamnya atau membatalkan muat turun lampiran yang telah diatur. Larian baru membaca semula sumber yang diaktifkan.

Penyempurnaan sejarah menerangkan bacaan sejarah sahaja. Lampiran mungkin kekal menunggu, gagal, atau dikecualikan oleh dasar yang dikonfigurasikan. Semak resit media dalam jurnal dan barisan menunggu lampiran; hanya resit yang disempurnakan dengan bait yang terpelihara dianggap sebagai lampiran yang disimpan. Operasi sejarah adalah permintaan snapshot eksplisit dan berasingan daripada suis yang memilih kategori acara langsung akan datang.

## Pindahkan dan sahkan

Simpan **laporan kemajuan yang ditandatangani**, kemudian gunakan **Eksport bukti** untuk memuat turun jurnal dan lampiran yang disimpan. Eksport bukti kemudian mungkin termasuk rekod tambahan; laporan ini mengikat pengiraannya kepada awalan jurnal pada masa ia dibuat. Jalankan pengesah daripada tarikan semak yang dipercayai bagi versi ini:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Simpan cap jari kunci tandatangan yang dijangka secara berasingan. Pengesah memeriksa tandatangan laporan, arkib bukti, titik pemeriksaan laporan, pelan sumber, akaun dan kiraan mesej yang disimpan/tidak tersedia. Tanpa `--evidence`, ia hanya memeriksa laporan yang ditandatangani dan keserasian dalamannya. Fasa kemajuan, tajuk, penunjuk dan ringkasan lampiran adalah kenyataan pengumpul yang disahkan, bukan dibina semula secara bebas oleh pemeriksa laporan ini. Pengesah bukti masih memeriksa bait media yang diarkibkan.

Mencatat tandatangan mahupun menamatkan sejarah yang tersedia tidak membuktikan asal Telegram, gambaran seketika atomik, atau kelengkapan sejarah. Mesej boleh berubah semasa dibaca; mesej yang dipadam, suntingan pertengahan yang belum dilihat dan Perbualan Rahsia tidak dapat dipulihkan. Seorang pengendali yang mengawal kunci tandatangan boleh memalsukan jurnal sebelum sebarang komitmen luaran wujud. Gunakan titik pemeriksaan yang disimpan secara berasingan atau saksi bebas untuk sifat pengesanan pengubahsuaian yang didokumenkan.

Penunjuk pemerolehan adalah status ruang kerja tempatan. Memulihkan ZIP bukti sahaja tidak memulihkan kerja pemerolehan yang tertangguh atau sesi Telegram. Simpan sandaran ruang kerja jika sambungan kerja asal diperlukan.
