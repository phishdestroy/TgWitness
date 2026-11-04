# Zobacz, jak działa system gromadzenia dowodów

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/concepts/

Wiadomości się zmieniają. Twój zapis tego, co widziałeś, nie powinien, i każdy powinien móc to sprawdzić.

Poniżej dwa małe eksperymenty. Fikcyjne wiadomości, wszystko działa w przeglądarce, nic nie trafia do Telegrama.

## Od eksportu czatu do weryfikowalnego zapisu

[Eksport Telegram Desktop](https://telegram.org/blog/export-and-more) zapisuje widoczną teraz historię jako HTML lub JSON. TgWitness dodaje ciągły dziennik zmian, podpisy na każdym wpisie i punkty kontrolne, z którymi inni mogą porównać.

| Zadanie | Eksport z aplikacji Telegram Desktop | TgWitness |
| --- | --- | --- |
| Przeglądaj zapisane rozmowy | HTML lub JSON z wybranymi plikami multimedialnymi | Zapisane rozmowy, dziennik z funkcją wyszukiwania oraz raporty dostępne w trybie offline |
| Śledź zmiany w czasie | Historia dostępna po wyeksportowaniu | Stare wersje, późniejsze edycje i usunięcia — wszystko zachowane |
| Sprawdź pliki po przekazaniu | Standardowe pliki eksportowe w formacie HTML/JSON nie są podpisane | Podpisany manifest, podpisane wpisy i zapieczętowane raporty, sprawdzane zaufanym kluczem |
| Porównaj z wcześniejszym stanem archiwalnym | Należy zachować oddzielną kopię referencyjną lub skrót | Podpisane punkty kontrolne, oddzielny świadek oraz opcjonalne zewnętrzne znaczniki czasu |

Porównanie opiera się na [kodzie eksportu Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) według stanu na 2 listopada 2026.

## Jedna wiadomość, trzy spostrzeżenia

Nowa wiadomość, edycja i usunięcie stają się trzema osobnymi wpisami. Edycja nie nadpisuje pierwszego, a usunięcie go nie kasuje.

01 / PRZEBIEG WIADOMOŚCIPrzykładowa sekwencja

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Collector · Rejestr · aktualizacja → · dodaj →

AKTUALNY WIDOK CZATU Wiadomość nr 42

Wiadomość usunięta

Wiadomość zniknęła z widoku czatu.

DZIENNIK OBSERWACJI 3 wpisy

1. 01

   `message.new`

   Spotkanie o godz. 10:00

   ✓
2. 02

   `message.edited`

   Spotkanie o godz. 11:00

   ✓
3. 03

   `message.deleted`

   Powiadomienie o usunięciu nr 42

   ✓

Wszystkie trzy odnotowane zdarzenia pozostają w dzienniku.

Uproszczona ścieżka dostępu dla jednego, już wybranego źródła. Zapisy operacyjne również odzwierciedlają rzeczywisty dziennik. Zakres rejestracji zależy od tego, co widzi dane konto oraz od tego, co udostępnia Telegram.

Telegram nie mówi, kto usunął wiadomość ani kiedy dokładnie. TgWitness zostawia te pola puste zamiast zgadywać.

## Zmień wpis. Śledź skrót.

Każdy wpis zawiera skrót poprzedniego. Punkt kontrolny przechowywany gdzie indziej utrwala długość dziennika i ostatni skrót.

02 / HASH-CHAIN SANDBOXPrawdziwy algorytm SHA-256 · przykładowe zapisy

ZAPIS 01**Otrzymano wiadomość**`h₁ = SHA-256(e₁)`Linki do 64 zer

REKORD 02**Spotkanie o godz. 11:00**`h₂ = SHA-256(e₂)`Zawiera nagłówek h₁

REKORD 03**Zaobserwowano usunięcie**`h₃ = SHA-256(e₃)`Zawiera h₂

PRZECHOWYWANE W INNYM MIEJSCU**3 wpisy · nagłówek `h₃`**Proszę porównać tę ustaloną granicę z dostarczonym dziennikiem.

Zmiana zdarzenia powoduje zmianę jego skrótu. Odtworzenie łańcucha powoduje zmianę jego początku. Usunięcie końca sprawia, że staje się on krótszy niż zachowany punkt kontrolny.

**Proszę sprawdzić wpis nr 2 oraz pełne skróty**

Oto dokładny kod JSON w formacie UTF-8 z hashowaniem, przedstawiony w tym przykładzie. Wartości są fikcyjne; dziewięć pól oraz sposób serializacji odpowiadają formatowi dziennika.

```

```

Skrót zapisanego rekordu nr 2

``

Przeliczony skrót rekordu nr 2

``

To środowisko testowe oblicza skróty, a nie podpisy. Prawdziwy weryfikator sprawdza również podpis Ed25519, sekwencję i link każdego zdarzenia. Samo odtworzenie skrótów nie pozwala na utworzenie ważnych podpisów przy użyciu zaufanego klucza.

## Rzeczywiste zasady w kilku zdaniach

HASH + PODPIS

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** to dziewięć pól zdarzenia jako JSON UTF-8: posortowane klucze, bez zbędnych spacji, bez escapowania ASCII, bez NaN/nieskończoności. `previous_hash` to hi−1, h0 to 64 zera, a podpisy obejmują 32 surowe bajty skrótu.

Pola: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Pełna specyfikacja: [kodowanie zdarzeń](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#event-canonicalization).

ZACHOWANY PUNKT KONTROLNY

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Sprawdź podpis punktu kontrolnego przypiętym kluczem, potem porównaj go z dziennikiem. Późniejszy eksport może być dłuższy, ale w punkcie kontrolnym musi się zgadzać.

## Trzy pytania, trzy różne weryfikacje

[01 / INTEGRALNOŚĆ**Czy ten zapis uległ zmianie?** Skróty i podpisy wobec klucza, któremu ufasz.](https://phishdestroy.github.io/TgWitness/pl/docs/exports/)[02 / CIĄGŁOŚĆ**Co zostało zachowane wcześniej?** Porównaj eksport z punktami kontrolnymi zachowanymi przez świadka.](https://phishdestroy.github.io/TgWitness/pl/docs/witness/)[03 / REALIZACJA**Czy te zdarzenia testowe dotarły?** Wyślij, zedytuj i usuń wiadomości testowe i zobacz, co złapało każde konto.](https://phishdestroy.github.io/TgWitness/pl/docs/cases/)

Podpisy odpowiadają na pytanie „czy zmieniano”, punkty kontrolne — „czy zgadza się z tym, co było wcześniej”, wiadomości testowe — „czy złapaliśmy wszystko”. [Co weryfikacja dowodzi, a czego nie.](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope)

Dalej: [dochodzenie na całym koncie](https://phishdestroy.github.io/TgWitness/pl/docs/cases/) od początku do paczki ze sprawą.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
