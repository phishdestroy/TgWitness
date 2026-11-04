# Pilih proksi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/proxies/

Pastikan akaun kekal dalam talian, dan tentukan sendiri sama ada ia boleh menunjukkan IP pelayan anda.

## Pilih mod IP terlebih dahulu

01**Sembunyikan alamat**

Proksi sahaja. Jika tiada yang berfungsi, ia menunggu.

02**Direktori sebagai pilihan terakhir**

Bersambung terus selepas tempoh tertangguh, kembali ke proksi sebaik ada yang berfungsi.

03**Pelayan di sebalik terowong atau VPN**

Sambungan terus tidak mengapa. Ia tidak menyediakan atau menyemak VPN untuk anda.

Rute memilih sambungan. Mod IP menentukan sama ada sambungan terus dibenarkan.

## Biarkan kolam mengekalkan laluan

1. **Akaun → Tetapan → Tetapan sambungan**.
2. Pilih mod IP dan **MTProxy Automatik**, atau laluan tetap.
3. Simpan, **Uji sambungan Telegram** (berfungsi sebelum log masuk juga).
4. Mulakan pengumpulan dan hantar mesej ujian kepada diri sendiri.

Ruang kerja baharu bermula dengan MTProxy automatik dan **Sembunyikan alamat**. Kolam menarik empat senarai awam, menyemak pelayan, menyimpan yang baik dan menukar yang mati.

## Gunakan proksi anda sendiri

SOCKS5, HTTP CONNECT, pautan proksi Telegram atau katalog pengendali. Jeda pemerhatian sebelum menukar. Rahsia Fake TLS (`ee`…) tidak berfungsi.

**Tetapan putar, kongsi dan cuba semula**

**Parameter → MTProxy Automatik**: ambang kegagalan, tempoh bertenang, putaran, akaun bagi setiap proksi. Had 1 bermaksud akaun menunggu dan bukannya berkongsi. Proksi berbeza masih boleh berkongsi IP keluar yang sama.

## Memisahkan Telegram daripada permintaan luaran

MTProxy hanya membawa Telegram. Cap masa, pemberitahuan, salinan dan semakan kod melalui proksi SOCKS5/HTTP berasingan, laluan SOCKS5/HTTP akaun, atau terus jika mod membenarkan. Atau matikan sahaja.

`TGWITNESS_PROXY_FEED_PROXY` menetapkan laluan untuk muat turun senarai. [Saksi](https://phishdestroy.github.io/TgWitness/ms/docs/witness/) mempunyai tetapannya sendiri. Semua ini tidak menyentuh pelayar atau rangkaian sistem anda.

Lagi: [mod dan nilai lalai](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes), [siapa yang boleh menukar laluan](https://phishdestroy.github.io/TgWitness/ms/docs/access/).
