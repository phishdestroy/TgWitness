# Kerja arkib

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/archive/

Cari mesej. Semak sumber. Bina kes.

Alat-alat ini tersedia dari cawangan utama semasa. Pratonton mudah alih 0.7.0 wujud sebelum mereka; gunakan keluaran sumber untuk aliran kerja ini.

01**Bawa masuk sejarah**

Muatkan mesej terdahulu daripada sumber yang telah diaktifkan ke dalam ruang kerja.

02**Ikuti sumber**

Cari dalam arkib dan buka mesej yang disimpan di sebalik setiap hasil.

03**Jaga agar penyerahan tetap jelas**

Simpan analisis anda secara berasingan dan eksport bukti yang ditandatangani di sebelahnya.

Rekod yang dirakam, teks yang diiktiraf dan kesimpulan penganalisis kekal berasingan.

## Muat mesej terdahulu

1. Buka **Sumber → Sembang dalam skop**, semak sembang yang didayakan dan mulakan pemerhatian.
2. Pilih **Muat Sejarah Penuh**. Jalannya menggunakan senarai sumber yang dipilih pada masa itu.
3. Gunakan **Sejarah Jeda** dan **Sejarah Teruskan** mengikut keperluan. Selepas memulakan semula, sambung secara eksplisit.
4. Semak hasil bagi setiap sumber dan barisan menunggu lampiran. Simpan laporan kemajuan yang ditandatangani bersama eksport bukti.

Ini mengisi ruang kerja dengan mesej yang tersedia. Eksport HTML/JSON bagi setiap sembang adalah operasi berasingan. [Butiran sejarah dan pemulihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/).

## Cari dahulu, kemudian buat keputusan tentang AI

1. Buka **Jurnal** untuk carian tempatan. Pilih ruang kerja dan gunakan penapis sumber dan masa.
2. Cari frasa atau domain. Buka rekod yang sepadan dan versi simpanannya.
3. Untuk analisis AI, pentadbir mendayakan dan mengkonfigurasikan penyedia dalam **Integrasi**. Buka **Tanya arkib** dan pilih sembang serta tempoh. Semak **Data dihantar ke model** dan nyahtanda petikan yang tidak diingini sebelum meluluskan permintaan.
4. Semak petikan yang dikembalikan. Simpan jawapan sebagai laporan dan tambahkan semakan atau nota anda sendiri.

Carian dijalankan secara tempatan tanpa AI. Laporan analitik mengekalkan rujukan sumber dan sejarah semakan; ia berasingan daripada jurnal yang disahkan. [Penyediaan penyedia dan laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/analysis/).

## Pilih sambungan yang anda perlukan

| Tugas | Terbuka | Pemasangan |
| --- | --- | --- |
| Bacalah sembang terpilih daripada klien AI | **Integrasi → MCP** | [Pasang MCP extra, keluarkan token berlingkup dan sambungkan klien](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/) |
| Kenal pasti teks dalam media yang disimpan | Rekod `media.saved` → **Kenal pasti lampiran** | [Sediakan pekerja Docker tempatan dan fail bahasa/model yang diperlukan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/media-analysis/) |
| Hantar peristiwa ke n8n atau SIEM | **Integrasi → Webhook keluaran** | [Tambah penerima, sahkan HMAC dan deduplikasikan ID acara](https://phishdestroy.github.io/TgWitness/ms/docs/reference/webhooks/) |

**Token akses mana perlu diletakkan di mana?**

Akses panel adalah untuk mereka yang menyemak kes. Sambungan MCP mendapat token arkib baca sahaja yang berasingan. Penerima webhook menggunakan rahsia HMAC sendiri. Tiada yang memerlukan fail sesi Telegram.

[Berkongsi akses panel](https://phishdestroy.github.io/TgWitness/ms/docs/access/) atau [menyediakan klien MCP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/).

## Serahkan sumber dan kesimpulan

Simpan laporan analitik yang telah disemak bersama fail ZIP bukti yang ditandatangani. Laporan itu menerangkan cara anda membaca sumber; ZIP membolehkan penerima menyemak rekod yang disimpan dengan cap jari dan titik pemeriksaan yang dipercayai secara bebas.

[Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/) · [Melalui satu siasatan penuh](https://phishdestroy.github.io/TgWitness/ms/docs/cases/)
