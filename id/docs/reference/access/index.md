# Akses dan izin

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/access/

Tentukan cakupan akses ke akun dan obrolan, pilih izin, batasi sesi dan alamat IP, serta cabut akses.

Berikan akses kepada peninjau ke satu obrolan, izin kepada analis untuk mengekspor suatu kasus, atau kontrol kepada operator atas akun-akun yang dipilih. Setiap orang mendapatkan tokennya masing-masing. Token panel utama tetap berada di tangan administrator.

[Pengaturan akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/) · [Rute koneksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/connection/) · [Model keamanan](https://phishdestroy.github.io/TgWitness/id/docs/reference/security/)

## Dua cakupan, dua tugas yang berbeda

**Cakupan pengumpulan** menentukan apa yang direkam oleh suatu akun: obrolan terpilih, folder Telegram, atau seluruh akun. **Cakupan akses** menentukan akun dan obrolan mana saja dari yang telah direkam tersebut yang dapat dilihat dan digunakan oleh orang lain. Memberikan akses tidak berarti bergabung ke obrolan Telegram, memulai pengumpulan, atau memberikan izin akun Telegram.

Akses dapat membuka ruang kerja yang dipilih, obrolan tertentu di dalamnya, atau semua ruang kerja. **Semua ruang kerja, termasuk yang ditambahkan kemudian**, juga mencakup akun di masa mendatang. Pilih ruang kerja secara eksplisit jika suatu kasus harus dibatasi hanya pada ruang kerja tersebut.

## Berikan akses kepada seseorang

1. Masuk sebagai administrator utama dan buka **Akses**.
2. Di bawah bagian "**Berikan akses kepada seseorang**", masukkan nama yang akan Anda kenali dalam log.
3. Pilih ruang kerja dan, jika diperlukan, obrolan individu.
4. Pilih tindakan yang mungkin dilakukan oleh orang ini. Opsi "**Lihat"** selalu disertakan.
5. Tentukan masa berlaku, batas masuk/sesi, dan alamat yang diizinkan sesuai kebutuhan.
6. Tekan **"Buat Akses**". Salin token sekarang: token ini hanya ditampilkan sekali.
7. Kirim alamat panel dan token secara pribadi. Penerima memasukkan token tersebut di halaman masuk biasa; mereka tidak memerlukan token panel utama Anda atau sesi Telegram.

Buka panel yang berisi token yang diterbitkan dalam sesi browser terpisah dan periksa obrolan yang terlihat serta tindakan yang diizinkan sebelum menyerahkannya.

## Pilih izin

| Izin | Fitur yang ditawarkan |
| --- | --- |
| `view` | Baca obrolan yang diizinkan, pesan yang direkam, profil, berkas, dan catatan jurnal yang telah difilter. Selalu disertakan. |
| `export` | Ekspor riwayat obrolan dan berkas yang diizinkan. Ekspor bukti seluruh ruang kerja memerlukan akses ke seluruh ruang kerja. |
| `sources` | Kelola sumber, snapshot, dan penangkapan profil. Akses terbatas pada obrolan hanya dapat diterapkan pada obrolan yang diizinkan; penemuan sumber dan pengaturan cakupan di seluruh akun tetap dinonaktifkan. |
| `collect` | Memulai atau menghentikan pengumpul data. Membutuhkan akses ke seluruh ruang kerja karena pengumpulan data memengaruhi akun. |
| `interact` | Lakukan interaksi Telegram yang didukung dalam lingkup akses. Akses terbatas pada obrolan tidak dapat menggunakan pratinjau tautan di seluruh akun. |
| `settings` | Ubah pengaturan pengumpulan data, cap waktu, pemberitahuan, salinan di luar situs, dan parameter. Membutuhkan akses ke seluruh ruang kerja. |
| `account` | Masuk atau keluar dari Telegram dan kelola rute koneksi. Membutuhkan akses ke seluruh ruang kerja. |

Izin dan cakupan diperiksa secara bersamaan. Mencentang suatu izin tidak akan membuka obrolan lain atau membuka operasi di seluruh ruang kerja untuk akses yang terbatas pada obrolan tertentu. Untuk ekspor paralel, akses harus mencakup obrolan yang diekspor di setiap akun yang dipilih. Akses yang diterbitkan tidak dapat membuat akses baru, mengelola sesi orang lain, atau membuka konsol administrator.

### Tiga pengaturan yang berguna

| Orang | Ruang Lingkup | Izin |
| --- | --- | --- |
| Peninjau | Percakapan yang direkam dari satu kasus | `view` |
| Analis yang sedang mempersiapkan serah terima | Percakapan yang akan diselidiki dan diekspor | `view`, `export`; tambahkan `interact` hanya jika mereka harus bertindak melalui Telegram |
| Operator pengumpulan data | Ruang kerja yang dipilih secara keseluruhan | `view`, `sources`, `collect`; tambahkan `settings` atau `account` hanya jika diperlukan |

Ini adalah contoh yang Anda konfigurasikan melalui kotak centang izin, bukan peran yang tetap.

## Batasan dan sesi

| Pengaturan | Cara kerjanya |
| --- | --- |
| Sesi paralel | Batasi sesi simultan menjadi 1–100. Saat mencapai batas tersebut, tolak upaya masuk berikutnya atau akhiri sesi yang paling lama. |
| Masuk diperbolehkan | Batasi penggunaan token yang berhasil untuk memulai sesi. Sesi yang sudah ada tidak akan berakhir hanya karena batas masuk terakhir yang diizinkan telah digunakan. |
| Berlaku hingga | Akses ini memiliki batas waktu kedaluwarsa yang mutlak. Akses yang telah kedaluwarsa tidak dapat masuk atau terus melakukan permintaan. |
| Menit tanpa aktivitas | Batas waktu ketidakaktifan sesi, mulai dari 5 menit hingga 30 hari. Permintaan yang berhasil akan memperpanjangnya; panel yang terbuka dapat mempertahankan status aktifnya dengan melakukan polling. |
| Alamat yang diizinkan | Terima alamat IP tertentu atau subnet CIDR. Biarkan kosong untuk mengizinkan alamat apa pun kecuali jika pengikatan saat masuk pertama kali diaktifkan. |
| Terikat pada sesi masuk pertama | Pendaftaran pertama yang berhasil akan menetapkan alamat yang diizinkan untuk akses tersebut. |

IP adalah alamat klien yang terlihat oleh aplikasi. Jika berada di balik proxy terbalik atau terowongan, periksa alamat yang ditampilkan di "**Sesi Terbuka"** sebelum mengandalkan aturan IP: jika tidak, beberapa pengguna mungkin tampak berbagi alamat proxy tersebut.

## Mengubah atau mencabut akses

Edit entri di bawah **Akses** untuk mengubah cakupan, izin, atau batasannya. Perubahan cakupan dan izin akan diperiksa pada permintaan berikutnya, termasuk permintaan dari sesi yang sudah terbuka. Mencabut akses akan mengakhiri sesi tersebut dan membuat token yang diterbitkan tidak dapat digunakan lagi. **Sesi terbuka** juga memungkinkan administrator mengakhiri sesi individu tanpa mencabut seluruh akses.

Pencabutan tidak dapat menarik kembali berkas yang telah diunduh oleh seseorang. Keluar dari akun, mengunci panel, atau mengakhiri sesi tidak akan menghentikan pengumpul yang sedang berjalan.

## Apa yang dapat dilihat oleh administrator

**Log sejak awal ini** menggabungkan log proses dengan aktivitas jurnal dari setiap ruang kerja: masuk, penolakan, perubahan rute, dan tindakan operator. Ini adalah konsol dalam memori untuk proses saat ini, bukan salinan permanen dari setiap pesan. Peristiwa pesan yang sering terjadi tetap tersimpan dalam jurnal daripada memenuhi konsol.

Penerbitan, perubahan, dan pencabutan akses, serta memulai atau mengakhiri sesi, juga menghasilkan catatan jurnal `access.*` yang ditandatangani. Token tidak termasuk dalam catatan tersebut. Token yang diterbitkan dan kredensial sesi disimpan sebagai hash di brankas terenkripsi.

****Administrator utama dan batas kepercayaan**** Token panel utama tetap tidak dibatasi. Masuk melalui browser menggunakan token tersebut akan membuat sesi yang tunduk pada batas sesi yang dikonfigurasi oleh administrator. Skrip yang mengirimkan token utama secara langsung tetap memiliki akses penuh dan tidak dihitung sebagai sesi browser. Ini adalah kontrol akses tingkat aplikasi dalam satu instalasi. Semua ruang kerja berbagi proses server; ini bukan isolasi dari administrator host. Jaga kerahasiaan token utama, sesi Telegram, kunci penandatanganan, dan direktori data. Token saksi adalah kredensial titik pemeriksaan/kesehatan terpisah, bukan token akses panel.
