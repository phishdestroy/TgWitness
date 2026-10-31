# Webhook keluaran

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/webhooks/

Hantar peristiwa berlingkup ke penerima HTTPS dengan tandatangan HMAC, percubaan semula dan status penghantaran.

**Utama semasa:** gunakan checkout sumber; pratonton mudah alih 0.7.0 wujud sebelum ciri ini.

[Panduan aliran kerja](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Buka **Integrasi → Webhook keluaran** di ruang kerja yang dipilih. Tambah penerima HTTPS, pilih acara pengumpul/media/pembuangan, dan secara pilihan pilih sembang untuk pemerhatian baharu dan perubahan. Teks mesej dilumpuhkan secara lalai. Mengaktifkan petikan menambah paling banyak 1,000 aksara kepada acara perubahan mesej; medan Telegram mentah dan kelayakan tidak pernah dihantar.

Salin rahsia HMAC sekali ke dalam konfigurasi terlindung penerima. Ia disulitkan dalam peti keselamatan TgWitness dan tidak dapat diperoleh semula daripada panel. Buang dan cipta semula destinasi untuk memutarnya. **Hantar** barisan **ujian sintetik** satu ujian tanpa kandungan sembang; segar semula status penghantaran untuk melihat hasilnya.

Penghantaran melanjutkan gelung pemberitahuan sedia ada bersama Apprise. Ia menggunakan laluan luar ruang kerja dan sekatan destinasi peribadi sedia ada. Tiada pelepasan balik atau pengalihan terus selepas itu. URL tidak boleh mengandungi kelayakan, rentetan pertanyaan atau fragmen; alamat peribadi memerlukan kebenaran rangkaian pada peringkat pelayan, bukan tetapan yang boleh diabaikan oleh pengguna panel.

## Payload dan tandatangan

Skema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Setiap muatan mengandungi `event_id`, `timestamp`, `workspace`, `type`, `synthetic`, dan pengira. Acara berasaskan jurnal merangkumi urutan dan hash mereka. Penyempurnaan eksport penuh dan ujian sintetik adalah acara penghantaran, tanpa rujukan jurnal berasingan yang dicipta. Notis pemadaman Telegram dan `missing_on_recheck` kekal sebagai jenis berasingan.

Header `X-TgWitness-Signature` ialah `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Hitung HMAC ke atas bait tepat `timestamp + "." + raw_request_body`, menggunakan rahsia yang dipaparkan sebagai bait UTF-8. Bandingkan tandatangan dalam masa tetap sebelum menganalisis atau bertindak ke atas badan. Tolak cap masa yang lebih daripada lima minit daripada jam anda. Cap masa dikemas kini pada setiap percubaan penghantaran.

Gunakan `event_id` sebagai kunci idempotensi dalam storan tahan lama, dengan sekatan unik atomik sebelum kesan sampingan. Tandatangan sah sahaja tidak menghalang permintaan terkini daripada dimainkan semula. Simpan ID yang telah diproses sekurang-kurangnya sepanjang keseluruhan tetingkap percubaan semula; simpan lebih lama jika penerima boleh memproses semula peristiwa yang disimpan.

## Cubaan semula

Penghantaran disusun dalam barisan secara kekal sebelum permintaan HTTP. Ia menggunakan semantik sekurang-kurangnya sekali: pengesahan yang hilang atau permulaan semula mungkin menghantar semula sesuatu peristiwa dengan ID yang sama. Terdapat lapan percubaan dengan selang masa penggandaan eksponen, bermula pada 15 saat dan dihadkan sehingga satu jam. Kejayaan memerlukan respons 2xx. Tugas yang gagal akan meninggalkan ralat yang dapat dilihat; penghantaran tidak dijamin selepas percubaan semula berakhir.

Barisan boleh memuat sehingga 1,000 penghantaran. Apabila penuh, pengimbasan acara jurnal akan berhenti dan disambung semula setelah ada ruang tersedia. Penyempurnaan eksport penuh yang tidak dapat diletakkan dalam barisan akan menyebabkan ralat barisan yang dapat dilihat. Sehingga lima penghantaran dicuba bagi setiap pusingan pemberitahuan, dan 100 rekod percubaan terkini akan disimpan. Mengalih keluar destinasi juga akan mengalih keluar penghantaran tertunggaknya.

## contoh n8n

Import [aliran kerja contoh](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Ia tidak aktif dan tidak mengandungi sebarang rahsia atau tindakan susulan. Setingkan `TGWITNESS_WEBHOOK_SECRET` dalam persekitaran pekerja n8n, benarkan akses ke persekitaran itu, dan benarkan builtin `crypto` untuk nod Kod. Contoh ini menggunakan pilihan raw-body nod Webhook, memeriksa tandatangan/kesegaran, dan mengesahkan acara yang disahkan. Ini sepadan dengan [pelaksanaan yang didokumenkan](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) bagi nod tersebut.

Sebelum menambah catatan SIEM atau pemberitahuan, tambahkan storan idempotensi tahan lama yang berasaskan kunci oleh`event_id`. Hadkan penyuntingan aliran kerja n8n dan pengekalan log pelaksanaan mengikut data yang anda pilih untuk dihantar. TgWitness tidak menambah sebarang arahan masuk.
