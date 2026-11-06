# Połączenia, serwery proxy i ochrona danych

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/

Uwierzytelnianie, automatyczne pule serwerów proxy, tryby adresów IP, zasady rezerwowe, żądania zewnętrzne oraz przechowywanie kluczy tajnych.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Niniejszy dokument opisuje działanie programu TgWitness w wersji 0.8.0 oraz jego ograniczenia. Uwierzytelnianie, dostęp do źródła, łączność sieciowa oraz kompletność przechwytywania stanowią odrębne stany. W przypadku procedur logowania, formatów plików oraz obsługi wielu kont proszę zapoznać się najpierw z sekcją [„Konta i formaty sesji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/)”. Informacje na temat zasad dotyczących zdarzeń oraz zachowania po ponownym uruchomieniu można znaleźć w sekcji [„Jak działa gromadzenie danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/)”.

## Konfiguracja połączenia z przewodnikiem

W **„Połączenie”** administrator może wybrać **„To konto”**, **„Grupa kont”** lub **„Wszystkie konta”**, a następnie wybrać trasę. **„Przejrzyj wybór”** wyświetla listę objętych kont. **„Przygotuj i sprawdź”** testuje proponowaną trasę bez zmiany zapisanej trasy. **„Zastosuj sprawdzone połączenie”** ponownie sprawdza, wstrzymuje obserwację, jeśli jest to konieczne, zapisuje trasę i wznawia już uruchomioną obserwację. Nigdy nie rozpoczyna gromadzenia danych na koncie, które wcześniej było nieaktywne. Pobieranie historii pozostaje wstrzymane i można je wznowić oddzielnie. Przed przełączeniem należy wstrzymać aktywne eksporty.

Zmiany w grupach domyślnie zachowują konta z ich własną ścieżką. Wyczyść tę opcję tylko wtedy, gdy podgląd zawiera listę zmian, które zamierzasz wprowadzić. Aplikacja raportuje wyniki dla każdego konta; nie jest to transakcja typu „wszystko albo nic” obejmująca wszystkie bazy danych. Nieudana zmiana przywraca poprzednie ustawienia tego konta. Brak możliwości wznowienia jest wyraźnie sygnalizowany. Podglądy wygasają po dziesięciu minutach, a zmiany w ustawieniach połączenia lub przynależności do grup wymagają ponownego sprawdzenia.

| Trasa | Czym zarządza TgWitness |
| --- | --- |
| Bezpośredni | Połączenia z hosta; zewnętrzna sieć VPN hosta nie jest wykrywana ani egzekwowana. |
| VPN | Jeden profil WireGuard z pełnym tunelem na konto, obsługiwany przez lokalny proces SOCKS5 w przestrzeni użytkownika. Nie jest zainstalowany żaden interfejs hosta ani sterownik. |
| Mój serwer proxy | Dane uwierzytelniające typu SOCKS5, HTTP CONNECT lub MTProxy. W polach SOCKS5/HTTP można wpisać adres URL. Wybranie kilku kont powoduje współdzielenie wprowadzonego serwera proxy. |
| Publiczny MTProto | Istniejąca pula przypisuje trasy Telegram. Żądania zewnętrzne są wyłączone do momentu skonfigurowania oddzielnego, odpowiedniego serwera proxy w ustawieniach zaawansowanych. |
| WARP | Osobny tunel lokalny dla każdego wybranego konta, z rejestracją WARP i profilem WireGuard przechowywanym w skarbcu tego konta. |

Sprawdzanie bieżącej trasy wykorzystuje nowe, nieuwierzytelnione połączenie Telegram, a nie sesję konta. W przypadku tras obsługujących HTTP wysyła również żądanie śledzenia HTTPS do Cloudflare przez tę trasę i wyświetla zgłoszony adres IP wyjściowy, kraj, stan WARP oraz czas sprawdzenia. Zmierzona latencja to czas nawiązania połączenia Telegram, a nie wynik polecenia ping ICMP. Przygotowanie WARP kończy się niepowodzeniem, chyba że ślad zgłasza, że WARP jest aktywny. Sprawdzenia te potwierdzają łączność, a nie autentyczność ani kompletność przechwyconych komunikatów. Sam uruchomiony proces lokalny nie oznacza pomyślnego zakończenia sprawdzenia wyjścia.

### Przenośne wersje WARP i WireGuard

