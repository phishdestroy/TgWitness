# Kelola sekumpulan akaun

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/groups/

Kelola beberapa akaun pengumpulan sekaligus sambil memastikan rekod setiap akaun dan identiti tandatangan masing-masing berasingan.

Kumpulan akaun menggabungkan status sambungan, kawalan pemerhatian, tetapan kongsi dan eksport ke dalam satu paparan kerja. Ia berguna apabila beberapa akaun merangkumi siasatan yang sama atau memerlukan tetapan operasi yang konsisten.

## Buka gambaran keseluruhan kumpulan

Dalam **Akaun**, buka kumpulan. Setiap akaun memaparkan status pemerhatiannya, laluan sambungan, kelewatan laluan terkini yang diukur apabila pemeriksaan semasa berjaya, dan mesej terakhir disimpan. Pautan **'Perlukan Perhatian'** ke akaun yang memerlukan kerja; **'Betulkan'** membuka ruang kerja dan kawalan berkaitan.

**Mulakan Semua** dan **Tunda Semua** bertindak pada akaun yang layak selepas pengesahan. **Tetapan kumpulan** berkongsi tetapan terpilih; akaun dengan nilai tersendiri mengekalkan nilai tersebut sehingga anda memilih untuk menggantikannya.

### Melihat semula perubahan laluan dalam kumpulan

Contoh sintetik · pemeriksaan dan hasil ilustratif

1. **Pilih.** Pilih kumpulan dan semak akaun yang akan diubah.
2. **Sediakan.** Kekalkan laluan akaun itu sendiri apabila ia perlu kekal berasingan.
3. **Semak.** Uji sambungan yang dicadangkan dan periksa keputusan yang diukur.
4. **Terapkan.** Semak semula sebelum menyimpan dan semak keputusan untuk setiap akaun.

#### Pasukan kes

Pengumpul saluran · Pengumpul kumpulan · Akaun rujukan

3 ruang kerja berasingan

#### Pilihan telah disemak

2 akaun mengambil laluan yang dicadangkan.

Akaun rujukan mengekalkan laluan tersendiri.

#### Semakan persiapan

Pengumpul saluran: Pengangkutan Telegram 84 ms

Pengumpul kumpulan: Penghantaran Telegram 91 ms

Nombor-nombor ini adalah ukuran rekaan untuk contoh.

#### Keputusan aplikasi

Pengumpul saluran: laluan disimpan, pemerhatian disambung semula.

Pengumpul kumpulan: semakan semula gagal, tetapan sebelumnya dipulihkan.

Akaun rujukan: laluan sendiri dikekalkan.

## Ubah laluan dengan langkah semakan

1. Pilih **Ubah laluan kumpulan**, kemudian pilih jenis sambungan dan tetapan.
2. Pilih **Pilihan Semakan**. Semak akaun yang disenaraikan dan penafian laluan individu mereka.
3. Pilih **Sediakan dan semak**. Semakan menggunakan saluran Telegram baharu; laluan HTTP yang disokong juga melaporkan pemeriksaan keluar HTTPS mereka.
4. Pilih **Terapkan sambungan yang diperiksa** dan periksa keputusan setiap akaun. Pengawasan yang sedang dijalankan sebelum ini disambung apabila aplikasi berjaya; akaun tidak aktif kekal tidak aktif.

Latensi menerangkan penyediaan sambungan Telegram yang diukur. Semakan IP keluar menerangkan laluan tersebut pada masa semakan yang direkodkan. Pengesahan akaun dan kesihatan pemantauan mempunyai penunjuk masing-masing; perubahan kumpulan boleh berakhir dengan hasil yang berbeza bagi setiap akaun.

## Gunakan akses bertindih

**Perbualan beberapa akaun**memaparkan sumber yang dikongsi dan liputan pemerhatian ruang kerja yang tersedia. Saluran dan superkumpulan yang layak boleh menggunakan **Eksport dengan … akaun** untuk membahagikan pemerolehan sejarah satu perbualan. Perbualan peribadi dan kumpulan biasa kekal dengan akaun asal kerana nombor mesej mereka tergolong dalam sejarah akaun tersebut.

## Eksport kumpulan sebagai pakej

**Kumpulan eksport** mencipta satu fail ZIP yang mengandungi eksport berasingan setiap akaun yang ditandatangani dan satu senarai berasingan fail tersebut yang ditandatangani. Identiti dan cap jari ruang kerja asal kekal tersedia untuk pengesahan. Bina naratif merentas akaun menggunakan rujukan tersebut; satu garisan masa gabungan tunggal masih disusun secara berasingan.

Teruskan dengan [reka bentuk laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reports/), [papan kes dalam ruang kerja](https://phishdestroy.github.io/TgWitness/ms/docs/case-board/), atau [pengesahan eksport](https://phishdestroy.github.io/TgWitness/ms/docs/exports/).
