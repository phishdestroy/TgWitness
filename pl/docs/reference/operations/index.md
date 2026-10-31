# Procesy i operacje

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/operations/

Codzienne działanie panelu: tryby pracy, kategorie monitorowania, parametry, powiadomienia, eksport danych, tworzenie kopii zapasowych oraz pojemność.

W przypadku pierwszego połączenia proszę skorzystać z [kont i formatów sesji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/). Wyjaśnienie dotyczące zapisanych wersji, zasad dotyczących zdarzeń oraz luk można znaleźć w sekcji [„Jak działa gromadzenie danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/)”. Niniejszy przewodnik obejmuje codzienne działanie oraz odzyskiwanie danych.

## Przebieg pracy operatora

Schemat blokowy · Wybierz opcję przechowywania danych i zabezpieczenia klucza → Proszę otworzyć panel za pomocą tokenu; Proszę otworzyć panel za pomocą tokenu → Proszę wybrać obszar roboczy; Proszę wybrać obszar roboczy → Konfiguracja połączenia bezpośredniego lub przez serwer proxy; Konfiguracja połączenia bezpośredniego lub przez serwer proxy → Wprowadź numer telefonu lub wybierz pliki / kod QR; Wprowadź numer telefonu lub wybierz pliki / kod QR → Proszę sprawdzić tożsamość konta i wybrać grupy, do których ma Pan/Pani dostęp; Proszę sprawdzić tożsamość konta i wybrać grupy, do których ma Pan/Pani dostęp → Zapisz zasady dotyczące zdarzeń i załączników, a następnie rozpocznij monitorowanie; Zapisz zasady dotyczące zdarzeń i załączników, a następnie rozpocznij monitorowanie → Monitorowanie błędów, dostępu, kolejek i dysku; Monitorowanie błędów, dostępu, kolejek i dysku → Zachowanie niezależnych punktów kontrolnych; Zachowanie niezależnych punktów kontrolnych → Eksportowanie i weryfikacja materiałów · Wybierz opcjęprzechowywania danychi zabezpieczeniaklucza · Proszę otworzyć panelza pomocą tokenu · Proszę wybrać obszarroboczy · Konfiguracjapołączeniabezpośredniego lubprzez serwer proxy · Wprowadź numertelefonu lub wybierzpliki / kod QR · Proszę sprawdzićtożsamość konta iwybrać grupy, doktórych ma Pan/Panidostęp · Zapisz zasadydotyczące zdarzeń izałączników, anastępnie rozpocznijmonitorowanie · Monitorowanie błędów,dostępu, kolejek idysku · Zachowanieniezależnych punktówkontrolnych · Eksportowanie iweryfikacja materiałów

**Schemat w formie tekstowej**

1. Wybierz opcję przechowywania danych i zabezpieczenia klucza → Proszę otworzyć panel za pomocą tokenu
2. Proszę otworzyć panel za pomocą tokenu → Proszę wybrać obszar roboczy
3. Proszę wybrać obszar roboczy → Konfiguracja połączenia bezpośredniego lub przez serwer proxy
4. Konfiguracja połączenia bezpośredniego lub przez serwer proxy → Wprowadź numer telefonu lub wybierz pliki / kod QR
5. Wprowadź numer telefonu lub wybierz pliki / kod QR → Proszę sprawdzić tożsamość konta i wybrać grupy, do których ma Pan/Pani dostęp
6. Proszę sprawdzić tożsamość konta i wybrać grupy, do których ma Pan/Pani dostęp → Zapisz zasady dotyczące zdarzeń i załączników, a następnie rozpocznij monitorowanie
7. Zapisz zasady dotyczące zdarzeń i załączników, a następnie rozpocznij monitorowanie → Monitorowanie błędów, dostępu, kolejek i dysku
8. Monitorowanie błędów, dostępu, kolejek i dysku → Zachowanie niezależnych punktów kontrolnych
9. Zachowanie niezależnych punktów kontrolnych → Eksportowanie i weryfikacja materiałów

