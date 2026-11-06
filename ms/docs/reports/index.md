# Telegram · Reka laporan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reports/

Bawa pembaca dari soalan kes terus ke rekod yang disimpan.

Report studio menghimpunkan data yang anda pilih, sejarah perubahan, carta dan dapatan anda. Lapan reka bentuk, HTML dan PDF asli. Setiap laporan HTML, PDF dan JSON dimeterai dengan kunci anda.

## Bina laporan dalam tiga langkah

1. **Eksport → Konfigurasi dan pratonton → Data**: seluruh ruang kerja, atau pilih sembang, pengarang, tarikh (UTC, bila TgWitness melihat rekod) dan jenis rekod.
2. **Reka bentuk & kandungan**: pilih reka bentuk dan apa yang dimasukkan: carta, peserta, transkrip, perubahan, item Case Board, butiran kes dan nota anda.
3. **Pratonton**: semak kiraan, aktiviti, sampel dan julat ID yang hilang. Simpan, kemudian muat turun format yang anda perlukan.

### Aturkan bahan yang disimpan yang sama untuk pembaca

Contoh sintetik · susun atur skematik, bukan laporan yang dijana

1. **Pilih.** Pilih dua sembang dan tempoh pemerhatian untuk kes.
2. **Menyusun.** Pilih susun atur dan bahagian yang menjawab soalan.
3. **Praperiksaan.** Semak kiraan yang dipilih dan teks sebelum dan selepas yang disimpan.
4. **Sahkan.** Jenerasikan fail akhir dan periksa tandatanganannya dengan cap jari ruang kerja yang dipercayai.

#### Perhatian terpilih

2 sembang · 1 hari pemerhatian

Mesej, suntingan dan notis pemadaman

#### Struktur laporan

##### Tujuan pembayaran telah diubah

Soalan kes → skop → penemuan → rujukan rekod

**Kontext mesej**

Perhatian #142: "Gunakan pautan pembayaran baru."

**Perubahan yang disimpan**

Sebelum: old.example.invalid → Selepas: new.example.invalid

#### Semak pilihan

18 pemerhatian · 2 suntingan disimpan

Masa dihantar, disunting dan diperhatikan mempunyai label berasingan.

#### Hasil akhir

PDF yang ditandatangani + JSON yang ditandatangani, atau ZIP yang ditandatangani dengan laporannya yang boleh dibaca

Penerima memeriksa fail dan cap jari yang dipercayai.

## Pilih gaya bacaan

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: rekod yang sama, rupa berbeza. Menukar reka bentuk mengekalkan pilihan dan nota anda. Mana-mana daripada 25 bahasa.

PDF dibina dengan fon yang disertakan, tanpa pelayar. Bahasa Cina, Jepun dan Korea memerlukan fon seperti Noto Sans CJK pada pelayan (seluruh sistem atau dalam `TGWITNESS_FONT_DIR`), jika tidak anda hanya mendapat HTML dan JSON.

## Bacalah perubahan beserta konteksnya

Suntingan menunjukkan sebelum dan selepas, pemadaman menunjukkan versi tersimpan terakhir. Balasan, kiriman semula, reaksi, butang dan lampiran mengekalkan rujukannya.

Pratonton reka bentuk menggunakan 50,000 rekod pertama, pratonton data mengira semuanya dengan tepat. Untuk susun atur halaman akhir, jana PDF.

## Pilih salinan penerima dengan sengaja

Penapis hanya membentuk laporan, ZIP bukti masih mengandungi seluruh jurnal dan fail. Jika penerima patut mendapat kurang, gunakan [serahan diminimumkan](https://phishdestroy.github.io/TgWitness/ms/docs/handover/). Lagi: [kandungan laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/), [mengesahkan eksport](https://phishdestroy.github.io/TgWitness/ms/docs/exports/).
