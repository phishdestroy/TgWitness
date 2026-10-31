# Analisis arsip

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/analysis/

Cari pesan yang disimpan, tinjau masukan AI, dan simpan laporan analitis beserta referensi sumbernya.

**Versi utama saat ini:** gunakan checkout sumber; pratinjau portabel 0.7.0 dirilis sebelum fitur ini tersedia.

[Panduan alur kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Buka **"Ask the archive**" di panel. Pemilih ruang kerja menentukan akun; formulir memilih obrolan dan periode pengamatan. Pencarian dijalankan secara lokal, tanpa AI. Frasa atau domain yang tepat mempersempit hasil pencarian; ID pesan meminta versi yang disimpan. Tinjau cuplikan yang ditampilkan dan buka catatan jurnal atau konteksnya. Tidak ada basis data vektor atau tindakan otomatis di Telegram.

## Penyedia layanan dan persetujuan

AI dinonaktifkan secara default di setiap ruang kerja. Hanya administrator utama yang dapat mengonfigurasi model, titik akhir (endpoint), kunci API terenkripsi, batas konteks/keluaran, batas waktu, dan kuota permintaan harian. Kunci tersebut tidak pernah dikembalikan ke browser. Biarkan kolom kunci kosong untuk mempertahankan kunci saat ini, atau hapus secara eksplisit.

Ollama menggunakan [titik akhir `/api/chat`](https://docs.ollama.com/api/chat) yang terdokumentasi dengan keluaran JSON non-streaming. Alamat defaultnya adalah `http://127.0.0.1:11434` di server TgWitness. Operator dapat mengubahnya menggunakan `TGWITNESS_AI_LOCAL_ENDPOINT`; ini bukanlah alamat yang dikendalikan oleh model. Pasang model yang dipilih sendiri. TgWitness tidak mengunduhnya secara otomatis.

Penyedia yang kompatibel mengharuskan URL dasar yang berakhiran `/v1` serta [protokol Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, mode respons JSON, `max_completion_tokens`, dan `choices[0].message.content`. Layanan yang tidak memiliki bidang-bidang ini tidak didukung. Pengujian koneksi mengirimkan teks sintetis dan dihitung dalam kuota permintaan.

Setiap permintaan menggunakan rute eksternal yang telah dikonfigurasi di ruang kerja. Rute yang diblokir atau MTProxy khusus Telegram akan menimbulkan kesalahan; tidak ada upaya ulang langsung. Alamat Ollama lokal yang dikonfigurasi secara sengaja memungkinkan tujuan pribadi, sambil tetap menggunakan rute yang dipilih. Untuk layanan pribadi lainnya, opsi tujuan pribadi tingkat server yang sudah ada berlaku. Panel menampilkan titik akhir yang sebenarnya telah dikonfigurasi.

Sebelum proses pembangkitan, **data yang dikirim ke model** mencakup permintaan: pertanyaan, kutipan yang diperiksa, jenis peristiwa, waktu pengamatan, dan penanda cakupan. Sesi Telegram, bidang mentah, kunci penyedia, byte lampiran, dan jurnal lengkap tidak termasuk dalam konteks tersebut. Hapus centang pada sumber yang tidak diinginkan, lalu setujui secara eksplisit proses pengolahan. Penyedia eksternal mungkin menyimpan konten yang dikirimkan sesuai dengan kebijakan mereka sendiri. Eksekusi lokal berarti titik akhir berada di lokal; hal ini bukan jaminan terkait perilaku layanan yang dikonfigurasi secara independen.

Secara global, terdapat paling banyak dua permintaan penyedia yang berjalan bersamaan dan satu per ruang kerja. Pratinjau akan kedaluwarsa setelah sepuluh menit dan dapat menghasilkan satu jawaban. Jumlah token yang dilaporkan oleh penyedia ditampilkan; perkiraan biaya hanya muncul jika tarif input dan output telah dikonfigurasi. Upaya yang gagal juga menghabiskan anggaran permintaan harian. Tidak ada upaya ulang otomatis yang menghabiskan anggaran tambahan.

## Sumber dan batasan

Fitur pencarian memeriksa teks pesan yang disimpan dengan pencarian leksikal yang dibatasi. Fitur ini mengembalikan hingga 24 sumber dan menandai kutipan yang terpotong atau kumpulan hasil yang tidak lengkap. Periode tersebut merujuk pada **waktu pengamatan**, bukan klaim bahwa riwayat Telegram lengkap. Peristiwa yang mencakup seluruh ruang kerja tidak disertakan dalam akses yang terbatas pada obrolan. Data yang hilang dijelaskan sebagai tidak ditemukan dalam arsip yang tersedia.

Model ini tidak menerima alat apa pun. ID sumbernya diverifikasi berdasarkan catatan yang dipilih, hash diperiksa ulang, dan string yang dikutip harus terdapat dalam catatan tersebut. ID yang tidak dikenal, kutipan yang diubah, dan klaim tanpa sumber akan menolak jawaban tersebut. Aplikasi ini membuat tautan; URL yang dihasilkan model tidak digunakan sebagai kutipan. Pemeriksaan ini memastikan keberadaan sumber dan keakuratan kutipan, bukan kebenaran suatu kesimpulan. Tinjau kesimpulan tersebut berdasarkan catatan sebelum mengandalkannya.

## Laporan

Simpan jawaban yang telah ditinjau sebagai laporan analitis terpisah. Laporan ini mencakup ringkasan model, urutan kronologis yang diamati, tautan dan handle yang diekstraksi, catatan pengeditan/penghapusan, batasan cakupan, serta hash peristiwa sumber. Penyedia, model, titik akhir, waktu, dan versi templat prompt juga disertakan. Identitas apa pun tidak digabungkan secara otomatis.

Revisi dan catatan analis disimpan terpisah dari ringkasan model. Laporan disimpan dalam berkas turunan yang terenkripsi, dengan indeks di luar aliran peristiwa yang ditandatangani; peristiwa dan media asli tidak berubah. Hanya pemilik atau administrator yang dapat membuka laporan, dan akses sumber diperiksa kembali. Pengunduhan juga memerlukan izin ekspor. Versi 1 tidak menandatangani laporan atau menyiratkan bahwa kesimpulan model merupakan bukti yang terverifikasi. Batasan: 100 laporan per ruang kerja dan 100 revisi analis per laporan.

Untuk OCR manual dan transkrip, lihat [pemrosesan media](https://phishdestroy.github.io/TgWitness/id/docs/reference/media-analysis/). Untuk akses klien, lihat [MCP](https://phishdestroy.github.io/TgWitness/id/docs/reference/mcp/).
