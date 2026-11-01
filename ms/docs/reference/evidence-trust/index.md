# Bukti dan kepercayaan

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence-trust/

Apa yang boleh disahkan oleh eksport, video, arkib web dan rekod yang disahkan, dan bagaimana peranti pengumpul mempengaruhi kebolehpercayaan mereka.

Eksport, tangkapan skrin atau rakaman boleh menjadi bukti yang berguna. Kebolehpercayaannya bergantung kepada cara ia dikumpul, dipelihara dan disahkan. **Hah atau tandatangan yang sah memeriksa bahan yang disimpan; ia tidak mengesahkan secara bebas bahawa peranti pengumpul telah menerima kandungan sumber yang benar.** Had ini juga terpakai kepada TgWitness.

Panduan ini memisahkan pengesahan teknikal daripada penilaian undang-undang. Dokumentasi produk dan peruntukan undang-undang di bawah telah disemak pada 1 November 2026; perbandingan Hunchly menerangkan dokumentasi terbitannya, bukan audit produk baharu.

## Di mana kepercayaan terlibat dalam tangkapan

Diyagram aliran · Akaun Telegram dan perkhidmatan → Klien, pelayar dan sistem pengendalian; Klien, pelayar dan sistem pengendalian → Eksport, tangkapan video atau tangkapan halaman; Eksport, tangkapan video atau tangkapan halaman → Hash dan tandatangan pengumpul; Hash dan tandatangan pengumpul → Hash yang disimpan oleh pihak bebas · Akaun Telegram danperkhidmatan · Klien, pelayar dansistem pengendalian · Eksport, tangkapanvideo atau tangkapanhalaman · Hash dan tandatanganpengumpul · Hash yang disimpanoleh pihak bebas

**Diagram sebagai teks**

1. Akaun Telegram dan perkhidmatan → Klien, pelayar dan sistem pengendalian
2. Klien, pelayar dan sistem pengendalian → Eksport, tangkapan video atau tangkapan halaman
3. Eksport, tangkapan video atau tangkapan halaman → Hash dan tandatangan pengumpul
4. Hash dan tandatangan pengumpul → Hash yang disimpan oleh pihak bebas

Model ancaman di sini menganggap bahawa penyerang atau pengendali boleh mengubah persekitaran pengumpulan sebelum bukti direkodkan. Ini adalah analisis bersyarat, bukan dakwaan bahawa peranti atau produk tertentu telah dikompromi.

Klien rasmi dan sambungan yang disulitkan membantu melindungi penggunaan biasa. Ia tidak menjadikan sistem operasi, pelayar atau paparan persekitarannya boleh dipercayai secara berasingan. Jika kandungan digantikan selepas penyahsulitan tetapi sebelum dirakam, pengeksport boleh menyimpannya dengan tepat dan penandatangan boleh menandatangannya dengan betul. Tiada satu pun operasi ini memerlukan algoritma hash yang rosak atau tandatangan palsu.

Sebuah video yang dirakam menggunakan peranti yang sama boleh merakam persembahan pengganti yang sama. Sebuah kamera berasingan boleh mengesahkan apa yang dipaparkan pada skrin, tetapi skrin itu sendiri tidak mengesahkan apa yang dibekalkan oleh Telegram. Begitu juga, HTML, JSON, tangkapan skrin dan log pelayar yang sepadan daripada satu persekitaran terkawal mungkin mengalami kegagalan yang sama. Persetujuan mereka adalah konteks yang berguna; ia bukan pengesahan bebas secara automatik.

## Apa yang disumbangkan oleh setiap bentuk bukti

