# Telegram · Eksport dan sahkan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/exports/

Serahkan fail yang boleh disemak sendiri oleh penerima terhadap ruang kerja anda.

Simpan rujukanEksport ZIP yang disahkanPenerima mengesahkan

Baru dengan tandatangan dan checkpoint? [Ubah rekod contoh](https://phishdestroy.github.io/TgWitness/ms/docs/concepts/#chain) dan lihat semakan mana yang menangkapnya.

Menyimpan salinan jauh daripada pengumpul? Pergi ke [tetapan S3](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3), [Object Lock](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3-retention) atau [pemulihan disahkan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3-restore).

## Simpan rujukan yang dipercayai

Catat cap jari kunci ruang kerja di tempat selain pengumpul. Semasa mengumpul, simpan juga checkpoint bertandatangan di tempat lain, atau jalankan [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/witness/). Itulah yang digunakan penerima untuk menyemak kunci dan keadaan jurnal terdahulu.

## Muat turun ZIP yang disahkan

**Eksport** → ZIP bukti bertandatangan. Ia mengandungi seluruh jurnal dan manifes fail bertandatangan. Bentukkan laporan yang mudah dibaca dalam [Report studio](https://phishdestroy.github.io/TgWitness/ms/docs/reports/), atau hantar data terpilih sahaja sebagai [ekstrak serahan](https://phishdestroy.github.io/TgWitness/ms/docs/handover/).

Laporan HTML, PDF dan JSON membawa meterai masing-masing. CSV hanyalah salinan kerja; untuk integriti gunakan CSV di dalam ZIP yang telah disahkan.

## Sahkan dengan salinan TgWitness yang dipercayai

Dalam persekitaran projek, dengan cap jari dan laluan anda sendiri:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Jika lulus, anda melihat `key_pinned: true` dan `checkpoint_checked: true`. Simpan output itu di sebelah arkib. Checkpoint mesti berada pada atau sebelum hujung eksport.

## Gunakan hasil pengesahan

- **Fail:** manifes mengikat hash fail, tandatangan mengikat jurnal. Sebarang perubahan akan kelihatan.
- **Identiti:** cap jari yang anda simpan membuktikan itu kunci yang anda jangkakan.
- **Keadaan terdahulu:** checkpoint membandingkan eksport dengan awalan jurnal yang disimpan sebelum serahan.
- **Liputan:** jurang, hasil pemerolehan dan ujian hantar → sunting → padam menunjukkan apa yang benar-benar ditangkap oleh persediaan ini.

Butiran: [apa yang dibuktikan oleh pengesahan dan apa yang tidak](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope).

## Menyediakan salinan luar tapak S3

**Eksport → Salinan luar tapak** dalam ruang kerja anda. Berfungsi dengan AWS S3 dan apa-apa yang serasi S3. Ia menyalin segmen jurnal, fail tersimpan, checkpoint dengan cap masanya dan eksport sembang yang siap, setiap satu disulitkan dengan `AES-256-GCM` sebelum meninggalkan pengumpul.

Demo dalam talian menunjukkan kawalan ini dengan muat naik dimatikan. Masukkan kelayakan sebenar hanya dalam pemasangan anda sendiri.

[![Panel salinan luar tapak lengkap: hujung, rantau, baldi, kunci akses, jadual, kawalan Kunci Objek dan kunci pemulihan](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Panel lengkap dengan pilihan lanjutan dibuka. Tiada kelayakan storan dipaparkan.

| Medan | Apa yang perlu dimasukkan |
| --- | --- |
| Titik hujung | URL storan, tanpa laluan bucket atau kelayakan. Contoh: `https://s3.example.invalid`. |
| Wilayah | Apa sahaja yang diperlukan penyedia anda. Lalai `us-east-1`. |
| Tong | Bucket sedia ada yang boleh anda tulis. Contoh: `example-case-backup`. |
| Folder dalam baldi | Awalan, lalai `tgwitness`. Awalan bagi setiap ruang kerja ditambah di atasnya. |
| ID kunci akses / Kunci akses rahsia | Kedua-duanya bersama, disimpan dalam peti besi. Biarkan kedua-duanya kosong kemudian untuk mengekalkannya. |
| Alamat gaya Path | Hidup: `endpoint/bucket`. Mati: `bucket.endpoint`. Bergantung pada penyedia. |
| Salin selang | 1 hingga 1,440 minit, lalai 5. Hanya semasa aplikasi berjalan. |
| Penahanan Object Lock | Hari dan mod, jika bucket menyokong Object Lock. Sifar mengekalkan lalai bucket. |

1. Cipta bucket, isikan destinasi dan kelayakan dengan **Simpan salinan luar tapak** tidak ditanda, tekan **Simpan salinan luar tapak**.
2. **Uji sambungan** memuat naik objek ujian yang disulitkan.
3. **Muat turun kunci penyulitan** dan simpan jauh daripada pengumpul. Tiada kunci, tiada pemulihan.
4. Tandakan **Simpan salinan luar tapak**, simpan, kemudian **Salin sekarang** atau biarkan jadual berjalan.

## Semak pengekalan dan kemajuan salinan

Di bawah **Lagi pilihan** pilih hari pengekalan dan `GOVERNANCE` atau `COMPLIANCE`. TgWitness membaca semula pengekalan daripada objek yang dimuat naik dan memberitahu anda: disahkan, tiada atau semakan gagal.

Panel menunjukkan larian terakhir, bilangan objek, bait, sempadan jurnal yang disalin dan ralat. Fail setempat yang hilang dilaporkan dan dicuba semula pada larian berikutnya, yang lain terus disalin.

Muat naik melalui sambungan terus, SOCKS5 atau HTTP. Dengan laluan MTProxy sahaja, salinan menunggu dengan ralat.

## Simpan kunci pemulihan secara berasingan

JSON kunci mengandungi kunci penyahsulitan, destinasi, awalan dan cap jari kunci. Untuk pemulihan anda memerlukannya serta kelayakan storan dengan akses baca.

Menukar endpoint, bucket atau awalan? Muat turun kunci sekali lagi. Salinan baharu bermula di destinasi baharu; eksport sembang lama kekal di tempatnya.

## Pulihkan dan sahkan pada mesin lain

Anda memerlukan pemasangan TgWitness yang dipercayai, JSON kunci, kelayakan storan baca sahaja dan folder kosong:

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

Semuanya disemak dahulu dalam folder sementara peribadi: seluruh jurnal, checkpoint, hash dan saiz fail. Laluan tidak selamat, segmen yang bercanggah atau jurnal yang lebih pendek daripada checkpointnya akan gagal, dan ketika itu tiada apa yang ditulis keluar.

Jika berjaya, anda mendapat `events.jsonl`, `media/`, `checkpoints/` dan `exports/`. Simpan output JSON arahan bersamanya, dan bandingkan dengan checkpoint atau rekod saksi yang anda simpan sendiri.
