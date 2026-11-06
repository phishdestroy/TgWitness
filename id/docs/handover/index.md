# Siapkan salinan untuk dibagikan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/handover/

Bagikan hanya yang perlu, berkas asli tetap utuh.

Serah terima adalah ekstrak bertanda tangan terpisah: pilih obrolan dan orang, sembunyikan identitas atau teks, tentukan berkas dan catatan tim yang ikut. Manifes mencatat apa yang dipertahankan, diringkas, dan dikeluarkan.

## Siapkan ekstrak untuk penerima

1. **Ekspor → Ekstrak serah terima**: tulis tujuannya, pilih obrolan dan periode, lalu **Muat orang dari obrolan pilihan** jika Anda butuh orang bernama.
2. Semua orang lain: nama samaran, dikeluarkan, atau sesuai rekaman. Teks dan berkas adalah sakelar terpisah; telepon dan email bisa disamarkan.
3. Case Board: tidak ada, penanda dan potongan, atau kartu dengan komentar. Nama tim bisa diganti alias.
4. **Unduh ekstrak serah terima**, buka, verifikasi, dan periksa sebelum dikirim.

### Satu salinan asli, satu salinan untuk dibagikan

Contoh sintetis · hanya untuk ilustrasi identitas

1. **Pilih.** Sertakan obrolan kasus dan identifikasi orang yang menjadi subjek cuplikan tersebut.
2. **Minimalkan.** Pilih bagaimana peserta lain ditampilkan dalam salinan yang dibagikan.
3. **Periksa.** Buka laporan dan catatan dari arsip yang dihasilkan sebelum mengirimkannya.
4. **Bagikan.** Kirimkan salinan yang telah diperiksa dan sampaikan sidik jari tepercaya-nya secara terpisah.

#### Pengamatan asli

Nora · pengguna 71002

“Saya telah menerima tautan yang telah direvisi.”

Jurnal sumber menyimpan pengamatan yang disimpan ini.

#### Salinan untuk Penerima

Tampilkan sesuai catatan: Nora · pengguna 71002 · “Saya telah menerima tautan yang telah direvisi.”

Nama samaran: P01 · “Saya telah menerima tautan yang telah direvisi.”

Hapus: pesan peserta ini tidak dimasukkan ke dalam teks.

#### Periksa berkas-berkas yang sebenarnya

Baca file report.html dan records.jsonl.

Periksa identitas, teks, lampiran, dan komentar tim (jika ada).

#### Kutipan yang ditandatangani

Pemilihan + hash file + manifest yang ditandatangani

Sebuah paket terpisah yang terhubung dengan batas jurnal sumbernya

## Gunakan kontrol-kontrol tersebut secara bersamaan

| Kontrol | Dampak terhadap teks |
| --- | --- |
| Orang | Orang yang dipilih tetap bernama; yang lain mendapat nama samaran atau dikeluarkan. |
| Teks | Semua teks, hanya teks orang yang dipilih dan akun Anda, atau tidak ada. |
| Berkas | Berkas orang yang dipilih dan akun Anda, semua berkas yang ditampilkan, atau tidak ada. |
| Papan Kasus | Tidak ada, penanda dan potongan, atau kartu dengan diskusi. |

Baca juga teks dan berkasnya: nama samaran tidak menghapus nama yang tertulis di dalam pesan atau lampiran. Jika berkas yang dipilih hilang, pulihkan atau keluarkan lampirannya.

## Pastikan teks dapat diverifikasi secara independen

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan sendiri arsip asli dan checkpoint-nya. Penerima bisa memverifikasi salinannya tanpa menerima seluruh ruang kerja. Desain: [Report studio](https://phishdestroy.github.io/TgWitness/id/docs/reports/). Rujukan tepercaya: [verifikasi ekspor](https://phishdestroy.github.io/TgWitness/id/docs/exports/).
