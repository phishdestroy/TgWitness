# Mengelola arsip

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/archive/

Temukan pesan. Periksa sumbernya. Bangun kasusnya.

01**Menampilkan riwayat**

Muat pesan-pesan sebelumnya dari sumber-sumber yang telah diaktifkan ke dalam ruang kerja.

02**Ikuti sumber-sumbernya**

Cari di arsip dan buka pesan yang disimpan di balik setiap hasil pencarian.

03**Pastikan proses serah terima tetap jelas**

Simpan analisis Anda secara terpisah dan ekspor bukti yang telah ditandatangani di sampingnya.

Catatan yang direkam, teks yang dikenali, dan kesimpulan analis tetap terpisah.

## Muat pesan-pesan sebelumnya

1. Buka **Sumber → Chat dalam cakupan**, tinjau chat yang diaktifkan, lalu mulai pengamatan.
2. Pilih "**Muat riwayat lengkap**". Proses ini menggunakan daftar sumber yang dipilih pada saat itu.
3. Gunakan "**Riwayat Jeda"** dan "**Riwayat Lanjutkan"** sesuai kebutuhan. Setelah restart, lanjutkan secara eksplisit.
4. Periksa hasil per sumber dan antrian lampiran. Simpan laporan kemajuan yang telah ditandatangani bersama ekspor bukti.

Fitur ini mengisi ruang kerja dengan pesan-pesan yang tersedia. Ekspor HTML/JSON per obrolan merupakan operasi terpisah. [Riwayat dan detail pemulihan](https://phishdestroy.github.io/TgWitness/id/docs/reference/history/).

## Cari dulu, baru putuskan soal AI

1. Buka **Jurnal** untuk pencarian lokal. Pilih ruang kerja dan gunakan filter sumber serta waktu.
2. Cari frasa atau domain. Buka catatan yang sesuai beserta versi-versi yang tersimpan.
3. Untuk analisis AI, administrator mengaktifkan dan mengonfigurasi penyedia di **Integrasi**. Buka **Tanyakan ke arsip**, lalu pilih chat dan periode. Tinjau **Data yang dikirim ke model** dan hapus centang pada cuplikan yang tidak diinginkan sebelum menyetujui permintaan.
4. Periksa kutipan yang ditampilkan. Simpan jawaban sebagai laporan dan tambahkan revisi atau catatan Anda sendiri.

Pencarian dijalankan secara lokal tanpa AI. Laporan analitis menyimpan referensi sumber dan riwayat revisi; laporan tersebut terpisah dari jurnal yang telah ditandatangani. [Pengaturan penyedia dan laporan](https://phishdestroy.github.io/TgWitness/id/docs/reference/analysis/).

## Pilih koneksi yang Anda butuhkan

| Tugas | Buka | Pengaturan |
| --- | --- | --- |
| Baca obrolan terpilih dari klien AI | **Integrasi → MCP** | [Instal ekstensi MCP, terbitkan token berskala, dan hubungkan klien](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/) |
| Mengenali teks dalam media yang disimpan | Catatan `media.saved` → **Mengenali lampiran** | [Siapkan worker Docker lokal dan file bahasa/model yang diperlukan](https://phishdestroy.github.io/TgWitness/id/docs/reference/media-analysis/) |
| Kirim peristiwa ke n8n atau SIEM | **Integrasi → Webhook keluar** | [Tambahkan penerima, verifikasi HMAC, dan hapus duplikat ID peristiwa](https://phishdestroy.github.io/TgWitness/id/docs/reference/webhooks/) |

**Token akses mana yang harus ditempatkan di mana?**

Akses panel diperuntukkan bagi pihak yang meninjau kasus. Koneksi MCP mendapatkan token arsip khusus yang hanya dapat dibaca. Penerima webhook menggunakan rahasia HMAC-nya sendiri. Tidak ada yang memerlukan berkas sesi Telegram.

[Bagikan akses panel](https://phishdestroy.github.io/TgWitness/id/docs/access/) atau [konfigurasikan klien MCP](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/).

## Sampaikan sumber dan kesimpulan

Simpan laporan analitis yang telah ditinjau bersama dengan berkas ZIP bukti yang telah ditandatangani. Laporan tersebut menjelaskan interpretasi Anda terhadap sumber-sumber tersebut; sedangkan berkas ZIP memungkinkan penerima memverifikasi catatan yang disimpan dengan membandingkannya terhadap sidik jari dan titik pemeriksaan yang tepercaya secara independen.

[Ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/exports/) · [Melakukan penyelidikan secara menyeluruh](https://phishdestroy.github.io/TgWitness/id/docs/cases/)
