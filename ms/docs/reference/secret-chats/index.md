# Telegram · Perbualan Rahsia: pelaksanaan dan demo

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/secret-chats/

Fahami pelaksanaan Secret Chat yang berasingan, cuba antaramuka fiksyen dan semak kecacatan yang belum diselesaikan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Status disemak pada 6 November 2026:** terdapat pelaksanaan Secret Chat berasingan yang sedang dibangunkan. Ia belum digabungkan ke dalam `main` yang diterbitkan di `3d23e52b647b`. Pengumpul biasa dan eksport Takeout tidak mengumpul Secret Chats. Senario laman web interaktif menunjukkan antara muka dengan data rekaan; ia tidak membolehkan komunikasi Telegram.

## Di mana pelaksanaan berada

Komit `0e60f88e` menambah **Sources → Pseudo-secret** dalam cawangan pembangunan tempatan `fix/panel-routes-sessions`. Snapshot yang diperiksa ialah `bb8788fb685c`. Pelaksanaannya merangkumi `tgwitness/secret_chats.py`, laluan aplikasi, `tgwitness/static/views/secret-chats.js` dan ujian khusus.

`secret-chats` ekstra pilihan dalam cabang itu menggunakan [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), yang dipautkan ke `d87bf037b90060383c7b704d8a06ebb98c621c6f`. Perpustakaan ini melaksanakan protokol sembang hujung-ke-hujung Telegram pada kebenaran Telethon sedia ada pada akaun. Menginstall perpustakaan itu sahaja tidak menambah integrasi yang hilang ke `main`.

## Apa yang dilakukan oleh antara muka pembangunan

| Tindakan | Tingkah laku yang direkod |
| --- | --- |
| Mulakan sembang dengan nama pengguna atau ID pengguna | Hantar permintaan; peserta lain mesti menerimanya. |
| Terima permintaan masuk | TgWitnessmenjadi titik akhir penerima untuk sembang tersebut. Penerimaan automatik adalah tetapan berasingan, dimatikan secara lalai. |
| Hantar atau terima mesej | Tambah rekod `secret_chat.message` keluar atau masuk dan tunjukkan dalam utas. |
| Menerima lampiran | Dekripsi ia, simpan baitnya mengikut SHA-256 dan rekod `secret_chat.file`. |
| Terima pemberitahuan pemasa atau pemadaman | Rekod pemberitahuan dan simpan kandungan yang telah dirakam sebelum ini. |
| Semak perbualan | Tunjukkan mesej, fail, notis dan visualisasi utama. Tab terbuka dikemas kini setiap empat saat. |

Dalam binaan pembangunan yang mengandungi integrasi, pengendali mengaktifkan modul untuk akaun yang dipilih dan menyambungkannya. Memulakan, menerima dan menghantar memerlukan kebenaran untuk berinteraksi dan perlindungan baca sahaja akaun tersebut perlu dimatikan. Peserta lain mesti menerima sembang keluar baru. Kawalan ini tidak wujud dalam aplikasi yang diterbitkan pada semakan di atas.

Hanya sembang yang dibuat atau diterima oleh sesi TgWitness ini dilindungi. Sembang Rahsia sedia ada pada telefon kekal pada peranti tersebut. Import sesi tidak membekalkan kunci penyulitan berasingan mereka. Bahan kunci sembang rahsia dan pengira disimpan dalam bilik perbendaharaan ruang kerja; mesej yang dipelihara dan fail yang disahsulitkan mengikuti perlindungan penyimpanan ruang kerja biasa.

## Demonstrasi laman web

Senario "**Try Secret Chat**" di laman web membuka perbualan fiksyen. Ia membolehkan pembaca memulakan permintaan, mensimulasikan penerimaannya, menghantar mesej contoh, menerima balasan berskrip dan fail, serta memeriksa pemasa dan notis pemadaman. Permintaan masuk juga boleh diterima. Kawalan melabel tindakan rakan sebaya yang disimulasikan secara eksplisit.

Senario ini dijalankan dalam memori pelayar. Menetap semula atau memuat semula akan membersihkannya. Ia tidak log masuk, menghubungi Telegram, mencipta kunci penyulitan sebenar atau mengubah muat turun sampel yang ditandatangani. Mesej yang dipaparkan bukan bukti yang disahkan. Senario ini menunjukkan interaksi yang dimaksudkan; ia tidak mengesahkan bahawa pelaksanaan pembangunan sudah siap.

## Semakan dan kecacatan yang belum diselesaikan

Lima ujian sedia ada merangkumi ketahanan kunci yang disulitkan, kitar hayat dan rekod mesej, dasar penerimaan masuk, penghantaran baca sahaja dan eksport lampiran. Mereka lulus terhadap perpustakaan yang dipasang semasa semakan 6 November. Tiga semakan sintetik tambahan menghasilkan semula kecacatan dalam snapshot yang sama:

| Penemuan | Konsekuensi |
| --- | --- |
| Penutupan memintas`read_only` | Laluan rapat boleh melaksanakan tindakan jauh apabila interaksi perlu disekat. |
| Pengesanan duplikat hanya mencari rekod terkini 500 | Penyiaran semula yang lebih lama boleh mencipta duplikat selepas memulakan semula. |
| Muat turun lampiran yang gagal akan membuang kemasukannya yang tertangguh | Kegagalan sementara menyebabkan kehilangan tugas percubaan semula. |

Ini adalah kecacatan terbuka, juga direkodkan dalam [audit yang diterbitkan](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md). Lima ujian lulus tidak merangkumi kegagalan ini. Semakan ini menggunakan ruang kerja sintetik dan meniru operasi Telegram; ia tidak mengulangi jabat tangan langsung atau mengesahkan penyebaran pengeluaran.
