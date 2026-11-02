# Sediakan salinan perkongsian

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/handover/

Berkongsi pemerhatian berkaitan sambil mengekalkan ruang kerja asal utuh.

Serahan ialah ekstrak berasingan yang ditandatangani. Pilih sembang dan orang, kurangkan identiti atau teks, dan tentukan fail serta nota pasukan yang sesuai dimasukkan dalam salinan penerima. Manifestnya merekodkan pilihan tersebut dan bilangan rekod yang tidak diubah, dikurangkan dan diabaikan.

## Sediakan ekstrak penerima

1. Buka **Eksport → Ekstrak Serahan**. Tulislah tujuannya, pilih sembang dan tempoh UTC pilihan, kemudian pilih **Muatkan senarai peserta sembang terpilih** jika anda memerlukan subjek bernama.
2. Pilih cara untuk mengendalikan semua orang lain: nama samaran, mengabaikan mesej mereka, atau memaparkan sebagai direkodkan. Tetapkan teks mesej dan lampiran secara berasingan; secara pilihan, sembunyikan nombor telefon dan alamat e-mel.
3. Pilih sama ada untuk memasukkan penanda buku dan hirisan Case Board, atau kad dengan komen. Alias penyiasat boleh menggantikan nama pasukan dalam salinan ini.
4. Pilih **ekstrak handover Muat Turun**. Buka laporan yang dijana dan rekod terpilih secara tempatan, sahkan arkib, dan periksa salinan sebelum menghantarnya.

### Satu salinan asal, satu salinan perkongsian yang disengajakan

Contoh sintetik · hanya ilustrasi identiti

1. **Pilih.** Sertakan sembang kes dan kenal pasti individu yang menjadi subjek petikan.
2. **Minimumkan.** Pilih cara peserta lain muncul dalam salinan perkongsian.
3. **Periksa.** Buka laporan dan rekod arkib yang dijana sebelum menghantarnya.
4. **Berkongsi.** Serahkan salinan yang telah diperiksa dan sampaikan cap jari yang dipercayai secara berasingan.

#### Perhatian asal

Nora · pengguna 71002

"Saya telah menerima pautan yang disemak semula."

Jurnal sumber menyimpan pemerhatian yang disimpan ini.

#### Salinan penerima

Tunjukkan seperti yang direkodkan: Nora · pengguna 71002 · "Saya telah menerima pautan yang disemak semula."

Pseudonim: P01 · "Saya telah menerima pautan yang disemak semula."

Omit: mesej peserta ini dikeluarkan daripada salinan.

#### Periksa fail sebenar

Bacalah report.html dan records.jsonl.

Semak identiti, teks, lampiran dan komen pasukan pilihan.

#### Petikan bertandatangan

Pemilihan + hash fail + manifes yang ditandatangani

Pakej berasingan yang dipautkan kepada sempadan jurnal sumbernya

## Gunakan kawalan bersama

| Kawal | Kesan pada salinan |
| --- | --- |
| Orang | Pastikan subjek terpilih boleh dikenal pasti; pseudonimkan atau hapuskan peserta lain mengikut pilihan. |
| Teks | Sertakan semua teks, hanya teks daripada orang terpilih dan akaun pemerhati, atau hapuskan teks mesej dan medan terperinci yang mengandungi teks. |
| Fail | Pilih fail bagi individu terpilih dan akaun pemerhati, semua fail mesej yang dipaparkan, atau tiada fail. |
| Papan Kes | Pilih tiada bahan papan, penanda buku dan hirisan, atau kad dengan perbincangan pasukan. |

Semak teks bebas dan kandungan fail serta identiti: pseudonim tidak secara automatik membuang setiap nama yang ditulis dalam mesej atau lampiran. Jika fail terpilih yang dipelihara tidak tersedia, pulihkannya atau nyatakan secara eksplisit untuk mengecualikan lampiran sebelum menjana ekstrak.

## Jaga agar teks boleh disemak secara bebas

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan arkib bukti yang ditandatangani asal dan titik pemeriksaan secara berasingan. Pemindahan merekodkan projeksi sendiri, supaya penerima boleh menyemak salinan yang dihantar tanpa menerima keseluruhan ruang kerja. [Studio laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reports/) menyediakan reka bentuk bacaannya; [pengesahan eksport](https://phishdestroy.github.io/TgWitness/ms/docs/exports/) menerangkan rujukan yang dipercayai.