Uprawnienia, łączność sieciowa, dostęp do grupy oraz kompletność dostarczenia to odrębne właściwości. Zielony status połączenia nie oznacza, że wszystkie zdarzenia zostały zarejestrowane.

## Udostępnianie wyników pracy bez ujawniania klucza głównego

Funkcja „Open **Access”** umożliwia przydzielenie recenzentowi lub analitykowi własnego tokenu. Należy wybrać konta i czaty, do których będą mieli dostęp, a następnie zezwolić na przeglądanie, eksportowanie lub wykonywanie czynności operacyjnych. Operator, który uruchamia lub zatrzymuje gromadzenie danych, potrzebuje dostępu do całego obszaru roboczego; osoba sprawdzająca może mieć dostęp ograniczony do jednej rozmowy. Limity sesji, wygaśnięcie uprawnień oraz reguły dotyczące adresów IP są niezależne od autoryzacji konta w Telegramie. Zobacz [sekcję „Dostęp i uprawnienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/)”.

Proszę skorzystać z opcji **„Otwarte sesje”**, aby zakończyć połączenie, lub cofnąć dostęp, co spowoduje zakończenie wszystkich sesji. Konsola administratora łączy informacje o bieżącej aktywności procesów we wszystkich obszarach roboczych. Zamknięcie sesji nie powoduje zatrzymania gromadzenia danych.

## Tryby działania

| Tryb | Działanie | Zachowanie |
| --- | --- | --- |
| Wersja demonstracyjna | scripts\Demo.cmd lub `--demo` | Dane syntetyczne; połączenia z prawdziwymi kontami wyłączone |
| Uwaga | Rozpocznij obserwację | Rejestruj dostarczone aktualizacje dla wybranych źródeł |
| Migawka historyczna | Źródła → migawka historii | Do 500 aktualnych wiadomości; brak odtwarzania wszystkich przeszłych zmian |
| Pauza | Wstrzymanie obserwacji | Zatrzymanie gromadzenia danych przy jednoczesnym zachowaniu danych i zadań oczekujących w kolejce |
| Przegląd/przekazanie | Eksport | Pliki ZIP, JSONL/CSV/HTML, punkty kontrolne, potwierdzenia przetworzenia oraz żądania dotyczące znaczników czasu |
| Wiele kont | Obszary robocze lub górny przycisk „**+**” | Dowolna liczba oddzielnych obszarów roboczych w ramach jednego procesu |

Dostęp do lokalnej wersji demonstracyjnej otwiera się automatycznie bez konieczności ręcznego wprowadzania tokenu. Wykorzystuje on uprawnienie ograniczone do czasu trwania procesu, ważne wyłącznie w przypadku bezpośredniego dostępu typu loopback do izolowanej syntetycznej wersji demonstracyjnej; token panelu głównego nie jest ujawniany. Prawdziwe środowiska robocze oraz zdalny lub pośredni dostęp do wersji demonstracyjnej wymagają uwierzytelnienia za pomocą tokenu. Dostęp do wersji demonstracyjnej nie zapewnia uprawnień w aplikacji Telegram.

## Kategorie monitorowania

