# Jeden dziennik. Cztery tryby gromadzenia danych. Osiem poziomów weryfikacji.

Canonical page: https://phishdestroy.github.io/TgWitness/pl/guides/modes.html

Tryby, scenariusze i poziomy dowodów

TgWitness Rejestruje to, co obserwuje podłączone konto. Strona trzecia może zweryfikować integralność zapisu w oparciu o niezależny, zaufany klucz.

[Tryby gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#scope)[Scenariusze](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#scenarios)[Poziomy dowodów](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#levels)

3–5-minutowy przegląd · fikcyjne przykłady · aktualna implementacja

1. **Telegram**

   Aktualizacje widoczne na koncie
2. **Kolektor**

   Powiązane rekordy, każdy z nich podpisany
3. **Weryfikator**

   Zaufany klucz + zachowana granica

`h₁ → h₂ → h₃ · Ed25519`Sprawdzana jest integralność. Pochodzenie z Telegrama i prawdziwość wiadomości pozostają odrębnymi kwestiami.

## Proszę wybrać zakres obserwacji

Trzy zakresy i wstępne ustawienie dotyczące dochodzenia. Wyłączenia i włączone typy źródeł nadal mają zastosowanie.

Domyślnie**Wybrane czaty**

Zapisy

Wyłącznie ręcznie wybrane źródła.

Nowe czaty

Nie są dodawane automatycznie.

Proszę wybrać

Znany zbiór kanałów lub grup. Nie określono stałej pojemności czatu.

**Nie wykonuje** Nie wykrywa on innych czatów ani nie uzupełnia wcześniejszej historii.

Folder konta**Folder Telegram**

Zapisy

Uwzględniane są foldery i kategorie, z wyłączeniem wykluczeń oraz zarchiwizowanych czatów, o ile zostały skonfigurowane.

Nowe czaty

Dopasowywanie aktywnych czatów; zmiany w folderach w ciągu godziny.

Proszę wybrać

Analityk prowadzi już folder sprawy. Proszę potwierdzić zebranie danych na dedykowanym koncie.

**Nie wykonuje** Nie uwzględnia ona zmieniających się muted/read warunków folderu.

Proszę potwierdzić zakres**Całe konto**

Zapisy

Czat widoczne na koncie, w tym rozmowy prywatne i boty, w ramach wybranych typów.

Nowe czaty

Zostanie dodane po pojawieniu się pierwszej aktualizacji.

Proszę wybrać

Dedykowane konto obserwacyjne, w tym konto uczestniczące w sprawie.

**Nie wykonuje** Nie dołącza on automatycznie do czatów ani nie omija dostępu do źródła.

Ustawienia domyślne dla całego konta**Tryb dochodzeniowy**

Zapisy

Wszystkie typy źródeł, własne działania, profile źródeł oraz 200 najnowszych widocznych wiadomości z nowo wykrytych źródeł.

Nowe czaty

Nowa rozmowa lub bot otrzymuje profil oraz migawkę historii.

Proszę wybrać

Proszę dołączyć do zespołu lub nawiązać interakcję z botem za pośrednictwem panelu. Proszę przejrzeć i zapisać ustawienia wstępne.

**Nie wykonuje** Nie tworzy ona migawek wszystkich istniejących czatów ani nie obserwuje wywołań zwrotnych uruchamianych w innym kliencie.

Karty te służą do lokalnego porównania, a nie do sterowania kolektorem na żywo. Nie powodują one zmian na koncie.

**Nie wykonuje** Żaden tryb nie odczytuje tajnych czatów, nie rejestruje danych podczas zatrzymania procesu, nie dołącza samodzielnie do źródeł ani nie pobiera wcześniejszej historii wykraczającej poza żądaną snapshot/export.

[Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/)

## Zbieranie przez GitHub Actions (wersja wstępna)

Nowe logowanie do Telegrama, jeden czat, zaszyfrowane archiwum i potwierdzenie pochodzenia GitHub.

[Otwórz asystenta zbierania](https://phishdestroy.github.io/TgWitness/pl/docs/capture/)

## Co jest rejestrowane

Do rejestru trafiają wyłącznie obserwacje dostarczone lub wyraźnie zgłoszone. Nieznane źródło pozostaje nieznane.

 Przełączniki przechwytywania · ilustracja lokalnaNowe wiadomościPoprawkiUsunięciaReakcjeCzłonkostwo

Panel stosuje te przełączniki dla poszczególnych obszarów roboczych. Wyłączenie jednego z nich powoduje zachowanie istniejących zapisów; ponowne włączenie nie odtwarza utraconych zdarzeń.

**Macierz zdarzeń: zgromadzone materiały i pozostałe niewiadome**

| Kategoria | Zapisano | Pozostaje nieznane |
| --- | --- | --- |
| Wiadomość | Tekst, identyfikatory, metadane nadawcy, kontekst odpowiedzi oraz oryginalna kopertka aktualizacji. | Brak podpisu Telegramu weryfikowalnego przez stronę trzecią. |
| Edytuj | Każda zaobserwowana wersja, bez nadpisywania wcześniejszych. | Edycje pośrednie mogą zostać pominięte; nadawca niekoniecznie jest redaktorem. |
| Usunięcie | Powiadomienie wraz z wcześniej zapisanym tekstem, o ile jest dostępny. | Nie podano podmiotu odpowiedzialnego za usunięcie ani dokładnego czasu wykonania działania. |
| Usunięcie bez określenia zakresu | Powiadomienie na poziomie konta; nieznany partner pozostaje wyraźnie wskazany. | Brak domniemanych rozmów. Korelacja wykorzystuje, w miarę możliwości, wcześniej zapisane identyfikatory w zakresie konta. |
| Reakcja | Dostarczone liczniki i widoczne najnowsze tożsamości. | Nie każdy reaktor jest widoczny; pełna lista dostępnych reaktorów wymaga oddzielnych zapytań. |
| Członkostwo | Dostarczone komunikaty serwisowe oraz aktualizacje dotyczące uczestników. | Rola i typ czatu ograniczają widoczność; milczenie nie oznacza nieobecności. |
| Załącznik | Deskryptor wersji oryginalnej, zapisane bajty, SHA-256 oraz wyniki prób. | Zniknięty plik może być niedostępny; nowsza wersja nie zastępuje go. |
| Migawka historii | Obecnie widoczne wiadomości, oznaczone jako obserwacje historii. | Wcześniejsze zmiany i usunięte treści nie są odtwarzane. |
| Własne działania | Wychodzące messages/edits oraz odpowiadające im metadane button_press . | Wywołania zwrotne uruchomione w innym kliencie Telegramu nie są widoczne. |
| Przyciski bota | Metadane dotyczące wywołania zwrotnego, adresu URL, aplikacji internetowej oraz żądania są zachowywane wraz z wiadomością. | Adresy URL oraz phone/location żądania mają postać tekstową i nie są automatycznie otwierane ani wykonywane. |

### Domyślne limity załączników

Zdjęcia

20 MiB

Wideo

100 MiB

Pliki

50 MiB

Animacje

20 MiB

Notatki wideo

50 MiB

Głos

20 MiB

Audio

50 MiB

Naklejki

5 MiB

**Nie wykonuje** Przełącznik nie usuwa osadzonych metadanych ani nie wyłącza rejestrów operacyjnych. Zrzut nie identyfikuje podmiotu, którego Telegram nie podał.

[Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/)

## Należy korzystać z posiadanych uprawnień

Każde konto posiada własną przestrzeń roboczą, dziennik, klucz podpisujący, trasę oraz kolejkę.

### Numer telefonu + kod

Wprowadź 2FA po włączeniu tej funkcji.

### QR kod

Należy skanować z autoryzowanego urządzenia; 2FA może to nadal być wymagane.

### Telethon .session

Proszę zaimportować plik sesji konta.

### Pyrogram .session

Należy zaimportować obsługiwany Pyrogram format sesji.

### TData ZIP

Obsługiwane jest jedno konto w aplikacji Desktop; lokalny kod dostępu, jeśli został ustawiony.

### StringSession tekst

Wklej Telethon StringSession.

### .session + .json

Należy wybrać sesję oraz odpowiadające jej metadane towarzyszące.

### Klucz autoryzacyjny HEX + DC ID

Proszę zaimportować autoryzację konta wraz z identyfikatorem centrum danych.

**API para**

Własna API para jest opcjonalna. W przypadku jej braku TgWitness korzysta z puli par publicznych, w tym par pochodzących z oficjalnej aplikacji Telegram Desktop.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy jest w fazie eksperymentalnej; dostępne są wbudowane publiczne MTProxy . Nieudana trasa proxy nie przechodzi na połączenie bezpośrednie.

Dwa obszary robocze na jednym komputerze nie stanowią dwóch niezależnych świadków.

**Nie wykonuje** Import nie omija procesu autoryzacji w Telegramie, 2FA ani nie obsługuje nieobsługiwanych formatów sesji. Konta nadal współdzielą proces aplikacyjny.

[Formaty kont](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/)

## Działaj z poziomu panelu

Proszę wysłać wiadomość lub odpowiedzieć, nacisnąć aktualny przycisk bota, zapisać podgląd linku, a następnie wyraźnie dołączyć do czatu lub uruchomić bota za pomocą jego parametru startowego.

`interaction.preview``interaction.requested``interaction.result`

Potwierdzenia podglądu, żądania i wyników są podpisane. Przed naciśnięciem przycisku serwer ponownie pobiera wiadomość i odrzuca zmienioną treść wprowadzoną z klawiatury. Zwrócony tekst wywołania zwrotnego oraz adresy URL pozostają w zarejestrowanym kontekście.

**Nie wykonuje** Żadnych aplikacji internetowych, płatności, phone/location udostępniania ani zapytań wbudowanych. Wyświetlenie adresu URL nie powoduje jego otwarcia.

[Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/)

## Odzyskiwanie i ciągłość działania

Luki są ujawniane, a nie ukrywane.

### Wróć do zapisanej pozycji

Po ponownym uruchomieniu aplikacja Telegram wyświetla prośbę o pobranie pominiętych aktualizacji. Ograniczony czas przechowywania danych oraz wygasłe różnice mogą powodować luki w danych.

### Proszę ponownie sprawdzić widoczne wiadomości

Ustawienia domyślne: źródła priorytetowe co 15 minut, pozostałe co 6 godzin. Wyniki obejmują message.recovered oraz message.missing_on_recheck.

### Przeczytaj coverage.json

Do podpisanego eksportu dołączone są okresy obserwacji, luki wraz z uzasadnieniami oraz nieobserwowane identyfikatory. Rekord „brakujący przy ponownej weryfikacji” nie stanowi powiadomienia o usunięciu.

**Nie wykonuje** Późniejsza migawka historii nie usuwa awarii ani nie odtwarza każdej zaginionej wersji. Zapisany kursor nie stanowi bezstratnego potwierdzenia przyjęcia dziennika.

[Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

## Siedem poziomów. Różne pytania.

Każdy mechanizm odpowiada na konkretne pytanie. Usługi zewnętrzne należy konfigurować oddzielnie, a ich kotwice zaufania należy przechowywać poza kolektorem.

1. ### Zapis

   SHA-256 łańcuch + Ed25519 na zdarzenie; pierwszy previous_hash to 64 zera.

   **Kontrole przeprowadzane przez strony trzecie** Kolejność i podpisy pod przypiętym kluczem kolektora.

   **Nie wykonuje** Nie stanowi to dowodu pochodzenia z serwisu Telegram ani kompletności danych.

   **Polecenie weryfikacyjne**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Kontener

   manifest.json zawiera listę skrótów plików; manifest.sig podpisuje go. media.saved powiązuje bajty załącznika z wydarzeniem.

   **Kontrole przeprowadzane przez strony trzecie** Dostarczone pliki są zgodne z podpisanym manifestem oraz potwierdzeniami odbioru multimediów.

   **Nie wykonuje** Nie podpisuje się oddzielnie pobranego CSV, HTML ani zrzutu ekranu.

   **Polecenie weryfikacyjne**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Zachowana granica

   Punkt kontrolny przy uruchomieniu, domyślnie co 5 minut, oraz uporządkowane zakończenie działania. Proszę zachować kopię w innym miejscu.

   **Kontrole przeprowadzane przez strony trzecie** Późniejszy eksport jest zgodny z wcześniej zachowaną długością i nagłówkiem; możliwe jest wykrycie cofnięcia zmian.

   **Nie wykonuje** Nie wykrywa ona zastąpienia zarówno dziennika, jak i wszystkich zachowanych punktów kontrolnych.

   **Polecenie weryfikacyjne**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Czas zewnętrzny

   Tryb dowodowy wysyła punkt kontrolny SHA-256 do RFC 3161 organy (FreeTSA, DigiCert) oraz OpenTimestamps kalendarzy.

   **Kontrole przeprowadzane przez strony trzecie** Zweryfikowana odpowiedź TSA określa datę tych bajtów; potwierdzone OpenTimestamps dowód zakotwicza je w sieci Bitcoin.

   **Nie wykonuje** Nie traktuje ona przygotowanego żądania ani oczekującego potwierdzenia kalendarzowego jako potwierdzonego znacznika czasu.

   **Polecenie weryfikacyjne**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Niezależny świadek

   Oddzielny host, punkt końcowy z ograniczonym dostępem tylko do odczytu, nowe wyzwanie oraz własny key/journal oraz TGW1 wpisów na kanale.

   **Kontrole przeprowadzane przez strony trzecie** Wcześniej zaakceptowane wersje; statusy: ok, key_changed, „rollback”, „fork”, „invalid” oraz no_response.

   **Nie wykonuje** Nie przekształca to dwóch obszarów roboczych na jednym hoście zbierającym w niezależnych świadków.

   **Polecenie weryfikacyjne**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Replika poza serwerem

   S3 Kopia zgodna z [specyfikacją], zaszyfrowana przy użyciu AES-256-GCM; Object Lock , o ile obsługuje to magazyn danych.

   **Kontrole przeprowadzane przez strony trzecie** Funkcja „Restore” publikuje pliki dopiero po pomyślnym zakończeniu weryfikacji dziennika, punktu kontrolnego oraz zachowanych multimediów.

   **Nie wykonuje** Nie przywraca danych bez wyeksportowanego klucza ani nie zakłada ich zachowania bez sprawdzenia odpowiedzi z pamięci.

   **Polecenie weryfikacyjne**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Sprawdź pochodzenie

   Podpisane potwierdzenie wykonania: skróty źródła, wersje zależności oraz kontekst procesu. Zgłoszone samodzielnie.

   **Kontrole przeprowadzane przez strony trzecie** Informacje przekazane przez moduł zbierający podpisy na temat własnego działania.

   **Nie wykonuje** Nie zapewnia to niezależnego poświadczenia procesu ani nie wyklucza naruszenia bezpieczeństwa przed rozpoczęciem rejestracji.

   **Polecenie weryfikacyjne**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Czego żaden poziom nie potwierdza

Dostarczenie każdej aktualizacji serwisu Telegram; prawdziwość treści; fakt, że identyfikator nadawcy identyfikuje rzeczywistą osobę; brak naruszenia bezpieczeństwa urządzenia zbierającego dane przed rozpoczęciem rejestracji; dopuszczalność dowodowa w sądzie.

[Niezależny świadek](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/)

Lokalny SHA-256 eksperyment

### Proszę spróbować zmienić rekord 2

Kolejny rekord zachowuje poprzednio zapisany link. Zmiana tekstu powoduje zmianę obliczonego skrótu rekordu nr 2.

Tekst zapisu nr 2

Zapis 1`h1`Zaczyna się od 64 zer

Zapis 2`h2`Zawiera zapisane h1

Zapis 3`h3`Zawiera zapisane h2

Przykład statyczny: h2 dotyczy wpisu „Spotkanie o godz. 11:00”. Zmiana tego tekstu powoduje zmianę h2; rekord nr 3 nadal odwołuje się do zapisanego h2.

**Proszę sprawdzić pełne skróty**

Hash zapisanego rekordu nr 2

`SHA-256(e₂)`

Ponownie obliczony skrót rekordu nr 2

`SHA-256(e₂)`

Ten przykład oblicza skróty, a nie podpisy. Prawdziwy weryfikator sprawdza każdy podpis i link względem zaufanego klucza.

 [Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/how-it-works/)

## Proszę wybrać ścieżkę analizy dowodów

Sytuacje fikcyjne. Proszę rozpocząć gromadzenie danych przed wystąpieniem danego zdarzenia; proszę zachować granice i luki wraz z treścią.

### Kanał zmienia szczegóły płatności

Tryb → zdarzenia

Wybrane czaty → wiadomości, edycje, usunięcia.

Wynik

Obserwowane wersje postów i załączniki na podstawie skrótów.

Weryfikacja

Podpisano ZIP + zachowany punkt kontrolny + zweryfikowana odpowiedź TSA.

**Nie wykonuje** Nie pozwala ona na odtworzenie oryginału, który nigdy nie został zarejestrowany.

### Wiadomości znikają po wystąpieniu incydentu

Tryb → zdarzenia

Folder lub całe konto → wszystkie kategorie zdarzeń.

Wynik

Zapisane oryginały, powiadomienia o usunięciu oraz zasięg z lukami.

Weryfikacja

Podpisano ZIP + niezależny dziennik świadka.

**Nie wykonuje** Nie pozwala to zidentyfikować osoby usuwającej na podstawie powiadomienia, które nie podaje podmiotu.

### Proszę zbadać bota sklepowego

Tryb → zdarzenia

Ustawienia domyślne trybu badawczego → przyciski, podglądy linków oraz jawne uruchamianie bota.

Wynik

Podpisane potwierdzenia interakcji, zwracane wywołania zwrotne oraz zapisane profile.

Weryfikacja

Po podpisaniu ZIP; należy zweryfikować każdą dokumentację względem ZIP.

**Nie wykonuje** Nie otwiera ona aplikacji internetowej bota, nie dokonuje płatności ani nie rejestruje wywołań zwrotnych innego klienta.

### Uczestnik zmienia nazwy w różnych czatach

Tryb → zdarzenia

Dowolny zakres → obserwowane sender/profile metadane.

Wynik

Historia nazw/nazw użytkowników według identyfikatorów numerycznych, linki „również w” oraz wyodrębnione tropy.

Weryfikacja

Dokumentacja JSON zweryfikowano w odniesieniu do podpisanego ZIP.

**Nie wykonuje** Nie przekształca ona portfela, ciągu znaków przypominającego numer telefonu ani nazwy użytkownika w potwierdzoną tożsamość.

### Długotrwała obserwacja z kopią przechowywaną poza serwerem

Tryb → zdarzenia

Dowolny zakres → tryb dowodowy oraz S3 replika z obsługą Object Lock.

Wynik

Kopia zaszyfrowana, zachowane punkty kontrolne oraz odpowiedzi z sygnaturą czasową.

Weryfikacja

Proszę przywrócić dane za pomocą wyeksportowanego klucza, a następnie zweryfikować je bez korzystania z oryginalnego serwera.

**Nie wykonuje** Nie zastępuje to niezależnego świadka ani oddzielnie przechowywanego klucza deszyfrującego.

[Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/)

## Należy przekazać pakiet umożliwiający weryfikację

Należy dostarczyć podpisany oryginał, niezależnie przechowywany odcisk klucza, odpowiedni punkt kontrolny oraz wynik weryfikacji.

- Podpisano ZIP
- JSONL
- CSV
- HTML
- Punkt kontrolny
- Potwierdzenie wysłania
- Eksport czatu: chat.json / chat.html
- Dokumentacja JSON
- Chronione hasłem AES-256 ZIP
- Oddzielne eksporty dla wielu kont
- Streaming CLI: 5 GiB limit domyślny

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Należy pobrać weryfikator z zaufanej kopii, a nie z archiwum poddawanego kontroli.

**Nie wykonuje** Wersja samodzielna CSV i HTML nie są podpisanymi kontenerami. Hasło chroni poufność transferu, a nie jego autentyczność. Wielokrotne eksporty nie łączą dzienników kont.

[Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

## Proszę porównać dostarczony artefakt

Podstawowe artefakty bez dodatkowych systemów podpisywania, znaczników czasu ani systemów świadków. Skrypty i rejestratory różnią się w zależności od implementacji; termin „częściowy” oznacza ograniczenie do materiału zarejestrowanego lub widocznego.

| Podejście | Zmiany / usunięcia | Rejestracja podpisu | Czas zewnętrzny | Niezależny świadek | Zakres / luki | Weryfikacja bez autora |
| --- | --- | --- | --- | --- | --- | --- |
| Eksport z aplikacji Telegram Desktop | Częściowe | Nie | Nie | Nie | Nie | Nie |
| Telethon skrypt tworzenia migawki | Częściowe | Nie | Nie | Nie | Nie | Nie |
| Rejestrator usunięć: dziennik tekstowy | Częściowe | Nie | Nie | Nie | Nie | Nie |
| Zrzuty ekranu / przechwytywanie stron internetowych | Częściowe | Nie | Nie | Nie | Nie | Nie |
| TgWitness z skonfigurowanymi dodatkami | Częściowe | Tak | Tak | Tak | Częściowe | Tak |

**Nie wykonuje** Tabela nie zawiera oceny każdego skryptu ani produktu do rejestrowania danych. Opcjonalne kontrole czasu i świadków wymagają własnych usług i punktów odniesienia zaufania; żadna z nich nie ustala prawdy źródłowej.

[Zapoznaj się ze szczegółami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

## Proszę zachować ograniczenia wraz z dowodami

Weryfikacja jest przydatna, gdy jej zakres pozostaje jednoznaczny.

- Ciche czaty są niedostępne.
- Podczas zatrzymania procesu nic nie jest rejestrowane; możliwości odzyskiwania danych są ograniczone.
- Zweryfikowany zapis nie stanowi dowodu na prawdziwość jego treści.
- Operator posiadający klucz może podpisać dowolną treść. Niezależni świadkowie i sygnatury czasowe ograniczają możliwość późniejszej zamiany danych, a nie nieuczciwego przechwycenia danych na początku.
- Proszę korzystać z dedykowanego konta, a nie z konta głównego.
- Telegram może ograniczyć dostęp do kont ze względu na liczbę wysyłanych żądań.

**Nie wykonuje** Żaden tryb ani poziom dowodowy nie gwarantuje dopuszczalności prawnej, pełnego dostarczenia wiadomości w Telegramie ani tożsamości w świecie rzeczywistym.

[Instrukcja konfiguracji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl)[Konto dedykowane](https://phishdestroy.github.io/TgWitness/pl/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/)
