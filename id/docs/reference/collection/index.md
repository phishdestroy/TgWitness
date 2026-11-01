# Cara kerja pengumpulan data

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/collection/

Ruang lingkup pengamatan, pembaruan langsung, pemeriksaan ulang, lampiran, tindakan pengguna, dan arti dari "gap", per catatan.

TgWitness merekam apa yang diamati oleh akun Telegram yang terhubung. Jurnal tersebut menyimpan pengamatan tersebut, urutannya, serta konteks yang menyertainya. Alat ini tidak menyimpulkan tindakan yang tidak terlihat berdasarkan pesan yang hilang atau akun yang sedang terhubung.

## Dari proses login hingga jurnal

Diagram alur · Otorisasi akun pengguna → Pilih grup dan saluran yang dapat diakses; Pilih grup dan saluran yang dapat diakses → Simpan pengaturan peristiwa dan lampiran; Simpan pengaturan peristiwa dan lampiran → Mulai pemantauan; Mulai pemantauan → Dapatkan pembaruan dari klien yang aktif; Dapatkan pembaruan dari klien yang aktif → Terapkan kebijakan sumber dan peristiwa; Terapkan kebijakan sumber dan peristiwa → Tambahkan pengamatan yang ditandatangani; Tambahkan pengamatan yang ditandatangani → Tinjau atau ekspor jurnal tersebut; Tambahkan pengamatan yang ditandatangani → Memproses lampiran yang ada dalam antrian; Memproses lampiran yang ada dalam antrian → Tambahkan hasil unduhan · Otorisasi akunpengguna · Pilih grup dan saluranyang dapat diakses · Simpan pengaturanperistiwa dan lampiran · Mulai pemantauan · Dapatkan pembaruandari klien yang aktif · Terapkan kebijakansumber dan peristiwa · Tambahkan pengamatanyang ditandatangani · Tinjau atau eksporjurnal tersebut · Memproses lampiranyang ada dalam antrian · Tambahkan hasilunduhan

**Diagram dalam bentuk teks**

1. Otorisasi akun pengguna → Pilih grup dan saluran yang dapat diakses
2. Pilih grup dan saluran yang dapat diakses → Simpan pengaturan peristiwa dan lampiran
3. Simpan pengaturan peristiwa dan lampiran → Mulai pemantauan
4. Mulai pemantauan → Dapatkan pembaruan dari klien yang aktif
5. Dapatkan pembaruan dari klien yang aktif → Terapkan kebijakan sumber dan peristiwa
6. Terapkan kebijakan sumber dan peristiwa → Tambahkan pengamatan yang ditandatangani
7. Tambahkan pengamatan yang ditandatangani → Tinjau atau ekspor jurnal tersebut
8. Tambahkan pengamatan yang ditandatangani → Memproses lampiran yang ada dalam antrian
9. Memproses lampiran yang ada dalam antrian → Tambahkan hasil unduhan

Otorisasi, akses ke sumber, pengumpul yang sedang berjalan, dan pengiriman yang lengkap adalah masalah yang berbeda. Login yang berhasil tidak menjamin akses ke setiap grup. Koneksi transportasi yang terhubung tidak menjamin bahwa setiap pembaruan yang relevan telah diterima.

## Cakupan pemantauan: obrolan yang dipilih, sebuah folder, atau seluruh akun

Sumber → **Ruang lingkup pengamatan** menentukan obrolan mana saja yang direkam oleh ruang kerja.

| Mode | Merekam | Obrolan baru |
| --- | --- | --- |
| Obrolan yang dipilih (default) | Hanya obrolan yang Anda tambahkan secara manual | Tidak pernah ditambahkan secara otomatis |
| Folder Telegram | Percakapan dalam salah satu folder akun: percakapan yang disertakan berdasarkan nama, ditambah kategori folder tersebut (kontak, bukan kontak, grup, saluran, bot), dikurangi percakapan yang dikecualikan, dan, jika folder tersebut mencantumkannya, percakapan yang diarsipkan | Obrolan yang sesuai akan ditambahkan segera setelah aktif; obrolan yang Anda tambahkan ke folder di Telegram akan terdeteksi dalam waktu satu jam |
| Akun lengkap | Setiap obrolan yang dilihat oleh akun tersebut | Setiap obrolan baru, grup, obrolan pribadi, atau bot akan ditambahkan begitu pembaruan pertamanya tiba |

