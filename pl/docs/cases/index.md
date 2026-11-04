# Przeprowadzanie dochodzeń we wszystkich czatach

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/cases/

Cała sprawa w kanałach, grupach, czatach prywatnych i botach: zebrać, połączyć fakty, odtworzyć chronologię, przekazać.

Jeden wymyślony incydent od początku do końca. Zbieranie, wyszukiwanie i profile osób znajdują wpisy, [Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/case-board/) je porządkuje, [Report studio](https://phishdestroy.github.io/TgWitness/pl/docs/reports/) prezentuje.

PRZYPADEK Z PRAKTYKI / ZMIANA ODBIORCY PŁATNOŚCI

### Jedno zdarzenie. Cztery rozmowy. Ślad do odtworzenia.

Post na kanale kieruje do bota. Grupa rozmawia o nowym linku do płatności, a bot go pokazuje. Post zostaje zedytowany, czat prywatny powtarza link, wiadomość w grupie znika.

Kto opublikował każdą z wersji?Gdzie pojawił się ten link?Który plik został zachowany?Co uległo zmianie i kiedy?

Wczytywanie historii, AI, MCP, OCR i webhooki: [Praca z archiwum](https://phishdestroy.github.io/TgWitness/pl/docs/archive/).

## 1. Zapewnienie pełnego zakresu monitorowania całego konta

Zakres całego konta tylko na osobnym koncie. Główne konto dostaje wybrane czaty albo folder.

1. [Podłącz konto](https://phishdestroy.github.io/TgWitness/pl/docs/accounts/) w osobnej przestrzeni. Zapisz sygnaturę sprawy, ID konta, przestrzeń i odcisk klucza.
2. **Źródła → Zakres obserwacji → Tryb dochodzenia**: **Całe konto**, wszystkie cztery typy źródeł, **Własne działania**. Każdy nowy czat dostaje zapisany profil i ostatnie **200 widocznych wiadomości**. **Zapisz zakres** i potwierdź.
3. **Wczytaj czaty** i porównaj z listą czatów konta. Limit to 1000 rozmów (do 20 000 w **Parametry → Czaty czytane z listy konta**); czaty ponad limit pojawią się, gdy staną się aktywne.
4. **Ustawienia zapisu** → **Cała widoczna aktywność**, sprawdź limity załączników i miejsce na dysku. Uruchom i sprawdź na wiadomości, edycji i usunięciu.

KanałyGrupyCzat prywatnyBoty

JEDNO KONTO / JEDEN KLUCZ PODPISUJĄCY**Wszystkie wybrane działania widoczne na koncie → jeden dziennik**

Wiadomości · edycje · powiadomienia o usunięciu · widoczne reakcje · zdarzenia związane z członkostwem · własne działania

„Całe konto” to każdy czat, który to konto może otworzyć, minus wykluczenia. Bez czatów sekretnych. Nowe czaty dochodzą, gdy się pojawiają; stara historia nie pobiera się sama.

## 2. Pozyskiwanie historii i archiwizacja plików

Utwórz kolekcję w Case Board i oznacz to, co ważne. Prowadź rejestr źródeł: ID czatu, nazwa, konto, rola, początek zbierania na żywo, wynik historii, wynik mediów, luki.

| Wymagania | Działania w panelu | Co oferuje |
| --- | --- | --- |
| Historia w ramach włączonych czatów | Źródła → Wyświetl pełną historię | Dostępne wiadomości z przeszłości trafiają do dziennika obszaru roboczego wraz z opcją wstrzymania/wznowienia oraz podpisanym raportem z postępów. [Przewodnik po historii](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/). |
| Istniejący kontekst rozmowy w dzienniku | Źródła → Ustawienia rejestrowania → Migawka historii | Ostatnie wiadomości jako podpisane wpisy. Domyślnie 500, do 10 000 w **Parametry → Największy zrzut historii**. |
| Pełna, aktualnie widoczna historia jednej rozmowy | Eksport całej rozmowy → Eksportuj całą rozmowę lub Rozmowy → Eksportuj rozmowę | Osobna podpisana paczka z `chat.json` i `chat.html`, po jednej na czat. |
| Kontekst pojawienia się nowej rozmowy | Zakres obserwacji → Gdy pojawia się nowa rozmowa lub bot | Jego profil i do 1000 ostatnich wiadomości (200 w trybie dochodzenia). Nie dotyczy istniejących czatów. |
| Liczba bajtów załącznika | Pobieranie widocznych załączników + limity dla poszczególnych typów | Szukaj `media.saved` z SHA-256 i rozmiarem. W kolejce, pominięte lub z błędem oznacza: niezapisane. |

Eksport czatu nie trafia do dziennika ani do profili osób. Aby przeszukiwać starą historię w TgWitness, użyj **Wczytaj całą historię** albo zrzutów.

Tutaj: kanał, grupa, czat z botem i czat prywatny, plus plik faktury i jego skrót. Tego, co usunięto przed zbieraniem, już nie odzyskasz.

## 3. Proszę śledzić rozwój rozmowy oraz swoje własne działania

Niech działa. Oznacz gorące czaty gwiazdką jako priorytetowe, ustaw ponowne sprawdzanie w **Ustawienia zapisu → Ponowne sprawdzanie** i pilnuj `recheck.completed`, FloodWait i wyników mediów.

**Czaty → Profil → Zapisz profil teraz** zapisuje opis czatu, polecenia bota i inne metadane.

**Obserwowanie bota lub skorzystanie z zaproszenia w ramach sprawy**

1. **Czaty → Otwórz link Telegrama**, najpierw zapisz podgląd. Link i podgląd stają się podpisanymi wpisami.
2. W razie potrzeby **Dołącz / otwórz i obserwuj** dołącza do czatu albo uruchamia bota z jego parametrem startowym.
3. Aby udokumentować działanie, odpowiedz albo użyj **Naciśnij przycisk** w panelu. Dostaniesz `interaction.requested` i `interaction.result` z odpowiedzią bota.

To prawdziwe działania. Przyciski naciśnięte w innej aplikacji nie są widoczne, tylko odpowiedź bota. Bez aplikacji webowych, płatności i telefonu/lokalizacji.

## 4. Śledzenie osób, linków i plików w różnych czatach

1. **Dziennik**, **Wszystkie źródła**, szukaj frazy, domeny lub nazwy użytkownika. Otwieraj wyniki i wysyłaj je **Na tablicę**.
2. **Czaty → Osoby → Włącz profile**, wybierz osobę: historia nazw, odpowiedzi, aktywność, **Także w…**, linki, portfele, telefony. Otwieraj cytowane wpisy.
3. Śledź ten sam liczbowy ID użytkownika w innych czatach. Zgodna nazwa, portfel czy awatar to trop, a nie dowód.
4. Porównaj skróty plików. Ten sam SHA-256 = te same bajty. Kto je udostępnił, to osobne pytanie.

MAPA SPRAWY / PRZEŚLEDŹ ODNIESIENIAPrzykładowa sprawa · nie jest to wykres na żywo

KANAŁ / OGŁOSZENIE**Oryginał → zredagowana wersja docelowa**

Zapisy nr 101, nr 188, wiadomość nr 84 · nadawca nieokreślony

GRUPA / DZIAŁALNOŚĆ**Użytkownik 71001 publikuje nowy link**

Zapis nr 146 · wiadomość nr 309 Potwierdzenie zapisania pliku nr 151

ROZMOWA DOTYCZĄCA BOTA / ZAMÓWIENIA**Przycisk prowadzi do tej strony**

Zapis nr 173 · wiadomość nr 12 Metadane przycisku „Powrót”

PRYWATNE / DALSZE DZIAŁANIA**Użytkownik 71001 ponownie podaje miejsce docelowe**

Zapis nr 205 · wiadomość nr 922 Potwierdzenie zapisania pliku nr 209

Cztery czaty zawierają różne spostrzeżenia. Należy śledzić rekordy źródłowe dla każdego połączenia; wpis na kanale nie ma przypisanej osoby wysyłającej.

Numeryczne identyfikatory i odniesienia do rekordów zostały wymyślone na potrzeby niniejszego przewodnika. Ta mapa objaśniająca pokazuje, jak połączyć wyniki wyszukiwania, profile i sprawdzone rekordy; Case Board przechowuje odpowiednie karty i odniesienia do źródeł.

| Połączenie | Uwagi uzupełniające | Wniosek: należy zachować |
| --- | --- | --- |
| To samo konto w serwisie Telegram | Użytkownik o identyfikatorze 71001 w grupie nr 146 oraz w prywatnym czacie nr 205 | Ten sam ID nadawcy w obu czatach. Kim jest w prawdziwym życiu — to inne pytanie. |
| Powtarzające się miejsce docelowe | `pay.example.invalid/new` w #146, metadane przycisku #173, edytowany wpis #188 i #205 | Ten sam link w czterech miejscach. Kto nim steruje — do tego potrzeba innych źródeł. |
| Ta sama liczba bajtów pliku | Identyczne pełne wartości SHA-256 w uzupełnionych potwierdzeniach odbioru multimediów nr 151 i nr 209 | Oba pliki są identyczne co do bajtu. |

Profile obejmują tylko osoby, które coś napisały w *tej przestrzeni*, to nie lista członków. Liczba cytatów na fakt: **Parametry → Wpisów cytowanych na fakt**.

## 5. Odtworzyć sekwencję i zaznaczyć luki

Wersje w **Czatach**, potem **Dziennik** z **Wszystkie źródła** + **Edycje**, **Usunięcia**, **Pokrycie**. W chronologii podawaj oba czasy: datę z Telegrama i moment obserwacji.

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

Kolejność w dzienniku to kolejność napływu, niekoniecznie kolejność zdarzeń. Trzymaj osobno wpisy na żywo, zrzuty, odzyskane wiadomości, usunięcia i „nie znaleziono przy ponownym sprawdzeniu”, a każdą lukę oznaczaj jako nieznaną.

## 6. Rozszerzenie zakresu na inne konta służące do gromadzenia danych

Jedna przestrzeń na konto, te same kroki. Zapisz rolę i odcisk każdego. Numery wiadomości są osobne dla każdego konta, więc zawsze podawaj przestrzeń i czat.

[Grupa kont](https://phishdestroy.github.io/TgWitness/pl/docs/groups/) pokazuje stan, dzieli ustawienia i eksportuje wszystkich razem — każde z własnym dziennikiem i kluczem. Wspólną chronologię kont budujesz we własnych notatkach.

Długa sprawa? Dodaj [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/witness/) i sprawdź, co naprawdę łapie każde konto.

## 7. Dostarczenie pakietu dowodowego umożliwiającego weryfikację

Podpisany ZIP z każdej przestrzeni (zawsze cały dziennik, filtry nie mają znaczenia), plus profile osób, eksporty czatów i pliki.

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

Odciski przekazuj osobno. Weryfikuj wszystko wobec jego własnej przestrzeni:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Zachowaj wynik weryfikatora, oryginały, pokrycie i zapis przekazania razem z wnioskami. Opracuj całość w Report studio. Jeśli odbiorca potrzebuje mniej, przygotuj [ograniczone przekazanie](https://phishdestroy.github.io/TgWitness/pl/docs/handover/).
