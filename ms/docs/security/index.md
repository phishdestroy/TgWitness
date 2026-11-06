# Jaga keselamatannya

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/security/

Apa yang meninggalkan mesin anda, apa yang dibuka oleh setiap rahsia, dan apa yang dilindungi berbanding apa yang menjadi tanggungjawab anda.

**127.0.0.1**alamat panel secara lalai

**256-bit**token panel rawak

**0**CDN, analitik atau fon jauh

**Ed25519**tandatangan pada setiap rekod

## Tempat segala-galanya wujud

Pengumpul, panel dan setiap rekod kekal pada mesin anda. Secara lalai hanya Telegram yang dihubungi; selebihnya suis berasingan.

06 / APA YANG KELUAR DARI MESINPemasangan anda

KOMPUTER ATAU PELAYAR ANDA

**Panel**127.0.0.1:8787 · token pembawa

**Pengumpul**satu klien Telegram bagi setiap ruang kerja

DIREKTORI DATA

**Jurnal**SQLite · berantai hash · disahkan

**Media**fail dinamakan oleh SHA-256

**Petak keselamatan**Fernet · sesi, pasangan API, kunci penandatangan, proksi

- **Telegram**Sentiasa · melalui laluan anda

  Sambungan MTProto akaun: terus, SOCKS5, HTTP atau MTProxy. Mod Sembunyikan IP menunggu proksi yang berfungsi. Peralihan terus memerlukan mod yang secara eksplisit membenarkannya.
- **Salinan luar tapak**Pilihan · dimatikan secara lalai

  Jurnal, fail dan titik pemeriksaan disulitkan dengan AES-GCM sebelum dimuat naik ke storan serasi S3. Kunci kekal bersama anda; lampiran dinamakan menggunakan hash berasaskan kunci, bukan hash kandungan mereka.
- **Pemberitahuan**Pilihan · dimatikan secara lalai

  Masalah dan kiraan perubahan dengan tajuk sembang. Petikan mesej hanya dihantar jika anda mengaktifkannya.
- **Pihak berkuasa cap masa**Pilihan · dimatikan secara lalai

  Hanya SHA-256 titik pemeriksaan yang ditandatangani dan nonce rawak. Tiada mesej, tiada nama sembang.
- **Saksi**Pilihan · dimatikan secara lalai

  Mengambil titik pemeriksaan yang ditandatangani dan pengira tangkapan dengan token baca sahaja. Ia tidak boleh membaca perbualan atau mengubah tetapan.

Lalai: hanya sambungan Telegram yang keluar dari mesin ini.

Tujuan pilihan dikonfigurasikan mengikut ruang kerja. Teks mesej dan media disimpan tanpa disulitkan dalam direktori data: lindungi ia dengan penyulitan cakera dan kebenaran fail.

## Apa yang dibuka oleh setiap rahsia

| Rahsia | Di mana ia disimpan | Apa yang dibukanya | Jika bocor |
| --- | --- | --- | --- |
| Token panel**** | `panel-token.txt` dalam direktori data; pelayar menyimpannya bagi setiap tab | Segala-galanya dalam setiap ruang kerja | Hentikan TgWitness, padam `panel-token.txt`, mulakan semula: anda mendapat yang baharu |
| **Sesi Telegram** | Vault, disulitkan (`credentials.enc`) | Akaun Telegram itu sendiri | Batalkan sesi di Telegram di bawah *Tetapan → Peranti* |
| **Kunci penandatangan** | Vault, disulitkan (`signing.enc`) | Menandatangani rekod di bawah cap jari anda | Checkpoint di tempat lain, saksi dan cap masa masih menunjukkan apa yang wujud sebelum ini |
| **Kunci peti besi** | `vault.key` di sebelah data, atau kunci induk luaran | Peti besi | Anggap sesi dan kunci tandatangan juga bocor |
| **Token saksi** | Pada hos saksi | Baca sahaja: checkpoint dan kesihatan | Padamkannya di halaman Saksi, buat yang baharu |
| **Salinan kunci luar tapak** | Vault; muat turun sekali untuk pemulihan | Salinan luar tapak | Sesiapa yang juga memegang bucket boleh menyahsulitnya: anggap salinan itu terdedah |