Jest to nieoficjalna integracja WARP **** przy użyciu [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) oraz [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3). Administrator wyraźnie akceptuje konfigurację przed pierwszym pobraniem lub rejestracją w WARP. Te połączenia konfiguracyjne prowadzą bezpośrednio do GitHub i Cloudflare oraz Te połączenia konfiguracyjne kierowane są bezpośrednio do serwisów GitHub i Cloudflare i ujawniają adres IP urządzenia. Zwykły ruch z konta zachowuje dotychczasową trasę aż do momentu uruchomienia aplikacji. Cloudflare wybiera adres wyjściowy i kraj; oddzielne tunele mogą współdzielić ten sam adres wyjściowy. Ta funkcja nie zapewnia wyboru kraju, okresowej rotacji adresów IP ani funkcji kill switch dla całej sieci.

Obsługiwane wersje narzędzi pomocniczych do pobrania: Linux i macOS x86-64/ARM64 oraz Windows x86-64. Pliki są sprawdzane pod kątem zgodności z skrótami SHA-256 zawartymi w sprawdzonym kodzie źródłowym, a pliki wykonywalne z pamięci podręcznej są ponownie sprawdzane przed uruchomieniem. Żadne narzędzie pomocnicze nie jest dodawane do ścieżki PATH, instalowane jako usługa systemowa ani nie otrzymuje publicznego punktu nasłuchowego. Wszystkie pliki znajdują się w katalogu `portable-routes/` obszaru roboczego oraz w zaszyfrowanych wpisach skarbca. Punkt nasłuchowy typu loopback SOCKS5 wymaga niezależnie wygenerowanych poświadczeń.

Prywatne profile i dane logowania do konta WARP są szyfrowane za pomocą istniejącego sejfu obszaru roboczego. Podczas działania program pomocniczy wymaga pliku konfiguracyjnego w postaci zwykłego tekstu, dostępnego wyłącznie dla właściciela; jest on usuwany po normalnym zakończeniu działania. Awaria hosta może spowodować pozostawienie tego pliku w folderze danych dostępnym wyłącznie dla właściciela. Nie powoduje to szyfrowania dysku ani nie zapewnia ochrony przed jego administratorem. Nadzorca zamyka tunel, jeśli nadrzędny potok panelu zniknie. Nieudany tunel nigdy nie włącza bezpośredniego rozwiązania awaryjnego. Ponowne uruchomienie panelu przywraca wybrany tunel; nieudane uruchomienia są ponawiane z ograniczonym opóźnieniem. **Zatrzymaj tunel** również wstrzymuje obserwację i utrzymuje stan zatrzymania. **Uruchom tunel** uruchamia tunel; obserwację należy wznowić oddzielnie, gdy będzie gotowa.

Przesłane profile WireGuard muszą zawierać jeden interfejs i jednego partnera, pełne trasy IPv4 i IPv6 oraz nie mogą zawierać żadnych hooków, include’ów, podstawień środowiskowych ani dodatkowych słuchaczy. Publiczne adresy punktów końcowych są rozpoznawane i przypisywane przed uruchomieniem. Należy korzystać z zewnętrznej sieci VPN lub bramy SOCKS5 dla OpenVPN/IPsec oraz prywatnych punktów końcowych.

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

**Przekonwertowany plik stanowi niezaszyfrowany sekret dostępu do konta.** Należy go przechowywać w zabezpieczonym miejscu i nigdy nie wprowadzać do systemu ani nie wysyłać do zewnętrznej usługi konwersji. TgWitness zapisuje autoryzowaną sesję w swoim zaszyfrowanym sejfie. Skopiowanie sesji nie powoduje utworzenia oddzielnej autoryzacji: nie należy uruchamiać równoległych klientów z sklonowanymi kluczami autoryzacyjnymi i zakładać niezależnego dostarczania aktualizacji.

Konwersja przenosi uprawnienia, a nie oryginalne wiadomości, pamięć podręczną obiektu ani trwały wskaźnik aktualizacji. Nie zapewnia odzyskiwania aktualizacji po ponownym uruchomieniu procesu.

## MTProto, Telethon i serwery proxy

MTProto to protokół serwisu Telegram. Telethon to biblioteka kliencka w języku Python, z której korzysta TgWitness. MTProxy to proxy transportowe serwisu Telegram; protokoły SOCKS5 i HTTP CONNECT zapewniają ogólne tunele. Żadne z nich nie zastępuje uwierzytelniania konta.

