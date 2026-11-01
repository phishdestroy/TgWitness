# Funkcje i ograniczenia

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/features/

Co narzędzie TgWitness obecnie realizuje, jakie ograniczenia nakłada platforma Telegram oraz jakie zadania pozostają do wykonania w przyszłości.

Odniesienie projektowe: 26 października 2026 r. Głównym przypadkiem użycia są prywatne grupy i kanały w aplikacji Telegram, do których dostęp mają połączone konta. Niniejszy dokument rozróżnia zrealizowane zachowania, ograniczenia platformy oraz przyszłe działania. Pozycja dotycząca architektury docelowej nie oznacza twierdzenia, że dana funkcja już istnieje.

## Aplikacja samodzielna

TgWitness posiada własną instalację, katalog danych oraz cykl życia wersji. Dołączony interfejs internetowy obsługuje konfigurację i przeglądanie; wyeksportowane zapisy mogą być wykorzystywane niezależnie.

Użytkownik łączy swoje konta, wybiera źródła widoczne dla każdego z nich i uzyskuje zapisany dziennik obserwacji. Panel przedstawia treść, zapisane zmiany, pochodzenie obserwacji oraz znane luki. Inny śledczy może zweryfikować wyeksportowany materiał.

Istotne znaczenie mają cztery odrębne stany: autoryzacja konta, dostęp do źródła, działający moduł zbierający oraz stopień, w jakim ustalono kompletność dostarczania. Żaden z pierwszych trzech stanów nie dowodzi automatycznie czwartego. Cicha grupa niekoniecznie oznacza, że moduł zbierający nie działa.

## Wspólne dochodzenia

Administrator może wydawać [tokeny dostępu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/) ograniczone do przestrzeni roboczych i poszczególnych czatów, z siedmioma uprawnieniami, ograniczeniami adresów IP, terminem ważności, limitami logowań oraz kontrolą sesji. Osoba sprawdzająca z uprawnieniami wyłącznie do odczytu może zapoznać się ze sprawą bez konieczności uzyskania autoryzacji w Telegramie ani klucza do panelu głównego. Dostęp ograniczony do czatu pozostaje oddzielony od ustawień obejmujących całe konto oraz eksportów pełnego dziennika.

Automatyczny MTProxy utrzymuje działające trasy Telegramu z czterech źródeł publicznych lub katalogu operatora. [Tryby IP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes) określają, czy w przypadku awarii należy czekać na inny serwer proxy, czy też można skorzystać z wyraźnie dozwolonej trasy bezpośredniej. Zewnętrzne żądania HTTP mają oddzielną trasę oraz opcję wyłączenia.

## Narzędzia archiwizacyjne

