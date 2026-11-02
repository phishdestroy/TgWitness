# Eksport dan sahkan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/exports/

Berikan penerima fail yang boleh mereka semak menentang ruang kerja pengumpulan dan sejarahnya yang disimpan.

Simpan rujukanEksport ZIP yang disahkanPenerima mengesahkan

Baru dengan tandatangan dan checkpoint? [Ubah rekod sampel](https://phishdestroy.github.io/TgWitness/ms/docs/concepts/#chain) dan lihat pemeriksaan mana yang mengesaninya.

Menyimpan salinan jauh daripada pengumpul? Pergi ke [tetapan S3](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3), [Object Lock](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3-retention) atau [pemulihan disahkan](https://phishdestroy.github.io/TgWitness/ms/docs/exports/#s3-restore).

## Simpan rujukan yang dipercayai

Simpan cap jari kunci awam ruang kerja di luar pengumpul. Semasa pengumpulan, simpan titik pemeriksaan yang disahkan di tempat lain atau gunakan [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/witness/). Rujukan ini membolehkan penerima memeriksa kunci dan sempadan jurnal terdahulu.

## Muat turun ZIP yang disahkan

Buka **Eksport** dan buat ZIP bukti yang ditandatangani. Ia merangkumi jurnal ruang kerja penuh dan manifes fail yang ditandatangani. Gunakan [Report Studio](https://phishdestroy.github.io/TgWitness/ms/docs/reports/) untuk membentuk laporan yang mudah dibaca, atau [ekstrak](https://phishdestroy.github.io/TgWitness/ms/docs/handover/) [penyerahan](https://phishdestroy.github.io/TgWitness/ms/docs/handover/) untuk menyampaikan hanya data terpilih yang dimampatkan.

Laporan HTML, PDF dan JSON mempunyai meterai berasingan yang ditandatangani dan boleh disemak secara berasingan. CSV adalah salinan analisis yang mudah; gunakan CSV tepat di dalam ZIP yang disahkan untuk memeriksa integritinya. Simpan ZIP yang ditandatangani apabila penerima juga memerlukan rekod sumber dan lampiran.

## Sahkan dengan salinan TgWitness yang dipercayai

Dalam persekitaran projek yang dipasang, gantikan cap jari contoh dan laluan fail:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Apabila kedua-dua rujukan lulus, hasilnya melaporkan `key_pinned: true` dan `checkpoint_checked: true`. Simpan keputusan pengesahan bersama arkib asal. Titik pemeriksaan yang disimpan mesti berada pada atau sebelum sempadan eksport.

## Gunakan hasil pengesahan

- **Periksa fail yang dihantar:** manifes mengikat hash mereka, dan tandatangan rekod mengikat jurnal yang disimpan. Fail yang diubah atau rantaian rekod yang terputus dikesan.
- **Semak identiti ruang kerja:** cap jari yang disimpan secara berasingan mengenal pasti kunci tandatangan yang anda jangkakan.
- **Bandingkan sempadan terdahulu:** checkpoint yang disimpan memeriksa eksport menentang awalan jurnal yang disimpan sebelum penyerahan.
- **Semak liputan pengumpulan:** jurang, keputusan pemerolehan dan hantaran terkawal → sunting → padam ujian menerangkan peristiwa yang dirakam oleh tetapan ini.

Simpan keputusan ini bersama salinan penerima. Lihat [apa yang ditetapkan oleh pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) untuk skop pemeriksaan dan penilaian berasingan terhadap tuntutan sumber dan liputan pengumpulan.

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

1. Buat bucket dengan penyedia anda, kemudian masukkan destinasi dan kelayakan. Biarkan **'Keep an off-site copy'** tidak dicentang semasa penyediaan, kemudian pilih **'Save off-site copy**'.
2. Pilih **Uji sambungan**. Ini memuat naik objek ujian yang disulitkan dan memeriksa respons storan.
3. Pilih **Muat turun kunci penyulitan**. Simpan fail itu secara berasingan daripada pengumpul; ia diperlukan untuk pemulihan.
4. Aktifkan kotak semak **Simpan salinan di luar tapak** dan simpan semula. Pilih **Salin sekarang** untuk proses manual, atau biarkan jadual berjalan.

## Semak pengekalan dan kemajuan salinan

Di bawah **Pilihan lanjut**, pilih hari pengekalan dan `GOVERNANCE` atau `COMPLIANCE` apabila baldi anda menyokong Object Lock. TgWitness membaca semula mod pengekalan dan tarikh akhir objek yang dimuat naik. Semak hasil pengekalan berasingan: disahkan, pengekalan hilang atau pemeriksaan gagal.

Panel melaporkan pusingan terakhir, bilangan objek, bait yang dipindahkan, sempadan jurnal yang disalin dan sebarang ralat. Media tempatan yang hilang atau berubah dilaporkan dan dicuba semula pada pusingan seterusnya. Fail, titik pemeriksaan dan eksport yang beratur selepas media tersebut masih boleh disalin.

Pemunggahan menggunakan laluan Direct, SOCKS5 atau HTTP ruang kerja. Pilih salah satu laluan ini untuk menyalin ke S3; laluan hanya MTProxy akan meninggalkan salinan dalam status menunggu dengan ralat.

## Simpan kunci pemulihan secara berasingan

JSON yang dimuat turun mengandungi kunci penyahsulit, tetapan destinasi, awalan objek ruang kerja dan cap jari kunci tandatangan. Pemulihan memerlukan kedua-dua fail kunci ini dan kelayakan storan berasingan dengan akses baca ke baldi. Simpan kelayakan tersebut dalam pelan pemulihan anda.

Jika anda menukar endpoint, bucket atau awalan folder, muat turun semula fail kunci supaya tetapan destinasi sepadan. Aplikasi memulakan salinan baru jurnal, fail dan checkpoint yang disimpan secara tempatan di destinasi baru. Eksport sembang siap yang telah dikeluarkan daripada barisan muat naik tempatan kekal di destinasi asal mereka.

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

Bandingkan bahan yang dipulihkan dengan titik pemeriksaan atau rekod saksi yang anda simpan secara bebas, kemudian semak liputan koleksi yang direkodkan untuk tempoh yang anda perlukan.