Zapisz trasę dla każdego obszaru roboczego w sekcji **Konto → Ustawienia → Ustawienia połączenia → Zmień trasę połączenia** przed zalogowaniem się. Nowe obszary robocze domyślnie korzystają z trybu **Automatyczny MTProxy · listy publiczne** z **opcją Ukryj adres**. Istniejące obszary robocze, które wyraźnie korzystały z trybu Bezpośredni, zachowują tryb pozwalający na jego użycie.

## Tryby IP

Trasa wybiera połączenie. Tryb IP, czyli **ochrona adresu IP** w sekcji „Konto” panelu, określa, kiedy adres serwera może zostać ujawniony. Te opcje nie powodują instalacji sieci VPN ani przekierowania całego ruchu z urządzenia.

| Tryb | Telegram | Prośby zewnętrzne |
| --- | --- | --- |
| Ukryj adres (`hide`) | Proszę skorzystać z serwera proxy; w razie braku dostępności należy poczekać. Brak bezpośredniego rozwiązania awaryjnego. | Wymagane jest użycie protokołu SOCKS5/HTTP; żądania bez odpowiedniego serwera proxy są odrzucane. |
| Korzystaj z funkcji „Direct” tylko w ostateczności (`fallback`) | Automatyczny serwer MTProxy może po upływie skonfigurowanego opóźnienia skorzystać z połączenia bezpośredniego (Direct), a następnie powrócić do działania za pośrednictwem serwera proxy. | Preferowane jest skonfigurowane zewnętrzne proxy lub trasa SOCKS5/HTTP danego konta; w przeciwnym razie dopuszczalne jest połączenie bezpośrednie. |
| Serwer za tunelem lub VPN (`tunnel`) | Dopuszczalne są bezpośrednie połączenia oraz natychmiastowe przełączanie awaryjne na pulę automatyczną. | Połączenie bezpośrednie jest dozwolone, gdy nie skonfigurowano żadnego odpowiedniego serwera proxy. |

Tryb tunelu lub VPN zakłada, że samodzielnie zarządzasz tą siecią. Bez działającego tunelu odbiorcy mogą zobaczyć adres samego serwera. Wybierz tryb zgodnie z rzeczywistą konfiguracją sieci, a nie na podstawie nazwy opcji.

### Proszę wybrać ścieżkę

| Trasa | Ustawienia | Zakres |
| --- | --- | --- |
| Automatyczny MTProxy | Wbudowane listy lub katalog operatorów | Utrzymuje działającą trasę Telegramu; bezpośredni mechanizm awaryjny zależy od trybu IP |
| Bezpośredni | Tryb tunelu lub VPN | Telethon korzysta z trasy sieciowej gospodarza |
| SOCKS5 | Serwer, port, opcjonalna nazwa użytkownika/hasło | python-socks, z włączoną obsługą zdalnych serwerów DNS |
| HTTP CONNECT | Serwer, port, opcjonalna nazwa użytkownika/hasło | Zwykłe połączenie HTTP CONNECT; protokół TLS w stosunku do samego serwera proxy nie został zaimplementowany |
| MTProxy | Serwer, port, klucz tajny | Eksperymentalny format transmisji Telethon; 32 cyfry szesnastkowe lub `dd` + 32 cyfry szesnastkowe |

