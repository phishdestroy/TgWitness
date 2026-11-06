# Telegram · Galeri publik

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/showcase/

Publikasikan pesan yang disimpan dari saluran publik yang dipilih serta snapshot yang ditandatangani melalui tautan yang kedaluwarsa dan dapat dicabut.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penerapan dan pemulihan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/)

![Penerapan & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

**Akses → Galeri Publik** membuat halaman terpisah yang hanya dapat dibaca menggunakan sistem token akses yang sudah ada. Halaman ini membaca pengamatan yang disimpan oleh instalasi. Halaman ini tidak menjalankan pengumpul data, masuk ke Telegram, atau memperoleh saluran untuk pengunjung.

## Publikasikan halaman

1. Simpan profil sumber untuk setiap saluran publik yang ingin Anda tampilkan. Sebuah saluran harus memiliki nama pengguna publik dalam profil terbarunya yang tersimpan; grup dan obrolan pribadi tidak memenuhi syarat.
2. Buka **Akses → Galeri publik** (atau `/showcase-manage.html`) sebagai administrator.
3. Pilih saluran dari maksimal 16 ruang kerja, masukkan judul halaman publik, dan pilih masa berlaku tautan selama 1, 7, atau 30 hari. Label ruang kerja internal tidak dipublikasikan. Maksimal 64 saluran dapat disertakan.
4. Tinjau teks dari saluran yang dipilih untuk dipublikasikan, lalu klik **Pratinjau catatan yang dipilih**. Pratinjau ini menggunakan proyeksi sisi server yang sama dengan halaman pengunjung.
5. Klik **"Buat tautan showcase**". Salin tautan tersebut selagi masih terlihat. Buka tautan tersebut di peramban terpisah untuk meninjau halaman penerima sebelum membagikannya.

Tautan tersebut berisi token akses dalam fragmen URL-nya. Halaman ini menghapus fragmen tersebut sebelum melakukan permintaan API dan menukarnya dengan sesi browser. Siapa pun yang memiliki tautan tersebut dapat membuka materi yang dipilih hingga masa berlakunya habis atau dicabut. Tautan baru memungkinkan 100 sesi bersamaan, masing-masing berdurasi maksimal satu jam. Kontrol akses yang ada juga dapat memberlakukan pembatasan alamat dan batas masuk melalui API grant. Akses peninjau biasa merupakan mode yang berbeda dan tetap mencakup pesan serta berkas yang diizinkan semula.

## Apa yang dilihat pengunjung

| Terlihat | Dijaga kerahasiaannya |
| --- | --- |
| Judul saluran publik terpilih, nama pengguna, dan tanggal pengamatan profil | Identitas akun, label ruang kerja internal, dan sumber yang tidak dipilih |
| Teks yang ditangkap dan setiap pengeditan yang disimpan | ID pengirim terstruktur, nama, nama pengguna, nomor telepon, dan nilai profil |
| Penghapusan catatan beserta teks yang telah disimpan sebelumnya, jika tersedia | Lampiran, avatar, gambar mini, nama file, dan muatan asli |
| Penanda yang menunjukkan bahwa seorang penulis/profil atau lampiran telah direkam | Metadata penerusan dan balasan, rute jaringan, alamat IP, dan kredensial |
| Jumlah peristiwa saluran terpilih, pengaturan koleksi saat ini, interval heartbeat, dan interval checkpoint | Kontrol koleksi dan API ekspor bukti standar |
| Jejak penandatanganan, titik pemeriksaan jurnal, dan bukti konsistensi | Kunci penandatanganan dan sesi Telegram |

**Teks pesan publik tidak dianonimkan secara otomatis.** Nama, sebutan, nomor telepon, atau tautan yang ditulis dalam pesan tetap menjadi bagian dari teks tersebut. `Redacted`Berlaku untuk bidang penulis/profil yang terstruktur. Periksa kembali konten yang sebenarnya dipilih sebelum mempublikasikannya, termasuk suntingan dan penghapusan yang dipertahankan.

Kelayakan mencerminkan **profil sumber terbaru yang disimpan**, bukan pencarian Telegram secara langsung. Jika profil berikutnya tidak lagi memiliki nama pengguna saluran publik, permintaan baru tidak akan menyertakan saluran tersebut. Segarkan profil sumber saat visibilitas publik berubah. Pembaca mungkin sudah menyimpan materi yang sebelumnya mereka terima.

Catatan asli yang telah ditandatangani tetap tidak berubah. Proyeksi yang ditampilkan ditandatangani secara terpisah dan memuat hash yang merujuk pada catatan aslinya. Tanda tangan proyeksi mengautentikasi pernyataan yang ditampilkan; ini bukanlah tanda tangan peristiwa asli atas byte yang telah disunting.

## Periksa tanda tangan dan kesinambungan

Perluas **"Fingerprint & signed checkpoint"** dan unduh snapshot. Setelah halaman diperbarui, unduhan tersebut mencakup snapshot browser sebelumnya dan bukti konsistensi Merkle antara batas-batas jurnal mereka. Pembaruan otomatis dilakukan sekali setiap menit selama halaman tersebut terlihat dan menampilkan halaman pertama pengamatannya.

Setelah menginstal TgWitness, verifikasi berkas yang diunduh secara offline:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

Sidik jari harus berasal dari referensi tepercaya yang terpisah. Untuk membandingkannya dengan snapshot yang Anda simpan sendiri, gunakan `--previous earlier.json`; ini akan menggantikan snapshot sebelumnya yang terdapat dalam unduhan. Bukti saat ini harus dimulai pada batas yang telah disimpan tersebut. Klien yang terotentikasi dapat meminta bukti tersebut menggunakan `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Jurnal yang lebih pendek akan mengembalikan HTTP 409 alih-alih secara diam-diam mengatur ulang batas tersebut.

Titik pemeriksaan yang ditandatangani mencakup **seluruh jurnal pengumpul**, termasuk jumlah catatannya dan hash kepala yang tidak transparan. Jumlah pesan yang ditampilkan hanya berlaku untuk saluran publik yang dipilih. Halaman ini tidak pernah mencantumkan isi jurnal lainnya. Ini adalah jumlah peristiwa, bukan jumlah pesan unik. Pengaturan tersebut menggambarkan konfigurasi saat ini, bukan setiap interval perekaman sebelumnya.

Verifikasi tanda tangan dan konsistensi dapat mendeteksi perubahan relatif terhadap batas yang disimpan. Verifikasi ini tidak menghitung ulang penghitung yang ditandatangani secara independen, mengesahkan asal Telegram, menunjukkan pencatatan tanpa gangguan, atau menggantikan saksi independen. Untuk tinjauan tersebut, gunakan [verifikator bukti](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [saksi independen](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/), dan [catatan berskala teruji](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/). Instalasi sintetis diberi label yang jelas sebagai sintetis.

## Batalkan atau host halaman ini

Gunakan **Revoke** di manajer showcase atau bagian **Akses** yang ada untuk menutup tautan dan mengakhiri semua sesinya. Pengunjung akan menghapus catatan yang ditampilkan ketika permintaan mendeteksi bahwa akses telah berakhir. Masa berlaku dan izin diperiksa pada setiap permintaan. Izin showcase tidak dapat dikonversi menjadi akses panel biasa di tempat; buat izin baru untuk mengubah mode.

Sajikan halaman ini melalui alamat HTTPS yang sudah ada pada instalasi. Mempublikasikan tautan tidak akan membuka port baru, membuat terowongan, atau mengubah DNS. Kode HTML dan API tetap berada di instalasi pengguna. Pengunjung showcase tidak dapat menggunakan API pesan, profil, media, ekspor, atau manajemen biasa dengan akses ini.
