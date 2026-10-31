# Saksi bebas

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/

Jalankan witness dengan kunci dan botnya sendiri, terbitkan titik pemeriksaan yang ditandatangani ke saluran dan periksa eksport menentangnya.

[Penyediaan bot dan proksi dalam bahasa Rusia](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Pengumpul menandatangani jurnalnya sendiri, jadi sesiapa yang mengawal pengumpul dan kuncinya secara prinsip boleh menulis semula atau memendekkan jurnal itu dan menandatangani semula. Seorang saksi menjadikannya dapat dikesan. Ia adalah proses berasingan — satu lagi kontena, atau lebih tepat sebuah pelayan yang dijalankan oleh orang lain — yang setiap beberapa minit mengambil kepala jurnal yang ditandatangani oleh pengumpul, menandatangani apa yang dilihatnya dengan kunci sendiri, menyimpannya dalam jurnalnya sendiri dan menyiarkannya ke saluran Telegram.

Diyagram aliran · Pengumpul → Saksi (titik pemeriksaan yang ditandatangani: jumlah rekod + hash kepala); Saksi → Jurnal saksi, kunci sendiri; Saksi → Saluran Telegram (pos yang disahkan melalui botnya sendiri); ZIP Bukti → verify.py; Jurnal saksi, kunci sendiri → verify.py; Saluran Telegram → verify.py (Eksport Telegram Desktop atau halaman t.me/s) · Pengumpul · Saksi · Jurnal saksi, kuncisendiri · Saluran Telegram · ZIP Bukti · verify.py · titik pemeriksaan yang · ditandatangani: jumlah rekod · + hash kepala · pos yang disahkan melalui · botnya sendiri · Eksport Telegram Desktop · atau halaman t.me/s

**Diagram sebagai teks**

1. Pengumpul → Saksi (titik pemeriksaan yang ditandatangani: jumlah rekod + hash kepala)
2. Saksi → Jurnal saksi, kunci sendiri
3. Saksi → Saluran Telegram (pos yang disahkan melalui botnya sendiri)
4. ZIP Bukti → verify.py
5. Jurnal saksi, kunci sendiri → verify.py
6. Saluran Telegram → verify.py (Eksport Telegram Desktop atau halaman t.me/s)

## Apa yang diperoleh oleh saksi, dan apa yang tidak

| Saksi mempunyai | Saksi tidak pernah |
| --- | --- |
| **Token saksi** baca sahaja untuk satu ruang kerja | Sesi Telegram atau kelayakan API pengumpul |
| Kunci Ed25519 dan jurnal tersendiri | Bilik perbendaharaan pengumpul, kunci tandatangan atau token panel |
| Token bot Telegramnya sendiri | Kandungan mesej: kepala ialah kiraan rekod dan hash |

Token ini dicipta di halaman **Witness** panel, dipaparkan sekali sahaja dan disimpan hanya sebagai SHA-256. Ia membuka tepat satu titik hujung, `GET /api/witness/head`, yang mengembalikan checkpoint yang baru ditandatangani serta penjejak pengumpulan tanpa kandungan yang ditandatangani dan status kesihatan operasi. Ia tidak dapat membuka panel, membaca kandungan mesej atau menukar tetapan, dan token panel tidak diterima di sana. Batalkan token di halaman yang sama. Pengumpul merekodkan bila kunci saksi baharu mula memeriksa (`witness.seen`) dan memaparkan pemeriksaan terakhir bagi setiap token; saksi yang belum memeriksa dalam tempoh 2.5 selang masa akan ditandakan lewat.

Saksi baharu menghantar cabaran rawak pada setiap undian; pernyataan tangkapan memantulkannya di bawah tandatangan pengumpul. Pengira diikat pada checkpoint tepat dan disertakan dalam kiriman saksi bertandatangan. Kepala warisan kekal diterima oleh saksi berdiri sendiri. Pertumbuhan jurnal sahaja tidak pernah dikira sebagai mesej baharu.

## Apa yang diperiksa dan direkodkan

Setiap selang (10 minit secara lalai) saksi:

1. mengambil kepala itu sendiri (pengumpul tidak boleh menolaknya atau melangkauinya);
2. memeriksa sahih tandatangan pengumpul, kunci pengumpul yang dipasang pin (`--collector-fingerprint`, atau kunci pertama yang dilihat), kiraan yang tidak berkurang dan kepala yang tidak berubah pada kiraan yang tidak berubah;
3. menambah rekod yang disahkan ke jurnalnya sendiri: `witness.anchor` dengan status `ok`, `key_changed`, `rollback` (lebih sedikit rekod berbanding sebelum ini), `fork` (panjang sama, kepala berbeza) atau `invalid` (jawapan gagal pengesahan), atau `witness.no_response` apabila pengumpul tidak menjawab;
4. menyiarkan hasil ke saluran, ditandatangani, termasuk "tiada jawapan" selagi saksi sedang berjalan dan boleh mengakses Bot API. ID siaran direkodkan (`witness.posted`), siaran gagal juga (`witness.post_failed`).

Satu pos kelihatan seperti ini; baris terakhir memuatkan kenyataan yang disahkan:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Jalankan witness

Anda memerlukan bot Telegram (cipta satu dengan @BotFather), sebuah saluran di mana bot tersebut adalah pentadbir, dan alamat pengumpul yang boleh diakses oleh saksi — melalui HTTPS di luar rangkaian persendirian (lihat profil HTTPS dalam [penyebaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/)).

Buka **Tambahan → Bot dalam saluran anda → Sediakan bot** dalam panel. Tiga langkah merangkumi akses baca sahaja, saluran anda dan selang, kemudian melancarkan saksi. Dasar penerbitan, proksi HTTP/SOCKS5 pilihan dan alamat Bot API tersuai berada di bawah **Tetapan Lanjutan** . Borang memuat turun `witness.json` dengan kunci pengumpul ruang kerja ini dilampirkan. Muat turun token baca sahaja yang baru dicipta dengan **Simpan fail akses** sebagai `witness-token.txt` ; letakkan ia dan `bot-token.txt` yang dicipta pada hos saksi di sebelah JSON itu. Pengumpul tidak pernah menerima token bot. Pemunggahan tidak memulakan perkhidmatan atau menerbitkan mesej. Tiada saksi projek yang dihoskan didaftarkan secara tersirat.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Perintah pertama memeriksa konfigurasi dan fail rahsia tanpa permintaan rangkaian atau penciptaan kunci. Laluan dalam JSON adalah relatif kepada fail tersebut; laluan CLI/persekitaran adalah relatif kepada direktori kerja. Simpan cap jari saksi di luar hosnya. Penunjuk tinjauan terakhir pengumpul hanya mengesahkan permintaan; penerbitan dilaporkan oleh Bukti atau disemak dalam jurnal saksi dan saluran.

Jika panel diletakkan di sebalik terowong SSH, pendedahkan hanya hujung witness yang dipetakan pada nama hos HTTPS berasingan dengan [contoh Caddy ini](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). Ruang kerja lalai kemudian menggunakan `https://witness.example.org`, manakala ruang kerja lain menggunakan `https://witness.example.org/profiles/ID`. Token masih diperlukan; panel dan laluan API lain tidak diteruskan oleh hos maya tersebut.

Pilih `all` untuk checkpoint yang diterbitkan secara berkala. Jeda lima minit bermaksud kira-kira 288 pos setiap ruang kerja setiap hari. `changes`/`problems` sengaja tidak menerbitkan beberapa pemeriksaan. MTProxy adalah untuk klien Telegram pengumpul. Pemantauan HTTP dan Bot API HTTPS Telegram menggunakan laluan langsung/HTTP/SOCKS5 mereka sendiri ([Bot API](https://core.telegram.org/bots/api)).

**Di sebelah pengumpul, dengan Docker** (hos yang sama — proses dan kunci yang berasingan, tetapi pengendali yang sama): masukkan nilai dalam `.env` dan mulakan profil.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Untuk imej yang diterbitkan, gunakan `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**Pada pelayan orang lain** (saksi bebas sebenar): salin repositori ke sana, tetapkan `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` ditambah tiga nilai di atas dalam `.env`, kemudian

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

atau tanpa Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Pilihan

| Pilihan | Persekitaran | Lalai | Maksud |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Minit antara pemeriksaan, 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | Masa menunggu untuk pengumpul dan Bot API, 5–600 |
| `--post` | `_POST` | `all` | `all`: setiap pemeriksaan; `changes`: ketua baru atau masalah; `problems`: hanya masalah dan jawapan yang hilang |
| `--title` | `_TITLE` | `TgWitness witness` | Kata pertama setiap kiriman saluran |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Pasang kunci pengumpul dan bukannya mempercayai jawapan pertama |
| `--proxy` | `_PROXY` | langsung | `socks5://host:port` atau `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Alamat Bot API, contohnya pelayan Bot API tempatan |
| `--data-dir` | `_DATA` | `witness-data` | Kunci saksi dan jurnal |
| `--config` | `_CONFIG` | – | Fail JSON dengan mana-mana pilihan di atas |

Alamat pengumpul, token dan saluran berasal daripada `--collector`, `--token` atau `--token-file`, `--bot-token` atau `--bot-token-file` dan `--channel`, atau `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` dan `_CHANNEL`, yang menyimpan rahsia di luar senarai proses.

Fail konfigurasi menggunakan nama pilihan dengan tanda hubung bawah, serta `texts`, yang menggantikan perkataan-perkataan dalam pos saluran:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Kunci `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Baris perintah mengatasi persekitaran, persekitaran mengatasi fail. Pilihan atau kunci teks yang tidak dikenali menghentikan saksi dengan mesej dan bukannya diabaikan. Penulisan tidak pernah menjejaskan pengesahan: verify.py menyemak token yang disahkan di akhir setiap kiriman. Dengan `--post changes` atau `problems`, pemeriksaan yang tidak dihantar masih terdapat dalam jurnal saksi dan `verify.py` menyenaraikannya sebagai tidak pernah dihantar; rekod permulaan menamakan dasar. Setiap pemeriksaan masih muncul dalam jurnal, jadi lebih sedikit kiriman bermakna lebih sedikit masa Telegram bebas, bukan lebih sedikit pemeriksaan.

Tanpa saluran, saksi masih menyimpan jurnalnya. Simpan cap jari kunci saksi (`python -m tgwitness.witness fingerprint`) di tempat lain.

## Sahkan

Pada pihak saksi, eksport jurnalnya:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Kemudian, di mana-mana, dengan fail ZIP yang disahkan oleh pengumpul dan saluran yang dieksport daripada Telegram Desktop (*Eksport sejarah sembang* → JSON menghasilkan `result.json` ) atau halaman awamnya `https://t.me/s/…` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` memeriksa jurnal saksi (rantaian dan tandatangan), kemudian memastikan **setiap kepala yang dilihat saksi adalah sebahagian daripada jurnal yang dieksport**: rekod pada kiraan itu mesti mempunyai hash yang tepat itu. Satu kepala yang tidak sepadan gagal pengesahan — jurnal itu telah diubah selepas saksi melihatnya. Ia juga melaporkan kepala yang dilihat selepas eksport, anomali yang direkodkan oleh saksi, jawapan yang gagal, tempoh yang checkpoint padanannya hadir dalam eksport ini ("Disaksikan dari X ke Y") dan kekosongan. Checkpoint kemudian tidak memanjangkan tempoh tersebut. Hasilnya termasuk nombor rekod padanan terakhir dan bilangan rekod-rekod terakhir yang tiada checkpoint sepadan. Hanya jawapan yang ditandatangani oleh kunci eksport itu sendiri dikira: eksport yang ditandatangani oleh kunci yang tidak pernah dilihat oleh saksi dilaporkan sebagai tidak disaksikan, dan tanpa `--fingerprint` penandatanganinya kekal tidak dipin. Dengan `--channel`, setiap kiriman yang disahkan mesti sepadan dengan jurnal saksi, rekod demi rekod: kiriman yang diubah gagal pengesahan, manakala kiriman yang hilang akan disenaraikan. Tarikh dalam eksport JSON Telegram yang disediakan adalah metadata yang boleh disunting, di luar token saksi yang disahkan. Kespadanan token tidak mengesahkan tarikh penerbitan; hasilnya secara eksplisit melaporkan bahawa pengesahan masa penerbitan tidak dijalankan.

### Perlukan sempadan eksport yang disaksikan

Untuk penyerahan yang mesti merangkumi rekod akhir disaksikan, tambahkan `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Ini memerlukan cap jari saksi yang disimpan secara berasingan dan checkpoint yang sepadan di hujung tepat eksport ini. Satu checkpoint yang hanya merangkumi pratonton awal adalah tidak mencukupi. Jeda pengumpulan, biarkan saksi memerhati keadaan akhir, dan eksport sebelum penulisan jurnal selanjutnya; jika jurnal berubah, simpan satu lagi checkpoint dan eksport keadaan itu. Satu checkpoint kemudian sahaja tidak dapat mengesahkan hash akhir eksport yang lebih pendek. Apabila `--channel` turut disertakan, pos yang didakwa hilang atau set padanan kosong akan menyebabkan pemeriksaan ketat ini gagal. Tanpa penanda itu, pemeriksaan integriti biasa masih melaporkan rekod yang tidak disaksikan tanpa menolak arkib yang sebaliknya utuh.

Penanda ini menguatkan konsistensi dengan rekod saksi yang disediakan dan dipaku. Pengendali masih perlu mengesahkan kebebasan saksi dan memelihara rekodnya secara berasingan. Ia tidak mengesahkan kebenaran mesej, pengumpulan lengkap atau jangka masa yang diukur secara bebas.

Saksi menunjukkan apa yang dilaporkan oleh pengumpul pada masa-masa tersebut dan bahawa eksport kemudian sepadan dengannya. Ia tidak menunjukkan bahawa pengumpul merekodkan segala yang dihantar oleh Telegram, atau bahawa kandungan mesej itu benar. Saksi yang dijalankan oleh pengendali yang sama pada mesin yang sama adalah lebih lemah daripada yang dijalankan oleh orang lain.

Bilangan yang meningkat sahaja tidak dapat membuktikan kesinambungan hanya-tambah dalam talian: perbandingan luar talian mesti memadankan setiap hash prefiks yang disimpan dengan eksport penuh pengumpul. Masa henti saksi dan kegagalan penerbitan meninggalkan selang tanpa jangkar luaran. Pos yang hilang boleh dilaporkan dalam jurnal saksi yang disimpan; sama ada saluran mahupun pelayan yang dikawal oleh pengendali yang sama bukanlah arkib pihak ketiga yang tidak berubah.
