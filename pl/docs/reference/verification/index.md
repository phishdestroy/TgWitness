# Co zostało przetestowane

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/

Test na żywo w serwisie Telegram, automatyczne kontrole, kontrole w przeglądarce oraz elementy, które pozostają niezweryfikowane.

## Test na żywo w serwisie Telegram, całe konto · 29 października 2026 r.

To samo konto nadal działało po przeprowadzeniu poniższego testu. 29 października o godz. 12:10 czasu UTC jego zakres został rozszerzony na całe konto (kanały, grupy, czaty prywatne i boty); panel poprosił o potwierdzenie, a podpisany dziennik to zarejestrował. O godz. 17:59 czasu UTC dziennik zawierał:

| Dane zarejestrowano w okresie od 27 października, godz. 21:36, do 29 października, godz. 17:59 czasu UTC | Liczba |
| --- | --- |
| Zapisy w dzienniku | 9,968 |
| Nowe wiadomości | 5,308 |
| z nich po przejściu na pełne konto | 3,878 |
| Usunięcia | 784 |
| z nich zostały usunięte po tym, jak TgWitness zapisało wiadomość | 596 |
| Edycje | 41 |
| Wiadomości dodane w wyniku ponownej weryfikacji | 2,273 |
| Wiadomości, których nie udało się odnaleźć podczas ponownej weryfikacji | 18 |
| Wiadomości zapisywane za pomocą migawek historii | 242 |
| Zapisane załączniki | 247 |
| Uruchomienie programu Collector | 19 |
| Funkcja „FloodWait” w Telegramie wstrzymuje działanie | 26 |

- W ramach kontroli **„Verify”** panelu potwierdzono podpisy oraz łańcuch skrótów wszystkich 9 968 rekordów.
- Wiadomości pochodziły z 2 grup lub kanałów oraz 3 prywatnych czatów i botów. Naciśnięto jeden przycisk wiadomości w **sekcji „Czaty”**; żądanie oraz odpowiedź serwisu Telegram znajdują się w dzienniku.
- Nowe czaty zostały dodane, gdy moduł zbierający ponownie przeskanował konto po ponownym uruchomieniu. Funkcja zapisywania wcześniejszych wiadomości z nowych czatów była wyłączona (`history = 0`), dlatego nie została tutaj uwzględniona.

Nie obejmuje: reakcji, zmian w składzie członków, profili użytkowników, wysyłania wiadomości, dołączania na zaproszenie, serwerów proxy, powiadomień, bota „witness” oraz korzystania z kilku kont jednocześnie. Pliki publiczne zawierają wyłącznie dane liczbowe.

## Plik eksportowy chroniony hasłem, otwierany za pomocą biblioteki libarchive · 29 października 2026 r.

Archiwum utworzone przy użyciu kodu szyfrowania eksportu (WinZip AES-256, format odczytywany przez programy 7-Zip i WinRAR ) zostało otwarte w systemie Windows za pomocą narzędzia `tar` (bsdtar 3.6.2, libarchive). Po wprowadzeniu prawidłowego hasła wyodrębniony plik wykazał zgodność z oryginalnym skrótem SHA-256; wprowadzenie nieprawidłowego hasła spowodowało komunikat „Nieprawidłowe hasło”. Same programy 7-Zip i WinRAR nie zostały uruchomione.

## Test na żywo w serwisie Telegram · 27–29 października 2026 r.

Jedno rzeczywiste konto w serwisie Telegram, zalogowane za pośrednictwem wbudowanej puli par API, rejestrowało dane z jednej supergrupy od **27 października, godz. 21:36 UTC do 29 października, godz. 05:15 UTC**. Moduł zbierający dane został uruchomiony 12 razy w tym okresie.

| Zarejestrowano | Liczba |
| --- | --- |
| Zapisy dziennika, w tym sygnały kontrolne i zapisy dotyczące działania usługi | 2,385 |
| Nowe wiadomości | 1,291 |
| Usunięcia | 472 |
| z nich zostały usunięte po tym, jak TgWitness zapisało treść | 347 |
| Edycje | 12 |
| Wiadomości pominięte w trakcie przerwy w działaniu, dodane podczas ponownej weryfikacji | 12 |
| Zapisane załączniki | 17 |
| Załączniki nie zostały pobrane (funkcja pobierania wyłączona lub brak pliku do pobrania) | 14 |
| Telegram FloodWait wstrzymuje działanie na 3 sekundy podczas ponownej weryfikacji | 8 |

- Podpisy oraz łańcuch skrótów wszystkich 2 385 wpisów można zweryfikować przy użyciu klucza publicznego dziennika.
- Po ponownym uruchomieniu moduł zbierający wznawia działanie od zapisanego stanu aktualizacji (`pts`), a Telethon nadrabia zaległości; następnie podczas ponownej weryfikacji dodawane są wiadomości, których wciąż brakuje.
- Przy każdym zdarzeniu typu „FloodWait” moduł zbierający dane odczekał żądany czas, a następnie kontynuował działanie.
- Konto pozostało zalogowane, a ta sama sesja została ponownie nawiązana 29 października.

