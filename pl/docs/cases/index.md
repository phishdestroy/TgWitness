# Przeprowadzanie dochodzeń we wszystkich czatach

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/cases/

Przeprowadź całą sprawę, obejmującą różne kanały, grupy, czaty prywatne i boty: gromadź, łącz, odtwarzaj i przekazuj dowody.

Niniejszy przewodnik przedstawia przebieg jednego fikcyjnego zdarzenia na podstawie kompletnego zapisu. Wykorzystuje on rzeczywiste funkcje gromadzenia danych, wyszukiwania, tworzenia profili osób oraz eksportu. Mapa sprawy stanowi przykład dokumentacji; Państwa wnioski oraz rejestr spraw są przechowywane poza aplikacją.

PRZYPADEK Z PRAKTYKI / ZMIANA ODBIORCY PŁATNOŚCI

### Jedno zdarzenie. Cztery rozmowy. Ślad do odtworzenia.

Ogłoszenie na kanale wskazuje na bota. Grupa operacyjna omawia nowy link do płatności. Prywatna wiadomość uzupełniająca powtarza tę informację. Później ogłoszenie zostaje edytowane, a wiadomość grupowa znika.

Kto opublikował każdą z wersji?Gdzie pojawił się ten link?Który plik został zachowany?Co uległo zmianie i kiedy?

