# Reka laporan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reports/

Berikan pembaca laluan yang jelas dari soalan kes ke rekod yang disimpan.

Report studio menggabungkan pemilihan data, sejarah perubahan yang boleh dibaca, carta dan penemuan bertulis anda. Lapan reka bentuk terintegrasi terpakai untuk keluaran HTML dan PDF asli yang disokong. Laporan HTML, PDF dan JSON mempunyai meterai berasingan masing; manifes ZIP juga mengikat fail-fail dalam pakej. HTML dan PDF dimeterai selepas susun atur akhir mereka selesai.

## Bina laporan dalam tiga langkah

1. Buka **Eksport → Konfigurasi dan pratonton → Data**. Gunakan keseluruhan ruang kerja atau pilih sembang, pengarang, termasuk tarikh pemerhatian UTC dan jenis rekod. Tarikh-tarikh tersebut menerangkan bila TgWitness memerhati rekod tersebut.
2. Dalam **Reka Bentuk & Kandungan**, pilih pratetap reka bentuk dan kandungan. Pilih carta aktiviti, label peserta, transkrip, perubahan yang disimpan dan bahan Papan Kes pilihan. Masukkan butiran kes anda dan nota pemeriksaan.
3. Buka **Pratonton** untuk menyemak bilangan, aktiviti, peserta, rekod sampel dan julat ID yang hilang. Simpan tetapan, kemudian muat turun format yang anda perlukan.

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

**Klasik, Editorial, Briefing, Analitik, Teknikal, Gambaran keseluruhan, Siri bacaan, dan Ledger & margin** mempersembahkan rekod asas yang sama dalam susun atur yang berbeza. Mengubah reka bentuk mengekalkan pemilihan data dan nota bertulis. Bahasa laporan boleh dipilih daripada 25 bahasa yang disokong.

Siri bacaan mengelompokkan kes, skop, penemuan dan perubahan di sekeliling rel seksyen. Ledger & margin menggunakan bab bernombor dan margin lebar. Kedua-duanya juga menyokong gambaran keseluruhan HTML akaun dan perkongsian salinan. PDF asli dijana dengan fon terbundar; mesin pengguna tidak memerlukan pelayar atau pemasangan Node untuk penjanaan PDF. PDF Cina, Jepun dan Korea juga memerlukan fon yang sesuai pada pelayan, seperti Noto Sans CJK, dipasang di seluruh sistem atau diletakkan di `TGWITNESS_FONT_DIR`. Tanpa fon tersebut, ZIP mengekalkan laporan HTML dan JSON.

## Bacalah perubahan beserta konteksnya

Suntingan yang disimpan dipaparkan sebelum dan selepas. Pemberitahuan pemadaman boleh disertakan dengan versi terakhir yang dirakam. Balasan, petikan, penghantaran semula, reaksi, butang dan metadata lampiran mengekalkan rujukan yang tersedia. Hah SHA-256 fail dan hash rekod jurnal dilabel secara berasingan.

Pratinjau reka bentuk memaparkan komponen muka depan, pemeriksaan dan carta menggunakan rekod yang sepadan daripada 50,000 rekod sumber pertama. Pratonton data berasingan mengimbas keseluruhan tangkapan jurnal yang stabil untuk kiraan pilihan tepat, dengan had sampel yang dipaparkan dilabelkan. Jenerasikan PDF untuk menyemak paginasi akhir. Pengeksportan akaun penuh mempunyai gambaran keseluruhan HTML; PDF sembang individu menggunakan reka bentuk yang dipilih.

## Pilih salinan penerima dengan sengaja

Penapis laporan membentuk laporan yang mudah dibaca. ZIP bukti penuh mengekalkan jurnal asal dan lampiran. Gunakan [penyerahan](https://phishdestroy.github.io/TgWitness/ms/docs/handover/) [minimum](https://phishdestroy.github.io/TgWitness/ms/docs/handover/) apabila penerima hanya perlu menerima data terpilih. Lihat [kandungan laporan dan pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/) atau [sahkan eksport yang telah selesai](https://phishdestroy.github.io/TgWitness/ms/docs/exports/).
