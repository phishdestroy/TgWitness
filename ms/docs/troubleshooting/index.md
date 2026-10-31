# Temui apa yang salah

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/troubleshooting/

Mulakan dengan simptom. Periksa satu lapisan pada satu masa.

## Panel meminta token

Gunakan token panel daripada fail tempatan yang dipaparkan oleh pelancar. Untuk Docker, jalankan `docker compose exec tgwitness cat /data/panel-token.txt`. Kod log masuk Telegram, token BotFather dan token saksi baca sahaja mempunyai tujuan yang berbeza.

## Telegram tidak bersambung

Buka tetapan sambungan dan jalankan pemeriksaan sambungan. Jika menggunakan proksi awam, cuba entri lain dan simpan laluan secara eksplisit. Semak jenis proksi dan format rahsia yang disokong. Mengemas kini senarai awam tidak menukar laluan akaun.

## Disambungkan, tetapi tiada mesej baru

1. Periksa bahawa observation sedang berjalan di ruang kerja yang betul.
2. Pastikan sumber telah dipilih dan dapat dilihat oleh akaun tersebut.
3. Hantar mesej baharu unik dalam kumpulan terkawal dan cari teks tepat itu.
4. Semak jurnal operasi untuk gangguan, kerja tertangguh atau ralat Telegram.

Snapshot sejarah dan peristiwa mesej baru adalah berbeza. Sumber senyap boleh disambungkan tanpa menghasilkan mesej baru. Gunakan ujian penghantaran terkawal apabila kesempurnaan menjadi penting.

## FloodWait atau jeda selepas memulakan semula

FloodWait bermaksud Telegram memerlukan jeda. Tunggu tempoh yang dinyatakan dan semak beban kerja pengumpulan; penyambungan semula berulang tidak membatalkan had. Keadaan kemas kini yang disimpan membantu mengejar ketinggalan selepas mula semula, tetapi kemas kini yang telah tamat tempoh dan beberapa tetingkap gangguan kekal sebagai keterbatasan. Catatkan jurang tersebut daripada menganggap jurnal itu lengkap.

## Bot telah dikonfigurasikan tetapi tidak menyiarkan apa-apa

Pastikan proses saksi benar-benar berjalan, bot boleh membuat hantaran di saluran dan saksi dapat mengakses API Pengumpul dan Bot. Periksa jurnalnya untuk penerbitan yang gagal. Hanya tinjauan Pengumpul yang berjaya sahaja tidak mengesahkan hantaran di saluran.

## Di manakah integrasi token GitHub?

**Dirancang.** Extras menerangkan aliran kerja verifikasi fork dan binaan yang dicadangkan. Pada masa ini tiada borang token GitHub atau pengesahan automatik bahawa pemasangan yang sedang berjalan sepadan dengan repositori. Lihat [status ciri semasa](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/).

Apabila melaporkan masalah, sertakan versi, sistem operasi, langkah-langkah dan ralat yang disensor. Pastikan sesi, token, mesej peribadi dan direktori data tidak dimasukkan ke dalam isu awam.
