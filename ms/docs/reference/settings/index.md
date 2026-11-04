# Pendaftaran awal dan tetapan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/settings/

Penyihir persediaan, matlamat, tahap antara muka, laluan sambungan dan tetapan yang dikongsi oleh kumpulan akaun.

[Akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/) · [Sambungan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) · [Akses](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/)

Satu ruang kerja baru dibuka `/first-run`: bahasa dan masa, tahap antara muka, matlamat, pautan, Telegram dan sembang. Setiap jawapan disimpan di pelayan sebaik sahaja ia berubah, jadi pemuatan semula meneruskan langkah yang sama. Skrin terakhir menyenaraikan jawapan dan membolehkan anda kembali ke mana-mana daripadanya.

Bahasa, zon waktu IANA, tema dan tahap disimpan bagi setiap pengendali dan setiap ruang kerja. Larasannya ialah bahasa pelayar, zon waktu peranti, tema sistem dan antara muka Mudah. Menukar bahasa mengekalkan sesi panel. Masa dalam jurnal yang disahkan tidak pernah berubah.

`/settings` menyunting rekod yang sama seperti wizard. Carian merangkumi medan utama, parameter dan borang lanjutan; medan tersembunyi boleh dibuka tanpa menukar peringkat. Peringkat hanya mengubah apa yang dipaparkan: pelayan menyemak kebenaran dengan sendirinya. Tetapan koleksi dan sambungan pertama adalah milik pentadbir ruang kerja.

| Tahap | Medan | Bar sisi |
| --- | --- | --- |
| Mudah | Hanya yang penting | Home, Chats, Perubahan, Arkib, Tetapan |
| Standard | Tetapan umum dengan penjelasan | Menambah Case Board, Akaun dan Akses |
| Pakar | Semua medan, had dan butiran teknikal | Menambah Sumber, Ekstra, Tanya arkib, Parameter, Akaun, Log Sistem dan Integrasi |

[Panduan panel](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/) menerangkan setiap bahagian.

## Matlamat

| Matlamat | Koleksi | Fail | Perkhidmatan luar | Alamat pelayan |
| --- | --- | --- | --- | --- |
| Salinan arkib | Padam; **Mulai** menjalankan eksport | Foto sehingga 20 MB | Padam | Otomatik |
| Ikuti sembang | Berterusan | Foto dan video sehingga 60 saat / 20 MB | Cap masa dan pemberitahuan masalah | Otomatik |
| Bukti | Berterusan | Semua fail sehingga 1 GB | Cap masa, drand, pemberitahuan | Tidak, sembunyikannya |

Salinan luar tapak, bot saksi dan pemeriksaan kod disyorkan untuk bukti. Alamat penyimpanan dan pemberitahuan memerlukan destinasi terlebih dahulu. Satu ciri yang berkomunikasi dengan perkhidmatan luar meminta kebenaran untuk membenarkan permintaan di luar Telegram; menamatkan ciri ini menawarkan untuk mematikan cap masa, pemberitahuan dan salinan luar tapak bersamanya.

Menukar matlamat akan memaparkan perbezaan terlebih dahulu, dan perubahan manual boleh disimpan. Medan yang berbeza daripada matlamat akan ditandakan "**Diperubahan oleh anda**" dan boleh dipulihkan. Semakan tetapan mengekalkan perbezaan yang telah disemak supaya ia tidak diterapkan ke atas perubahan yang dibuat dalam tab lain.

## Sambungan

**Automatic** mencuba pelayan MTProxy awam secara automatik, kemudian WARP, kemudian sambungan terus, yang terakhir hanya apabila alamat pelayan boleh dipaparkan. Automatic dan WARP boleh memasang komponen yang disemak hash dan mendaftarkan pelayan dengan Cloudflare. WARP menggunakan pengurus wgcf/wireproxy sedia ada dan port SOCKS5 tempatan; jadual penghalaan sistem tidak diubah. Apabila perkhidmatan luar diperlukan, Automatic lebih memilih WARP berbanding MTProxy.

Proksi anda sendiri menerima `tg://proxy`, `socks5://`, `http://` dan `https://`. Sijil proksi HTTPS diperiksa sebelum kelayakan dihantar kepadanya.

Semakan sambungan sah untuk lima minit dan terikat kepada laluan, dasar dan jawapan wizard; menukar mana-mana daripadanya memerlukan semakan baru. **Sambungan tanpa semakan** tersedia dan tidak menggantikan kemasukan Telegram. Laluan yang dipilih disemak semula di latar belakang, dan Automatic menjalankan rantaiannya semula selepas sambungan terputus. Apabila tiada proksi awam yang menjawab, kiraan bertukar merah dengan tindakan WARP dan semak semula.

## Kumpulan akaun

Akaun dalam kumpulan berkongsi tetapan mereka. Buka **Akaun → Kumpulan dan tetapan dikongsi → Tetapan dikongsi**, atau **Tetapan kumpulan** pada halaman Tetapan akaun.

Kumpulan berkongsi matlamat, fail yang disimpan, cap masa, drand, pemberitahuan masalah, salinan luar tapak, permintaan di luar Telegram, mod IP, apa yang hendak dirakam, jadual semakan semula, peraturan pemberitahuan, tetapan laporan, parameter dan laluan sambungan. Destinasi pemberitahuan, kelayakan proksi dan log masuk kekal bagi setiap akaun, begitu juga permulaan dan penggantungan pengumpulan.

- Setiap ahli mengikuti kumpulan. Tetapan menandakan nilai 🔗 **Daripada kumpulan** atau ✏️ **Nilai sendiri**; **Kembali ke nilai kumpulan** memulihkannya.
- Perubahan menyenaraikan akaun yang terjejas (**Berkuat kuasa pada 2 daripada 3 akaun**) dan bertanya bagi setiap akaun sebelum menggantikan nilai sedia ada. Akaun yang tidak dicentang mengekalkan nilai asal mereka.
- Parameter yang tidak dikongsi oleh kumpulan kekal **Tidak dikongsi: setiap akaun mengekalkan nilai tersendiri** sehingga anda menekan **Kongsi nilai ini**.
- **Menyalin tetapan daripada satu akaun** mengambil nilai akaun terpilih sebagai nilai kumpulan.
- Akaun yang dipindahkan ke dalam kumpulan akan ditanya**: Ambil nilai kumpulan?** Jika tidak, ia mengekalkan nilai sendiri, ditandakan ✏️. Akaun yang ditambah kemudian bermula dengan nilai kumpulan.
- Akaun pemerhati mengekalkan mod IPnya sehingga ia dihentikan seketika.

Setiap perubahan direkodkan dalam jurnal yang ditandatangani bagi ruang kerja utama dan setiap ahli yang menerimanya. Menghapus kumpulan mengekalkan akaun-akaunnya dan nilai semasa mereka.

Laman kumpulan `/groups/<id>` menunjukkan ahli, perkara yang memerlukan perhatian dan sembang yang dilihat oleh beberapa akaun. Lihat [kumpulan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/#bulk-import-and-account-groups).

## Ruang kerja sedia ada

Sebuah ruang kerja dengan sesi atau persediaan yang telah selesai sebelum ini tidak akan mendapat wizard. Nilainya tidak digantikan oleh matlamat apabila halaman dimuat. Menyembunyikan medan tidak menutup ciri tersebut atau memadam nilainya.

Saiz dan anggaran masa membaca sehingga tiga sembang terpilih dan sehingga 20 mesej daripada masing-masing. Ia hanyalah anggaran: ia tidak meramalkan had Telegram, kelajuan pelayan tertentu atau fail dalam setiap sembang.
