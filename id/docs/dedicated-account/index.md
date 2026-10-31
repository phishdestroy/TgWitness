# Gunakan akun terpisah. Jangan pernah menggunakan akun utama Anda.

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/dedicated-account/

Baca sebelum Anda menghubungkan akun

Saran kami agar Anda tidak menggunakan akun utama Anda bukanlah lelucon. Ini adalah kenyataan.

Akun utama

- Dengan hash aplikasi Anda sendiri, 99% akun akan keluar
- Pemblokiran akun hanya karena tingkat kepercayaan yang rendah sering terjadi
- Menggunakan akun utama Anda adalah ide yang benar-benar bodoh

Akun tambahan pada pasangan ID API/hash API publik

- Lebih dari satu juta akun telah didaftarkan melalui pasangan ID API/hash API ini
- Pasangan API ID/API hash ini telah aktif selama lebih dari 5 tahun
- Tidak ada yang dapat melihat data Anda apa pun melalui pasangan API ini

01

## Mengapa Anda tidak boleh menggunakan akun utama Anda

Ini adalah informasi yang akurat. Kami tahu persis di mana letak kendala dari masalah-masalah ini.

1. ### Dengan hash aplikasi Anda sendiri, 99% akun akan keluar

   Masuk ke my.telegram.org menggunakan akun yang tidak Anda miliki aksesnya, untuk mendapatkan hash aplikasi, dan kemudian setiap permintaan yang dilakukan melalui hash aplikasi tersebut berarti ada kemungkinan 99% bahwa akun tersebut telah keluar. Anda dapat memeriksanya.
2. ### Pemblokiran akun hanya karena tingkat kepercayaan yang rendah sering terjadi

   Akun diblokir hanya karena Telegram tidak mempercayainya, dan pemblokiran semacam itu sering terjadi. Anda juga dapat memeriksanya. Menggunakan akun Anda sendiri adalah ide yang benar-benar bodoh.
