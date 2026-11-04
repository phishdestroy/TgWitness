# Mengelola arsip

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/archive/

Temukan pesan. Periksa sumbernya. Bangun kasusnya.

01**Menampilkan riwayat**

Tarik pesan lama dari sumber aktif Anda ke ruang kerja.

02**Ikuti sumber-sumbernya**

Cari, lalu buka pesan tersimpan di balik setiap hasil.

03**Pastikan proses serah terima tetap jelas**

Analisis Anda di satu berkas, bukti bertanda tangan di sebelahnya.

Catatan yang direkam, teks yang dikenali, dan kesimpulan analis tetap terpisah.

## Muat pesan-pesan sebelumnya

1. **Sumber → Obrolan dalam cakupan**: periksa obrolan aktif, mulai pengamatan.
2. **Muat seluruh riwayat**. Daftar sumber diambil apa adanya saat itu.
3. **Jeda riwayat** / **Lanjutkan riwayat** kapan saja. Setelah dimulai ulang, lanjutkan secara manual.
4. Periksa hasil per sumber dan antrean unduhan, simpan laporan kemajuan bertanda tangan bersama ekspor.

Ini mengisi ruang kerja. Ekspor satu obrolan ke HTML/JSON adalah hal lain. [Detail](https://phishdestroy.github.io/TgWitness/id/docs/reference/history/).

## Cari dulu, baru putuskan soal AI

1. **Jurnal** mencari secara lokal, dengan filter sumber dan waktu.
2. Cari frasa atau domain, buka catatannya dan versinya.
3. Untuk AI, admin menyiapkan penyedia di **Integrasi**. Lalu **Tanya arsip**: pilih obrolan dan periode, lihat **Data yang dikirim ke model**, dan hapus centang yang tidak boleh keluar.
4. Periksa kutipannya, simpan jawaban sebagai laporan, tambahkan catatan Anda.

Pencarian tidak butuh AI. Laporan menyimpan sumber dan revisinya, terpisah dari jurnal bertanda tangan. [Penyiapan penyedia](https://phishdestroy.github.io/TgWitness/id/docs/reference/analysis/).

## Pilih koneksi yang Anda butuhkan

| Tugas | Buka | Pengaturan |
| --- | --- | --- |
| Izinkan klien AI membaca obrolan pilihan | **Integrasi → MCP** | [Pasang MCP, buat token terbatas, sambungkan](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/) |
| Mengenali teks dalam media yang disimpan | Catatan `media.saved` → **Mengenali lampiran** | [Siapkan worker Docker lokal](https://phishdestroy.github.io/TgWitness/id/docs/reference/media-analysis/) |
| Kirim peristiwa ke n8n atau SIEM | **Integrasi → Webhook keluar** | [Tambahkan penerima, periksa HMAC, buang ID ganda](https://phishdestroy.github.io/TgWitness/id/docs/reference/webhooks/) |

**Token akses mana yang harus ditempatkan di mana?**

Akses panel untuk manusia. MCP punya token baca-saja sendiri, webhook punya rahasia HMAC sendiri. Tidak ada yang butuh sesi Telegram.

[Bagikan akses panel](https://phishdestroy.github.io/TgWitness/id/docs/access/) atau [konfigurasikan klien MCP](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/).

## Sampaikan sumber dan kesimpulan

Taruh laporan di sebelah ZIP bertanda tangan. Laporan adalah bacaan Anda atas sumbernya; ZIP adalah yang diverifikasi penerima.

[Ekspor dan verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/exports/) · [Melakukan penyelidikan secara menyeluruh](https://phishdestroy.github.io/TgWitness/id/docs/cases/)