Niniejszy test nie obejmuje następujących kwestii: obsługi wielu kont jednocześnie, ról administratora, serwerów proxy, przerw w działaniu trwających dłużej niż kilka godzin oraz pełnej [procedury akceptacji na żywo](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Pliki publiczne zawierają wyłącznie następujące dane: brak identyfikatorów kont lub czatów, wiadomości ani danych uwierzytelniających.

Poniższe starsze wpisy opisują poszczególne przebiegi testów; w większości z nich wykorzystano syntetyczne klienty testowe. Najnowsze wyniki testów automatycznych przedstawiono poniżej.

## Wbudowane publiczne listy MTProxy · 29 października 2026 r.

Poniżej znajduje się historyczny zapis testów dotyczący pierwotnej wersji oprogramowania z ręcznym wyborem serwerów. Informacje na temat aktualnych trybów automatycznego wyboru puli serwerów oraz adresów IP można znaleźć w [ustawieniach połączenia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes). Podane poniżej dane liczbowe oraz informacje o funkcjach nieobsługiwanych odnoszą się do tej testowanej wersji.

Dodano pakietową kopię publiczną oraz jawne odświeżanie HTTPS z repozytoriów SoliSpirit/mtproto oraz zakky8/mtproto-proxy-pro. Na tym serwerze program pobierający aplikację pomyślnie pobrał oba strumienie danych 29 października 2026 r. o godz. 12:58 czasu UTC: **118 unikalnych, kompatybilnych punktów końcowych** po filtrowaniu, deduplikacji oraz zastosowaniu limitu 64 wpisów na źródło. Potwierdza to pobranie listy, a nie łączność ani dostarczanie komunikatów za pośrednictwem tych punktów końcowych. Żadne rzeczywiste konto nie było połączone z wymienionym serwerem proxy podczas tych prac. [Podręcznik operatora i użytkownika](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

W przypadku nieudanych, pustych lub niezgodnych odpowiedzi źródłowych zachowywane są poprzednie wpisy wraz z datami. Aktualizacje nie zmieniają wybranej trasy. Adresy publiczne są weryfikowane, a rozpoznane adresy IP są przypisywane po ich wyborze; trasy operatorskie i ręczne pozostają oddzielne. Test połączenia jest teraz dostępny w panelu przed zalogowaniem się na konto. Fałszywy certyfikat TLS oraz automatyczny wybór serwera proxy nadal nie są obsługiwane. Katalog operatora całkowicie zastępuje subskrypcje.

- Pełny zestaw testów: **366 zaliczonych, 3 pominiętych**, 287,94 sekundy. Istniejące ostrzeżenia dotyczące zależności oraz pominięcia związane z platformą pozostają. Ostateczna regresja listy publicznej/lokalizacji: **36 zaliczonych**, w tym odrzucenie nieprawidłowych portów serwerów proxy pobierania; pokrywa się to z pełnym zestawem testów.
- Test zgodności z przeglądarkami zakończył się sukcesem w językach angielskim i rosyjskim, w trybie jasnym i ciemnym przy rozdzielczości 390/1440 pikseli: wbudowane opcje wyboru, brak zewnętrznych żądań podczas otwierania ustawień, jawne odświeżanie, zachowanie tras i pamięci podręcznej w przypadku awarii, test przed logowaniem, izolacja obszaru roboczego w przypadku opóźnionych odpowiedzi, szczegóły źródła oraz układ i kontrast. Brak błędów JavaScript ani zewnętrznych żądań przeglądarki.
- Ostateczny zakres tłumaczenia statycznego został zatwierdzony dla wszystkich 13 lokalizacji; nowy tekst został przetłumaczony na język rosyjski, z wyraźnymi angielskimi wersjami rezerwowymi w pozostałych miejscach. Zaktualizowany wbudowany przewodnik przeszedł pomyślnie testy układu i kontrastu w obu motywach.
- Przeprowadzono wstępną weryfikację i kontrolę publikacji (259 plików publicznych, 1 354 linki lokalne); zaktualizowano przetworzono pliki YAML dla funkcji Compose i CI. Nie uruchomiono tutaj Docker ani zdalnego CI.
- Przebudowane narzędzie przeszło pomyślnie testy instalacji w trybie izolowanym, wczytywania listy pakietów oraz weryfikacji eksportu z podpisem . Wszystkie 69 zasobów pakietu było zgodnych z obszarem roboczym; zweryfikowano skróty kodu źródłowego.

Potwierdzenia: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` oraz `test-results/public-proxies-package.log`. Dane dotyczące przeglądarki, konta i transportu są fikcyjne; dwa powyższe pobrania kanałów są rzeczywistymi żądaniami HTTPS.

## Prezentacja opcjonalnych dodatków · 29 października 2026 r.

Dotychczasowa strona botu Proof nosi obecnie nazwę **Extras**: zawiera krótki przegląd, po którym następuje osobna strona konfiguracyjna dla wybranej opcji. Formularz Witness składa się z trzech etapów, przy czym opcje zarządzania połączeniami, ustawienia sieciowe oraz szczegóły wdrożenia są ukryte. GitHub jest wyraźnie uwzględniony i nie wymaga podawania danych uwierzytelniających. [Przegląd w języku rosyjskim](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- Przeprowadzono 30 ukierunkowanych testów dotyczących lokalizacji, konfiguracji serwisu Witness oraz kontroli publikacji.
- Test akceptacji konfiguracji w oparciu o Chromium zakończył się pomyślnie w językach angielskim i rosyjskim, w trybie jasnym i ciemnym, przy rozdzielczości 390/1440 pikseli: fokus klawiatury i klawisz Return, brak domyślnych połączeń podczas wybierania opcji dodatkowych, przechowywanie wersji roboczych, pobieranie przypiętych konfiguracji i tokenów, czyszczenie tokenów po zablokowaniu oraz działające linki do lokalnych przewodników. Przeprowadzono pomyślnie testy układu oraz kontrastu tekstu na jednolitym tle.
- Zatwierdzono obsługę zmiany obszaru roboczego, w tym opóźnioną odpowiedź tokenu pojawiającą się po zmianie. Szybka nawigacja pozwala znaleźć dodatkowe informacje za pomocą terminów związanych z botami, dowodami i serwisem GitHub; istniejące testy rozdzielczości 320/390/1440 pikseli oraz testy rosyjskiego języka i kierunku pisania z prawej do lewej (RTL) również zakończyły się powodzeniem.
- Podczas uruchomienia konfiguracyjnego nie zaobserwowano żadnych błędów JavaScript ani zewnętrznych żądań przeglądarki. Są to syntetyczne testy interfejsu użytkownika, a nie nowe dowody pochodzące z rzeczywistej publikacji w Telegramie lub przez bota.
- Zakończono ładowanie języków i zapewniono kompletność słownika dla wszystkich 13 lokalizacji, zachowując wyraźne angielskie wersje zastępcze poza językiem rosyjskim. Rozszerzony przewodnik Proof również przeszedł kontrole układu i kontrastu przy rozdzielczościach 320/768/1440 pikseli w obu motywach.
- Przebudowana wersja przeszła weryfikację izolowanej instalacji oraz eksportu z podpisem. Wszystkie 67 zasobów w pakiecie odpowiadało zawartości obszaru roboczego; archiwum źródłowe zawiera 253 publiczne pliki. Sprawdzanie źródeł i linków zakończyło się powodzeniem dla 1 346 lokalnych linków do dokumentacji.

Potwierdzenia: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` oraz `test-results/extras-artifacts.json`. Na zrzutach ekranu wykorzystano syntetyczne środowiska robocze.

## Audyt konfiguracji bota Witness i serwera proxy · 29 października 2026 r.

Konfiguracja narzędzia Witness (obecnie w menu **„Dodatki” → „Bot w Państwa kanale**”) przygotowuje niezależnie wdrożony moduł Witness: przypięty klucz kolektora, pobieranie tokenu o ograniczonym zakresie, własny kanał, polityka publikacji, trasa HTTP/SOCKS5 oraz niestandardowe API bota. Token bota pozostaje na serwerze świadka. Jego nowy `--check-config` weryfikuje konfigurację i pliki bez nawiązywania połączenia sieciowego ani tworzenia klucza. Ścieżki do plików JSON są rozpoznawane obok konfiguracji. Wszystkie warianty świadka Compose przekazują teraz ustawienia proxy HTTP oraz Bot API.

Ustawienia konta obsługują zarządzany przez operatora publiczny katalog MTProxy, niestandardowy podgląd linków proxy serwisu Telegram oraz istniejące pola ręczne. Odpowiedzi katalogu pomijają dane poufne; wybrana trasa jest zapisywana w skarbcu obszaru roboczego. Brakujące lub nieprawidłowo sformułowane katalogi pozostawiają dostępne trasy ręczne. Żadne adresy proxy projektu ani hostowana usługa świadka nie są domyślnie generowane ani włączane. Przykład Caddy udostępnia wyłącznie punkt końcowy typu „head” o ograniczonym zakresie, gdy zewnętrzny świadek musi połączyć się z kolektorem, którego panel pozostaje prywatny.

Weryfikacja:

- Pełny zestaw testów: **348 zaliczonych, 3 pominiętych**, 195,81 sekundy. Pominięcia wynikają z ograniczeń systemu Windows; utrzymują się dwa istniejące ostrzeżenia dotyczące wycofywania zależności.
- Ostateczny przebieg testów regresyjnych dotyczących świadków/konfiguracji/wydania: **11 zaliczonych, 1 pominięty**. Zakres ten pokrywa się z pełnym zestawem testów. Testy obejmują rozpoznawanie ścieżek, wstępną weryfikację w trybie offline, podpisywanie/publikowanie za pośrednictwem rzeczywistego elementu testowego typu loopback HTTP Bot API, odnotowane niepowodzenia dostarczenia, weryfikację tokenu kanału oraz wykluczenie tajnego klucza proxy.
- Test akceptacji konfiguracji Chromium zakończył się pomyślnie w języku angielskim/rosyjskim przy rozdzielczości 390/1440 pikseli: pobieranie przypiętych plików konfiguracyjnych i tokenów, czyszczenie tokenów po zablokowaniu, wybór katalogu, podgląd linków niestandardowych, a następnie jawne zapisanie, układ/kontrast oraz brak błędów JavaScript lub zewnętrznych żądań przeglądarki. Skorygowano wąski nagłówek konta w języku rosyjskim oraz przepełnienie zakładki logowania.
- Przeprowadzono weryfikację treści, sprawdzenie źródeł i linków oraz analizę pliku YAML dotyczącego tworzenia treści i przepływu pracy.
- Przebudowane narzędzie przeszło pomyślnie testy instalacji izolowanej, zasobów panelowych/statycznych oraz uwierzytelniania API, a także niezależną weryfikację bezpośrednich i przesyłanych strumieniowo syntetycznych eksportów obejmujących 32 zdarzenia.

Potwierdzenia: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` oraz `setup-package.log`. Testy te wykorzystują syntetyczne konta/serwery proxy oraz lokalną instalację Bot API. Nie zakładają one istnienia rzeczywistej publikacji bota, działającego publicznego serwera MTProxy, zdalnego uruchomienia CI ani wdrożenia w Dockerze. Zachowana powyżej rzeczywista historia obserwacji w Telegramie pozostaje odrębnym elementem dowodowym. [Instrukcje konfiguracji](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Przegląd prezentacji i dokumentacji · 29 października 2026 r.

Strona produktu, ekran logowania, pliki README w języku angielskim i rosyjskim oraz obrazy prezentacyjne mają teraz jednolity styl wizualny. Publiczne zrzuty ekranu wykorzystują fikcyjne dane demonstracyjne. W ramach przeglądu poprawiono również przestarzałe opisy dotyczące walidacji na żywo i odzyskiwania danych, o których mowa powyżej.

- Ukierunkowana lokalizacja oraz testy strony i publikacji: **33 zaliczone, 1 pominięty**. Pominięty test wymaga utworzenia dowiązania symbolicznego, co nie jest możliwe na tym serwerze.
- Przeprowadzono ogólną akceptację panelu Chromium, obejmującą wszystkie katalogi językowe, układ RTL, jasne/ciemne motywy, odpowiedni kontrast tekstu oraz przełączanie obszarów roboczych. Sprawdzanie tworzenia profilu oczekuje teraz na faktyczną odpowiedź HTTP przed sprawdzeniem wybranego obszaru roboczego.
- Ekrany dostępu w językach angielskim i rosyjskim przeszły testy układu i kontrastu w obu motywach przy rozdzielczościach 320, 390, 768, 850 i 1440 pikseli; przycisk przesyłania pozostaje w początkowym obszarze widocznym.
- Weryfikacja wyświetlania na stronach publicznych zakończyła się pomyślnie przy rozdzielczościach 320, 390, 768, 1024 i 1440 pikseli, z uwzględnieniem historii wiadomości, powiększanie zrzutów ekranu/klawisz Escape/powrót do fokusu, przechodzenie między zakładkami za pomocą klawiatury, odrzucanie zawartości schowka, podścieżki projektu, zredukowany ruch oraz rezerwowa wersja bez obsługi JavaScript. Nie zaobserwowano żadnych nieudanych żądań zasobów, żądań zewnętrznych ani błędów JavaScript.
- Przebudowane narzędzie przeszło test instalacji w środowisku izolowanym: zasoby panelu i ustawienia regionalne zostały załadowane, dostęp do API wymaga uwierzytelnienia, a eksporty bezpośrednie i strumieniowe niezależnie weryfikują wszystkie 32 syntetyczne zdarzenia. Testy Ruffa oraz sprawdzanie źródeł publicznych i linków zakończyły się powodzeniem.

Lokalne potwierdzenia: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` oraz `design-package/install-receipt.json`. W związku z niniejszą zmianą w prezentacji/dokumentacji nie przeprowadzono ponownego uruchomienia pełnego zestawu narzędzi zaplecza; poprzedni wynik pozostaje w audycie przed publikacją.

## Wersja 0.6.1

Wersja 0.6.1 wprowadza zmiany w wyglądzie panelu, programach uruchamiających, pakiecie instalacyjnym oraz dokumentacji; kod odpowiedzialny za gromadzenie, przechowywanie, podpisywanie i eksport danych pozostaje niezmieniony. W systemie Windows 11 / Python 3.12.10 z przypiętym środowiskiem uruchomieniowym:

- Pełny pakiet przeszedł **137 testów,** z **2 pominięciami** i istniejącym ostrzeżeniem dotyczącym biblioteki Starlette. Nowe testy obejmują obsługę skrótu klawiszowego Ctrl+C przez program uruchamiający (serwer otrzymuje 30 sekund na uporządkowane zakończenie działania) oraz błędy na etapie konfiguracji, które wymagają podjęcia działań.
- Chromium (powłoka bezinterfejsowa 156) przeszedł pomyślnie wszystkie **45 scenariuszy ogólnych** oraz **35 scenariuszy związanych z importem konta, kodami QR i kluczami uwierzytelniającymi**, w tym test kontrastu tekstu jednolitego, brak przesunięcia poziomego w rozdzielczościach 320–1440 px oraz widoczność pól pierwszego logowania przy rozdzielczościach 320/390 px. Nie zaobserwowano żadnych błędów JavaScript na stronie ani zewnętrznych żądań.
- `python start.py --setup-only` ponownie zainstalował pakiet w wersji 0.6.1, a `python start.py --check` zgłosił gotowość. Prawdziwy serwer `python -m tgwitness --demo` zwrócił panel, arkusz stylów, skrypt, logo, instrukcję oraz wersję `/api/status` 0.6.1; usunięty serwer `workspace.css` zwrócił kod błędu 404.
- `Start.cmd` wykrył instalację języka Python poza ścieżką PATH. Wobec braku dostępnego środowiska Python wyświetlił ofertę instalacji; po odrzuceniu instrukcji z podręcznika zakończył działanie w wersji 1. W ramach etapu pobierania z witryny python.org pobrano instalator w wersji 3.12.10, który przeszedł kontrolę Authenticode przeprowadzoną przez Python Software Foundation; sam instalator nie został uruchomiony na tym hoście.
- `start.sh`, bez użycia języka Python, wyświetlił wskazówkę instalacyjną i zakończył działanie 1. `scripts\Docker.cmd` oraz `scripts/docker-start.sh` zostały przetestowane na fałszywych plikach wykonywalnych `docker`: poprawna sekwencja wywołań, adres panelu i wyjście tokenu, brak komunikatu o powodzeniu po niepowodzeniu.
- `python tools/build_portable.py` skompilował pakiet dla systemu Windows o rozmiarze 18,8 MiB po zweryfikowaniu przypiętej sumy kontrolnej środowiska uruchomieniowego typu embeddable-runtime. Po rozpakowaniu do ścieżki zawierającej spacje i uruchomieniu z uwzględnieniem wyłącznie katalogów `C:\Windows` w zmiennej PATH, wbudowany moduł Python przeszedł test `TgWitness-Check.cmd`, udostępnił wersję demonstracyjną (32 zdarzenia) oraz aktywny obszar roboczy, a przeglądarka Chromium wyświetliła dziennik i panel szczegółów bez błędów JavaScript. Dane zostały zapisane w folderze `data` pakietu.
- `python tools/build_preview.py` wygenerowało archiwum źródłowe zawierające 110 plików. Próba testowa `git add` wykazała te same 110 plików, bez plików sesji, kluczy, baz danych, tokenów, logów ani plików eksportowych, bez lokalnych ścieżek bezwzględnych oraz bez ciągów znaków o charakterze poufnym.

W tej konkretnej serii kompilacji z dnia 27 października nie przeprowadzono: samej automatycznej instalacji w języku Python, kontroli kompilacji/konfiguracji Docker, uruchomień w systemach Linux/macOS ani nowego ćwiczenia z wykorzystaniem aktywnego konta. Rzeczywiste dowody z serwisu Telegram zostały zarejestrowane powyżej oraz w ramach wcześniejszych kontroli kont przedstawionych poniżej. Same definicje CI nie kwalifikują wykonania na platformie.

## Wersja 0.6.0

Najnowszy kompletny zestaw testów w trybie przypiętego środowiska uruchomieniowego w systemie Windows 11 / Python 3.12.10 przeszedł **135 testów**, z jednym**pominięciem**, w czasie 26,53 sekundy oraz z istniejącym ostrzeżeniem dotyczącym biblioteki Starlette. Pominięcie to wymaga uprawnień POSIX. Po dodaniu modułu renderującego kody QR do kontroli gotowości i pomiarów procesów, 8 powiązanych kontroli gotowości/środowiska pracy również zakończyło się powodzeniem.

Nowe obszary objęte dokumentacją obejmują schematy Telethon 7/8, schematy Pyrogram 2/3, kompletne klucze JSON oraz pliki JSON zawierające wyłącznie metadane, pliki kont zgodne/sprzeczne, kody dostępu TData, manipulacje sumami kontrolnymi i niebezpieczne ścieżki, konwersję w trybie offline/uwierzytelnioną w pamięci, sprawdzanie identyfikatorów kont online, powodzenie kodów QR/2FA/wygaśnięcie, unieważnienie nieaktualnych danych oraz izolację kont. Elementy testowe TData wykorzystują oddzielną implementację algorytmu AES-IGE do szyfrowania.

Chromium przeszedł pomyślnie **45 scenariuszy ogólnych** oraz **35 scenariuszy dotyczących importu konta, kodów QR i kluczy uwierzytelniających**, przy czym nie zaobserwowano żadnych błędów JavaScript na stronach ani żądań zewnętrznych. Nowe testy przeglądarek obejmują łącznie wszystkie cztery formaty danych wejściowych, chronione dane TData, metadane API, renderowanie kodów QR, wygaśnięcie/ponowne próby, uwierzytelnianie dwuskładnikowe (2FA), odrzucenie niewłaściwego konta, blokadę/anulowanie obszaru roboczego, responsywny układ strony oraz opóźnione odpowiedzi konwersji po wybraniu nowszego pliku.

Oba pakiety przeglądarek ponownie przeszły testy po wprowadzeniu zmian dotyczących logowania do konta. Konfiguracja na żywo otwiera formularz konta; tryb demonstracyjny otwiera przykładowy dziennik. Strona demonstracyjna „Konto” wyświetla instrukcje uruchamiania na żywo i ukrywa pola wprowadzania danych uwierzytelniających. Szczegółowe kontrole przy rozdzielczościach 320, 390 i 1440 pikseli potwierdziły, że pole liczbowe i główny przycisk mieszczą się na ekranie bez konieczności przewijania, pola API są początkowo zwinięte, a kontrast tekstu pozostaje czytelny. Elementy sterujące przechwytywania i weryfikacji pozostają zakryte po otwarciu nowych, rozwijanych sekcji.

Przepływ bezpośredni z wykorzystaniem klucza autoryzacyjnego (Auth Key) został przetestowany przy użyciu syntetycznych danych uwierzytelniających poprzez rzeczywiste punkty końcowe importu i autoryzacji. Sprawdzono następujące elementy: niekompletne klucze, brakujący DC, nieprecyzyjne identyfikatory użytkownika, niezgodność tożsamości konta, zapisane dane uwierzytelniające API, widoczny postęp żądania, czyszczenie tajnych danych oraz opóźnione odpowiedzi po edycjach lub zmianach metod. Wszystkie cztery metody logowania zostały sprawdzone przy rozdzielczościach 320, 390 i 1440 pikseli. Selektor plików wyświetla się przed wskazówkami dotyczącymi formatu, a przycisk „Połącz” mieści się w początkowym oknie wyświetlania o szerokości 844 pikseli przy zwiniętych ustawieniach API. W ramach tego testu akceptacyjnego interfejsu użytkownika nie podjęto próby rzeczywistej autoryzacji za pomocą klucza autoryzacyjnego.

Ponownie sprawdzono odświeżanie panelu przy użyciu obu pakietów przeglądarek: nie zaobserwowano żadnych błędów JavaScript na stronie ani żądań zewnętrznych. Pakiet funkcji konta obejmuje obecnie wklejanie jednej pary identyfikatora API i skrótu, odrzucanie nieprawidłowo sformułowanych lub wielokrotnych par bez zastępowania pól, wytyczne dotyczące wyłącznie metadanych oraz ignorowanie nieaktualnych odpowiedzi importu po zmianie metody logowania lub ręcznej edycji danych uwierzytelniających. Sześć dodatkowych ukierunkowanych testów zakończyło się powodzeniem w zakresie przewodnika konfiguracji, wyraźnego uruchamiania/wstrzymywania, przywracania po pustym wyszukiwaniu oraz ostatecznego układu połączenia/przewodnika lokalnego i wyraźnego kontrastu tekstu przy rozdzielczościach 320, 390 i 1440 pikseli. Aktualizacja dotycząca bezpośredniego logowania dodaje operację polegającą na podaniu numeru telefonu i żądaniu kodu oraz ponownie wykorzystuje zapisaną w bieżącym obszarze roboczym parę API do logowania za pomocą numeru telefonu, kodu QR oraz sesji. Pełny zestaw testów w języku Python wymieniony powyżej obejmuje nowe testy dotyczące trwałości, odrzucania częściowych danych uwierzytelniających oraz izolacji obszaru roboczego. Kontrole przeglądarki obejmują bezpośrednie wprowadzanie numeru telefonu, ponowne wykorzystanie zapisanych poświadczeń, kierowanie wyłącznie na podstawie metadanych, autoryzację plików jednym przyciskiem oraz odrzucanie zduplikowanych kont. Uproszczone formularze tokenu panelowego i numeru telefonu zostały również sprawdzone bez wstępnego przewijania przy rozdzielczościach 320, 390 i 1440 pikseli. Kontrola zgodności potwierdziła, że formularz bezpośredniego logowania za pomocą numeru telefonu może korzystać z wcześniejszych punktów końcowych konfiguracji/kodu, nawet gdy starszy proces nadal jest uruchomiony.

Jedno konto dostarczone przez użytkownika zostało sprawdzone oddzielnie, poza publicznymi zestawami testowymi. Dane wejściowe z Telethon, Pyrogram i TData wskazywały na tę samą autoryzację; dołączony plik JSON zawierał dane uwierzytelniające do API. Wszystkie cztery pliki zostały załadowane za pośrednictwem panelu w wersji 0.6.0, a serwis Telegram potwierdził oczekiwany numeryczny identyfikator konta. Pliki źródłowe pozostały niezmienione. Nie wybrano żadnych źródeł, a tryb obserwacji pozostawał wyłączony. Stanowi to przykład pojedynczego importu/logowania, a nie rzeczywistego gromadzenia danych, odzyskiwania ani wydajności.

Telegram wygenerował również prawdziwy kod QR, który został unieważniony przed zeskanowaniem. Pełny proces potwierdzenia za pomocą kodu QR oraz procedura uwierzytelniania dwuskładnikowego (2FA) zostały przetestowane przy użyciu syntetycznych klientów; potwierdzenie na urządzeniu mobilnym za pomocą prawdziwej aplikacji Telegram pozostaje odrębnym etapem akceptacji. W plikach publicznych nie zawarto żadnych rzeczywistych identyfikatorów kont, danych poufnych ani zrzutów ekranu.

Zakończono aktualizację programu uruchamiającego; kod źródłowy, zainstalowane metadane oraz wskaźnik gotowości wskazują wersję 0.6.0, z kodem QR 8.2 i pozytywnym wynikiem testu `pip check`. Zainstalowany moduł „wheel” obsługiwał panel i przewodnik, odrzucał nieautoryzowane żądania API oraz niezależnie weryfikował bezpośrednie i strumieniowe eksporty syntetyczne obejmujące 32 zdarzenia. Zaktualizowany przewodnik offline został sprawdzony przy rozdzielczościach 320, 390 i 1440 pikseli. Publiczne zrzuty ekranu pozostają syntetyczne.

Wersja źródłowa zawiera 107 plików z listy dozwolonych. Linki do lokalnej dokumentacji działają poprawnie. Kwestie dotyczące uruchamiania w środowisku Docker/Caddy, zdalnej integracji ciągłej (CI) i publikacji pakietów, środowiska uruchomieniowego ARM64, ciągłego gromadzenia danych oraz pełnej matrycy akceptacji Telegramu na żywo nie zostały tutaj uwzględnione.

## Wersja 0.5.1

W systemie Windows 11 / Python 3.12.10 pełny zestaw testów środowiska projektowego zakończył się powodzeniem: **94 testy zakończone sukcesem, 2 pominięte**, w czasie 31,21 sekundy, z istniejącym ostrzeżeniem dotyczącym biblioteki Starlette. Pominięcia wynikają z braku uprawnień POSIX oraz niemożności utworzenia dowiązań symbolicznych na tym hoście. Moduł testowy pobierania HTTP wyświetlił diagnostykę wątku żądania; wszystkie asercje zostały zaliczone. Niniejsze uruchomienie nie wyklucza występowania problemów z transportem na hoście.

Nowe testy pokrycia regresyjnego obejmowały odrzucone sesje StringSession, zmiany w kodzie i na kontach 2FA, anulowane wyszukiwanie tożsamości, oczekujące anulowanie logowania oraz aktualizacje za pośrednictwem zarejestrowanych modułów obsługi na klientach aktywnych, odrzuconych, zastąpionych i testowych. Tylko aktywny moduł zbierający przekazuje zdarzenia; zapisane dane uwierzytelniające i podpisana historia pozostają nienaruszone. Inne nowe kontrole obejmują wyszukiwanie Unicode po ponownym otwarciu bazy danych, uwzględnienie granic polityki monitorowania w Coverage oraz wykluczenia pakietów ze źródeł publicznych.

W ramach projektu `pythonw.exe` uruchomiono izolowany panel syntetyczny, zwrócono kod stanu HTTP 200, a dane diagnostyczne uruchomienia zachowano w `logs/server.log`. Dziennik nie zawierał wygenerowanego tokenu panelu ani zapisów dostępu HTTP. Test zakończył jedynie własny proces syntetyczny. Nie zarejestrowano żadnego zadania w Harmonogramie zadań; logowanie/wylogowanie, tryb uśpienia oraz przywracanie działania usługi pozostają odrębnymi kryteriami kwalifikacyjnymi.

Test zgodności z Chromium zakończył się pomyślnie **w 45 scenariuszach**, przy czym nie odnotowano żadnych błędów JavaScript na stronach ani żadnych zewnętrznych żądań. Nowe testy obejmują daty i godziny na osi czasu o rozdzielczości 601/768/850 pikseli, wersje robocze załączników podczas odświeżania statusu, nowsze edycje dokonywane podczas zapisywania, kasowanie wyników weryfikacji przy zmianie konta, opóźnione odpowiedzi weryfikacyjne po przejściu do innej strony i powrocie, a także wyraźne granice weryfikacji w momencie pojawienia się nowych zdarzeń. Skorygowano również odstępy między ikoną wyszukiwania a tekstem, a następnie ponownie uruchomiono pakiet przeglądarek.

Podczas uruchomienia w przeglądarce wykorzystano przypięte środowisko uruchomieniowe w `.venv` oraz istniejący, dostarczony przez system Playwright 1.62.0/Chromium, dodany po środowisku projektowym w ścieżce importu. Opcjonalna instalacja zależności programistycznych została przerwana z powodu powolnego pobierania Playwrighta; nie zakwalifikowano żadnej nowej wersji narzędzia przeglądarkowego. Normalny proces `python start.py --setup-only` zakończył aktualizację aplikacji. Kod źródłowy, zainstalowane metadane oraz znacznik programu uruchamiającego wskazują wersję 0.5.1; proces `pip check` zakończył się pomyślnie. Kontrole gotowości zakończyły się pomyślnie na nowej, nieużywanej ścieżce, przy czym utrzymano oczekiwane ostrzeżenie dotyczące lokalnego klucza sejfu.

Pakiet 0.5.1 został zainstalowany oddzielnie i poddany testom wstępnym: wszystkie zasoby paneli i przewodników zostały udostępnione, nieautoryzowany dostęp do API został odrzucony, a zarówno bezpośrednie, jak i przesyłane strumieniowo pliki ZIP zawierające 32 zdarzenia przeszły niezależną weryfikację. Pliki aplikacji zawarte w zainstalowanym pakiecie zostały porównane z kodem źródłowym. Publiczne archiwum źródłowe wykorzystuje wyraźną listę dozwolonych typów plików i odrzuca pliki źródłowe dołączone jako linki; materiały uruchomieniowe umieszczone w katalogach źródłowych są wykluczane przez testy regresyjne.

Podczas cyklu poprawek kodu wybór kodu publicznego oraz zbiór kandydatów w systemie Git zawierały 86 plików, bez uwzględnienia katalogów danych uruchomieniowych. Skanowanie pod kątem rozpoznawalnych wzorców kluczy prywatnych, tokenów GitHub, tokenów botów Telegramu oraz StringSession nie wykazało żadnych dopasowań. Jest to ograniczona kontrola wzorców, a nie kompleksowy audyt poufnych danych. Testy reguł ignorowania obejmują dwanaście typowych artefaktów związanych z kontami, danymi i eksportem. Pliki YAML dotyczące przepływu pracy, zgłoszeń i kompozycji oraz skrypt zadań systemu Windows zostały pomyślnie przeanalizowane. Lokalne linki do dokumentacji działają poprawnie.

Omówiono wszystkie siedem ustaleń z przeglądu z dnia 27 października. Realizacja procesu roboczego na GitHubie, środowisko uruchomieniowe Linux/macOS/Docker, rzeczywisty Telegram, zewnętrzna interoperacyjność z serwerami proxy/TSA oraz kwalifikacja pod kątem obciążenia ciągłego pozostają poza zakresem niniejszego lokalnego uruchomienia. Nie przeprowadzono publikacji repozytorium, rejestracji usługi ani gromadzenia danych z rzeczywistych kont.

### Aktualizacja dokumentacji w języku angielskim

Plik README, informacje dotyczące kont i sesji, procedura gromadzenia danych oraz dołączony przewodnik zawierają obecnie opisy obsługiwanych danych wejściowych, działania środowiska roboczego, zasad dotyczących zdarzeń oraz formatów eksportu w języku angielskim. Trzy publicznie dostępne zrzuty ekranu zostały zaktualizowane przy użyciu danych syntetycznych. W tym momencie zbiór zasobów publicznych zawierał 88 plików, w tym dwa nowe przewodniki. Wszystkie 131 lokalnych linków w 23 dokumentach Markdown działają poprawnie.

Po wprowadzeniu zmian w interfejsie i instrukcji obsługi test akceptacyjny Chromium ponownie zakończył się pomyślnie we wszystkich 45 scenariuszach; nie zaobserwowano żadnych błędów JavaScript na stronach ani zewnętrznych żądań. W ramach niniejszej aktualizacji dokumentacji i prezentacji nie przeprowadzono ponownego uruchomienia pełnego zestawu testów w języku Python; powyższy wynik 94 pomyślnych testów odnosi się do poprzedniego przebiegu testów po poprawkach w kodzie.

Przebudowane koło zostało zainstalowane w nowym, izolowanym środowisku testowym. Jego elementy panelowe i prowadzące działały prawidłowo, nieautoryzowany dostęp do API został zablokowany, a zarówno eksport bezpośredni, jak i strumieniowy przeszły niezależną weryfikację obejmującą 32 syntetyczne zdarzenia.

### Aktualizacja dotycząca instalacji i wdrożenia

Ukierunkowane testy instalatora, pakietu oraz gotowości przeszły pomyślnie **14 testów**, przy czym jeden test został pominięty z powodu braku możliwości utworzenia dowiązania symbolicznego. Testy natywnej otoczki obejmują ścieżki zawierające spacje, przekazywanie argumentów, tryby konfiguracyjne/demonstracyjne oraz propagację wyników wyjścia niezerowych. Kontrole w Git Bash sprawdzają działanie pomocnika powłoki Docker przy użyciu symulowanego demona, uwzględniając brak Docker, brak Compose, nieudane oczekiwanie na sprawdzenie stanu oraz pomyślne uruchomienie na alternatywnym porcie. Te symulowane kontrole nie potwierdzają zgodności środowiska uruchomieniowego Docker.

Kompletna kopia z otwartych źródeł została zainstalowana w nowym katalogu systemu Windows, którego ścieżka zawiera spacje. `scripts\Setup.cmd` utworzył nowe środowisko i zainstalował przypięte środowisko uruchomieniowe; `Start.cmd --check --json` zgłosił gotowość bez utworzenia docelowego katalogu danych. `pip check` przeszedł pomyślnie. Przebudowane koło również przeszło sprawdzenie zainstalowanego pakietu, w tym bezpośredni i strumieniowy eksport 32 zdarzeń.

Przeanalizowano składnię języka Shell oraz pięć plików YAML dotyczących przepływu pracy i konfiguracji Compose. Konfiguracje źródłowe i graficzne Compose są zgodne pod względem ustawień przechowywania danych i środowiska uruchomieniowego. Na tym etapie rozpoznano wszystkie 139 lokalnych odnośników w 23 dokumentach Markdown. Zbiór plików dostępnych publicznie zawiera 99 plików.

Definicje CI obejmują obecnie nową konfigurację natywną w systemach Windows/Linux/macOS, sprawdzanie stanu działania Compose, kontrolę dostępu oraz trwałość danych po odtworzeniu kontenera, a także konfigurację Caddy. Proces wydawania wersji uzależnia publikację od wyników tych kontroli oraz dodaje emulowany test ARM64 typu „smoke check”. Docker jest niedostępny na tym hoście: rzeczywiste wykonanie Compose/Caddy, wydawanie certyfikatów, wykonywanie kodu ARM64 oraz zdalny przepływ pracy/publikacja pakietów pozostają lokalnie bez zastrzeżeń. Kod aplikacji i interfejsu użytkownika nie uległ zmianie w wyniku tej aktualizacji; wcześniejsze pełne wyniki testów w języku Python oraz w przeglądarce nie zostały ponownie uruchomione.

## Wersja 0.5.0

Pełny zestaw testów „pinned-runtime” zakończył się powodzeniem: **81 testów zakończonych sukcesem, 1 pominięty**, w czasie 22,00 sekund, z istniejącym ostrzeżeniem dotyczącym biblioteki Starlette. Sprawdzanie uprawnień POSIX jest pomijane w systemie Windows. Nowe testy modułów obsługi wysyłają wiadomości, edycje, usunięcia z zakresem/bez zakresu, reakcje, aktualizacje uczestników oraz komunikaty usługi członkostwa zgodnie z różnymi politykami. Wyłączone kategorie nie generują odpowiadających im obserwacji na żywo; diagnostyka zasięgu oraz jawne migawki pozostają dostępne. Testy weryfikują trwałość zasad, separację obszarów roboczych, podpisane zapisy audytowe przed i po, zachowanie przy niezmienionych zasadach, ścisłą walidację oraz uwzględnienie w kolejnym potwierdzeniu przetworzenia.

Testy dostępu do wersji demonstracyjnej potwierdzają, że jej możliwości różnią się od skonfigurowanego tokenu panelu, nie umożliwia ona autoryzacji aktywnego obszaru roboczego, nie pozwala na zmianę ustawień gromadzenia danych oraz nie jest wydawana ani akceptowana w przypadku żądań zdalnych, przekazywanych, międzydomenowych lub zawierających nieprawidłowy adres hosta. Otwarcie zapisanej wersji demonstracyjnej bez wyraźnego oznaczenia „demo” nie powoduje automatycznego uzyskania dostępu.

Test akceptacji Chromium zakończył się pomyślnie w **39 scenariuszach**, w tym w przypadku lokalnego dostępu demonstracyjnego bez wprowadzania tokenu, monitorowania ustawień wstępnych, przejścia od wyboru źródła do polityki, niezależności poszczególnych kont oraz sprawdzania układu na komputerze stacjonarnym (320/390 pikseli) i kontrastu tekstu. Nie wystąpiły żadne błędy JavaScript na stronie. Żądania wstrzyknięte przez AdGuard pozostają w potwierdzeniu odbioru. Moduł testowy HTTP pobierania zarejestrował zresetowanie połączenia po tym, jak klient zamknął swoje połączenie; testy nadal zakończyły się powodzeniem. Nie jest to wynik z rzeczywistej usługi.

Standardowy program uruchamiający zaktualizował izolowane środowisko do wersji 0.5.0; wersje źródłowe i zainstalowane są zgodne, a test pip zakończył się powodzeniem. Istniejące szyfrowanie skarbca tajnych danych, odrzucanie błędnych lub brakujących kluczy oraz kontrole integralności podpisów i plików multimedialnych przeszły pomyślnie w pełnym zestawie testów. Nie zgłoszono wprowadzenia żadnego nowego szyfrowania treści wiadomości ani załączników przez aplikację.

Lokalna wersja demonstracyjna zostaje uruchomiona ponownie w celu udostępnienia zaktualizowanego interfejsu użytkownika. Istniejące syntetyczne zapisy zostają zachowane; zatrzymanie starego procesu demonstracyjnego działającego w tle powoduje utworzenie granicy trybu offline przy następnym uruchomieniu. Do tych sprawdzeń nie wykorzystuje się żadnych rzeczywistych sesji w aplikacji Telegram.

Uruchomiony panel pod adresem localhost:8787 wyświetlał wersję 0.5.0, automatyczny dostęp do wersji demonstracyjnej, pięć elementów sterujących monitorowaniem oraz 33 zachowane syntetyczne zdarzenia dziennika. Oddzielnie zainstalowany pakiet wheel w wersji 0.5.0 obsługiwał wszystkie zasoby panelu i przewodnika, blokował nieautoryzowany dostęp do API oraz generował zweryfikowany plik ZIP zawierający 32 zdarzenia, zarówno bezpośrednio, jak i za pośrednictwem narzędzia do pobierania strumieniowego. Wersje pakietów uruchomieniowych pozostają ustalone zgodnie z zapisem dla wersji 0.4.

## Wersja 0.4.0

Pełny zestaw testów w trybie przypiętym zakończył się sukcesem: **78 testów zakończonych pomyślnie, 1 pominięty**, w czasie 19,77 sekundy. Pominięta kontrola wymaga uprawnień POSIX; nadal występuje ostrzeżenie o wycofaniu z użycia modułu Starlette TestClient w wersji źródłowej. Nowe testy obejmują strumieniowe pobieranie/kierowanie do obszaru roboczego, nagłówki autoryzacyjne, odmowę nadpisania, przekierowania, skrócone odpowiedzi, ogłoszone/rzeczywiste limity rozmiaru, odczyty ograniczone, czyszczenie, systemy plików bez dowiązań twardych, błędy gotowości oraz tryby uruchamiania, które nie mogą instalować pakietów. Testy eksportu potwierdzają obecność plików tymczasowych lokalnych w obszarze roboczym oraz selektywne czyszczenie plików osieroconych.

Test zgodności z Chromium zakończył się pomyślnie we wszystkich 36 wymienionych scenariuszach, bez żadnych błędów JavaScript na stronie. Obejmuje on symulację logowania za pomocą telefonu/kodu/autoryzacji dwuskładnikowej (2FA), przekształcone sesje, dwa obszary robocze oraz oddzielne trasy/stany, obserwacje, podpisy, punkty kontrolne i żądania znaczników czasu, a ponadto:

- Układy dla komputerów stacjonarnych oraz o rozdzielczości 320/390 pikseli, brak przepełnienia w poziomie, widoczna nawigacja, a także pole do pierwszego logowania w początkowym obszarze widocznym o szerokości 844 pikseli.
- Tekst na jednolitym tle zapewnia kontrast zgodny z progami WCAG AA. Wyłączono elementy sterujące, przezroczystość oraz tła obrazkowe i gradientowe; nie jest to pełny audyt zgodności z WCAG.
- Rzeczywista lokalna odpowiedź na żądanie eksportu wygenerowana za pomocą symulowanego selektora plików systemu operacyjnego z możliwością zapisu, a następnie niezależna weryfikacja pliku ZIP; anulowanie nie powoduje wysłania żądania eksportu.
- Błąd zapisu powoduje przerwanie operacji wysyłania do miejsca docelowego; mechanizm awaryjny 128 MiB odrzuca zbyt dużą zgłoszoną odpowiedź bez przydzielania odpowiedniej przestrzeni na dane.
- Angielski przewodnik lokalny dotyczący wersji na komputery stacjonarne oraz obu wąskich formatów.

Okno dialogowe zapisywania w systemie operacyjnym oraz rzeczywiste zapisy w przeglądarce o wielkości wielu gigabajtów nie zostały zautomatyzowane ani poddane weryfikacji. Testy pobierania w języku Python wykorzystują ograniczone fragmenty danych i elementy testowe typu loopback. Pełna akceptacja wdrożenia z wykorzystaniem rzeczywistego serwisu Telegram pozostaje odrębną kwestią.

Standardowy instalator zaktualizował wersję `.venv` do 0.4.0. Metadane źródłowe i zainstalowane są zgodne; `pip check` przeszedł pomyślnie. `python start.py --check --json` zgłosił gotowość na nowej ścieżce syntetycznej bez tworzenia katalogu danych. Ostrzeżenie dotyczące przechowywania kluczy lokalnych pozostaje aktualne: dzienniki/pliki multimedialne nie są szyfrowane przez aplikację.

Plik wheel w wersji 0.4.0 został skompilowany i zainstalowany w oddzielnym katalogu. Wszystkie 23 pliki aplikacji są identyczne z plikami źródłowymi, bajt po bajcie. Zainstalowany pakiet udostępniał panel oraz angielską instrukcję obsługi i zasoby, blokował nieautoryzowany dostęp do API oraz wyeksportował syntetyczny plik ZIP zawierający 32 zdarzenia, który przeszedł weryfikację. Polecenie pobierania strumieniowego pobrało również niezależnie zweryfikowany plik ZIP z uruchomionej, zainstalowanej aplikacji.

Dokumentacja publiczna oraz lokalny przewodnik są w języku angielskim; linki do lokalnej dokumentacji działają poprawnie. PowerShell przeanalizował szablon zadania systemu Windows, a Python przeanalizował plik plist systemu macOS. Są to kontrole składniowe, a nie uruchomienie usługi. Nie zarejestrowano żadnego zadania ani usługi. Konfiguracja CI obejmuje obecnie kontrole gotowości, jednak zdalne CI nie zostało tutaj uruchomione.

Podczas ponownego uruchomienia przeglądarki w wersji 0.4 ponownie zaobserwowano wstrzyknięcie kodu przez AdGuard oraz błąd OSError 10022 związany z czyszczeniem gniazd asyncio w systemie Windows. Testy przeglądarki zakończyły się powodzeniem; te obserwacje środowiskowe są zachowywane, a nie traktowane jako stałe zachowanie aplikacji. Wstępne próby uruchomienia w piaskownicy OpenSSL/przeglądarki/pip zakończyły się niepowodzeniem; udane przebiegi kwalifikacyjne wykorzystywały zatwierdzone wykonanie poza piaskownicą.

## Wersja 0.3.1 zawiera poprawki zwiększające gotowość operacyjną

Przeprowadzono testy dotyczące uruchamiania, przechowywania dowodów oraz interfejsu API: **31 testów zakończyło się powodzeniem, 1 pominięto**, wystąpiło jedno ostrzeżenie z biblioteki Starlette. Pominięty test sprawdza uprawnienia katalogów zgodne ze standardem POSIX i nie może ustalić tych uprawnień na tym hoście z systemem Windows. Test dla starej wersji Pythona symuluje granicę między wersjami i importami; nie zainstalowano ani nie zakwalifikowano żadnego interpretera Pythona 3.10. Wyniki zestawu testów 0.3, który wcześniej zakończył się powodzeniem, przedstawiono poniżej; całego zestawu testów oraz scenariuszy przeglądarkowych nie uruchomiono ponownie w związku z tymi ukierunkowanymi zmianami.

Standardowy program uruchamiający zaktualizował środowisko lokalne do wersji 0.3.1; metadane źródłowe i zainstalowane są zgodne, a test pip zakończył się powodzeniem. Oddzielnie zainstalowany pakiet wheel w wersji 0.3.1 obsługiwał panel i zasoby, odrzucał nieautoryzowany dostęp do API oraz wygenerował zweryfikowany syntetyczny eksport zawierający 32 zdarzenia. Plik YAML opisujący przepływ pracy został przeanalizowany, jednak nie przeprowadzono nowej kontroli środowiska uruchomieniowego kontenera: nie było dostępne żadne nadające się do użytku lokalne środowisko uruchomieniowe Docker/Podman/Linux.

Proszę zapoznać się z [wynikami oceny gotowości](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) w zakresie pozostałych luk dotyczących użyteczności, działania w trybie rzeczywistym oraz platformy. Niniejsza poprawka nie rozszerza obsługi na dodatkowe systemy operacyjne.

## Wersja 0.3.0

Pełny zestaw testów w środowisku przypiętym (pinned-runtime) zakończył się powodzeniem: zaliczono **61 testów**, przy jednym ostrzeżeniu o wycofaniu biblioteki Starlette TestClient z poziomu upstream. Metadane środowiska uruchomieniowego wskazują wersje TgWitness 0.3.0 oraz python-socks 2.8.2; sprawdzenie pip zakończyło się powodzeniem. Test akceptacyjny w przeglądarce zakończył się powodzeniem bez błędów JavaScript na stronie.

Pakiet 0.3.0 został skompilowany i zainstalowany w oddzielnym katalogu pakietów. Obsługiwał panel i zasoby, odrzucał nieautoryzowane żądania API oraz wyeksportował syntetyczny dziennik zawierający 32 zdarzenia, który przeszedł niezależną weryfikację. Lokalne linki do dokumentacji działają poprawnie. Po korekcie normalizacji klucza podstawowego w MTProxy wszystkie dziewięć testów połączeń i bezpieczeństwa zostało pomyślnie powtórzonych.

Nowe informacje obejmują:

- Nazwa użytkownika i hasło SOCKS5 oraz połączenie HTTP CONNECT za pośrednictwem rzeczywistych serwerów testowych typu loopback; nieaktywny, skonfigurowany serwer proxy zwraca błąd zamiast przełączać się na serwer docelowy.
- Weryfikacja serwerów proxy, wybór protokołu transportowego MTProxy, odrzucanie fałszywych kluczy tajnych TLS, trwałość danych, izolacja obszaru roboczego, blokowanie zmian podczas obserwacji oraz wykluczanie kluczy tajnych ze statusu API i podpisanych zdarzeń.
- Konwersja schematów syntetycznych Telethon SQLite nr 7 i 8 w trybie tylko do odczytu; niezmieniony skrót źródła; odrzucenie innych formatów, widoków SQL oraz nierozliczonego pliku WAL.
- Zewnętrzny klucz główny do skarbca: różne klucze robocze wygenerowane na jego podstawie, pomyślne ponowne otwarcie, odrzucenie w przypadku nieprawidłowego lub brakującego klucza oraz brak domyślnej migracji istniejących lokalnych skarbców.
- Ustawienia proxy przeglądarki, czyszczenie danych uwierzytelniających, ujawnianie informacji dotyczących ochrony pamięci masowej, strona poświęcona połączeniom mobilnym, autoryzacja plików przekonwertowanych sesji, oddzielne ścieżki, oraz wszystkie omówione wcześniej scenariusze gromadzenia i eksportu danych przy użyciu fałszywego klienta Telegramu.

Podczas prac rozwojowych test pętli zwrotnej oczekiwał w nieskończoność na zamknięcie połączenia przez partnera; w innym przebiegu zaobserwowano zresetowanie połączenia w systemie Windows po nawiązaniu połączenia. Obecnie moduł testowy ogranicza całą wymianę danych i traktuje sygnał EOF lub zresetowanie po zakończonym nawiązaniu połączenia jako zamknięcie połączenia. Nadal wymagane są asercje dotyczące uzgadniania połączenia i uwierzytelniania. Nie wyklucza to działania prawdziwych dostawców usług proxy ani nie sugeruje stałej usterki w transporcie danych w aplikacji Telegram.

Opisana poniżej obserwacja żądania AdGuard nadal ma zastosowanie. Nie wykorzystano żadnego rzeczywistego konta w serwisie Telegram, proxy SOCKS/HTTP ani działającego serwera MTProxy. MTProxy ma charakter eksperymentalny, a sprawdzono jedynie wybrane opcje i weryfikację kluczy tajnych, a nie interoperacyjność w warunkach rzeczywistych. Nowe polecenia dotyczące kluczy zewnętrznych i konwersji sesji zostały przetestowane wyłącznie przy użyciu syntetycznych kluczy tajnych. Systemy Linux/macOS/Docker pozostają w tym zakresie bez zastrzeżeń.

Poniższy pomiar przepustowości dla wersji 0.2 nie został powtórzony i nie wolno go przedstawiać jako nowego testu porównawczego dla wielu kont/serwerów proxy w wersji 0.3.

## Wersja 0.2.0 – wersja bazowa

Sprawdzono w systemie Windows z wykorzystaniem języka Python w wersji 3.12.10. Nie podłączono żadnego rzeczywistego konta w serwisie Telegram.

| Sprawdź | Wynik |
| --- | --- |
| Pakiet narzędzi w języku Python | 52 testy zakończyły się powodzeniem w środowisku programistycznym i 52 w środowisku uruchomieniowym z przypiętą wersją; w każdym przebiegu pojawiło się jedno ostrzeżenie o wycofaniu biblioteki Starlette TestClient z głównego gałęzi projektu. |
| Składnia języka JavaScript | Zrealizowano przy użyciu Node.js |
| Zgodność z Chromium | Zaliczono; brak błędów JavaScript na stronie |
| Układ na komputery stacjonarne/urządzenia mobilne | Sprawdzono w rozdzielczościach 1440 × 1060 oraz 390 × 844; brak poziomego przepełnienia dokumentu |
| Treść wiadomości w formacie HTML | Wyświetlono jako tekst; wstawiony skrypt nie został wykonany |
| Przykładowy przebieg obsługi konta | Dane uwierzytelniające API → numer telefonu → kod → uwierzytelnianie dwuskładnikowe (2FA) → wybierz grupę → start → migawka → pauza → odśwież |
| Dowody w przeglądarce | Porównanie zmian, poprzednia treść po usunięciu, filtry, pobieranie plików ZIP, punkt kontrolny, podpisane potwierdzenie przetworzenia, pobieranie żądania zgodnego z RFC 3161 oraz powiązanie z punktem kontrolnym |
| Obsługa wielu kont | Oddzielne dzienniki, klucze, źródła i stany aktualne; zmiana przeglądarki nie powoduje zatrzymania działania pozostałych modułów zbierających dane; obszary robocze są ponownie otwierane po ponownym uruchomieniu; odrzucane są zduplikowane konta oraz próby ponownego przypisania kont |
| Awarie kryptograficzne | Zmieniono pola podpisane, dodano pola niepodpisane, błędny klucz, uszkodzony element archiwum, zmienione/brakujące pliki multimedialne, odrzucono skrócenie wykryte przez punkt kontrolny |
| Przechowywanie danych | Równoczesne dodawanie wpisów jest weryfikowane; aktualizacja lub usunięcie powoduje odrzucenie; program startowy odrzuca zmieniony dziennik bez dodania nowych wpisów i zwalnia jego blokadę |
| Trwałość nośników danych | Atomowe zapisy wiadomości/zadań; odzyskiwanie po ponownym uruchomieniu; zachowanie deskryptorów wersji oryginalnych; odrzucanie zastępowania kolejki i uszkodzeń istniejących plików; funkcja FloodWait zachowana; izolacja awarii źródeł |
| Transmisja na żywo | Stały prefiks jest eksportowany w miarę dodawania nowych wpisów; zachowany punkt kontrolny wykrywa niekompletny dziennik; eksport nie obejmuje całego strumienia zdarzeń |
| RFC 3161 | OpenSSL 3.5.9 odczytuje wygenerowane żądania; akceptowane są lokalnie wygenerowane syntetyczne odpowiedzi CA/TSA; odrzucane są zmodyfikowane dane, wartości nonce oraz nieprawidłowe certyfikaty CA; otoczenie certyfikatów CA nie zastępuje jawnie wyrażonego zaufania |
| Konfiguracja lokalna | Komenda `start.py --setup-only` zaktualizowała izolowane środowisko .venv do wersji 0.2.0; dane źródłowe i zainstalowane metadane są zgodne; test pip zakończył się powodzeniem |
| Wheel | Wersja 0.2.0 została skompilowana i zainstalowana oddzielnie w katalogu „test-results”; udostępniono elementy panelu i zasoby, zablokowano dostęp do API dla użytkowników nieautoryzowanych, wyeksportowano i zweryfikowano syntetyczne archiwum zawierające 32 zdarzenia |

W testach źródłowych wykorzystano FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 oraz Playwright 1.62.0. Zablokowane środowisko uruchomieniowe wykorzystuje FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 oraz cryptography 50.0.2. Plik deploy/constraints.txt zawiera informacje o przypisanych wersjach środowiska uruchomieniowego; pliki deploy/requirements.lock oraz deploy/build.lock zawierają skróty SHA-256 wszystkich plików pakietów, a serwery Docker oraz serwery o wysokim poziomie bezpieczeństwa instalują oprogramowanie wyłącznie na podstawie tych skrótów (pip --require-hashes). Żadne z powyższych nie stanowi dowodu zgodności na każdej skonfigurowanej platformie CI. Zdalna integracja ciągła (CI) nie została uruchomiona.

## Syntetyczny pomiar lokalnych możliwości

Polecenie: `python tools/check_capacity.py --events 10000 --chats 100`

| Metryka | Zaobserwowano |
| --- | --- |
| Dane wejściowe | 10 000 syntetycznych zdarzeń związanych z wiadomościami z 100 wybranych syntetycznych źródeł |
| Treść wiadomości | 400 znaków; bez multimediów ani odniesień do sieci |
| Przetwarzanie danych | 53,273 sekundy; 187,7 zdarzeń na sekundę |
| Opóźnienie obsługi | p50 4,162 ms; p95 7,784 ms; maksymalnie 129,118 ms |
| Eksport do pliku ZIP | 19,868 sekundy przy włączonej funkcji tracemalloc |
| Szczytowe wartości przydziałów eksportu w języku Python | 0,51 MiB; brak obsługi RSS |
| Rozmiar pliku ZIP | 4 610 962 bajtów |
| Niezależna weryfikacja | Wszystkie 10 000 zdarzeń zostało zweryfikowanych |

Niniejszy pomiar dotyczy lokalnej ścieżki zapisu/eksportu na tym hoście z systemem Windows. Nie obejmuje on dostarczania wiadomości za pośrednictwem protokołu MTProto, kont działających jednocześnie, ograniczeń przepustowości w serwisie Telegram, plików multimedialnych, długotrwałego obciążenia ani gwarantowanej liczby rzeczywistych czatów. Pomiar ten został przeprowadzony przed wprowadzeniem ostatecznej wersji narzędzia do generowania znaczników czasu w trybie offline, które nie zmienia mierzonej ścieżki wiadomości.

## Obserwacje środowiskowe

Ograniczenia środowiska izolowanego systemu Windows zablokowały domyślne katalogi tymczasowe pytest/pip oraz podproces Playwright. Pytest wykorzystywał nowy katalog tymczasowy wewnątrz projektu; procesy instalacyjne i przeglądarkowe wymagały zatwierdzonego uruchomienia poza środowiskiem izolowanym.

Program AdGuard zainstalowany na komputerze przekierował żądania do serwisu local.adguard.org w przeglądarce. W historii przeglądarki zachowały się te żądania. Niniejszy przebieg **nie** stanowi dowodu na brak żadnych żądań wychodzących w niezmodyfikowanym środowisku przeglądarki; sam kod źródłowy aplikacji nie zawiera żadnych żądań dotyczących zasobów zewnętrznych, sieci CDN ani narzędzi analitycznych. Ustawienia programu AdGuard nie zostały zmienione.

Podczas ostatniego uruchomienia przeglądarki odnotowano również błąd OSError 10022 związany z czyszczeniem gniazd asyncio w systemie Windows. Wszystkie testy przeglądarki zakończyły się powodzeniem i nie wystąpiły żadne błędy JavaScript na stronach. Przyczyna tego błędu nie została ustalona, a niniejsze uruchomienie nie wyklucza występowania problemów z transportem po stronie serwera.

Pierwsza sonda HTTP oparta na zainstalowanym pakiecie, wykorzystująca żądania typu „connection-close” biblioteki urllib, napotkała zresetowania połączeń zarówno wewnątrz, jak i na zewnątrz środowiska sandbox oraz w przypadku obu zestawów zależności. Ostateczna sonda wykorzystywała standardowe trwałe połączenia HTTP/1.1 za pośrednictwem http.client i zakończyła się powodzeniem. Żądania przeglądarki również przeszły pomyślnie. Nie ustalono dokładnej przyczyny zresetowań; nie uznano ich za stałą usterkę aplikacji.

## Pozostałe informacje

Zachowany dziennik na żywo dokumentuje faktyczne zdarzenia związane z gromadzeniem danych, edycjami, powiadomieniami o usunięciu, załącznikami, ponownymi weryfikacjami oraz obsługą ograniczeń szybkości. Nie obejmuje on jednak wyczerpujących danych dotyczących dostarczenia ani kontrolowanej matrycy widoczności ról, podmiotów reagujących, przedłużonego czasu oczekiwania (FloodWait), blokad kont oraz przywracania działania po przerwach w sieci lub procesach. Wydawanie tokenów QR pozostaje odrębne od zakończonego procesu potwierdzenia za pomocą mobilnego kodu QR.

Kompilacja i uruchamianie w Dockerze, instalacja w systemach Linux/macOS, obsługa długotrwałego wysokiego obciążenia, niezależny przegląd bezpieczeństwa, rzeczywista niezależna reakcja TSA, weryfikacja unieważnienia certyfikatów i archiwizacji oraz certyfikacja kryminalistyczna pozostają poza zakresem niniejszej kwalifikacji. Zaimplementowano zapis stanu MTProto oraz funkcję nadrabiania zaległości; nie ustalono jeszcze możliwości atomowego, trwałego odtwarzania. Gromadzenie logów administracyjnych, dodatkowe listy reaktorów oraz priorytetowe krótkie odpytywanie pozostają odrębnymi funkcjami. Proszę zapoznać się z [aktualną wersją](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) matrycy kwalifikacji kontrolowanych.

Szczegółowe lokalne zrzuty ekranu i kopie wiadomości znajdują się w katalogu test-results/ (ignorowanym przez Git). Publiczny zrzut ekranu w katalogu docs/assets/ zawiera wyłącznie fikcyjne dane demonstracyjne.

## Przygotowanie strony internetowej i publikacji · 27 października 2026 r.

Oddzielna prezentacja `website/` oraz kompilacja w formacie Pages zostały dodane po przeprowadzeniu powyższych kontroli panelowych. Nie wprowadzono żadnych zmian w konfiguracji konta produkcyjnego ani w logice gromadzenia danych.

- Istniejący pakiet aplikacji przeszedł pomyślnie testy: 138 testów zakończyło się sukcesem, 1 test dotyczący wyłącznie standardu POSIX został pominięty, a także pojawiło się jedno ostrzeżenie o wycofaniu biblioteki Starlette/httpx w wersji źródłowej. 11 dodanych testów kompilacji serwisu zakończyło się sukcesem niezależnie, w tym testy odrzucania nieoczekiwanych wyników oraz odrzucania powiązanych danych wejściowych.
- Oba skrypty przeglądarkowe aplikacji przeszły pomyślnie testy przy użyciu środowiska project-venv Playwright oraz powłoki bezinterfejsowej Chromium 156. Nie odnotowano żadnych błędów JavaScript na stronach ani żądań zewnętrznych. We wszystkich scenariuszach dotyczących kont wykorzystano fałszywy transport i fikcyjne dane.
- Test `tools/check_site.py` zakończył się powodzeniem przy szerokościach 320, 390, 768, 1024 i 1440, z podścieżką URL projektu, klawiszami tabulatora, pomyślnym/odmówionym dostępem do schowka, ograniczonym ruchem oraz wyłączoną obsługą JavaScript. Nie wystąpiły żadne nieudane żądania zasobów ani żądania zewnętrzne.
- `tools/build_site.py` wygenerowało 10 plików publicznych umieszczonych na liście dozwolonych, o łącznej wielkości około 460 KB. Zrzuty ekranu z przeglądarki oraz potwierdzenie transakcji znajdują się w pliku `test-results/site/`, który został pominięty.
- Plik wheel został pomyślnie utworzony po zainstalowaniu narzędzi setuptools/wheel przeznaczonych wyłącznie do kompilacji w środowisku projektowym. Instalacja w izolowanym środowisku docelowym oraz uruchomienie testu `tools/check_install.py` zakończyły się powodzeniem: zasoby statyczne, kontrola dostępu, podpisany eksport syntetyczny obejmujący 32 zdarzenia oraz niezależnie zweryfikowane pobieranie strumieniowe.
- Test `pip check` zakończył się powodzeniem. Skanowanie wzorców wybranych publicznie dostępnych kandydatów z repozytorium Git nie wykazało żadnych rozpoznawalnych bloków kluczy prywatnych, tokenów GitHub/bot/AWS, długich dosłownych przypisów tajnych ani znaczników konfliktów scalania. Nie stanowi to dowodu na brak wszystkich możliwych formatów tajnych danych. Sondaże dotyczące danych uruchomieniowych, sesji i kluczy zostały zignorowane przez system Git.
- Uwierzytelnianie za pomocą GitHub CLI było nieprawidłowe; nie skonfigurowano serwera zdalnego i nie istniało żadne początkowe zgłoszenie. Nie przeprowadzono żadnego przesłania, hostowanego przepływu pracy, wdrożenia Pages ani wydania. Kwalifikacja Docker oraz działającego Telegrama/platformy pozostają poza zakresem tej kontroli.

Na tym serwerze wystąpiła awaria blokady pobierania programu Playwright w systemie plików obszaru roboczego E:. Instalacja Chromium w środowisku `%LOCALAPPDATA%/tgwitness-playwright` oraz wykorzystanie tego samego `PLAYWRIGHT_BROWSERS_PATH` do przeprowadzenia testów zakończyły się powodzeniem. Jest to rozwiązanie tymczasowe dotyczące środowiska, a nie zmiana zależności uruchomieniowych aplikacji.

## Interaktywna dokumentacja i metadane strony internetowej · 29 października 2026 r.

Publiczna strona internetowa składa się z 12 angielskich stron HTML: strony głównej, spisu treści przewodników oraz dziesięciu przewodników. Zestaw zawiera 28 wyraźnie wymienionych plików prezentacyjnych o rozmiarze około 1,85 MB oraz nie zawiera żadnych danych zebranych przez narzędzie. Publiczna strona internetowa jest w języku angielskim; tłumaczenia aplikacji oraz przetłumaczone przewodniki w repozytorium są dostępne oddzielnie.

- Testy dotyczące witryny, publikacji źródłowej oraz granic wydania: **18 zaliczonych, 2 pominięte**. Pominięcia dotyczą tworzenia dowiązań symbolicznych w tym systemie plików Windows. Testy sprawdzają unikalne metadane stron, strony publiczne wyłącznie w języku angielskim, kanoniczne adresy URL, wszystkie wpisy w mapie witryny, lokalne zasoby/punkty kotwic, uporządkowaną nawigację oraz wykluczenie plików prywatnych.
- Zarówno `tools/check_site.py`, jak i `tools/check_docs_site.py` przeszły testy w przeglądarce Chromium przy rozdzielczościach 320, 390, 768, 1024 i 1440 pikseli w ramach podścieżki URL projektu. Sprawdzane elementy obejmują wszystkie 11 stron dokumentacji, wyszukiwanie i nawigację za pomocą klawiatury, działanie schowka (powodzenie/niepowodzenie) oraz czytelność treści bez obsługi JavaScript.
- Pięć zatwierdzonych interaktywnych przykładów: odtwarzanie/przechodzenie krok po kroku/wstrzymywanie/resetowanie wiadomości z ograniczonymi animacjami i zawieszeniem poza ekranem; oryginalne/zmienione/odtworzone/skrócone łańcuchy skrótów; decyzje świadka dotyczące akceptacji/cofnięcia/rozgałęzienia/braku odpowiedzi; oraz scenariusze dostarczenia kompletnego/opóźnionego/brakującego; a także mapa śledztwa łącząca fikcyjne obserwacje z różnych czatów według identyfikatora nadawcy, miejsca docelowego i skrótu załącznika. Elementy kontroli śledczej przeszły pomyślnie testy nawigacji klawiaturowej oraz testy rezerwowe bez obsługi JavaScript. Wyniki Wyniki algorytmu SHA-256 w przeglądarce zostały niezależnie porównane z wynikami algorytmu `hashlib` w języku Python oraz kanonicznym plikiem JSON. Przykładowy skrót zachował również swoją czytelność w trybie awaryjnym, gdy biblioteka Web Crypto była niedostępna.
- Wskaźniki dostarczalności i znaczniki wykresów zostały dostosowane do tabeli dostępnej dla użytkowników. Etykiety osi w wersji mobilnej zostały powiększone po weryfikacji wizualnej. Każdy przykład jest oznaczony jako ilustracyjny lub syntetyczny, a żaden z przykładów przeglądarkowych nie nawiązuje połączenia z serwisem Telegram.
- Nie odnotowano żadnych żądań zewnętrznych, nieudanych żądań HTTP ani błędów JavaScript. Zrzuty ekranu z wersji na komputery stacjonarne i urządzenia mobilne oraz potwierdzenia znajdują się w sekcjach `test-results/site/` i `test-results/docs-site/`. Indeks dokumentacji, przykłady wiadomości i skrótów, układ interfejsu Witness, wykres dostarczenia oraz mapa dochodzenia zostały sprawdzone w rozmiarach dostosowanych do komputerów stacjonarnych i urządzeń mobilnych.
- Weryfikacja publikacji zakończyła się pomyślnie dla 282 plików ze źródeł publicznych oraz 1 426 lokalnych linków do dokumentacji. Ruff pomyślnie przeszedł testy zmodyfikowanych narzędzi i testów strony w języku Python.
- `docs/HOW-IT-WORKS.md` zawiera uzupełnienie w formacie Markdown na GitHubie wraz z diagramami i wzorami w formacie Mermaid. `docs/INVESTIGATION.md` obejmuje zakres całego konta, pozyskiwanie historii poszczególnych czatów, profile użytkowników, odniesienia między czatami, osie czasu oraz zweryfikowane przekazywanie spraw. Jego etapy i ograniczenia zostały zweryfikowane pod kątem aktualnego zakresu, gromadzenia danych, dokumentacji, eksportu, kodu weryfikatora oraz kodu panelu. Nie sprawdzono renderowania hostowanego na GitHubie.

Jest to lokalna kontrola strony internetowej/dokumentacji. Nie zapewnia ona aktualnej weryfikacji działania serwisu Telegram ani nie potwierdza wdrożenia hostowanych stron, powodzenia zdalnej integracji z infrastrukturą (CI) ani indeksowania przez wyszukiwarki. Prosimy zapoznać się z [procedurą publikacji](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) oraz [uwagami dotyczącymi metadanych strony internetowej](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
