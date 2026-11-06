# Jak działa ten rejestr dowodów

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/

Wyjaśnienie pojęć łańcucha skrótów, podpisów, punktów kontrolnych i świadków wraz z dokładnymi wzorami stosowanymi przez weryfikatora.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dowody i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

![Dowody i weryfikacja](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

TgWitness zachowuje dane zebrane przez konto gromadzące, łączy te obserwacje w podpisany dziennik i umożliwia innej osobie weryfikację eksportowanych danych przy użyciu zaufanego klucza oraz wcześniej zachowanego punktu kontrolnego.

[Lokalna strona internetowa z dokumentacją](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) zawiera interaktywne przykłady w sekcji `/docs/concepts/`, narzędzie do przeglądania decyzji dotyczących punktów kontrolnych w sekcji `/docs/witness/` oraz instrukcje dotyczące [Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-board/), [projektowania raportów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/) i [fragmentów dokumentacji przekazywania](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#handover-extract). Wszystkie przykładowe wiadomości, liczby i opóźnienia są fikcyjne. Skróty w piaskownicy łańcucha są obliczane za pomocą algorytmu SHA-256 w przeglądarce. Żadne dane nie są wysyłane do serwisu Telegram.

**Na tej stronie**

- [Zmiany w wiadomościach; gromadzenie obserwacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/#a-message-changes-observations-accumulate)
- [Co obejmuje skrót](https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/#what-a-hash-covers)
- [Co dodaje wcześniejszy punkt kontrolny](https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/#what-an-earlier-checkpoint-adds)
- [Gdzie należy umieścić świadka](https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/#where-a-witness-belongs)
- [Sprawdzenie działania w odniesieniu do znanych działań](https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/#test-delivery-against-known-actions)
- [Wybierz schemat działania](https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/#pick-a-workflow)

## Wiadomość ulega zmianie; obserwacje się kumulują

Diagram sekwencji · Telegram → Kolektor: Nowa wiadomość: Spotkanie o godz. 10:00; Kolektor → Podpisany dziennik: Dodaj wiadomość.new; Telegram → Kolektor: Aktualizacja: Spotkanie o godz. 11:00; Kolektor → Podpisany dziennik: Dodaj wiadomość.edited; Telegram → Kolektor: Powiadomienie o usunięciu; Kolektor → Podpisany dziennik: Dodaj wiadomość.usunięto; Uwaga dotycząca Podpisany dziennik: Zachowane są informacje o treści oryginalnej, edycjach oraz usunięciach · Telegram · Kolektor · Podpisany dziennik · Nowa wiadomość: Spotkanie o godz. 10:00 · Dodaj wiadomość.new · Aktualizacja: Spotkanie o godz. 11:00 · Dodaj wiadomość.edited · Powiadomienie o usunięciu · Dodaj wiadomość.usunięto · Zachowane są informacje o treści oryginalnej,edycjach oraz usunięciach

**Schemat w formie tekstowej**

1. Telegram → Kolektor: Nowa wiadomość: Spotkanie o godz. 10:00
2. Kolektor → Podpisany dziennik: Dodaj wiadomość.new
3. Telegram → Kolektor: Aktualizacja: Spotkanie o godz. 11:00
4. Kolektor → Podpisany dziennik: Dodaj wiadomość.edited
5. Telegram → Kolektor: Powiadomienie o usunięciu
6. Kolektor → Podpisany dziennik: Dodaj wiadomość.usunięto
7. Uwaga dotycząca Podpisany dziennik: Zachowane są informacje o treści oryginalnej, edycjach oraz usunięciach

Ta uproszczona sekwencja zakłada, że Telegram dostarczył każdą aktualizację, a wybrane konto miało do niej wgląd. W dzienniku odnotowywane są również zdarzenia operacyjne. Powiadomienie o usunięciu nie podaje osoby dokonującej usunięcia ani dokładnego czasu usunięcia. Powtarzające się dostarczenia są oddzielnymi obserwacjami; nie ma funkcji eliminacji duplikatów w całym dzienniku.

## Co obejmuje skrót (hash)

![Obserwacja, kodowanie, generowanie skrótu i podpisywanie: każde nowe zdarzenie zawiera poprzedni skrót.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Proszę zapoznać się z formułą od końca do początku: **C** przekształca dziewięć pól w konkretne bajty; **SHA-256** generuje ich skrót; **format szesnastkowy** służy do przechowywania tego skrótu. Poprzedni skrót znajduje się już w zdarzeniu. **Funkcja unhex** przekształca zapisany skrót z powrotem w 32 bajty, które są podpisywane przez algorytm Ed25519.

[Schemat łańcucha statycznego](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Niech C(ei) będzie kanonicznym plikiem JSON w formacie UTF-8 zawierającym dziewięć pól zdarzeń. Pierwszy rekord `previous_hash` składa się z 64 znaków zerowych. Każdy kolejny rekord zawiera szesnastkowy skrót poprzedniego rekordu:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

Podpis obejmuje 32 bajty surowego skrótu. Dane wejściowe skrótu zawierają dokładnie `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` oraz `previous_hash`. Klucze obiektów są posortowane; pominięto spacje i znaki ASCII z symbolami escape; wartości NaN i nieskończoność są odrzucane. Proszę zapoznać się z [dokładnym kodowaniem](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#event-canonicalization).

Schemat blokowy · 64 znaki zerowe → Wpis 1 / skrót h1; Wpis 1 / skrót h1 → Zapis nr 2 zawiera nagłówek h1 / hash h2; Zapis nr 2 zawiera nagłówek h1 / hash h2 → Zapis nr 3 zawiera nagłówek h2 / hash h3; Zapis nr 3 zawiera nagłówek h2 / hash h3 → Podpisany punkt kontrolny: liczba 3, nagłówek h3 (przechowywać w innym miejscu) · 64 znaki zerowe · Wpis 1 / skrót h1 · Zapis nr 2 zawieranagłówek h1 / hash h2 · Zapis nr 3 zawieranagłówek h2 / hash h3 · Podpisany punktkontrolny: liczba 3,nagłówek h3 · przechowywać w innym miejscu

**Schemat w formie tekstowej**

1. 64 znaki zerowe → Wpis 1 / skrót h1
2. Wpis 1 / skrót h1 → Zapis nr 2 zawiera nagłówek h1 / hash h2
3. Zapis nr 2 zawiera nagłówek h1 / hash h2 → Zapis nr 3 zawiera nagłówek h2 / hash h3
4. Zapis nr 3 zawiera nagłówek h2 / hash h3 → Podpisany punkt kontrolny: liczba 3, nagłówek h3 (przechowywać w innym miejscu)

| Zmiana w dostarczonym dzienniku | Co to wykrywa |
| --- | --- |
| Zmodyfikować rekord nr 2, zachowując jego zapisany skrót | Przeliczony skrót zdarzenia jest inny; jego podpis nie obejmuje już zmienionego zdarzenia |
| Odtworzenie zmienionego zapisu oraz wszystkich późniejszych skrótów | Oryginalne podpisy są nieprawidłowe; zachowany punkt kontrolny na danej granicy również wykazuje rozbieżności |
| Należy usunąć końcówkę, zachowując jednak pozostałą część przedrostka w niezmienionej postaci | Wcześniejszy zapisany punkt kontrolny, wykraczający poza podany prefiks, wskazuje, że eksport jest zbyt krótki |
| Ponowne podpisanie zastępczego dziennika za pomocą innego klucza | Oddzielny, zaufany odcisk klucza odrzuca próbę podmiany tożsamości |

![Zmiana wartości w zapisanym polu powoduje zmianę jego skrótu; ponowne wygenerowanie skrótów nie przywraca oryginalnych podpisów.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Proszę wypróbować tę logikę na zapisie nr 2:** proszę zmienić `Meet at 11:00` na `Meet at 12:00` w zapisanym zdarzeniu. Jego ponownie obliczony skrót już się nie zgadza. Ponowne obliczenie późniejszej sekwencji może naprawić jej ogniwa, ale nie jest w stanie sprawić, by oryginalne podpisy obejmowały nowe skróty. Natomiast zaobserwowana edycja w Telegramie staje się nowym wpisem w dzienniku.

[Schemat zmian statycznych](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Same linki do skrótów nie uniemożliwiają komuś ponownego obliczenia łańcucha zastępczego. Zaufanie wynika ze sprawdzania podpisów przy użyciu niezależnego, zaufanego klucza oraz porównywania ich z danymi referencyjnymi przechowywanymi poza systemem gromadzącym dane.

## Co wnosi wcześniejszy punkt kontrolny

![Należy zachować liczbę 3 oraz nagłówek h3; późniejszy eksport 4 rekordów jest sprawdzany w pozycji 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Odniesienie pozostaje niezmienne, podczas gdy dziennik się powiększa.** Jeśli punkt kontrolny wskazuje „3 rekordy, nagłówek h3”, eksport zawierający cztery rekordy może zostać zaakceptowany poprzez dopasowanie nagłówka h3 w pozycji 3. Najnowszym nagłówkiem jest h4, który zgodnie z oczekiwaniami powinien się różnić. Eksport zawierający tylko dwa rekordy zakończy się niepowodzeniem.

[Schemat statycznych punktów kontrolnych](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Po zweryfikowaniu podpisu punktu kontrolnego należy:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Eksport może wykraczać poza punkt kontrolny. Musi on być zgodny na zachowanej granicy. Rzeczywisty weryfikator sprawdza również sekwencję każdego zdarzenia, poprzedni link, skrót oraz podpis. Porównanie wyłącznie końcowego, zapisanego nagłówka spowodowałoby pominięcie zmienionego rekordu wewnętrznego, którego zapisany skrót nie został zaktualizowany.

## Gdzie należy świadek

Schemat blokowy · Moduł gromadzący / sesja konta / klucz A → Punkt końcowy punktu kontrolnego tylko do odczytu; Witness / klucz kolektora przypięty / klucz własny B → Oddzielny, podpisany dziennik dowodowy; Witness / klucz kolektora przypięty / klucz własny B → Punkt końcowy punktu kontrolnego tylko do odczytu (Poproś o weryfikację); Punkt końcowy punktu kontrolnego tylko do odczytu → Witness / klucz kolektora przypięty / klucz własny B (Podpisana odpowiedź); Witness / klucz kolektora przypięty / klucz własny B → Kanał zawierający podpisane posty TGW1 (API bota / własny token) · Serwer A · Host B · Moduł gromadzący / sesjakonta / klucz A · Punkt końcowy punktukontrolnego tylko doodczytu · Witness / klucz kolektoraprzypięty / klucz własny B · Oddzielny, podpisanydziennik dowodowy · Kanał zawierającypodpisane posty TGW1 · Poproś o weryfikację · Podpisana odpowiedź · API bota / własny token

**Schemat w formie tekstowej**

1. Moduł gromadzący / sesja konta / klucz A → Punkt końcowy punktu kontrolnego tylko do odczytu
2. Witness / klucz kolektora przypięty / klucz własny B → Oddzielny, podpisany dziennik dowodowy
3. Witness / klucz kolektora przypięty / klucz własny B → Punkt końcowy punktu kontrolnego tylko do odczytu (Poproś o weryfikację)
4. Punkt końcowy punktu kontrolnego tylko do odczytu → Witness / klucz kolektora przypięty / klucz własny B (Podpisana odpowiedź)
5. Witness / klucz kolektora przypięty / klucz własny B → Kanał zawierający podpisane posty TGW1 (API bota / własny token)

Narzędzie Witness rejestruje cofnięcia zmian, odmienne nagłówki przy tej samej liczbie, zmienione klucze, nieprawidłowe odpowiedzi oraz brakujące odpowiedzi. Sama wyższa liczba nie oznacza, że wszystkie wcześniejsze zapisy pozostały niezmienione; proszę porównać eksport z zachowanymi punktami kontrolnymi. Umieszczenie narzędzia Witness na innym serwerze pozwala uniknąć skutków awarii serwera kolektora; oddzielny operator zapewnia dodatkową niezależność.

Świadek potwierdza zgłoszony przez zbierającego stan dziennika. Należy skorzystać z testu kontrolowanej dostawy, aby sprawdzić, które działania w Telegramie dotarły do konta zbierającego. Zobacz [konfigurację świadka](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/).

## Testowanie działania w oparciu o znane scenariusze

Należy wykorzystać grupę kontrolną, odrębne konta do gromadzenia danych oraz nowy znacznik. Proszę celowo wysyłać, edytować i usuwać wiadomości, sprawdzając poprawność przechwytywania na poszczególnych etapach. Przed analizą wyników należy zdefiniować oczekiwane działania oraz punkt graniczny.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Liczą się wyłącznie działania zgodne z oczekiwaniami; zduplikowane potwierdzenia nie zwiększają licznika. Mianownik musi być niezerowy. Brakujące potwierdzenie nie ma zmierzonego opóźnienia. Należy odnotować niepewność pomiaru czasu; należy stosować własny, kontrolowany czas działania związanego z usunięciem, ponieważ Telegram nie podaje dokładnego czasu usunięcia. Wynik taki jak 5/6 (83,3%) opisuje działania testowe, a nie kompletność całego ruchu w Telegramie.

## Proszę wybrać schemat działania

[Pełny opis przebiegu dochodzenia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/) obejmuje incydent występujący na kanale, w grupie, w botcie oraz w prywatnym czacie:

1. Na dedykowanym koncie do gromadzenia danych włącz tryb dochodzeniowy dla całego konta i zrób spis dostępnych czatów. Użyj wybranych czatów lub folderu dla konta głównego.
2. Pobieraj zrzuty ekranu dziennika, pełną historię poszczególnych czatów oraz zachowane załączniki.
3. Należy zachować zmiany wprowadzane na bieżąco oraz wszelkie celowe interakcje z panelami wraz z ich potwierdzeniami.
4. Proszę śledzić numeryczne identyfikatory nadawców, relacje odpowiedzi, powtarzające się adresy docelowe oraz skróty plików w oparciu o cytowane zapisy i profile użytkowników.
5. Należy dodawać notatki powiązane ze źródłami oraz zbiory w Case Board. Należy odtworzyć oś czasu obejmującą różne czaty z uwzględnieniem zarówno znaczników czasu, jak i wyraźnych luk.
6. Porównuj obszary robocze innych kont, zachowując jednocześnie odrębność ich pochodzenia i kluczy.
7. Prosimy o zestawienie i weryfikację podpisanych dzienników, profili oraz eksportów historii wraz z notatkami dotyczącymi spraw.

Przewodnik na stronie internetowej w sekcji `/docs/cases/` zawiera interaktywną mapę sprawy oraz warianty dotyczące sporów z botami, usuniętych wiadomości i zmian nazw użytkowników. Case Board przechowuje notatki i zbiory danych w obrębie obszaru roboczego. Eksporty grupowe gromadzą oddzielne pakiety z obszarów roboczych; korelacja między obszarami roboczymi oraz połączona oś czasu pozostają zadaniem analityków.

[Zakończona walidacja i pozostałe zadania](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/) · [Eksportowanie i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#investigation-handoff) · [Zacznij od jednego konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/)
