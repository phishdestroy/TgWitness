# Należy korzystać z oddzielnego konta. Nigdy nie należy używać konta głównego.

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/dedicated-account/

Proszę zapoznać się z poniższymi informacjami przed połączeniem konta

Nasza rada, aby nie korzystać z Państwa głównego konta, nie jest żartem. To rzeczywistość.

Konto główne

- Hash Państwa aplikacji: 99% wylogowanych
- Często dochodzi do blokad wyłącznie z powodu niskiego poziomu zaufania
- Korzystanie z tego rozwiązania jest naprawdę głupim pomysłem

Dodatkowe konto w parach publicznych

- Ponad milion kont zarejestrowanych za pośrednictwem tych par
- Pary te funkcjonują od ponad 5 lat
- Nikt nie może za ich pośrednictwem uzyskać dostępu do Państwa danych

01

## Dlaczego nie Państwa główne konto?

Są to dokładne informacje. Wiemy dokładnie, gdzie leżą pułapki związane z tymi problemami.

1. ### Hash Państwa aplikacji: 99% wylogowanych

   Zalogowanie się na stronie my.telegram.org z konta, do którego nie ma Pan/Pani dostępu, w celu uzyskania skrótu aplikacji, a następnie wysłanie jakiegokolwiek żądania za pomocą tego skrótu oznacza 99-procentowe prawdopodobieństwo, że konto zostało wylogowane. Może Pan/Pani to sprawdzić.
2. ### Często dochodzi do blokad wyłącznie z powodu niskiego poziomu zaufania

   Konta są blokowane wyłącznie dlatego, że Telegram im nie ufa, a takie blokady są częste. Można to również sprawdzić. Korzystanie z własnego konta jest naprawdę głupim pomysłem.
