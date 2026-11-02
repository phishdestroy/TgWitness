# Funkcje i ograniczenia

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/features/

Obecny model gromadzenia danych, procesy obsługi wielu kont, eksporty oraz ograniczenia operacyjne programu TgWitness.

TgWitness archiwizuje rozmowy w Telegramie dostępne dla połączonych kont, rejestruje zaobserwowane zmiany i przygotowuje weryfikowalne eksporty. Niniejszy dokument opisuje model gromadzenia danych, aktualne procesy oraz ich ograniczenia.

## Aplikacja samodzielna

TgWitness posiada własną instalację, katalog danych oraz cykl życia wersji. Dołączony interfejs internetowy obsługuje konfigurację i przeglądanie; wyeksportowane zapisy mogą być wykorzystywane niezależnie.

Użytkownik łączy swoje konta, wybiera źródła widoczne dla każdego z nich i uzyskuje zapisany dziennik obserwacji. Panel przedstawia treść, zapisane zmiany, pochodzenie obserwacji oraz znane luki. Inny śledczy może zweryfikować wyeksportowany materiał.

Panel rozróżnia autoryzację konta, dostęp do źródła, aktywność modułu zbierającego oraz zakres rejestracji. Należy przeanalizować te stany łącznie podczas oceny okresu, w którym odnotowano niewielką liczbę wiadomości lub wystąpił problem z połączeniem.

## Wspólne dochodzenia

Administrator może wydawać [tokeny dostępu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/) ograniczone do obszarów roboczych i poszczególnych czatów, z uprawnieniami dla poszczególnych działań, ograniczeniami adresów IP, terminem ważności, limitami logowań oraz kontrolą sesji. Osoba sprawdzająca z uprawnieniami tylko do odczytu może przeglądać sprawę bez otrzymywania autoryzacji Telegramu ani klucza do panelu głównego. Dostęp ograniczony do czatu pozostaje oddzielony od ustawień dotyczących całego konta oraz eksportów pełnego dziennika.

Automatyczny MTProxy utrzymuje działające trasy Telegramu z czterech źródeł publicznych lub katalogu operatora. [Tryby IP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes) określają, czy w przypadku awarii należy czekać na inny serwer proxy, czy też można skorzystać z wyraźnie dozwolonej trasy bezpośredniej. Zewnętrzne żądania HTTP mają oddzielną trasę oraz opcję wyłączenia.

## Narzędzia archiwizacyjne

