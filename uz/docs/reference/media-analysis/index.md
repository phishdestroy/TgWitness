# Mahalliy OCR va transkripsiya

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/media-analysis/

Mahalliy ishchi yordamida ushlangan tasvirlar va audio materiallarni aniqlang; hosil qilingan matnni uning manba fayli bilan bog'lab saqlang.

[Ish jarayoni bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

`media.saved` jurnal yozuvini oching, **Ilovani aniqlashni** tanlang, so'ngra **Arxivdan so'rash** bo'limida OCR yoki transkripsiyani tanlang. Ishlov berish qo'lda va mahalliy tarzda amalga oshiriladi. Bulutli media rejimi yoki avtomatik yuklash mavjud emas. Ilova asl baytlari va `media_sha256` o'zgarmasligicha qoladi; aniqlangan matn aniq mashinaviy tan olish deb belgilangan va manba xesh, dvigatel/model versiyasi, til, parametrlar va yakunlanish vaqti bilan alohida saqlanadi. Transkriptlar qaytarilgan vaqt tamg'alarini saqlab qoladi.

Ushbu natijalarni **matnni avtomatik aniqlash** va OCR/transkript filtri yordamida qidiring. Bu alohida hosil ma'lumotlar bo'yicha qidiruv; u mashinaning aniqlashini sukut bo'yicha asl Telegram matniga aylantirmaydi yoki imzolangan voqealarga qo'shmaydi.

## Ixtiyoriy ishchini sozlang

1-versiya mahalliy Docker daemoniga ega Linux mezbonini talab qiladi. Windowsda TgWitness o'zining mahalliy daemoniga ega Linux VM/WSL muhitida ishlashi mumkin. Panel hech qachon ishonchsiz ilovamani o'zi deksodlamaydi.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Ushbu o'zgaruvchilarni TgWitness xizmat muhitida sozlang va uni qayta ishga tushiring. Daemon soketi standart bo'yicha `/var/run/docker.sock` ga o'rnatiladi; rootless joylashtirishlarda `TGWITNESS_DOCKER_SOCKET` ni belgilash mumkin. Worker masofaviy Docker kontekstiga emas, balki aynan shu Unix soketidan foydalanadi. Docker API ni panel foydalanuvchilariga ochiq qoldirmang yoki uning soketini tanib olish konteyneri ichida montaj qilmang.

Transkripsiya uchun CTranslate2 bilan mos Whisper modelini alohida o'rnating, so'ngra `TGWITNESS_WHISPER_MODEL_DIR` ni uning papkasiga o'rnating. Worker uni `local_files_only=True` bilan yuklaydi; tanlangan model va kirish faqat o'qish uchun o'rnatiladi. Dasturning [model yuklash bo'yicha hujjatlar](https://github.com/SYSTRAN/faster-whisper)ini ko'ring. Taqdim etilgan OCR tasviriga ingliz va rus tillariga o'rgatilgan ma'lumotlar kiritilgan. Zarur bo'lganda tasvirga boshqa tilni ham qo'shing; til kodlari [Tesseract'ning CLI'siga](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html) muvofiq keladi.

Ishlash vaqtida hech qanday model yuklab olinmaydi. Qurish/yuklab olish o'rnatmasi tarmoqni ishlatishi mumkin; har bir haqiqiy tanish konteynerida tarmoq o'chirib qo'yilgan. Ijroni yoqishdan oldin tasvirni o'rnating; ijro vaqti`--pull=never`dan foydalanadi.

## Chegaralar va tiklash

Kontener imtiyozsiz foydalanuvchi sifatida, faqat o'qish uchun root huquqi bilan, imtiyozlari cheklangan (`no-new-privileges` ), bitta CPU, 2 GiB xotira, PID chegarasi va chegaralangan vaqtinchalik fayl tizimi bilan ishga tushadi. Faqat tanlangan faylning tasdiqlangan nusxasi va ixtiyoriy model papkasi ulanadi. Yig'uvchining ma'lumotlar bazasi, ombori va sessiyasi yuklanmaydi. [Docker ijro etish vaqti bayroqlari](https://docs.docker.com/reference/cli/docker/container/run/) ushbu cheklovlarni majbur qiladi; bu konteyner chegarasi bo'lib qoladi, apparat enklyavi emas.

Fayllar 50 MiB, rasmlar 20 million piksel, audio ma'lum davomiylikda 30 daqiqa va qayta ishlash 5 daqiqagacha cheklangan. Bir vaqtning o'zida bitta ishchi ishlaydi, har bir ish maydoni uchun maksimal 20 ta navbatga qo'yilgan/ijro etilayotgan ish va 100 ta saqlangan ish mavjud. Bekor qilish konteynerni to'xtatadi; qayta urinish oldingi urinishga bog'langan yangi ish yaratadi. To'xtatilgan ishlar qayta ishga tushirilgandan keyin belgilab qo'yiladi. Modeli sozlangan chegaralarga mos kelmasa, ishlov berish muvaffaqiyatsiz bo'lishi mumkin; u izolyatsiyasiz jimjit ishlayvermaydi.
