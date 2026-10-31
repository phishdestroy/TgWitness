# Zobacz, jak działa system gromadzenia dowodów

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/concepts/

Treść wiadomości może ulec zmianie. Zapis tego, co Pan/Pani zaobserwował(a), powinien pozostać możliwy do zweryfikowania.

Zapoznaj się z dwoma niewielkimi eksperymentami poniżej. Wykorzystują one fikcyjne wiadomości, działają w Państwa przeglądarce i nigdy nie łączą się z serwisem Telegram.

## Jedna wiadomość, trzy spostrzeżenia

Gdy Telegram dostarcza nową wiadomość, powiadomienie o edycji lub usunięciu, aplikacja gromadząca dane dodaje trzy odrębne zapisy. Edycja nie zastępuje pierwszego zapisu. Powiadomienie o usunięciu nie powoduje jego skasowania.

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

Powiadomienie o usunięciu nie podaje ani wiarygodnego czasu usunięcia, ani osoby, która usunęła wiadomość. Nieujawnianie tych informacji pozwala zachować rozróżnienie między obserwacją a domysłem.

## Zmień wpis. Śledź skrót.

Każdy wpis zawiera skrót poprzedniego wpisu. Jego własny skrót obejmuje pola zdarzenia, w tym ten link. Zewnętrzny punkt kontrolny określa konkretną długość dziennika oraz skrót początkowy.

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

**C** serializuje dziewięć pól zdarzenia w formacie JSON UTF-8: posortowane klucze, bez dodatkowych spacji, bez sekwencji escape dla znaków ASCII oraz bez wartości NaN/nieskończoności. Wartość `previous_hash` zdarzenia wynosi hi−1. Wyświetlana wartość h0 oznacza 64 znaki zerowe; podpisy obejmują 32 bajty surowego skrótu.

Dziewięć pól to: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` oraz `previous_hash`. Jest to [udokumentowany format kodowania JSON](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#event-canonicalization) stosowany przez TgWitness; same skróty i podpisy nie stanowią pól przeznaczonych na dane wejściowe do funkcji skrótu.

ZACHOWANY PUNKT KONTROLNY

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Proszę zweryfikować podpis punktu kontrolnego pod przypiętym kluczem kolektora, a następnie porównać jego granice z zweryfikowanym dziennikiem. Późniejszy eksport może zawierać więcej rekordów; musi on jednak nadal być zgodny z wcześniejszym punktem kontrolnym.

## Trzy pytania, trzy różne weryfikacje

[01 / INTEGRALNOŚĆ**Czy ten zapis uległ zmianie?** Należy zweryfikować skróty i podpisy przy użyciu oddzielnego, zaufanego klucza.](https://phishdestroy.github.io/TgWitness/pl/docs/exports/)[02 / CIĄGŁOŚĆ**Co zostało zachowane wcześniej?** Proszę porównać podpisany eksport z punktami kontrolnymi przechowywanymi przez odrębnego świadka.](https://phishdestroy.github.io/TgWitness/pl/docs/witness/)[03 / REALIZACJA**Czy te zdarzenia testowe dotarły?** Należy porównać kontrolowane działania związane z wysyłaniem, edycją i usuwaniem wiadomości z dziennikiem każdego konta.](https://phishdestroy.github.io/TgWitness/pl/docs/cases/)

Zgodny łańcuch skrótów stanowi odpowiedź na pytanie dotyczące integralności. Nie potwierdza on jednak pełnego dostarczenia wiadomości w Telegramie, prawdziwości treści ani niezależnie potwierdzonego czasu obserwacji.

Proszę śledzić przebieg [całego postępowania wyjaśniającego,](https://phishdestroy.github.io/TgWitness/pl/docs/cases/) od momentu pozyskania danych aż po przygotowanie akt sprawy.