- **Jenis sumber** (saluran, grup, obrolan pribadi, bot) mempersempit mode folder dan mode seluruh akun. Obrolan yang dipilih dapat berupa jenis apa pun, termasuk obrolan pribadi dan bot.
- **Obrolan yang dikecualikan** tidak pernah direkam, dalam mode apa pun. Dalam mode folder dan seluruh akun, opsi *"Kecualikan"* dan *"Hapus"* pada sumber akan memasukkannya ke dalam daftar ini, sehingga cakupan tidak akan menambahkannya lagi. Memilih obrolan tersebut kembali secara manual (di bagian "Sumber" atau dari "Obrolan") akan menghapusnya dari daftar. Daftar ini dapat menampung hingga 5.000 obrolan; jika melebihi batas tersebut, *perintah "Hapus"* akan ditolak dan obrolan tersebut dapat dijeda sebagai gantinya.
- **Tindakan sendiri** (aktif secara default): pesan yang dikirim oleh akun ini, pengeditannya, dan penekanan tombol pada keyboard balasan. Jika dinonaktifkan, pesan keluar dan pengeditan akan dilewati.
- Beralih ke folder atau seluruh akun akan meminta konfirmasi: mode-mode ini merekam obrolan pribadi dan pesan pihak ketiga, dan hanya boleh digunakan pada akun khusus. Konfirmasi dan setiap perubahan cakupan merupakan catatan `scope.changed` yang ditandatangani.
- Obrolan yang ditambahkan oleh cakupan akan muncul sebagai sumber yang ditandai *"auto"*, direkam sebagai `scope.applied` (pada awal dan setiap jam) atau `source.discovered` (obrolan baru saat pemantauan berlangsung). Kembali ke obrolan yang dipilih akan menghentikan sementara semua sumber yang ditambahkan secara otomatis.

Hal-hal yang tidak dapat dilakukan oleh mode-mode ini:

