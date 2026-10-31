# Eksport dan sahkan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/exports/

Berkongsi rekod yang disahkan supaya orang lain boleh menyemak.

Simpan rujukanEksport ZIP yang disahkanPenerima mengesahkan

Baru dengan tandatangan dan checkpoint? [Ubah rekod sampel](https://phishdestroy.github.io/TgWitness/ms/docs/concepts/#chain) dan lihat pemeriksaan mana yang mengesaninya.

Menyimpan salinan jauh daripada pengumpul? Pergi ke [tetapan S3](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3), [Object Lock](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3-retention) atau [pemulihan disahkan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3-restore).

## Simpan rujukan yang dipercayai

Simpan cap jari kunci awam ruang kerja di luar pengumpul. Semasa pengumpulan, simpan titik pemeriksaan yang disahkan di tempat lain atau gunakan [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/witness/). Rujukan ini membolehkan penerima memeriksa kunci dan sempadan jurnal terdahulu.

## Muat turun ZIP yang disahkan

Buka **Eksport** dan cipta ZIP bukti yang disahkan. Ia merangkumi jurnal ruang kerja dan manifes fail yang disahkan. Penapis panel tidak mengehadkan eksport jurnal penuh ini: semak bahan sebelum berkongsi.

Muat turun HTML dan CSV berdiri sendiri berguna untuk bacaan dan analisis. Simpan fail ZIP yang ditandatangani sebagai asal yang boleh disahkan; fail HTML atau CSV berasingan tidak mempunyai tandatangan berdiri sendiri.

## Sahkan dengan salinan TgWitness yang dipercayai

Dalam persekitaran projek yang dipasang, gantikan cap jari contoh dan laluan fail:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Apabila kedua-dua rujukan lulus, hasilnya melaporkan `key_pinned: true` dan `checkpoint_checked: true`. Simpan keputusan pengesahan bersama arkib asal. Titik pemeriksaan yang disimpan mesti berada pada atau sebelum sempadan eksport.

## Memahami keputusan

- **Integriti:** sejarah yang direkodkan dan fail yang dieksport sepadan dengan tandatangan mereka.
- **Perhatian awal:** titik pemeriksaan luaran membolehkan anda membandingkan eksport dengan awalan jurnal yang telah disimpan sebelum ini.
- **Penghantaran:** ujian hantar terkawal → sunting → padam memeriksa peristiwa tertentu terhadap rekod yang dirakam.

Tandatangan yang sah tidak membuktikan bahawa setiap peristiwa Telegram telah tiba, bahawa sumber itu berkata benar atau bahawa jam pengumpul adalah tepat.

## Menyediakan salinan luar tapak S3

Di ruang kerja anda yang sedang berjalan, buka **Eksport → Salinan luar tapak**. Ciri pilihan ini berfungsi dengan AWS S3 dan perkhidmatan lain yang serasi S3. Ia menyalin segmen jurnal, foto dan fail yang disimpan, titik pemeriksaan dengan respons cap masa mereka, dan eksport sembang yang telah selesai. Setiap objek disulitkan pada pengumpul dengan `AES-256-GCM` sebelum dimuat naik.

Demonstrasi dalam talian memaparkan kawalan yang sama dengan muat naik dilumpuhkan. Masukkan kelayakan storan hanya di ruang kerja anda sendiri yang sedang dijalankan.

[![Panel salinan luar tapak lengkap: hujung, rantau, baldi, kunci akses, jadual, kawalan Kunci Objek dan kunci pemulihan](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Panel lengkap dengan pilihan lanjutan dibuka. Tiada kelayakan storan dipaparkan.

| Medan | Apa yang perlu dimasukkan |
| --- | --- |
| Titik hujung | URL perkhidmatan penyimpanan, tanpa laluan bakul atau kelayakan. Contoh rekaan: `https://s3.example.invalid` |
| Wilayah | Wilayah yang diperlukan oleh penyedia anda. Lalai aplikasi ialah `us-east-1`. |
| Bucket | Dump sedia ada yang boleh anda akses. Contoh fiksyen: `example-case-backup`. |
| Folder dalam baldi | Awalan objek; lalai `tgwitness`. Aplikasi menambah awalan yang diperoleh daripada cap jari kunci tandatangan ruang kerja ini. |
| ID kunci akses / Kunci akses rahsia | Masukkan kedua-dua kelayakan storan sekaligus. Ia disimpan dalam peti besi ruang kerja. Biarkan kedua-duanya kosong pada simpanan kemudian untuk mengekalkan pasangan yang disimpan. |
| Alamat gaya Path | Gunakan `endpoint/bucket` apabila diaktifkan, atau `bucket.endpoint` apabila dinyahaktifkan, mengikut penyedia. |
| Salin selang | Dari 1 hingga 1,440 minit; lalai 5 minit. Aplikasi mesti berjalan untuk salinan yang dijadualkan. |
| Penahanan Object Lock | Hari pengekalan dan mod untuk baldi yang menyokong Object Lock. Hari sifar mengekalkan pengekalan lalai baldi. |

1. Masukkan destinasi dan kelayakan. Biarkan **salinan luar tapak** tidak dicentang semasa penyediaan, kemudian pilih **Simpan salinan luar tapak**.
2. Pilih **Uji sambungan**. Ini memuat naik objek ujian yang disulitkan dan memeriksa respons storan.
3. Pilih **Muat turun kunci penyulitan**. Simpan fail itu secara berasingan daripada pengumpul; ia diperlukan untuk pemulihan.
4. Aktifkan kotak semak **Simpan salinan di luar tapak** dan simpan semula. Pilih **Salin sekarang** untuk proses manual, atau biarkan jadual berjalan.

**Tidak melakukannya.** Ia tidak mencipta tong simpanan. Pemunggahan terjadual berhenti apabila aplikasi berhenti.

## Semak pengekalan dan kemajuan salinan

Di bawah **Pilihan lanjut**, pilih hari pengekalan dan `GOVERNANCE` atau `COMPLIANCE` apabila baldi anda menyokong Object Lock. TgWitness membaca semula mod pengekalan dan tarikh akhir objek yang dimuat naik. Status melaporkan pengesahan, pengekalan yang hilang atau kegagalan semakan; hanya muat naik yang berjaya sahaja tidak mengesahkan pengekalan.

Panel melaporkan pusingan terakhir, bilangan objek, bait yang dipindahkan, sempadan jurnal yang disalin dan sebarang ralat. Media tempatan yang hilang atau berubah dilaporkan dan dicuba semula pada pusingan seterusnya. Fail, titik pemeriksaan dan eksport yang beratur selepas media tersebut masih boleh disalin.

Pemunggahan menggunakan laluan Direct, SOCKS5 atau HTTP ruang kerja. Salinan S3 tidak tersedia melalui MTProxy; aplikasi tidak beralih kepada sambungan terus.

**Tidak melakukannya**. Ia tidak memaksa penyedia menguatkuasakan Object Lock semata-mata kerana muat naik telah diterima.

## Simpan kunci pemulihan secara berasingan

JSON yang dimuat turun mengandungi kunci penyahsulit, tetapan destinasi, awalan objek ruang kerja dan cap jari kunci tandatangan. Ia tidak mengandungi kelayakan akses S3: pemulihan memerlukan kelayakan berasingan dengan akses baca ke baldi.

Jika anda menukar endpoint, bucket atau awalan folder, muat turun semula fail kunci supaya tetapan destinasi sepadan. Aplikasi memulakan salinan baru jurnal, fail dan checkpoint yang disimpan secara tempatan di destinasi baru. Eksport sembang siap yang telah dikeluarkan daripada barisan muat naik tempatan kekal di destinasi asal mereka.

**Tidak melakukannya.** Ia tidak menyahsulit salinan tanpa kunci yang dieksport. Kredensial akses storan tidak dapat menggantikan kunci tersebut.

## Pulihkan dan sahkan pada mesin lain

Gunakan pemasangan TgWitness yang dipercayai, fail JSON kunci yang dimuat turun, butiran storan dengan kebenaran baca, dan direktori output kosong. Gantikan penanda tempat butiran rekaan di bawah.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Muat turun dan objek yang didekripsi kekal dalam storan sementara peribadi sementara keseluruhan jurnal, titik pemeriksaan yang disimpan dan has serta saiz media yang dipelihara diperiksa. Laluan tidak selamat, segmen jurnal yang bertembung dan jurnal yang lebih pendek daripada titik pemeriksaannya ditolak. Pengesahan yang gagal tidak menerbitkan sebarang fail yang dipulihkan.

Pemulihan yang berjaya menghasilkan `events.jsonl`, `media/`, `checkpoints/` dan `exports/` bagi bahan yang terdapat dalam salinan. Simpan hasil JSON arahan bersama bahan yang dipulihkan.

**Tidak melakukannya.** Ia tidak membina semula pemerhatian yang tidak pernah sampai ke jurnal atau menggantikan titik pemeriksaan atau saksi yang disimpan secara bebas.