![Ustawienia monitorowania dla poszczególnych kont z wykorzystaniem syntetycznych danych źródłowych](https://phishdestroy.github.io/TgWitness/assets/sources.png)

W sekcji **Źródła → Ustawienia przechwytywania → Wybierz zmiany do zachowania** należy niezależnie zaznaczyć nowe wiadomości, edycje, powiadomienia o usunięciu, aktualizacje reakcji oraz zdarzenia związane z członkostwem. Ustawienie domyślne zachowuje wszystkie kategorie. Opcja **„Wiadomości, edycje i usunięcia”** zachowuje oryginalny kontekst, wyłączając jednocześnie oddzielne aktualizacje dotyczące reakcji i członków. Opcja **„Wszystkie widoczne działania”** przywraca wszystkie pięć kategorii. Ustawienia wstępne zmieniają formę; naciśnij **„Zapisz ustawienia monitorowania”,** aby zastosować zmiany.

Zapisana polityka ma zastosowanie do wszystkich wybranych źródeł w danym obszarze roboczym. Pozostałe obszary robocze zachowują własne ustawienia. Każda faktyczna zmiana jest rejestrowana wraz z podpisanymi wartościami „przed” i „po” ; aktualna polityka jest również uwzględniana w potwierdzeniach procesów oraz rekordach rozpoczęcia obserwacji. Wyłączenie kategorii nie powoduje usunięcia wcześniejszych obserwacji. Ponowne włączenie nie pozwala na odzyskanie pominiętych zmian. W tej wersji nie ma możliwości nadpisania kategorii na poziomie poszczególnych grup.

Należy pozostawić włączoną opcję rejestrowania nowych wiadomości, gdy istotna jest wcześniejsza treść: powiadomienie o usunięciu nie pozwala na odzyskanie tekstu, który nigdy nie został zarejestrowany. Zapisy operacyjne/dotyczące zasięgu oraz inne zdarzenia związane z obsługą grup są zawsze zachowywane. Wyraźne migawki historii są oddzielone od wyboru kategorii na żywo i mogą zawierać komunikaty serwisowe. Te opcje nie ukrywają metadanych dotyczących reakcji/członków osadzonych w obiekcie Telegramu, który został w inny sposób zarejestrowany.

W przypadku wstrzymania działania funkcji „migawka historii” załączniki mogą zostać umieszczone w kolejce. Należy rozpocząć obserwację, aby je przetworzyć. Umieszczenie w kolejce nie oznacza pobrania. Niedostępny plik oryginalny nie jest zastępowany nowszą, edytowaną wersją; wyniki są rejestrowane oddzielnie.

**Funkcja „Lock”** kasuje dostęp przeglądarki oraz pola tajne, ale pozostawia proces gromadzenia danych uruchomiony. Zamknięcie karty również nie powoduje zatrzymania procesu. Zatrzymanie procesu lub usługi w języku Python powoduje zatrzymanie gromadzenia danych niezależnie od stanu przeglądarki.

Usunięcie dodatkowego obszaru roboczego zatrzymuje działanie jego modułu zbierającego dane i usuwa dane lokalne. Jeśli zablokowany plik lub błąd systemu plików przerwie proces usuwania, panel zgłasza niepowodzenie i utrzymuje obszar roboczy na liście jako niedostępny (`DeletionPending`). Proszę zamknąć programy korzystające z jego plików i ponowić próbę **usunięcia**. Ponowne uruchomienie TgWitness pozostawia ten obszar roboczy w stanie zatrzymanym i nie odtwarza częściowo usuniętego dziennika ani kluczy. Pomyślne usunięcie zostaje zarejestrowane dopiero po usunięciu katalogu; oddzielnie wyeksportowane lub zarchiwizowane kopie pozostają podlegające własnym zasadom przechowywania danych.

## Powiadomienia

**Źródła** otwarte **→ Powiadomienia → Alerty i codzienne podsumowanie**. TgWitness wykorzystuje aplikację Apprise do wysyłania alertów do serwisów Matrix, Telegram, Discord, Slack, ntfy, poczty elektronicznej oraz innych obsługiwanych usług. Do jednego obszaru roboczego można dodać kilka miejsc docelowych.

1. W każdym wierszu proszę podać jeden adres docelowy Apprise. Proszę skorzystać z [katalogu usług i formatów adresów URL](https://appriseit.com/services/) odpowiednich dla Państwa usługi.
2. Proszę włączyć opcję **„Wysyłaj powiadomienia”**, a następnie wybrać alerty o problemach, zmiany w obserwowanych czatach oraz codzienne podsumowanie. Godzina podsumowania jest podawana według czasu serwera.
3. Proszę włączyć opcję **„Dołącz krótkie fragmenty”,** jeśli chcą Państwo, aby w powiadomieniach pojawiał się zapisany tekst z usuniętych i edytowanych wiadomości.
4. Proszę kliknąć **„Zapisz powiadomienia”**, a następnie **„Wyślij test”,** aby sprawdzić, czy wiadomość została dostarczona.

Aby skonfigurować własny odbiornik, proszę skorzystać z [webhooka JSON](https://appriseit.com/services/json/) firmy Apprise. Na przykład `jsons://notify.example.org/tgwitness` wysyła dane JSON przez protokół HTTPS do tego punktu końcowego. Jest to przykład fikcyjny; proszę zastąpić go własnym adresem docelowym.

Miejsca docelowe i ustawienia należą do wybranego obszaru roboczego. Powiadomienia o zmianach obejmują obserwowane źródła, w tym nowo dodane czaty. Dzwonek na górnym pasku wyświetla również ostatnie problemy i zmiany w czatach.

W wersji demonstracyjnej elementy sterujące powiadomieniami są widoczne, ale wysyłanie jest wyłączone. Skonfiguruj dostarczanie w rzeczywistym środowisku roboczym. Powiadomienia wykorzystują trasę Direct, SOCKS5 lub HTTP tego środowiska roboczego; MTProxy nie może ich przesyłać. Miejsca docelowe inne niż HTTP, takie jak SMTP, wymagają trasy bezpośredniej.

## Układ panelu

![Środowisko robocze Connection wykorzystujące dane syntetyczne](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Dziennik** zawiera obserwacje, funkcje wyszukiwania i filtry. Edycja powoduje wyświetlenie zarejestrowanych wersji; usunięcie powoduje wyświetlenie poprzedniej treści, o ile jest ona dostępna. Nieznane źródła są wyraźnie zaznaczone. Liczby są dostępne w **sekcji „Przegląd”**; szczegóły dotyczące pozyskiwania danych znajdują się w lokalnym przewodniku.

**Sekcja „Źródła”** zawiera zakres monitorowania (wybrane czaty, folder w aplikacji Telegram lub całe konto), dostępne czaty każdego typu, wybrane źródła oznaczone gwiazdkami priorytetowymi, ustawienia dotyczące załączników i ponownej weryfikacji oraz migawki historii. Źródła prywatne wybiera się na podstawie dialogu/identyfikatora bez publicznego linku. Status dostępu opisuje wynik ostatniej weryfikacji, a nie stałe uprawnienia.

**W sekcji „Czat” → „Osoby”** wyświetlana jest lista wszystkich osób, których wiadomości zostały zapisane; jeśli w danym czacie włączono wyświetlanie profili użytkowników, kliknięcie otwiera profil danej osoby wraz z linkami do wpisów w dzienniku.

**Witness** tworzy tokeny świadków z prawem tylko do odczytu, pokazuje, kiedy każdy ze świadków został ostatnio sprawdzony, oraz udostępnia polecenia i opcje umożliwiające uruchomienie jednego ([niezależnego) świadka](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/).

**Sekcja „Parametry”** zawiera wszystkie ograniczenia i tempo działania środowiska pracy, które nie zostały omówione na innych stronach: liczbę odczytywanych rozmów, częstotliwość ponownego odczytu listy czatów, interwały sygnałów kontrolnych i punktów kontrolnych, bufor startowy, sposób rozkładania żądań podczas ponownych sprawdzeń (pierwsze opóźnienie, liczba czatów na przejście, przerwa między czatami, odzyskane i ponownie żądane wiadomości), rezerwa miejsca na dysku, limity czasu i ponowne próby pobierania, kryteria wyszukiwania profili użytkowników (w tym własne wyrażenia regularne), rozmiar i częstotliwość powiadomień, limity migawek, plików ZIP i pobrań w przeglądarce, a także limity czasu i ponowne próby klienta Telegram. Każde pole wyświetla swój zakres i wartość domyślną; zmienione pola są oznaczone i można je przywrócić pojedynczo lub wszystkie naraz. Każda zmiana jest rejestrowana jako „`parameters.changed`” wraz z wartościami przed i po zmianie, a zapisy rozpoczęcia obserwacji podają aktualne wartości. Wartości obowiązują od momentu ich następnego użycia; limity czasu i ponowne próby klienta – od następnego połączenia. Interwały ponownej weryfikacji, typy i rozmiary załączników, dowody oraz interwały tworzenia kopii poza serwisem pozostają na osobnych stronach i mogą przyjmować dowolną wartość z podanego zakresu, a nie tylko wartości domyślne.

Dzwonek na górnym pasku wyświetla listę najnowszych problemów i zmian w obserwowanych czatach; wiadomości nieprzeczytane są zliczane do momentu oznaczenia ich jako przeczytane. Zmiany są pogrupowane według czatów i godzin („12 usuniętych, 1 edytowana, 0 nieznalezionych”), a problemy, takie jak wylogowanie lub zapełnienie dysku, pozostają na liście niezależnie od tego, jak intensywna jest aktywność na czatach.

**Rejestracja** rozpoczyna się od pola numeru telefonu. **Kontynuacja** prowadzi bezpośrednio do wprowadzenia kodu, a o podanie danych uwierzytelniających API prosi się wyłącznie w przypadku ich braku. Kody QR i import plików to alternatywne zakładki. Zapisane dane uwierzytelniające API są ponownie wykorzystywane wyłącznie w ramach danego obszaru roboczego. Ekran rejestracji nie zawiera paska bocznego, statystyk ani sekcji konfiguracyjnych. Ikona **„Ustawienia**” otwiera opcje kontroli API, serwera proxy, pamięci oraz dodatkowych kont. Nowe instalacje rozpoczynają się tutaj; połączone konta bez wybranych źródeł rozpoczynają się od opcji **„Wybierz czaty**”. Zmiana ścieżki wymaga wstrzymania obserwacji i powoduje anulowanie niedokończonego logowania. Istniejącego dziennika nie można w sposób automatyczny powiązać z innym kontem w aplikacji Telegram.

**Funkcja eksportu** sprawdza integralność dziennika i generuje pliki przenośne. Identyfikator obszaru roboczego można przekazać do interfejsu wiersza poleceń (CLI) służącego do pobierania. Każdy eksport przypisuje prefiks pełnego dziennika; późniejsze zdarzenia trafiają do kolejnego eksportu. Filtry wyszukiwania nie zmieniają zakresu pakietu. Szczegółowe informacje dotyczące podpisywania i zakresu znajdują się w sekcji **„Weryfikacja i ograniczenia**”.

Panel w sekcji „Stan kolektora” przedstawia stan kolektora, pliki multimedialne w kolejce lub z niepowodzeniem, najstarsze pliki multimedialne oczekujące, wolne miejsce na dysku, wstrzymania żądań oraz źródła, do których dostęp nie został potwierdzony w **sekcji „Stan kolektora**”. Szczegóły te są początkowo zwinięte i ukryte w sekcji „Konto”. Karta konfiguracji przedstawia kolejny krok: podłączenie konta, wybór źródeł lub rozpoczęcie monitorowania. Lista kont stanowi migawkę z momentu ładowania; wybrany obszar roboczy jest okresowo odświeżany. Nie jest to wieloprocesowy monitor SLA.

Interfejs użytkownika wykorzystuje lokalne zasoby oraz renderowanie tekstu dla treści źródłowych. Przetestowano układy dla komputerów stacjonarnych oraz wąskich okien przeglądarki Chromium. Nie jest to pełna certyfikacja dostępności; ocena użyteczności dla czytników ekranu oraz dla użytkowników pozostaje odrębnym zadaniem.

## Środowiska wdrożeniowe

| Środowisko | Instalacja | Status weryfikacji |
| --- | --- | --- |
| Komputery PC z systemem Windows / serwery | Python 3.11+, skrypty w katalogu Setup.cmd/Start.cmd, prywatny katalog danych | Sprawdzono lokalnie w systemie Windows z wykorzystaniem języka Python 3.12 |
| Serwer Linux/VPS | Środowisko venv w języku Python, dedykowany serwer, protokoły HTTPS/SSH | Podano przykładowy kod, CI oraz systemd; nie są one uruchamiane na tym serwerze |
| macOS | Środowisko venv w języku Python, proces działający w tle lub agent użytkownika | Podano przykładowy plik launchd; konieczna jest oddzielna weryfikacja instalacji |
| Docker/Compose | Stała wydajność, jeden pracownik | Zawiera definicję oraz funkcję sprawdzania środowiska uruchomieniowego CI; Docker niedostępny lokalnie |
| Przeglądarka w telefonie | Proszę połączyć się z chronionym panelem na uruchomionym serwerze | Przetestowano wąski układ oparty na silniku Chromium; narzędzie do gromadzenia danych nie działa na systemach iOS ani Android |

Przenośność oznacza brak konieczności korzystania z usługi w chmurze ani tworzenia interfejsu użytkownika. Każdy komputer docelowy nadal wymaga kompatybilnych zależności języka Python i bibliotek kryptograficznych, a także dostępu do dysku lokalnego i sieci. Proszę zapoznać się z [plikiem DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/) oraz [szablonami usług](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Środowiska robocze współdzielą procesor, pamięć oraz pętlę zdarzeń. W celu izolacji procesów należy stosować odrębne instancje, porty, katalogi danych oraz uprawnienia do kont. Nie istnieje ujednolicony panel obejmujący oddzielne instancje. Nigdy nie należy kierować kilku procesów roboczych do jednej bazy danych.

## Sprawdzanie i eksportowanie danych

Przed uruchomieniem przygotowanego środowiska należy wykonać polecenie `python start.py --check`. Należy dodać `--json` w celu przeprowadzenia kontroli nadających się do odczytu maszynowego lub przekazać zamierzone wartości `--data-dir`, `--host` i `--port`. Polecenie to sprawdza warunki wstępne bez konieczności logowania się do serwisu Telegram ani tworzenia dziennika. Nie weryfikuje ono dziennika ani nie potwierdza gotowości do przechwytywania danych; weryfikacja dziennika odbywa się podczas uruchamiania aplikacji. Zajęty port może po prostu oznaczać istniejącą instancję.

Przeglądarki obsługujące interfejs API dostępu do systemu plików zapisują eksportowane dane za pośrednictwem strumienia z prawem zapisu. Inne przeglądarki buforują maksymalnie 128 MiB. W przypadku większych eksportów lub przeglądarek nieobsługujących strumieniowania plików należy skorzystać z interfejsu CLI do strumieniowania:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Proszę dodać `--profile ID` z sekcji „Exports” dla podprzestrzeni roboczej. W celu uzyskania zdalnego dostępu należy użyć `--url https://server` . Zwykły protokół HTTP jest akceptowany wyłącznie w przypadku adresów docelowych typu loopback. Token jest odczytywany z pliku i wysyłany w nagłówku; nie jest wyświetlany ani umieszczany w adresie URL. Przekierowania są odrzucane. Istniejące adresy docelowe nie są nadpisywane. W przypadku nieudanych transferów usuwany jest tymczasowy plik częściowy. Zgłoszony kod SHA-256 stanowi sumę kontrolną transferu; prosimy o oddzielną weryfikację podpisanego pliku ZIP za pomocą zaufanego odcisku palca/punktu kontrolnego.

## Tworzenie kopii zapasowych, przywracanie danych i przerwy w działaniu

1. Wstrzymaj obserwację i zakończ proces w sposób uporządkowany.
2. Skopiuj cały katalog danych: bazy danych, pliki WAL/SHM (jeśli występują), pliki multimedialne, `credentials.enc`, `signing.enc`, `network.enc`, klucze sejfu/metadane, token, punkty kontrolne oraz każdy katalog `profiles/`.
3. W trybie klucza zewnętrznego należy oddzielnie przechowywać klucz główny oraz zachować każdy klucz `vault.external.json`. Wygenerowanie nowego klucza nie pozwala na odzyskanie starych tajnych danych.
4. Proszę przywrócić dane, gdy miejsce docelowe jest zatrzymane; skonfigurować oryginalny klucz, ograniczyć dostęp oraz zweryfikować integralność przed wznowieniem.
5. Należy odnotować przerwy w działaniu oraz wyniki weryfikacji. Migawka historii nie może stanowić dowodu na to, że podczas przerwy nie doszło do usunięcia żadnych wiadomości.

Pliki ZIP z dowodami nie zawierają kluczy sesji ani kluczy prywatnych i nie stanowią pełnych kopii zapasowych serwisu. Cztery rodzaje danych są chronione w różny sposób:

| Co | Ochrona |
| --- | --- |
| Eksportowanie plików bez hasła (ustawienie domyślne) | Nie jest zaszyfrowany. Jest podpisany, dzięki czemu zmiany są wykrywalne, ale każdy, kto posiada ten plik, może go odczytać. |
| Eksport plików z hasłem | W przypadku ustawienia hasła gotowy plik eksportu zostanie zapisany bez zmian w formacie ZIP z szyfrowaniem AES-256 za pomocą programu WinZip, który można otworzyć za pomocą programów 7-Zip i WinRAR; hasło nie jest zapisywane ([zgodnie z zasadami postępowania z materiałami dowodowymi](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)) |
| Baza danych dziennika oraz załączniki zapisane na dysku | Dane nie są szyfrowane przez TgWitness; prosimy o korzystanie z szyfrowanego dysku lub partycji |
| Sesje w Telegramie i klucze podpisujące | Zaszyfrowane w katalogu danych (`credentials.enc`, `signing.enc`, `network.enc`) |

Pełna kopia zapasowa to opisany powyżej katalog danych zatrzymanych, a nie eksport. W obu przypadkach należy stosować zabezpieczoną pamięć masową oraz przemyślany mechanizm transferu. Tymczasowe eksporty serwerowe są przechowywane w katalogu `temporary-exports/` każdego obszaru roboczego; zakończone odpowiedzi są usuwane, a pliki przerwanych eksportów są usuwane przy następnym uruchomieniu, podczas gdy instancja tego obszaru roboczego pozostaje zablokowana.

Przywrócenie połączenia nie gwarantuje odzyskania zmian wprowadzonych w międzyczasie. Trwałe zadania związane z multimediami oraz stan aktualizacji aplikacji Telegram pozostają zachowane po ponownym uruchomieniu; proszę zapoznać się z [formatem dowodów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Pojemność i okres przechowywania

Domyślne limity, które można zmienić w **sekcji „Parametry**”: pierwsze 1 000 rozmów, 500 wiadomości na zrzut, 4 GiB nieskompresowanej, podpisanej zawartości pliku ZIP (większe archiwa wymagają `verify.py --max-gib N`) oraz 128 MiB rezerwy dla przeglądarki. Załączniki zajmują od 1 do 2 000 MiB na typ w sekcji **Źródła → Załączniki**. Domyślna wartość dla interfejsu CLI pobierania wynosi 5 GiB przesłanych danych. Dostępna przestrzeń dyskowa może stanowić dolną granicę. Należy zarezerwować miejsce na dzienniki, multimedia, pliki WAL, tymczasowe eksporty oraz kopie zapasowe. Eksporty wykorzystują objętość danych zamiast wartości 512 MiB określonej w opcji „`/tmp`” w sekcji „Compose”.

Należy mierzyć liczbę zdarzeń na sekundę, wiek kolejki, liczbę bajtów multimediów oraz opóźnienie dysku, a nie ograniczać się wyłącznie do zliczania grup. Syntetyczne testy porównawcze w środowisku lokalnym nie gwarantują dostarczenia wiadomości w Telegramie. Nie ma automatycznego usuwania danych po upływie okresu przechowywania. Usunięcie końcowej części dziennika unieważnia jego powiązanie z zachowanymi punktami kontrolnymi.

Istnieją już priorytetowe weryfikacje: źródła oznaczone gwiazdką są domyślnie weryfikowane co 15 minut, pozostałe co 6 godzin (patrz [poziomy weryfikacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/#recheck-tiers)). Istnieje możliwość eksportu chronionego hasłem, zgodnie z powyższym opisem. Akceptacja danych z Telegrama/proxy w czasie rzeczywistym, trwałe odtwarzanie, dziennik administratora i sondaż reakcji, izolowane procesy robocze, szyfrowanie lokalnego dziennika i multimediów przez sam TgWitness oraz niezależna weryfikacja pozostają odrębnymi zadaniami. Dostęp z ograniczeniami zakresu jest udokumentowany w sekcji [„Dostęp i uprawnienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/)”. Zobacz pl [iki READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) oraz [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/).