## Apa yang dilindungi oleh perlindungan

### Diliputi

- Rekod yang diubah, dibuang atau disusun semula: rantaian hash atau tandatangan rosak.
- Jurnal yang dipotong atau dibina semula selepas anda menyimpan checkpoint di tempat lain: checkpoint tidak lagi sepadan.
- Meneka token: 256 bit rawak, perbandingan masa malar, 15 kegagalan seminit dan alamat itu disekat.
- Kandungan sembang berniat jahat: teks kekal teks, tidak pernah HTML; lampiran dimuat turun sebagai fail; panel tidak memuatkan apa-apa daripada laman lain.
- Direktori data yang dicuri dengan kunci peti besi luaran: sesi dan kunci kekal disulitkan.

### Dibiarkan kepada anda

- Token utama boleh melakukan apa sahaja. Beri orang lain akses berskop dan simpan token utama untuk diri sendiri.
- Sesiapa yang menjadi pentadbir pada mesin boleh membaca segala-galanya dan menandatangani semula jurnal. Simpan cap jari dan checkpoint di tempat lain.
- TgWitness tidak menyulitkan mesej dan media. Sulitkan cakera, ketatkan kebenaran.
- HTTP biasa di luar localhost membocorkan token. Gunakan HTTPS atau terowong SSH.
- Tandatangan tidak memberitahu apa yang terlepas. Semak liputan dan uji penghantaran pada akaun dan sumber anda sendiri.

[Kongsi akses kepada kes](https://phishdestroy.github.io/TgWitness/ms/docs/access/) dengan kebenaran, tarikh luput dan had sesi.

## Mengukuhkan pemasangan

0 daripada 8 telah selesai

1. **Gunakan akaun Telegram khusus**, jangan sekali-kali akaun utama anda.
2. **Kekalkan panel pada 127.0.0.1.** Akses jauh hanya melalui HTTPS (Caddy yang disertakan) atau terowong SSH.
3. **Sulitkan cakera** yang menyimpan direktori data, mesej dan media disimpan seadanya.
4. **Hadkan direktori data** kepada akaun perkhidmatan (0700 pada Unix, kebenaran folder pada Windows).
5. **Simpan kunci peti besi di tempat lain** pada pelayan: tetapkan `TGWITNESS_VAULT_KEY_FILE` sebelum mula pertama.
6. **Simpan cap jari dan checkpoint** pada sistem lain, jalankan saksi pada hos lain.
7. **Jangan muat naik** `data/`, sesi, `panel-token.txt` atau kunci vault ke GitHub atau sembang.
8. **Jangan log** penanda aras `Authorization` atau badan permintaan di proksi terbalik.

**Bolehkah saya menukar token panel tanpa kehilangan data?**

Ya, ia hanya membuka panel. Hentikan TgWitness, padam `panel-token.txt`, mulakan semula. Jurnal, sesi dan kunci kekal. Jika `TGWITNESS_TOKEN` ditetapkan, nilai itu mengatasi fail.

**Mengapa mesej tidak disulitkan semasa disimpan?**

Pengumpul perlu membacanya untuk mencari, membandingkan dan mengeksport. Kunci pada mesin yang sama tidak akan menghalang seseorang yang memang boleh membaca mesin itu. Penyulitan cakera melindungi cakera yang dicuri, kebenaran melindungi sistem yang sedang berjalan.

## Laporkan kerentanan

**Security → Report a vulnerability** di GitHub. Versi, kesan dan penghasilan semula minimum dengan data palsu. Jangan sekali-kali hantar kelayakan, folder akaun atau bukti sebenar. Jika pelaporan peribadi dimatikan, buka issue untuk meminta saluran peribadi, tanpa butiran eksploit.
