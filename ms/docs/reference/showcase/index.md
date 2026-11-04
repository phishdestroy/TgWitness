# Paparan awam

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/showcase/

Menerbitkan mesej yang disimpan daripada saluran awam terpilih dan snapshot yang ditandatangani melalui pautan yang akan tamat tempoh dan boleh ditarik balik.

**Akses → Pameran Awam** mencipta halaman berasingan yang hanya untuk dibaca menggunakan sistem token-akses sedia ada. Ia membaca pemerhatian yang disimpan oleh pemasangan. Ia tidak memulakan pengumpul, log masuk ke Telegram atau mendapatkan saluran untuk pelawat.

## Terbitkan halaman

1. Simpan profil sumber untuk setiap saluran awam yang anda ingin tunjukkan. Saluran mesti mempunyai nama pengguna awam dalam profil simpanan terbarunya; kumpulan dan sembang peribadi tidak layak.
2. Buka **Akses → Paparan awam** (atau `/showcase-manage.html`) sebagai pentadbir.
3. Pilih saluran merentasi sehingga 16 ruang kerja, masukkan tajuk halaman awam, dan pilih jangka hayat pautan selama 1, 7 atau 30 hari. Label ruang kerja dalaman tidak diterbitkan. Sehingga 64 saluran boleh disertakan.
4. Semak teks saluran terpilih untuk penerbitan, kemudian klik **Pratonton rekod terpilih**. Pratonton menggunakan projeksi sisi pelayan yang sama seperti halaman pelawat.
5. Klik **pautan 'Create showcase**'. Salin pautan tersebut semasa ia kelihatan. Buka pautan itu dalam pelayar berasingan untuk menyemak halaman penerima sebelum mengedarkannya.

Pautan mengandungi token akses dalam fragmen URLnya. Halaman tersebut membuang fragmen tersebut sebelum membuat permintaan API dan menukarnya dengan sesi pelayar. Sesiapa yang memiliki pautan boleh membuka bahan terpilih sehingga tamat tempoh atau pembatalan. Pautan baharu membenarkan 100 sesi serentak, setiap satu berlangsung paling lama satu jam. Kawalan Akses sedia ada juga boleh menguatkuasakan sekatan alamat dan had log masuk melalui API pemberian. Akses penilai biasa adalah mod yang berbeza dan masih merangkumi mesej dan fail asal yang dibenarkan.

## Apa yang dilihat pelawat

| Tersedia | Disimpan secara peribadi |
| --- | --- |
| Tajuk saluran awam terpilih, nama pengguna dan tarikh pemerhatian profil | Identiti akaun, label ruang kerja dalaman dan sumber yang tidak dipilih |
| Teks yang dirakam dan setiap suntingan yang disimpan | ID penghantar berstruktur, nama, nama pengguna, nombor telefon dan nilai profil |
| Perhatian pemadaman dengan teks yang disimpan sebelum ini, jika tersedia | Lampiran, avatar, miniatur, nama fail dan muatan asal |
| Penanda yang menunjukkan bahawa penulis/profil atau lampiran telah direkodkan | Méta data penghantaran dan balasan, laluan rangkaian, alamat IP dan kelayakan |
| Bilangan peristiwa saluran terpilih, suis pengumpulan semasa, rentak degupan dan selang pemeriksaan | Kawalan pengumpulan dan API eksport bukti biasa |
| Cap jari tandatangan, titik pemeriksaan jurnal dan bukti keserasian | Kunci penandatanganan dan sesi Telegram |

**Teks mesej awam tidak dianonimkan secara automatik.** Nama, sebutan, nombor telefon atau pautan yang ditulis dalam mesej kekal sebagai sebahagian daripada teks tersebut. `Redacted`terpakai pada medan pengarang/profil berstruktur. Semak kandungan yang dipilih sebelum menerbitkannya, termasuk suntingan dan pemadaman yang disimpan.

Kelayakan mencerminkan **profil sumber terkini yang disimpan**, bukan carian Telegram secara langsung. Jika profil seterusnya tidak lagi mempunyai nama pengguna saluran awam, permintaan baharu mengecualikan saluran tersebut. Kemaskini profil sumber apabila keterlihatan awam berubah. Pembaca mungkin sudah menyimpan bahan yang mereka terima sebelum ini.

Rekod asal yang ditandatangani kekal tidak berubah. Projeksian yang dipaparkan ditandatangani secara berasingan dan membawa hash yang merujuk kepada rekod asalnya. Tandatangan projeksian mengesahkan kenyataan yang dipaparkan; ia bukan tandatangan peristiwa asal ke atas bait yang disembunyikan.

## Semak tandatangan dan kesinambungan

Perluas **Cap Jari & checkpoint yang disahkan** dan muat turun snapshot. Selepas halaman dikemas kini, muat turun merangkumi snapshot pelayar sebelumnya dan bukti konsistensi Merkle antara sempadan jurnal mereka. Pemutakhiran automatik berlaku setiap minit selagi halaman dipaparkan dan memaparkan halaman pertama pemerhatian.

Dengan pemasangan TgWitness, sahkan fail yang dimuat turun secara luar talian:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

Cap jari mesti berasal daripada rujukan yang dipercayai secara berasingan. Untuk membandingkan dengan snapshot yang anda simpan sendiri, gunakan `--previous earlier.json`; ini menimpa snapshot sebelumnya yang dibawa dalam muat turun. Bukti semasa mesti bermula pada sempadan yang disimpan itu. Klien yang disahkan boleh meminta bukti itu menggunakan `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Jurnal yang lebih pendek akan mengembalikan HTTP 409 bukannya menetapkan semula sempadan secara senyap.

Titik pemeriksaan yang disahkan merakamkan **keseluruhan jurnal pengumpul**, termasuk jumlah rekod dan hash kepala yang tidak telus. Jumlah mesej yang dipaparkan hanya terpakai kepada saluran awam yang dipilih. Halaman ini tidak pernah menyenaraikan kandungan jurnal lain. Ini adalah kiraan peristiwa, bukan kiraan mesej unik. Tetapan menerangkan konfigurasi semasa, bukan setiap selang rakaman sebelum ini.

Pengesahan tandatangan dan konsistensi boleh mengesan perubahan berbanding sempadan yang disimpan. Ia tidak mengira semula pengira tandatangan secara bebas, mengesahkan asal Telegram, menunjukkan tangkapan tanpa gangguan, atau menggantikan saksi bebas. Untuk semakan tersebut, gunakan [pengesah bukti](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/) dan [rekod skala diuji](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/). Pemasangan sintetik dilabelkan secara jelas sebagai sintetik.

## Batal atau hos halaman

Gunakan **Revoke** dalam pengurus paparan atau bahagian **Akses** sedia ada untuk menutup pautan dan menamatkan semua sesi. Pelawat memadam rekod yang dipaparkan apabila permintaan mengesan bahawa akses telah tamat. Tamat tempoh dan kebenaran disemak pada setiap permintaan. Pemberian paparan tidak boleh ditukar kepada akses panel biasa di tempat; buat pemberian baharu untuk menukar mod.

Hidangkan halaman melalui alamat HTTPS sedia ada pada pemasangan. Menerbitkan pautan tidak membuka port baru, mewujudkan terowong atau menukar DNS. HTML dan API kekal pada pemasangan pengguna. Pelawat paparan tidak boleh menggunakan API biasa untuk mesej, profil, media, eksport atau pengurusan dengan capaian ini.