Fałszywe klucze TLS typu `ee` są odrzucane. Funkcja normalizacji w Telethon 1.45 może usunąć prefiks i domenę, ale nie realizuje to mechanizmu Fake TLS. Proszę wkleić `tg://proxy?server=…&port=…&secret=…` lub `https://t.me/proxy?server=…&port=…&secret=…` i wybrać opcję **„Wypełnij pola z linku**”. Spowoduje to sprawdzenie poprawności i wypełnienie pól bez nawiązywania połączenia ani zapisywania; proszę sprawdzić i zapisać trasę oddzielnie. Pola do ręcznego wprowadzania danych pozostają dostępne. Zobacz [linki proxy serwisu Telegram](https://core.telegram.org/api/links#proxy-links).

### Publiczne serwery proxy udostępniane przez Państwa instalację

Wbudowana lista łączy cztery źródła: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) oraz [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Dołączona migawka zawiera dane dotyczące punktów końcowych, informacje o źródłach oraz daty pobrania. Wymienienie dostawcy w wykazie nie stanowi dowodu na to, że serwer proxy działa lub dostarcza wszystkie aktualizacje aplikacji Telegram.

**MTProxy automatycznie** sprawdza łączność transportową z Telegramem, utrzymuje działający serwer proxy i przełącza się na inny w przypadku awarii. Obszary robocze preferują różne serwery proxy, gdy dostępnych jest wystarczająco wiele działających wpisów; nie gwarantuje się unikalnego adresu wyjściowego. Serwery proxy, które zawiodły, odczekują przed kolejną próbą. Jeśli żaden nie działa, tryb IP określa, czy gromadzenie danych musi zostać wstrzymane, czy też można skorzystać z bezpośredniego połączenia. Zmiana serwerów proxy nie powoduje zmiany konta ani nie usuwa jego dziennika. Wybory tras i zmiany są rejestrowane w podpisanym dzienniku.

Gdy trasy automatyczne są aktywne, listy są odświeżane co godzinę, a kontrole przesyłek odbywają się domyślnie co dziesięć minut. Odstępy te można konfigurować. **Aktualizacja list publicznych** powoduje odświeżenie; samo wyświetlenie listy nie powoduje zmiany zapisanej trasy ręcznej.

**Ruch w aplikacji Telegram oraz żądania HTTPS wykorzystują różne trasy.** Pobieranie list odbywa się za pośrednictwem oddzielnego połączenia HTTPS oraz dostarczonej trasy żądań zewnętrznych. `TGWITNESS_PROXY_FEED_PROXY` wyraźnie zastępuje tę trasę za pomocą serwera proxy HTTP/SOCKS5; oba warianty kolektora Compose przekazują ją dalej. Pula działająca w tle podąża za głównym obszarem roboczym. Do dostawców danych nie są przesyłane żadne sesje serwisu Telegram, dane uwierzytelniające API, token panelu ani token bota. Nazwy dostawców, daty migawek oraz trasa pobierania są wyświetlane w sekcji **„Skąd pochodzi lista**”.

MTProxy obsługuje wyłącznie ruch z Telegrama. Operacje HTTP w obszarze roboczym, takie jak znaczniki czasu, powiadomienia, kopie poza serwisem i weryfikacje źródła, korzystają z oddzielnego proxy SOCKS5/HTTP, jeśli zostało skonfigurowane, a następnie z trasy SOCKS5/HTTP danego konta. W przypadku braku obu opcji funkcja „Ukryj adres” odrzuca żądanie; pozostałe tryby zezwalają na połączenie bezpośrednie. Żądania zewnętrzne można wyłączyć. Wyraźnie skonfigurowane proxy do pobierania kanałów pozostaje oddzielnym nadpisaniem przez operatora. Niezależna usługa świadków zachowuje własną trasę.

W przypadku usług prywatnych zarządzanych przez operatora istniejące ustawienie środowiska serwera `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` zezwala na prywatne miejsca docelowe i zachowuje rozpoznawanie nazw hostów po stronie proxy. Nie można go włączyć z poziomu panelu. Tryb wyłącznie publiczny odrzuca miejsca docelowe `.onion` przed wysłaniem zapytania do publicznego serwera rozpoznającego; usługi Tor typu onion wymagają wyraźnego ustawienia prywatnych miejsc docelowych oraz odpowiedniego serwera proxy. To zachowanie DNS dotyczy zewnętrznych operacji HTTP, a nie transportu Telegramu. Cloudflare udokumentowało [punkt końcowy DNS](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/) w formacie [JSON](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/).

****Parametry automatycznego puli****

Under **Parameters → Automatic MTProxy**, configure the failure threshold, cooldown, planned rotation, proxy sharing and permitted fallback delay.

| Kontrola | Domyślnie |
| --- | --- |
| Disconnects before replacement | 3 within 10 minutes |
| Proxies tried per connection attempt | 3 |
| First / maximum rest after failure | 10 minutes / 6 hours |
| Planned rotation | Disabled; switch on failure |
| Accounts per proxy | 0: prefer separate entries, share when needed. Set 1 to wait for an exclusive entry. |
| Delay before permitted Direct fallback | 10 minutes; Hide the address still refuses Direct |
| Feed refresh / transport checks | 60 / 10 minutes; main workspace values apply to the shared pool |

Different proxies do not guarantee different exit addresses. These settings do not override Telegram limits or prove anonymity.

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
