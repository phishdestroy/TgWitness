# Saksi bebas

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/

Jalankan witness dengan kunci dan botnya sendiri, terbitkan titik pemeriksaan yang ditandatangani ke saluran dan periksa eksport menentangnya.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[Eksport dan sahkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/) · [Jaminan tinggi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/) · [Panduan panel](https://phishdestroy.github.io/TgWitness/ms/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

Diyagram aliran · Pengumpul → Saksi (titik pemeriksaan yang ditandatangani: jumlah rekod + hash kepala); Saksi → Jurnal saksi, kunci sendiri; Saksi → Saluran Telegram (pos yang disahkan melalui botnya sendiri); ZIP Bukti → verify.py; Jurnal saksi, kunci sendiri → verify.py; Saluran Telegram → verify.py (Eksport Telegram Desktop atau halaman t.me/s) · Pengumpul · Saksi · Jurnal saksi, kuncisendiri · Saluran Telegram · ZIP Bukti · verify.py · titik pemeriksaan yang · ditandatangani: jumlah rekod · + hash kepala · pos yang disahkan melalui · botnya sendiri · Eksport Telegram Desktop · atau halaman t.me/s

**Diagram sebagai teks**

1. Pengumpul → Saksi (titik pemeriksaan yang ditandatangani: jumlah rekod + hash kepala)
2. Saksi → Jurnal saksi, kunci sendiri
3. Saksi → Saluran Telegram (pos yang disahkan melalui botnya sendiri)
4. ZIP Bukti → verify.py
5. Jurnal saksi, kunci sendiri → verify.py
6. Saluran Telegram → verify.py (Eksport Telegram Desktop atau halaman t.me/s)

**On this page**

- [What the witness gets, and what it does not](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [What it checks and records](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#what-it-checks-and-records)
- [Run a witness](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#run-a-witness)
- [Public proof page for several workspaces](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Verify](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/#verify)

## Apa yang diperoleh oleh saksi, dan apa yang tidak

| Saksi mempunyai | Saksi tidak pernah |
| --- | --- |
| **Token saksi** baca sahaja untuk satu ruang kerja | Sesi Telegram atau kelayakan API pengumpul |
| Kunci Ed25519 dan jurnal tersendiri | Bilik perbendaharaan pengumpul, kunci tandatangan atau token panel |
| Token bot Telegramnya sendiri | Kandungan mesej: kepala ialah kiraan rekod dan hash |

Token itu dicipta di **Ekstra → Saksi Bebas**, dipaparkan sekali sahaja dan disimpan hanya sebagai imej SHA-256. Ia membuka tepat satu titik hujung, `GET /api/witness/head`, yang mengembalikan checkpoint yang baru ditandatangani serta penjejak koleksi kosong yang ditandatangani dan kesihatan operasi. Ia tidak dapat membuka panel, membaca kandungan mesej atau menukar tetapan, dan token panel tidak diterima di sana. Batalkan token di halaman yang sama. Pengumpul merekodkan bila kunci saksi baru mula memeriksa (`witness.seen`) dan memaparkan pemeriksaan terakhir bagi setiap token; seorang saksi yang belum memeriksa dalam tempoh 2.5 selang masa akan ditandakan sebagai lewat.

Saksi baharu menghantar cabaran rawak pada setiap undian; pernyataan tangkapan memantulkannya di bawah tandatangan pengumpul. Pengira diikat pada checkpoint tepat dan disertakan dalam kiriman saksi bertandatangan. Kepala warisan kekal diterima oleh saksi berdiri sendiri. Pertumbuhan jurnal sahaja tidak pernah dikira sebagai mesej baharu.

## Apa yang diperiksa dan direkodkan

Setiap selang (10 minit secara lalai) saksi:

1. mengambil kepala itu sendiri (pengumpul tidak boleh menolaknya atau melangkauinya);
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
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

Buka **Extras → Saksi Bebas → Konfigurasi** dalam panel. Tiga langkah merangkumi akses baca sahaja, saluran dan selang anda, kemudian melancarkan saksi. Dasar penerbitan, proksi HTTP/SOCKS5 pilihan dan alamat Bot API tersuai berada di bawah **Tetapan Lanjutan**. Borang memuat turun `witness.json` dengan kunci pengumpul ruang kerja ini dipin. Muat turun token baca sahaja yang baru dicipta dengan **Simpan fail akses** sebagai `witness-token.txt`; letakkan ia dan a `bot-token.txt`yang dicipta pada hos saksi di sebelah JSON tersebut. Pengumpul tidak pernah menerima token bot. Pemunggahan tidak memulakan perkhidmatan atau menerbitkan mesej. Tiada saksi projek yang dihoskan didaftarkan secara implisit.

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

### Terbitkan ke Discord

Saksi boleh menyiarkan ke saluran Discord sebagai ganti Telegram. Di Discord, buka **Sunting Saluran → Integrasi → Webhook**, buat webhook dan salin URLnya. Dalam panel, pilih **webhook Discord · saluran anda** pada langkah 2. Pada hos saksi, simpan URL sebagai `discord-webhook.txt` di sebelah `witness.json`; ia tidak pernah sampai ke pengumpul.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Saksi mempunyai satu penerbit sahaja: saluran Telegram atau webhook Discord, bukan kedua-duanya. Pos membawa kenyataan berasingan yang sama dan tidak boleh menghantar pemberitahuan kepada sesiapa. Pos yang lebih panjang daripada 2,000 aksara Discord digantikan dengan satu baris pendek dengan semakan penuh dilampirkan sebagai `witness-check.txt`. Setiap ID pos direkodkan sebagai `witness.posted`. `verify.py --channel`membaca hanya eksport saluran Telegram, jadi untuk Discord simpan jurnal saksi: ia mengandungi setiap semakan.

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

Alamat pengumpul, token dan saluran datang daripada `--collector`, `--token` atau `--token-file`, `--bot-token` atau `--bot-token-file`, `--discord-webhook-file` dan `--channel`, atau `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` dan `_CHANNEL`, yang menyembunyikan rahsia daripada senarai proses.

Fail konfigurasi menggunakan nama pilihan dengan tanda hubung bawah, serta `texts`, yang menggantikan perkataan-perkataan dalam pos saluran:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Kunci `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Baris perintah mengatasi persekitaran, persekitaran mengatasi fail. Pilihan atau kunci teks yang tidak dikenali menghentikan saksi dengan mesej dan bukannya diabaikan. Penulisan tidak pernah menjejaskan pengesahan: verify.py menyemak token yang disahkan di akhir setiap kiriman. Dengan `--post changes` atau `problems`, pemeriksaan yang tidak dihantar masih terdapat dalam jurnal saksi dan `verify.py` menyenaraikannya sebagai tidak pernah dihantar; rekod permulaan menamakan dasar. Setiap pemeriksaan masih muncul dalam jurnal, jadi lebih sedikit kiriman bermakna lebih sedikit masa Telegram bebas, bukan lebih sedikit pemeriksaan.

Tanpa saluran, saksi masih menyimpan jurnalnya. Simpan cap jari kunci saksi (`python -m tgwitness.witness fingerprint`) di tempat lain.

## Halaman bukti awam untuk beberapa ruang kerja

`python -m tgwitness.proof` menyaksikan sehingga 32 ruang kerja sekaligus dan menyediakan halaman baca sahaja dengan semakan berasingan terkini bagi setiap satu. Setiap ruang kerja mendapat kunci saksi dan jurnal sendiri di bawah folder data serta kunci pengumpul yang dipin; penghantaran ke saluran Telegram adalah pilihan bagi setiap ruang kerja. Mulakan dari [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Medan | Maksud |
| --- | --- |
| `title` | Tajuk halaman, 1–100 aksara |
| `data_dir` | Kunci dan jurnal saksi, berbanding fail; lalai `proof-data` |
| `interval`, `timeout` | Minit antara pemeriksaan (1–1440, lalai 5); saat untuk menunggu (5–600, lalai 20) |
| `workspaces[].id`, `label` | Alias huruf kecil dan nama yang dipaparkan |
| `workspaces[].collector` | Alamat pengumpul; ruang kerja lain berakhir dengan `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Diperlukan, berbeza untuk setiap ruang kerja |
| `workspaces[].token_file` | Fail dengan token saksi baca sahaja bagi ruang kerja tersebut |
| `workspaces[].channel`, `bot_token_file` | Pilihan, secara bersama: hantar setiap semakan ke saluran |
| `workspaces[].proxy`, `bot_api` | Alamat API laluan dan Bot pilihan |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

Perintah pertama mengesahkan fail dan fail token tanpa membuka sambungan. Halaman ini hanya menjawab GET dan HEAD:

- `/` menunjukkan setiap ruang kerja; ruang kerja yang tidak diperiksa untuk selang 2.5 ditandakan sebagai lapuk.
- `/api/proof` mengembalikan nilai yang sama seperti JSON.
- `/api/proof/<id>` memuat turun kenyataan bertandatangan terkini (`tgwitness-public-proof-v1`): nombor rekod saksi dan hash, status, kunci pengumpul yang dipin, checkpoint, koleksi pengira dan sama ada pos saluran berjaya, ditandatangani oleh kunci saksi ruang kerja tersebut.
- `/healthz` menjawab 503 apabila monitor ruang kerja telah berhenti.

Berikan halaman nama hosnya sendiri, seperti dalam [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). Untuk pengesahan, eksport jurnal saksi ruang kerja dengan `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` dan gunakan ia seperti yang diterangkan di bawah.

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

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