3. ### Skopiowane klucze sesji mogą zostać unieważnione

   Jednoczesne uruchomienie zaimportowanego klucza TData/session w aplikacjach Telegram Desktop i TgWitness może spowodować wygenerowanie komunikatu `AUTH_KEY_DUPLICATED`. Telegram unieważnia tę autoryzację, więc obie kopie wymagają ponownego zalogowania. Posiadanie dedykowanego konta nie zapobiega tej sytuacji.

   Należy całkowicie zamknąć oryginalną aplikację i pozostawić ją zamkniętą podczas korzystania z zaimportowanej sesji. W celu równoległego korzystania należy zalogować się do TgWitness za pomocą telefonu lub kodu QR, aby utworzyć oddzielne upoważnienie; inne oddzielnie autoryzowane aplikacje mogą pozostać zalogowane.

   [Proszę zapoznać się z ostrzeżeniem dotyczącym importu sesji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl#session-warning)

Dokumentacja serwisu Telegram

- [Błędy wylogowania: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Tworzenie własnego skrótu aplikacji: uzyskanie identyfikatora api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Dlaczego TgWitness działa w oparciu o publiczne pary skrótów aplikacji i identyfikatorów aplikacji

Właśnie dlatego stworzyliśmy TgWitness w oparciu o publiczne pary skrótów aplikacji i identyfikatorów aplikacji. Zgodnie z naszą logiką ryzyko zablokowania jest w tym przypadku mniejsze: za pośrednictwem tych par zarejestrowano ponad milion kont Telegram, a wiele różnych programów korzysta z nich. Zgodnie z naszą logiką jest to lepsze rozwiązanie niż bezpośrednia praca z osobistym skrótem aplikacji: pary te z pewnością funkcjonują już od ponad 5 lat.

### Państwa własna nowa para

Utworzono na stronie my.telegram.org z poziomu konta.

- Około 99% kont zostało wylogowanych
- Jedna nowa aplikacja, jedno konto

### Pary publiczne z puli

Te same pary, z których korzysta wiele programów.

- Zarejestrowano ponad milion kont
- Wiele różnych programów
- Ponad 5 lat doświadczenia

### Dlaczego nikt nie może zobaczyć Państwa danych za pośrednictwem tych par

- #### Para ta stanowi nazwę, a nie klucz

  Telegram prosi o podanie identyfikatora API oraz skrótu API, gdy program nawiązuje połączenie oraz gdy żąda kodu logowania. Dane te identyfikują aplikację i nie zapewniają dostępu do żadnego konta; dokumentacja Telethon wskazuje, że jedna para danych działa z dowolnym numerem telefonu.
- #### Pański klucz sesji nigdy nie opuszcza Pańskiego serwera

  Zalogowanie się powoduje utworzenie klucza autoryzacyjnego w wyniku wymiany Diffie–Hellmana między Państwa TgWitness a Telegramem; sam klucz nigdy nie jest wysyłany. Dokumentacja Telegramu: po autoryzacji klucz zostaje powiązany z użytkownikiem, a każde wywołanie przy użyciu tego klucza odbywa się w imieniu tego użytkownika. Inne programy korzystające z tej samej pary kluczy posiadają własne klucze i nie mogą korzystać z Państwa klucza.
- #### Ruch jest szyfrowany za pomocą Państwa klucza

  Każde żądanie i odpowiedź są szyfrowane za pomocą klucza autoryzacyjnego sesji, a nie za pomocą skrótu API. Znajomość skrótu API nie pozwala na odszyfrowanie żadnych danych.
- #### Właściciel pary nie widzi niczego

  Telegram nie udostępnia funkcji umożliwiającej wyświetlenie listy kont, sesji lub wiadomości według identyfikatora API. Właściciel pary widzi jedynie ustawienia swojej aplikacji na stronie my.telegram.org.
- #### Tylko Państwa konto widzi, o jaką aplikację chodzi

  W sekcji Ustawienia → Urządzenia na Państwa koncie wyświetlana jest lista zawierająca nazwę aplikacji i identyfikator API każdej sesji, urządzenie, adres IP oraz daty. Nikt inny nie ma dostępu do tej listy.

Dokumentacja serwisu Telegram

- [Autoryzacja użytkownika: kluczem staje się użytkownik](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Tworzenie klucza autoryzacyjnego](https://core.telegram.org/mtproto/auth_key)
- [Szyfrowanie MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Co zawiera zapis sesji](https://core.telegram.org/constructor/authorization)
- [Uzyskiwanie identyfikatora api_id](https://core.telegram.org/api/obtaining_api_id)
- [Kod źródłowy aplikacji Telegram](https://telegram.org/apps#source-code)

Biblioteki i dyskusje

- [Telethon: logowanie](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: oficjalne interfejsy API aplikacji](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: czy wartość api_hash powinna pozostać tajna?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Te same pary w innych programach7

Pary oficjalnych aplikacji Telegram są publicznie dostępne i wbudowane w wiele niezależnych programów oraz bibliotek:

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

  Lista oficjalnych par aplikacji na forum, opublikowana w celu rejestracji kont

03

## Sposoby utworzenia dodatkowego konta

Konto w serwisie Telegram wymaga podania numeru telefonu, na który zostanie wysłany kod logowania. Wybór należy dokonać w zależności od tego, jak długo konto ma funkcjonować.

- Najlepszy wybór

  ### Karta SIM typu prepaid lub eSIM

  ********

  Ostatnie zmiany

  O ile tylko zadba Pan o jego uzupełnienie

  Proszę zachować ostrożność

  Najbardziej niezawodne rozwiązanie: Telegram najlepiej akceptuje prawdziwe numery telefonów komórkowych. Numer odebrany przez operatora trafia do kogoś innego.
- ### Aplikacja do obsługi numerów wirtualnych

  ********

  Ostatnie zmiany

  Chociaż aplikacja zachowuje liczbę

  Proszę zachować ostrożność

  Telegram może odmówić przyznania numeru wirtualnego, nie dostarczyć kodu lub od razu nałożyć ograniczenia na nowe konto; niektóre aplikacje odbierają numery, które nie są używane.
- ### Wynajem numerów

  ********

  Ostatnie zmiany

  Okres wynajmu

  Proszę zachować ostrożność

  Po zakończeniu numer przechodzi do kolejnego klienta.
- ### Jednorazowa aktywacja

  ********

  Ostatnie zmiany

  Jeden kod

  Proszę zachować ostrożność

  Numer natychmiast wraca do puli, często wraz z historią poprzednich właścicieli. Proszę przede wszystkim ustawić hasło do chmury.

Ktokolwiek będzie później posiadał ten numer, może poprosić o kod logowania. Hasło w chmurze (weryfikacja dwuetapowa) uniemożliwia mu zalogowanie się; bez niego konto należy do kolejnego właściciela tego numeru.

Dokumentacja serwisu Telegram

- [Często zadawane pytania dotyczące spamu: numery wirtualne i poprzedni właściciele](https://telegram.org/faq_spam)
- [Weryfikacja dwuetapowa](https://core.telegram.org/api/srp)

### Wynajęte numery +888 (Fragment)

Niektóre platformy handlowe i serwisy oferują tymczasowy wynajem oficjalnych numerów +888 serwisu Telegram za pośrednictwem Fragment.

Orientacyjna cena: 20 USD dziennie.

- Można zarejestrować konto bezpośrednio w Telegram Web lub Telegram Desktop.
- Można usunąć konta powiązane z danym numerem i utworzyć nowe.
- Konta te zazwyczaj podlegają mniejszej liczbie kontroli antyoszustwowych, jednak nie zapewniają one immunitetu ani specjalnych przywilejów.

Ten numer nie należy do Państwa. Po zakończeniu okresu wynajmu właściciel może go odzyskać. Proszę niezwłocznie ustawić hasło w chmurze i nie traktować tego konta jako długoterminowego.

Posiadanie numeru +888 na własność lub korzystanie z karty SIM typu prepaid, nad którą sprawują Państwo kontrolę, pozostaje rozwiązaniem bardziej niezawodnym.

### Gotowe konta z platform handlowych

Niektóre platformy handlowe (na przykład G2G lub Z2U) oferują gotowe konta w aplikacji Telegram — nowe, z historią aktywności lub wraz z plikami sesji.

- [G2G: Oferty sprzedaży kont Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Oferty sprzedaży kont Telegram](https://www.z2u.com/telegram/accounts-5-15140)

NIGDY NIE KORZYSTAJ Z PAŃSTWA GŁÓWNEGO KONTA! Konto dedykowane, utworzone w ten sposób, jest nadal bezpieczniejsze niż podanie Państwa głównego konta w Telegramie w aplikacji TgWitness.

#### Ostrzeżenia przed zakupem

- Stanowi to naruszenie Warunków korzystania z usługi Telegram.
- Wiele kont zostało zarejestrowanych masowo (automatyczna rejestracja) lub ma nieznaną historię.
- Niektórzy sprzedawcy mogą nadal posiadać dostęp do funkcji odzyskiwania.
- Konta z takich rynków są często później blokowane lub poddawane ograniczeniom.
- Należy unikać platform handlowych, które otwarcie sprzedają oprogramowanie służące do kradzieży danych, narzędzia do phishingu lub konta, co do których nie ma wątpliwości, że zostały skradzione.
- Zakup konta — nawet takiego, które jest reklamowane jako „auto-reg” — na platformach otwarcie sprzedających narzędzia phishingowe, programy do kradzieży danych, skradzione sesje lub konta stanowi naruszenie nie tylko Warunków korzystania z usługi Telegram, ale także przepisów prawnych obowiązujących w większości krajów. Może to w przyszłości spowodować unieważnienie Państwa dowodów. Proszę dokonywać wyboru rozważnie.

#### Jeśli skorzystają Państwo z tej opcji

1. Proszę traktować to konto jako jednorazowe.
2. Należy natychmiast zakończyć wszystkie pozostałe sesje, ustawić hasło w chmurze oraz zmienić metody odzyskiwania dostępu.
3. Proszę skorzystać z 2–3 kont pochodzących od różnych dostawców lub kont zarejestrowanych samodzielnie.

**Usługa Premium, usunięcie konta i siedmiodniowe opóźnienie**

Jeśli konto posiada subskrypcję Premium, osoba mająca dostęp do numeru telefonu nie może natychmiast usunąć konta. Otrzymają Państwo powiadomienie i mają Państwo siedem dni na podjęcie działań przed usunięciem konta.

Ma to znaczenie, ponieważ Państwa dochodzenie zależy od tego konta: mają Państwo czas na przygotowanie zamiennika.

**Nowe konta i dane uwierzytelniające API**

Jeśli uzyska Pan/Pani i wykorzysta własny identyfikator api_id/api_hash z nowego konta, które zarejestrował Pan/Pani samodzielnie przy użyciu numeru z usługi SMS, konto zostanie wylogowane przy pierwszym żądaniu API lub autoryzacji sesji. Proszę o tym pamiętać podczas planowania dochodzenia.

04

## Tworzenie konta

Od numeru do pierwszej zarejestrowanej rozmowy.

1. ### Uzyskaj numer

   Karta SIM typu prepaid lub eSIM, gdy konto ma funkcjonować przez dłuższy czas; karta wypożyczona lub aktywowana jednorazowo w przypadku krótkotrwałego zadania. Usługi wymieniono poniżej.
2. ### Zarejestruj się oddzielnie od swojego głównego konta

   Zarejestruj się w oficjalnej aplikacji Telegram na oddzielnym urządzeniu, emulatorze lub profilu telefonicznym, a nie obok swojego głównego konta.
3. ### Zabezpiecz go hasłem do chmury

   Proszę niezwłocznie ustawić hasło do usługi w chmurze oraz adres e-mail do odzyskiwania dostępu, które nie są używane nigdzie indziej.
4. ### Zamknij ustawienia prywatności

   Numer telefonu **„Nikt”**, „Znajdź mnie po numerze”, **„Moje kontakty**”, „Ostatnio widziany”, „Zdjęcia profilowe” i „Biografia” – **„Nikt”** lub **„Moje kontakty”**; wyłącz synchronizację kontaktów.
5. ### Zapobiegaj samozniszczeniu

   Ustaw proszę funkcję samozniszczenia konta na najdłuższy możliwy okres, tak aby zatrzymanie działania TgWitness nie spowodowało utraty konta.
6. ### Należy nadać mu neutralny profil

   Nie należy podawać imienia i nazwiska, zdjęcia, nazwy użytkownika ani biografii z Państwa innych kont, ani też danych kontaktowych osób prywatnych.
7. ### Proszę poczekać na uruchomienie

   Na początku dołączaj do kilku czatów dziennie. Nowe konta, które działają zbyt pochopnie, są jako pierwsze objęte ograniczeniami.
8. ### Nie udostępniajcie żadnych informacji botom

   Nigdy nie należy naciskać opcji „Udostępnij numer telefonu” ani „Udostępnij lokalizację” w przypadku bota. Linki i mini-aplikacje należy otwierać za pośrednictwem sieci VPN lub serwera proxy na danym urządzeniu.
9. ### Proszę połączyć to z TgWitness

   W swoim obszarze roboczym przejdź do sekcji „**Konto → Kod QR**”, a następnie wybierz opcję „**Źródła → Tryb dochodzeniowy**”. Aplikacja służy do wykonywania czynności, natomiast TgWitness stanowi rejestr tych działań.

Dokumentacja serwisu Telegram

- [Weryfikacja dwuetapowa](https://core.telegram.org/api/srp)
- [Ustawienia prywatności](https://core.telegram.org/api/privacy)
- [Samozniszczenie konta](https://core.telegram.org/method/account.setAccountTTL)

05

## Usługi numeryczne

Opcje, od których warto zacząć. Kraje, ceny oraz to, czy Telegram akceptuje zmianę numeru, ulegają częstym zmianom; prosimy o sprawdzenie przed dokonaniem płatności.

### Karty SIM typu prepaid i eSIM 11

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
  - Przedpłacone

  Plan PayGo, bardzo tani
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Przedpłacone
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Przedpłacone
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Przedpłacone
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Aplikacje z numerami wirtualnymi 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Tylko dla Stanów Zjednoczonych; rejestracja wymaga podania numeru telefonu z USA
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Numer zostanie cofnięty, jeśli nie zostanie przez Państwa wykorzystany
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
  - Inne kraje
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
  - Płatne

  W ramach okresu próbnego
- [Hushedhushed.com](https://hushed.com)

  - Wiele krajów
  - Płatne

  Tanie
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

  Europejskie numery telefonów komórkowych w aplikacji
- [Sonetelsonetel.com](https://sonetel.com)

  - Wiele krajów
  - Bezpłatny numer
- [Zadarmazadarma.com](https://zadarma.com)

  - Wiele krajów

  Numery wirtualne

### Liczba wynajmów i aktywacji: 12

Wynajem zapewnia numer na okres tygodni lub miesięcy. Jednorazowa aktywacja generuje pojedynczy kod: należy ustawić hasło do chmury zaraz po rejestracji.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Wynajem
  - Aktywacje
- [SMSPVAsmspva.com](https://smspva.com)

  - Wynajem
  - Aktywacje
- [5SIM5sim.net](https://5sim.net)

  - Wynajem
  - Aktywacje
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Wynajem
  - Jednorazowe
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Wynajem
  - Aktywacje
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Wynajem
  - Aktywacje
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Wynajem
  - Aktywacje
- [365SMS365sms.org](https://365sms.org)

  - Wynajem
  - Aktywacje
- [SIMSMSsimsms.org](https://simsms.org)

  - Wynajem
  - Aktywacje
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Jednorazowe
- [SMS-MANsms-man.com](https://sms-man.com)

  - Jednorazowe
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Jednorazowe
