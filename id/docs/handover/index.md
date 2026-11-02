# Siapkan salinan untuk dibagikan

Canonical page: https://phishdestroy.github.io/TgWitness/id/docs/handover/

Bagikan pengamatan yang relevan sambil menjaga ruang kerja asli tetap utuh.

Serah terima adalah ekstrak terpisah yang telah ditandatangani. Pilih obrolan dan orang-orang yang relevan, kurangi identitas atau teks, dan tentukan file serta catatan tim mana yang harus dimasukkan ke dalam salinan penerima. Manifesnya mencatat pilihan tersebut serta jumlah catatan yang tidak diubah, dipersingkat, dan dihilangkan.

## Siapkan ekstrak untuk penerima

1. Buka **Ekspor → Ekstrak Serah Terima**. Tulis tujuannya, pilih obrolan dan periode UTC (opsional), lalu pilih "**Muat orang-orang dari obrolan yang dipilih"** jika Anda memerlukan subjek yang disebutkan namanya.
2. Pilih cara menangani pengguna lain: gunakan nama samaran, hilangkan pesan mereka, atau tampilkan sebagaimana tercatat. Atur teks pesan dan lampiran secara terpisah; secara opsional, sembunyikan nomor telepon dan alamat email.
3. Pilih apakah akan menyertakan bookmark dan potongan Case Board, atau kartu dengan komentar. Alias penyelidik dapat menggantikan nama tim dalam teks ini.
4. Pilih **"Unduh Ekstrak Serah Terima**". Buka laporan yang dihasilkan dan catatan yang dipilih secara lokal, verifikasi arsip, dan periksa salinannya sebelum mengirimkannya.

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
| Orang | Pastikan subjek yang dipilih tetap dapat diidentifikasi; gunakan nama samaran atau hilangkan peserta lain sesuai pilihan. |
| Teks | Sertakan semua teks, hanya teks dari orang-orang yang dipilih dan akun pengamat, atau hilangkan teks pesan beserta bidang detail yang berisi teks tersebut. |
| Berkas | Pilih berkas dari orang-orang yang dipilih dan akun yang diawasi, semua berkas pesan yang ditampilkan, atau tidak ada berkas. |
| Case Board | Pilih opsi tanpa materi papan, penanda, dan potongan, atau kartu dengan diskusi tim. |

Periksa teks bebas dan isi berkas serta identitas: nama samaran tidak secara otomatis menghapus setiap nama yang tertulis dalam pesan atau lampiran. Jika berkas yang dipilih dan telah diarsipkan tidak tersedia, pulihkan berkas tersebut atau hilangkan lampiran secara eksplisit sebelum menghasilkan ekstrak.

## Pastikan teks dapat diverifikasi secara independen

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Simpan arsip bukti asli yang telah ditandatangani dan titik pemeriksaan secara terpisah. Proses penyerahan mencatat proyeksinya sendiri, sehingga penerima dapat memeriksa salinan yang dikirimkan tanpa perlu menerima seluruh ruang kerja. [Studio Laporan](https://phishdestroy.github.io/TgWitness/id/docs/reports/) menyediakan desain pembacaannya; [verifikasi ekspor](https://phishdestroy.github.io/TgWitness/id/docs/exports/) menjelaskan referensi tepercaya.
