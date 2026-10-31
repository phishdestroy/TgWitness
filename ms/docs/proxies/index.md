# Pilih proksi

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/proxies/

Pastikan akaun kekal disambungkan. Tetapkan secara eksplisit bila laluannya boleh menggunakan alamat pelayan.

## Pilih mod IP terlebih dahulu

01**Sembunyikan IP**

Gunakan proksi. Apabila tiada yang berfungsi, tunggu tanpa sambungan Telegram terus.

02**Benarkan sandaran**

Benarkan Direct selepas kelewatan yang telah ditetapkan; kembali ke proksi kerja apabila seseorang menjawab.

03**Terowong / VPN**

Benarkan laluan terus melalui rangkaian hos. Pilihan ini tidak memasang atau mengesahkan VPN.

Rute memilih sambungan. Mod IP menentukan sama ada sambungan terus dibenarkan.

## Biarkan kolam mengekalkan laluan

1. Buka **Akaun → Tetapan → Tetapan sambungan**.
2. Pilih mod IP dan **MTProxy Automatik**, atau masukkan laluan tetap.
3. Simpan dan jalankan **ujian sambungan Telegram**. Ia juga berfungsi sebelum log masuk.
4. Selepas memulakan pengumpulan, semak bahawa mesej terkawal sampai ke jurnal.

Ruang kerja baharu menggunakan MTProxy automatik dengan tingkah laku Sembunyikan IP. Kolam gabungan ini menggabungkan empat sumber awam, menyemak kemasukan, mengekalkan laluan aktif dan menggantikan proksi yang gagal. Muat turun yang gagal mengekalkan snapshot sebelumnya.

## Gunakan proksi anda sendiri

Masukkan butiran SOCKS5 atau HTTP CONNECT, tampal pautan proksi Telegram yang disokong, atau sediakan katalog pengendali. Jeda pemantauan sebelum menukar laluan aktif. Rahsia TLS MTProxy palsu yang bermula dengan `ee` tidak disokong.

**Tetapan putar, kongsi dan cuba semula**

Di bawah **Parameter → Automatic MTProxy**, tetapkan ambang kegagalan, tempoh penyejukan, pusing ganti yang dirancang dan akaun setiap proksi. Had perkongsian satu menyebabkan akaun menunggu apabila tiada entri eksklusif tersedia. Jeda penyegaran senarai dan jeda prob diikuti nilai ruang kerja utama. Proksi berasingan tidak menjamin IP keluar yang berasingan.

## Memisahkan Telegram daripada permintaan luaran

MTProxy hanya membawa trafik Telegram. Cap masa, pemberitahuan, salinan dan semakan sumber menggunakan proksi SOCKS5/HTTP berasingan, laluan SOCKS5/HTTP akaun, atau Direct apabila mod IP membenarkannya. Permintaan luaran tersebut boleh dilumpuhkan.

`TGWITNESS_PROXY_FEED_PROXY` yang eksplisit mengkonfigurasi laluan pemuat turun suapan. [Saksi bebas](https://phishdestroy.github.io/TgWitness/ms/docs/witness/) mengekalkan tetapan sendiri. Kawalan ini tidak memasang VPN sistem atau mengalihkan trafik pelayar.

Lihat [semua mod, lalai dan senarai sumber](https://phishdestroy.github.io/TgWitness/ms/docs/reference/connection/#ip-modes), atau [pilih siapa yang boleh menukar laluan akaun](https://phishdestroy.github.io/TgWitness/ms/docs/access/).
