# Telegram · Sediakan salinan perkongsian

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/handover/

Kongsi hanya apa yang perlu, yang asal kekal tidak disentuh.

Serahan ialah ekstrak bertandatangan berasingan: pilih sembang dan orang, sembunyikan identiti atau teks, pilih fail dan nota pasukan. Manifes merekodkan apa yang dikekalkan, dipangkas dan ditinggalkan.

## Sediakan ekstrak penerima

1. **Eksport → Ekstrak Serahan**: tulis tujuan, pilih sembang dan tempoh, **Muat orang daripada sembang terpilih** jika anda memerlukan orang bernama.
2. Semua orang lain: nama samaran, ditinggalkan, atau seperti direkodkan. Teks dan fail ialah suis berasingan; telefon dan e-mel boleh disamarkan.
3. Case Board: tiada, tanda buku dan hirisan, atau kad dengan komen. Nama pasukan boleh ditukar kepada alias.
4. **Muat turun ekstrak serahan**, bukanya, sahkannya, teliti sebelum dihantar.

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
| Orang | Orang terpilih kekal bernama; yang lain mendapat nama samaran atau ditinggalkan. |
| Teks | Semua teks, hanya teks orang terpilih dan akaun anda, atau tiada. |
| Fail | Fail orang terpilih dan akaun anda, semua fail yang dipaparkan, atau tiada. |
| Papan Kes | Tiada, tanda buku dan hirisan, atau kad dengan perbincangan. |

Baca teks dan fail juga: nama samaran tidak membuang nama yang ditulis di dalam mesej atau lampiran. Jika fail terpilih hilang, pulihkannya atau tinggalkan lampiran.

## Jaga agar teks boleh disemak secara bebas

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan sendiri arkib asal dan checkpoint. Penerima boleh mengesahkan salinan mereka tanpa mendapat seluruh ruang kerja. Reka bentuk: [Report studio](https://phishdestroy.github.io/TgWitness/ms/docs/reports/). Rujukan dipercayai: [pengesahan eksport](https://phishdestroy.github.io/TgWitness/ms/docs/exports/).
