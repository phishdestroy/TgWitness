# Eksport akaun

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/account-export/

Eksport apa yang boleh dibaca oleh akaun sekarang: skop, kerja yang boleh disambung semula, arkib yang ditandatangani dan salinan perkongsian yang dimimumkan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bukti dan pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

![Bukti & pengesahan](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

Eksport akaun menempah akaun itu secara eksklusif. Jedakan pemantauan atau pengumpulan lain secara nyata sebelum memulakan atau menyambung; aplikasi tidak pernah menghentikannya secara automatik.

Sebagai pentadbir pemasangan, pilih **Mula di sini → Eksport akaun saya**, atau **Eksport → Akaun Telegram → Konfigurasikan eksport akaun**. Log masuk jika perlu, semak skop, dan mulakan eksport secara eksplisit. Pemantauan berterusan tidak diperlukan. **Pemantauan yang disimpan** adalah eksport berasingan daripada jurnal sedia ada; jurnal tersebutZIP merangkumi semua sumber tanpa mengira penapis jurnal. Setiap ruang kerja mempunyai tugas, identiti tandatangan dan storan sendiri. Akses panel yang dikeluarkan, termasuk pemberian kuasa eksport biasa tanpa had, tidak dapat membuka laluan merentas akaun ini.

Penapis penghantar dan teks berkembang di bawah **Tapis mengikut penghantar atau teks mesej**. **Data akaun & kaedah sambungan** mengandungi kategori akaun pilihan dan pilihan Eksport/sesi biasa; ringkasannya memaparkan pilihan aktif walaupun ditutup. Menutup bahagian ini mengekalkan tetapan mereka. Draf eksport dan laporan kekal dalam sesi panel semasa semasa menukar pandangan; ia tidak disimpan melalui muat semula pelayar. Tugas sedia ada kekal boleh diakses daripada mana-mana pilihan eksport.

Aliran kerja ini mengeksport data yang kini boleh diakses oleh akaun yang disambungkan. Lalai menggunakan [Telegram Takeout](https://core.telegram.org/api/takeout); ia bukan sandaran data Telegram yang tidak tersedia atau telah dipadam. Perbualan Rahsia, sejarah yang tidak dapat diakses dan suntingan terdahulu tidak dipulihkan. Telegram boleh mengenakan tempoh menunggu sebelum Takeout bermula. Panel memaparkan tempoh menunggu itu; ia tidak menukar pengangkutan secara senyap. Pilihan API biasa secara eksplisit mempunyai liputan berbeza dan merekod kategori yang tidak disokong.

Takeout ialah API eksport rasmi yang juga digunakan oleh Telegram Desktop. TgWitness boleh menulis JSON yang serasi Desktop terus daripada pemerolehan sendiri; mengimport arkib orang lain tidak diperlukan. ID sembang dan mesej tersedia melalui kedua-dua pengangkutan. Sembang awam atau kebenaran untuk meneruskan tidak menjamin eksport yang lebih pantas atau menghapuskan kelewatan kelulusan Takeout. Ukur skop dan tetapan media yang sama sebelum membandingkan kelajuan.

Untuk sehingga 20 ID sembang yang dipilih secara eksplisit, eksport API biasa menyelesaikan rakan sebaya tersebut secara langsung sebelum mempertimbangkan inventori dialog lengkap akaun. Oleh itu, saluran awam yang boleh dibaca boleh dieksport tanpa menyertainya, walaupun ia tiada dalam senarai dialog. Rakan sebaya yang tidak di-cache akan kembali menggunakan inventori biasa. Penapis arkib kekal dikuatkuasakan: jika Telegram tidak mengembalikan dialog dan sembang yang diarkibkan dikecualikan, status arkib yang tidak diketahui akan direkodkan sebagai satu pengecualian. Takeout mengekalkan prosedur inventori julat-terpisahnya. Kedua-dua laluan tidak menggabungkan sembang atau mengubah kebenaran penghantaran semula. Dalam JSON serasi Desktop, saluran yang ditandakan oleh Telegram se`left` akan muncul di bawah `left_chats`, termasuk saluran awam yang boleh dibaca tetapi belum disertai oleh akaun tersebut.

Kedua-dua `FLOOD_WAIT` dan `FLOOD_PREMIUM_WAIT` menangguhkan permintaan untuk tempoh penuh yang diminta oleh pelayan. Tarikh akhir akaun dikekalkan semasa penyambungan semula dan permulaan semula; menunggu lebih singkat kemudian tidak dapat memendekkannya. Cubaan semula dihadkan, pembatalan mengekalkan halaman tersegel, dan kelayakan API tidak dirotax untuk memintas had kadar. Tiada pembelian Premium dibuat.

## Pilih apa yang dikumpul

| Persetelan | Maksud |
| --- | --- |
| Tujuan | Rakamkan mengapa pemerolehan ini diperlukan. Jangan masukkan nama yang tidak perlu atau butiran kes yang sensitif di sini. |
| Bahasa laporan | Pilih bahasa label laporan yang boleh dibaca. Teks mesej asal kekal tidak berubah; label templat yang tidak diterjemahkan menggunakan Bahasa Inggeris. Bahasa ditetapkan bersama pilihan kerja yang ditandatangani. |
| Jenis sembang / ID sembang | Semua jenis yang dipilih, atau hanya sembang yang disenaraikan; Mesej Disimpan milik sembang peribadi. Sembang yang diarkibkan boleh dipilih secara berasingan. |
| Tarikh | UTC. Tarikh kalendar From dan Through pada panel kedua-duanya disertakan. API menggunakan inklusif `from_utc` dan eksklusif `to_utc`; panel menghantar permulaan hari selepas Through. Batasan kosong membiarkan sisi itu tidak terhad. |
| ID Pengirim | Hanya mesej daripada penghantar yang disenaraikan; senarai kosong merangkumi semua penghantar. |
| Teks mengandungi | Frasa literal tanpa sensitiviti huruf besar-kecil, dipadankan dengan ATAU. Syarat penghantar/tarikh/mesej sendiri digabungkan dengan DAN. |
| Mesej sendiri | Hanya simpan mesej yang dihantar keluar. |
| Jenis media | Pilih kategori lampiran, atau nyahpilih semuanya untuk mengelakkan memuat turun fail mesej. |
| Had fail / had media keseluruhan | MiB bagi setiap fail dan jumlah GiB media yang dimuat turun. Teks, resit, laporan yang boleh dibaca dan overhead ZIP memerlukan ruang cakera tambahan. |
| Kategori akaun | Profil, kenalan, foto profil, cerita, metadata sesi dan data Takeout lain mempunyai kawalan berasingan. |

Preset **koleksi Minimize** menyahaktifkan metadata fail dan akaun. Penapis penghantar/kandungan digunakan sebelum halaman mesej yang disimpan dan muat turun media. Telegram masih menghantar halaman sejarah API yang mengandungi mesej yang diperlukan untuk menilai penapis tersebut: penapisan tidak menjamin mesej yang tidak dipilih tidak akan memasuki memori proses. Pemantauan berterusan lain dalam ruang kerja mempunyai skop dan tetapan penyimpanan sendiri.

Sejarah foto profil dan cerita tidak dipilih secara lalai. Matikan profil dan kenalan juga apabila kes hanya memerlukan mesej. Jika lampiran atau metadata tidak diperlukan, mengeluarkannya semasa pemerolehan mengelakkan penyimpanan satu lagi salinan peribadi dalam eksport ini.

Beban foto menggunakan varian imej pegun yang dikenal pasti dalam metadata dan manifes hash mereka, termasuk foto dengan varian avatar animasi. Animasi itu tidak menggantikan imej pegun yang dipilih. Beban yang lebih pendek atau lebih panjang daripada saiz yang diperhatikan direkodkan sebagai lampiran gagal, dan representasi yang diubah semasa pembaharuan rujukan fail ditolak. Kegagalan ini menjadikan arkib tidak lengkap sambil mengekalkan rekod mesej. Pengesahan bebas juga menolak lampiran yang disimpan yang panjang tandatanganannya bercanggah dengan saiz atau representasi yang diperhatikan, termasuk dalam arkib lama.

## Ringkasan, liputan dan pengesahan

Setiap tugasan membekukan opsinya dan identiti akaun. Inventori dan halaman yang dirakam ditandatangani; resit halaman merekodkan hash, penunjuk, masa, keputusan lampiran dan resit sebelumnya. Hanya halaman yang telah diserahkan akan menambah kemajuan. Mulakan semula/lanjutan memeriksa rekod tersebut sebelum meneruskan. Akaun yang diubah, halaman yang ditandatangani diubah atau rantaian resit yang tidak konsisten akan ditolak. Pilihan tidak boleh disunting di tengah-tengah pemerolehan: mulakan tugasan lain untuk skop lain.

Pause menghentikan operasi akaun yang sedang berjalan. Memulakan semula aplikasi meninggalkan kerja yang belum selesai tersedia untuk disambung semula secara eksplisit. Sesi Takeout yang tamat tempoh memerlukan sambungan semula secara eksplisit; menukar julat split Telegram mungkin memerlukan pengambilalihan baharu. Sambung semula mengekalkan pemerhatian sebelumnya, jadi eksport jangka panjang bukanlah satu snapshot atomik. Operasi lain yang mengubah akaun dan eksport yang bertembung dihalang semasa pengambilalihan. Tunggu pembungkusan selesai sebelum memadam ruang kerja.

Resume mengesahkan kandungan yang telah dirakam sebelum meneruskan. Arkib besar pada storan perlahan boleh melebihi had **tamat masa tindakan Panel → Parameter** yang dikonfigurasikan (120 saat secara lalai). Tingkatkan tetapan itu sebelum mencuba semula; pembatalan/gangguan storan akan menyebabkan kerja terhenti, dan pemeriksaan integriti yang gagal akan menghasilkan kerja gagal dengan penjelasan. Pengesahan mesti selesai atau berhenti dengan selamat sebelum failnya boleh ditutup. Tiada tuntutan throughput akaun besar telah disahkan oleh pemeriksaan sintetik.

Panel membezakan skop terpilih yang telah diselesaikan daripada arkib separa, dan merekod pengecualian serta bacaan yang gagal. Fail yang sengaja dikecualikan berbeza daripada fail yang gagal atau tidak tersedia. Periksa liputan walaupun pengesahan integriti berjaya. Tiada pembaca tempatan dapat membuktikan Telegram telah memulangkan setiap mesej yang pernah wujud.

ZIPyang telah selesai kekal tersedia untuk dimuat turun berulang kali dan melalui julatan HTTP. Arkib akaun mengandungi `manifest.json`, `manifest.sig`, ditandatangani `job.json`, `inventory.json`, `receipts/`, berkuasa `data/*.jsonl`, terpilih `media/`, HTML boleh dibaca dan pengesah. Pin cap jari pengumpul melalui saluran bebas, kemudian sahkan menggunakan pemasangan yang dipercayai:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Untuk arkib yang kandungannya yang diperluas melebihi 4 GiB, tetapkan nilai eksplisit yang mencukupi `--max-gib`Panel mengesahkan arkib tempatan yang disahkan dan lengkap menggunakan saiz pengembangan yang dinyatakan dan digest ZIP yang diterbitkan; CLI luaran mengekalkan had saiz bebasnya. Sahkan sebelum membuka HTML yang boleh dibaca. Pengesah terbina dalam arkib adalah mudah, tetapi pengesah yang diperoleh secara bebas mengelakkan mempercayai kod boleh laji yang disertakan bersama bukti.

Tandatangan Ed25519 dan hashes SHA-256 mengesan perubahan selepas pengumpul menyimpan bait yang berkaitan. Ia **tidak** membuktikan bahawa Telegram menandatangani mesej-mesej tersebut, bahawa pengendali pengumpul itu jujur, bahawa sejarah akaun itu lengkap, atau bahawa mahkamah akan menerima bahan tersebut. Masa tangkapan menggunakan jam pengumpul. Cap masa bebas dan asal usul pemerolehan bebas mesti dinilai secara berasingan.

## Sediakan pendedahan untuk peguam atau penerima lain

Selepas memuat turun eksport yang siap, simpan ZIP asal dan buka `index.html` daripada salinan yang diekstrak. Laporan ini menerangkan skop, liputan dan had yang tersedia. Rujukan rekodnya menggabungkan rujukan arkib, laluan dokumen dan nombor rekod, supaya penerima dapat mencari entri yang sama dalam HTML atau cetakan. Untuk contoh yang telah dibuat, [buka laporan rekaan](https://phishdestroy.github.io/TgWitness/demo/report/).

Daripada eksport akaun yang telah selesai, pilih **Sediakan salinan perkongsian**. Ini menghasilkan turunan berasingan yang ditandatangani. Sumber ZIP kekal tidak berubah dan peribadi; jangan hantar bersama turunan yang dimampatkan melainkan penerima dibenarkan menerima kandungannya sepenuhnya. Pilih bahasa laporan secara berasingan. Menukar bahasa atau sebarang tetapan pilihan memerlukan pratonton lain sebelum penciptaan.

1. Masukkan tujuan pendedahan dan pilih tarikh, ID penghantar dan kriteria teks literal.
2. Pilih sama ada untuk mengekalkan identiti, mendedahkan hanya peserta yang disenaraikan, atau pseodonimkan semua orang. Dalam mod pseodonim, ID/tajuk sembang dan ID mesej juga digantikan. Pseodonim kekal stabil dalam satu pendedahan dan berubah antara pendedahan yang disediakan secara berasingan.
3. Simpan teks mesej, hapuskan sepenuhnya, atau tambahkan nama/frasa literal untuk menyamarkan. Dalam mod peribadi, alat ini juga menyamarkan nama penghantar tersembunyi yang diketahui dan nama pengguna alternatif, ID penghantar token penuh, nama sembang langsung, pautan, alamat e-mel dan rentetan seperti nombor telefon. Padanan nama yang diketahui mengendalikan lipatan huruf Unicode, termasuk `Straße`/`STRASSE`. Tajuk kumpulan/saluran generik tidak dikeluarkan secara automatik daripada teks mesej. Jika had penyamaran identiti yang diketahui melebihi, sempitkan eksport sumber atau tinggalkan teks; alat ini enggan secara senyap melangkau nama-nama kemudian. Ini adalah peraturan usaha terbaik, bukan penganoniman umum.
4. Biarkan fail dikecualikan melainkan penerima memerlukannya. Fail asal yang disertakan mengekalkan piksel, audio, teks dan metadata mereka. Mereka **tidak** dianonimkan oleh alat ini.
5. Pratinjau kiraan, amaran dan contoh mesej yang diubah, kemudian sahkan penciptaan secara eksplisit. Contoh terhad kepada 12 mesej dan 2,000 aksara teks setiap satu. Ini adalah contoh, bukan ulasan penuh terhadap hasil. Menukar tetapan memerlukan pratonton lain. Pratonton tamat selepas 15 minit dan terikat kepada sesi pentadbir tersebut serta ZIP asal yang tepat; ia tidak boleh digunakan semula selepas dicipta. Pratonton baru membatalkan yang sebelumnya untuk tugasan dan sesi yang sama.
6. Periksa hasil yang lengkap `index.html` dan `messages.jsonl` secara tempatan sebelum menyerahkannya. Jika ia mendedahkan maklumat yang tidak perlu, buat pendedahan baru dengan pengecualian yang lebih ketat. Jangan sunting ZIP yang telah ditandatangani di tempatnya.

### Mesej yang ditinggalkan oleh pemilihan

**Rangka pratonton.** Pendedahan tidak kelihatan lengkap apabila ia tidak lengkap. Di dalam setiap sembang yang mengandungi sekurang-kurangnya satu mesej yang didedahkan, mesej yang tidak terpilih akan muncul sebagai penanda, `[withheld by selection — rule: sender]` (atau `text`, `period`). Pilih **Mesej yang terlepas daripada pilihan**: satu penanda bagi setiap siri mesej berturut-turut yang disembunyikan (lalai) atau satu bagi setiap mesej. Penanda hanya mengandungi peraturan dan kiraan, tidak pernah teks, penghantar, tarikh atau fail. Perbualan yang tiada pendedahan langsung akan diabaikan sepenuhnya, jadi pakej ini tidak mendedahkan kewujudannya.

Balasan yang didedahkan menyatakan apa yang dijawabnya: mesej yang disertakan dalam salinan ini, mesej yang disembunyikan oleh pemilihan, atau mesej yang tidak terdapat dalam eksport sumber (dihapuskan sebelum eksport atau tidak pernah dieksport; eksport tidak dapat membezakan yang mana). Mesej yang disembunyikan yang dijawab oleh balasan yang didedahkan sentiasa mendapat penanda tersendiri, jadi balasan itu merujuk kepada rekod yang menerangkan mengapa ia kosong. Ketiga-tiga keadaan ini berbeza daripada pemadaman dan jurang pengumpulan, yang tergolong dalam eksport sumber.

Dalam `messages.jsonl` (format `tgwitness-account-disclosure-v2`) setiap mesej mempunyai `state`: `disclosed`, atau `withheld` dengan `rules` dan `count`. Jawapan yang didedahkan mempunyai `reply_to` dengan sasaran `id` dan `state` (`disclosed`, `withheld`, `not_in_source`). Manifest mengira mesej yang didedahkan, sembang, media dan `withheld` mesej. `verify.py` menolak penanda yang membawa kandungan dan balasan yang merujuk kepada rekod yang hilang daripada pakej; pakej versi 1 disahkan seperti sebelum ini.

Format minimized mengabaikan profil akaun berstruktur, kenalan, avatar, sesi, cerita, objek Telegram mentah, tajuk penghantaran semula, petikan balasan, kad kenalan dan metadata lokasi. Ia mengecualikan fail JSONL asal, tetapan penapis peribadi, kunci pseudonim dan peta identiti. Teks terpilih, identiti yang disimpan secara eksplisit dan fail yang disertakan masih boleh mengandungi nama, ID atau frasa yang sama yang digunakan dalam penapis tersebut; ia memerlukan semakan berasingan. Dasar privasi dan kunci pseudonim disimpan dalam keadaan disulitkan di peti besi tempatan untuk tugasan tersebut; memadam tugasan tersebut akan memadam rekod pendedahan peribadi yang berkaitan dengannya. Rekod dasar awam menapis kiraan dan bukannya nilai penapisan. Tujuan yang dinyatakan adalah awam dalam manifes dan HTML: kriteria peribadi yang jelas dan, dalam mod pseudonim, identiti tersembunyi yang diketahui turut disamarkan di sana, termasuk apabila teks mesej diabaikan. Pastikan tujuan bebas daripada butiran peribadi yang tidak perlu; konteks pengecaman yang tidak diketahui boleh kekal.

Manifestnya mengikat fail derivatif, dasar awam dan hash asal ZIP. Pengesahan boleh menentukan integriti dan, jika sumber dibekalkan secara tempatan, pautan sumber yang sepadan:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Pautan sumber tidak membuktikan secara bebas bahawa transformasi telah memilih setiap item yang diperlukan atau menghapuskan setiap butiran pengenalan. Teks asal tidak disertakan sebagai bukti. Semakan semula diperlukan untuk membuat penilaian tersebut.

## Perkongsian dan tangkapan hos

Pilih mesej dan fail yang diperlukan oleh penerima, semak salinan perkongsian lengkap, dan simpan sumber secara berasingan. Rekodkan hash ZIP yang dihantar supaya penerima dapat mengenal pasti dan mengesahkan salinan tepat tersebut. Pseudonimisasi menggantikan pengecam terpilih; teks yang disertakan dan fail asal kekal sebagai sebahagian daripada semakan.

GitHub Actions menyokong eksport akaun penuh dan sembang terpilih melalui Takeout atau API biasa, serta jurnal peristiwa satu sembang. [Panduan tangkapan yang dihoskan](https://phishdestroy.github.io/TgWitness/docs/capture/) menerangkan pengesahan tetapan dan had 120 minit. Untuk mengesahkan salinan perkongsian yang diperoleh daripada tangkapan yang dihoskan, semak hash sumbernya dengan arkib asal dan sahkan pengesahan arkib tersebut dengan [pemeriksaan khusus mod](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope).

[Format bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/) · [Laporan kes](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/)
