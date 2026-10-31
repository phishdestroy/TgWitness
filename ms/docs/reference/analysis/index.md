# Analisis arkib

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/analysis/

Cari mesej yang disimpan, semak input AI dan simpan laporan analitik beserta rujukan sumbernya.

**Utama semasa:** gunakan checkout sumber; pratonton mudah alih 0.7.0 wujud sebelum ciri ini.

[Panduan aliran kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Gunakan **Jurnal** untuk carian tempatan tanpa AI. Untuk **Tanya arkib**, dayakan dan konfigurasikan penyedia dalam **Integrasi** terlebih dahulu. Pemilih ruang kerja memilih akaun; borang memilih sembang dan tempoh pemerhatian. Pengambilan semula dijalankan secara tempatan. Frasa tepat atau domain menyempitkan pengambilan semula; ID mesej meminta versi yang disimpan. Semak petikan dan buka rekod jurnal atau konteksnya. Tiada pangkalan data vektor atau tindakan Telegram automatik.

## Penyedia dan persetujuan

AI dihidupkan secara lalai dalam setiap ruang kerja. Hanya pentadbir utama boleh mengkonfigurasi model, hujung, kunci API yang disulitkan, had konteks/keluar, masa tamat dan bajet permintaan harian. Kunci tidak pernah dikembalikan ke pelayar. Biarkan medan kunci kosong untuk mengekalkan kunci semasa, atau menghapuskannya secara nyata.

Ollama menggunakan [titik akhir `/api/chat`](https://docs.ollama.com/api/chat) yang didokumentasikan dengan keluaran JSON bukan penstriman. Alamat lalainya ialah `http://127.0.0.1:11434` pada pelayan TgWitness. Pengendali boleh menukarnya menggunakan `TGWITNESS_AI_LOCAL_ENDPOINT`; ini bukan alamat dikawal oleh model. Pasang model yang dipilih sendiri. TgWitness tidak memuat turunnya secara automatik.

Penyedia yang serasi menjangkakan URL asas yang berakhir dengan `/v1` dan [protokol Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, mod respons JSON, `max_completion_tokens`, dan `choices[0].message.content`. Perkhidmatan yang tidak mempunyai medan ini tidak disokong. Ujian sambungan menghantar teks sintetik dan dikira ke dalam bajet permintaan.

Setiap permintaan menggunakan laluan luar yang dikonfigurasikan oleh ruang kerja. Route yang disekat atau MTProxy hanya untuk Telegram adalah ralat; tiada percubaan semula secara langsung. Alamat Ollama tempatan yang dikonfigurasikan secara sengaja membenarkan destinasi peribadi, sambil masih menggunakan route yang dipilih. Untuk perkhidmatan peribadi lain, pilihan untuk menggunakan destinasi peribadi peringkat pelayan sedia ada terpakai. Panel memaparkan titik akhir yang sebenar dikonfigurasikan.

Sebelum penjanaan, **data yang dihantar ke model** memaparkan permintaan: soalan, petikan yang disemak, jenis peristiwa, masa pemerhatian dan penanda liputan. Sesi Telegram, medan mentah, kunci penyedia, bait lampiran dan jurnal penuh bukan sebahagian daripada konteks tersebut. Nyahpilih sumber yang tidak diingini, kemudian luluskan pemprosesan secara eksplisit. Penyedia luaran mungkin mengekalkan kandungan yang dihantar di bawah dasar mereka sendiri. Pelaksanaan tempatan bermaksud titik akhir adalah tempatan; ia bukan jaminan mengenai tingkah laku perkhidmatan yang dikonfigurasikan secara bebas.

Terdapat paling banyak dua permintaan penyedia serentak di seluruh dunia dan satu bagi setiap ruang kerja. Pratonton akan tamat tempoh selepas sepuluh minit dan boleh menjana satu jawapan. Bilangan token yang dilaporkan oleh penyedia dipaparkan; anggaran kos akan muncul hanya apabila kedua-dua tarif input dan output telah dikonfigurasikan. Percubaan yang gagal juga menggunakan bajet permintaan harian. Tiada percubaan semula automatik yang menggunakan bajet tambahan.

## Sumber dan had

Pemulihan memeriksa teks mesej yang disimpan dengan carian leksikal terhad. Ia memaparkan sehingga 24 sumber dan menandakan petikan yang dipotong atau set keputusan yang tidak lengkap. Tempoh merujuk kepada **masa pemerhatian**, bukan dakwaan bahawa sejarah Telegram adalah lengkap. Acara liputan merentas ruang kerja disembunyikan daripada capaian skop sembang. Data yang hilang diterangkan sebagai tidak ditemui dalam arkib yang tersedia.

Model tidak menerima sebarang alat. ID sumbernya diselesaikan terhadap rekod terpilih, hash disemak semula, dan rentetan petikan mesti wujud dalam rekod tersebut. ID yang tidak diketahui, petikan yang diubah dan dakwaan tanpa rujukan menolak jawapan tersebut. Aplikasi ini mencipta pautan; URL yang dijana oleh model tidak digunakan sebagai rujukan. Semakan ini mengesahkan kewujudan sumber dan ketepatan petikan, bukan kebenaran sesuatu inferens. Semak inferens menentang rekod sebelum bergantung kepadanya.

## Laporan

Simpan jawapan yang telah disemak sebagai laporan analitik berasingan. Ia merangkumi ringkasan model, kronologi pemerhatian, pautan dan nama pengguna yang diekstrak, rekod suntingan/pembuangan, had liputan, dan hash peristiwa sumber. Penyedia, model, titik akhir, masa dan versi templat arahan disertakan bersamanya. Tiada identiti yang digabungkan secara automatik.

Pindaan dan nota penganalisis disimpan berasingan daripada ringkasan model. Laporan disimpan dalam fail terbitan yang disulitkan, dengan indeks di luar aliran peristiwa yang ditandatangani; peristiwa dan media asal tidak berubah. Hanya pemilik atau pentadbir boleh membuka laporan, dan capaian sumber akan disemak semula. Pemuat turun juga memerlukan kebenaran eksport. Versi 1 tidak menandatangani laporan atau menyiratkan bahawa kesimpulan model adalah bukti yang disahkan. Had: 100 laporan setiap ruang kerja dan 100 semakan penganalisis setiap laporan.

Untuk OCR manual dan transkrip, lihat [pemprosesan media](https://phishdestroy.github.io/TgWitness/ms/docs/reference/media-analysis/). Untuk capaian klien, lihat [MCP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/).
