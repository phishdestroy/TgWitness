# Rujukan Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-board/

Penanda buku, sorotan tepat, hirisan tindakan, perbincangan, akses terhad dan sejarah anotasi bertandatangan yang digunakan oleh Case Board.

Case Board memberikan pasukan penyiasatan paparan kerja bersama bagi bahan yang disimpan. Tandakan pemerhatian, sorot petikan tepat, simpan satu siri tindakan, dan bincangkannya dengan rakan sekerja. Kad mengekalkan rujukan sumber dan sejarah semakan yang disahkan. Anotasi pasukan kekal di ruang kerja, boleh dibezakan secara berasingan daripada pemerhatian Telegram asal.

[Model bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/) · [Akses](https://phishdestroy.github.io/TgWitness/ms/docs/reference/access/) · [Laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/) · [Bahasa Rusia](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/CASE-BOARD.md)

![Suapan siasatan sintetik](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Bekerja dengan satu kes

Buka **Siasatan → Papan Kes** dalam mod Standard atau Pakar. Bahasa mengikut panel. Gunakan **papan Penanda** di sebelah rekod jurnal atau mesej sembang yang disimpan, atau fokuskannya dan tekan **B**. Penanda halaman ditambah ke Peti Masuk dengan satu klik. Sunting tajuk, label dan nota, atau pindahkan ke koleksi. Kad yang diubah akan menambah semakan bertandatangan; memadamnya mengekalkan sejarah.

Untuk kes pertama, pilih satu koleksi dan tambahkan rekod yang menjawab satu soalan. Gunakan ulasan untuk menyemak tafsiran, kemudian **Presentasi** untuk meneroka kad dan konteks sumber. Pilih bahan Papan Kes secara berasingan di [Studio Laporan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/case-reports/) apabila menyediakan hasil kerja. Menyimpan hirisan tidak secara automatik mengkonfigurasi penapis data laporan.

Pilih teks dalam mesej sembang yang disimpan untuk mendedahkan **Sorotan → papan**. Pilih warnanya dan tambah nota. Pelayan memeriksa petikan tepat dan versi yang disimpan, termasuk emoji, teks RTL dan tanda gabungan. Antaramuka tidak memetakan pilihan melalui teks yang disamarkan atau diubah suai.

Klik-pindahkan dua rekod dalam satu sembang untuk **memotong di antaranya**, gunakan **Potongan mengikut masa**, atau simpan penapis sembang semasa, tempoh dan jenis-peristiwa jurnal. Potongan yang disimpan mempunyai predikat berkuasa sendiri: membukanya dalam Jurnal juga menerapkan pelbagai sembang, had nombor mesej dan penapis pelaku. **Tunjukkan rekod yang ditambah sejak penanda buku** memisahkan penambahan kemudian. Menukar penapis Jurnal akan keluar daripada hirisan. Daripada Orang, **Hiris tindakan orang ini** menggunakan ID pelaku yang direkodkan; ia tidak menganggap bahawa penulis mesej telah menyunting, memadam atau bertindak balas terhadap mesej.

Tetingkap pratonton Slice memaparkan kiraan sebelum membenarkan penciptaan. `all` merangkumi setiap jenis yang direkodkan, termasuk imej skrin, suntingan, pemadaman, reaksi, kemas kini keahlian/perkhidmatan, tindakan sendiri, butang, hasil media, mesej yang dipulihkan dan jenis peristiwa masa depan. Pilihan ini menerangkan pemerhatian yang disimpan. Notis pemadaman sembang tidak diketahui adalah konteks berasingan, hanya tersedia kepada akses seluruh ruang kerja, dan tidak pernah dikaitkan dengan mana-mana sembang yang dipilih.

Koleksi mempunyai skop sembang yang dinyatakan. Skop kosong bermaksud keseluruhan ruang kerja. Satu koleksi tidak boleh mengandungi kad di luar skopnya; peserta yang terhad kepada sembang tidak boleh membaca koleksi yang lebih luas. Inbox adalah koleksi maya untuk kad yang tidak ditugaskan. Carian dan penapis hanya merangkumi kad yang kelihatan; benang dan sebutan mewarisi capaian kad induk. Komen yang dipadam mempunyai penanda kubur dalam perbincangan. Tiada sejarah paparan direkodkan.

**Pembentangan** membuka semua kad dalam koleksi yang dipilih, dengan paparan Konteks Kad, Sumber dan komen Pasukan serta kawalan papan kekunci Sebelum/Seterusnya. Ia tidak menyediakan sebarang kawalan penyuntingan. Suapan biasa dipaginasi; pembentangan memuatkan senarainya dalam halaman dan memuatkan butiran satu kad pada satu masa.

## Kebenaran

Semua operasi memerlukan `view`, skop ruang kerja/sembang dan `board.read`. `board.write` menambah kad, komen, pemindahan dan status buka/semak. `board.manage` membenarkan pengurusan koleksi, status disahkan/ditolak, semakan/pembuangan kad orang lain. Status adalah keputusan pasukan bukan hasil pengesahan kriptografi.

Preset bentuk akses: Pengulas = baca; Penganalisis = baca/tulis; Pengendali = baca/tulis/urus, di samping kebenaran sedia ada mereka. Pemberian kebenaran sedia ada tidak secara senyap memperoleh hak baharu. Pentadbir utama mempunyai semua hak, dan menyiarkan sebagai **Pentadbir utama**. Gunakan pemberian bernama untuk pengesahan. Senarai sebutan hanya menyenaraikan capaian semasa yang dapat membaca keseluruhan kad induk.

Kebenaran untuk sembang A tidak dapat memperoleh kad atau hirisan untuk A+B, walaupun dengan meneka IDnya atau memberikan `target.chat_id` palsu. Metadata sasaran diselesaikan daripada hash peristiwa yang disahkan di pelayan. Kumpulan, bilangan perbincangan, kad berkaitan dan pemberitahuan langsung ditapis sebelum maklum balas. Pengeksportan memerlukan `export` serta `board.read`; pengeksport sedia ada tanpa akses papan mendapat arkib bukti biasa tanpa nota pasukan. SSE menyemak semula kebenaran semasa sebelum setiap kelompok.

## Kontrak yang disimpan

Seperti pemerhatian, anotasi ditulis secara transaksi ke dalam jadual SQLite yang hanya menambah di ruang kerja. `annotations.jsonl` ialah eksport kanonik tepat daripadanya daripada snapshot baca yang sama seperti `events.jsonl`. Tiada stor anotasi kedua yang bersaing dan tiada acara jurnal `board.activity`.

Setiap baris mempunyai tepat:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

Contoh ringkas di atas menggambarkan sampul; muatan sebenar merangkumi lalai model mereka dan medan sasaran yang diselesaikan oleh pelayan. Skema permintaan API berada di bawah [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), dijana daripada model Pydantic masa larian oleh `python tools/build_board_schemas.py`. Medan permintaan tambahan ditolak. ID dijana di pihak pelayan apabila diabaikan. Penulisan, masa, snapshot dan tandatangan tidak boleh dibekalkan oleh pemanggil. ID pemberian bernama mengikuti format 16-heksadeksa sedia ada Access; ID kad adalah 32 heksadeksa.

JSON kanonik adalah UTF-8, kunci objek disusun, tiada ruang kosong antara token, Unicode tanpa pelarian, dan tiada NaN/infiniti. Hash anotasi ialah SHA-256 bagi objek kanonik yang mengandungi `format: "tgwitness-annotations-v1"` dan semua tujuh medan sampul sehingga `previous_hash`. Tag format ini memisahkan domain hashnya daripada pemerhatian. Tandatangan adalah Ed25519 ke atas 32 bait hash mentah. Urutan bermula pada 1. Semakan mengekalkan ID kad dan menamakan hash anotasi sebelumnya dalam `supersedes`; ia tidak boleh menukar skop sembang. Pergerakan, status dan pemadaman adalah rekod berasingan. Jadual SQLite menolak UPDATE dan DELETE.

`case-board.json` mengandungi `{statement, signature}`. Pernyataan kanonik ditandatangani oleh kunci ruang kerja dan mengandungi `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning`, dan `state`. Keadaan adalah ulangan deterministik: `annotations_head`, satu tatasusunan `items` yang teratur (koleksi, kad, komen termasuk batu nisan), dan `status_history`. Item mengekalkan hash anotasi terakhir, urutan, pengarang dan masa mereka, serta pencipta asal dan masa penciptaan merentasi semakan. Main semula menyemak semakan, ibu bapa, rujukan koleksi dan ID tindakan dwi. `manifest.json` dan titik pemeriksaan baharu juga mengikat `annotations_head`. Kekalkan titik pemeriksaan secara berasingan untuk mengesan pemotongan atau penulisan semula dengan kunci tandatangan yang disalin.

### Versi teks

`range.start` adalah ofset titik kod Unicode berasaskan sifar, `length` adalah kiraan titik kod positif, dan `quote` mesti sama dengan subrentetan tepat daripada `payload.text` atau `payload.caption` pada acara sasaran. Tiada NFC/NFKC, lipatan huruf besar/kecil atau normalisasi grafem diterapkan. Potongan rentetan Python dan JavaScript `Array.from(text)` melaksanakan indeksasi yang sama. Menggabungkan tanda dan emoji ZWJ mungkin mengambil beberapa titik kod. `range.version` ialah hash acara sasaran, bukan versi mesej semasa atau ofset entiti UTF-16 Telegram. Suntingan kemudian tidak akan memindahkan sorotan secara automatik.

### Potong identiti dan masa

`query` menerima tepat satu `chat_id` atau `chat_ids` yang tidak kosong, pilihan `from`/`to` yang merangkumi, batas ID-mesej yang merangkumi (satu sembang sahaja), `kinds: "all"` atau jenis wildcard tepat/awalan, `actors` yang nyata, `search`, `hide_system`, dan `include_unscoped`. Kumpulan jenis Jurnal berkembang kepada predikat tepat mereka. Carian menggunakan carian muatan jurnal NFC/case-folded tanpa mengubah teks sumber yang ditandatangani. Tarikh memerlukan zon waktu dan dinormalisasi ke UTC. Tarikh menapis **observed_at**. Telegram`source_at` dipaparkan secara berasingan. Pemadaman tanpa cap masa sumber tidak mempunyai masa pemadaman rekaan. Rekod lewat yang diperhatikan di luar selang masa tidak akan dimasukkan ke dalamnya; hirisan message-ID boleh merangkumi pemadaman kemudian untuk ID mesej tersebut.

`snapshot` menetapkan masa penciptaan, sempadan urutan/hash jurnal, bilangan padanan, urutan pertama/terakhir dan `result_hash`. Yang terakhir ialah SHA-256 bagi susunan JSON kanonik UTF-8 yang mengandungi hash peristiwa yang sepadan disusun secara leksikografik, termasuk `[]` untuk hirisan kosong. Ia juga membawa kiraan tepat jenis dan miniatur masa pemerhatian 24-bin. Satu hirisan menyimpan pertanyaan, bukan rekod sumber dwiulang. Semasa eksport, `board/slices/<id>.json` menyenaraikan hash semasa dan urutan yang ditambah/dihapuskan. Pemverifikasi membina semula keputusan asal pada sempadan penciptaan, kemudian keputusan semasa. Rekod yang ditambah dilaporkan sebagai fakta perubahan. Mengeluarkan peristiwa asal memutuskan rantaian bukti yang tidak dapat diubah; ia tidak diterima secara senyap sebagai penghapusan biasa daripada hirisan.

Snek reaksi mempunyai senarai pelakon terkini yang tidak lengkap. Penjelajah membandingkan snek bersebelahan bagi sembang/mesej yang sama, termasuk satu snek sebelumnya di luar potongan, dan melaporkan perbezaan jumlah agregat **antara pemerhatian**. Pelakon terkini yang hilang tidak dianggap telah membuang reaksi. Sneak peek pertama tidak mempunyai keadaan awal yang disimpulkan. Pengamatan pelaku kekal dikaitkan dengan sneak peek di mana ia disediakan, bukan kepada masa tindakan yang dicipta.

## API dan eksport

`GET /api/board` menerima collection/chat/author/label/state/from/to/q/kind/comments, offset/limit dan susunan newest/oldest. `GET /api/board/card/{id}` memulangkan kad, pratonton sumber, rentetan, sejarah status dan kad berkaitan. Subrute peserta memulangkan pilihan sebutan yang layak. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` menambah rekod. `POST /api/board/slice-preview` mengira pertanyaan. Rekod potongan dipaparkan secara berhalaman di `GET /api/board/slice/{id}/records`; pengiraan semula sentiasa menggunakan snapshot bacaan stabil semasa. `/api/stream` secara langsung menghantar pemberitahuan `board` tanpa muatan, berasingan daripada penuding jurnal.

`GET /api/board/export` memulangkan dokumen yang disahkan. Akses terhad sembang menerima **pendedahan** yang disahkan dan dilabel dengan jelas, bukan anotasi sembang lain atau keseluruhan rantaian. ZIP bukti penuh mengandungi `annotations.jsonl`, `case-board.json` yang disahkan dan lampiran JSON hirisan. Tetapan laporan HTML/PDF/JSON membolehkan pilihan tiada papan, penanda buku/hirisan tanpa perbincangan, atau kad dengan komen. Bahagian ini secara eksplisit memisahkan pendapat pasukan daripada pemerhatian. Penapis data laporan juga mengehadkan nota yang boleh dibaca; fail sumber berasingan yang ditandatangani dalam ZIP bukti kekal lengkap.

`GET /api/board/slice/{id}/export` menghasilkan petikan JSON `tgwitness-board-selection-v1` yang ditandatangani; `?format=csv` menghasilkan jadual yang mudah tanpa tandatangan berdiri sendiri. Kekalkan JSON dan ZIP:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Semakan pemilihan mengesahkan kenyataan yang ditandatangani, rekod sumber yang tepat dan kelengkapan pertanyaan pada sempadan yang dinyatakan. Fail ZIP bukti mungkin lebih baru tetapi mesti mengandungi awalan tersebut. Sasaran tergantung dilaporkan secara eksplisit. Snek potongan asal yang berbeza, anotasi yang diubah, keadaan main semula yang tidak sepadan atau sumber yang diubah akan menyebabkan kegagalan. Arkib lama tanpa anotasi mengekalkan tingkah laku pengesahan sedia ada.

Serahan secara lalai ditetapkan sebagai **Jangan sertakan**. Penyertaan eksplisit memaparkan kad melalui rekod yang telah dimampatkan, mengecualikan sasaran yang tidak dapat diakses/yang dikecualikan, menahan sorotan yang teks sumbernya telah dimampatkan, membersihkan teks pasukan dengan peraturan sebutan/penghubungan yang sama, dan secara pilihan menggantikan label penyiasat dengan R01, R02… dalam metadata dan kemunculan yang diketahui dalam nota. Tiada `annotations.jsonl` asal didedahkan. Fail sidecar `tgwitness-case-board-handover-v1` yang disahkan dan laporan mengandungi bahan yang diminiaturkan yang sama. Bilangan hirisan hanya menerangkan rekod yang didedahkan, dengan butiran pelaku sorotan/permintaan asal disembunyikan. Nama dalam teks bebas yang tidak diketahui oleh peminimal masih memerlukan semakan, seperti dalam penyerahan biasa. Derivatif ini tidak mendakwa mengekalkan tandatangan anotasi asal selepas penyensoran.

## Had operasi

Parameter termasuk had lembut 10,000 kad dan 50,000 komen, satu halaman hirisan sehingga 5,000 rekod, dan kawalan pratonton media. Had lembut memberi amaran tanpa memadam sejarah. Halaman suapan dihadkan kepada maksimum 200 kad. Petikan potongan JSON berdiri sendiri dihadkan kepada 64 MiB; sempitkan pertanyaan atau gunakan fail ZIP yang disahkan untuk bahan yang lebih besar. Pengesah berdiri sendiri mengehadkan ulangan anotasi kepada 256 MiB. Tiada pemberitahuan komen luaran diaktifkan atau dilaksanakan oleh Case Board.

Penerimaan automatik ciri ini menggunakan data rekaan dan pengangkutan Telegram simulasi untuk memeriksa penyimpanan, capaian, pemaparan dan eksport. Lihat [skop pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) untuk julat pemeriksaan bukti.
