# Gunakan akaun berasingan. Jangan sekali-kali akaun utama anda.

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/dedicated-account/

Bacalah sebelum anda menyambungkan akaun

Nasihat kami untuk tidak menggunakan akaun utama anda bukanlah gurauan. Ia adalah realiti.

Akaun utama

- Hash aplikasi anda sendiri: 99% log keluar
- Larangan hanya kerana tahap kepercayaan rendah adalah kerap
- Menggunakannya adalah idea yang sangat bodoh

Akaun tambahan pada pasangan awam

- Lebih sejuta akaun didaftarkan melalui pasangan ini
- Pasangan-pasangan ini telah wujud selama lebih 5 tahun
- Tiada siapa pun dapat melihat apa-apa daripada anda melalui mereka

01

## Mengapa bukan akaun utama anda

Ini adalah maklumat yang tepat. Kami tahu dengan tepat di mana perangkap masalah-masalah ini terletak.

1. ### Hash aplikasi anda sendiri: 99% log keluar

   Log masuk ke my.telegram.org daripada akaun yang anda tidak mempunyai akses, untuk mendapatkan hash aplikasi, dan kemudian sebarang permintaan melalui hash aplikasi itu bermakna terdapat 99% kemungkinan akaun tersebut telah dilog keluar. Anda boleh menyemakinya.
2. ### Larangan hanya kerana tahap kepercayaan rendah adalah kerap

   Akaun diharamkan semata-mata kerana Telegram tidak mempercayainya, dan larangan sedemikian kerap berlaku. Anda juga boleh menyemak perkara ini. Menggunakan akaun sendiri adalah idea yang sangat bodoh.
