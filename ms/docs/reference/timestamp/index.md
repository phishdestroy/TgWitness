# Cap masa

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/

Cap masa RFC 3161 untuk checkpoint berasingan: apa yang dihantar kepada pihak berkuasa dan bagaimana respons disahkan.

TgWitness menyediakan permintaan RFC 3161 dan mengesahkan respons pihak berkuasa cap masa (TSA). Prosedur manual ini tidak memilih TSA mahupun menghantar data; mod bukti melakukan kedua-duanya mengikut jadual ([format bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Permintaan yang telah disediakan **belum lagi** merupakan **bukti cap masa**.

## Apa yang bukti ikat

Diyagram aliran · Perhatian akaun → Rantaian SHA-256 dan tandatangan Ed25519; Rantaian SHA-256 dan tandatangan Ed25519 → Pemeriksaan berasingan yang ditandatangani; Pemeriksaan berasingan yang ditandatangani → Hash bait tepat dan nonse rawak; Hash bait tepat dan nonse rawak → Permintaan RFC 3161; Permintaan RFC 3161 → TSA Bebas; TSA Bebas → Tindak balas TSA yang disahkan; Pemeriksaan berasingan yang ditandatangani → Verifikasi data, nonce dan kepercayaan CA yang eksplisit; Tindak balas TSA yang disahkan → Verifikasi data, nonce dan kepercayaan CA yang eksplisit · Perhatian akaun · Rantaian SHA-256 dantandatangan Ed25519 · Pemeriksaan berasinganyang ditandatangani · Hash bait tepat dannonse rawak · Permintaan RFC 3161 · TSA Bebas · Tindak balas TSA yangdisahkan · Verifikasi data, noncedan kepercayaan CAyang eksplisit

**Diagram sebagai teks**

1. Perhatian akaun → Rantaian SHA-256 dan tandatangan Ed25519
2. Rantaian SHA-256 dan tandatangan Ed25519 → Pemeriksaan berasingan yang ditandatangani
3. Pemeriksaan berasingan yang ditandatangani → Hash bait tepat dan nonse rawak
4. Hash bait tepat dan nonse rawak → Permintaan RFC 3161
5. Permintaan RFC 3161 → TSA Bebas
6. TSA Bebas → Tindak balas TSA yang disahkan
7. Pemeriksaan berasingan yang ditandatangani → Verifikasi data, nonce dan kepercayaan CA yang eksplisit
8. Tindak balas TSA yang disahkan → Verifikasi data, nonce dan kepercayaan CA yang eksplisit

Tandatangan pengumpul mengikat rekod kepada kuncinya. Respons TSA yang dipercayai boleh mengesahkan bahawa satu checkpoint tertentu wujud pada masa yang dinyatakan oleh TSA. Checkpoint itu kemudian boleh mengikat awalan jurnal. Ini tidak menetapkan masa bagi setiap tindakan Telegram atau kebenaran kandungan yang dirakam.

## Prosedur

1. Simpan cap jari kunci pengumpul melalui saluran dipercayai berasingan. Kunci yang dibekalkan hanya oleh ZIP yang diperiksa tidak mencukupi untuk mengenal pasti pengumpul.
2. Di **Eksport → Sediakan permintaan cap masa**, muat turun ZIP permintaan ruang kerja yang dipilih. Ekstrak `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` dan `README.txt`. Jangan ubah bait checkpoint.
3. Pilih TSA yang sesuai untuk siasatan. Hantar `timestamp.tsq` menggunakan kaedah yang didokumenkan, dengan `application/timestamp-query` untuk perkhidmatan HTTP. Simpan balasan binari asal sebagai `timestamp.tsr`, titik akhir, masa pemulihan dan keputusan permintaan. Permintaan mengandungi hash dan nonce bukannya mesej; metadata rangkaian masih mendedahkan permintaan tersebut.
4. Dapatkan sijil akar yang dipercayai secara bebas daripada balasan, serta mana-mana sijil perantara yang diperlukan. Sijil dalam balasan tidak menjadi dipercayai semata-mata kerana ia disertakan di sana.
5. Daripada pemasangan TgWitness yang dipercayai, sahkan:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Tambah `--intermediates tsa-intermediates.pem` atau `--openssl /path/to/openssl` jika perlu. OpenSSL mesti menyokong `ts`. Pada Windows, pengesah juga mencari pemasangan Git piawai. OpenSSL 3.5.9 telah diuji secara tempatan dengan CA/TSA sintetik.

1. Eksport fail ZIP jurnal yang ditandatangani selepas penanda aras supaya ia termasuk awalan tersebut. Sahkan menggunakan cap jari yang diketahui secara bebas:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Pelihara fail ZIP, titik pemeriksaan, permintaan, balasan, rantaian sijil, keputusan pengesahan dan rekod penyerahan di luar pengumpul. Ulang pengesahan apabila diterima.

Untuk menyediakan permintaan daripada titik pemeriksaan yang disimpan:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Persiapan mengkanonikan JSON dan memasukkan checkpoint yang sepadan dalam arkib. Gunakan **bait checkpoint daripada arkib tersebut** untuk pengesahan TSA, walaupun fail input mempunyai ruang kosong yang berbeza.

## Batas pengesahan

| Semak | Tingkah laku semasa |
| --- | --- |
| Data | SHA-256 bagi bait checkpoint tepat mesti sepadan dengan respons |
| Permintaan | Dengan `--request`, pertanyaan asal dan nonce disahkan |
| Tandatangan TSA | OpenSSL mengesahkan tandatangan dan rantaian kepada CA eksplisit |
| Tandatangan pengumpul | Disahkan secara berasingan oleh pengesah jurnal dengan kunci yang dipasang |
| Pencabutan | Tiada pemulihan OCSP/CRL secara automatik |
| Kesahihan jangka panjang | Tiada pengesahan arkib selepas tamat tempoh sijil |
| Penghantaran dijadualkan | Mod bukti, dimatikan secara lalai |

`--request` secara teknikalnya adalah pilihan, tetapi mengabaikannya menghalang pengesahan nonse asal. Untuk prosedur penuh ini, `request_checked` hasil mesti benar. Pengesahan sijil mengikut peraturan dan masa pengesahan OpenSSL yang dipasang. Pemeliharaan jangka panjang memerlukan dasar sijil/bukti pembatalan yang berasingan.

Tandatangan kriptografi yang sah tidak secara automatik menjadi cap masa bertauliah atau penentuan kebolehterimaan undang-undang. Jika seorang pengendali mereka-reka pemerhatian sebelum mencap masa, TSA mengikat bait-bait tersebut; ia tidak membuktikan kebenarannya.

## Rekod penyerahan

Rakam pengecam kes, penghantar dan penerima, masa pemindahan UTC dan sumbernya, tujuan, nama fail/nilai SHA-256, cap jari pengumpul, julat urutan, jurang yang diketahui, versi pengesah dan keputusan pengesahan. Tandatangani dan simpan rekod ini secara berasingan melalui proses organisasi anda. Sistem rekod pemilikan pelbagai pengguna tidak dilaksanakan dalam TgWitness.

Tiada TSA langsung bebas dihubungi semasa pembangunan. Ujian tempatan mencipta CA/TSA sintetik untuk memeriksa keserasian dan penolakan data yang diubah, nonce atau CA.
