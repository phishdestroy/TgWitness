# Siasat di semua sembang

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/cases/

Satu kes penuh merentas saluran, kumpulan, sembang peribadi dan bot: kumpul, hubungkan titik-titik, bina semula garis masa, serahkan.

Satu insiden rekaan, dari mula hingga akhir. Pengumpulan, carian dan profil orang menemui rekod, [Case Board](https://phishdestroy.github.io/TgWitness/ms/docs/case-board/) menyusunnya, [Report studio](https://phishdestroy.github.io/TgWitness/ms/docs/reports/) membentangkannya.

KES YANG DIKENDALIKAN / DESTINASI PEMBAYARAN YANG DIUBAH

### Satu insiden. Empat perbualan. Satu jejak untuk dibina semula.

Satu hantaran saluran menunjuk ke sebuah bot. Satu kumpulan bercakap tentang pautan pembayaran baharu dan bot memaparkannya. Hantaran itu disunting, sembang peribadi mengulangi pautan, satu mesej kumpulan hilang.

Siapa yang menyiarkan setiap versi?Di manakah pautan itu muncul?Fail mana yang telah dipelihara?Apa yang berubah, dan bila?

Memuat sejarah, AI, MCP, OCR dan webhook: [Mengusahakan arkib](https://phishdestroy.github.io/TgWitness/ms/docs/archive/).

## 1. Menetapkan liputan merentasi keseluruhan akaun

Skop seluruh akaun hanya pada akaun khusus. Akaun utama menggunakan sembang terpilih atau satu folder.

1. [Sambungkan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/accounts/) dalam ruang kerjanya sendiri. Catat rujukan kes, ID akaun, ruang kerja dan cap jari kunci.
2. **Sumber → Skop pemerhatian → Mod siasatan**: **Seluruh akaun**, keempat-empat jenis sumber, **Tindakan sendiri**. Setiap sembang baharu disimpan profilnya dan **200 mesej kelihatan** terakhir. **Simpan skop** dan sahkan.
3. **Muat sembang** dan bandingkan dengan senarai sembang akaun. Hadnya 1,000 dialog (sehingga 20,000 dalam **Parameter → Sembang yang dibaca daripada senarai akaun**); sembang melebihi had muncul apabila ia aktif.
4. **Tetapan Rakaman** → **Semua aktiviti kelihatan**, semak had lampiran dan ruang cakera. Mulakan, kemudian uji dengan satu mesej, satu suntingan dan satu pemadaman.

SaluranKumpulanPerbualan peribadiBot

SATU AKAUN / SATU KUNCI PENANDATANGAN**Semua aktiviti yang boleh dilihat oleh akaun terpilih → satu jurnal**

Mesej · suntingan · notis pemadaman · reaksi yang kelihatan · acara keahlian · tindakan sendiri

"Seluruh akaun" bermaksud setiap sembang yang boleh dibuka akaun ini, tolak pengecualian. Tiada sembang rahsia. Sembang baharu menyertai apabila muncul; sejarah lama tidak dimuat turun secara automatik.

## 2. Dapatkan sejarah dan memelihara fail

Buat koleksi Case Board dan tanda buku apa yang penting. Simpan daftar sumber: ID sembang, tajuk, akaun, peranan, permulaan tangkapan langsung, hasil sejarah, hasil media, jurang.

| Perlu | Tindakan dalam panel | Apa yang disediakan |
| --- | --- | --- |
| Sejarah merentas sembang yang diaktifkan | Sumber → Muat sejarah penuh | Mesej yang tersedia sebelum ini dimasukkan ke dalam jurnal ruang kerja, dengan henti/lanjutan dan laporan kemajuan yang ditandatangani. [Panduan sejarah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/). |
| Kontext sembang sedia ada dalam jurnal | Sumber → Tetapan rakaman → Gambar rajah sejarah | Mesej terkini sebagai rekod bertandatangan. 500 secara lalai, sehingga 10,000 dalam **Parameter → Snapshot sejarah terbesar**. |
| Sejarah lengkap yang kini boleh dilihat bagi satu sembang | Eksport sembang penuh → Eksport sembang penuh, atau Sembang → Eksport sembang | Berkas bertandatangan berasingan dengan `chat.json` dan `chat.html`, satu bagi setiap sembang. |
| Kontext apabila sembang baru muncul | Skop pemerhatian → Apabila sembang atau bot baru muncul | Profilnya dan sehingga 1,000 mesej terkini (200 dalam Mod siasatan). Tidak digunakan pada sembang sedia ada. |
| Bait lampiran | Muat turun lampiran yang boleh dilihat + had bagi setiap jenis | Cari `media.saved` dengan SHA-256 dan saiz. Dalam baris gilir, dilangkau atau gagal bermaksud tidak disimpan. |

Eksport sembang tidak masuk ke dalam jurnal atau profil orang. Untuk mencari sejarah lama di dalam TgWitness, gunakan **Muat Sejarah Penuh** atau snapshot.

Di sini: saluran, kumpulan, sembang bot dan sembang peribadi, serta fail invois dan hashnya. Apa yang dipadam sebelum tangkapan sudah hilang.

## 3. Kekalkan perbualan yang sedang berkembang dan tindakan anda sendiri

Biarkan ia berjalan. Bintangkan sembang panas sebagai keutamaan, laraskan semakan semula dalam **Tetapan Rakaman → Semakan Semula**, dan perhatikan `recheck.completed`, FloodWait dan hasil media.

**Sembang → Profil → Simpan profil sekarang** menyimpan penerangan sembang, arahan bot dan metadata lain.

**Mengikuti bot atau jemputan sebagai sebahagian daripada kes**

1. **Sembang → Buka pautan Telegram**, simpan pratonton dahulu. Pautan dan pratonton menjadi rekod bertandatangan.
2. Jika perlu, **Sertai / buka dan perhati** menyertai sembang atau memulakan bot dengan parameter mulanya.
3. Untuk mendokumentasikan tindakan, balas atau gunakan **Tekan butang** dari panel. Anda mendapat `interaction.requested` dan `interaction.result` bersama jawapan bot.

Ini tindakan sebenar. Butang yang ditekan dalam aplikasi lain tidak kelihatan, hanya balasan bot. Tiada aplikasi web, pembayaran atau telefon/lokasi.

## 4. Ikuti orang, pautan dan fail merentas sembang

1. **Jurnal**, **Semua sumber**, cari frasa, domain atau nama pengguna. Buka hasil dan hantar **Ke papan**.
2. **Sembang → Orang → Hidupkan profil**, pilih seseorang: sejarah nama, balasan, aktiviti, **Juga dalam…**, pautan, dompet, telefon. Buka rekod yang dipetik.
3. Ikuti ID pengguna berangka yang sama ke sembang lain. Nama, dompet atau avatar yang sepadan ialah petunjuk, bukan bukti.
4. Bandingkan hash fail. SHA-256 sama = bait sama. Siapa yang berkongsinya ialah soalan lain.

PETA KES / IKUT RUJUKANKes fiksyen · bukan graf langsung

SALURAN / PENGUMUMAN**Asal → destinasi yang disunting**

Merekod #101, #188 Mesej #84 · penghantar tidak dapat dikenal pasti

KELOMPOK / OPERASI**Pengguna 71001 menyiarkan pautan baru**

Rekod #146 · mesej #309 Resit fail yang disimpan #151

PERBINCANGAN BOT / PESANAN**Butang menunjuk ke destinasi tersebut**

Rekod #173 · mesej #12 Metadata butang yang dikembalikan

PERIBADI / SUSULAN**Pengguna 71001 mengulangi destinasi**

Rekod #205 · mesej #922 Resit fail yang disimpan #209

Empat perbualan menyumbang pemerhatian yang berbeza. Ikuti rekod sumber untuk setiap sambungan; kiriman saluran tidak mempunyai penghantar yang dikaitkan.

ID numerik dan rujukan rekod dicipta untuk panduan ini. Peta penjelasan ini menunjukkan cara menghubungkan hasil carian, profil dan rekod yang diperiksa; Case Board menyimpan kad yang sepadan dan rujukan sumber.

| Sambungan | Mendukung pemerhatian | Kesimpulan untuk disimpan |
| --- | --- | --- |
| Akaun Telegram yang sama | ID Pengguna 71001 dalam kumpulan #146 dan sembang peribadi #205 | ID pengirim yang sama dalam kedua-dua sembang. Siapa orang itu di dunia nyata ialah soalan lain. |
| Tujuan berulang | `pay.example.invalid/new` dalam #146, metadata butang #173, pos yang disunting #188 dan #205 | Pautan yang sama di empat tempat. Siapa yang mengawalnya memerlukan sumber lain. |
| Bait fail yang sama | Nilai SHA-256 penuh yang sama dalam resit media yang diselesaikan #151 dan #209 | Kedua-dua fail serupa bait demi bait. |

Profil hanya meliputi orang yang menulis sesuatu dalam *ruang kerja ini*, bukan senarai ahli. Petikan bagi setiap fakta: **Parameter → Rekod dipetik bagi setiap fakta**.

## 5. Rekonstrui urutan dan tandakan kekosongan

Versi dalam **Sembang**, kemudian **Jurnal** dengan **Semua sumber** + **Suntingan**, **Pemadaman**, **Liputan**. Masukkan kedua-dua masa dalam garis masa: tarikh Telegram dan bila ia diperhatikan.

1. 09:00 · #101**Pos saluran dirakam**

   Tujuan asal dikekalkan.
2. 09:12 · #146 / #151**Kumpulan memperkenalkan pautan yang berbeza**

   Pengguna 71001 menyiarkannya; muat turun lampiran selesai.
3. 09:16 · #173**Bot menunjukkan destinasi yang sama**

   Metadata papan kekunci yang disimpan membawa pautan.
4. 09:20 · #188**Perubahan pengumuman saluran**

   Pengamatan asal dan yang disunting kedua-duanya kekal.
5. 09:24 · #205 / #209**Susulan peribadi mengulanginya**

   Lampiran yang disimpan mempunyai SHA-256 penuh yang sama seperti #151.
6. 09:28 · #231**Notis pemadaman kumpulan tiba**

   Perhatian awal masih berkuat kuasa; tiada maklumat tentang penghapus atau masa pemadaman yang tepat disediakan.

Masa pemerhatian dan rujukan ilustratif. Rekod jurnal lain berlaku di antara entri ini.

Susunan jurnal ialah susunan ketibaan, tidak semestinya susunan kejadian. Asingkan rekod langsung, snapshot, mesej yang dipulihkan, pemadaman dan "tiada semasa semakan semula", dan tandakan setiap jurang sebagai tidak diketahui.

## 6. Melanjutkan kes ke akaun pengumpul lain

Satu ruang kerja bagi setiap akaun, langkah yang sama. Catat peranan dan cap jari masing-masing. Nombor mesej adalah mengikut akaun, jadi sentiasa nyatakan ruang kerja dan sembang mana.

[Kumpulan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/groups/) menunjukkan status, berkongsi tetapan dan mengeksport semua sekali gus, setiap satu dengan jurnal dan kuncinya sendiri. Garis masa merentas akaun anda bina dalam nota anda.

Kes panjang? Tambah [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/witness/), dan uji apa yang benar-benar ditangkap setiap akaun.

## 7. Sampaikan pakej kes yang boleh disemak

ZIP bertandatangan daripada setiap ruang kerja (sentiasa seluruh jurnal, penapis tidak berkesan), serta profil orang, eksport sembang dan fail.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Hantar cap jari secara berasingan. Sahkan semuanya terhadap ruang kerjanya sendiri:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan output pengesah, fail asal, liputan dan rekod pemindahan bersama dapatan anda. Tulis semuanya dalam Report studio. Jika penerima memerlukan kurang, buat [serahan diminimumkan](https://phishdestroy.github.io/TgWitness/ms/docs/handover/).
