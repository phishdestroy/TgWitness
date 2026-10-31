# Jaga keselamatannya

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/security/

Ketahuilah laluan untuk Telegram, senarai proksi awam dan perkhidmatan luaran pilihan. Ketahuilah apa yang dibuka oleh setiap rahsia, apa yang dilindungi dan apa yang diserahkan kepada anda.

**127.0.0.1**alamat panel secara lalai

**256-bit**token panel rawak

**0**CDN, analitik atau fon jauh

**Ed25519**tandatangan pada setiap rekod

## Tempat segala-galanya wujud

Pengumpul, panelnya dan setiap rekod yang disimpan kekal pada komputer atau pelayan yang anda jalankannya. Telegram adalah satu-satunya destinasi secara lalai; setiap destinasi lain adalah suis berasingan.

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
| **Panel token** | `panel-token.txt` dalam direktori data; pelayar menyimpannya hanya untuk tab tersebut | Segala-galanya dalam setiap ruang kerja: baca dan eksport, ubah skop, log masuk ke akaun | Hentikan TgWitness, padamkan `panel-token.txt`, mulakan semula: token baru telah dicipta |
| **Sesi Telegram** | Vault, disulitkan (`credentials.enc`) | Akaun Telegram itu sendiri | Batalkan sesi di Telegram di bawah *Tetapan → Peranti* |
| **Kunci penandatangan** | Vault, disulitkan (`signing.enc`) | Menandatangani rekod yang disahkan di bawah cap jari anda | Titik pemeriksaan disimpan di tempat lain, seorang saksi dan cap masa menunjukkan apa yang wujud sebelum |
| **Kunci peti besi** | `vault.key`di sebelah data, atau kunci induk luaran untuk direktori data baru | Mengekodekan semula peti besi | Anggap juga sesi dan kunci tandatangan telah bocor |
| **Token saksi** | Pada hos saksi | Hanya baca: checkpoint ber tandatangan dan kesihatan | Padamkannya di halaman Witness; buat yang baru |
| **Salinan kunci luar tapak** | Vault; muat turun sekali untuk pemulihan | Mengekodekan semula salinan luar tapak | Sesiapa yang juga memegang objek yang disimpan boleh menyahsulitkannya: anggap salinan itu telah terdedah |

## Apa yang dilindungi oleh perlindungan

### Diliputi

- Rekod yang diubah, dipadam atau disusun semula dalam eksport: rantaian hash atau tandatangan tidak lagi dapat disahkan.
- Jurnal dipulihkan atau dibina semula selepas titik pemeriksaan disimpan di tempat lain: titik pemeriksaan yang disimpan tidak lagi sepadan.
- Meneka token panel: 256 bit rawak, dibandingkan dalam masa tetap; selepas 15 kegagalan seminit, alamat ditolak.
- Kandungan sembang bermusuhan: teks dimasukkan sebagai teks, bukan sebagai HTML; lampiran dimuat turun sebagai fail; panel tidak memuat apa-apa daripada laman lain.
- Direktori data salinan dengan kunci peti besi luaran: sesi dan kunci penandatanganan kekal disulitkan tanpa kunci induk.

### Dibiarkan kepada anda

- Token panel utama mempunyai kawalan penuh. Berikan orang lain akses terhad kepada akaun, sembang dan tindakan yang mereka perlukan; jaga kunci utama agar kekal peribadi.
- Pentadbir mesin boleh membaca semuanya dan menulis semula serta menandatangani semula jurnal tersebut. Simpan cap jari dan titik pemeriksaan pada sistem lain.
- Teks mesej dan media tidak disulitkan oleh TgWitness. Gunakan penyulitan cakera dan kebenaran yang ketat.
- HTTP biasa di luar localhost mendedahkan token di rangkaian. Gunakan HTTPS atau terowong SSH.
- Tandatangan membuktikan apa yang dirakam tidak diubah, bukan bahawa setiap peristiwa Telegram telah dirakam.

[Berkongsi akses kepada satu kes](https://phishdestroy.github.io/TgWitness/ms/docs/access/) dengan kebenaran, tarikh luput dan had sesi. Token saksi kekal sebagai kelayakan berasingan.

## Mengukuhkan pemasangan

0 daripada 8 telah selesai

1. **Gunakan akaun Telegram khusus** — jangan sekali-kali akaun utama anda. Token panel dan sesi memberikan kawalan penuh ke atasnya.
2. **Biarkan panel pada 127.0.0.1.** Aksesnya secara jauh hanya melalui HTTPS (konfigurasi Caddy yang disertakan) atau terowong SSH.
3. **Sulitkan cakera** yang mengandungi direktori data: teks mesej dan media disimpan seperti mana ia diterima.
4. **Hadkan direktori data** kepada akaun perkhidmatan. Direktori baru mendapat mod 0700 pada Unix; pada Windows, tetapkan kebenaran folder.
5. **Simpan kunci induk peti di lokasi lain** pada pelayan: tetapkan `TGWITNESS_VAULT_KEY_FILE` sebelum mencipta direktori data.
6. **Simpan cap jari kunci penandatanganan dan titik pemeriksaan** pada sistem lain, dan tambahkan saksi pada hos lain.
7. **Jangan muat naik** `data/`, sesi, `panel-token.txt` atau kunci vault ke GitHub atau sembang.
8. **Jangan log** penanda aras `Authorization` atau badan permintaan di proksi terbalik.

**Bolehkah saya menukar token panel tanpa kehilangan data?**

Ya. Token hanya membuka panel. Hentikan TgWitness, padamkan `panel-token.txt` daripada direktori data dan mulakan semula; jurnal, sesi dan kunci tidak terjejas. Apabila `TGWITNESS_TOKEN` ditetapkan, nilai persekitaran digunakan sebaliknya fail.

**Mengapa mesej tidak disulitkan semasa disimpan?**

Pengumpul mesti membacanya untuk mencari, membandingkan versi dan mengeksport. Mengkripsi dengan kunci pada mesin yang sama hanya menambah sedikit perlindungan terhadap seseorang yang boleh membaca mesin tersebut. Penyulitan cakera melindungi cakera yang dimatikan atau dicuri; kebenaran ketat melindungi cakera yang sedang berjalan.

## Laporkan kerentanan

Gunakan **Security → Laporkan kerentanan** di repositori GitHub. Sertakan versi, impak dan reproduksi sintetik minimum. Jangan sekali-kali menghantar maklumat log masuk, direktori akaun atau arkib bukti sebenar. Jika pelaporan peribadi tidak tersedia, buka isu untuk meminta saluran peribadi tanpa butiran eksploitasi.
