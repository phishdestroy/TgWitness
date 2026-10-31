# Permulaan pantas

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/

Setiap cara untuk memasang dan melancarkan TgWitness: pakej Windows, Python, Docker dan demo sintetik, dengan pemeriksaan awal.

**Inggeris** · [Bahasa Rusia](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Bahasa Ukraine](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Sepanyol](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Portugis (Brazil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Bahasa Turki](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [Bahasa Arab](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [Bahasa Parsi](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Bahasa Vietnam](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Teks ringkas Cina](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness adalah aplikasi berdiri sendiri untuk memerhati kumpulan dan saluran Telegram yang boleh diakses oleh akaun anda. Ia berjalan secara tempatan dengan direktori data tersendiri.

**Lawatan pertama kali?** [Terokai demo](https://phishdestroy.github.io/TgWitness/ms/docs/reference/quickstart/#explore-the-interface) sebelum menyambungkan akaun. [Pilih panduan](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) untuk proksi, saksi, eksport atau penyediaan pelayan.

## Pasang dan mulakan

[Pengumpulan melalui GitHub Actions (pratonton)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Pilih satu kaedah. Muat turun mudah alih akan tersedia selepas binaan rilis diterbitkan:

| Penyedia hos | Tiada pemasangan | Daripada sumber: Python 3.11+ | Docker: Engine/Desktop dengan Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | Ekstrak `TgWitness-<version>-windows-amd64-portable.zip` daripada GitHub Releases, klik dua kali `TgWitness.cmd` | Klik dua kali `Start.cmd` | Klik dua kali `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Untuk kaedah sumber, muat turun dan ekstrak fail ZIP sumber daripada GitHub Releases atau klon repositori. `Start.cmd` menawarkan pemasangan Python 3.12 untuk pengguna Windows anda jika tiada Python yang sesuai ditemui (winget, atau pemasang python.org yang disahkan). `start.sh` mencetak arahan pemasangan tepat untuk pengedaran Linux anda atau macOS jika Python tiada. Pelancaran sumber pertama mencipta `.venv` dan memasang kebergantungan secara automatik.

Docker membina aplikasi dan memulakannya di latar belakang; Python hos tidak diperlukan. `scripts\Docker.cmd` dan `scripts/docker-start.sh` mencetak alamat panel dan token apabila kontena sihat. Perintah Docker yang setara pada setiap hos yang disokong ialah:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Buka **http://127.0.0.1:8787**. Gunakan token yang dicetak oleh pembantu Docker atau arahan Docker kedua, atau baca **data/live/panel-token.txt** untuk pemasangan mudah alih atau sumber. Teruskan di **Sambungkan Telegram** di bawah. Pemasangan asli dan Docker menggunakan storan berasingan; memulakan Docker tidak mengimport jurnal asli sedia ada.

Untuk pelayan, [penyebaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/) merangkumi HTTPS automatik, permulaan semula, imej yang diterbitkan, kemas kini, dan sandaran.

## Terokai antaramuka

1. Jalankan **TgWitness-Demo.cmd** dalam pakej mudah alih, **scripts\Demo.cmd** dalam folder sumber Windows, atau `sh start.sh --demo` pada Linux/macOS. Pelancaran sumber pertama kali mencipta `.venv` dan memasang kebergantungan.
2. Buka **http://127.0.0.1:8787**.
3. Demo tempatan membuka jurnal sampel secara automatik. Tiada salinan token diperlukan untuk akses tempatan secara langsung.

Mesej demo adalah rekaan. Mod demo tidak dapat menyambungkan akaun Telegram sebenar.

## Sambungkan Telegram

> [!AMARAN] **Jangan gunakan apa-apa yang anda tidak mampu kehilangan.** Kami sangat menasihatkan agar tidak menyambungkan akaun peribadi atau berharga dan tidak mencipta ID/hash API pada akaun yang anda hargai. Telegram mengharamkan akaun secara tidak menentu dan sering kali kekal, tanpa mengira klien. Jalannya ujian yang lancar bergantung pada Telegram, bukan pada TgWitness, dan tidak menjamin apa-apa untuk masa hadapan.

1. Jika demo asli sedang berjalan, hentikannya dan jalankan **Start.cmd** atau `sh start.sh`. Jika tidak, biarkan pemasangan langsung yang sedang berjalan di atas terus berjalan.
2. Gunakan token panel untuk kaedah pemasangan anda untuk membuka panel.
3. Jika anda memerlukan proksi, simpannya di bawah **Akaun → Tetapan → Tetapan sambungan → Ubah laluan sambungan**.
4. Di **Akaun**, masukkan nombor telefon anda dan tekan **Teruskan**, pilih **Kod QR → Tunjukkan Kod QR**, atau pilih fail dan tekan **Sambungkan akaun**. **ID API + Hash** adalah pilihan: ruang kerja menggunakan pasangan yang disimpan atau diimport, atau pasangan berfungsi daripada kolam terbina dalam. Untuk menggunakan aplikasi anda sendiri, tampal satu pasangan `API ID:API Hash` ke dalam ID API. Untuk kunci kebenaran lengkap, pilih **Kunci Auth**, tampal semua 512 aksara heksadesimal, dan pilih ID DC yang disediakan. ID Pengguna adalah pilihan dan akan dicentang jika dimasukkan.
5. Lengkapkan kaedah log masuk yang anda pilih: telefon/kod/2FA, pengesahan daripada aplikasi Telegram yang telah log masuk untuk imbas QR, atau import sesi bertauliah yang disokong.
6. Semak ID akaun yang dipaparkan. **Sumber** Terbuka: sembang anda dimuat secara automatik; tambahkan kumpulan anda.
7. Di bawah **Pilih perubahan yang hendak disimpan**, pilih kategori acara atau pratetap **Mesej, suntingan & pemadaman**, kemudian simpan tetapan pemantauan.
8. Pilih tetapan lampiran secara berasingan, kemudian tekan **Mula pemerhatian**.

Kredensial API mengenal pasti aplikasi anda; ia tidak memberi kebenaran kepada akaun secara sendirinya. Kumpulan peribadi tidak memerlukan nama pengguna awam, tetapi akaun anda mesti mempunyai akses.

Untuk akaun sedia ada, lihat [format akaun dan sesi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/): panel menerima Telethon StringSession, Telethon/Pyrogram SQLite, TData ZIP akaun tunggal, dan JSON akaun yang disokong. Pilih sesi dan JSON pendampingnya bersama-sama, tekan **Hubungkan akaun**. Log masuk QR juga tersedia dengan tetapan API pilihan yang sama. TDLib, bot, dan senarai akaun pukal tidak disokong.

Untuk menambah akaun lain, tekan **+** di sebelah pemilih akaun atau buka **Akaun → Tetapan → Tetapan sambungan → Ruang kerja**, atau gunakan **Akaun**. Ruang kerja mempunyai sesi, jurnal, kunci, sumber dan barisan menunggu yang berasingan. Menukar paparan tidak menghentikan pengumpul lain yang sedang berjalan. Akaun Telegram yang sama tidak boleh ditugaskan kepada dua ruang kerja dalam pemasangan ini. Tiada bilangan ruang kerja yang tetap; ia berkongsi satu proses, jadi kapasiti bergantung pada mesin.

Token panel langsung melindungi akses ke kebenaran Telegram dan bahan yang disimpan; ia berasingan daripada kelayakan API Telegram. Hanya demo tempatan yang dimulakan secara eksplisit dan diakses secara langsung mendapat kemasukan automatik. Demo jauh/proksi masih menggunakan `data/demo/panel-token.txt`.

## Semak dan eksport

- **Jurnal:** cari dan tapis pemerhatian mengikut sumber dan jenis peristiwa.
- Pilih satu acara untuk menyemak rekod asal, atribusi dan versi yang disimpan.
- Butiran suntingan menunjukkan kandungan sebelum/selepas yang tersedia. Butiran pemadaman menunjukkan kandungan terakhir yang dirakam, jika ada; pelaku yang tidak diketahui kekal tidak diketahui.
- **Eksport:** ZIP ber tandatangan, JSONL, CSV dan HTML luar talian.
- **Eksport sembang penuh** (Sumber → Eksport sembang penuh): muat turun keseluruhan sejarah sembang yang boleh dilihat sebagai bundel yang ditandatangani dengan `chat.json` (gaya eksport Telegram) dan `chat.html` yang boleh dibaca. Sembang peribadi berfungsi apabila akaun adalah ahli. Ia adalah snapshot semasa, bukan pembinaan semula mesej yang telah dipadam atau disunting sebelum ini. Sahkan salinan dengan `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Simpan titik pemeriksaan:** letakkan sempadan jurnal yang ditandatangani di luar pengumpul.
- **Muat turun resit larian yang disahkan:** memelihara rekod program/versi pengumpul.
- **Sediakan permintaan cap masa:** sediakan permintaan luar talian kepada pihak berkuasa cap masa; ikuti [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/) untuk mendapatkan dan mengesahkan respons.
- **Sahkan jurnal:** periksa tandatangan peristiwa dan pautan rantaian. Eksport ZIP juga memeriksa media.

Pelayar yang disokong menyimpan eksport besar terus ke fail pilihan. Pelayar lain menyimpan dalam tompokan sehingga 128 MiB. Semasa pelayan sedang berjalan, CLI penstriman menyokong muat turun yang lebih besar tanpa menyimpan keseluruhan respons dalam tompokan:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Untuk ruang kerja lain, tambahkan `--profile ID` menggunakan **Eksport → ID Ruang Kerja**. Untuk pelayan jauh, tambahkan `--url https://your-server`. Had pemindahan lalai ialah 5 GiB; `--max-mib` mengubahnya. Kandungan ZIP yang disahkan mempunyai had pengesahan berasingan 4 GiB tanpa pemampatan secara lalai (**Parameters** menaikannya; sahkan arkib seperti ini dengan `verify.py --max-gib N`). Sahkan arkib tersebut menggunakan salinan verifier yang dipercayai dan cap jari/titik pemeriksaan kunci yang disimpan secara bebas.

## Semak pemasangan

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` memeriksa kebergantungan tempatan, sokongan penandatanganan, storan, konfigurasi kunci dan alamat pendengar. Ia tidak memasang apa-apa atau menyambung ke Telegram. Pelabuhan yang sibuk mungkin bermakna instans lain sedang berjalan. Gunakan `--port` yang berbeza atau hentikannya terlebih dahulu.

Pelancar memasang ke dalam `.venv`. Perintah tambahan `python -m tgwitness...` mesti menggunakan `.venv\Scripts\python.exe` pada Windows atau `.venv/bin/python` pada Linux/macOS, melainkan persekitaran tersebut sudah diaktifkan.

## Sesi, perlindungan dan operasi

`.session` yang tertutup dan konsisten boleh ditukar secara tempatan dengan `python -m tgwitness.sessions account.session --out account.tgwitness-session`, kemudian dimuatkan dalam Akaun. Import fail terus dan log masuk QR juga tersedia. Lihat [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/) untuk format log masuk, SOCKS5, HTTP CONNECT, MTProxy dan kunci induk luaran.

**Pause pemerhatian** menghentikan pengumpulan. **Mengunci** hanya menutup akses pelayar. Menutup tab membiarkan proses pengumpul terus berjalan. Menghentikan proses mengganggu pengumpulan; snapshot sejarah tidak dapat membina semula semua suntingan atau pemadaman yang terlepas. Lihat [bagaimana pengumpulan berfungsi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/) untuk dasar acara, barisan lampiran, penasingan akaun, dan tingkah laku permulaan semula.

Sesi dan rahsia disulitkan. Kandungan mesej, media dan eksport memerlukan cakera atau volum yang disulitkan. Tandatangan menetapkan integriti berbanding kunci yang dipercayai; ia tidak menetapkan asal Telegram atau menghalang pembohongan oleh operator yang mengawal pengumpul dan kuncinya.

Baca [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/operations/) untuk sandaran/pemulihan, [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/) untuk hosting, dan [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) untuk contoh perkhidmatan. Panel yang dipasang juga merangkumi panduan persediaan luar talian di `/guide.html`

Pengesahan sebenar dan had yang masih ada direkodkan dalam [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) dan [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