3. ### Kunci sesi yang disalin dapat dicabut

   Menjalankan kunci TData/sesi yang diimpor di Telegram Desktop dan TgWitness secara bersamaan dapat memicu pesan `AUTH_KEY_DUPLICATED`. Telegram akan membatalkan otorisasi tersebut, sehingga kedua salinan tersebut memerlukan proses login baru. Akun khusus tidak dapat mencegah hal ini.

   Tutup sepenuhnya klien asli dan biarkan tetap tertutup saat menggunakan sesi yang diimpor. Untuk penggunaan paralel, masuk ke TgWitness melalui ponsel atau QR untuk membuat otorisasi terpisah; klien lain yang telah diotorisasi secara terpisah dapat tetap masuk.

   [Baca peringatan impor sesi](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=id#session-warning)

Dokumentasi Telegram

- [Kesalahan saat logout: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Membuat hash aplikasi Anda sendiri: mendapatkan api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Mengapa TgWitness beroperasi melalui pasangan app hash dan app ID publik

Itulah mengapa kami membangun TgWitness berdasarkan pasangan hash aplikasi/ID aplikasi publik. Menurut logika kami, risiko pemblokiran lebih kecil dengan menggunakan pasangan tersebut: lebih dari satu juta akun Telegram telah terdaftar melalui pasangan ini, dan banyak program berbeda beroperasi melalui pasangan tersebut. Menurut logika kami, ini lebih baik daripada bekerja langsung dengan hash aplikasi pribadi: pasangan ini sudah pasti ada selama lebih dari 5 tahun.

### Pasangan API ID/API hash baru Anda sendiri

Dibuat di my.telegram.org dari akun tersebut.

- Sekitar 99% dari akun-akun ini akan keluar secara otomatis
- Satu aplikasi baru, satu akun

### Pasangan ID API publik/API hash dari kumpulan

Pasangan API ID/API hash yang sama yang digunakan oleh banyak program.

- Lebih dari satu juta akun terdaftar
- Berbagai program yang berbeda
- Pasangan API ini telah beroperasi selama lebih dari 5 tahun

### Mengapa tidak ada yang dapat melihat data Anda melalui pasangan API ini

- #### Pasangan API tersebut adalah nama, bukan kunci

  Telegram meminta ID API dan hash API saat sebuah program terhubung dan saat meminta kode login. Keduanya berfungsi untuk mengidentifikasi aplikasi dan tidak memberikan akses ke akun apa pun; dokumentasi Telethon menyebutkan bahwa satu pasangan ID dan hash tersebut dapat digunakan dengan nomor telepon apa pun.
- #### Kunci sesi Anda tidak pernah meninggalkan server Anda

  Proses masuk (login) menciptakan kunci otorisasi melalui pertukaran Diffie–Hellman antara TgWitness Anda dan Telegram; kunci itu sendiri tidak pernah dikirim. Dokumentasi Telegram: setelah otorisasi, kunci tersebut dikaitkan dengan pengguna, dan setiap panggilan yang menggunakan kunci ini dijalankan sebagai pengguna tersebut. Program lain dengan pasangan kunci yang sama memiliki kunci mereka sendiri dan tidak dapat menggunakan kunci Anda.
- #### Lalu lintas data dienkripsi menggunakan kunci Anda

  Setiap permintaan dan respons dienkripsi menggunakan kunci otorisasi sesi, bukan menggunakan hash API. Mengetahui hash API tidak akan mendekripsi apa pun.
- #### Pemilik pasangan ID API/hash API tidak melihat apa pun

  Telegram tidak memiliki metode yang menampilkan daftar akun, sesi, atau pesan berdasarkan ID API. Pemilik pasangan akun tersebut hanya dapat melihat pengaturan aplikasinya di my.telegram.org.
- #### Hanya akun Anda yang dapat melihat aplikasi mana yang dimaksud

  Pengaturan → Perangkat pada akun Anda mencantumkan nama aplikasi dan ID API, perangkat, alamat IP, serta tanggal dari setiap sesi. Tidak ada orang lain yang mendapatkan daftar ini.

Dokumentasi Telegram

- [Otorisasi pengguna: kunci tersebut terikat pada pengguna](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Membuat kunci otorisasi MTProto](https://core.telegram.org/mtproto/auth_key)
- [Enkripsi MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Apa saja yang terkandung dalam entri otorisasi (sesi) Telegram](https://core.telegram.org/constructor/authorization)
- [Mendapatkan api_id](https://core.telegram.org/api/obtaining_api_id)
- [Kode sumber terbuka aplikasi Telegram](https://telegram.org/apps#source-code)

Pustaka dan utas diskusi

- [Telethon: masuk ke Telegram](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: kredensial API dari aplikasi resmi](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: apakah api_hash harus dijaga kerahasiaannya?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Pasangan API ID/API hash yang sama di program lain 7

Pasangan API ID/API hash dari aplikasi Telegram resmi bersifat publik dan terintegrasi ke dalam banyak program dan pustaka independen:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Sebuah postingan forum yang mencantumkan pasangan API ID/API hash dari aplikasi Telegram resmi, yang dipublikasikan untuk mendaftarkan akun

03

## Cara membuat akun tambahan

Akun Telegram memerlukan nomor telepon untuk menerima kode login. Pilih berdasarkan berapa lama akun tersebut harus tetap aktif.

- Pilihan terbaik

  ### SIM prabayar atau eSIM

  ********

  Berapa lama masa berlakunya

  Selama Anda terus mengisi ulang saldo

  Perlu diingat

  Yang paling andal: Telegram paling baik menerima nomor ponsel asli. Nomor yang ditarik kembali oleh operator akan diberikan kepada orang lain.
- ### Aplikasi dengan nomor telepon virtual

  ********

  Berapa lama masa berlakunya

  Selama aplikasi tersebut menyimpan nomor telepon tersebut

  Perlu diingat

  Telegram mungkin menolak nomor virtual, tidak mengirimkan kode, atau langsung membatasi akun baru; beberapa aplikasi menarik kembali nomor yang tidak digunakan.
- ### Penyewaan nomor telepon

  ********

  Berapa lama masa berlakunya

  Untuk masa sewa

  Perlu diingat

  Setelah selesai, nomor tersebut akan dialihkan ke pelanggan berikutnya.
- ### Aktivasi satu kali

  ********

  Berapa lama masa berlakunya

  Hanya satu kode login

  Perlu diingat

  Nomor tersebut langsung kembali ke kumpulan, seringkali disertai riwayat pemilik sebelumnya. Tetapkan kata sandi cloud sebelum melakukan hal lain.

Siapa pun yang memiliki nomor tersebut di kemudian hari dapat meminta kode login. Kata sandi cloud (verifikasi dua langkah) mencegah mereka masuk; tanpa kata sandi tersebut, akun tersebut menjadi milik pemilik nomor berikutnya.

Dokumentasi Telegram

- [FAQ Spam: nomor virtual dan pemilik sebelumnya](https://telegram.org/faq_spam)
- [Verifikasi dua langkah](https://core.telegram.org/api/srp)

### Nomor +888 yang disewa (Fragment)

Beberapa pasar dan layanan menawarkan penyewaan sementara nomor +888 resmi Telegram dari Fragment.

Perkiraan harga: US$20 per hari.

- Anda dapat mendaftarkan akun secara langsung di Telegram Web atau Telegram Desktop.
- Anda dapat menghapus akun pada nomor tersebut dan membuat yang baru.
- Akun-akun ini umumnya menghadapi lebih sedikit pemeriksaan anti-penipuan, tetapi tidak memberikan kekebalan atau hak istimewa khusus.

Nomor tersebut bukan milik Anda. Setelah masa sewa berakhir, pemilik dapat mengambilnya kembali. Segera atur kata sandi cloud dan jangan menganggap akun ini sebagai akun jangka panjang.

Memiliki nomor +888 sendiri atau menggunakan SIM prabayar yang Anda kendalikan tetap lebih dapat diandalkan.

### Akun siap pakai dari pasar online

Beberapa pasar (misalnya G2G atau Z2U) menjual akun Telegram siap pakai — baru, yang sudah lama, atau dengan file sesi.

- [G2G: Daftar akun Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Daftar akun Telegram](https://www.z2u.com/telegram/accounts-5-15140)

JANGAN PERNAH MENGGUNAKAN AKUN UTAMA ANDA! Akun khusus yang diperoleh dengan cara ini tetap lebih aman daripada memasukkan akun Telegram utama Anda ke dalam TgWitness.

#### Peringatan sebelum pembelian

- Hal ini melanggar Ketentuan Layanan Telegram.
- Banyak akun yang didaftarkan secara massal (pendaftaran otomatis) atau memiliki riwayat yang tidak diketahui.
- Beberapa penjual mungkin masih memiliki akses pemulihan.
- Akun dari pasar semacam itu sering kali diblokir atau dibatasi di kemudian hari.
- Hindari pasar gelap yang secara terbuka menjual perangkat pencurian, alat phishing, atau akun yang jelas-jelas dicuri.
- Membeli akun — bahkan yang diiklankan sebagai "auto-reg" — dari platform yang secara terbuka menjual alat phishing, pencuri data, sesi yang dicuri, atau akun, tidak hanya melanggar Ketentuan Layanan Telegram tetapi juga undang-undang di sebagian besar negara. Hal ini dapat membuat bukti Anda tidak sah di kemudian hari. Pilihlah dengan hati-hati.

#### Jika Anda menggunakan opsi ini

1. Perlakukan akun ini sebagai akun sekali pakai.
2. Akhiri semua sesi lainnya, atur kata sandi cloud, dan ubah metode pemulihan segera.
3. Gunakan 2–3 akun dari penyedia yang berbeda atau akun yang Anda daftarkan sendiri.

**Premium, penghapusan, dan penundaan tujuh hari**

Jika akun tersebut memiliki Premium, seseorang yang memiliki akses ke nomor telepon tersebut tidak dapat langsung menghapus akun tersebut. Anda akan menerima pemberitahuan dan memiliki waktu tujuh hari sebelum akun tersebut dihapus.

Hal ini penting karena penyelidikan Anda bergantung pada akun tersebut: Anda masih memiliki waktu untuk menyiapkan akun pengganti.

**Akun baru dan kredensial API**

Jika Anda memperoleh dan menggunakan api_id/api_hash Anda sendiri dari akun baru yang Anda daftarkan sendiri menggunakan nomor dari layanan SMS, akun tersebut akan keluar pada permintaan API pertama atau otorisasi sesi. Ingatlah hal ini saat merencanakan penyelidikan.

04

## Membuat akun

Mulai dari mendapatkan nomor telepon hingga obrolan pertama yang terekam.

1. ### Dapatkan nomor telepon

   SIM prabayar atau eSIM jika akun harus aktif dalam jangka panjang; sewa atau aktivasi satu kali untuk pekerjaan jangka pendek. Layanan-layanan tersebut tercantum di bawah ini.
2. ### Daftarkan akun terpisah dari akun utama Anda

   Daftarkan diri Anda di aplikasi Telegram resmi menggunakan perangkat terpisah, emulator, atau profil ponsel, bukan di perangkat yang sama dengan akun utama Anda.
3. ### Lindungi akun dengan kata sandi cloud

   Segera atur kata sandi cloud dan alamat email pemulihan yang tidak digunakan di tempat lain.
4. ### Batasi pengaturan privasi akun

   Nomor telepon **"Tidak ada**", "Temukan saya melalui nomor saya", **"Kontak saya**", "Terakhir terlihat", foto profil, dan bio **"Tidak ada"** atau "**Kontak saya**"; matikan sinkronisasi kontak.
5. ### Mencegah akun agar tidak terhapus secara otomatis

   Atur fitur penghancuran otomatis akun ke periode terpanjang, sehingga TgWitness yang dihentikan tidak akan membuat Anda kehilangan akun.
6. ### Buat profil yang netral untuk akun tersebut

   Tidak ada nama, foto, nama pengguna, atau deskripsi profil dari akun Anda yang lain, serta tidak ada kontak pribadi.
7. ### Biarkan akun baru tersebut 'beradaptasi'

   Pada awalnya, bergabunglah hanya di beberapa obrolan setiap hari. Akun baru yang terburu-buru akan dibatasi terlebih dahulu.
8. ### Jangan berbagi apa pun dengan bot

   Jangan pernah menekan tombol “Bagikan nomor telepon” atau “Bagikan lokasi” untuk bot. Buka tautan dan Mini Apps melalui VPN atau proxy di perangkat tersebut.
9. ### Hubungkan akun tersebut ke TgWitness

   Di ruang kerja Anda sendiri, sambungkan melalui **Akun → Kode QR**, lalu tekan **Sumber → Mode Investigasi**. Aplikasi ini adalah tempat Anda bertindak, sedangkan TgWitness adalah pencatatnya.

Dokumentasi Telegram

- [Verifikasi dua langkah](https://core.telegram.org/api/srp)
- [Pengaturan privasi](https://core.telegram.org/api/privacy)
- [Penghapusan otomatis akun jika tidak aktif](https://core.telegram.org/method/account.setAccountTTL)

05

## Layanan nomor telepon

Ini adalah opsi-opsi untuk memulai. Negara, harga, dan apakah Telegram menerima nomor tertentu sering berubah, jadi periksa terlebih dahulu sebelum membayar.

### SIM prabayar dan eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Prabayar

  Paket PayGo, sangat murah
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Prabayar
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Prabayar
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Prabayar
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Aplikasi dengan nomor telepon virtual 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Hanya untuk AS; pendaftaran memerlukan nomor telepon AS
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Nomor tersebut akan ditarik kembali jika Anda tidak menggunakannya
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Negara lain
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - Layanan berbayar

  Dengan masa uji coba
- [Hushedhushed.com](https://hushed.com)

  - Banyak negara
  - Layanan berbayar

  Harga murah
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Nomor ponsel Eropa dalam sebuah aplikasi
- [Sonetelsonetel.com](https://sonetel.com)

  - Banyak negara
  - Nomor gratis
- [Zadarmazadarma.com](https://zadarma.com)

  - Banyak negara

  Nomor telepon virtual

### Penyewaan nomor telepon dan aktivasi satu kali 12

Dengan menyewa nomor telepon, Anda dapat menggunakannya selama berminggu-minggu atau berbulan-bulan. Aktivasi satu kali akan memberikan satu kode login: atur kata sandi cloud segera setelah mendaftar.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Penyewaan nomor
  - Aktivasi satu kali
- [SMSPVAsmspva.com](https://smspva.com)

  - Penyewaan nomor
  - Aktivasi satu kali
- [5SIM5sim.net](https://5sim.net)

  - Penyewaan nomor
  - Aktivasi satu kali
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Penyewaan nomor
  - Aktivasi satu kali
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Penyewaan nomor
  - Aktivasi satu kali
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Penyewaan nomor
  - Aktivasi satu kali
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Penyewaan nomor
  - Aktivasi satu kali
- [365SMS365sms.org](https://365sms.org)

  - Penyewaan nomor
  - Aktivasi satu kali
- [SIMSMSsimsms.org](https://simsms.org)

  - Penyewaan nomor
  - Aktivasi satu kali
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Aktivasi satu kali
- [SMS-MANsms-man.com](https://sms-man.com)

  - Aktivasi satu kali
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Aktivasi satu kali
