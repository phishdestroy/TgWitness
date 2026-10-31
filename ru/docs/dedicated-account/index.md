# Используйте отдельный аккаунт. Никогда не основной.

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/dedicated-account/

Прочитайте до того, как подключать аккаунт

Наш совет не использовать основной аккаунт — не шутка, а реальность.

Основной аккаунт

- Свой app hash = 99% разлогин аккаунта
- Блокировки просто из-за нетраста аккаунта — частые
- Использовать свой аккаунт — очень идиотская идея

Доп. аккаунт на публичных парах app hash/app ID

- Через эти пары зарегистрировано более миллиона аккаунтов
- Эти пары живут 5+ лет точно
- Через них никто не сможет увидеть ничего вашего

01

## Почему не основной аккаунт

Это точная информация. Мы точно знаем подводные камни этих проблем.

1. ### Свой app hash = 99% разлогин аккаунта

   Вход на my.telegram.org с аккаунта, к которому у вас нет доступа, для получения app hash, а потом любой запрос через этот app hash = 99% разлогин аккаунта. Можете проверить.
2. ### Блокировки просто из-за нетраста аккаунта — частые

   Блокировки просто из-за нетраста аккаунта случаются часто — можете проверить. Но использовать свой аккаунт — очень идиотская идея.
3. ### Скопированные сессионные ключи могут быть отозваны

   Одновременный запуск импортированного ключа TData/сеанса в Telegram Desktop и TgWitness может вызвать ошибку `AUTH_KEY_DUPLICATED`. Telegram аннулирует данную авторизацию, поэтому обе копии потребуют нового входа в систему. Наличие отдельной учетной записи не предотвращает эту ситуацию.

   Полностью закройте исходный клиент и держите его закрытым во время использования импортированной сессии. Для параллельного использования войдите в TgWitness с помощью телефона или QR-кода, чтобы создать отдельную авторизацию; другие клиенты с отдельной авторизацией могут оставаться авторизованными.

   [Ознакомьтесь с предупреждением об импорте сеанса](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ru#session-warning)

Документация Telegram

- [Ошибки разлогина: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Свой app hash: получение api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Почему TgWitness работает через публичные пары app hash/app ID

Поэтому мы сделали реализацию через публичные пары app hash/app ID. По нашей логике, баны там менее вероятны: через эти пары зарегистрировали более миллиона аккаунтов Telegram и через них работает много разных программ. По нашей логике, это оптимальнее, чем прямое взаимодействие с личным app hash: эти пары живут 5+ лет точно.

### Своя новая пара

Создаётся на my.telegram.org с этого же аккаунта.

- Около 99% аккаунтов — разлогин
- Одно новое приложение, один аккаунт

### Публичные пары из пула

Те же пары, через которые работают многие программы.

- Более миллиона зарегистрированных аккаунтов
- Много разных программ
- Живут 5+ лет

### Почему через эти пары никто не сможет увидеть ничего вашего

- #### Пара — это имя приложения, а не ключ

  Telegram запрашивает API ID и API hash, когда программа подключается и когда запрашивает код входа. Они указывают на приложение и не дают доступа ни к какому аккаунту; в документации Telethon отмечено, что одна пара работает с любым номером телефона.
- #### Ваш сессионный ключ никогда не покидает ваш сервер

  При входе ваш TgWitness и Telegram создают ключ авторизации обменом Диффи–Хеллмана; сам ключ никогда не передаётся. Документация Telegram: после авторизации ключ привязывается к пользователю, и каждый вызов с этим ключом выполняется от имени этого пользователя. У других программ с той же парой — свои ключи, ваш они использовать не могут.
- #### Трафик шифруется вашим ключом

  Каждый запрос и ответ шифруется ключом авторизации сессии, а не API hash. Знание API hash ничего не расшифровывает.
- #### Владелец пары ничего не видит

  В Telegram нет метода, который выдаёт аккаунты, сессии или сообщения по API ID. Владелец пары видит только настройки своего приложения на my.telegram.org.
- #### Какое это приложение, видит только ваш аккаунт

  В «Настройки» → «Устройства» вашего аккаунта для каждой сессии видны название приложения и API ID, устройство, IP-адрес и даты. Больше этот список не видит никто.

Документация Telegram

- [Авторизация пользователей: ключ привязывается к пользователю](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Создание ключа авторизации](https://core.telegram.org/mtproto/auth_key)
- [Шифрование MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Что хранит запись о сессии](https://core.telegram.org/constructor/authorization)
- [Получение api_id](https://core.telegram.org/api/obtaining_api_id)
- [Открытый исходный код приложений Telegram](https://telegram.org/apps#source-code)

Библиотеки и обсуждения

- [Telethon: вход](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: API официальных приложений](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: нужно ли держать api_hash в секрете?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Те же пары в других программах 7

Пары официальных приложений Telegram публичны и встроены во многие независимые программы и библиотеки:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Список официальных пар на форуме, опубликован для регистрации аккаунтов

03

## Способы создать доп. аккаунт

Для аккаунта Telegram нужен номер телефона, на который придёт код входа. Выбирайте по тому, сколько должен прожить аккаунт.

- Лучший выбор

  ### Предоплаченная SIM или eSIM

  ********

  Живёт

  Пока вы пополняете баланс

  Учтите

  Самый надёжный вариант: реальные мобильные номера Telegram принимает лучше всего. Номер, который оператор забрал, достаётся другому человеку.
- ### Приложение виртуальных номеров

  ********

  Живёт

  Пока приложение не забрало номер

  Учтите

  Telegram может не принять виртуальный номер, не прислать код или сразу ограничить новый аккаунт; некоторые приложения забирают неиспользуемые номера.
- ### Аренда номера

  ********

  Живёт

  Срок аренды

  Учтите

  Когда аренда закончится, номер получит следующий клиент.
- ### Разовая активация

  ********

  Живёт

  Один код

  Учтите

  Номер сразу возвращается в пул, часто с историей прошлых владельцев. Первым делом поставьте облачный пароль.

Тот, к кому номер попадёт потом, сможет запросить код входа. Облачный пароль (двухэтапная аутентификация) не даст ему войти; без пароля аккаунт достанется следующему владельцу номера.

Документация Telegram

- [FAQ о спаме: виртуальные номера и прошлые владельцы](https://telegram.org/faq_spam)
- [Двухэтапная проверка](https://core.telegram.org/api/srp)

### Аренда номеров +888 (Fragment)

Некоторые маркеты и сервисы предлагают временную аренду официальных номеров Telegram +888 с Fragment.

Примерная цена — около 20 долларов США в день.

- Зарегистрировать аккаунт можно прямо в Telegram Web или Telegram Desktop.
- На одном номере можно удалять аккаунты и создавать новые.
- Антифрод-проверок в целом меньше, но это не даёт неуязвимости или особых преимуществ.

Номер вам не принадлежит. После окончания аренды владелец может вернуть его себе. Сразу установите облачный пароль и не рассчитывайте на долгосрочное использование аккаунта.

Собственный номер +888 или предоплаченная SIM-карта под вашим контролем остаются более надёжным вариантом.

### Готовые аккаунты с торговых площадок

На некоторых маркетплейсах, например G2G и Z2U, продаются готовые аккаунты Telegram — новые, с возрастом или с файлами сессий.

- [G2G: списки аккаунтов Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: списки аккаунтов Telegram](https://www.z2u.com/telegram/accounts-5-15140)

НИ В КОЕМ СЛУЧАЕ НЕ ИСПОЛЬЗУЙТЕ СВОЙ ОСНОВНОЙ АККАУНТ! Отдельный аккаунт, полученный таким способом, всё равно безопаснее, чем подключение вашего основного аккаунта Telegram к TgWitness.

#### Предупреждения перед покупкой

- Это нарушает условия использования Telegram (ToS).
- Многие аккаунты зарегистрированы массово (авторег) или имеют неизвестную историю.
- У продавца может сохраниться доступ к восстановлению аккаунта.
- Аккаунты с таких площадок впоследствии часто блокируются или получают ограничения.
- Избегайте площадок, которые открыто продают стилеры, фишинговые инструменты или явно украденные аккаунты.
- Покупка аккаунта, даже заявленного как авторег, на платформах, которые открыто продают фишинговые инструменты, стилеры, украденные сессии или аккаунты, нарушает не только ToS Telegram, но и законы большинства стран. Впоследствии это может уничтожить ваши улики. Внимательно подойдите к этому вопросу.

#### Если вы выбрали этот вариант

1. Считайте такой аккаунт одноразовым.
2. Завершите все остальные сессии, сразу установите облачный пароль и смените способы восстановления.
3. Используйте 2–3 аккаунта от разных поставщиков или аккаунты, которые зарегистрировали лично.

**Premium, удаление и задержка в семь дней**

Если на аккаунте есть Premium, человек с доступом к номеру телефона не сможет удалить аккаунт моментально. Вам придёт уведомление, и до удаления будет семь дней.

Это важно: ваше расследование зависит от аккаунта, и у вас будет время подготовить новый.

**Новые аккаунты и учетные данные API**

Если вы получите и начнёте использовать собственные api_id/api_hash на свежем аккаунте, который лично зарегистрировали на номер из SMS-сервиса, аккаунт разлогинит при первом же запросе к API или авторизации сессии. Учитывайте это при планировании расследования.

04

## Создание аккаунта

От номера до первого записанного чата.

1. ### Получите номер

   Предоплаченная SIM или eSIM — если аккаунт должен жить долго; аренда или разовая активация — для короткой задачи. Сервисы перечислены ниже.
2. ### Регистрируйте отдельно от основного аккаунта

   Регистрируйтесь в официальном приложении Telegram на отдельном устройстве, в эмуляторе или в отдельном профиле телефона — не рядом с основным аккаунтом.
3. ### Закройте облачным паролем

   Сразу поставьте облачный пароль и почту для восстановления, которые больше нигде не используются.
4. ### Закройте настройки конфиденциальности

   Номер телефона — **Никто**, поиск по номеру — **Мои контакты**, последняя активность, фото профиля и «О себе» — **Никто** или **Мои контакты**; синхронизацию контактов выключите.
5. ### Не дайте ему самоудалиться

   Поставьте самый долгий срок самоудаления аккаунта, чтобы остановка TgWitness не стоила вам аккаунта.
6. ### Нейтральный профиль

   Никаких имён, фото, юзернеймов и описаний из других ваших аккаунтов, никаких личных контактов.
7. ### Дайте ему прогреться

   Сначала вступайте в несколько чатов в день. Новые аккаунты, которые торопятся, первыми получают ограничения.
8. ### Ничего не давайте ботам

   Никогда не нажимайте «Поделиться номером» или «Поделиться геопозицией» для бота. Ссылки и мини-приложения открывайте через VPN или прокси на этом устройстве.
9. ### Подключите его к TgWitness

   В отдельном рабочем пространстве подключите его через **«Аккаунт» → «QR-код»**, затем нажмите **«Источники» → «Режим расследования»**. Действуете вы в приложении, TgWitness ведёт запись.

Документация Telegram

- [Двухэтапная проверка](https://core.telegram.org/api/srp)
- [Настройки конфиденциальности](https://core.telegram.org/api/privacy)
- [Самоудаление аккаунта](https://core.telegram.org/method/account.setAccountTTL)

05

## Сервисы номеров

С чего начать. Страны, цены и то, принимает ли Telegram номер, часто меняются — проверяйте перед оплатой.

### Предоплаченные SIM и eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Предоплата

  Тариф PayGo, очень дёшево
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Предоплата
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Предоплата
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Предоплата
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Приложения виртуальных номеров 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Только США; для регистрации нужен номер США
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Номер забирают, если им не пользоваться
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Другие страны
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - Платно

  С пробным периодом
- [Hushedhushed.com](https://hushed.com)

  - Много стран
  - Платно

  Дёшево
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Европейские мобильные номера в приложении
- [Sonetelsonetel.com](https://sonetel.com)

  - Много стран
  - Бесплатный номер
- [Zadarmazadarma.com](https://zadarma.com)

  - Много стран

  Виртуальные номера

### Аренда номеров и активации 12

Аренда держит номер за вами недели или месяцы. Разовая активация даёт один код: поставьте облачный пароль сразу после регистрации.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Аренда
  - Активации
- [SMSPVAsmspva.com](https://smspva.com)

  - Аренда
  - Активации
- [5SIM5sim.net](https://5sim.net)

  - Аренда
  - Активации
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Аренда
  - Разовые
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Аренда
  - Активации
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Аренда
  - Активации
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Аренда
  - Активации
- [365SMS365sms.org](https://365sms.org)

  - Аренда
  - Активации
- [SIMSMSsimsms.org](https://simsms.org)

  - Аренда
  - Активации
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Разовые
- [SMS-MANsms-man.com](https://sms-man.com)

  - Разовые
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Разовые
