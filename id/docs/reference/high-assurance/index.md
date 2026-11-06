# Phala / Intel TDX · Penerapan dengan jaminan keamanan tinggi

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/

Server yang diamankan 24/7 di Hetzner atau Phala Cloud, Gateway DNS, serta pemeriksaan yang dapat diulang oleh pihak ketiga.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penerapan dan pemulihan](https://phishdestroy.github.io/TgWitness/id/docs/reference/deployment/)

![Penerapan & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Penerapan dengan jaminan tinggi menambahkan pemeriksaan independen terhadap lingkungan pengumpulan ke dalam verifikasi arsip. Peninjau memeriksa catatan penerapan dan akses yang disimpan oleh penyedia layanan cloud dan Cloudflare, dan penerapan Intel TDX menambahkan pengesahan perangkat keras terhadap lingkungan pengumpul.

Penggunaan lokal dan Docker biasa tetap tidak berubah. Tidak ada yang berjalan di sini kecuali Anda melakukan deployment dengan `python -m tgwitness.cloud`, dan pengumpul hanya membaca hostnya saat penyebaran tersebut ditetapkan `TGWITNESS_ASSURANCE`.

Diagram alur · Operator → Server, firewall tanpa aturan masuk (API penyedia); Operator → Tunnel dan DNS (API Cloudflare); Server, firewall tanpa aturan masuk → Tunnel dan DNS (hanya keluar); Server, firewall tanpa aturan masuk → Kunci penandatanganan dibuat di server; Verifier, token yang hanya dapat dibaca → Log penyedia dan firewall; Verifier, token yang hanya dapat dibaca → Alamat konektor terowongan dan ingress; Verifier, token yang hanya dapat dibaca → Pernyataan /api/assurance yang ditandatangani; Verifier, token yang hanya dapat dibaca → Berkas ZIP Bukti · Operator · Verifier, token yang hanyadapat dibaca · Server, firewall tanpaaturan masuk · Log penyedia dan firewall · Alamat konektor terowongandan ingress · Pernyataan /api/assuranceyang ditandatangani · Berkas ZIP Bukti · Tunnel dan DNS · Kunci penandatanganandibuat di server · API penyedia · API Cloudflare · hanya keluar

**Diagram dalam bentuk teks**

1. Operator → Server, firewall tanpa aturan masuk (API penyedia)
2. Operator → Tunnel dan DNS (API Cloudflare)
3. Server, firewall tanpa aturan masuk → Tunnel dan DNS (hanya keluar)
4. Server, firewall tanpa aturan masuk → Kunci penandatanganan dibuat di server
5. Verifier, token yang hanya dapat dibaca → Log penyedia dan firewall
6. Verifier, token yang hanya dapat dibaca → Alamat konektor terowongan dan ingress
7. Verifier, token yang hanya dapat dibaca → Pernyataan /api/assurance yang ditandatangani
8. Verifier, token yang hanya dapat dibaca → Berkas ZIP Bukti

**Di halaman ini**

- [Apa yang dapat diperiksa oleh verifikator](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#what-a-verifier-can-check)
- [Penyedia](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#providers)
- [VM Rahasia di Phala Cloud (Intel TDX)](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [Sebelum Anda memulai](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#before-you-start)
- [Dari panel](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#from-the-panel)
- [Terowongan cepat tanpa domain](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [Deploy](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#deploy)
- [Penerapan debug dan penguncian](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#debug-deployment-and-lock)
- [Hapus penyebaran](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#remove-a-deployment)
- [Server apa pun (diverifikasi sendiri)](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#any-server-self-attested)
- [Verifikasi](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#verify)
- [Laporan untuk penyerahan bukti](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare sebagai saksi eksternal](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [Membaca hasil penyebaran](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#reading-the-deployment-result)

## Apa yang dapat diperiksa oleh verifikator

| Klaim | Bagaimana cara memeriksanya | Dikelola oleh |
| --- | --- | --- |
| Server tersebut dibuat melalui API penyedia pada waktu yang diketahui | Objek server dan pembuatannya dalam log milik penyedia | Penyedia |
| Tidak ada yang menggunakan jalur akses penyedia tersebut | Log permintaan konsol, pemulihan, reset kata sandi, pembangunan ulang, ISO, gambar, dan cadangan | Penyedia |
| Tidak ada yang dapat terhubung ke sana | Firewall penyedia tidak memiliki aturan masuk; SSH disembunyikan sejak boot pertama | Penyedia (firewall), host (SSH) |
| Panel tersebut hanya dapat diakses melalui terowongan | Masukan terowongan diteruskan hanya ke panel; konektor berjalan dari alamat server | Cloudflare |
| Perangkat lunak ini berjalan | Hash pohon sumber yang ditandatangani oleh pengumpul sama dengan hasil checkout dari commit yang telah diterapkan | Collector, disinkronkan dengan Git |
| Kunci penandatanganan dibuat di server tersebut | Kunci tersebut menandatangani pernyataan yang mencantumkan ID server penyedia dan hash dari cloud-init yang diterimanya | Collector, telah diverifikasi oleh penyedia |
| Jurnal tersebut terkait dengan kunci dan server tersebut | Setiap proses yang dimulai di bukti ZIP membawa pengukuran host untuk server tersebut | Bukti ZIP |

Pengumpul mencatat status SSH, sesi, riwayat login, dan informasi boot dalam catatan process-start dan `host.state` yang telah ditandatangani. Pada VM biasa, ini merupakan catatan inventaris lokal, yang kemudian dibandingkan oleh peninjau dengan catatan independen dari penyedia layanan. Penerapan Intel TDX di bawah ini juga memverifikasi pengukuran yang didukung perangkat keras.

## Penyedia

| `--provider` | Kredensial | Akses hanya baca bagi Verifier | Log penyedia untuk verifikator | Disimpan untuk |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Baca token dari proyek yang sama | Tindakan server dan firewall | Selama sumber daya tersebut tersedia |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Token akses pribadi yang hanya dapat dibaca | Tindakan Droplet | Selama Droplet masih ada |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` ruang lingkup baca-saja | Peristiwa akun, versi aturan firewall | 90 hari |
| `vultr` | `VULTR_API_KEY` | Pengguna dengan akses baca dan `activity_logs` izin | Log aktivitas akun (metode, jalur, pelaku) | 30 hari, lebih lama dengan langganan log audit |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Riwayat peristiwa CloudTrail | 90 hari |
| `phala` | `PHALA_CLOUD_API_KEY` | Kunci API dari ruang kerja yang sama | Revisi aplikasi dan operasi CVM: perubahan konfigurasi dan lingkungan Docker Compose, restart, serta pembaruan sistem operasi | Selama aplikasi ini masih ada |
| `generic` | tidak ada | tidak ada | none: **disertifikasi sendiri** | – |

Gunakan proyek, tim, akun, atau sub-akun khusus untuk setiap kasus: akses hanya baca dari verifikator kemudian hanya menampilkan penyebaran ini. Kredensial dibaca dari `--provider-token-file` atau variabel di atas, bukan dari baris perintah. Untuk AWS, berkas tersebut berisi `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; wilayahnya adalah `--location`.

Apa yang tidak dapat ditampilkan oleh catatan masing-masing penyedia dicantumkan dalam setiap laporan. Singkatnya: Hetzner mencatat permintaan konsol; Konsol Pemulihan DigitalOcean, Lish/Glish dari Linode, dan konsol web Vultr tidak dicatat sebagai permintaan konsol, sehingga akses root dikunci pada booting pertama dan login konsol akan memerlukan reset kata sandi atau perubahan konfigurasi booting, yang keduanya dicatat. Vultr mengembalikan alamat konsol ke kunci apa pun yang dapat mengakses instance; baik catatan maupun laporan tidak menyimpannya.

## VM Rahasia di Phala Cloud (Intel TDX)

Dengan `--provider phala` pengumpul berjalan di mesin virtual rahasia Intel TDX di [Phala Cloud](https://phala.com/), yang dikelola oleh dstack. Host dan staf Phala tidak dapat membaca memori mesin tersebut, dan prosesor menandatangani pernyataan tentang apa yang dijalankan saat mesin dinyalakan. Verifikator tidak hanya mempercayai pernyataan Phala begitu saja: `tgwitness.tdx` memverifikasi setiap pernyataan tersebut secara mandiri, hingga ke Intel SGX Root CA yang disematkan, dengan membandingkannya terhadap daftar pencabutan Intel dan data platform yang ditandatangani Intel, serta menolak mesin yang dapat di-debug atau dimigrasikan.

| Entri laporan | Apa yang ditampilkannya |
| --- | --- |
| `tdx_binding` | Pengesahan ini mencakup pernyataan yang ditandatangani oleh pengumpul serta nilai acak dari permintaan ini |
| `tdx_quote` | Intel menjamin keabsahan sertifikasi tersebut; sertifikasi hanya akan disetujui jika Intel menilai platform tersebut telah diperbarui |
| `tdx_compose_hash` | RTMR3, yang diambil dari log peristiwa dstack, mengukur laporan komposisi aplikasi yang dilaporkan oleh pengumpul |
| `tdx_compose` | Kode tersebut, byte demi byte, sama persis dengan kode yang dihasilkan oleh commit yang telah di-deploy: berkas sumber diidentifikasi berdasarkan hash, kedua gambar berdasarkan digest, tanpa kode lain apa pun |
| `tdx_identity` | Pengesahan berasal dari aplikasi dan instans yang telah diimplementasikan, dengan kunci dari KMS Phala dan disk terenkripsi |
| `tdx_os` | MRTD dan RTMR0-2 sama dengan nilai yang dihitung oleh verifikator dari gambar OS dstack yang diterbitkan oleh Dstack-TEE, yang ditemukan berdasarkan hash gambar OS yang dilaporkan oleh CVM, serta dari tabel ACPI yang dibuat oleh QEMU untuk konfigurasi VM: firmware, kernel, initrd, baris perintah beserta hash sistem berkas root, memori, vCPU, dan perangkat. Gambar pengembangan gagal |

Gambar sistem operasi (sekitar 180 MB, di mana 21 MB disimpan) diunduh sekali dari [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) ke dalam `dstack-images` di samping catatan; `--tdx-image FOLDER` menggunakan folder lain atau gambar yang telah diekstrak, `--tdx-image none` melewatkan perbandingan. Pengukuran dilakukan oleh `dstack-mr` dan paket Rust `qemu-acpi` dari Dstack-TEE/dstack; `tools/check_dstack_image.py` memeriksanya terhadap keluaran ACPI QEMU sendiri dan terhadap catatan attestation perangkat keras Phala Cloud yang sebenarnya, sedangkan `--live` juga memeriksanya terhadap gambar yang dipublikasikan. `--tdx-measurements` tetap membandingkan MRTD dan RTMR0-2 yang diberikan dalam format JSON.

Setiap kali pengumpul dimulai dan dicatat dalam jurnal, hal tersebut disertai dengan pengesahan tersebut, sehingga `verify --evidence` memeriksa setiap kali pengumpul dimulai serta citra sistem operasi yang digunakan untuk mem-boot-nya. Revisi aplikasi Phala dan operasi CVM berfungsi sebagai log penyedia: konfigurasi Docker Compose yang diubah setelah penyebaran akan menyebabkan laporan gagal, dan proses restart dicantumkan untuk ditinjau.

Di panel, pilih **Mesin Virtual Rahasia · Phala Cloud** di bawah **Ekstra** → **Server 24/7** dan tempelkan kunci API Phala Cloud; terowongan cepat berfungsi seperti di Hetzner. Dari baris perintah:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` membaca sertifikat dan daftar pencabutan Intel dari sebuah berkas, bukan mengunduhnya dari Intel. Gateway DNS tidak tersedia di sini: Phala tidak memiliki firewall penyedia layanan untuk lalu lintas keluar.

### Sertifikat attestation

Untuk penyebaran Phala, `verify --report certificate.md` juga menulis sertifikat: sebuah `certificate.html` yang berdiri sendiri dan `certificate.pdf` berukuran A4 yang berisi kesimpulan, rantai kepercayaan dari root Intel hingga kunci pengumpul, perbandingan dengan server biasa dan server dengan jaminan tinggi, pengukuran di samping nilai yang dihitung dari gambar yang dipublikasikan, pihak yang menjamin setiap bagian, rantai sertifikat Intel, setiap pemeriksaan, log penyedia, dan cara mengulangi verifikasi. Laporan JSON tetap menjadi catatan resmi; halaman-halaman ini menampilkannya.

Laporan ini disegel secara digital dengan tanda tangan dan cap waktu, dalam berkas `certificate.seal.json` serta berkas `.tsq`/`.tsr` di sampingnya:

| Segel | Fitur tambahan |
| --- | --- |
| Cap waktu elektronik yang terverifikasi, `http://tsa.belgium.be/connect` | Cap waktu RFC 3161 pada byte yang tepat dari `certificate.json` dari penyedia layanan kepercayaan yang memenuhi syarat pemerintah federal Belgia (FPS Policy and Support, BOSA). Unit tersebut terdaftar sebagai layanan penandaan waktu yang memenuhi syarat, dengan status "diberikan", dalam daftar tepercaya UE Belgia; akar (Belgium Root CA6) dan entri-entri dalam daftar tersebut, berdasarkan daftar yang diterbitkan pada 20 Oktober 2026, disematkan dalam `tgwitness/tsa_roots.py`. Berdasarkan Peraturan (UE) No. 910/2014, Pasal 41, cap waktu semacam itu dianggap akurat dalam hal tanggal dan waktu serta integritas data di setiap negara anggota UE |
| Stempel waktu RFC 3161, FreeTSA | Stempel waktu kedua yang independen |
| Tanda tangan verifikator | Ed25519 diterapkan pada pernyataan yang mencantumkan SHA-256 laporan dan setiap cap waktu, menggunakan kunci verifikator itu sendiri (`--sign-with FOLDER`, default `~/.tgwitness/verifier`); PDF tersebut memuat tanda tangan dengan kunci yang sama |

`--timestamp URL` (dapat diulang) memilih otoritas lain, `--timestamp none` tidak memilih apa pun, `--sign-with
none` membiarkan segel tidak ditandatangani. `check-report` memeriksa hash laporan, tanda tangan verifikator, setiap cap waktu ke akar tepercaya dan status kualifikasinya, serta tanda tangan PDF. Bobot hukum dari cap waktu yang memenuhi syarat di luar UE, serta dari laporan secara keseluruhan, ditentukan oleh pengadilan atau otoritas yang menerimanya; segel tersebut menunjukkan kapan laporan tersebut ada dan bahwa laporan tersebut tidak berubah.

Sebuah pengesahan tidak dapat mengesampingkan adanya kelemahan pada modul TDX atau mikrokode Intel, atau akses fisik ke bus memori. Siapa pun yang mengendalikan aplikasi di akun Phala dapat menerapkan pesan baru; pesan tersebut muncul sebagai revisi baru dengan hash pesan baru. Host mengendalikan sumber waktu dan jaringan mesin.

Penerapan, verifikasi dengan `--evidence`, restart, perbandingan citra sistem operasi, sertifikat yang disegel secara digital dengan tanda tangan dan cap waktu, serta penghancuran telah dijalankan di Phala Cloud itu sendiri; lihat [pada 4 November 2026, jalankan](https://phishdestroy.github.io/TgWitness/id/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

## Sebelum Anda mulai

1. Sebuah zona Cloudflare, ID akunnya, dan token API dengan izin **Cloudflare Tunnel Edit**, **Zone Read**, dan **DNS Edit**, yang diberikan bersama `--cloudflare-token-file` atau `CLOUDFLARE_API_TOKEN`. Untuk verifikator: **Cloudflare Tunnel Read**, **DNS Read**, dan, untuk log audit, **Account Settings Read**. Tanpa domain, [quick tunnel](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#quick-tunnel-without-a-domain) tidak memerlukan semua ini.
2. Kredensial penyedia dengan akses tulis ke proyek khusus; `lock` menggunakan hal yang sama:

   - Hetzner: Token API dengan izin Baca & Tulis;
   - DigitalOcean: token akses pribadi dengan hak akses tulis;
   - Linode: token akses pribadi dengan `linodes`, `firewall` dan `events` ruang lingkup baca/tulis;
   - Vultr: Kunci API dari akun khusus atau sub-akun;
   - AWS: Kredensial IAM diizinkan `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` dan `ec2:RevokeSecurityGroupIngress`.
3. Komitmen yang akan dijalankan. Tag rilis diselesaikan sekali ke komitmennya dengan `git ls-remote`; server hanya menerima commit berpanjang 40 karakter.

## Dari panel

Di komputer Anda sendiri, **Extras → Server 24/7** menjalankan hal yang sama `deploy` untuk Hetzner dalam tiga langkah: pilih Eropa atau Amerika Serikat, tempelkan token Hetzner (Baca & Tulis), lalu periksa jenis server, harga bulanan, alamat, dan versi yang ditemukan panel berdasarkan token tersebut. Tidak ada yang dibuat sebelum Anda mengonfirmasi. Panel menampilkan setiap langkah sebagai `deploy` dilaporkan, kemudian alamat, token panel, dan sidik jari kunci penandatanganan. Tanpa domain, server akan mendapatkan [terowongan cepat](https://phishdestroy.github.io/TgWitness/id/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **menu “Server Anda” → “Temukan Alamat Saat Ini”** akan mencarinya kembali setelah restart. Untuk alamat tetap di bawah domain Anda sendiri, buka **“Opsional · domain Anda sendiri”** dan tambahkan token Cloudflare (tautan yang telah disiapkan akan memilih “Baca Zona”, “Edit DNS”, dan “Edit Terowongan Cloudflare”).

Token-token tersebut dikirim bersama setiap permintaan dari tab browser ke TgWitness di komputer yang sama dan tidak disimpan di mana pun; catatan penyebaran, cloud-init yang disunting, token panel, dan, untuk terowongan cepat, kunci alamat disimpan di `deployments/NAME` di dalam direktori data. Panel ini hanya menawarkan fitur ini kepada administrator utama melalui koneksi loopback langsung (`127.0.0.1`, tanpa header proxy atau terowongan); panel yang diakses melalui jaringan akan menampilkan perintah-perintah sebagai gantinya. Versi secara default menggunakan tag rilis dari panel yang sedang berjalan, yang diselesaikan melalui API GitHub. Lokasi, jenis server, dan harga berasal dari API Hetzner: `cpx22` jika tersedia di sana, jika tidak, tipe x86 termurah dengan memori minimal 2 GB.

## Tunnel cepat tanpa domain

`--quick-tunnel` menggantikan `--zone`, `--cloudflare-account` dan `--panel-host`; tidak ada akun atau token Cloudflare yang terlibat:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Di server, cloudflared membuka [terowongan cepat](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) ke panel: sebuah alamat acak `https://….trycloudflare.com` yang berubah setiap kali cloudflared atau server dimulai ulang. Sebuah layanan kecil di server memposting setiap alamat ke topik ntfy.sh yang acak, ditandatangani (HMAC-SHA256) dengan kunci yang hanya disimpan di direktori deployment (`address-key.txt`), dan mengulanginya setiap tiga jam karena ntfy.sh menyimpan postingan selama 12. `deploy` dan **Temukan alamat saat ini** hanya menerima posting yang ditandatangani, sehingga posting palsu tidak dapat mengalihkan Anda, beserta token panel Anda, ke alamat orang lain. Topik tersebut tercatat dan dipublikasikan melalui cloud-init: siapa pun yang memilikinya dapat membaca alamat saat ini, yang tetap meminta token panel. Server tidak membuka port masuk apa pun dalam kedua kasus tersebut.

Seorang verifikator tidak memiliki kunci alamat, dan siapa pun yang membaca topik tersebut dapat memposting ke sana. Jadi, pengumpul juga memposting alamat itu sendiri, yang ditandatangani dengan kunci Ed25519 miliknya sendiri, dan `verify` mengambil posting terbaru yang ditandatangani oleh kunci pengumpul dalam catatan penyebaran; posting diurutkan berdasarkan waktu ntfy.sh menerimanya, bukan waktu yang mereka klaim. Seorang pengumpul dari sebelum perubahan ini tidak menandatangani apa pun, dan `verify` kemudian mengambil posting terbaru dan menyatakan hal itu dalam pemeriksaan `statement`; sebuah posting palsu hanya dapat membuat pemeriksaan tersebut gagal, karena alamat tersebut tetap harus merespons dengan kunci pengumpul.

Biayanya: tidak ada akun Cloudflare yang menyimpan catatan tentang terowongan cepat, sehingga `verify` melaporkan terowongan, konektor, dan pemeriksaan DNS sebagai tidak tersedia, dan hasilnya paling baik adalah `incomplete` (di Phala Cloud, pemeriksaan justru lulus: konektor berjalan di dalam konfigurasi Docker Compose yang diukur); catatan penyedia, firewall, pernyataan yang ditandatangani, pengukuran host, dan perbandingan penginstal diperiksa seperti biasa. Perbandingan byte dengan penginstal referensi memerlukan commit yang telah diterapkan yang sudah mengenal `--quick-tunnel`; checkout versi 0.7.0 membangun penginstal domain dan melaporkan perbedaannya. Cloudflare tidak memberikan jaminan waktu aktif untuk terowongan cepat, mengizinkan 200 permintaan yang sedang diproses, dan tidak mendukung Server-Sent Events, sehingga pembaruan langsung pada panel (versi setelah 0.7.0) mungkin tidak sampai melalui terowongan tersebut dan tampilan perlu dimuat ulang; bagian tersebut belum dicoba. Untuk kasus yang harus tetap berfungsi, gunakan domain Anda sendiri.

## Lakukan penyebaran

Periksa terlebih dahulu semua yang akan dikirim. `plan` tidak melakukan permintaan ke penyedia layanan atau Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Kemudian lakukan deployment dengan opsi dan kredensial yang sama:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Jenis server yang dapat digunakan untuk memulai: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` dan `--image` secara default menggunakan Ubuntu 24.04 dari masing-masing penyedia di wilayah Eropa.

`--repository` mengambil commit dari repositori Git https lain, tanpa kredensial dalam URL (secara default `https://github.com/phishdestroy/TgWitness.git`). `deploy` juga menerima `--out` untuk direktori penyebaran lain (default `deployments/NAME`; direktori yang sudah berisi penyebaran akan ditolak) dan `--wait`, waktu tunggu dalam menit untuk pernyataan yang ditandatangani oleh pengumpul: 1 hingga 240, default 20, atau 60 untuk `generic`.

Perintahnya:

1. membuat terowongan Cloudflare yang mengarahkan lalu lintas masuk ke nama host panel dan, jika ditentukan, nama host saksi ke `/api/witness/head` dan `/api/assurance` saja;
2. membuat catatan CNAME yang diproksi untuk nama-nama host tersebut, dan menolak nama-nama yang sudah ada;
3. membuat firewall penyedia tanpa aturan masuk dan sebuah server di belakangnya tanpa kunci SSH, tanpa cadangan, tanpa agen konsol, serta cloud-init yang menyembunyikan SSH, mengunci akses root, menginstal `cloudflared`, mengambil commit yang tepat, memeriksanya, dan menjalankan TgWitness sebagai layanan systemd yang diperkuat;
4. menunggu pernyataan yang telah ditandatangani oleh pengumpul dan memeriksa apakah pernyataan tersebut menyebutkan server ini dan hash dari cloud-init ini.

`deployments/case-2026-11/` kemudian berisi:

| Berkas | Daftar Isi | Bagikan? |
| --- | --- | --- |
| `deployment.json` | ID, hash, panggilan API yang dilakukan (metode, jalur, status), dan pernyataan pertama yang ditandatangani | Ya, dengan verifikator |
| `cloud-init.redacted.yaml` | Perintah cloud-init yang tepat dengan dua rahasianya diganti dengan `REDACTED` | Ya |
| `panel-token.txt` | Token panel | Tidak |

Kata sandi root penyedia, token terowongan, dan token panel tidak pernah ditulis ke `deployment.json`. Publikasikan sidik jari pengumpul yang tercantum di bagian akhir melalui saluran yang tidak Anda kendalikan sendiri, misalnya saluran saksi atau pesan kepada penerima.

Masuk ke Telegram di `https://case.example.org` dengan token panel, seperti yang dijelaskan dalam [panduan akun](https://phishdestroy.github.io/TgWitness/id/docs/reference/accounts/). Tindakan panel dicatat dalam jurnal yang ditandatangani; tindakan tersebut bukanlah sesi SSH. Seorang [saksi](https://phishdestroy.github.io/TgWitness/id/docs/reference/witness/) dapat melakukan polling `https://case-witness.example.org`.

Tidak ada SSH: jika proses bootstrap gagal, kolektor tidak akan pernah merespons. Hapus server dan lakukan deployment ulang, atau gunakan deployment debug untuk mencari penyebabnya.

### Rahasia dalam data pengguna

Cloud-init menyimpan dua rahasia: token panel dan token terowongan Cloudflare. Kunci penandatanganan tidak termasuk di antaranya; kunci tersebut dibuat di server. Hetzner, DigitalOcean, dan Linode tidak mengembalikan data pengguna melalui API mereka. Vultr mengembalikannya ke kunci apa pun yang dapat membaca instans tersebut, sedangkan EC2 melalui `DescribeInstanceAttribute`. Untuk AWS, berikan verifikator hanya tiga tindakan dalam tabel, jangan pernah `ec2:Describe*`. Untuk Vultr, anggaplah kunci verifikator dapat membaca kedua token tersebut. Token terowongan memungkinkan seseorang menjalankan konektor kedua: `verify` melaporkan konektor apa pun yang tidak ada di server, dan pernyataan pengumpul tidak dapat dipalsukan dengan cara itu karena masing-masing menandatangani tantangan baru. Dengan `--quick-tunnel` rahasia kedua adalah kunci alamat: siapa pun yang membacanya dapat memposting alamat palsu yang akan diterima oleh panel.

Pernyataan publik sang pengumpul tidak mencantumkan alamat server dan sumber-sumber login; keduanya tetap tersimpan dalam jurnal yang telah ditandatangani.

## Penyebaran debug dan penguncian

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` Menyimpan SSH untuk satu kunci dari satu alamat atau jaringan kecil, paling banyak /24 untuk IPv4 atau /48 untuk IPv6. `KEY` sudah terdaftar pada penyedia: nama atau ID kunci SSH dalam proyek Hetzner, ID atau sidik jari kunci SSH dalam tim DigitalOcean, nama pengguna Linode yang kunci SSH profilnya ditambahkan ke root, ID kunci SSH dalam akun Vultr, atau nama pasangan kunci EC2 di wilayah tersebut. Opsi-opsi ini tidak berlaku untuk `generic`. Penyebaran semacam itu dicatat sebagai `debug` dan **tidak pernah** dilaporkan sebagai jaminan tinggi. Setelah selesai, jalankan `sudo tgwitness-lock` sebagai perintah terakhir dari sesi SSH terakhir, lalu:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Firewall kehilangan semua aturan masuk. Laporan kemudian menunjukkan kapan SSH diizinkan dan kapan SSH ditutup; jendela tersebut tetap terlihat.

## Hapus penyebaran

`destroy` menghapus server dan firewall-nya, yang ditemukan berdasarkan label deployment sehingga deployment yang gagal di tengah jalan juga dihapus, kemudian catatan DNS yang mengarah ke tunnel-nya, serta tunnel itu sendiri. Jurnal server dan kunci penandatanganan juga dihapus bersamanya: ekspor bukti terlebih dahulu. Catatan tetap tersimpan, ditandai `removed`, dengan panggilan API penghapusan tersebut.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Penghapusan melalui API telah diimplementasikan untuk Hetzner. Untuk penyedia lain `destroy` , hentikan proses sebelum menghapus apa pun dan tentukan label yang akan dihapus di konsol penyedia layanan. Server yang diinstal secara manual (`generic`) hanya kehilangan catatan terowongan dan DNS-nya. Penerapan terowongan cepat tidak memerlukan token Cloudflare: terowongannya berakhir di server, dan postingannya kedaluwarsa dari ntfy.sh dalam waktu 12 jam.

## Server apa pun (yang telah diverifikasi sendiri)

`--provider generic` ditujukan untuk server yang dibeli atau diinstal secara manual. `deploy` membuat terowongan dan DNS, menulis `install.sh` (pribadi) dan `install.redacted.sh` (untuk dipublikasikan), lalu menunggu. Salin `install.sh` ke server Ubuntu 24.04 yang baru diinstal dan jalankan di sana:

```
sudo bash install.sh
```

Alat ini merekam kondisi host sebagaimana adanya (login, akun, `authorized_keys`, soket pendengar, layanan, tugas terjadwal, paket), menginstal commit, mengaktifkan firewall host, menghapus dirinya sendiri, menyamarkan SSH, dan mengakhiri sesi. Laporan untuk server semacam itu, paling banter, bersifat **SELF-ATTESTED**: siapa pun yang menjalankan penginstal telah memiliki akses root sebelumnya, dan tidak ada catatan penyedia yang tersedia bagi pihak yang memverifikasi. Hal ini tetap lebih baik daripada server yang tidak dapat dijelaskan: inventaris, hash penginstal, dan setiap login selanjutnya telah ditandatangani.

## Verifikasi

Verifikator memerlukan `deployment.json`, penginstal yang telah dipublikasikan, kredensial baca-saja, dan, idealnya, salinan commit serta bukti ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Setiap penyedia dan nilai Cloudflare diminta oleh verifikator pada saat itu; catatan hanya menyediakan ID yang akan ditanyakan. Kode keluar adalah 0 untuk **LULUS**, 1 untuk **GAGAL,** dan 2 untuk **TINJAUAN**, **BELUM LENGKAP,** atau **DISERTIFIKASI SENDIRI**. `--fingerprint` harus berasal dari saluran independen; tanpa itu, kunci hanya dibandingkan dengan catatan operator. `python verify.py` tetap memverifikasi bukti ZIP itu sendiri, seperti dalam [Evidence](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/).

Tindakan penyedia diklasifikasikan: pembuatan dan pengaktifan dalam waktu 30 menit setelah pembuatan lolos; konsol, penyelamatan, reset kata sandi, pembangunan ulang, ISO, gambar, snapshot, cadangan, Systems Manager, EC2 Instance Connect, dan pembukaan firewall gagal; tindakan daya dan segala hal yang tidak terduga ditandai untuk ditinjau. Tindakan yang tidak dikenal tidak pernah lolos tanpa pemberitahuan.

## Laporan untuk penyerahan bukti

`--report report.md` menulis laporan Markdown dan `report.json` di sebelahnya:

1. hasil, sidik jari kunci pengumpul, penyebaran, penyedia, komit, server, firewall, terowongan;
2. setiap pemeriksaan beserta status dan sumbernya (API penyedia, API Cloudflare, laporan pengumpul, jurnal bukti);
3. log penyedia yang berisi penilaian setiap tindakan dan, jika penyedia mencatatnya, pelaku tindakan tersebut;
4. titik akhir Cloudflare yang menyimpan koneksi terowongan, konfigurasi, dan log audit;
5. pernyataan kolektor yang telah ditandatangani;
6. apa yang ditetapkan dalam laporan ini dan apa yang tidak;
7. perintah untuk mereproduksinya, serta SHA-256 dari setiap berkas yang diberikan kepadanya.

Serahkan laporan, `report.json`, `deployment.json`, penginstal yang telah dipublikasikan, dan bukti ZIP. Buat laporan tersebut sedini mungkin: log penyedia disimpan hanya untuk jangka waktu terbatas.

## Cloudflare sebagai saksi eksternal

Semua hal di sini bersifat opsional. Tanpa akun Cloudflare, server tetap berjalan, dan dua di antaranya saat ini berfungsi:

| Apa | Apa yang ditampilkannya | Dalam TgWitness |
| --- | --- | --- |
| Tunnel cepat atau tunnel domain Anda | Panel tersebut hanya dapat diakses melalui terowongan | wizard server, lihat di atas |
| drand relay `drand.cloudflare.com` | catatan setelah putaran drand lebih baru daripada itu: jurnal tersebut ditulis seiring berjalannya waktu | mode bukti, **lebih banyak saksi**, tanpa akun ([format](https://phishdestroy.github.io/TgWitness/id/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Pemberitahuan status terowongan | ketika terowongan tidak aktif, melalui email atau webhook dari Cloudflare | atur pengaturannya di dasbor Cloudflare |
| Gateway DNS (`--gateway-dns`, atau **Cloudflare Gateway DNS** di wizard) | setiap nama yang dicari oleh server, dijawab oleh Cloudflare melalui TLS; firewall Hetzner mencegah DNS mengakses apa pun selain itu; apakah kebijakan Gateway dapat mengubah jawaban | Hetzner, paket Zero Trust gratis, tanpa domain; `verify` memeriksa firewall, lokasi, pencatatan, kebijakan, kueri server, dan log audit; mode bukti menyalin log ke dalam jurnal |
| Gateway dengan Cloudflare Satu klien di server, sebuah firewall keluar yang hanya mengizinkan Cloudflare | setiap koneksi yang dibuat oleh server, bukan hanya DNS | belum dibuat |
| Akses di bagian depan panel | siapa yang masuk ke panel dan kapan | belum tersedia: memerlukan domain Anda sendiri |
| Pencatatan perintah SSH | setiap perintah dalam sesi debug | belum dibuat |

Logpush, yang akan menyimpan salinan milik Cloudflare sendiri di R2, merupakan fitur Enterprise: pada paket gratis, Cloudflare merespons `logpush is not enabled for this account`. Log Gateway-nya bertahan selama 24 jam di sana, sehingga mode bukti menyalinnya ke dalam jurnal yang ditandatangani (**log Cloudflare Gateway mengenai permintaan DNS server ini**, sebuah token baca-saja dengan akses Account Analytics Read).

Tanpa rencana Zero Trust, sebuah akun memiliki satu lokasi DNS. Ketika Cloudflare menolak yang lain, server membagikan lokasi yang ada dan kueri-kuerinya dibedakan berdasarkan alamatnya; filter tersebut juga memerlukan akses Zero Trust PII Read, dan `destroy` meninggalkan lokasi bersama. Satu kueri log mencakup paling lama tiga jam, sehingga salinan dan `verify` membaca data harian dalam jendela waktu tiga jam.

Gateway DNS mencakup resolver sistem. DNS melalui HTTPS pada port 443 ke resolver lain, dan koneksi ke alamat yang tidak dicari di mana pun (misalnya, pusat data Telegram), tidak tercatat dalam lognya.

Cloudflare tidak dapat melihat isi enkripsi Telegram, perangkat lain pada akun Telegram (daftar perangkat dalam mode bukti mencatatnya dari sisi Telegram) atau hypervisor penyedia layanan.

## Membaca hasil penyebaran

Untuk VM biasa, penyedia mengontrol infrastruktur host, dan inventaris lokal diverifikasi bersamaan dengan catatan penyedia. Untuk Intel TDX, verifikator juga memeriksa spesifikasi perangkat keras, pengikatan pengumpul, komposisi, dan pengukuran sistem operasi. Baca hasil masing-masing untuk melihat pemeriksaan mana yang lulus atau tidak tersedia.

Rincian firewall historis bergantung pada penyedia; Linode menyimpan versi aturan. Catatan validasi   mencantumkan penerapan yang telah diuji dan pemeriksaan aktif yang tersisa, serta ruang lingkup verifikasi   menghubungkan pemeriksaan lingkungan ini dengan akuisisi arsip dan integritasnya.
