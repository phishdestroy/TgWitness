# Kerja arkib

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/archive/

Cari mesej. Semak sumber. Bina kes.

01**Bawa masuk sejarah**

Tarik mesej lama daripada sumber yang didayakan ke dalam ruang kerja.

02**Ikuti sumber**

Cari, kemudian buka mesej tersimpan di sebalik setiap hasil.

03**Jaga agar penyerahan tetap jelas**

Analisis anda dalam satu fail, bukti bertandatangan di sebelahnya.

Rekod yang dirakam, teks yang diiktiraf dan kesimpulan penganalisis kekal berasingan.

## Muat mesej terdahulu

1. **Sumber → Sembang dalam skop**: semak sembang yang didayakan, mulakan pemerhatian.
2. **Muat Sejarah Penuh**. Ia mengambil senarai sumber seperti sedia ada sekarang.
3. **Jeda sejarah** / **Teruskan sejarah** pada bila-bila masa. Selepas mula semula, sambung secara manual.
4. Semak hasil bagi setiap sumber dan baris gilir muat turun, simpan laporan kemajuan bertandatangan bersama eksport.

Ini mengisi ruang kerja. Eksport HTML/JSON satu sembang ialah perkara lain. [Butiran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/).

## Cari dahulu, kemudian buat keputusan tentang AI

1. **Jurnal** mencari secara setempat, tapis mengikut sumber dan masa.
2. Cari frasa atau domain, buka rekod dan versinya.
3. Untuk AI, pentadbir menyediakan penyedia dalam **Integrasi**. Kemudian **Tanya arkib**: pilih sembang dan tempoh, lihat **Data yang dihantar kepada model** dan nyahtanda apa yang tidak patut keluar.
4. Semak petikan, simpan jawapan sebagai laporan, tambah nota anda.

Carian tidak memerlukan AI. Laporan menyimpan sumber dan semakannya sendiri, berasingan daripada jurnal bertandatangan. [Persediaan penyedia](https://phishdestroy.github.io/TgWitness/ms/docs/reference/analysis/).

## Pilih sambungan yang anda perlukan

| Tugas | Terbuka | Pemasangan |
| --- | --- | --- |
| Benarkan klien AI membaca sembang terpilih | **Integrasi → MCP** | [Pasang MCP, buat token berskop, sambungkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/) |
| Kenal pasti teks dalam media yang disimpan | Rekod `media.saved` → **Kenal pasti lampiran** | [Sediakan worker Docker setempat](https://phishdestroy.github.io/TgWitness/ms/docs/reference/media-analysis/) |
| Hantar peristiwa ke n8n atau SIEM | **Integrasi → Webhook keluaran** | [Tambah penerima, semak HMAC, buang ID pendua](https://phishdestroy.github.io/TgWitness/ms/docs/reference/webhooks/) |

**Token akses mana perlu diletakkan di mana?**

Akses panel adalah untuk manusia. MCP mendapat token baca sahaja sendiri, webhook mendapat rahsia HMAC sendiri. Tiada satu pun memerlukan sesi Telegram.

[Berkongsi akses panel](https://phishdestroy.github.io/TgWitness/ms/docs/access/) atau [menyediakan klien MCP](https://phishdestroy.github.io/TgWitness/ms/docs/reference/mcp/).

## Serahkan sumber dan kesimpulan

Letakkan laporan di sebelah ZIP bertandatangan. Laporan ialah bacaan anda terhadap sumber, ZIP ialah apa yang disahkan oleh penerima.

[Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/) · [Melalui satu siasatan penuh](https://phishdestroy.github.io/TgWitness/ms/docs/cases/)