3. ### Kunci sesi yang disalin boleh dibatalkan

   Menggunakan kunci TData/session yang diimport dalam Telegram Desktop dan TgWitness pada masa yang sama boleh mencetuskan `AUTH_KEY_DUPLICATED`. Telegram membatalkan kebenaran itu, jadi kedua-dua salinan memerlukan log masuk baru. Akaun khusus tidak dapat menghalang perkara ini.

   Tutup sepenuhnya klien asal dan biarkan ia tertutup semasa menggunakan sesi yang diimport. Untuk penggunaan selari, log masuk ke TgWitness melalui telefon atau QR untuk mencipta kebenaran berasingan; klien lain yang dibenarkan secara berasingan boleh terus log masuk.

   [Baca amaran import sesi](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ms#session-warning)

Dokumentasi Telegram

- [Ralat log keluar: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Mencipta hash aplikasi anda sendiri: mendapatkan api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Mengapa TgWitness berfungsi melalui pasangan hash aplikasi/ID aplikasi awam

Itulah sebabnya kami membina TgWitness pada pasangan hash aplikasi/ID aplikasi awam. Menurut logik kami, larangan kurang mungkin berlaku dengan mereka: lebih daripada sejuta akaun Telegram telah didaftarkan melalui pasangan ini, dan banyak program berbeza berfungsi melalui mereka. Menurut logik kami, ini lebih baik daripada bekerja terus dengan hash aplikasi peribadi: pasangan ini sudah wujud selama lebih 5 tahun dengan pasti.

### Pasangan baharu anda sendiri

Dicipta di my.telegram.org daripada akaun.

- Kira-kira 99% akaun telah log keluar
- Satu aplikasi baharu, satu akaun

### Pasangan awam kolam

Pasangan yang sama digunakan oleh banyak program.

- Lebih sejuta akaun telah didaftarkan
- Banyak program yang berbeza
- Beroperasi selama 5+ tahun

### Mengapa tiada siapa pun dapat melihat apa-apa daripada anda melalui pasangan ini

- #### Pasangan adalah nama, bukan kunci

  Telegram meminta ID API dan hash API apabila program menyambung dan apabila ia meminta kod log masuk. Mereka mengenal pasti aplikasi dan tidak memberikan sebarang akses kepada mana-mana akaun; dokumentasi Telethon menyatakan bahawa satu pasangan berfungsi dengan mana-mana nombor telefon.
- #### Kunci sesi anda tidak pernah meninggalkan pelayan anda

  Log masuk menghasilkan kunci kebenaran melalui pertukaran Diffie–Hellman antara TgWitness dan Telegram anda; kunci itu sendiri tidak pernah dihantar. Dokumentasi Telegram: selepas kebenaran, kunci itu menjadi dikaitkan dengan pengguna, dan setiap panggilan dengan kunci ini dijalankan sebagai pengguna tersebut. Program lain dengan pasangan yang sama mempunyai kunci mereka sendiri dan tidak dapat menggunakan kunci anda.
- #### Lalu lintas disulitkan dengan kunci anda

  Setiap permintaan dan jawapan disulitkan dengan kunci kebenaran sesi, bukan dengan hash API. Mengetahui hash API tidak dapat menyahsulitkan apa-apa.
- #### Pemilik sepasang tidak melihat apa-apa

  Telegram tidak mempunyai kaedah yang menyenaraikan akaun, sesi atau mesej mengikut ID API. Pemilik sepasang hanya melihat tetapan aplikasi mereka di my.telegram.org.
- #### Hanya akaun anda yang dapat melihat aplikasi mana ia

  Tetapan → Peranti pada akaun anda menyenaraikan nama aplikasi dan ID API setiap sesi, peranti, alamat IP dan tarikh. Tiada siapa lain mendapat senarai ini.

Dokumentasi Telegram

- [Pengesahan pengguna: kunci menjadi pengguna](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [inisiasi sambungan](https://core.telegram.org/method/initConnection)
- [Mencipta kunci kebenaran](https://core.telegram.org/mtproto/auth_key)
- [Sulitan MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Apa yang direkodkan oleh rekod sesi](https://core.telegram.org/constructor/authorization)
- [Memperoleh api_id](https://core.telegram.org/api/obtaining_api_id)
- [Kod sumber terbuka aplikasi Telegram](https://telegram.org/apps#source-code)

Perpustakaan dan perbincangan

- [Telethon: menandatangani masuk](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: API aplikasi rasmi](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: patutkah api_hash disimpan secara rahsia?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Pasangan yang sama dalam program lain 7

Pasangan aplikasi rasmi Telegram adalah awam dan terbina dalam banyak program dan perpustakaan bebas:

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

  Senarai forum pasangan aplikasi rasmi, diterbitkan untuk mendaftarkan akaun

03

## Cara untuk membuat akaun tambahan

Akaun Telegram memerlukan nombor telefon yang menerima kod log masuk. Pilih tempoh hayat akaun tersebut.

- Pilihan terbaik

  ### SIM prabayar atau eSIM

  ********

  Tahan lama

  Selagi anda terus menambah baki

  Berhati-hati

  Yang paling boleh dipercayai: Telegram menerima nombor mudah alih sebenar dengan terbaik. Nombor yang diambil semula oleh pembekal akan diberikan kepada orang lain.
- ### Aplikasi nombor maya

  ********

  Tahan lama

  Walaupun aplikasi mengekalkan nombor

  Berhati-hati

  Telegram mungkin menolak nombor maya, tidak menghantar kod atau mengehadkan akaun baru serta-merta; sesetengah aplikasi mengambil balik nombor yang tidak digunakan.
- ### Nombor penyewaan

  ********

  Tahan lama

  Tempoh sewaan

  Berhati-hati

  Apabila ia berakhir, nombor itu beralih kepada pelanggan seterusnya.
- ### Aktivasi sekali sahaja

  ********

  Tahan lama

  Satu kod

  Berhati-hati

  Nombor itu kembali ke kolam dengan segera, seringkali dengan sejarah pemilik sebelumnya. Tetapkan kata laluan awan sebelum apa-apa lagi.

Sesiapa yang memegang nombor itu kemudian boleh meminta kod log masuk. Kata laluan awan (pengesahan dua langkah) menghalang mereka daripada log masuk; tanpanya akaun itu milik pemilik nombor seterusnya.

Dokumentasi Telegram

- [FAQ Spam: nombor maya dan pemilik terdahulu](https://telegram.org/faq_spam)
- [Pengesahan dua langkah](https://core.telegram.org/api/srp)

### Nombor +888 disewa (Fragment)

Sesetengah pasaran dan perkhidmatan menawarkan penyewaan sementara nombor +888 rasmi Telegram daripada Fragment.

Anggaran harga: US $20 sehari.

- Anda boleh mendaftar akaun terus di Telegram Web atau Telegram Desktop.
- Anda boleh memadam akaun pada nombor tersebut dan mencipta yang baru.
- Akaun-akaun ini umumnya menghadapi pemeriksaan anti-penipuan yang lebih sedikit, tetapi ia tidak memberikan imuniti atau keistimewaan khas.

Nombor ini bukan milik anda. Setelah tempoh sewaan tamat, pemilik boleh menuntutnya semula. Tetapkan kata laluan awan dengan segera dan jangan anggap akaun ini bersifat jangka panjang.

Memiliki +888 sendiri atau menggunakan SIM prabayar yang anda kawal kekal lebih boleh dipercayai.

### Akaun siap pakai dari pasaran

Sesetengah pasaran (contohnya G2G atau Z2U) menjual akaun Telegram siap pakai — baharu, lama, atau dengan fail sesi.

- [G2G: Senarai akaun Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Senarai akaun Telegram](https://www.z2u.com/telegram/accounts-5-15140)

JANGAN PERNAH MENGGUNAKAN AKAUN UTAMA ANDA! Akaun khusus yang diperoleh dengan cara ini masih lebih selamat daripada memasukkan akaun Telegram utama anda ke dalam TgWitness.

#### Amaran sebelum pembelian

- Ini melanggar Terma Perkhidmatan Telegram.
- Banyak akaun didaftarkan secara besar-besaran (auto-reg) atau mempunyai sejarah yang tidak diketahui.
- Sesetengah penjual mungkin masih mempunyai akses pemulihan.
- Akaun daripada pasaran sedemikian sering diharamkan atau dihadkan kemudian.
- Elakkan pasaran yang secara terbuka menjual perisian pencuri, alat pancingan, atau akaun yang jelas dicuri.
- Membeli akaun — walaupun yang diiklankan sebagai auto-reg — daripada platform yang secara terbuka menjual alat pancingan, pencuri, sesi curi atau akaun mencabul bukan sahaja Terma Perkhidmatan Telegram tetapi juga undang-undang kebanyakan negara. Ini boleh membatalkan bukti anda kemudian. Pilih dengan berhati-hati.

#### Jika anda menggunakan pilihan ini

1. Anggap akaun ini boleh dibuang.
2. Tamatkan semua sesi lain, tetapkan kata laluan awan dan ubah kaedah pemulihan dengan segera.
3. Gunakan 2–3 akaun daripada penyedia berbeza atau akaun yang anda daftarkan sendiri.

**Premium, pemadaman dan kelewatan tujuh hari**

Jika akaun mempunyai Premium, seseorang yang mempunyai akses kepada nombor telefon tidak boleh memadam akaun dengan segera. Anda akan menerima pemberitahuan dan mempunyai tujuh hari sebelum ia dipadamkan.

Ini penting kerana siasatan anda bergantung pada akaun ini: anda mempunyai masa untuk menyediakan pengganti.

**Akaun baharu dan kelayakan API**

Jika anda mendapatkan dan menggunakan api_id/api_hash anda sendiri daripada akaun baru yang anda daftarkan sendiri menggunakan nombor daripada perkhidmatan SMS, akaun tersebut akan log keluar pada permintaan API pertama atau kebenaran sesi. Perlu diingat perkara ini apabila merancang siasatan.

04

## Mencipta akaun

Daripada nombor ke sembang pertama yang direkodkan.

1. ### Dapatkan nombor

   SIM prabayar atau eSIM apabila akaun perlu bertahan lama; penyewaan atau pengaktifan sekali sahaja untuk kerja jangka pendek. Perkhidmatan disenaraikan di bawah.
2. ### Daftar berasingan daripada akaun utama anda

   Daftar dalam aplikasi Telegram rasmi pada peranti berasingan, emulator atau profil telefon, bukan bersebelahan akaun utama anda.
3. ### Kunci dengan kata laluan awan

   Segera tetapkan kata laluan awan dan emel pemulihan yang tidak digunakan di tempat lain.
4. ### Tutup tetapan privasi

   Nombor telefon **Tiada siapa**, cari saya melalui nombor saya **Kenalan saya**, terakhir dilihat, foto profil dan bio **Tiada siapa** atau **Kenalan saya**; matikan penyegerakan kenalan.
5. ### Hindarkan ia daripada memusnahkan diri sendiri

   Atur pemusnahan akaun ke tempoh terpanjang, supaya TgWitness yang dihentikan tidak menyebabkan anda kehilangan akaun.
6. ### Berikan profil neutral

   Tiada nama, foto, nama pengguna atau bio daripada akaun lain anda, tiada kenalan peribadi.
7. ### Biarkan ia memanas

   Sertailah beberapa perbualan sehari pada mulanya. Akaun baru yang tergesa-gesa akan dihadkan terlebih dahulu.
8. ### Jangan kongsi apa-apa dengan bot

   Jangan sekali-kali menekan "Berkongsi nombor telefon" atau "Berkongsi lokasi" untuk bot. Buka pautan dan Mini Apps melalui VPN atau proksi pada peranti tersebut.
9. ### Sambungkannya ke TgWitness

   Di ruang kerja anda sendiri, sambungkan dengan **Akaun → Kod QR**, kemudian tekan **Sumber → Mod Siasatan**. Aplikasi adalah tempat anda bertindak, TgWitness adalah rekodnya.

Dokumentasi Telegram

- [Pengesahan dua langkah](https://core.telegram.org/api/srp)
- [Tetapan privasi](https://core.telegram.org/api/privacy)
- [Akaun bunuh diri](https://core.telegram.org/method/account.setAccountTTL)

05

## Nombor perkhidmatan

Pilihan untuk bermula. Negara, harga dan sama ada Telegram menerima perubahan nombor sering berubah; semak sebelum membayar.

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

  Pelan PayGo, sangat murah
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

### Aplikasi nombor maya 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  AS sahaja; pendaftaran memerlukan nombor AS
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Nombor akan diambil semula jika anda tidak menggunakannya
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
  - Dibayar

  Dengan tempoh percubaan
- [Hushedhushed.com](https://hushed.com)

  - Banyak negara
  - Dibayar

  Murah
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

  Nombor mudah alih Eropah dalam aplikasi
- [Sonetelsonetel.com](https://sonetel.com)

  - Banyak negara
  - Nombor percuma
- [Zadarmazadarma.com](https://zadarma.com)

  - Banyak negara

  Nombor maya

### Nombor penyewaan dan aktivasi 12

Sewaan mengekalkan nombor selama berminggu-minggu atau berbulan-bulan. Pengaktifan sekali sahaja memberikan satu kod: tetapkan kata laluan awan sebaik sahaja mendaftar.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Sewaan
  - Aktivasi
- [SMSPVAsmspva.com](https://smspva.com)

  - Sewaan
  - Aktivasi
- [5SIM5sim.net](https://5sim.net)

  - Sewaan
  - Aktivasi
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Sewaan
  - Satu kali
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Sewaan
  - Aktivasi
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Sewaan
  - Aktivasi
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Sewaan
  - Aktivasi
- [365SMS365sms.org](https://365sms.org)

  - Sewaan
  - Aktivasi
- [SIMSMSsimsms.org](https://simsms.org)

  - Sewaan
  - Aktivasi
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Satu kali
- [SMS-MANsms-man.com](https://sms-man.com)

  - Satu kali
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Satu kali