| Bahan | Sumbangan berguna | Soalan yang tinggal |
| --- | --- | --- |
| Eksport Telegram Desktop | Perbualan yang boleh dibaca atau dibaca oleh mesin dan media terpilih | Siapa yang mengawal fail klien dan eksport, dan apa yang tersedia atau dikecualikan? |
| Skrinshot atau rakaman skrin | Kontext yang dapat dilihat, urutan tindakan dan penyampaian | Adakah pembentangan mencerminkan sumber dengan setia, dan apa yang berlaku di luar rakaman? |
| Arkib web tempatan, termasuk MHTML | Kandungan halaman dan sumber berkaitan untuk pemeriksaan kemudian | Apakah yang dibekalkan oleh pelayar kepada pengarkib, dan siapa yang mengawal pelayar itu? |
| Arkib yang ditandatangani oleh pengumpul | Perubahan pada bait yang ditandatangani boleh dikesan berbanding kunci yang dipercayai dan rujukan yang disimpan | Siapa yang mengawal kunci penandatanganan dan input sebelum menandatangani? |
| Pemeriksa titik pemeriksaan atau cap masa yang disahkan secara bebas | Satu hash atau titik pemeriksaan yang disimpan untuk dibandingkan dengan penghantaran kemudian | Byte dan sempadan mana yang dilindungi, dan apa sebenarnya yang disahkan oleh pihak bebas? |