- **Obrolan rahasia** dienkripsi ujung-ke-ujung antara dua perangkat dan tidak pernah sampai ke TgWitness, dalam mode apa pun.
- **Tidak ada yang direkam saat TgWitness tidak berjalan.** Setelah di-restart, TgWitness meminta Telegram untuk pembaruan yang terlewat dan memeriksa ulang obrolan, tetapi Telegram tidak mengembalikan semua data setelah gangguan yang lama. Laporan dan `verify.py` menampilkan periode tersebut sebagai celah (lihat [cakupan](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Hanya 1.000 percakapan pertama yang ditampilkan pada awalnya (batasnya tercantum di **bagian Parameter**); percakapan yang lebih lama akan ditambahkan saat percakapan tersebut aktif kembali. Riwayat awal dari percakapan yang ditambahkan tidak diambil — ambil tangkapan layar riwayat atau ekspor percakapan lengkap saat Anda membutuhkannya.
- Kondisi folder yang terus berubah (dibisukan, telah dibaca) tidak diterapkan: obrolan semacam itu tetap dipantau.
- **Tombol bot inline (callback)** yang ditekan di aplikasi lain tidak terlihat oleh sesi kedua ; balasan atau pengeditan bot dicatat. Tekan tombol balasan pada keyboard tiba sebagai pesan keluar dan diberi label `button_press`.
- Semakin banyak obrolan berarti semakin banyak permintaan. Telegram membatasi akun yang dianggap memiliki volume yang berlebihan, yang menjadi alasan tambahan untuk menggunakan akun khusus.

## Ruang lingkup dan pemilihan peristiwa

Setiap ruang kerja memiliki sumbernya sendiri. TgWitness tidak bergabung dengan grup, menerima undangan, atau menghitung setiap anggota secara otomatis. Sumber harus sudah dapat diakses oleh akun tersebut. Saat dimulai, pengumpul memeriksa sumber yang dipilih terhadap percakapan yang terlihat di akun; 1.000 percakapan pertama diperiksa kecuali jika **Parameter → Obrolan yang dibaca dari daftar akun** menyatakan sebaliknya. Sumber yang tidak ada ditandai sebagai **akses belum dikonfirmasi**, tidak diasumsikan telah menghapus Anda.

| Pengaturan | Mengumpulkan | Dampak jika dinonaktifkan |
| --- | --- | --- |
| Pesan baru | Pesan yang dikirim secara biasa | Pengeditan atau penghapusan yang dilakukan kemudian mungkin tidak memiliki teks yang terekam sebelumnya untuk dibandingkan. |
| Pengeditan | Menyajikan versi pesan yang telah diedit | Perubahan yang terjadi di antara proses tersebut tidak direkonstruksi kemudian. |
| Penghapusan | Pemberitahuan penghapusan yang terbatas cakupannya dan pemberitahuan tingkat akun yang tidak terbatas cakupannya | Pemberitahuan penghapusan tidak ditambahkan ke jurnal. |
| Reaksi | Cuplikan reaksi yang ditampilkan | Pembaruan reaksi terpisah tidak ditambahkan. |
| Keanggotaan | Penyampaian pesan layanan keanggotaan dan pembaruan bagi peserta | Pengamatan keanggotaan tersebut tidak ditambahkan. |

Pengaturan berlaku untuk semua sumber yang dipilih di ruang kerja. Simpan formulir untuk menerapkan perubahan; perubahan dicatat dengan nilai sebelum/sesudah yang ditandatangani. Menonaktifkan suatu kategori tidak akan menghapus catatan sebelumnya. Mengaktifkannya kembali tidak akan mengisi kembali pembaruan yang terlewat.

Catatan operasional dan peristiwa layanan grup lainnya tetap terpisah dari pengaturan ini. Pesan layanan keanggotaan dapat membuat catatan pesan saat fitur keanggotaan diaktifkan, meskipun penangkapan pesan baru biasa dinonaktifkan. Objek Telegram yang ditangkap tetap mempertahankan metadata yang tertanam; pengaturan ini bukanlah aturan penyuntingan.

**Penghapusan dalam obrolan pribadi dan grup biasa** tercatat sebagai ID pesan tanpa obrolan. Obrolan-obrolan ini berbagi urutan ID pesan yang berlaku untuk seluruh akun, sehingga ketika pesan dengan ID tersebut telah disimpan sebelumnya, obrolannya diketahui: penghapusan tersebut dicatat dalam obrolan tersebut dengan penjelasan cara kerjanya oleh `chat_resolution`. ID yang tidak pernah disimpan tetap menjadi **penghapusan tanpa cakupan** dengan sumber yang secara eksplisit tidak diketahui; pengumpul data tidak membuat tebakan. Telegram tidak pernah menyebutkan siapa yang menghapus pesan; ketika pesan yang dihapus dikirim oleh akun ini, catatan tersebut mencantumkannya (`deleted_message_was_outgoing`) tanpa menyebutkan nama penghapus.

## Tindakan sendiri

Pesan yang dikirim oleh akun yang diamati diberi label `outgoing`. Pengeditan pesan keluar mencatat bahwa dalam obrolan pribadi dan grup, hanya penulisnya yang dapat mengeditnya, sedangkan posting saluran dapat diedit oleh admin lain. Ketika sebuah pesan keluar mengulang teks tombol dari papan ketik balasan terbaru yang disimpan dalam obrolan tersebut, pesan tersebut diberi label `button_press` dengan tautan ke catatan papan ketik tersebut.

Pengecualian terhadap tindakan pengguna sendiri juga berlaku untuk pemeriksaan ulang latar belakang dan riwayat obrolan baru otomatis. Pesan keluar yang dilewati akan memajukan posisi pemeriksaan ulang sehingga tidak dapat menghalangi pesan masuk selanjutnya. Tindakan panel yang eksplisit dan cuplikan riwayat yang diminta secara manual tetap terekam.

## Mode investigasi: bergabung dengan tim dan berkomunikasi dengan bot

**Sumber → Cakupan pengamatan → Mode investigasi** menyiapkan cakupan untuk akun khusus yang bergabung dengan obrolan grup, memulai bot, dan mengirim pesan ke bot tersebut: seluruh akun, setiap jenis sumber, tindakan sendiri, serta untuk setiap obrolan atau bot yang muncul, profilnya dan 200 pesan terbaru yang terlihat. Tinjau formulir dan tekan **Simpan cakupan**; peralihan ke seluruh akun akan meminta konfirmasi seperti biasa.

- **Tombol.** Tombol di bawah pesan tetap menyertai pesan tersebut dan ditampilkan di **Obrolan**: tautan, aplikasi web , tautan masuk, teks untuk disalin, data panggilan balik, kueri sebaris, permintaan nomor telepon atau lokasi. Tautan ditampilkan sebagai teks dan tidak pernah dibuka oleh panel. Ketika bot hanya mengubah tombol-tombol tersebut (tautan pembayaran baru), hal itu dianggap sebagai versi baru dari pesan tersebut, baik dari pembaruan langsung maupun dari pemeriksaan ulang.
- **Obrolan dan bot baru.** Dalam mode folder dan akun keseluruhan, **ketika obrolan atau bot baru muncul**, data akan disimpan segera setelah muncul:

  - profilnya sebagai catatan `source.profile`: deskripsi bot dan perintah, teks "Tentang" dari pengguna, grup, atau saluran, anggota, obrolan yang tertaut, dan tautan undangan jika Telegram menyediakannya;
  - pesan-pesan terbarunya yang terlihat (hingga 1.000) sebagai cuplikan riwayat yang ditandai dengan `new_chat`: pesan-pesan sebelumnya dari obrolan tim yang baru saja bergabung, atau apa yang dikatakan bot sebelum pengamatan memperhatikan obrolan tersebut. Pesan yang sudah disimpan secara langsung tidak diulang.

  Obrolan yang sudah ada dalam daftar saat mode diaktifkan akan ditambahkan tanpa tangkapan layar. Fitur FloodWait akan menghentikan sementara proses ini dan dilanjutkan setelahnya; kegagalan dicatat dan perekaman obrolan secara langsung tetap berlanjut. - **Profil berdasarkan permintaan. Obrolan → Profil → Simpan profil kini** menyimpan profil saat ini dari sumber mana pun; profil terbaru ditampilkan di atas pesan. - **Tidak terlihat.** Tombol inline (callback) yang ditekan di aplikasi Telegram lain, popup atau tautan yang digunakan bot sebagai respons atas penekanan tersebut, serta tautan undangan yang digunakan di aplikasi lain tidak sampai ke TgWitness. Apa yang dikirim atau diedit oleh bot setelahnya akan dicatat.

### Tindakan dari panel

**Obrolan** kini mencakup klien mini yang menggunakan akun Telegram dari ruang kerja yang dipilih:

- Tulis pesan teks biasa atau pilih **"Balas"** di bawah pesan yang telah disimpan. Pesan keluar yang dikirimkan akan terekam meskipun cakupan pengaturan tidak mencakup pembaruan pesan keluar.
- Tekan **tombol "Press"** di bawah tombol callback atau teks yang sedang aktif. Server akan mengambil pesan tersebut kembali dan menolak tindakan tersebut jika teks yang dimasukkan berbeda dari versi yang tersimpan. Tanda terima callback mempertahankan teks popup Telegram, bendera peringatan, dan URL; jawabannya juga ditampilkan di bawah percakapan. URL tetap berupa teks yang dapat dipilih dan tidak dibuka secara otomatis.
- Buka **tautan Telegram**, masukkan `@username`, tautan `https://t.me/name` publik, `https://t.me/+invite` / `joinchat/invite`, atau tautan bot dengan `?start=parameter`, lalu tekan **Simpan pratinjau**. Tautan asli dan pratinjau Telegram akan ditandatangani sebelum bergabung. **Bergabung / buka dan amati**, kemudian bergabung dengan grup/saluran atau membuka pengguna/bot, tambahkan obrolan sebagai sumber yang diaktifkan, dan kirimkan `/start` ke bot, termasuk parameter awalnya. Permintaan bergabung yang menunggu persetujuan administrator dicatat sebagai tertunda, bukan sebagai keanggotaan.

Aktifkan "**Mulai Pengamatan**" untuk merekam balasan yang masuk secara langsung. Tindakan panel tetap berfungsi saat pengamatan dijeda, tetapi hanya respons langsungnya yang dijamin akan disimpan. Sumber yang baru ditambahkan menggunakan profil/riwayat yang telah dikonfigurasi saat pengamatan sedang berjalan. Saat sebuah sumber dijeda, aktifkan terlebih dahulu di bagian "**Sumber**" sebelum mengirim pesan atau menekan tombolnya.

`interaction.preview`, `interaction.requested`, dan `interaction.result` adalah peristiwa jurnal bertanda tangan biasa yang disertakan dalam ekspor bukti. Permintaan mengidentifikasi akun, pesan/tombol atau catatan pratinjau, serta apakah pengamatan sedang berjalan. Tanda terima membedakan antara keberhasilan, penolakan, persetujuan tertunda, dan hasil yang tidak diketahui. Permintaan yang terputus mungkin telah sampai ke Telegram: periksa obrolan sebelum memulai tindakan baru. Menggunakan kembali ID permintaan akan mengambil tanda terima yang tersimpan tanpa mengulangi tindakan, termasuk setelah restart. Panel mempertahankan ID tersebut setelah respons ambigu untuk tindakan yang sama selama sesi halaman saat ini. Panel juga mempertahankan ID tersebut ketika penyegaran tampilan gagal setelah tindakan berhasil: tanda terima tetap terlihat, dan mengklik lagi akan mengambilnya kembali. RPC callback dan join memiliki satu upaya aplikasi; pembacaan yang dapat dicoba ulang mempertahankan kebijakan percobaan ulang yang telah dikonfigurasi. Beralih obrolan secara langsung akan menghapus draf dan target balasan serta menonaktifkan pengiriman hingga percakapan baru dimuat.

Mini-klien ini menangani teks dan tombol panggilan balik. Aplikasi web, permintaan login/nomor telepon/lokasi, pembayaran, kueri sebaris, dan lampiran masih memerlukan klien Telegram; metadata tombol yang disimpan tetap terlihat. Kontrol baru ini menggunakan teks dalam bahasa Inggris.

## Tingkat verifikasi ulang

Pemeriksaan ulang meminta Telegram kembali untuk pesan yang terlewat, pengeditan, dan pesan yang tidak lagi dikembalikan. Sumber yang ditandai dengan bintang adalah sumber **prioritas**, diperiksa ulang setiap 15 menit secara default; semua sumber lainnya setiap 6 jam. Obrolan yang dipilih dimulai sebagai sumber prioritas, sedangkan obrolan yang ditambahkan melalui folder atau seluruh akun sebagai sumber reguler. Paling banyak 30 sumber diperiksa ulang per siklus dan sisanya menunggu hingga menit berikutnya; setelah koneksi terhubung kembali, sumber prioritas diproses terlebih dahulu. Kedua interval tersebut diatur di Sumber → Pengaturan perekaman → Pemeriksaan Ulang (0 menonaktifkan tingkatan) dan dicatat sebagai `recheck.changed`.

Pesan yang terlewat diambil mulai dari titik di mana proses sebelumnya berhenti, dengan batas maksimal yang ditentukan di **Parameter → pesan baru per pemeriksaan ulang** (1.000 secara default) per proses. Setelah jeda yang lama, proses pemeriksaan ulang ini akan mengisi seluruh celah tersebut, bahkan jika pesan-pesan langsung yang lebih baru daripada celah tersebut telah disimpan terlebih dahulu. Obrolan yang masih dalam proses penyesuaian akan diperiksa ulang pada menit berikutnya alih-alih menunggu interval tingkatan; `recheck.completed` akan menampilkan `continues_after` hingga proses selesai.

Perbandingan mencakup teks pesan, entitas, papan ketik (termasuk penghapusan), serta konten/identitas lampiran. Mengubah hash akses berkas atau referensi berkas saja tidak dianggap sebagai pengeditan, begitu pula hal-hal yang diisi secara otomatis oleh Telegram: pemuatan pratinjau tautan, tampilan cerita, media berbayar yang dibuka oleh akun ini, serta tanda terima faktur. Setiap versi yang disimpan di Obrolan tertaut ke catatan jurnal lengkapnya, termasuk metadata media.

## Riwayat pesan dan atribusi

Misalkan pengumpul mengamati “Pertemuan pukul 10:00,” kemudian melihat “Pertemuan pukul 11:00,” dan kemudian menerima pemberitahuan penghapusan. Alat ini menambahkan tiga catatan terpisah. Teks asli tetap ada, suntingan menjadi versi terpisah, dan pemberitahuan tersebut mencatat bahwa telah terdeteksi adanya penghapusan.

Jika pengumpulan dimulai setelah versi pertama menghilang, teks tersebut tidak tersedia. Jika terjadi beberapa pengeditan saat proses dalam keadaan offline, hanya versi yang diamati setelahnya yang dapat disimpan. Pemberitahuan penghapusan tidak dapat memulihkan konten yang tidak pernah terekam.

Pengirim pesan tidak secara otomatis dianggap sebagai pengedit. Telegram biasanya tidak menyediakan informasi mengenai orang yang menghapus pesan atau waktu penghapusan yang tepat. Aktor yang tidak dikenal tetap tidak diketahui. Cuplikan reaksi dan pembaruan peserta hanya berisi jumlah serta identitas yang ditampilkan Telegram kepada akun tersebut.

Nomor urut menunjukkan urutan pengamatan. Cap waktu UTC pengumpul adalah waktu lokalnya; cap waktu sumber Telegram disimpan secara terpisah jika tersedia. Keduanya bukanlah cap waktu tepercaya yang independen.

## Cuplikan riwayat

Sebuah snapshot meminta pesan-pesan terbaru yang terlihat dari sumber yang diaktifkan, hingga 500 pesan per permintaan. Hasilnya diberi label sebagai pengamatan riwayat. Pengamatan ini dapat tumpang tindih dengan penangkapan langsung, dan pengamatan yang berulang disimpan sebagai catatan terpisah.

Cuplikan mengikuti kebijakan lampiran tetapi tetap terpisah dari peralihan peristiwa langsung. Cuplikan tersebut tidak merekonstruksi pesan yang dihapus atau versi perantara yang terlewat. Anda dapat meminta cuplikan saat proses dijeda; lampiran apa pun yang masuk ke antrian akan menunggu hingga pengamatan dimulai dan proses pengunduhan berjalan.

## Penanganan lampiran

Pengunduhan lampiran diaktifkan secara default dan akan dihentikan sementara jika ruang disk kosong kurang dari 1 GiB. Pengumpul melakukan pengamatan pesan dan tugas pengunduhan secara bersamaan. Tugas tersebut mempertahankan deskriptor media asli dan kebijakan ukuran, sehingga lampiran yang diedit kemudian tidak akan diganti tanpa pemberitahuan.

Pengunduhan dijalankan setelah penangkapan pesan. Pengunduhan yang selesai akan menghasilkan catatan `media.saved` beserta SHA-256 dan jumlah byte-nya. Pekerjaan yang dilewati, gagal, dicoba ulang, dan terputus memiliki hasil yang terpisah. Pekerjaan yang berada dalam antrian bukanlah bukti bahwa berkas tersebut telah disimpan. File yang telah selesai juga harus sesuai dengan jumlah byte dalam deskriptor lampiran asli yang diamati. Respons yang pendek atau panjang secara tak terduga tidak dicatat sebagai media yang telah disimpan.

Batas disetel **per jenis**: foto, video, GIF dan animasi, pesan video bulat, pesan suara, musik dan audio, stiker, serta file. Setiap jenis dapat dinonaktifkan dan memiliki batas ukuran tersendiri mulai dari 1 hingga 2.000 MiB; ruang kerja baru dimulai dengan 20 MiB untuk foto, 100 MiB untuk video, 50 MiB untuk file, audio, dan video bulat, 20 MiB untuk pesan suara dan GIF, serta 5 MiB untuk stiker. Ruang kerja baru menonaktifkan GIF dan stiker hingga diaktifkan. Ruang kerja dengan kebijakan yang disimpan sebelum batasan per jenis akan mengaktifkan semua jenis dan mempertahankan batasan tunggal untuk setiap jenis. *Ukuran file maksimum* menentukan semua jenis sekaligus. Jenis yang dinonaktifkan menghasilkan catatan `media.skipped`; file dengan ukuran tidak diketahui atau berukuran melebihi batas tidak akan diunduh. File besar mendapatkan waktu unduh tambahan berdasarkan ukurannya dan kecepatan dasar 256 KiB/s. Tugas tetap ada setelah restart, tetapi referensi yang kedaluwarsa, akses yang hilang, atau file yang dihapus tetap dapat menghalangi pemulihan. Pekerjaan yang sedang menunggu mempertahankan batas yang tersimpan bersamanya, sehingga peningkatan batas hanya berlaku untuk file baru. Menonaktifkan suatu jenis atau menurunkan batasnya juga akan melewatkan file-file yang sedang menunggu yang dikecualikan, masing-masing dengan catatan `media.skipped`; menonaktifkan unduhan akan menjeda antrian hingga diaktifkan kembali.

## Jeda, kunci, putuskan sambungan, dan mulai ulang

| Tindakan atau kondisi | Efek |
| --- | --- |
| Beralih ke ruang kerja | Mengubah tampilan panel; pengumpul lainnya tetap mempertahankan statusnya. |
| Kunci panel atau tutup tab | Membiarkan server dan pemantauan tetap berjalan. |
| Jeda pengamatan | Menghentikan pengumpul tersebut dan mempertahankan pekerjaan lampiran yang sedang dalam antrian. |
| Nonaktifkan sumber | Menghentikan penangkapan berkala di masa mendatang; tugas media yang sedang dalam antrian akan ditunda selama fitur ini dinonaktifkan. |
| Hapus sumber | Mencatatnya sebagai sumber dan menghapus profil penggunanya; catatan yang sudah disimpan tetap berada di jurnal yang hanya dapat ditambahkan. Lampiran yang masih menunggu dicatat sebagai gagal (`source_removed`). Dalam mode folder dan akun keseluruhan, hal ini juga dikecualikan. |
| Ubah rute koneksi | Membutuhkan jeda, menutup klien lama, dan membatalkan proses login yang belum selesai. |
| Hentikan proses Python | Menghentikan semua ruang kerja; tidak ada pengamatan yang dilakukan saat alat ini dalam keadaan offline. |
| Mulai ulang setelah pengamatan aktif | Upaya untuk melanjutkan cakupan yang disimpan menggunakan sesi yang disimpan. Penundaan manual akan menghapus niat tersebut. |

Pengumpul mencatat pemutusan koneksi yang terdeteksi, upaya ulang, kesalahan, proses mulai/berhenti, dan sinyal detak jantung. Gangguan singkat dapat terlewatkan oleh pemeriksaan konektivitas berkala. Setelah restart, pembaruan yang terlewat diminta mulai dari posisi pembaruan yang tersimpan dan obrolan yang dipantau diperiksa ulang secara berkala; lihat [format bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#durable-collection-and-process-receipts-02). Sebuah snapshot memberikan konteks; hal ini tidak membuktikan bahwa celah tersebut telah diperbaiki.

## Isolasi dan verifikasi akun

Setiap ruang kerja memiliki jurnal, otorisasi, kunci penandatanganan, kebijakan, dan antrian tersendiri. Hanya klien yang aktif yang dapat menyumbangkan pengamatan secara langsung. Klien yang ditolak, dalam antrian, digantikan, dan sedang melakukan uji koneksi tidak dapat menulis pembaruan langsung ke dalam jurnalnya. Akun yang berbeda dapat mengamati grup yang sama, tetapi jurnal masing-masing tetap terpisah.

Setiap peristiwa mencakup hash sebelumnya dan tanda tangan Ed25519. Ekspor mencakup seluruh jurnal ruang kerja melalui nomor urut tetap. Filter panel tidak menyaring ekspor; pengumpulan data mungkin berlanjut melampaui batasnya saat ekspor sedang disiapkan.

**Jurnal verifikasi** memeriksa rantai peristiwa dan tanda tangan melalui batas yang ditampilkan. Hasilnya akan dihapus saat ruang kerja berubah, dan panel akan mengidentifikasi catatan baru yang ditambahkan setelah pemeriksaan. Ekspor ZIP juga memverifikasi media yang dikumpulkan.

Tanda tangan yang sah menjamin integritas relatif terhadap kunci tepercaya, bukan asal dari Telegram atau kebenaran isi pesan. Simpan sidik jari dan titik pemeriksaan secara terpisah. Lihat [model bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/), [operasi harian](https://phishdestroy.github.io/TgWitness/id/docs/reference/operations/), dan [prosedur penerimaan langsung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) untuk persyaratan kepercayaan dan pengiriman.
