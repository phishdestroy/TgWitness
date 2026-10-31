# Połączenia, serwery proxy i ochrona danych

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/

Uwierzytelnianie, automatyczne pule serwerów proxy, tryby adresów IP, zasady rezerwowe, żądania zewnętrzne oraz przechowywanie kluczy tajnych.

Niniejszy dokument opisuje działanie programu TgWitness w wersji 0.7.0 oraz jego ograniczenia. Uwierzytelnianie, dostęp do źródła, łączność sieciowa oraz kompletność przechwytywania stanowią odrębne stany. W przypadku procedur logowania, formatów plików oraz obsługi wielu kont proszę zapoznać się najpierw z sekcją [„Konta i formaty sesji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/)”. Informacje na temat zasad dotyczących zdarzeń oraz zachowania po ponownym uruchomieniu można znaleźć w sekcji [„Jak działa gromadzenie danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/)”.

## Metody uwierzytelniania

**Identyfikator API i skrót API służą do identyfikacji aplikacji; nie zastępują one danych logowania do konta.** W TgWitness są one opcjonalne. Kolejność pierwszeństwa: para wprowadzona w formularzu, następnie para z zaimportowanego pliku JSON konta, następnie para zapisana w obszarze roboczym, a na końcu wbudowana pula 50 par publicznych, wypróbowywanych w losowej kolejności z automatyczną rotacją w przypadku odrzucenia jednej z nich przez Telegram. Jedynie para z aplikacji Telegram Desktop (2040) jest wysyłana wraz z pasującym opisem klienta Telegram Desktop. Państwa własna para z narzędzi programistycznych API dostępnych na [stronie my.telegram.org](https://my.telegram.org) może być używana ze wszystkimi Państwa kontami; każde konto nadal posiada własną autoryzację.

| Metoda | Wymagania | Pomoc techniczna TgWitness |
| --- | --- | --- |
| Numer telefonu, kod, opcjonalne uwierzytelnianie dwuskładnikowe (2FA) | Dostęp do konta; para kluczy API opcjonalna | Logowanie do panelu |
| Klucz autoryzacyjny HEX + identyfikator DC | Pełny klucz o długości 512 znaków oraz DC 1–5 | Zakładka „Bezpośredni **klucz autoryzacyjny”**; opcjonalny identyfikator użytkownika jest sprawdzany przed zapisaniem autoryzacji |
| Telethon StringSession | Prawidłowy ciąg sesji | Logowanie do panelu |
| Telethon SQLite `.session` | Tekst zamknięty, spójny | Bezpośredni import schematów za pomocą panelu 7/8; opcjonalny interfejs CLI w trybie offline |
| Pyrogram SQLite `.session` | Zamknięta sesja użytkownika w środowisku produkcyjnym | Bezpośredni import schematów za pomocą panelu 2/3 |
| Telegram Desktop TData ZIP | Jedno nowoczesne konto; lokalny kod dostępu, jeśli konto jest chronione | Konwersja w pamięci z kontrolą sum kontrolnych i deszyfrowania |
| Konto JSON | Obsługiwane pola API/sesji/klucza | Same metadane wystarczają do wypełnienia danych uwierzytelniających API; nadal wymagane jest logowanie za pomocą sesji/klucza lub numeru telefonu/kodu QR |
| Logowanie za pomocą kodu QR | Potwierdzenie z autoryzowanej aplikacji Telegram | Lokalne generowanie kodów QR, wygasanie/ponowna próba, opcjonalne uwierzytelnianie dwuskładnikowe (2FA) |
| TDLib / Pyrogram StringSession | Inne formaty specyficzne dla bibliotek | Nieobsługiwane |
| Token bota | Bot z własnym modelem dostępu i aktualizacji | Niewykorzystane przez tego zbierającego dane |

Telegram wybiera dostarczanie kodów; dostarczenie SMS-ów nie jest gwarantowane. Skrót API nie pozwala przywrócić unieważnionej sesji ani zastąpić zapomnianego hasła do uwierzytelniania dwuskładnikowego (2FA). TgWitness nie zapisuje kodów logowania ani hasła do uwierzytelniania dwuskładnikowego (2FA) w Telegramie na dysku.

W przypadku źródła prywatnego konto musi już posiadać dostęp. Nazwa użytkownika grupy nie jest konieczna. Korzystanie z serwera proxy lub import sesji nie przyznaje ani członkostwa, ani uprawnień administratora. Obecne członkostwo nie gwarantuje dostępu do historii sprzed dołączenia.

## Importuj plik sesji Telethon

Telethon SQLite, Pyrogram SQLite oraz Telegram Desktop TData wykorzystują różne formaty. Panel wykrywa i konwertuje obsługiwane struktury; zmiana nazwy pliku nie stanowi konwersji. Proszę wybrać jedną sesję oraz towarzyszący jej plik JSON w sekcji **„Pliki**”, a następnie nacisnąć przycisk **„Połącz konto**”. Akceptowane są maksymalnie cztery pasujące pliki o łącznej wielkości do 8 MiB. Szczegółowe informacje na temat [ograniczeń formatów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/) TData/JSON można znaleźć tutaj. Nie ma możliwości odzyskania kodu dostępu. Logowanie za pomocą telefonu/2FA lub kodu QR tworzy oddzielne uprawnienie.

Opcjonalna ścieżka wiersza poleceń przeznaczona wyłącznie dla Telethon pozostaje dostępna:

1. Należy zatrzymać działanie klienta korzystającego z oryginalnej sesji i utworzyć spójną kopię. Konwerter odrzuca pliki z niekompletnym dziennikiem WAL/dziennikiem operacji. Należy prawidłowo zamknąć oryginalnego klienta zamiast usuwać te pliki w celu ominięcia kontroli.
2. W środowisku TgWitness należy wykonać następujące polecenie:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. W sekcji **„Dodaj konto” → „Pliki**” proszę załadować wynik lub wkleić jego ciąg znaków, a następnie kontynuować.
2. Proszę sprawdzić wyświetlony numeryczny identyfikator konta, wybrać źródła i rozpocząć obserwację.

Konwerter otwiera bazę danych SQLite w trybie tylko do odczytu, nie przeprowadza aktualizacji schematu ani nie wysyła żądań sieciowych, a także nie wyświetla treści sesji. Sprawdza wersję schematu, typy tabel, pojedynczy wiersz sesji, adres IP/port/centrum danych oraz długość klucza. Wielkość danych wejściowych w interfejsie CLI jest ograniczona do 64 MiB; tekst StringSession jest ograniczony do 4 KiB. Konwersja w panelu polega na przesłaniu plików na uwierzytelniony serwer TgWitness, przetworzeniu ich w pamięci oraz zwróceniu znormalizowanych danych uwierzytelniających do tej przeglądarki bez zapisywania przesłanych oryginałów. W przypadku serwera zdalnego należy używać protokołu HTTPS.

**Przekonwertowany plik stanowi niezaszyfrowany sekret dostępu do konta.** Należy go przechowywać w zabezpieczonym miejscu i nigdy nie wprowadzać do systemu ani nie wysyłać do zewnętrznej usługi konwersji. TgWitness zapisuje autoryzowaną sesję w swoim zaszyfrowanym sejfie. Skopiowanie sesji nie powoduje utworzenia oddzielnej autoryzacji: nie należy uruchamiać równoległych klientów z sklonowanymi kluczami autoryzacyjnymi i zakładać niezależnego dostarczania aktualizacji.

Konwersja przenosi uprawnienia, a nie oryginalne wiadomości, pamięć podręczną obiektu ani trwały wskaźnik aktualizacji. Nie zapewnia odzyskiwania aktualizacji po ponownym uruchomieniu procesu.

## MTProto, Telethon i serwery proxy

MTProto to protokół serwisu Telegram. Telethon to biblioteka kliencka w języku Python, z której korzysta TgWitness. MTProxy to proxy transportowe serwisu Telegram; protokoły SOCKS5 i HTTP CONNECT zapewniają ogólne tunele. Żadne z nich nie zastępuje uwierzytelniania konta.

Proszę zapisać trasę połączenia dla każdego obszaru roboczego w sekcji **Konto → Ustawienia → Ustawienia połączenia → Zmień trasę połączenia** przed zalogowaniem się. Nowe obszary robocze domyślnie korzystają z **opcji Automatyczny MTProxy · listy publiczne** z funkcją ukrywania adresu IP. Istniejące obszary robocze, które wyraźnie korzystały z trybu Bezpośredni, zachowują tryb umożliwiający jego stosowanie.

## Tryby IP

Trasa wyznacza połączenie. Tryb IP określa, kiedy adres serwera może zostać ujawniony. Te opcje nie powodują instalacji sieci VPN ani nie przekierowują całego ruchu z urządzenia.

| Tryb | Telegram | Prośby zewnętrzne |
| --- | --- | --- |
| Hide IP (`hide`) | Proszę skorzystać z serwera proxy; w razie braku dostępności należy poczekać. Brak bezpośredniego rozwiązania awaryjnego. | Wymagane jest użycie protokołu SOCKS5/HTTP; żądania bez odpowiedniego serwera proxy są odrzucane. |
| Zezwól na wersję awaryjną (`fallback`) | Automatyczny serwer MTProxy może po upływie skonfigurowanego opóźnienia skorzystać z połączenia bezpośredniego (Direct), a następnie powrócić do działania za pośrednictwem serwera proxy. | Preferowane jest skonfigurowane zewnętrzne proxy lub trasa SOCKS5/HTTP danego konta; w przeciwnym razie dopuszczalne jest połączenie bezpośrednie. |
| Tunnel / VPN (`tunnel`) | Dopuszczalne są bezpośrednie połączenia oraz natychmiastowe przełączanie awaryjne na pulę automatyczną. | Połączenie bezpośrednie jest dozwolone, gdy nie skonfigurowano żadnego odpowiedniego serwera proxy. |

Tryb tunelu/VPN zakłada, że zarządzają Państwo tą siecią oddzielnie. Bez działającego tunelu odbiorcy mogą zobaczyć adres samego serwera. Proszę wybrać tryb zgodnie z Państwa rzeczywistą konfiguracją sieci, a nie na podstawie nazwy opcji.

### Proszę wybrać ścieżkę

| Trasa | Ustawienia | Zakres |
| --- | --- | --- |
| Automatyczny MTProxy | Wbudowane listy lub katalog operatorów | Utrzymuje działającą trasę Telegramu; bezpośredni mechanizm awaryjny zależy od trybu IP |
| Bezpośredni | Tryb tunelu/VPN | Telethon korzysta z trasy sieciowej gospodarza |
| SOCKS5 | Serwer, port, opcjonalna nazwa użytkownika/hasło | python-socks, z włączoną obsługą zdalnych serwerów DNS |
| HTTP CONNECT | Serwer, port, opcjonalna nazwa użytkownika/hasło | Zwykłe połączenie HTTP CONNECT; protokół TLS w stosunku do samego serwera proxy nie został zaimplementowany |
| MTProxy | Serwer, port, klucz tajny | Eksperymentalny format transmisji Telethon; 32 cyfry szesnastkowe lub `dd` + 32 cyfry szesnastkowe |

Fałszywe klucze TLS typu `ee` są odrzucane. Funkcja normalizacji w Telethon 1.45 może usunąć prefiks i domenę, ale nie realizuje to mechanizmu Fake TLS. Proszę wkleić `tg://proxy?server=…&port=…&secret=…` lub `https://t.me/proxy?server=…&port=…&secret=…` i wybrać opcję **„Wypełnij pola z linku**”. Spowoduje to sprawdzenie poprawności i wypełnienie pól bez nawiązywania połączenia ani zapisywania; proszę sprawdzić i zapisać trasę oddzielnie. Pola do ręcznego wprowadzania danych pozostają dostępne. Zobacz [linki proxy serwisu Telegram](https://core.telegram.org/api/links#proxy-links).

### Publiczne serwery proxy udostępniane przez Państwa instalację

Wbudowana lista łączy cztery źródła: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) oraz [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Dołączona migawka zawiera dane dotyczące punktów końcowych, informacje o źródłach oraz daty pobrania. Wymienienie dostawcy w wykazie nie stanowi dowodu na to, że serwer proxy działa lub dostarcza wszystkie aktualizacje aplikacji Telegram.

**MTProxy automatycznie** sprawdza łączność transportową z Telegramem, utrzymuje działający serwer proxy i przełącza się na inny w przypadku awarii. Obszary robocze preferują różne serwery proxy, gdy dostępnych jest wystarczająco wiele działających wpisów; nie gwarantuje się unikalnego adresu wyjściowego. Serwery proxy, które zawiodły, odczekują przed kolejną próbą. Jeśli żaden nie działa, tryb IP określa, czy gromadzenie danych musi zostać wstrzymane, czy też można skorzystać z bezpośredniego połączenia. Zmiana serwerów proxy nie powoduje zmiany konta ani nie usuwa jego dziennika. Wybory tras i zmiany są rejestrowane w podpisanym dzienniku.

Gdy trasy automatyczne są aktywne, listy są odświeżane co godzinę, a kontrole przesyłek odbywają się domyślnie co dziesięć minut. Odstępy te można konfigurować. **Aktualizacja list publicznych** powoduje odświeżenie; samo wyświetlenie listy nie powoduje zmiany zapisanej trasy ręcznej.

Każda odpowiedź z kanału jest ograniczona do 1 MiB, z ośmiosekundowym limitem czasu na wysłanie żądania oraz 20-sekundowym ogólnym terminem pobierania; przekierowania są odrzucane. Z każdego źródła zachowywanych jest maksymalnie 64 zgodnych wpisów, które są deduplikowane. Parser akceptuje obsługiwane klucze w formacie szesnastkowym i base64url oraz kanał JSON. Fałszywe certyfikaty TLS typu „`ee`”, nieprawidłowe linki, prywatne/zarezerwowane literały adresów IP oraz lokalne nazwy hostów są pomijane. Nazwy hostów są rozpoznawane i sprawdzane przed użyciem, a wybrany adres IP jest przypisywany na stałe do danego połączenia. Automatyczne ponowne pozyskiwanie danych powoduje ponowne rozpoznanie nazwy hosta; w celu ponownego rozpoznania należy ponownie wprowadzić wpis ręcznie.

W przypadku nieudanych, pustych lub niezgodnych odpowiedzi z kanału zachowywana jest poprzednia migawka źródła. Aktualizacje mają charakter atomowy, są serializowane i ograniczone do jednej próby na minutę na obszar roboczy. Pomyślny test transmisji potwierdza jedynie łączność, a nie anonimowość ani kompletność przechwytywania danych.

**Ruch w aplikacji Telegram oraz żądania HTTPS wykorzystują różne trasy.** Pobieranie list odbywa się za pośrednictwem oddzielnego połączenia HTTPS oraz dostarczonej trasy żądań zewnętrznych. `TGWITNESS_PROXY_FEED_PROXY` wyraźnie zastępuje tę trasę za pomocą serwera proxy HTTP/SOCKS5; oba warianty kolektora Compose przekazują ją dalej. Pula działająca w tle podąża za głównym obszarem roboczym. Do dostawców danych nie są przesyłane żadne sesje serwisu Telegram, dane uwierzytelniające API, token panelu ani token bota. Nazwy dostawców, daty migawek oraz trasa pobierania są wyświetlane w sekcji **„Skąd pochodzi lista**”.

Proxy MTProxy obsługuje wyłącznie ruch z aplikacji Telegram. Operacje HTTP w obszarze roboczym, takie jak znaczniki czasu, powiadomienia, kopie zewnętrzne i weryfikacja źródeł, korzystają z oddzielnego proxy SOCKS5/HTTP, o ile zostało ono skonfigurowane, a następnie z trasy SOCKS5/HTTP danego konta. W przypadku braku którejkolwiek z tych opcji usługa Hide IP odrzuca żądanie; pozostałe tryby zezwalają na połączenie bezpośrednie. Żądania zewnętrzne można wyłączyć. Wyraźnie skonfigurowany serwer proxy do pobierania kanałów pozostaje odrębną opcją nadpisującą ustawienia domyślne. Niezależna usługa świadków zachowuje własną trasę.

****Parametry automatycznego puli**** W sekcji **Parametry → Automatyczny MTProxy** należy skonfigurować próg awarii, czas oczekiwania, planowaną rotację, udostępnianie serwerów proxy oraz dopuszczalne opóźnienie przełączenia awaryjnego. | Parametr | Wartość domyślna | | --- | --- | | Rozłączenie przed wymianą | 3 w ciągu 10 minut | | Liczba prób połączenia z serwerami proxy na jedną próbę połączenia | 3 | | Pierwsza / maksymalna przerwa po awarii | 10 minut / 6 godzin | | Planowana rotacja | Wyłączona; przełączanie w przypadku awarii | | Liczba kont na serwer proxy | 0: preferowane są oddzielne wpisy, współdzielenie w razie potrzeby. Ustawienie wartości 1 powoduje oczekiwanie na wyłączny wpis. | | Opóźnienie przed dozwolonym przejściem awaryjnym na Direct | 10 minut; funkcja „Ukryj IP” nadal odrzuca połączenia przez Direct | | Odświeżanie kanału / kontrole transmisji | 60 / 10 minut; wartości z głównego obszaru roboczego mają zastosowanie do puli współdzielonej | Różne serwery proxy nie gwarantują różnych adresów wyjściowych. Ustawienia te nie zastępują limitów serwisu Telegram ani nie zapewniają anonimowości.

Aby zastąpić publiczną listę własnym katalogiem operatorów, skonfiguruj poniższe nadpisanie. Powoduje to całkowite wyłączenie subskrypcji zewnętrznych, nawet jeśli tablica `proxies` jest pusta.

Skopiuj [pusty katalog](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) do `proxy-config/proxies.json` i dodaj swoje wdrożone publiczne punkty końcowe:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Należy zastąpić przykładowe wartości. Dopuszczalne jest maksymalnie 32 różne wpisy. Uwierzytelniona lista zwraca etykiety/hosty/porty bez wspólnych kluczy; wybranie jednego z nich powoduje zapisanie jego danych uwierzytelniających w skarbcu obszaru roboczego. Dostępność pozostaje niesprawdzona do czasu przeprowadzenia wyraźnego testu transportu. W przypadku nieprawidłowo sformułowanego katalogu możliwa jest konfiguracja ręczna.

Uruchomienie w środowisku natywnym: należy ustawić ścieżkę JSON na `TGWITNESS_PROXY_CATALOG`. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Nakładka montuje katalog `proxy-config` w trybie tylko do odczytu; pliki muszą być dostępne do odczytu dla kontenera o identyfikatorze UID 10001. Katalog ten jest wykluczony z repozytorium Git, kontekstu kompilacji Docker oraz archiwów źródłowych. Niniejszy katalog konfiguruje konta służące do gromadzenia danych; [bot świadczący](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/) wykorzystuje własną trasę HTTP/SOCKS5, a nie MTProxy.

Bezpośredni tryb awaryjny podlega zasadom trybu IP opisanym powyżej. Należy wstrzymać obserwację przed zmianą trasy. Zapisanie trasy powoduje rozłączenie starych klientów i anulowanie niedokończonego logowania; nowy klient korzysta z zapisanej trasy. Powiązanie dziennika z sesją konta pozostaje niezmienione. Ustawienia zastępują poprzednią trasę: podczas edycji należy ponownie wprowadzić dane uwierzytelniające serwera proxy.

Dane uwierzytelniające są szyfrowane w standardzie `network.enc`. Interfejs API nie zwraca nazwy użytkownika, hasła ani klucza tajnego. Podpisane zapisy zawierają typ trasy oraz informację o tym, czy dane uwierzytelniające są obecne, z wyłączeniem punktu końcowego i kluczy tajnych. Operator może zobaczyć punkt końcowy w panelu. Pola zawierające klucze tajne są czyszczone po zapisaniu, zablokowaniu lub zmianie obszaru roboczego.

**Funkcja „Sprawdź połączenie z Telegramem**”, dostępna również przed zalogowaniem, otwiera i zamyka tymczasowe nieautoryzowane połączenie z Telegramem poprzez wyznaczoną trasę. Nie nawiązuje ona połączenia z witryną sprawdzającą adresy IP. Pomyślny wynik potwierdza łączność transportową, a nie dostęp do grup, pełną dostawę wiadomości ani anonimowość.

Serwer proxy ma zastosowanie do połączeń klienta Telegram, w tym do pobierania multimediów z serwerów dystrybucyjnych (DC) Telegramu. Przeglądarka, pip, SSH oraz narzędzia TSA uruchamiane ręcznie mają oddzielne trasy. Nazwa hosta serwera proxy może być rozpoznawana lokalnie. `rdns` ma wpływ na nazwy hostów docelowych; Telegram często podaje numeryczne adresy IP serwerów dystrybucyjnych (DC).

Protokoły SOCKS5 i zwykły HTTP CONNECT same w sobie nie szyfrują danych uwierzytelniających serwera proxy ani tunelu między klientem a serwerem proxy. MTProto oddzielnie zabezpiecza ruch w aplikacji Telegram. W sieci, której nie ufa się, należy korzystać z odpowiedniego, bezpiecznego kanału łączącego z serwerem proxy. Grupy prywatne są czatami w chmurze; protokół MTProto nie przekształca ich w czaty tajne z szyfrowaniem typu end-to-end.

## Szyfrowanie i podpisy

| Warstwa | Zrealizowano | Odpowiedzialność operatora |
| --- | --- | --- |
| Ruch w aplikacji Telegram | Telethon MTProto | Zaufanie do platformy, trasa i dostępność |
| Panel internetowy | Token typu „bearer”, domyślna pętla zwrotna, limity żądań | HTTPS lub tunel SSH do zdalnego dostępu |
| Sekrety | Fernet do zarządzania danymi uwierzytelniającymi API, sesjami, danymi uwierzytelniającymi serwerów proxy oraz kluczem prywatnym służącym do podpisywania | Należy chronić klucz deszyfrujący oraz serwer, na którym działa aplikacja |
| Klucz do skarbca | Klucz lokalny lub zewnętrzny klucz główny dla nowej instalacji | Oddzielna, zabezpieczona pamięć masowa oraz kopia zapasowa klucza |
| Wiadomości i załączniki | Przechowywanie danych aplikacji w postaci zwykłego tekstu | Szyfrowany dysk/wolumin |
| ZIP/JSONL/CSV/HTML | Kontrole integralności, brak szyfrowania treści | Ochrona wyeksportowanych kopii i przekazów |
| Pochodzenie i czas | Podpisany dziennik, potwierdzenie przetworzenia, narzędzia zgodne z RFC 3161 | Klucz zaufany, niezależne punkty kontrolne/TSA oraz procedura przechowywania danych |

**Funkcja ochrony pamięci masowej** w sekcji „Konto” wyświetla te stany. Token panelu stanowi klucz dostępu, a nie hasło szyfrujące. Zapewnia on dostęp administratora; [wygenerowane tokeny](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/) można ograniczyć do określonych kont i czatów. Obszary robocze współdzielą proces hosta i nie stanowią odizolowanych instancji.

Wyraźnie uruchomiona, izolowana syntetyczna wersja demonstracyjna może otwierać się automatycznie poprzez bezpośrednie połączenie typu loopback. Wykorzystuje to funkcję o odrębnym cyklu życia procesu; nie ujawnia ona skonfigurowanego tokenu panelu ani nie przyznaje dostępu do rzeczywistych przestrzeni roboczych. Żądania zdalne, przekazywane przez serwer proxy lub międzydomenowe nie mogą uzyskać ani wykorzystać tej funkcji automatycznego dostępu. Ta wygoda nie znosi ograniczeń związanych z uwierzytelnianiem w odniesieniu do rzeczywistych danych konta.

BitLocker, LUKS, FileVault lub zarządzany wolumin szyfrowany mogą chronić pamięć masową w ramach odpowiednich modeli zagrożeń. Administrator odblokowanego, uruchomionego komputera nadal może odczytać dane. W planowaniu pamięci masowej należy uwzględnić pliki WAL/SHM bazy SQLite, multimedia, tymczasowe eksporty, pliki wymiany, kopie zapasowe oraz pliki pobrane z przeglądarki. Wolumin Docker nie jest szyfrowany tylko dlatego, że jest woluminem. TgWitness nie obsługuje szyfrowania SQLCipher ani szyfrowania obiektowego.

## Zewnętrzny klucz główny

W przypadku **nowej** instalacji należy umieścić klucz główny poza katalogiem danych. Nie spowoduje to automatycznej migracji istniejącego magazynu kluczy lokalnych. Należy przygotować katalog kluczy dostępny wyłącznie dla tożsamości usługi, a następnie uruchomić:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, z wykorzystaniem zainstalowanego środowiska projektowego:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

W środowisku Docker należy zamontować plik w trybie tylko do odczytu poza katalogiem `/data`, na przykład w katalogu `/run/secrets/tgwitness-master.key`, a następnie ustawić zmienną środowiskową na tę ścieżkę. Identyfikator UID usługi musi mieć uprawnienia do odczytu tego pliku. Należy przekazać ścieżkę, a nie bajty klucza, za pośrednictwem plików środowiskowych/konfiguracyjnych.

Każdy obszar roboczy otrzymuje losowy publiczny salt oraz własny klucz Fernet wygenerowany za pomocą algorytmu HKDF-SHA256. `vault.external.json` przechowuje metadane dotyczące generowania klucza, a nie sam klucz główny. Brakujący lub nieprawidłowy klucz uniemożliwia uruchomienie systemu bez cichej zamiany klucza. Należy zachować zarówno metadane dotyczące saltu, jak i klucz główny na potrzeby odzyskiwania danych.

Wszystkie obszary robocze wywodzą się z tego samego klucza głównego; jego naruszenie ma wpływ na całą instalację. Uruchomiony proces może odszyfrowywać dane poufne. Nie jest to moduł HSM ani algorytm KDF oparty na haśle. Dowolne hasła wprowadzane przez użytkownika nie są akceptowane w miejsce klucza losowego.

Należy zachować dotychczasowy klucz w istniejących instalacjach do czasu przeprowadzenia i zweryfikowania celowej migracji. Usunięcie klucza `vault.key` lub zastąpienie klucza głównego może uniemożliwić dostęp do sesji lub kluczy podpisujących. Należy przechowywać zaszyfrowane kopie zapasowe i klucze oddzielnie oraz przetestować proces odzyskiwania danych w izolowanej instancji.

## Źródła i zakres weryfikacji

Sprawdzono dnia 26 października 2026 r.:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, `Connection._proxy_connect`, `TcpMTProxy.normalize_secret` oraz metody pobierania.

Lokalne testy obejmują testy pętli zwrotnej SOCKS5/HTTP CONNECT, syntetyczne sesje SQLite, izolację tras, wykluczanie tajnych danych oraz odrzucanie w przypadku braku klucza. Nie odzwierciedlają one rzeczywistej interoperacyjności między Telegramem a serwerem proxy ani rzeczywistego zachowania MTProxy. Proszę zapoznać się z [plik ami VERIFICATION.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/) oraz [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