Telegram mendokumenkan eksport Desktopnya sebagai salinan HTML/JSON luar talian dan API Takeoutnya sebagai cara untuk mendapatkan semula data akaun terpilih. Keterangan ini tidak menyediakan tandatangan Telegram ke atas arkib eksport akhir untuk disahkan oleh penerima. Kesimpulan kami terhad kepada mekanisme eksport yang didokumenkan tersebut; ia bukan satu dakwaan bahawa bukti Telegram tidak mempunyai nilai undang-undang. [Eksport Telegram Desktop](https://telegram.org/blog/export-and-more),[API Takeout](https://core.telegram.org/api/takeout).

Perbezaan yang sama terpakai kepada permintaan latar belakang, entri cache dan log rangkaian. Mereka mungkin mendedahkan ketidakseragaman dan membantu mengesahkan satu pengumpulan. Kerumitan mereka sahaja tidak menentukan siapa yang menghasilkannya. Satu arkib yang diurus secara bebas atau rekod perkhidmatan yang diperoleh secara berasingan memperkenalkan sumber yang berbeza untuk dibandingkan, tertakluk kepada had pengumpulan dan pemilikan tersendiri.

## Hunchly menggambarkan sempadan yang sama

Dokumentasi Hunchly menerangkan penghasian SHA-256 bagi tangkapan MHTML, foto dan lampiran, dengan pengesahan hasih bebas. Ia juga menerangkan mengapa fail yang diubah suai yang disertakan dengan hasih yang dikira semula boleh lulus perbandingan itu, dan menunjukkan tandatangan serta pengesahan sumber sebagai semakan tambahan. [Hunchly: penghasian kandungan, foto dan lampiran](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

*Panduan Bukti* terbitannya, semakan 1.0 bertarikh 17 Oktober 2018, menerangkan kunci GPG yang dijana secara tempatan dan tandatangan untuk tangkapan MHTML. Ia secara eksplisit mengenal pasti akses kepada kunci peribadi tempatan sebagai cara untuk menandatangani semula bahan yang diubah suai. Ini adalah had kepercayaan yang didokumenkan, bukan bukti eksploitasi semasa yang tidak didedahkan. Panduan itu juga menyatakan Chrome melaksanakan tangkapan MHTML. Menggambarkan Hunchly hanya bergantung pada reputasi penyiasat akan mengabaikan kawalan teknikal ini.[Panduan Bukti Hunchly, seksyen 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

Sama ada bahan yang dikumpul dengan produk tertentu telah diterima dalam sesuatu kes memerlukan keputusan dan keadaan yang relevan. Kami tidak membuat sebarang dakwaan di sini mengenai kekerapan mahkamah menerima Hunchly atau TgWitness, atau mengenai mana-mana produk tersebut mempunyai kelulusan mahkamah secara am.

## Apa yang ditambah oleh TgWitness, dan di mana perlindunganannya berakhir

TgWitness merekod pemerhatian dalam jurnal yang ditandatangani dan dipautkan serta menyediakan eksport yang boleh disemak oleh penerima. Titik pemeriksaan yang disimpan, cap masa dan saksi berasingan memberikan rujukan kepada pemeriksa melangkaui fail semasa pengumpul. Mereka membantu mendedahkan perubahan pada rekod yang telah disahkan sebelum ini. Rekod liputan dan hasil pengumpulan yang nyata membantu menerangkan apa yang telah dan tidak dirakam.[Format bukti dan penyerahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/), [skop pengumpulan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/collection/).

Masa penggantian yang mungkin berlaku adalah penting:

1. **Selepas menandatangani, tanpa akses kepada kunci penandatanganan:** mengubah rekod yang ditandatangani atau fail yang diikat pada manifesto akan menyebabkan pengesahan gagal dengan pengesah dan kunci yang dipercayai.
2. **Dengan kunci pengumpul, selepas titik pemeriksaan bebas disimpan:** jurnal pengganti boleh mempunyai tandatangan baru yang sah, tetapi pratanda yang berubah akan gagal dalam perbandingan dengan titik pemeriksaan terdahulu itu. Titik pemeriksaan yang disimpan hanya pada peranti terkawal yang sama boleh digantikan bersama jurnal tersebut. Rekod di luar sempadan yang disimpan memerlukan liputan mereka sendiri.
3. **Sebelum satu titik pemeriksaan yang merangkumi pemerhatian disimpan secara bebas:** masukan palsu boleh ditandatangani dan dipatahkan dengan jayanya, termasuk rekod baharu yang disambungkan selepas satu titik pemeriksaan terdahulu. Titik pemeriksaan atau cap masa yang terhasil masih merangkumi rekod palsu tersebut; ia tidak membuktikan kebenarannya.

Saksi TgWitness menerima checkpoint ber tandatangan pengumpul; ia tidak membaca secara bebas perbualan Telegram yang mendasari. Kuncinya dan rekod yang disimpannya mesti dipercayai secara berasingan. Apabila keseluruhan jurnal yang dihantar perlu disaksikan, gunakan[prosedur penyerahan yang memerlukan sempadan eksport akhir](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#require-a-witnessed-export-boundary). Pas integriti biasa masih boleh melaporkan ekor yang tidak disaksikan.

Respon RFC 3161 yang disahkan boleh menyokong bahawa satu checkpoint wujud pada masa yang dinyatakan oleh pihak berkuasa. Ia tidak menetapkan bila mesej Telegram dihantar atau sama ada kandungannya benar. Permintaan yang disediakan atau fail respons yang disertakan sahaja tidak mencukupi. Apabila mengesahkan eksport dengan `tgwitness.verify`, memeriksa tandatangan TSA yang disertakan memerlukan CA yang dipercayai secara eksplisit melalui `--tsa-ca`. Resit OpenTimestamps memerlukan `ots verify` bebas, dengan peningkatan bukti di mana perlu. [Prosedur cop masa](https://phishdestroy.github.io/TgWitness/ms/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

Dalam [tangkapan GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), pelaksana hos sementara mengumpul mesej-mesej tersebut. Pengesahan mengikat arkib kepada aliran kerja yang diluluskan. Mod ini masih mempercayai GitHub, perisian dan kebergantungan yang diluluskan, pembantu/pelayar dan terowong. Ia bukan perkakasan sulit, tandatangan Telegram, atau bukti bahawa tiada siapa mengakses hos. Resit pelaksanaan tandatangan tempatan juga merupakan ukuran yang dilaporkan sendiri, bukan pengesahan perkakasan.

## Berat undang-undang bergantung pada asasnya

Empat persoalan harus kekal berasingan: sama ada item itu benar-benar seperti yang didakwa, sama ada bait yang dihantar sepadan dengan rekod yang disimpan, sama ada kandungan menyokong fakta yang didakwa, dan sama ada peraturan yang berkenaan membenarkan penggunaannya. Semakan kriptografi hanya menangani sebahagian daripada asas tersebut.

Dalam prosiding persekutuan AS, Peraturan 901 menyediakan cara untuk mengesahkan bukti, termasuk keterangan saksi yang berpengetahuan dan bukti mengenai sesuatu proses atau sistem. Peraturan 902(13) dan 902(14) menyediakan laluan pensijilan untuk rekod elektronik dan salinan tertentu, dengan keperluan prosedur. Nota jawatankuasa membezakan pengesahan daripada isu seperti keterangan tidak langsung, kaitan dan pengesahan pengarang. Tandatangan perisian sahaja bukan merupakan pensijilan orang berkelayakan yang diterangkan di situ. [Peraturan Bukti Persekutuan 901](https://www.law.cornell.edu/rules/fre/rule_901), [Peraturan Bukti Persekutuan 902](https://www.law.cornell.edu/rules/fre/rule_902).

Di mana Akta Bukti Kanada terpakai, seksyen 31.1 membincangkan pengesahan dokumen elektronik. Seksyen 31.2 menghubungkan peraturan bukti terbaik dengan integriti sistem atau andaian yang berkenaan; seksyen 31.3 menyatakan keadaan bagi andaian integriti. Ini adalah syarat bukti yang ditakrifkan, bukan andaian menyeluruh bahawa mana-mana penyiasat berlesen atau produk komersial adalah tidak boleh silap. [Akta Bukti Kanada, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Contoh-contoh ini tidak menentukan kebolehterimaan di bidang kuasa lain atau dalam kes tertentu. Semakan teknikal hendaklah digunakan secara konsisten terhadap bahan yang menyokong atau mencabar suatu dakwaan. Panduan ini tidak membuat sebarang dakwaan bahawa bukti pendakwaan secara amnya lebih mudah diterima berbanding bukti pembelaan.

## Sediakan rekod yang boleh dinilai oleh orang lain

- Terangkan akaun, peranti pengumpulan, pengendali, versi perisian, hak akses, skop terpilih dan tempoh pengumpulan. Rekodkan gangguan dan kemungkinan pelanggaran keselamatan, bukannya menganggap pemeriksaan tandatangan yang berjaya sebagai ujian peranti yang bersih.
- Simpan pakej asal dan rekod pemindahan, hash dan sumber masa. Simpan cap jari kunci dan titik pemeriksaan melalui saluran dipercayai berasingan. Semak saksi sebenar atau liputan cop masa sebelum menerangkannya dalam laporan.
- Carilah pengesahan bebas yang sesuai dengan tuntutan: rekod peserta lain, tangkapan bebas atau rekod perkhidmatan yang diperoleh secara sah. Terangkan kebebasan dan keterbatasan mereka; persetujuan antara salinan tidak mencukupi dengan sendirinya.
- Pelihara konteks berkaitan. Kenal pasti fail yang diabaikan, sejarah yang tidak tersedia dan pembetulan. Sediakan [pendedahan berasingan yang diminiaturkan](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient) apabila perlu, dan terangkan transformasinya tanpa menyajikannya sebagai versi asal penuh.
- Berikan penerima arahan pengesahan dan bahan yang diperlukan untuk semakan tersebut. Pastikan pemerhatian, penemuan teknikal dan kesimpulan penganalisis dapat dibezakan.

Untuk penyerahan tertentu, nyatakan hash arkib, kunci dipercayai, keputusan pengesahan dan sempadan yang dilindungi secara luaran dengan tepat. Huraikan keaslian sumber, pengaitan akaun, kelengkapan dan kesimpulan undang-undang secara berasingan. Ini memberikan pemeriksa seterusnya tuntutan khusus untuk diperiksa.
