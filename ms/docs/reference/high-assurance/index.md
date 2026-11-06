# Penyebaran berjaminan tinggi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/

Pelayan 24/7 yang disegel di Hetzner atau Phala Cloud, Gateway DNS dan pemeriksaan yang boleh diulang oleh pihak ketiga.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Penyebaran dan pemulihan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/deployment/)

![Penyebaran & pemulihan](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Penyebaran berjaminan tinggi menambah semakan bebas terhadap persekitaran pengumpulan kepada pengesahan arkib. Penilai menyemak rekod penyebaran dan capaian yang disimpan oleh penyedia awan dan Cloudflare, dan penyebaran Intel TDX menambah pengesahan perkakasan terhadap persekitaran pengumpul.

Penggunaan biasa secara tempatan dan Docker tidak berubah. Tiada apa yang berjalan di sini melainkan anda menyebarkan dengan `python -m tgwitness.cloud`, dan pengumpul hanya membaca hosnya apabila penyebaran menetapkan `TGWITNESS_ASSURANCE`.

Diyagram aliran · Pengendali → Pelayan, firewall tanpa peraturan masuk (API penyedia); Pengendali → Terowong dan DNS (API Cloudflare); Pelayan, firewall tanpa peraturan masuk → Terowong dan DNS (keluar sahaja); Pelayan, firewall tanpa peraturan masuk → Kunci penandatangan dicipta pada pelayan; Pemverifikasi, token baca sahaja → Log penyedia dan tembok api; Pemverifikasi, token baca sahaja → Alamat penyambung terowong dan kemasukan; Pemverifikasi, token baca sahaja → Pernyataan /api/jaminan yang ditandatangani; Pemverifikasi, token baca sahaja → ZIP Bukti · Pengendali · Pemverifikasi, token bacasahaja · Pelayan, firewall tanpaperaturan masuk · Log penyedia dan tembokapi · Alamat penyambung terowongdan kemasukan · Pernyataan /api/jaminanyang ditandatangani · ZIP Bukti · Terowong dan DNS · Kunci penandatangandicipta pada pelayan · API penyedia · API Cloudflare · keluar sahaja

**Diagram sebagai teks**

1. Pengendali → Pelayan, firewall tanpa peraturan masuk (API penyedia)
2. Pengendali → Terowong dan DNS (API Cloudflare)
3. Pelayan, firewall tanpa peraturan masuk → Terowong dan DNS (keluar sahaja)
4. Pelayan, firewall tanpa peraturan masuk → Kunci penandatangan dicipta pada pelayan
5. Pemverifikasi, token baca sahaja → Log penyedia dan tembok api
6. Pemverifikasi, token baca sahaja → Alamat penyambung terowong dan kemasukan
7. Pemverifikasi, token baca sahaja → Pernyataan /api/jaminan yang ditandatangani
8. Pemverifikasi, token baca sahaja → ZIP Bukti

**Pada halaman ini**

- [Apa yang boleh disemak oleh pengesah](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#what-a-verifier-can-check)
- [Penyedia](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#providers)
- [VM Peribadi di Phala Cloud (Intel TDX)](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [Sebelum anda bermula](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#before-you-start)
- [Daripada panel](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#from-the-panel)
- [Terowong pantas tanpa domain](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [Tempatkan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#deploy)
- [Debug penyebaran dan kunci](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#debug-deployment-and-lock)
- [Hapuskan penyebaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#remove-a-deployment)
- [Sebarang pelayan (yang mengesahkan sendiri)](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#any-server-self-attested)
- [Verifikasi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#verify)
- [Laporan penyerahan bukti](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare sebagai saksi luar](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [Membaca keputusan penyebaran](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#reading-the-deployment-result)

## Apa yang boleh disemak oleh pengesah

| Tuntutan | Bagaimana ia disemak | Disimpan oleh |
| --- | --- | --- |
| Pelayan ini dicipta melalui API penyedia pada masa yang diketahui | Objek pelayan dan penciptaannya dalam log penyedia sendiri | Penyedia |
| Tiada siapa menggunakan laluan akses penyedia | Logs permintaan konsol, pemulihan, menetapkan semula kata laluan, membina semula, ISO, imej, sandaran | Penyedia |
| Tiada apa pun boleh menyambung kepadanya | Firewall penyedia tidak mempunyai peraturan masuk; SSH disamarkan sejak but pertama. | Penyedia (tembok api), hos (SSH) |
| Panel ini hanya boleh diakses melalui terowong | Pemasukan terowong meneruskan sambungan hanya ke panel; penyambung dijalankan dari alamat pelayan | Cloudflare |
| Perisian ini tepat berjalan | Hash pokok sumber yang ditandatangani oleh pengumpul sama dengan checkout komit yang dikerahkan | Pengumpul, disemak menentang Git |
| Kunci penandatanganan telah dibuat pada pelayan tersebut | Kunci menandatangani pernyataan yang menamakan ID pelayan penyedia dan hash cloud-init yang diterimanya | Pengumpul, disemak menentang penyedia |
| Jurnal ini milik kunci dan pelayan tersebut | Setiap proses bermula dalam bukti ZIP membawa ukuran hos untuk pelayan tersebut | Bukti ZIP |

Pengumpul merekodkan keadaan SSH, sesi, sejarah log masuk dan maklumat but dalam rekod bermula-proses yang ditandatangani dan rekod `host.state`. Pada VM biasa, ini adalah rekod inventori tempatan yang dibandingkan oleh pemeriksa dengan rekod bebas penyedia. Penyebaran Intel TDX di bawah juga mengesahkan ukuran yang disokong perkakasan.

## Penyedia

| `--provider` | Kredensial | Akses baca sahaja untuk pengesah | Log penyedia untuk pengesah | Disimpan untuk |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Bacakan token projek yang sama | Tindakan pelayan dan tembok api | Sementara sumber-sumber wujud |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Token akses peribadi baca sahaja | Tindakan Droplet | Sementara Droplet wujud |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` skop baca sahaja | Acara akaun, versi peraturan tembok api | 90 hari |
| `vultr` | `VULTR_API_KEY` | Pengguna dengan akses baca dan `activity_logs` izin | Log aktiviti akaun (kaedah, laluan, pelaku) | 30 hari, lebih lama dengan langganan log audit |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Sejarah acara CloudTrail | 90 hari |
| `phala` | `PHALA_CLOUD_API_KEY` | Kunci API bagi ruang kerja yang sama | Revisi aplikasi dan operasi CVM: konfigurasi Docker Compose dan perubahan persekitaran, permulaan semula, peningkatan OS | Sementara aplikasi wujud |
| `generic` | tiada | tiada | tiada: **disahkan sendiri** | – |

Gunakan projek, pasukan, akaun atau sub-akaun khusus untuk setiap kes: akses baca sahaja pemeriksa kemudian hanya memaparkan penyebaran ini. Kredensial dibaca daripada `--provider-token-file` atau pembolehubah di atas, tidak pernah daripada baris perintah. Untuk AWS fail tersebut mengandungi `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; rantau adalah `--location`.

Apa yang tidak dapat ditunjukkan oleh rekod setiap penyedia dicetak dalam setiap laporan. Ringkasnya: Hetzner merekod permintaan konsol; Konsol Pemulihan DigitalOcean, Lish/Glish Linode dan konsol web Vultr tidak direkod sedemikian, jadi root dikunci pada but pertama dan log masuk konsol memerlukan menetapkan semula kata laluan atau menukar but, yang direkodkan. Vultr memulangkan alamat konsol kepada mana-mana kunci yang boleh membaca instans; neither rekod mahupun laporan menyimpannya.

## VM Peribadi di Phala Cloud (Intel TDX)

Dengan `--provider phala` pengumpul dijalankan dalam mesin maya sulit Intel TDX di [Phala Cloud](https://phala.com/), yang diuruskan oleh dstack. Host dan kakitangan Phala tidak dapat membaca memori-nya, dan pemproses menandatangani pengesahan tentang apa yang dimuatkan oleh mesin. Pengesah tidak mengambil kata Phala begitu sahaja: `tgwitness.tdx` memeriksa setiap pengesahan itu sendiri, sehingga ke Intel SGX Root CA yang dipasang, menentang senarai penarikan balik Intel dan data platform yang disahkan oleh Intel, dan menolak mesin yang boleh diperiksa pepijat atau dipindahkan.

| Laporan kemasukan | Apa yang dipaparkan |
| --- | --- |
| `tdx_binding` | Pengesahan merangkumi pernyataan bertandatangan pengumpul dan nilai rawak permintaan ini |
| `tdx_quote` | Intel menjamin pengesahan itu; ia hanya diluluskan apabila Intel menilai platform tersebut sebagai terkini |
| `tdx_compose_hash` | RTMR3, dimainkan semula daripada log acara dstack, mengukur komposisi aplikasi yang dilaporkan oleh pengumpul |
| `tdx_compose` | Kompos itu bait demi bait adalah sama dengan yang dibina oleh kod komit yang dikerahkan: fail sumber yang dipin oleh hash, kedua-dua imej oleh digest, tiada kod lain |
| `tdx_identity` | Pengesahan datang daripada aplikasi dan instans yang dikerahkan, dengan kunci daripada KMS Phala dan cakera yang disulitkan |
| `tdx_os` | MRTD dan RTMR0-2 sama dengan nilai yang dikira oleh pengesah daripada imej OS dstack yang diterbitkan oleh Dstack-TEE, yang ditemui melalui hash imej OS yang dilaporkan oleh CVM, dan daripada jadual ACPI yang dibina oleh QEMU untuk bentuk VM: firmware, kernel, initrd, baris perintah dengan hash sistem fail root, memori, vCPU dan peranti. Imej pembangunan gagal |

Imej OS (kira-kira 180 MB, di mana 21 MB disimpan) dimuat turun sekali dari [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) ke dalam `dstack-images` di sebelah rekod; `--tdx-image FOLDER` menggunakan folder lain atau imej yang tidak dikemas, `--tdx-image none` melangkau perbandingan. Pengukuran ini diikuti oleh `dstack-mr` dan pakej Rust `qemu-acpi` daripada Dstack-TEE/dstack; `tools/check_dstack_image.py` menyemaknya dengan keluaran ACPI QEMU sendiri dan dengan rekod pengesahan perkakasan Phala Cloud sebenar, `--live` juga menyemak dengan imej yang diterbitkan. `--tdx-measurements` masih membandingkan MRTD dan RTMR0-2 yang diberikan sebagai JSON sebaliknya.

Setiap permulaan pengumpul yang direkodkan dalam jurnal membawa pengesahan sedemikian, jadi `verify --evidence` memeriksa setiap permulaan dan imej OS yang dibootstrap. Semakan aplikasi Phala dan operasi CVM berfungsi sebagai log penyedia: konfigurasi Docker Compose yang diubah selepas penyebaran gagal laporan itu, dan permulaan semula disenaraikan untuk semakan.

Dalam panel pilih **Mesin maya sulit · Phala Cloud** di bawah **Ekstra** → **Pelayan 24/7** dan tampal kunci API Phala Cloud; terowong pantas berfungsi seperti di Hetzner. Dari baris arahan:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` membaca sijil Intel dan senarai pembatalan daripada fail dan bukannya memuat turunnya daripada Intel. Gateway DNS tidak tersedia di sini: Phala tiada firewall penyedia untuk trafik keluar.

### Sijil pengesahan

Untuk penyebaran Phala `verify --report certificate.md` juga menulis sijil: a `certificate.html` yang berdiri sendiri dan sebuah A4 `certificate.pdf` dengan keputusan, rantaian kepercayaan daripada root Intel kepada kunci pengumpul, perbandingan dengan pelayan biasa dan pelayan berjaminan tinggi, ukuran di sebelah nilai yang dikira daripada imej yang diterbitkan, siapa yang menjamin setiap bahagian, rantaian sijil Intel, setiap semakan, log penyedia, dan cara mengulangi pengesahan. Laporan JSON kekal sebagai rekod yang sah; halaman-halaman memaparkannya.

Laporan ini disegel secara digital dengan tandatangan dan cap masa, dalam `certificate.seal.json` dan fail `.tsq`/`.tsr` di sisinya:

| Segel | Apa yang ditambahkannya |
| --- | --- |
| Cop masa elektronik berkelayakan, `http://tsa.belgium.be/connect` | Cap masa RFC 3161 ke atas bait tepat `certificate.json` daripada penyedia perkhidmatan kepercayaan berkelayakan kerajaan persekutuan Belgium (FPS Policy and Support, BOSA). Unitnya disenaraikan sebagai perkhidmatan cop masa bertauliah, status diberikan, dalam senarai dipercayai EU Belgium; root (Belgium Root CA6) dan entri dalam senarai itu, setakat senarai yang dikeluarkan pada 20 Oktober 2026, disemat dalam `tgwitness/tsa_roots.py`. Di bawah Peraturan (EU) No 910/2014, artikel 41, cop masa sedemikian dianggap tepat dari segi tarikh dan masa serta integriti data di setiap negara anggota EU |
| Cap masa RFC 3161, FreeTSA | Cap masa kedua yang bebas |
| Tandatangan pengesah | Ed25519 ke atas satu kenyataan yang menamakan SHA-256 laporan dan setiap cap masa, dengan kunci verifier sendiri (`--sign-with FOLDER`, lalai `~/.tgwitness/verifier`); PDF itu mengandungi tandatangan dengan kunci yang sama |

`--timestamp URL` (boleh diulang) memilih pihak berkuasa lain, `--timestamp none` tiada, `--sign-with
none` meninggalkan meterai tanpa ditandatangani. `check-report` memeriksa hash laporan, tandatangan pengesah, setiap cap masa kepada akar dipercayai dan status berkelayakannya, serta tandatangan PDF. Berat undang-undang cap masa bertauliah di luar EU, dan laporan secara keseluruhannya, adalah terpulang kepada mahkamah atau pihak berkuasa yang menerimanya; meterai menunjukkan bila laporan itu wujud dan bahawa ia tidak berubah.

Satu pengesahan tidak dapat menolak kecacatan dalam modul TDX atau mikrokod Intel, atau akses fizikal ke pembus memori. Sesiapa yang mengawal aplikasi dalam akaun Phala boleh menyebarkan compose lain; ia muncul sebagai semakan baru dengan hash compose baru. Host mengawal sumber masa mesin dan rangkaian.

Tugaskan, sahkan dengan `--evidence`, mulakan semula, bandingkan imej OS, sijil yang disegel secara digital dengan tandatangan dan cop masa dan musnahkan telah dijalankan pada Phala Cloud itu sendiri; lihat [, larian 4 November 2026](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

## Sebelum anda bermula

1. Zon Cloudflare, ID akaunnya, dan token API dengan **Cloudflare Tunnel Edit**, **Zone Read** dan **DNS Edit**, diberikan dengan `--cloudflare-token-file` atau `CLOUDFLARE_API_TOKEN`. Untuk pengesah: **Baca Terowong Cloudflare**, **Baca DNS** dan, untuk log audit, **Baca Tetapan Akaun**. Tanpa domain, [terowong pantas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#quick-tunnel-without-a-domain) tidak memerlukan mana-mana daripadanya.
2. Kredensial penyedia dengan akses menulis ke projek khusus; `lock` menggunakan yang sama:

   - Hetzner: token API dengan kebenaran Baca & Tulis;
   - DigitalOcean: token akses peribadi dengan kebenaran menulis;
   - Linode: token akses peribadi dengan `linodes`, `firewall` dan `events` skop baca/tulis;
   - Vultr: Kunci API akaun khusus atau sub-akaun;
   - AWS: kelayakan IAM dibenarkan `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` dan `ec2:RevokeSecurityGroupIngress`.
3. Komit untuk dijalankan. Tag rilis diselesaikan sekali ke komitnya dengan `git ls-remote`; pelayan hanya menerima komit 40 aksara itu.

## Daripada panel

Pada komputer anda sendiri, **Ekstra → Pelayan 24/7** menjalankan perkara yang sama `deploy` untuk Hetzner dalam tiga langkah: pilih Eropah atau Amerika Syarikat, tampal token Hetzner (Baca & Tulis), kemudian semak jenis pelayan, harga bulanan, alamat dan versi yang ditemui oleh panel dengan token tersebut. Tiada apa-apa yang dicipta sebelum anda mengesahkan. Panel memaparkan setiap langkah sebagai `deploy` melaporkannya, kemudian alamat, token panel dan cap jari kunci penandatangan. Tanpa domain, pelayan mendapat [terowong pantas](https://phishdestroy.github.io/TgWitness/ms/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **Pelayan anda → Cari alamat semasa** mencarinya semula selepas but semula. Untuk alamat tetap di bawah domain anda sendiri, buka **Pilihan · domain anda sendiri** dan tambahkan token Cloudflare (pautan yang disediakan memilih Baca Zon, Sunting DNS dan Sunting Terowong Cloudflare).

Token-token ini dibawa bersama setiap permintaan dari tab pelayar ke TgWitness pada komputer yang sama dan tidak ditulis di mana-mana; rekod penyebaran, cloud-init yang disembunyikan, token panel dan, untuk terowong pantas, kunci alamat disimpan dalam `deployments/NAME` dalam direktori data. Panel ini hanya menawarkannya kepada pentadbir utama melalui sambungan loopback langsung (`127.0.0.1`, tiada penanda aras atau pengepala terowong); panel yang diakses melalui rangkaian memaparkan arahan sebaliknya. Versi secara lalai adalah tag keluaran panel yang sedang berjalan, diselesaikan melalui API GitHub. Lokasi, jenis pelayan dan harga diperoleh daripada API Hetzner: `cpx22` di mana ia ditawarkan, jika tidak, jenis x86 paling murah dengan sekurang-kurangnya 2 GB memori.

## Terowong pantas tanpa domain

`--quick-tunnel` menggantikan `--zone`, `--cloudflare-account` dan `--panel-host`; tiada akaun atau token Cloudflare terlibat:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Pada pelayan, cloudflared membuka [terowong pantas](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) ke panel: satu rawak `https://….trycloudflare.com` alamat yang berubah setiap kali cloudflared atau pelayan dihidupkan semula. Satu perkhidmatan kecil pada pelayan menyiarkan setiap alamat ke topik ntfy.sh rawak, yang disahkan (HMAC-SHA256) dengan kunci yang hanya dipegang oleh direktori penyebaran (`address-key.txt`), dan mengulanginya setiap tiga jam kerana ntfy.sh menyimpan kiriman selama 12 jam. `deploy` dan **Cari alamat semasa** hanya menerima kiriman bermasa, jadi kiriman palsu tidak dapat menghantar anda, dan token panel anda, ke alamat orang lain. Topik itu terdapat dalam rekod dan cloud-init yang diterbitkan: sesiapa yang memilikinya boleh membaca alamat semasa, yang masih meminta token panel. Pelayan tidak membuka sebarang port masuk.

Pemverifikasi tidak mempunyai kunci alamat, dan sesiapa sahaja yang membaca topik boleh menghantar kiriman kepadanya. Jadi pengumpul juga menghantar alamat itu sendiri, yang ditandatangani dengan kunci Ed25519 miliknya sendiri, dan `verify` mengambil kiriman terbaru yang ditandatangani oleh kunci pengumpul dalam rekod penyebaran; kiriman diatur mengikut masa ntfy.sh menerimanya, bukan masa yang mereka dakwa. Pengumpul dari sebelum perubahan ini tidak menandatangani apa-apa, dan `verify` kemudian mengambil pos terbaru dan menyatakan demikian dalam pemeriksaan `statement`; pos palsu hanya boleh menyebabkan pemeriksaan itu gagal, kerana alamat masih perlu menjawab dengan kunci pengumpul.

Kosnya: tiada akaun Cloudflare menyimpan rekod terowong pantas, jadi `verify` melaporkan terowong, penyambung dan semakan DNS sebagai tidak tersedia dan hasilnya paling baik ialah `incomplete` (pada Phala Cloud pemeriksaan lulus sebaliknya: penyambung dijalankan di dalam konfigurasi Docker Compose yang diukur); rekod penyedia, firewall, pernyataan bertauliah, pengukuran hos dan perbandingan pemasang diperiksa seperti biasa. Perbandingan bait dengan pemasang rujukan memerlukan commit yang telah dikerahkan yang sudah mengetahui `--quick-tunnel`; checkout 0.7.0 membina pemasang domain dan melaporkan perbezaannya. Cloudflare memberikan terowong pantas tanpa jaminan masa operasi, membenarkan 200 permintaan serentak dan tidak menyokong Server-Sent Events, jadi kemas kini langsung panel (versi selepas 0.7.0) mungkin tidak sampai melalui satu terowong dan paparan perlu dimuat semula; bahagian itu belum dicuba. Untuk kes yang perlu bertahan, gunakan domain anda sendiri.

## Tempatkan

Lihat dahulu semua yang akan dihantar. `plan` tidak membuat permintaan kepada penyedia atau Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Kemudian, sebar dengan pilihan yang sama dan maklumat kelayakan:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Jenis pelayan untuk dimulakan: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` dan `--image` secara lalai ke Ubuntu 24.04 setiap penyedia di rantau Eropah.

`--repository` mengambil komit daripada repositori Git https lain, tanpa kelayakan dalam URL (laluan lalai `https://github.com/phishdestroy/TgWitness.git`). `deploy` juga menerima `--out` untuk direktori penyebaran lain (default `deployments/NAME`; direktori yang sudah mengandungi penyebaran akan ditolak) dan `--wait`, minit untuk menunggu kenyataan berkanun pengumpul: 1 hingga 240, lalai 20, atau 60 untuk `generic`.

Perintah:

1. mencipta terowong Cloudflare yang kemasukannya meneruskan nama hos panel kepada panel dan, jika diberikan, nama hos saksi kepada `/api/witness/head` dan `/api/assurance` hanya;
2. mencipta rekod CNAME proksi untuk nama hos tersebut, menolak nama yang sudah wujud;
3. mencipta firewall penyedia tanpa peraturan masuk dan sebuah pelayan di belakangnya tanpa kunci SSH, tiada sandaran, tiada ejen konsol, dan cloud-init yang menyamar SSH, mengunci root, memasang `cloudflared`, memuat turun tepat commit tersebut, memeriksanya dan memulakan TgWitness sebagai perkhidmatan systemd yang dipertingkatkan;
4. menunggu kenyataan berasingan pengumpul dan memeriksa bahawa ia menamakan pelayan ini dan hash cloud-init ini.

`deployments/case-2026-11/` kemudian memegang:

| Fail | Kandungan | Kongsi? |
| --- | --- | --- |
| `deployment.json` | ID, hash, panggilan API yang dibuat (kaedah, laluan, status) dan kenyataan pertama yang ditandatangani | Ya, dengan pengesah |
| `cloud-init.redacted.yaml` | Cloud-init tepat dengan dua rahsia digantikan oleh `REDACTED` | Ya |
| `panel-token.txt` | Token panel | Tidak |

Kata laluin root penyedia, token terowong dan token panel tidak pernah ditulis ke `deployment.json`. Terbitkan cap jari pengumpul yang dicetak di bahagian akhir melalui saluran yang anda tidak kendalikan bersendirian, contohnya saluran saksi atau mesej kepada penerima.

Log masuk ke Telegram di `https://case.example.org` dengan token panel, seperti dalam [panduan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/reference/accounts/). Tindakan panel direkodkan dalam jurnal yang ditandatangani; ia bukan sesi SSH. [Saksi](https://phishdestroy.github.io/TgWitness/ms/docs/reference/witness/) boleh membuat permintaan `https://case-witness.example.org`.

Tiada SSH: jika bootstrap gagal, pengumpul tidak akan menjawab. Padamkan pelayan dan deploy semula, atau gunakan deploy debug untuk mencari puncanya.

### Rahsia dalam data pengguna

cloud-init membawa dua rahsia: token panel dan token terowong Cloudflare. Kunci tandatangan tidak termasuk di dalamnya; ia dicipta pada pelayan. Hetzner, DigitalOcean dan Linode tidak mengembalikan data pengguna melalui API mereka. Vultr mengembalikannya kepada mana-mana kunci yang boleh membaca instans, dan EC2 melalui `DescribeInstanceAttribute`. Untuk AWS berikan pengesah hanya tiga tindakan dalam jadual, jangan pernah `ec2:Describe*`. Untuk Vultr, anggap kunci pengesah boleh membaca kedua-dua token. Token terowong membolehkan seseorang menjalankan penyambung kedua: `verify` melaporkan mana-mana penyambung yang tidak berada di pelayan, dan kenyataan pengumpul tidak dapat dipalsukan dengan cara itu kerana setiap satu menandatangani cabaran baharu. Dengan `--quick-tunnel` rahsia kedua ialah kunci alamat sebaliknya: sesiapa yang membacanya boleh menyiarkan alamat palsu yang akan diterima oleh panel.

Pernyataan awam pengumpul tidak menyertakan alamat pelayan dan sumber log masuk; kedua-duanya kekal dalam jurnal yang ditandatangani.

## Debug penyebaran dan kunci

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` menjaga SSH untuk satu kunci daripada satu alamat atau rangkaian kecil, paling banyak /24 untuk IPv4 atau /48 untuk IPv6. `KEY` telah didaftarkan dengan penyedia: nama atau ID kunci SSH dalam projek Hetzner, ID atau cap jari kunci SSH dalam pasukan DigitalOcean, nama pengguna Linode yang kunci SSH profilnya ditambah ke root, ID kunci SSH dalam akaun Vultr, atau nama pasangan kunci EC2 di rantau tersebut. Pilihan ini tidak terpakai kepada `generic`. Penyebaran sedemikian direkodkan sebagai `debug` dan **tidak pernah** dilaporkan sebagai high-assurance. Apabila anda selesai, jalankan `sudo tgwitness-lock` sebagai arahan terakhir sesi SSH terakhir, kemudian:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Firewall kehilangan setiap peraturan masuk. Laporan kemudian menunjukkan bila SSH dibenarkan dan bila ia ditutup; tetingkap itu kekal kelihatan.

## Hapus penyebaran

`destroy` memadam pelayan dan firewall-nya, yang ditemui melalui label penyebaran supaya penyebaran yang gagal separuh jalan turut dialihkan, kemudian rekod DNS yang menunjuk ke terowongnya, dan terowong itu. Jurnal pelayan dan kunci tandatangan dipadam bersamanya: eksport bukti terlebih dahulu. Rekod kekal, ditandakan `removed`, dengan panggilan API penyingkiran.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Penghapusan melalui API dilaksanakan untuk Hetzner. Bagi penyedia lain `destroy` berhenti sebelum memadam apa-apa dan menamakan label untuk dipadam dalam konsol penyedia. Pelayan yang dipasang secara manual (`generic`) hanya kehilangan rekod terowong dan DNSnya. Penyebaran terowong pantas tidak memerlukan token Cloudflare: terowongnya berakhir pada pelayan, dan kirimannya luput dari ntfy.sh dalam masa 12 jam.

## Sebarang pelayan (disahkan sendiri)

`--provider generic` adalah untuk pelayan yang dibeli atau dipasang secara manual. `deploy` mencipta terowong dan DNS, menulis `install.sh` (peribadi) dan `install.redacted.sh` (untuk diterbitkan), dan menunggu. Salin `install.sh` ke pelayan Ubuntu 24.04 yang baru dipasang dan jalankan di sana:

```
sudo bash install.sh
```

Ia merekodkan hos seperti sedia kala (log masuk, akaun, `authorized_keys`, soket pendengaran, perkhidmatan, kerja terjadual, pakej), memasang komit, mengaktifkan firewall hos, memadam dirinya sendiri, menyamarali SSH dan menamatkan sesi. Laporan untuk pelayan sedemikian pada yang terbaik adalah **SELF-ATTESTED**: sesiapa yang menjalankan pemasang sudah mempunyai hak root sebelum itu, dan tiada rekod penyedia tersedia untuk pemeriksa. Ia masih lebih baik daripada pelayan yang tidak dijelaskan: inventori, hash pemasang dan setiap log masuk kemudian disahkan.

## Sahkan

Pemverifikasi memerlukan `deployment.json`, pemasang yang diterbitkan, kelayakan baca sahaja dan, secara idealnya, satu keluaran komit dan bukti ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Setiap penyedia dan nilai Cloudflare diminta oleh pengesah pada masa itu; rekod hanya membekalkan ID yang hendak ditanya. Kod keluar ialah 0 untuk **PASS**, 1 untuk **FAIL** dan 2 untuk **REVIEW**, **INCOMPLETE** atau **SELF-ATTESTED**. `--fingerprint` perlu datang daripada saluran bebas; tanpa itu, kunci hanya dibandingkan dengan rekod pengendali sahaja. `python verify.py` masih mengesahkan bukti itu sendiri,ZIP seperti dalam [Evidence](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/).

Tindakan penyedia diklasifikasikan: penciptaan dan permulaan dalam masa 30 minit selepas penciptaan lulus; konsol, penyelamatan, menetapkan semula kata laluan, bina semula, ISO, imej, snapshot, sandaran, Pengurus Sistem, pautan Instance EC2 dan pembukaan firewall gagal; tindakan kuasa dan apa-apa yang tidak dijangka ditandakan untuk semakan. Tindakan tidak diketahui tidak pernah lulus dengan senyap.

## Laporan untuk penyerahan bukti

`--report report.md` menulis laporan Markdown dan `report.json` di sebelahnya:

1. hasil, cap jejak kunci pengumpul, penyebaran, penyedia, komit, pelayan, tembok api, terowong;
2. setiap semakan dengan status dan sumbernya (API penyedia, API Cloudflare, kenyataan pengumpul, jurnal bukti);
3. log penyedia dengan penilaian setiap tindakan dan, di mana penyedia mencatatnya, pelaku;
4. titik hujung Cloudflare yang menyimpan sambungan terowong, konfigurasi dan log audit;
5. pernyataan pengumpul yang disahkan;
6. apa yang dilaporkan dan apa yang tidak;
7. perintah untuk mereproduksinya, dan SHA-256 setiap fail yang diberikan kepadanya.

Serahkan laporan itu, `report.json`, `deployment.json`, pemasang yang diterbitkan dan bukti ZIP. Sediakan laporan itu awal: log penyedia disimpan untuk tempoh terhad.

## Cloudflare sebagai saksi luar

Semua di sini adalah pilihan. Tanpa akaun Cloudflare, pelayan masih berjalan, dan dua daripadanya berfungsi hari ini:

| Apa | Apa yang dipaparkan | Dalam TgWitness |
| --- | --- | --- |
| Terowong pantas atau terowong domain anda | panel hanya boleh diakses melalui terowong | penolong pemasangan pelayan, lihat di atas |
| drand relay `drand.cloudflare.com` | rekod selepas pusingan drand lebih baru daripadanya: jurnal itu ditulis seiring ia berjalan | mod bukti, **lebih ramai saksi**, tiada akaun ([format](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Notifikasi kesihatan terowong | apabila terowong terhenti, melalui e-mel atau webhook daripada Cloudflare | tetapkan mereka dalam papan pemuka Cloudflare |
| Gateway DNS (`--gateway-dns`, atau **Cloudflare Gateway DNS** dalam wizard) | setiap nama yang disemak oleh pelayan, dijawab oleh Cloudflare melalui TLS; tembok api Hetzner membenarkan DNS mengakses tiada apa-apa lagi; sama ada dasar Gateway boleh menulis semula jawapan | Hetzner, pelan Zero Trust percuma, tiada domain; `verify` memeriksa firewall, lokasi, log, dasar, pertanyaan pelayan dan log audit; mod bukti menyalin log ke dalam jurnal |
| Gateway dengan klien Cloudflare One pada pelayan, firewall keluar yang hanya membenarkan Cloudflare | setiap sambungan yang dibuat oleh pelayan, bukan hanya DNS | belum dibina |
| Akses di hadapan panel | siapa yang log masuk ke panel dan bila | tidak dibina: memerlukan domain anda sendiri |
| Log arahan SSH | setiap arahan dalam sesi debug | belum dibina |

Logpush, yang akan menyimpan salinan Cloudflare sendiri di R2, adalah ciri Enterprise: pada pelan percuma Cloudflare menjawab `logpush is not enabled for this account`. Log Gatewaynya bertahan selama 24 jam di sana, jadi mod bukti menyalinnya ke dalam jurnal yang ditandatangani (**log Gateway Cloudflare bagi pertanyaan DNS pelayan ini**, satu token baca sahaja dengan Akses Baca Analitik Akaun).

Tanpa pelan Zero Trust, akaun mempunyai satu lokasi DNS. Apabila Cloudflare menolak lokasi lain, pelayan berkongsi lokasi sedia ada dan pertanyaannya dibezakan mengikut alamatnya; penapis itu juga memerlukan Zero Trust PII Read, dan `destroy` meninggalkan lokasi kongsi. Satu pertanyaan log merangkumi maksimum tiga jam, jadi salinan dan `verify` membaca hari itu dalam tetingkap tiga jam.

Gateway DNS merangkumi penyelesai sistem. DNS melalui HTTPS pada port 443 ke penyelesai lain, dan sambungan ke alamat yang tidak dicari di mana-mana (contohnya pusat data Telegram), tidak terdapat dalam lognya.

Cloudflare tidak dapat melihat ke dalam penyulitan Telegram, peranti lain pada akaun Telegram (senarai peranti mod bukti merekodkannya dari pihak Telegram) atau hipervisor penyedia.

## Membaca hasil penyebaran

Untuk VM biasa, penyedia mengawal infrastruktur hos, dan inventori tempatan diperiksa bersama rekod penyedia. Untuk Intel TDX, pengesah juga memeriksa petikan perkakasan, pengikatan pengumpul, kompos dan ukuran OS. Baca keputusan individu untuk melihat pemeriksaan yang lulus atau yang tidak tersedia.

Perincian firewall bersejarah bergantung pada penyedia; Linode mengekalkan versi peraturan. [Rekod pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/verification/) menyenaraikan penyebaran yang diuji dan pemeriksaan langsung yang masih aktif, dan [skop pengesahan](https://phishdestroy.github.io/TgWitness/ms/docs/reference/evidence/#verification-scope) menghubungkan pemeriksaan persekitaran ini dengan pemerolehan arkib dan integriti.
