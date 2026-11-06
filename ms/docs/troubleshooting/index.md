# Telegram · Temui apa yang salah

Canonical page: https://phishdestroy.github.io/TgWitness/ms/docs/troubleshooting/

Mulakan dari gejala, semak satu perkara pada satu masa.

## Panel meminta token

Ia mahukan token panel daripada fail yang dicetak pelancar. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Bukan kod Telegram, bukan token bot, bukan token saksi.

## Telegram tidak bersambung

Jalankan semakan sambungan. Pada proksi awam, pilih yang lain dan simpan. Semak jenis proksi dan format rahsia. Menyegar semula senarai tidak menukar laluan dengan sendirinya.

## Disambungkan, tetapi tiada mesej baru

1. Adakah pemerhatian berjalan, dalam ruang kerja yang betul?
2. Adakah sumber dipilih dan kelihatan kepada akaun itu?
3. Hantar mesej unik dalam kumpulan ujian anda dan carinya.
4. Cari gangguan atau ralat Telegram dalam jurnal.

Sembang yang sunyi memang tiada apa yang baharu. Jika kelengkapan penting, jalankan ujian penghantaran terkawal.

## FloodWait atau jeda selepas memulakan semula

FloodWait ialah Telegram berkata "perlahan sikit". Tunggu sehingga ia berlalu dan kurangkan beban, menyambung semula tidak membantu. Selepas mula semula TgWitness mengejar apa yang Telegram masih ada; selebihnya ialah jurang, jadi catatkannya.

## Bot telah dikonfigurasikan tetapi tidak menyiarkan apa-apa

Adakah saksi berjalan, bolehkah bot menyiar dalam saluran, bolehkah ia mencapai pengumpul dan Bot API? Cari hantaran yang gagal dalam jurnalnya. Tinjauan di pihak pengumpul tidak bermaksud hantaran telah keluar.

## Di manakah integrasi token GitHub?

**Dirancang.** Extras menerangkan aliran kerja verifikasi fork dan binaan yang dicadangkan. Pada masa ini tiada borang token GitHub atau pengesahan automatik bahawa pemasangan yang sedang berjalan sepadan dengan repositori. Lihat [status ciri semasa](https://phishdestroy.github.io/TgWitness/ms/docs/reference/features/).

Melaporkan pepijat? Versi, OS, langkah dan ralat yang telah disunting. Jangan sekali-kali letakkan sesi, token, mesej peribadi atau direktori data dalam issue awam.
