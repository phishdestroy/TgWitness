# Obrolan Rahasia: implementasi dan demo

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/secret-chats/

Pahami implementasi Obrolan Rahasia yang terpisah, coba antarmuka fiktif, dan tinjau masalah yang belum terselesaikan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Status diperiksa pada 6 November 2026:** implementasi Obrolan Rahasia terpisah sedang dalam pengembangan. Implementasi tersebut belum digabungkan ke dalam `main` yang telah diterbitkan pada `3d23e52b647b`. Pengumpul biasa dan ekspor Takeout tidak mengumpulkan data Obrolan Rahasia. Skenario situs web interaktif mendemonstrasikan antarmuka dengan data fiktif; skenario tersebut tidak mengaktifkan komunikasi Telegram.

## Di mana implementasi tersebut berada

Commit `0e60f88e` menambahkan **Sources → Pseudo-secret** di cabang pengembangan lokal `fix/panel-routes-sessions`. Snapshot yang diperiksa adalah `bb8788fb685c`. Implementasinya mencakup `tgwitness/secret_chats.py`, rute aplikasi, `tgwitness/static/views/secret-chats.js`, dan pengujian khusus.

Fitur tambahan `secret-chats` opsional di cabang tersebut menggunakan [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), yang disematkan ke `d87bf037b90060383c7b704d8a06ebb98c621c6f`. Pustaka tersebut mengimplementasikan protokol obrolan ujung-ke-ujung Telegram pada otorisasi Telethon yang sudah ada di akun tersebut. Menginstal pustaka tersebut saja tidak akan menambahkan integrasi yang hilang ke `main`.

## Fungsi antarmuka pengembangan

| Tindakan | Perilaku yang terekam |
| --- | --- |
| Mulai obrolan berdasarkan nama pengguna atau ID pengguna | Kirim permintaan; peserta lain harus menerimanya. |
| Terima permintaan yang masuk | TgWitness menjadi titik akhir penerima untuk obrolan tersebut. Penerimaan otomatis merupakan pengaturan terpisah, yang dinonaktifkan secara default. |
| Mengirim atau menerima pesan | Tambahkan catatan `secret_chat.message` yang keluar atau masuk dan tampilkan di utas percakapan. |
| Terima lampiran | Dekripsi token tersebut, simpan byte-bytenya berdasarkan SHA-256, dan catat `secret_chat.file`. |
| Menerima pemberitahuan timer atau penghapusan | Catat pemberitahuan tersebut dan simpan konten yang telah ditangkap sebelumnya. |
| Tinjau percakapan tersebut | Tampilkan pesan, berkas, pemberitahuan, dan visualisasi kunci. Tab yang terbuka diperbarui setiap empat detik. |

Dalam build pengembangan yang berisi integrasi tersebut, operator mengaktifkan modul untuk akun yang dipilih dan menghubungkannya. Untuk memulai, menerima, dan mengirim, diperlukan izin untuk berinteraksi serta perlindungan baca-saja pada akun tersebut harus dinonaktifkan. Peserta lainnya harus menerima obrolan keluar yang baru. Kontrol-kontrol ini tidak ada dalam aplikasi yang telah dirilis pada revisi di atas.

Hanya obrolan yang dibuat atau diterima oleh sesi TgWitness ini yang tercakup. Obrolan Rahasia yang sudah ada di ponsel tetap berada di perangkat tersebut. Impor sesi tidak menyediakan kunci enkripsi terpisah untuk obrolan tersebut. Materi kunci dan penghitung obrolan rahasia disimpan di brankas ruang kerja; pesan yang disimpan dan berkas yang telah didekripsi mengikuti perlindungan penyimpanan ruang kerja yang biasa.

## Demo situs web

Skenario "**Coba Obrolan Rahasia**" di situs web ini menampilkan percakapan fiktif. Skenario ini memungkinkan pembaca untuk memulai permintaan, mensimulasikan penerimaannya, mengirim pesan contoh, menerima balasan dan berkas yang telah disiapkan, serta memeriksa pengatur waktu dan pemberitahuan penghapusan. Permintaan yang masuk juga dapat diterima. Kontrol-kontrol tersebut secara eksplisit memberi label pada tindakan rekan yang disimulasikan.

Skenario ini berjalan di memori browser. Mengatur ulang atau memuat ulang akan menghapusnya. Skenario ini tidak melakukan login, menghubungi Telegram, membuat kunci enkripsi yang sebenarnya, atau mengubah unduhan sampel yang telah ditandatangani. Pesan yang ditampilkan bukanlah bukti yang ditandatangani. Skenario ini mendemonstrasikan interaksi yang dimaksudkan; skenario ini tidak menjamin bahwa implementasi pengembangan sudah siap.

## Pemeriksaan dan cacat yang belum diperbaiki

Lima pengujian yang ada mencakup persistensi kunci terenkripsi, siklus hidup, dan catatan pesan, kebijakan penerimaan masuk, pengiriman hanya-baca, serta ekspor lampiran. Pengujian tersebut lulus saat diuji terhadap pustaka yang disematkan selama tinjauan pada tanggal 6 November. Tiga pemeriksaan sintetis tambahan mereproduksi cacat pada snapshot yang sama:

| Temuan | Konsekuensi |
| --- | --- |
| Penutupan melewati `read_only` | Jalur penutupan dapat melakukan tindakan jarak jauh ketika interaksi harus diblokir. |
| Pencarian duplikat hanya dilakukan pada catatan terbaru 500 | Replay yang lebih lama dapat menghasilkan duplikat setelah restart. |
| Unduhan lampiran yang gagal akan menghapus entri yang tertunda | Kegagalan sementara akan menyebabkan tugas percobaan ulang hilang. |

Ini adalah cacat yang terbuka, yang juga tercatat dalam audit [yang telah dipublikasikan](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md). Lima uji yang lulus tidak mencakup kegagalan ini. Peninjauan tersebut menggunakan ruang kerja sintetis dan simulasi operasi Telegram; peninjauan tersebut tidak mengulangi proses handshake langsung atau menguji penerapan di lingkungan produksi.
