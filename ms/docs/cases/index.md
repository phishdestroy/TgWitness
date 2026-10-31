# Siasat di semua sembang

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/cases/

Kerjakan keseluruhan kes merentasi saluran, kumpulan, sembang peribadi dan bot: kumpulkan, hubungkan, rekonstruksi dan serahkan bukti.

Panduan langkah demi langkah ini mengikuti satu insiden fiksyen sepenuhnya. Ia menggunakan ciri pengumpulan, carian, profil orang dan eksport sebenar. Peta kes adalah contoh dokumentasi; kesimpulan dan daftar kes anda diselenggara di luar aplikasi.

KES YANG DIKENDALIKAN / DESTINASI PEMBAYARAN YANG DIUBAH

### Satu insiden. Empat perbualan. Satu jejak untuk dibina semula.

Pengumuman saluran merujuk kepada bot. Kumpulan operasi membincangkan pautan pembayaran baru. Susulan peribadi mengulanginya. Kemudian, pengumuman itu disunting dan mesej kumpulan hilang.

Siapa yang menyiarkan setiap versi?Di manakah pautan itu muncul?Fail mana yang telah dipelihara?Apa yang berubah, dan bila?

Untuk memuatkan sejarah, semakan sumber AI pilihan, MCP, OCR dan webhook keluar, lihat [Work the archive](https://phishdestroy.github.io/TgWitness/ms/docs/archive/).

## 1. Menetapkan liputan merentasi keseluruhan akaun

1. [Sambungkan akaun pengumpulan](https://phishdestroy.github.io/TgWitness/ms/docs/accounts/) ke ruang kerja sendiri. Catatkan rujukan kes, ID akaun, nama ruang kerja dan cap jari kunci tandatangan dalam nota kes anda.
2. **Sumber** Terbuka **→ Skop Pengamatan → Mod Siasatan**. Semak **keseluruhan akaun**, keempat-empat jenis sumber dan **tindakan sendiri**. Preset ini membolehkan menyimpan profil sumber baru dan **200 mesej** teratas yang **boleh dilihat**. Tekan **Simpan skop** dan lengkapkan pengesahan skop.
3. Tekan **Muatkan sembang**. Bandingkan sumber dengan senarai dialog akaun dan pengecualian semakan. Di bawah **Parameter → Sembang yang dibaca daripada senarai akaun**, laras had senarai awal jika perlu: lalai ialah 1,000 dialog, boleh disesuaikan sehingga 20,000. Perbualan yang melebihi had akan dikesan apabila ia menjadi aktif.
4. Dalam **tetapan Rakaman**, pilih dan simpan **Semua aktiviti yang kelihatan**. Semak jenis lampiran, had saiz dan ruang cakera kosong. Mulakan pemerhatian dan sahkan mesej terkawal, suntingan dan pemadaman sebelum bergantung pada tetapan tersebut.

SaluranKumpulanPerbualan peribadiBot

SATU AKAUN / SATU KUNCI PENANDATANGAN**Semua aktiviti yang boleh dilihat oleh akaun terpilih → satu jurnal**

Mesej · suntingan · notis pemadaman · reaksi yang kelihatan · acara keahlian · tindakan sendiri

"Akaun keseluruhan" merangkumi sembang yang boleh diakses oleh akaun ini, dengan jenis sumber dan pengecualian yang dikonfigurasikan. Sembang rahsia tidak tersedia. Dialog baharu ditambah apabila kemas kini diterima; mengaktifkan mod ini tidak secara automatik memuat turun keseluruhan sejarah lama bagi setiap sembang sedia ada.

## 2. Dapatkan sejarah dan memelihara fail

Bina daftar sumber untuk keseluruhan siasatan. Berikan setiap sembang satu baris dengan ID numeriknya, tajuk, akaun, capaian/peranan, permulaan langsung, pemerolehan sejarah, hasil media dan jurang yang diketahui. Tandakan sumber sebagai diperoleh hanya selepas menyemak hasil yang berkaitan.

| Perlu | Tindakan dalam panel | Apa yang disediakan |
| --- | --- | --- |
| Sejarah merentas sembang yang diaktifkan | Sumber → Muat sejarah penuh | Utama semasa: mesej yang tersedia sebelum ini dimasukkan ke dalam jurnal ruang kerja, dengan henti/lanjutan dan laporan kemajuan yang disahkan. [Panduan sejarah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/history/). |
| Kontext sembang sedia ada dalam jurnal | Sumber → Tetapan rakaman → Gambar rajah sejarah | Mesej terkini yang kelihatan sebagai pemerhatian yang ditandatangani. Lalai maksimum 500; **Parameter → Snapshot sejarah terbesar** boleh meningkatkannya sehingga 10,000. |
| Sejarah lengkap yang kini boleh dilihat bagi satu sembang | Eksport sembang penuh → Eksport sembang penuh, atau Sembang → Eksport sembang | Bungkusan berasingan yang ditandatangani dengan `chat.json` dan `chat.html`. Ulang bagi setiap sumber; simpan keputusan kejayaan/kegagalan. |
| Kontext apabila sembang baru muncul | Skop pemerhatian → Apabila sembang atau bot baru muncul | Profil sumber dan sehingga 1,000 mesej terkini yang kelihatan; mod siasatan memilih 200. Perbualan sedia ada tidak menerima pengambilan ini secara retrospektif. |
| Bait lampiran | Muat turun lampiran yang boleh dilihat + had bagi setiap jenis | Semak `media.saved`, SHA-256 dan kiraan baitnya. Muat turun yang diletakkan dalam barisan, dilangkau atau gagal bukanlah fail yang terpelihara. |

Eksport sembang penuh adalah snapshot berasingan; ia tidak mengimport keseluruhan sejarahnya ke dalam jurnal atau profil orang. Gunakan **Muatkan sejarah penuh** merentas sumber yang diaktifkan, atau snapshot jurnal terhad, untuk bahan sejarah yang anda perlu cari dalam TgWitness. Semak senarai sumber sebelum memulakan pelaksanaan.

Dalam kes yang dikerjakan, peroleh saluran pengumuman, kumpulan operasi, perbualan bot dan susulan peribadi. Pelihara bait dan hash lampiran invois. Sejarah yang tersedia hari ini tidak dapat membina semula mesej yang dipadam sebelum tangkapan atau suntingan pertengahan yang tidak lagi dikembalikan oleh Telegram.

## 3. Kekalkan perbualan yang sedang berkembang dan tindakan anda sendiri

Teruskan pemantauan sepanjang kes berkembang. Tandakan sembang kes aktif sebagai sumber keutamaan; konfigurasi semakan semula keutamaan dan sumber lain di bawah **Tetapan Rakaman → Semakan Semula**. Semak semula `recheck.completed`, sambungan catch-up, FloodWait dan hasil media seiring kemajuan kerja.

Gunakan **Chats → Profile → Save profile now** untuk mengekalkan deskripsi sumber semasa, arahan bot dan metadata lain yang dikembalikan oleh Telegram. Profil sumber ini berasingan daripada profil orang yang dibina daripada mesej jurnal.

**Mengikuti bot atau jemputan sebagai sebahagian daripada kes**

1. Dalam **Chats → Buka pautan Telegram**, simpan pratonton terlebih dahulu. Pautan asal dan pratonton yang dikembalikan menjadi rekod yang disahkan.
2. Jika siasatan memerlukannya, **Join / Open dan perhatikan** sambungan atau pembukaan sumber dan mulakan bot dengan parameter permulaan yang disediakan. Permintaan sambungan yang belum diselesaikan kekal dalam rekod.
3. Untuk tindakan yang perlu didokumenkan, gunakan balasan teks panel atau kawalan **butang Tekan** yang disokong. Jurnal mengekalkan `interaction.requested` dan `interaction.result`, termasuk teks callback atau URL yang dikembalikan.

Kawalan ini melaksanakan tindakan Telegram sebenar. Callback yang ditekan dalam aplikasi Telegram lain tidak kelihatan kepada pengumpul; mesej atau suntingan seterusnya oleh bot mungkin kelihatan. Aplikasi web, pembayaran dan permintaan telefon/lokasi berada di luar mini-klien.

## 4. Ikuti orang, pautan dan fail merentas sembang

1. Buka **Jurnal**, biarkan penapis sumber pada **Semua sumber** dan cari frasa unik, domain, nama pengguna atau pengecam yang disimpan. Buka setiap rekod yang sepadan dan catat sembang, ID mesej dan nombor urutan jurnal.
2. Untuk sembang yang berkaitan, buka **Sembang → Orang → Hidupkan profil**, kemudian pilih seseorang. Semak sejarah nama/nama pengguna, hubungan balasan, aktiviti, **juga dalam…** sembang lain yang diperhatikan dan pautan yang diekstrak, dompet atau nombor telefon. Buka rekod jurnal yang dirujuk.
3. Ikuti ID pengguna Telegram bernombor yang sama ke dalam sembang lain dalam ruang kerja ini. Anggap nama yang sepadan, sebutan dompet atau avatar yang serupa sebagai petunjuk untuk disemak. Alamat yang disebut tidak menetapkan pemilikan; avatar yang serupa tidak menetapkan orang yang sama.
4. Bandingkan nilai SHA-256 lampiran yang dipelihara merentas rekod. Hashes yang sama menyokong identiti bait fail yang disimpan. Periksa rekod mesej dan penghantar yang berkaitan sebelum membuat kesimpulan tentang siapa yang berkongsi lampiran tersebut.

PETA KES / IKUT RUJUKANKes fiksyen · bukan graf langsung

SALURAN / PENGUMUMAN**Asal → destinasi yang disunting**

Merekod #101, #188 Mesej #84 · penghantar tidak dapat dikenal pasti

KELOMPOK / OPERASI**Pengguna 71001 menyiarkan pautan baru**

Rekod #146 · mesej #309 Resit fail yang disimpan #151

PERBINCANGAN BOT / PESANAN**Butang menunjuk ke destinasi tersebut**

Rekod #173 · mesej #12 Metadata butang yang dikembalikan

PERIBADI / SUSULAN**Pengguna 71001 mengulangi destinasi**

Rekod #205 · mesej #922 Resit fail yang disimpan #209

Empat perbualan menyumbang pemerhatian yang berbeza. Ikuti rekod sumber bagi setiap sambungan; jangan kaitkan kiriman saluran kepada pengguna 71001 tanpa penghantar yang disahkan.

ID numerik dan rujukan rekod dicipta untuk panduan ini. Peta ini menerangkan aliran kerja penganalisis menggunakan carian, profil dan pemeriksaan rekod; aplikasi ini tidak menjana graf penyiasatan global.

| Sambungan | Mendukung pemerhatian | Kesimpulan untuk disimpan |
| --- | --- | --- |
| Akaun Telegram yang sama | ID Pengguna 71001 dalam kumpulan #146 dan sembang peribadi #205 | ID penghantar yang sama disediakan dan dipaparkan dalam kedua-dua sembang. Identiti sebenar kekal sebagai persoalan berasingan. |
| Tujuan berulang | `pay.example.invalid/new` dalam #146, metadata butang #173, pos yang disunting #188 dan #205 | Tujuan yang sama muncul dalam empat konteks yang diperhatikan. Ini sahaja tidak membuktikan siapa yang mengawalnya. |
| Bait fail yang sama | Nilai SHA-256 penuh yang sama dalam resit media yang diselesaikan #151 dan #209 | Kedua-dua lampiran yang disimpan adalah identik dari segi bait. Nama fail atau miniatur sahaja tidak dapat mengesahkannya. |

Profil orang merangkumi penulis dengan mesej yang disimpan dalam sembang tersebut dan mengaitkannya dengan sembang lain dalam *jurnal ruang kerja* yang *sama*. Ia bukan direktori keahlian yang lengkap. Hashes avatar datang daripada cache tempatan yang berasingan; petikan profil mempunyai had yang boleh dikonfigurasikan di bawah **Parameter → Rekod yang dicita per fakta**.

## 5. Rekonstrui urutan dan tandakan kekosongan

Dalam Chats, periksa versi yang disimpan dan pautan rekod Jurnal #… Mereka dalam Jurnal, gunakan Semua sumber serta Suntingan, Pemadaman dan Liputan. Bina garis masa kes dengan tarikh Telegram yang disediakan dan masa pemerhatian pengumpul.

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

Susunan urutan jurnal menyusun mengikut urutan penerimaan, bukan semestinya tindakan asal Telegram. Sisipan sejarah lama boleh tiba selepas mesej langsung yang lebih baru. Pastikan pemerhatian langsung, snapshot, mesej yang dipulihkan, notis pemadaman dan "hilang semasa semakan semula" dipisahkan. Tambahkan selang masa tidak diketahui secara eksplisit di mana-mana liputan menunjukkan jurang; snapshot kemudian tidak menghapuskan jurang tersebut.

## 6. Melanjutkan kes ke akaun pengumpul lain

Tambah ruang kerja untuk setiap akaun berasingan dan ulangi inventori skop dan sejarah. Rekodkan keahlian/peranan dan cap jari kunci tandatangan untuk setiap satu. Pastikan pengecam diklasifikasikan mengikut ruang kerja dan sembang: nombor mesej yang sama bukan pengecam merentas akaun secara global.

Bandingkan pemerhatian berkaitan dalam nota kes atau alat analisis anda, sambil mengekalkan rujukan akaun dan jurnal bagi setiap baris. TgWitness pada masa ini tidak menyediakan carian global, garis masa gabungan, graf orang atau arkib kes merentas ruang kerja. Eksport penuh berbilang akaun bagi satu saluran atau superkumpulan adalah ciri berasingan; ia bukan penggabungan semua jurnal akaun.

Semasa kerja yang lebih panjang, tambahkan [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/witness/) untuk mengekalkan sempadan awal. Gunakan pilot penghantaran terkawal untuk menentukan laluan tangkapan dan keterlihatan akaun.

## 7. Sampaikan pakej kes lengkap yang boleh disemak

Eksport fail ZIP jurnal yang ditandatangani dari setiap ruang kerja. Ia mengandungi keseluruhan jurnal yang dirakam tanpa mengira penapis carian panel. Eksport profil orang yang berkaitan secara berasingan, simpan setiap bundel sejarah sembang penuh, dan pelihara bukti lampiran yang lengkap.

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

Simpan cap jari yang dipercayai melalui saluran berasingan. Daripada pemasangan yang dipercayai, sahkan setiap artifak terhadap identiti ruang kerja masing-masing:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Semak keputusan pengesah sebenar, pelihara bahan asal, dan simpan laporan liputan, kegagalan pemerolehan dan rekod pemindahan bersama penemuan anda. Folder kes peringkat tertinggi dan kesimpulan penganalisis disusun secara luaran; artifak TgWitness individu membawa tandatangan mereka sendiri.

## Gunakan kaedah yang sama untuk siasatan lain

**Pertikaian pesanan atau pembayaran yang dikendalikan oleh bot**

**Soalan:** apa yang dijanjikan oleh bot, destinasi butang mana yang dibekalkan, dan apa yang berubah selepas itu?

**Jejak:** kiriman kemasukan saluran → pratonton pautan bot yang disimpan → parameter permulaan bot → versi mesej dan papan kekunci → sebarang resit callback yang dikeluarkan oleh panel → susulan kumpulan/peribadi. Padankan setiap destinasi dengan rekod sumbernya; simpan deskripsi profil dan media yang diselesaikan.

**Sampaikan:** garis masa tawaran dan respons yang diperhatikan, rujukan sumber dan eksport yang disahkan. Pautan pembayaran yang dipaparkan bukan bukti bahawa pembayaran telah berlaku.

**Mesej yang dipadam selepas insiden merentas sembang**

**Soalan:** apa yang telah diperhatikan sebelum mesej berkaitan hilang?

**Jejak:** semua sembang terjejas → mesej asal → suntingan dihantar → notis pemadaman atau keputusan tiada pada semakan semula kemudian → lampiran yang disimpan → liputan sekitar insiden. Bandingkan pemerhatian akaun bebas dengan keterlihatan yang dinyatakan.

**Hantar:** satu urutan versi yang disimpan dan selang masa tidak diketahui secara eksplisit. Jangan jadikan mesej sejarah yang tiada bukti bahawa seseorang tertentu memadamnya.

**Seorang peserta menukar nama di beberapa sembang**

**Soalan:** aktiviti mana yang diperhatikan milik akaun Telegram yang sama walaupun nama berubah?

**Jejak:** ID penghantar numerik → sejarah nama/nama pengguna yang disimpan → balasan → sembang lain dalam ruang kerja → destinasi yang disebut dan fail yang disimpan. Semak rekod sumber untuk setiap sambungan yang didakwa; pisahkan akaun serupa.

**Sampaikan:** garis masa aktiviti akaun yang dirujuk dan hipotesis berasingan mengenai hubungan. Keserupaan nama dan pHash avatar adalah petunjuk, bukan bukti identiti.