[Funkcje pozyskiwania historii](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/), [wyszukiwania i analizy archiwów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/),[MCP tylko do odczytu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/), [lokalne OCR/transkrypcja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/) oraz[wychodzące webhooki](https://phishdestroy.github.io/TgWitness/pl/docs/reference/webhooks/) są dostępne na stronie 0.7.1. Raporty analityczne i rozpoznany tekst pozostają oddzielone od zarejestrowanych zdarzeń.

## Opcjonalne dodatki

Codzienna konfiguracja to: konto → źródła → obserwacja. **Sekcja „Dodatki”** to osobna sekcja zawierająca bota Telegram Witness oraz podgląd przechwytywania na GitHubie. Każda z nich podaje informacje o dostępności i wymaganiach przed wyświetleniem ustawień. Wybranie karty otwiera instrukcje; nie powoduje to rejestracji ani uruchomienia usługi.

Konfiguracja bota składa się z trzech kroków: utworzenia dostępu tylko do odczytu, wyboru ustawień publikacji oraz uruchomienia na hoście Witness. Opcje sieciowe i publikacyjne, istniejące połączenia oraz polecenia weryfikacyjne są udostępniane na żądanie. Pobrana konfiguracja różni się od uruchomionego serwera świadka. Zmiana dodatków powoduje zachowanie wersji roboczej; zmiany na koncie i zablokowanie powodują wyczyszczenie tymczasowego tokenu i formularza. Wbudowany przewodnik zawiera instrukcje uruchamiania. [GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)uruchamia przypięty moduł zbierający z Twojego forku, przechwytuje jedną rozmowę i generuje zaszyfrowane przekazanie wraz z pochodzeniem przepływu pracy.

## Protokół i źródła prywatne

**MTProto to protokół serwisu Telegram; Telethon to biblioteka języka Python, z której korzysta TgWitness w celu komunikacji za pomocą protokołu MTProto.** Nie są to alternatywne metody połączenia. Funkcja „Collection” wykorzystuje protokół MTProto; opcjonalny moduł „witness” publikuje podpisane raporty weryfikacyjne za pośrednictwem interfejsu API bota.

Każdy obszar roboczy posiada własnego autoryzowanego klienta oraz strumień aktualizacji konta. TgWitness wybiera obserwacje ze skonfigurowanych źródeł i wysyła oddzielne, wyraźne żądania dotyczące takich funkcji, jak migawki historii oraz pobieranie plików multimedialnych.

Prywatne źródło nie wymaga publicznej nazwy użytkownika. Identyfikatorami są typ węzła w sieci Telegram oraz identyfikator numeryczny; tytuły i nazwy użytkowników mogą ulegać zmianom. Dostęp zależy od aktualnego członkostwa i uprawnień. TgWitness nie dołącza automatycznie do źródeł ani nie omija procesu zatwierdzania dołączenia. Skrót dostępu z innego konta nie stanowi uniwersalnego tokenu dostępu.

Model gromadzenia danych musi uwzględniać ukrytą historię sprzed dołączenia do grupy, role uczestników/administratorów, unieważnienie sesji, usunięcie lub zmianę uprawnień, migrację z grupy do supergrupy, tematy/fora, powiązane dyskusje, tożsamości kanałów oraz niedostępne załączniki. Nie każda kombinacja została jeszcze przetestowana w warunkach rzeczywistych.

Widoczność źródła jest sprawdzana przy uruchomieniu modułu zbierającego. Brak źródła w ograniczonym wyniku dialogu oznacza, że **dostęp nie został potwierdzony**, a nie że usunięcie zostało udowodnione. Jedno niedostępne źródło nie uniemożliwia obserwacji innych dostępnych źródeł. Nigdy nie umieszczaj linków zaproszeniowych ani prawdziwych sesji w publicznych zestawach danych.

## Wiele kont

Panel obsługuje dowolną liczbę **obszarów roboczych**, z których każdy posiada:

- Autoryzacja, zaszyfrowany sejf oraz trasa połączenia.
- Dziennik w formacie SQLite oraz tożsamość podpisująca Ed25519.
- Wybrane źródła, kolejka mediów oraz ustawienia przechwytywania.
- Stan obserwacji, błędy, punkty kontrolne i eksporty.

Zmiana wyświetlanego obszaru roboczego nie powoduje zatrzymania działania innego modułu zbierającego dane. Podwójna autoryzacja konta w różnych obszarach roboczych jest odrzucana. Dziennik już powiązany z jednym kontem w Telegramie nie może zostać przypisany do innego; dozwolone jest ponowne połączenie tego samego konta. Pozwala to zachować tożsamość konta oraz odpowiedni zakres identyfikatorów wiadomości.

Nie ma ustalonej liczby ani gwarancji mierzonej przepustowości. Obszary robocze współdzielą proces w języku Python oraz pętlę zdarzeń. Oddzielne procesy obsługujące konta pozostają zadaniem na przyszłość. W celu obecnej izolacji procesów należy stosować oddzielne instalacje, porty i katalogi danych.

Należy przypisać każdemu kontu źródła, do których ma ono dostęp. Różne konta mogą obserwować tę samą grupę, jednak ich obserwacje pozostają oddzielne i zachowują swoje pochodzenie. Dwa konta na jednym urządzeniu kontrolowanym przez operatora nie stanowią dwóch niezależnych świadków. Eksporty są prowadzone na poziomie obszaru roboczego; nie zaimplementowano funkcji scalania pakietów spraw ani globalnej osi czasu Telegramu.

## Rejestrowanie i przypisywanie autorstwa

W sekcji „Źródła” dostępne są przełączniki dla poszczególnych kont, dotyczące nowych wiadomości, edycji, usunięć, reakcji oraz członkostwa. Ustawienia wstępne pozwalają zachować albo wszystkie kategorie, albo wiadomości/edycje/usunięcia. Polityka ta ma zastosowanie do wybranych grup w obszarze roboczym, pozostaje aktywna po ponownym uruchomieniu i jest podpisana z podaniem stanu przed i po wprowadzeniu zmian. Ustawienia domyślne zachowują wszystkie kategorie. Wyłączenie kategorii nie powoduje usunięcia starych zapisów; ponowne jej włączenie nie odtwarza pominiętych zdarzeń. Zapisy operacyjne, inne zdarzenia związane z obsługą grup oraz wyraźne migawki historii są oddzielne. Przechwycone obiekty Telegramu mogą zachowywać osadzone metadane niezależnie od ustawień dotyczących oddzielnych aktualizacji. Nie ma jeszcze możliwości nadpisywania kategorii na poziomie grupy.

| Materiały | Zarejestrowano właśnie | Zakres |
| --- | --- | --- |
| Wiadomość | Tekst, identyfikatory rozmówców/wiadomości, metadane nadawcy, odpowiedzi oraz oryginalna kopertka aktualizacji | Brak publicznie weryfikowalnego podpisu Telegramu dla tej wiadomości |
| Edytuj | Nowa zaobserwowana wersja oraz wszelkie wcześniej zapisane wersje | Edycje dokonane w trakcie przestoju mogą zostać utracone; nadawca niekoniecznie jest osobą dokonującą edycji |
| Usunięcie | Powiadomienia oraz ewentualne wcześniej zarejestrowane treści | Zazwyczaj nie podaje się osoby usuwającej ani dokładnego czasu działania |
| Usunięcie bez określenia zakresu | Oryginalne powiadomienie na poziomie konta bez zgadywania, kto jest rozmówcą | Ścisła korelacja z wcześniej zapisanymi identyfikatorami w zakresie konta stanowi zadanie do realizacji w przyszłości |
| Reakcja | Dostarczone liczniki i widoczne najnowsze tożsamości | Uzyskanie pełnej listy dostępnych serwerów wymaga złożenia oddzielnych zapytań; kanały mogą ukrywać tożsamość użytkowników |
| Członkostwo | Komunikaty serwisowe oraz aktualizacje przekazywane uczestnikom | Widoczność zależy od roli użytkownika i rodzaju czatu; brakujące zdarzenia nie oznaczają ich braku |
| Działania administratora | Wyłącznie istotne informacje o aktualizacjach | Nie zaimplementowano oddzielnego odczytu dziennika administracyjnego |
| Załącznik | Opis wersji oryginalnej, liczba pobranych bajtów/SHA-256 oraz wyniki prób | Utracony plik może okazać się niemożliwy do odzyskania; najnowsza wersja nie zastępuje poprzedniej. |
| Historia | Wyraźny zrzut ekranu przedstawiający aktualnie widoczne wiadomości | Nie odtwarza wszystkich zmian ani usuniętych treści |
| Proces gromadzenia danych | Uruchamianie/zatrzymywanie, sygnał kontrolny, błędy, ustawienia, zakres działania oraz potwierdzenie odbioru programu | Oświadczenie własne, a nie niezależne poświadczenie procesu |

Dane działanie przypisuje się danej osobie wyłącznie wtedy, gdy źródło faktycznie wskazuje tę osobę jako sprawcę. W przeciwnym razie interfejs zgłasza brak przypisania. Nazwy użytkowników i imiona to atrybuty obserwowane, a nie dowód tożsamości w świecie rzeczywistym.

## Pojemność i ograniczenia serwisu Telegram

Nie ma uniwersalnej liczby czatów, które można monitorować z gwarancją jakości. Wydajność zależy od szczytowej liczby zdarzeń na sekundę, liczby i rozmiarów załączników, dodatkowych wywołań RPC, liczby aktywnych kont, opóźnień dyskowych/wolnego miejsca na dysku, warunków sieciowych, limitów serwisu Telegram, dopuszczalnego opóźnienia oraz głębokości kolejki.

Telegram rozróżnia dostarczanie pasywne od aktywnego krótkiego odpytywania. Dokumentacja dotycząca aktualizacji opisuje dodatkowe wywołania `updates.getChannelDifference` dla otwartych kanałów/supergrup i zaleca maksymalnie **dziesięć źródeł poddawanych jednocześnie krótkiemu odpytywaniu**. Nie jest to ograniczenie do dziesięciu wybranych grup ani gwarancja kompletności.

| Tryb | Cel | Status |
| --- | --- | --- |
| Standardowa uwaga | Rejestruj dostarczone aktualizacje z wybranych źródeł | Zrealizowano |
| Obserwacja priorytetowa | Dodatkowe kontrole różnic dla ograniczonego zbioru źródeł | Nie zostało zaimplementowane w trybie użytkownika |

Dowolne odpytywanie z dużą częstotliwością, ignorowanie opcji FloodWait lub zakładanie liniowej pojemności z dodatkowych kont nie stanowi prawidłowego modelu wymiarowania. Domyślne limity to pierwsze 1 000 wymienionych rozmów, do 500 wiadomości na migawkę historii, 1–2 000 MiB na zebrany plik w zależności od typu oraz 4 GiB nieskompresowanej, podpisanej zawartości pliku ZIP; każda z tych wartości można zmienić dla poszczególnych obszarów roboczych w sekcji **„Parametry**”. Eksporty nie mają ustalonego limitu liczby zdarzeń. Tryb awaryjny przeglądarki jest domyślnie ograniczony do 128 MiB; interfejs CLI do przesyłania strumieniowego posiada konfigurowalny limit transferu, domyślnie wynoszący 5 GiB.

`tools/check_capacity.py` mierzy lokalne pozyskiwanie i eksport danych syntetycznych. Wyniki tego narzędzia nie stanowią pomiarów dostarczalności wiadomości w Telegramie ani nie gwarantują rzeczywistej liczby czatów. Proszę zapoznać się z plikiem [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/), aby uzyskać informacje na temat mierzonej wersji i obciążenia.

## Niezawodność i odzyskiwanie danych

Zaimplementowane funkcje obejmują transakcje SQLite WAL/synchroniczne; atomowe zapisy wiadomości i zadań związanych z multimediami; zadania trwałe i opóźnienia ponownych prób; deskryptory wersji oryginalnej; ograniczone ponowne próby; trwałe oczekiwanie na pliki multimedialne (FloodWait); pobieranie plików multimedialnych poza okresem oczekiwania sieciowego zdarzenia tekstowego; eksporty ze stabilnym prefiksem przy kontynuacji późniejszych zapisów; atomowe ustawienia i zapisy audytowe; zachowanie aktualnych uprawnień po nieudanej próbie ponownego logowania; izolację uszkodzonego dodatkowego obszaru roboczego; jawne próby ponownego połączenia; wyraźne raportowanie utraty uprawnień; oraz wykrywanie zmian czasu zegarowego przy użyciu zegara monotonicznego.

Pozycje (pts/qts/seq) kont i kanałów są zapisywane i przywracane po ponownym uruchomieniu, a obserwowane czaty są okresowo ponownie sprawdzane; patrz [format dowodów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#durable-collection-and-process-receipts-02). Okresowe zapisywanie pozycji nie stanowi atomowego, bezstratnego potwierdzenia akceptacji dziennika.

Każde uruchomienie procesu rejestruje poprzednią pozycję wskaźnika oraz granicę trybu offline. Bieżąca historia nie jest traktowana jako uzupełnienie luk. Pojemność bufora różnicowego w Telegramie jest ograniczona; `differenceTooLong` nie jest w stanie odtworzyć wszystkich znikniętych treści. Luki niemożliwe do odtworzenia muszą pozostać wyraźnie zaznaczone, nawet jeśli późniejsza migawka historii zakończy się powodzeniem.

## Model dowodowy

Każde zdarzenie zawiera sekwencję, lokalny czas obserwacji w strefie UTC, czas źródłowy (o ile został podany), rodzaj, źródło, podmiot (o ile został podany), oryginalną treść, poprzedni skrót oraz podpis. Obserwacje wiadomości zachowują również informacje o koncie kolektora oraz kontekście uruchomienia.

Podpisane potwierdzenie procesu zawiera losowy identyfikator przebiegu; wersje bibliotek zależnych TgWitness/Python/OS; wartości SHA-256 plików źródłowych oraz zagregowany odcisk cyfrowy; początkowe dane konta, zakres i ustawienia; odczyty czasu UTC oraz wartości monotoniczne; a także poprzedni nagłówek dziennika. Zmiany ustawień, uruchomienia/zatrzymania oraz błędy są zapisywane w tym samym dzienniku. Punkty kontrolne są zachowywane podczas uruchamiania, co pięć minut w trakcie obserwacji (czas ten można zmienić) oraz przy prawidłowym zakończeniu działania. Zachowany lokalny punkt kontrolny umożliwia wykrycie cofnięcia do wcześniejszego prefiksu dziennika.

| Mechanizm | Co określa |
| --- | --- |
| Suma kontrolna pliku SHA-256 | Liczba bajtów jest zgodna ze znanym skrótem |
| Łańcuch skrótów zdarzeń | Porządkowanie i powiązanie zapisów względem znanej granicy |
| Ed25519 | Podpis wygenerowany przy użyciu określonego klucza |
| Niezależnie utrzymywany punkt kontrolny | Późniejsze treści są zgodne z zachowaną granicą |
| Analiza plików programu | Raport własny modułu zbierającego dotyczący zmierzonych plików |
| Ważna, niezależna odpowiedź TSA | Istnienie określonych bajtów w momencie TSA przy wyraźnych założeniach dotyczących zaufania |

Zaimplementowano przygotowywanie żądań zgodnie z RFC 3161 oraz weryfikację odpowiedzi za pomocą OpenSSL. Nie zaimplementowano automatycznego przesyłania. Żądanie lub lokalny podpis zawierający czas systemowy urządzenia nie stanowi niezależnego znacznika czasu. Proszę zapoznać się z [plikiem TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/).

Operator kontrolujący moduł gromadzący dane oraz klucz podpisujący może sfabrykować nowe, podpisane wpisy. Podpisy nie potwierdzają pochodzenia z serwisu Telegram, prawdziwości ani automatycznej dopuszczalności dowodowej. Bardziej rygorystyczne przechowywanie danych wymaga niezależnego punktu kontrolnego/przechowywania w czasie, kontroli dostępu do kluczy, rejestrów transferów oraz weryfikacji za pomocą zaufanego oprogramowania.

## Eksport, wdrożenie i przekazanie

Podpisany plik ZIP zawiera oryginalne pliki JSONL, CSV, HTML, zachowane załączniki, skróty, podpisany manifest oraz narzędzie ułatwiające weryfikację. Obejmuje on jeden obszar roboczy oraz stały, pełny prefiks dziennika. Filtry wyszukiwania w panelu nie usuwają rekordów w sposób niewidoczny. Klucze tajne, tokeny oraz sesje Telegrama są wykluczone; oryginalne obserwacje mogą nadal zawierać dane osobowe oraz metadane Telegrama.

Należy oddzielnie zachować skrót pliku ZIP, zaufany odcisk cyfrowy, punkt kontrolny, potwierdzenie przetworzenia oraz zapis przekazania. Należy korzystać z narzędzia weryfikującego pochodzącego z zaufanej instalacji, zamiast polegać wyłącznie na kodzie wykonywalnym tylko dlatego, że znajduje się on w badanym pliku ZIP.

Interfejs przeglądarkowy działa lokalnie bez konieczności korzystania z Node.js, sieci CDN ani zewnętrznych czcionek. Instalacją zarządza jeden token operatora. Dostęp zdalny wymaga protokołu HTTPS lub tunelu SSH. Dostarczane są natywne definicje w języku Python oraz definicje kontenerów, a przykłady usług znajdują się w [katalogu deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); wyniki przeprowadzonych testów platformy są wymienione oddzielnie.

Domyślny obszar roboczy wykorzystuje katalog główny danych; dodatkowe obszary robocze wykorzystują katalog `profiles/<id>/`. Tworzenie kopii zapasowej wymaga zatrzymania procesu oraz kompletnego zestawu danych i kluczy. Pliki ZIP z dowodami nie są kopiami zapasowymi aplikacji. W przypadku danych poufnych można użyć zewnętrznego klucza głównego dla nowego katalogu danych; szyfrowanie dziennika i multimediów zapewnia dysk lub wolumin operatora. Zob. [pliki CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) oraz [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/operations/).

## Kryteria wydania stabilnej wersji

Przed wydaniem stabilnej wersji należy zaznaczyć:

1. Prawdziwe grupy prywatne, supergrupy, fora i kanały wraz z rolami członków/administratorów oraz ukrytą/widoczną historią, w tym danymi logowania/uwierzytelnianiem dwuskładnikowym (2FA), unieważnieniem uprawnień i utratą dostępu.
2. Kontrolowane zmiany, usunięcia, reakcje, członkostwo oraz materiały multimedialne w kontekście znanych działań.
3. Awarie procesu/serwera, awarie dysków/przepełnienie dysku, wygasłe odwołania do plików, błąd FloodWait, utrata połączenia sieciowego, uszkodzone pliki oraz przywrócenie bazy danych do poprzedniego stanu.
4. Długotrwałe korzystanie z wielu kont z uwzględnieniem opóźnień, kolejek, pamięci i miejsca na dysku, w tym zarówno cichych, jak i hałaśliwych źródeł jednocześnie.
5. Przerwa między zmianą stanu protokołu MTProto a zatwierdzeniem wpisu w dzienniku.
6. Prawidłowa instalacja w docelowej matrycy systemów operacyjnych/kontenerów oraz zweryfikowane przywracanie kopii zapasowej.
7. Niezależna ocena kwestii bezpieczeństwa, podpisów oraz twierdzeń dotyczących przypisania autorstwa i dowodów.

Odczytywanie logów administracyjnych, dodatkowe listy reaktorów, odczytywanie priorytetowe, oddzielne procesy robocze oraz szyfrowanie na poziomie całej aplikacji pozostają zadaniami do realizacji w przyszłości. Dostęp do paneli o ograniczonym zakresie opisano w sekcji [„Dostęp i uprawnienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/)”. Wersja 0.6 obsługuje ograniczoną do jednego konta funkcję TData oraz import plików kont opisany w [pliku ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/). Przed publikacją prosimy o zapoznanie się z warunkami korzystania z API serwisu Telegram. Źródła badań oraz ustalenia dotyczące platformy znajdują się w [pliku RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