Aby uzyskać informacje na temat wczytywania historii, opcjonalnej weryfikacji źródeł przez sztuczną inteligencję, MCP, OCR oraz wychodzących webhooków, zobacz [sekcję „Praca z archiwum](https://phishdestroy.github.io/TgWitness/pl/docs/archive/)”.

## 1. Zapewnienie pełnego zakresu monitorowania całego konta

1. [Proszę podłączyć konto służące do gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/docs/accounts/) w oddzielnym obszarze roboczym. Proszę odnotować numer referencyjny sprawy, identyfikator konta, nazwę obszaru roboczego oraz odcisk palca klucza podpisu w notatkach dotyczących sprawy.
2. **Źródła** otwarte **→ Zakres obserwacji → Tryb dochodzeniowy**. Przejrzyj **całe konto**, wszystkie cztery typy źródeł oraz **własne działania**. To ustawienie wstępne umożliwia zapisanie profilu nowego źródła oraz jego ostatnich **200 widocznych wiadomości**. Proszę nacisnąć **przycisk „Zapisz zakres”** i potwierdzić wybrany zakres.
3. Naciśnij przycisk **„Załaduj czaty**”. Porównaj źródła z listą rozmów na koncie i sprawdź wykluczenia. W sekcji **„Parametry” → „Czaty odczytywane z listy konta**” dostosuj w razie potrzeby początkowy limit listy: domyślnie wynosi on 1 000 rozmów, można go skonfigurować do 20 000. Czatów wykraczających poza ten limit nie wykrywa się, dopóki nie staną się aktywne.
4. W **ustawieniach rejestrowania** należy wybrać opcję **„Wszystkie widoczne działania**” i zapisać ją. Należy sprawdzić typy załączników, limity rozmiaru oraz ilość wolnego miejsca na dysku. Przed rozpoczęciem korzystania z konfiguracji należy uruchomić monitorowanie oraz zweryfikować, czy narzędzie poprawnie rejestruje kontrolowaną wiadomość, jej edycję oraz usunięcie.

KanałyGrupyCzat prywatnyBoty

JEDNO KONTO / JEDEN KLUCZ PODPISUJĄCY**Wszystkie wybrane działania widoczne na koncie → jeden dziennik**

Wiadomości · edycje · powiadomienia o usunięciu · widoczne reakcje · zdarzenia związane z członkostwem · własne działania

Opcja „Całe konto” obejmuje czaty, do których konto to ma dostęp, wraz ze skonfigurowanymi typami źródeł i wykluczeniami. Czaty tajne są niedostępne. Nowe okna dialogowe są dodawane w miarę pojawiania się aktualizacji; włączenie tego trybu nie powoduje automatycznego pobrania pełnej historii wszystkich istniejących czatów.

## 2. Pozyskiwanie historii i archiwizacja plików

Proszę utworzyć rejestr źródeł dla całego dochodzenia. Każdej rozmowie należy przyporządkować wiersz zawierający jej identyfikator numeryczny, tytuł, konto, uprawnienia/rolę, datę rozpoczęcia monitorowania na żywo, datę pozyskania historii, wyniki dotyczące multimediów oraz znane luki. Źródło należy oznaczyć jako pozyskane dopiero po sprawdzeniu odpowiednich wyników.

| Wymagania | Działania w panelu | Co oferuje |
| --- | --- | --- |
| Historia w ramach włączonych czatów | Źródła → Wyświetl pełną historię | Obecna funkcja główna: dostępne wiadomości z przeszłości trafiają do dziennika obszaru roboczego wraz z opcją wstrzymania/wznowienia oraz podpisanym raportem z postępów. [Przewodnik po historii](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/). |
| Istniejący kontekst rozmowy w dzienniku | Źródła → Ustawienia rejestrowania → Migawka historii | Najnowsze widoczne wiadomości jako podpisane obserwacje. Domyślna maksymalna liczba to 500; w sekcji **Parametry → Największy zrzut historii** można zwiększyć tę liczbę do 10 000. |
| Pełna, aktualnie widoczna historia jednej rozmowy | Eksport całej rozmowy → Eksportuj całą rozmowę lub Rozmowy → Eksportuj rozmowę | Oddzielny, podpisany pakiet zawierający klucze `chat.json` i `chat.html`. Czynność należy powtórzyć dla każdego źródła; należy zachować wyniki zakończenia lub niepowodzenia. |
| Kontekst pojawienia się nowej rozmowy | Zakres obserwacji → Gdy pojawia się nowa rozmowa lub bot | Profil źródła oraz do 1 000 ostatnich widocznych wiadomości; tryb śledczy wybiera 200. Istniejące czaty nie są objęte tym procesem z mocą wsteczną. |
| Liczba bajtów załącznika | Pobieranie widocznych załączników + limity dla poszczególnych typów | Należy sprawdzić obecność kodu `media.saved`, jego wartość SHA-256 oraz liczbę bajtów. Plik znajdujący się w kolejce, pominięty lub pobrany nieprawidłowo nie jest traktowany jako zachowany. |

Pełny eksport czatu stanowi oddzielną migawkę; nie powoduje on zaimportowania całej historii do dziennika ani profili użytkowników. Aby przeszukiwać materiały historyczne w TgWitness, należy skorzystać z opcji **„Załaduj pełną historię** ze wszystkich włączonych źródeł” lub z ograniczonych migawek dziennika. Przed rozpoczęciem operacji należy sprawdzić listę źródeł.

W analizowanym przypadku należy pozyskać kanał ogłoszeniowy, grupę operacyjną, rozmowę z botem oraz prywatną korespondencję uzupełniającą. Należy zachować bajty i skrót pliku załączonego do wiadomości. Dostępna obecnie historia nie pozwala na odtworzenie wiadomości usuniętej przed jej przechwyceniem ani pośredniej edycji, której Telegram już nie udostępnia.

## 3. Proszę śledzić rozwój rozmowy oraz swoje własne działania

Proszę kontynuować monitorowanie w miarę rozwoju sprawy. Proszę oznaczyć aktywne czaty związane ze sprawą jako źródła priorytetowe; skonfigurować ponowne sprawdzanie źródeł priorytetowych i innych w sekcji **Ustawienia rejestrowania → Ponowne sprawdzanie**. Proszę weryfikować wyniki `recheck.completed`, dalsze uzupełnianie danych, FloodWait oraz wyniki dotyczące multimediów w miarę postępów prac.

Proszę skorzystać z **opcji „Czat” → „Profil” → „Zapisz profil teraz”**, aby zachować aktualne opisy źródeł, polecenia bota oraz inne metadane zwracane przez Telegram. Ten profil źródła jest odrębny od profili osób tworzonych na podstawie wiadomości z dziennika.

**Obserwowanie bota lub skorzystanie z zaproszenia w ramach sprawy**

1. W **sekcji „Czat” → „Otwórz link w Telegramie**” należy najpierw zapisać podgląd. Oryginalny link oraz wygenerowany podgląd stają się podpisanymi zapisami.
2. Jeśli wymaga tego dochodzenie, **polecenie „Join / open and observe”** powoduje dołączenie do źródła lub jego otwarcie oraz uruchamia bota z podanym parametrem startowym. Oczekujące zaproszenie do dołączenia pozostaje w rejestrze jako oczekujące.
3. W przypadku czynności, którą należy udokumentować, należy skorzystać z odpowiedzi tekstowej w panelu lub obsługiwanej funkcji **przycisku „Naciśnij**”. Dziennik zachowuje wartości `interaction.requested` i `interaction.result`, w tym zwracany tekst wywołania zwrotnego lub adres URL.

Te elementy sterujące wykonują rzeczywiste działania w aplikacji Telegram. Naciśnięcie przycisku zwrotnego w innej aplikacji Telegram nie jest widoczne dla modułu zbierającego dane; widoczna może być natomiast kolejna wiadomość lub edycja wysłana przez bota. Aplikacje internetowe, płatności oraz żądania dotyczące numeru telefonu i lokalizacji pozostają poza zasięgiem mini-klienta.

## 4. Śledzenie osób, linków i plików w różnych czatach

1. Otwórz **dziennik**, pozostaw filtr źródeł ustawiony na **„Wszystkie źródła”** i wyszukaj charakterystyczną frazę, domenę, nazwę użytkownika lub zapisany identyfikator. Otwórz każdy pasujący wpis i zanotuj nazwę czatu, identyfikator wiadomości oraz numer sekwencyjny w dzienniku.
2. Aby przejść do odpowiedniej rozmowy, proszę otworzyć **sekcję „Rozmowy” → „Osoby” → „Włącz profile”**, a następnie wybrać daną osobę. Proszę przejrzeć historię nazwisk/nazw użytkowników, relacje odpowiedzi, aktywność, **a także sekcję „Również w…” zawierającą** inne obserwowane rozmowy oraz wyodrębnione linki, portfele lub numery telefonów. Proszę otworzyć cytowane wpisy w dzienniku.
3. Proszę śledzić ten sam numeryczny identyfikator użytkownika Telegrama w innych czatach w tej przestrzeni roboczej. Proszę traktować pasującą nazwę, wzmiankę o portfelu lub podobny awatar jako wskazówkę do sprawdzenia. Wzmianka o adresie nie potwierdza własności; podobny awatar nie oznacza, że chodzi o tę samą osobę.
4. Porównaj wartości SHA-256 zachowanych załączników w poszczególnych wpisach. Identyczne skróty potwierdzają zgodność bajtową zapisanych plików. Przed wyciągnięciem wniosków dotyczących tego, kto je udostępnił, należy sprawdzić powiązane wpisy wiadomości i nadawców.

MAPA SPRAWY / PRZEŚLEDŹ ODNIESIENIAPrzykładowa sprawa · nie jest to wykres na żywo

KANAŁ / OGŁOSZENIE**Oryginał → zredagowana wersja docelowa**

Zapisy nr 101, nr 188, wiadomość nr 84 · nadawca nieokreślony

GRUPA / DZIAŁALNOŚĆ**Użytkownik 71001 publikuje nowy link**

Zapis nr 146 · wiadomość nr 309 Potwierdzenie zapisania pliku nr 151

ROZMOWA DOTYCZĄCA BOTA / ZAMÓWIENIA**Przycisk prowadzi do tej strony**

Zapis nr 173 · wiadomość nr 12 Metadane przycisku „Powrót”

PRYWATNE / DALSZE DZIAŁANIA**Użytkownik 71001 ponownie podaje miejsce docelowe**

Zapis nr 205 · wiadomość nr 922 Potwierdzenie zapisania pliku nr 209

Cztery czaty zawierają różne spostrzeżenia. Należy śledzić zapisy źródłowe dla każdego połączenia; nie należy przypisywać wpisu na kanale do użytkownika 71001 bez podania nadawcy.

Numeryczne identyfikatory i odniesienia do zapisów zostały wymyślone na potrzeby niniejszego przewodnika. Niniejsza mapa wyjaśnia przebieg pracy analityka z wykorzystaniem funkcji wyszukiwania, profili oraz przeglądu zapisów; aplikacja nie generuje globalnego wykresu śledczego.

| Połączenie | Uwagi uzupełniające | Wniosek: należy zachować |
| --- | --- | --- |
| To samo konto w serwisie Telegram | Użytkownik o identyfikatorze 71001 w grupie nr 146 oraz w prywatnym czacie nr 205 | W obu rozmowach podano ten sam identyfikator nadawcy. Kwestia tożsamości w rzeczywistości pozostaje odrębnym zagadnieniem. |
| Powtarzające się miejsce docelowe | `pay.example.invalid/new` w #146, metadane przycisku #173, edytowany wpis #188 i #205 | Ta sama strona docelowa pojawia się w czterech zaobserwowanych kontekstach. Sam ten fakt nie pozwala ustalić, kto ją kontroluje. |
| Ta sama liczba bajtów pliku | Identyczne pełne wartości SHA-256 w uzupełnionych potwierdzeniach odbioru multimediów nr 151 i nr 209 | Dwa zachowane załączniki są identyczne pod względem bajtów. Same nazwy plików lub miniatury nie pozwoliłyby tego ustalić. |

Profile użytkowników obejmują autorów, których wiadomości zostały zapisane w danym czacie, i powiązują ich z innymi czatami w tym *samym dzienniku obszaru roboczego*. Nie stanowią one kompletnego wykazu członków. Skróty awatarów pochodzą z oddzielnej lokalnej pamięci podręcznej; liczba cytowań w profilach podlega konfiguracji w sekcji **Parametry → Liczba cytowanych wpisów na fakt**.

## 5. Odtworzyć sekwencję i zaznaczyć luki

W **sekcji „Czat”** proszę przejrzeć zapisane wersje oraz linki do **wpisów w dzienniku o numerach #…** W sekcji **„Dziennik**” proszę skorzystać z opcji **„Wszystkie źródła**” oraz **„Edycje”**, **„Usunięcia”** i **„Zakres**”. Proszę stworzyć oś czasu sprawy, uwzględniając zarówno datę podaną przez Telegram, jak i czas obserwacji określony przez osobę gromadzącą dane.

1. 09:00 · #101**Zrzut wpisu z kanału**

   Zachowano pierwotny adres docelowy.
2. 09:12 · #146 / #151**Grupa udostępnia inny link**

   Użytkownik 71001 publikuje wpis; pobieranie załącznika zostaje zakończone.
3. 09:16 · #173**Bot wskazuje ten sam adres docelowy**

   Link znajduje się w zapisanych metadanych z klawiatury.
4. 09:20 · #188**Zmiany w ogłoszeniach na kanale**

   Zachowane zostają zarówno oryginalne, jak i edytowane obserwacje.
5. 09:24 · #205 / #209**Prywatna wiadomość uzupełniająca powtarza to**

   Zapisany załącznik posiada ten sam pełny skrót SHA-256 co #151.
6. 09:28 · #231**Pojawia się powiadomienie o usunięciu grupy**

   Wcześniejsza uwaga pozostaje aktualna: nie podano ani osoby, która dokonała usunięcia, ani dokładnego czasu usunięcia.

Przykładowe czasy obserwacji i odniesienia. Pomiędzy tymi wpisami znajdują się inne zapisy dziennika.

Kolejność wpisów w dzienniku odpowiada kolejności ich otrzymania, a niekoniecznie pierwotnym działaniom w aplikacji Telegram. Starsza migawka historii może pojawić się po nowszej wiadomości na żywo. Należy wyraźnie rozróżniać obserwacje na żywo, migawki, odzyskane wiadomości, powiadomienia o usunięciu oraz przypadki „braku przy ponownej weryfikacji”. W miejscach, gdzie w zakresie pokrycia występuje luka, należy wyraźnie zaznaczyć nieznany przedział czasowy; późniejsza migawka nie usuwa tej luki.

## 6. Rozszerzenie zakresu na inne konta służące do gromadzenia danych

Należy utworzyć osobny obszar roboczy dla każdego odrębnego konta i powtórzyć proces określenia zakresu oraz sporządzenia wykazu historii. Należy odnotować przynależność/rolę oraz odcisk klucza podpisującego dla każdego z nich. Identyfikatory należy kwalifikować według obszaru roboczego i czatu: ten sam numer wiadomości nie stanowi globalnego identyfikatora obejmującego wszystkie konta.

Porównaj istotne spostrzeżenia w notatkach dotyczących sprawy lub narzędziach analitycznych, zachowując odniesienie do konta i dziennika dla każdego wiersza. TgWitness nie oferuje obecnie jednej globalnej wyszukiwarki, połączonej osi czasu, wykresu kontaktów ani archiwum spraw obejmującego wszystkie obszary robocze. Pełny eksport jednego kanału lub supergrupy z wielu kont stanowi odrębną funkcję; nie jest to połączenie dzienników wszystkich kont.

W przypadku dłuższych działań należy zaangażować [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/witness/) w celu zachowania wcześniej ustalonych granic. Proszę skorzystać z pilotażowego programu kontrolowanej dostawy, aby zweryfikować ścieżki przechwytywania kont oraz ich widoczność.

## 7. Dostarczenie kompletnego, weryfikowalnego pakietu dowodowego

Z każdego obszaru roboczego można wyeksportować plik ZIP zawierający podpisany dziennik. Zawiera on pełną treść zarejestrowanego dziennika, niezależnie od filtrów wyszukiwania zastosowanych w panelu. Istnieje możliwość oddzielnego eksportowania profili odpowiednich osób, zachowania pełnych zestawów historii czatów oraz kompletnych dowodów w postaci załączników.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Proszę przechowywać zaufane odciski palców w oddzielnym kanale. Z poziomu zaufanej instalacji należy zweryfikować każdy artefakt pod kątem jego tożsamości w ramach własnego obszaru roboczego:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Proszę sprawdzić rzeczywiste wyniki weryfikacji, zachować oryginały oraz przechować raport z zakresu analizy, informacje o nieudanych operacjach pozyskiwania danych oraz rejestr transferów wraz z Państwa ustaleniami. Folder nadrzędny sprawy oraz wnioski analityków są tworzone zewnętrznie; poszczególne artefakty TgWitness posiadają własne podpisy.

## Proszę stosować tę samą metodę w przypadku innych dochodzeń

**Spór dotyczący zamówienia lub płatności obsługiwany przez bota**

**Pytanie:** co obiecał bot, jaki był docelowy przycisk oraz co uległo zmianie później?

**Ścieżka:** wpis na kanale → zapisany podgląd linku bota → parametr uruchomienia bota → wersje wiadomości i wpisów z klawiatury → wszelkie potwierdzenia wywołania zwrotnego wysłane przez panel → dalsze działania w grupie lub w rozmowie prywatnej. Należy dopasować każdy element docelowy do jego rekordu źródłowego; zachować opisy profili oraz kompletne pliki multimedialne.

**Należy przedstawić:** oś czasu zawierającą zaobserwowaną ofertę i odpowiedzi, odniesienia do źródeł oraz zweryfikowane eksporty danych. Wyświetlony link do płatności nie stanowi dowodu na to, że płatność miała miejsce.

**Wiadomości usunięte po incydencie związanym z wymianą wiadomości między czatami**

**Pytanie:** co zaobserwowano jeszcze przed zniknięciem istotnych wiadomości?

**Ślad:** wszystkie czaty, których dotyczy zdarzenie → oryginalne wiadomości → dostarczone zmiany → powiadomienia o usunięciu lub późniejsze wyniki wskazujące na brak wiadomości przy ponownej weryfikacji → zachowane załączniki → relacje dotyczące zdarzenia. Proszę porównać obserwacje z niezależnych źródeł wraz z podaną informacją o ich widoczności.

**Należy przedstawić:** sekwencję zachowanych wersji oraz wyraźnie zaznaczone nieznane przedziały czasowe. Nie należy traktować braku wiadomości w historii jako dowodu na to, że dana osoba ją usunęła.

**Jeden z uczestników zmienia imiona w kilku czatach**

**Pytanie:** Która z zaobserwowanych czynności należy do tego samego konta w Telegramie pomimo zmiany nazwy?

**Ścieżka:** numeryczny identyfikator nadawcy → historia zapisanych nazw/nazw użytkowników → odpowiedzi → inne czaty w obszarze roboczym → wymienione miejsca docelowe i zapisane pliki. Należy sprawdzić zapisy źródłowe dla każdego zgłoszonego połączenia; należy oddzielnie traktować konta o podobnych nazwach.

**Dostarczamy:** cytowaną oś czasu aktywności konta oraz odrębne hipotezy dotyczące powiązań. Podobieństwo nazwisk oraz wartość pHash awatara stanowią wskazówki, a nie dowód tożsamości.