[Funkcje pozyskiwania historii](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/), [wyszukiwania i analizy archiwów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/),[MCP tylko do odczytu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/), [lokalne OCR/transkrypcja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/) oraz[wychodzące webhooki](https://phishdestroy.github.io/TgWitness/pl/docs/reference/webhooks/) są dostępne na stronie 0.7.1. Raporty analityczne i rozpoznany tekst pozostają oddzielone od zarejestrowanych zdarzeń.

[Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-board/) dodaje zakładki powiązane ze źródłami, cytaty, notatki i kolekcje w obrębie obszaru roboczego. [Kreator](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/) [raportów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/) wybiera materiał, sekcje oraz jeden z ośmiu szablonów do eksportu w obsługiwanych formatach HTML/PDF.

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

Aplikacja nie określa stałej liczby obszarów roboczych. Każdy obszar roboczy uruchamia własne zadania kolektora służące do monitorowania połączeń, pobierania multimediów, ponownych kontroli oraz przyjmowania nowych czatów w ramach wspólnego procesu w języku Python i pętli zdarzeń. Przepustowość zależy od obciążenia. W celu izolacji procesów należy stosować oddzielne instalacje, porty i katalogi danych.

Każdemu kontu należy przypisać źródła, do których ma ono dostęp. Różne konta mogą obserwować tę samą grupę, ale ich obserwacje pozostają oddzielne i zachowują swoje pochodzenie. Dwa konta na jednym komputerze kontrolowanym przez operatora nie stanowią dwóch niezależnych świadków. **Eksport grupy** łączy osobno podpisane pliki ZIP obszarów roboczych z podpisaną listą plików zawierającą ich identyfikatory obszarów roboczych, skróty i odciski palców kluczy podpisujących. Każdy dziennik zachowuje własne granice. Twórz połączoną oś czasu obejmującą różne obszary robocze w notatkach dotyczących sprawy lub narzędziach analitycznych, zachowując te odniesienia do źródeł.

## Rejestrowanie i przypisywanie autorstwa

W sekcji „Źródła” dostępne są przełączniki dla poszczególnych kont, dotyczące nowych wiadomości, edycji, usunięć, reakcji oraz członkostwa. Ustawienia wstępne pozwalają zachować albo wszystkie kategorie, albo wiadomości/edycje/usunięcia. Polityka ta ma zastosowanie do wybranych grup w obszarze roboczym, pozostaje aktywna po ponownym uruchomieniu i jest podpisana z podaniem stanu przed i po wprowadzeniu zmian. Ustawienia domyślne zachowują wszystkie kategorie. Wyłączenie kategorii nie powoduje usunięcia starych zapisów; ponowne jej włączenie nie odtwarza pominiętych zdarzeń. Zapisy operacyjne, inne zdarzenia związane z obsługą grup oraz wyraźne migawki historii są oddzielne. Przechwycone obiekty Telegramu mogą zachowywać osadzone metadane niezależnie od ustawień dotyczących oddzielnych aktualizacji. Nie ma jeszcze możliwości nadpisywania kategorii na poziomie grupy.

| Materiały | Zarejestrowano właśnie | Zakres |
| --- | --- | --- |
| Wiadomość | Tekst, identyfikatory rozmówców/wiadomości, metadane nadawcy, odpowiedzi oraz oryginalna kopertka aktualizacji | Zachowane jako obserwacja widoczna na koncie, podpisana przez osobę gromadzącą dane |
| Edytuj | Nowa zaobserwowana wersja oraz wszelkie wcześniej zapisane wersje | Edycje dokonane w trakcie przestoju mogą zostać utracone; nadawca niekoniecznie jest osobą dokonującą edycji |
| Usunięcie | Powiadomienia oraz ewentualne wcześniej zarejestrowane treści | Zazwyczaj nie podaje się osoby usuwającej ani dokładnego czasu działania |
| Powiadomienie o usunięciu na poziomie konta | Oryginalne powiadomienie; rozwiązane zapisy obejmują zapisany czat oraz metodę korelacji | Wymagane jest dokładnie jedno wcześniej zapisane dopasowanie czatu prywatnego lub zwykłej grupy w zakresie; pozostałe identyfikatory pozostają w stanie „`deletion.unscoped`”. Identyfikatory kanałów i supergrup są wyłączone z tej korelacji. |
| Reakcja | Dostarczone liczniki i widoczne najnowsze tożsamości | Uzyskanie pełnej listy dostępnych serwerów wymaga złożenia oddzielnych zapytań; kanały mogą ukrywać tożsamość użytkowników |
| Członkostwo | Komunikaty serwisowe oraz aktualizacje przekazywane uczestnikom | Widoczność zależy od roli użytkownika i rodzaju czatu; brakujące zdarzenia nie oznaczają ich braku |
| Działania administratora | Odpowiednie dostarczone aktualizacje oraz migawka dziennika administratora w eksportach czatów z kanałów/supergrup | Funkcja eksportu odczytuje dziennik, o ile jest on dostępny dla konta administratora odpowiedzialnego za eksport; ciągłe sprawdzanie dziennika administratora wykracza poza ten proces. |
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
| Priorytetowe weryfikacje | Źródła oznaczone gwiazdką wykorzystują własne, konfigurowalne interwały i mają pierwszeństwo w każdym ograniczonym cyklu ponownej weryfikacji | Zaimplementowano funkcje wyszukiwania historii i wiadomości |

Gwiazdka priorytetu kontroluje te ponowne sprawdzania. Dodatkowe krótkie odpytywanie funkcji ``updates.getChannelDifference` ` nie jest udostępniane jako oddzielny tryb użytkownika.

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

Zaimplementowano przygotowywanie żądań zgodnie z RFC 3161 oraz weryfikację odpowiedzi za pomocą OpenSSL. Tryb dowodowy przesyła również skróty punktów kontrolnych do skonfigurowanych usług znaczników czasu. Należy zachować i zweryfikować odpowiedź organu w celu ustalenia niezależnego punktu odniesienia czasowego. Zobacz [plik TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/).

Należy niezależnie zachowywać punkty kontrolne, kontrolować dostęp do kluczy podpisujących, przechowywać zapisy transferów oraz weryfikować eksporty za pomocą zaufanego oprogramowania. [Zakres](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope) [weryfikacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope) wyjaśnia, w jaki sposób te kontrole wzajemnie się uzupełniają oraz jakie założenia dotyczące zaufania mają zastosowanie.

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

Dostęp do paneli o ograniczonym zakresie opisano w sekcji [„Dostęp i uprawnienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/)”. Wersja 0.6 obsługuje ograniczoną funkcję TData dla pojedynczego konta oraz import plików kont opisany w [pliku](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/) [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/). Przed publikacją należy zapoznać się z warunkami korzystania z API serwisu Telegram. Informacje dotyczące badań i ustaleń dotyczących platformy znajdują się w [pliku](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md) [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
