# Telegram · Przewodnik po panelach

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/

Każdy ekran panelu: czaty, dziennik, źródła, eksporty, opcje dodatkowe, tryby ochrony oraz sprawdzanie kodu.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Pierwsze kroki](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/)

![Pierwsze kroki](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Pierwsza konfiguracja i ustawienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/settings/) · [Konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/) · [Eksportowanie i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/) · [Raporty dotyczące spraw](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/)

Jak działa każdy ekran, co zapisuje w podpisanym dzienniku i gdzie znajduje się szczegółowy przewodnik. Panel wyświetla po jednym obszarze roboczym na raz: jedno konto Telegramu z własnymi źródłami, dziennikiem i kluczem podpisującym. Selektor u góry paska bocznego służy do przełączania obszarów roboczych. Adres zawiera nazwę obszaru roboczego (`?ws=…`); dopóki adres, selektor i załadowane konto nie są zgodne, działania pozostają zablokowane.

Użyj metod porównawczych [Compare](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md), aby wybrać między obserwacją na żywo, pełną historią, eksportami nowych kont/czatów oraz przekazaniem zapisanych rekordów. Strona Eksporty zawiera to samo porównanie powyżej elementów sterujących pobieraniem.

**Na tej stronie**

- [Zorientuj się w temacie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#find-your-way)
- [Zacznij tutaj](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#start-here)
- [Czat](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#chats)
- [Dziennik](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#journal)
- [Źródła](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#sources)
- [Eksporty](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#exports)
- [Ustawienia, konta i połączenie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#settings-accounts-and-connection)
- [Dodatki](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#extras)
- [Tryby ochrony](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#protection-modes)
- [Więcej narzędzi](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#more-tools)

## Zorientuj się w serwisie

Sekcje codzienne znajdują się u góry paska bocznego, **sekcja „Konta”** znajduje się pod **„Obszarem roboczym** ”, a wszystko inne znajduje się w sekcji **„Więcej narzędzi i ustawień** ”. Przełącznik **poziomu interfejsu** na górnym pasku określa, ile sekcji jest wyświetlanych:

| Poziom | Sekcje na pasku bocznym |
| --- | --- |
| Proste | Strona główna, Czaty, Zmiany, Archiwa i Ustawienia |
| Standard | Zobacz też Case Board, Konta i dostęp |
| Ekspert | Ponadto: Źródła, Dodatki, Zapytaj archiwum, Parametry, Konto, Dziennik systemowy i Integracje |

Proste wywołania: „Start here”, „Journal” oraz „Exports **Home**”, **„Changes”** i **„Archives**”. Poziom służy wyłącznie do ukrywania sekcji. Ukryta funkcja nadal działa, a serwer samodzielnie sprawdza każde uprawnienie. Poziom, język, motyw i strefa czasowa są zapisywane osobno dla każdego operatora i obszaru roboczego; zobacz [ustawienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/settings/).

W górnym pasku znajdują się również:

- **Przejdź do sekcji** (Ctrl+K lub ⌘K na komputerze Mac): znajdź czat, parametr lub wpis w dzienniku według `#number`. Klawisze strzałek służą do poruszania się, Enter otwiera, Esc zamyka.
- **Powiadomienia**: problemy i zmiany w czacie wygenerowane na podstawie dziennika. Opcja **„Oznacz wszystko jako przeczytane”** zeruje licznik, a **„Reguły powiadomień”** otwiera okno z regułami. Wysyłanie powiadomień do Telegrama, Discorda lub na e-mail konfiguruje się w sekcji [„Dodatki” → „Powiadomienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#notifications)”.
- Wskaźnik połączenia dla tego obszaru roboczego. **Stan kolektora** pod górnym paskiem dzieli go na połączenie z Telegramem, pobieranie zdarzeń, źródła oraz kolejkę załączników.
- **Lock**: zamyka panel w tej przeglądarce. Kolekcja nadal działa na serwerze.
- Tryb ochrony obok numeru wersji; zobacz [tryby ochrony](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#protection-modes).

Przestrzeń robocza demonstracyjna zawiera fikcyjne wiadomości i nigdy nie łączy się z Telegramem. Czynności, które mogłyby zmienić rzeczywistą przestrzeń roboczą, są tam blokowane.

## Zacznij tutaj

Wybierz zadanie. Op**cja „Eksportuj moje konto”** pobiera dane, do których konto ma obecnie dostęp. **Opcja „Śledź dochodzenie”** rejestruje nowe wiadomości, zaobserwowane zmiany i powiadomienia o usunięciu z wybranych przez Ciebie czatów. Karta konfiguracji przedstawia trzy kroki: podłącz konto, wybierz źródła, rozpocznij obserwację. Pytanie dotyczące celu pozostaje na tej stronie, dopóki nie udzielisz na nie odpowiedzi lub nie pominiesz go. Zamiast tego otwiera się nowy obszar roboczy z [pierwszą konfiguracją](https://phishdestroy.github.io/TgWitness/pl/docs/reference/settings/).

## Czat

Zapisane rozmowy, domyślnie tylko do odczytu.

- Przeszukuj listę według nazwy lub identyfikatora. **Opcja „Wybierz”** pozwala dodawać lub usuwać obserwowane czaty. Opcja „Otwórz **link Telegrama”** przyjmuje nazwę użytkownika lub link zaproszenia i zapisuje podgląd w dzienniku. Polecenie **„Dołącz / otwórz i obserwuj”** powoduje dołączenie do czatu i dodanie go do twoich źródeł; otwarcie bota powoduje jego wysłanie `/start`.
- Nagłówek czatu zlicza wiadomości **usunięte, tekst zachowany**, **usunięty przed zapisaniem** oraz **nieznalezione podczas ponownej weryfikacji**. Lista czatów i powiadomienia wykorzystują te same definicje. Usunięta wiadomość jest zaznaczona na czerwono i zachowuje swój zapisany tekst; edytowana wiadomość zachowuje każdą zapisaną wersję. Każde usunięcie zawiera znane informacje: kiedy wiadomość została wyświetlona, że Telegram nie informuje, kto ją usunął, lub że dotarło jedynie powiadomienie.
- **Opcja „Załaduj historię”** wyświetla ostatnie 100, 250 lub 500 wiadomości w tym widoku oraz w dzienniku. Aby załadować wszystkie włączone źródła, wybierz opcję [Źródła → Pełna historia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#sources).
- **Funkcja „Eksportuj czat”** pobiera całą widoczną historię jako podpisany `chat.json` i `chat.html`. Kilka połączonych kont może dzielić się pracą: każde pobiera swój własny zakres numerów wiadomości i podpisuje swoją część, a konto, które rozpoczyna eksport, podpisuje archiwum. Zobacz: [eksport jednego czatu](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- Lista **osób** zawiera wszystkich użytkowników, którzy mają zapisane wiadomości na tym czacie. Profile osób są domyślnie wyłączone, ponieważ zawierają dane osobowe osób trzecich. Gdy są włączone dla danego czatu, profil pokazuje imię i nazwisko oraz historię nazw użytkownika, flagi Telegrama, skróty awatarów, aktywność, kto komu odpowiada, inne obserwowane czaty oraz wspomniane portfele, numery telefonów, nazwy użytkowników i linki. Każdy fakt odsyła do swojego zapisu. **Eksport profili** powoduje zapisanie podpisanego pliku, opcjonalnie w formacie ZIP z hasłem; wyłączenie profili powoduje usunięcie pliku profilu. Zobacz [profile użytkowników](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#people-profiles).
- **Zapisz profil teraz** rejestruje migawkę czatu lub profilu bota: opis, członkowie, link zaproszeniowy, polecenia bota.

### Tryb tylko do odczytu, wysyłanie i tajemnice

Dwa przełączniki nad wiadomościami chronią konto i czytelnika:

- **Tryb „tylko do odczytu”** jest włączony po otwarciu czatu. Wyłącz tę opcję, aby wysyłać wiadomości lub naciskać przyciski bota . Każda akcja wyświetla pytanie **„Wysłać jako @konto?”** lub **„Nacisnąć ten przycisk bota jako @konto?**”, informując, że członkowie czatu to zobaczą i że trafi to do podpisanego dziennika. **Opcja „Nie pytaj ponownie przez 10 minut w tym czacie”** pomija to pytanie na chwilę. Wysyłanie jest wyłączone dla celu „**Dowody w sprawie**”, zarówno w panelu, jak i w API.
- **Funkcja „Mask secrets”** ukrywa dane wyglądające jak hasło, kod logowania, klucz API lub skrót, token bota, ciąg sesji, klucz prywatny, token JWT lub numer karty płatniczej (numery kart są sprawdzane za pomocą sumy Luhna). **Opcja „Show”** ujawnia jedną wartość; ujawnienie to jest rejestrowane w dzienniku. Wyłączenie maskowania dla tej przeglądarki również jest rejestrowane. Zmienia się jedynie wyświetlanie: oryginalne zapisy i wszystkie eksporty zachowują pełny tekst.

## Rejestr

Wszystkie zapisy podpisane przez obszar roboczy, najnowsze na początku.

- **W sekcji „Przegląd”** podane są liczby zaobserwowanych wiadomości, zarejestrowanych zmian, powiadomień o usunięciu oraz wybranych źródeł.
- **Oś czasu zdarzeń** filtruje według typu zdarzenia (wszystkie, edycje, usunięcia, reakcje, członkostwo, zasięg), według tekstu i według źródła. **Załaduj wcześniejsze wydarzenia** pozwala przejść do poprzedniej strony.
- Otwórz zapis, aby wyświetlić jego szczegóły, skrót i zawartość. **Link do tego zapisu** to adres, który otwiera ten sam zapis. Ewentualne dane poufne są zamaskowane w tym podglądzie; w eksportowanych plikach zachowana jest oryginalna treść.
- Dziennik jest tylko do dodawania: żadna opcja w panelu nie edytuje ani nie usuwa wpisu. Sprawdź to w sekcji **Eksportuj → Zweryfikuj dziennik** lub `python -m tgwitness.verify`; zobacz [eksportowanie i weryfikację](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/).

## Źródła

Które rozmowy rejestruje ten obszar roboczy i jakie informacje z nich zachowuje. Zmiany dotyczą przyszłej aktywności; zapisane dane pozostają bez zmian.

**Funkcja „Odśwież listę czatów”** odczytuje czaty i foldery konta. Nie pobiera ona wiadomości.

### Zakres

- **Co rejestruje to konto** : **Wybrane rozmowy** (tylko czaty, które dodasz), **Folder Telegram** (jeden z folderów konta, zawierający czaty dodane do niego później) lub **Całe konto** (każdy czat oraz każdy nowy czat, grupę, czat prywatny lub bota w momencie ich pojawienia się). **Tryb dochodzeniowy** służy do obsługi dedykowanego konta: rejestruje wszystko, co widzi to konto, jego własne wiadomości i naciśnięcia przycisków, a także natychmiast zapisuje profil każdego nowego czatu oraz wcześniej widoczne wiadomości. [przewodnik po kontach](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) wyjaśnia, dlaczego nigdy nie należy używać swojego głównego konta.
- **Typy źródeł** ograniczają tryby folderów i całego konta do kanałów, grup, prywatnych czatów i botów. **Opcja „Własne działania”** dodaje wiadomości, edycje i naciśnięcia klawiszy odpowiedzi na klawiaturze związane z danym kontem.
- **Gdy pojawi się nowy czat lub bot**: zapisz jego profil oraz do wybranej liczby jego najnowszych widocznych wiadomości.

Ograniczenia: opublikowany moduł zbierający dane w chmurze nie odbiera tajnych czatów. Oddzielny interfejs [Pseudo-secret oraz jego wersja demonstracyjna](https://phishdestroy.github.io/TgWitness/pl/docs/reference/secret-chats/) zostały udokumentowane wraz z stanem rozwoju i istniejącymi błędami. Nic nie jest rejestrowane, gdy TgWitness nie działa; po ponownym uruchomieniu nadrabia on jedynie to, co Telegram nadal zwraca, a raport pokazuje tę lukę. Czatowanie wykraczające poza limit listy czatów (dialogi 1,000, o ile nie zmieniono tego w parametrach) jest dodawane, gdy tylko staną się aktywne. Przyciski bota wbudowane w inną aplikację są niewidoczne; rejestrowana jest odpowiedź bota.

### Czat w zakresie

Filtruj według statusu (**Włączone**, **Wstrzymane**, **Priorytetowe**, **Wykluczone**, **Niepotwierdzony dostęp**, **Zignorowane**) i typu, a następnie wykonaj działanie na zaznaczonych elementach: włącz, wstrzymaj, oznacz lub usuń priorytet, wyklucz z zakresu lub usuń. Ikona statusu pokazuje jedynie stan; działania znajdują się w menu każdego wiersza wraz z opisem ich funkcji. Wstrzymanie i wykluczenie wymagają potwierdzenia, również w trybie zbiorczym. Usunięcie źródła wymaga podania jego nazwy i powoduje usunięcie profili osób z nim związanych; zapisane rekordy pozostają w dzienniku.

Źródłem, którego nie widać na liście czatów konta, jest **odbieranie aktualizacji, które nie znajdują się na liście czatów**, podczas gdy zapisy wciąż napływają; w przeciwnym razie jest to **dostęp niepotwierdzony**. **Dostępne czaty** dodaje czaty z **Dodaj wybrane** lub **Dodaj wszystkie wyniki**.

### Pełna historia

Wczytuje dostępną historię każdego włączonego źródła do sekcji „Czat” i dziennika. Postępy są zachowywane po ponownym uruchomieniu; załączniki są dostosowywane zgodnie z ustawieniami multimediów. Zobacz [historię źródła](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/).

### Rejestrowanie

- **Wybierz, które zmiany chcesz zachować**: nowe wiadomości, edycje, powiadomienia o usunięciu, widoczne reakcje, dołączenia i opuszczenia. Ustawienie wstępne zmienia formularz; **opcja „Zapisz ustawienia rejestracji”** powoduje jego zastosowanie. Ponowne włączenie kategorii nie powoduje odzyskania przepuszczonych zdarzeń.
- **Zachowaj multimedia, jeśli są dostępne**: pobieraj załączniki o rozmiarze nieprzekraczającym określonej wartości na plik, ustaw dla każdego typu od 1 do 2 000 MiB oraz ogranicz długość wideo w sekundach (0 oznacza brak ograniczenia). Każda próba pobrania jest rejestrowana wraz z wynikiem.
- **Ponowna kontrola**: czaty priorytetowe co kilka minut, pozostałe rzadziej, dzięki czemu konto nie przekracza limitów FloodWait serwisu Telegram. Wartość 0 wyłącza grupę. Czaty priorytetowe należy oznaczyć gwiazdką na liście; liczba czatów na przebieg oraz przerwa między czatami są określone w sekcji „Parametry”. Zobacz [kolekcję](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/).

## Eksport

**Sekcja „Pobieranie”** służy do przygotowywania plików; sekcja **„Raport kompilacji”** pozwala wybrać wygląd raportów.

| Co | Wykorzystaj go do | Przewodnik |
| --- | --- | --- |
| Eksport konta | Aktualny zrzut ekranu przedstawiający treści, do których konto ma obecnie dostęp | [Eksport konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/account-export/) |
| Udostępnianie kopii | Zminimalizowana wersja gotowego eksportu konta | [Ujawnienie informacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Podpisano ZIP | Dziennik, raport, załączniki i narzędzia weryfikacyjne w ramach ustalonej granicy dziennika | [Eksportuj i zweryfikuj](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/) |
| Raport w formacie HTML, PDF, JSON | Zapieczętowany, czytelny raport | [Raporty dotyczące spraw](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/) |
| JSONL, CSV | Oryginalne zapisy z podpisami; arkusz kalkulacyjny zgodny z formułami | [Eksportuj i zweryfikuj](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/) |
| Fragment protokołu przekazania | Tylko te czaty, okresy i osoby, których potrzebuje odbiorca | [Dowody](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#investigation-handoff) |
| Eksport czatu | Jeden czat z podpisem `chat.json` oraz `chat.html` | [Eksportuj jedną rozmowę](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Zaszyfrowanie powyższych plików do pobrania hasłem** (co najmniej 12 znaków) powoduje zapisanie pliku AES-256 ZIP, który można otworzyć za pomocą programu 7-Zip lub WinRAR. Znajdujący się w środku podpisany plik pozostaje niezmieniony. Hasło nie jest zapisywane.
- **W przygotowanych eksportach** przechowywanych jest maksymalnie 20 plików o łącznej wielkości do 2 GiB oraz najnowszy plik, co umożliwia wielokrotne pobieranie; każdy z nich zawiera element SHA-256. Przygotowanie pliku nie oznacza potwierdzenia jego dostarczenia.
- Gdy przeglądarka odrzuca okno dialogowe zapisu, panel przechodzi na zwykłe pobieranie pliku.
- **Twoja tożsamość podpisująca** pokazuje odcisk klucza. **Opcje „Zapisz punkt kontrolny**” i „Pobierz**podpisane potwierdzenie uruchomienia”** pozwalają uzyskać zapisy, które można przechowywać poza kolektorem. Opcja „Przygotuj **żądanie sygnatury czasowej”** tworzy żądanie zgodne z RFC 3161 bez nawiązywania połączenia z żadną usługą.

## Ustawienia, konta i połączenie

- **Ustawienia**: cel, połączenie, co rejestrować oraz interfejs. Zobacz: [pierwsza konfiguracja i ustawienia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/settings/).
- **Konta**: każda przestrzeń robocza wraz ze swoim stanem, źródłami, zdarzeniami i kolejką załączników. Filtruj według: **„Wymaga uwagi**”, **„Gromadzenie”**, **„Offline” lub „Wstrzymane”** albo **„Brak połączenia”**, wstrzymaj lub wznowij wybrane działania, importuj pliki kont zbiorczo i zarządzaj grupami. Zobacz [konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/).
- **Konto**: logowanie i trasa połączenia dla tego konta. Połączenie bezpośrednie, profil WireGuard, własny serwer proxy, publiczna pula MTProto lub WARP; przygotuj i sprawdź trasę, a następnie zastosuj ją do tego konta, grupy lub wszystkich kont. Zobacz: [połączenia oraz serwery](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) [proxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md).

## Dodatki

Opcjonalnie: do rozpoczęcia gromadzenia danych wystarczy konto i źródła. Tylko wybrana przez Ciebie opcja otwiera swoje ustawienia, a nic nie jest podłączane automatycznie. Karta **„Poziom ochrony**” u góry pokazuje [tryb ochrony](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#protection-modes).

| Karta | Co to wnosi | Przewodnik |
| --- | --- | --- |
| Pamięć masowa i miejsce na dysku | Kopie zapasowe, przenoszenie starszych plików do chmury, kopia dowodowa, której nie można usunąć | [Przechowywanie danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/storage/) |
| Cel i poziom ochrony | Sugerowane ustawienia dla Twojego celu i dwóch skal | [poniżej](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#goal-and-protection-level) |
| Powiadomienia | Problemy, zmienione wiadomości i codzienne podsumowanie; własny bot kontrolny | [poniżej](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#notifications) |
| Dowody i kopie zapasowe | Sygnatury czasowe, dodatkowi świadkowie oraz zaszyfrowana kopia przechowywana poza serwerem | [poniżej](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#evidence-and-backups) |
| Serwer działa 24 godziny na dobę, 7 dni w tygodniu | Serwer w chmurze bez SSH, tworzony i usuwany z poziomu panelu | [Wysoki poziom bezpieczeństwa](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/#from-the-panel) |
| Niezależny świadek | Podpisane sprawdziany publikowane na Twoim kanale w Telegramie lub na Discordzie | [Świadek](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/) |
| Sprawdzanie kodu | Porównuje uruchomiony program z publicznym commitem na GitHubie | [poniżej](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#code-check) |

### Cel i poziom ochrony

Cztery pytania:

1. **Do czego służy? Do prowadzenia** osobistego rejestru, prowadzenia dochodzenia lub gromadzenia dowodów w sprawie.
2. **Jak dużo chcesz monitorować?** Kilka czatów (do około 50), wiele czatów (do około 500) czy całe konta. To ustawia limit listy czatów na 1 000, 3 000 lub 20 000.
3. **Zdjęcia i pliki?** Tylko tekst, zdjęcia i krótkie pliki multimedialne (zdjęcia do 20 MB, filmy do 100 MB) lub wszystko (filmy i dokumenty do 1 GB każdy). Opcja „Wszystko” z pełnymi kontami zapewnia również 4 GiB wolnego miejsca na dysku.
4. **Gdzie będzie działać? Na** tym komputerze lub na serwerze, który jest zawsze włączony.

Lista sugestii zawiera niezależne znaczniki czasu, drand oraz listę urządzeń Telegrama, a przy każdym z nich znajduje się opis tego, co dodaje. Znaczniki czasu są generowane co 60, 30 lub 10 minut dla rejestru osobistego , dochodzenia lub dowodów; drand i lista urządzeń wymagają znaczników czasu. Zmiany **należy stosować** wyłącznie w odniesieniu do tych elementów, zasad dotyczących załączników oraz dwóch powyższych parametrów. Każda zmiana stanowi wpis do dziennika, a ponadto `setup.applied`. Powiadomienia, kopia poza serwisem, serwer, brama DNS, weryfikacja kodu i świadek są proponowane jako kolejne kroki wraz z własnymi formularzami.

Dwie skale są obliczane na podstawie aktualnych ustawień, a nie na podstawie celu:

| Skala | Punkty |
| --- | --- |
| Wiarygodność | Podpisany dziennik 1, znaczniki czasu 3, drand 1, lista urządzeń 1, sprawdzenie zgodności kodu 1, sondaż świadków 1, poświadczony serwer 2, dziennik DNS bramy 1 |
| Niezawodność | Serwer zawsze aktywny 3, kopia poza siedzibą 3, blokada obiektów 1, powiadomienia o problemach 1 |

Maksymalnie 80% lub więcej oznacza **poziom „maksymalny”**, 50% – **„wysoki”**, 25% – **„umiarkowany”**, a poniżej tego poziomu – **„podstawowy**”. Niezawodność jest obecnie obliczana na podstawie serwera działającego w trybie ciągłym, zgodnie z odpowiedzią na pytanie 4, zanim sprawdzone zostaną jakiekolwiek serwery.

### Powiadomienia

Powiadomienia są wysyłane przez Apprise do Telegramu, Discorda, Slacka, ntfy, poczty e-mail, Matrixa oraz ponad 100 innych usług. Wybierz usługę, wypełnij jedno lub dwa pola i wyślij test lub wklej bezpośrednio adresy Apprise.

- **Problemy**: dysk prawie pełny, wylogowanie z konta, błędy związane z kolekcją, kopiowaniem lub sygnaturą czasową . Na serwerze zablokowanym problemem jest również otwarty port SSH lub logowanie.
- **Zmiany**: usunięte, edytowane i brakujące wiadomości w obserwowanych czatach, pogrupowane w jedno powiadomienie na każdą kontrolę (co minutę, o ile nie zmieniono tego w ustawieniach).
- **Zrealizowane zadania**: historia, eksporty i kopie zapasowe.
- **Codzienne podsumowanie** o wybranej godzinie według czasu serwera.

Powiadomienia zawierają nazwy czatów i liczbę wiadomości. Fragmenty wiadomości są domyślnie wyłączone; gdy są włączone, treść wiadomości opuszcza to urządzenie.

**Twój bot operatorski** to własny bot utworzony za pomocą @BotFather, który odpowiada `/status` i `/stats`, a opcjonalnie `/pause`, `/resume` oraz `/copy`. Mogą z niego korzystać wyłącznie wymienione czaty i identyfikatory użytkowników Telegrama; treść rozmowy pozostaje w obszarze roboczym. Użyj oddzielnego bota, jeśli inna aplikacja już odbiera jego polecenia. Zobacz [powiadomienia](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) i [bota operatora](https://phishdestroy.github.io/TgWitness/pl/docs/reference/storage/#operator-bot-and-completion-notices).

### Dowody i kopie zapasowe

- **Niezależne znaczniki czasu** wysyłają wyłącznie element SHA-256 każdego podpisanego punktu kontrolnego do organów RFC 3161 oraz kalendarzy OpenTimestamps co 5 do 1 440 minut. **Anchor obecnie** uruchamia cykl. Zobacz [znaczniki czasu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/).
- **Więcej świadków**, z których każdy jest wyłączony, dopóki nie zostanie wybrany: najnowsza runda drand, lista Telegramu zawierająca zalogowane urządzenia bez adresów IP oraz dziennik zapytań DNS serwera prowadzony przez Cloudflare Gateway. Zobacz [opcjonalne zapisy](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **Szyfrowana kopia zapasowa** kopiuje dziennik, pliki, punkty kontrolne i eksporty czatów do magazynu zgodnego ze standardem S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Wszystko jest najpierw szyfrowane na tym komputerze. **Pobierz klucz szyfrujący** i przechowuje go osobno: bez niego kopia nie może zostać odczytana. Funkcja Object Lock w trybie Governance lub Compliance zapobiega usunięciu obiektów przez określoną liczbę dni. Zobacz [kopia poza witryną](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Sprawdzanie kodu

Sprawdza, czy zainstalowany program jest zgodny z opublikowaną wersją.

1. Wprowadź repozytorium GitHub (oficjalne jest już wpisane) oraz tag, gałąź lub commit.
2. **Funkcja „Check now”** wysyła zapytanie do API serwisu GitHub, korzystając z trasy tego obszaru roboczego przeznaczonej dla żądań zewnętrznych, w celu uzyskania listy plików z danego commitu. Następnie porównuje identyfikator blobu git każdego mierzonego pliku programu z danym commitem. Wersja pobrana w systemie Windows z przekonwertowanymi znakami końca linii nadal jest zgodna.
3. Wynik zawiera listę zmienionych, dodatkowych i brakujących plików (po maksymalnie 50 z każdej kategorii) i jest zapisywany jako wpis `source.checked` zapis dziennika.

Wynik jest aktualny tylko tak długo, jak długo pliki uruchomionego programu pozostają niezmienione: sprawdź ponownie po aktualizacji. Nie jest wymagany żaden token, a działają wyłącznie repozytoria publiczne; czaty i dane uwierzytelniające nie są przesyłane. Dopasowanie identyfikuje kod na dysku. Nie jest to poświadczenie sprzętowe; w tym celu zapoznaj się z [Phala Cloud](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Tryby ochrony

Przełącznik obok numeru wersji pokazuje wybrany tryb oraz liczbę aktywnych spośród 18 warstw ochrony, na przykład `🟠 Witnessed 9/18`. **Zmiana trybu** w **menu „Dodatki” → „Poziom ochrony”** otwiera listę opcji. Każdy tryb opisuje konkretny cel i wskazuje, czego jeszcze brakuje; rejestrowanie, podpisywanie oraz zapisane ustawienia są takie same we wszystkich trybach.

| Tryb | Dla | Dodaje |
| --- | --- | --- |
| 🟢 Łatwe | Śledzenie czatu i przechowywanie kopii | Czat, dziennik i eksporty czatów; podpisywanie odbywa się w tle |
| 🟡 Podpisane | Zgłasza się do platformy, administratora serwera lub działu ds. nadużyć | Podpisane archiwum, kontrola dziennika, punkty kontrolne, wyciąg z przekazania |
| 🟠 Poświadczone | Sytuacje, w których ktoś może twierdzić, że zapis został zmieniony | Niezależny moduł publikujący podpisane nagłówki dziennika |
| 🔴 Gotowe do wykorzystania w sądzie | Dowody dla prawnika, policji lub sądu | Sygnatury czasowe, zaszyfrowana kopia przechowywana poza serwerem, szczegóły sprawy w raportach |
| 🟣 Zweryfikowane przez GitHub | Zapisy, których oprogramowanie musi być możliwe do sprawdzenia przez każdego | Sprawdzanie kodu i rejestrowanie działań w GitHub Actions |
| ⚫ Mossad | Sprawy o wysoką stawkę przeciwko dobrze finansowanemu przeciwnikowi | Zabezpieczony serwer działający 24 godziny na dobę, 7 dni w tygodniu, ukryty adres IP, wszystkie 18 warstw |

Warstwy: każdy zapis jest podpisany i połączony w łańcuch; podpisane potwierdzenie wykonania; załączniki zapisane za pomocą SHA-256; podpisane punkty kontrolne; ponowne sprawdzanie; alerty o problemach; dostęp świadka tylko do odczytu; świadek sprawdzający zgodnie z harmonogramem; sygnatury czasowe RFC 3161; dowody OpenTimestamps; zweryfikowana najnowsza sygnatura czasowa; zaszyfrowana kopia poza lokalizacją; szczegóły sprawy w raportach; sprawdzanie zgodności kodu ; Telegram nigdy nie widzi adresu IP tego urządzenia; żądania zewnętrzne kierowane przez serwer proxy; blokada obiektu na kopii; zapieczętowany serwer z zapisami dostawcy. Warstwa, która jest wyłączona, posiada **opcję „Konfiguruj”**, która otwiera odpowiedni formularz. Wybranie trybu niższego wymaga potwierdzenia i nie powoduje usunięcia żadnych danych.

## Więcej narzędzi

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Zapytaj archiwum**: przeszukaj zapisane obserwacje, przejrzyj źródła, a następnie zdecyduj, czy przesłać je do modelu AI. Zobacz [analizę archiwum](https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/) oraz [lokalne OCR i transkrypcję](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/).
- **Parametry**: limity i tempo gromadzenia danych, ponowne sprawdzanie, pobieranie, profile, powiadomienia i eksporty. Wyszukiwanie według nazwy, opcja „Pokaż **tylko zmienione** wartości” oraz przygotowanie ustawień domyślnych jako wersji roboczej za pomocą opcji **„Przywróć ustawienia domyślne…**”. Opcja **„Zapisz parametry”** stosuje te wartości od następnego użycia, a każda zmiana jest rejestrowana w dzienniku.
- **Dostęp**: oddzielne tokeny dla recenzentów, analityków i operatorów, ograniczone do wybranych przestrzeni roboczych, czatów i uprawnień. Zobacz [sekcję „Dostęp](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/)”.
- **Dziennik systemowy** : informacje o działaniach tego procesu od momentu uruchomienia (połączenia, zmiany serwerów proxy, logowania, odmowy, zmiany ustawień) z ukrytymi adresami IP. Opcja **„Śledź nowe wiersze”** sprawia, że najnowszy wiersz pozostaje widoczny. Wiadomości pozostają wyłącznie w dzienniku.
- **Integracje**: dostawca AI, połączenia [MCP tylko do odczytu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/) oraz [podpisane webhooki](https://phishdestroy.github.io/TgWitness/pl/docs/reference/webhooks/).
- **Case Board**: prywatne notatki zespołu, zakładki i fragmenty obok dowodów. Zobacz [Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-board/).
- **GitHub Actions przechwytuje** w sekcji „Exports”: jeden czat przechwycony z twojego forka. Zobacz [zabezpieczone przechwycenie](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
