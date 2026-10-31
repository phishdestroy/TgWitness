# Wiadomości ulegają zmianom. Zachowaj to, co widział Pan/Pani.

Canonical page: https://phishdestroy.github.io/TgWitness/pl/

[Oprogramowanie typu open source / v0.7.0](https://phishdestroy.github.io/TgWitness/pl/docs/reference/changelog/)

Przechwytuj wiadomości z Telegrama, zachowuj wprowadzone w nich zmiany i eksportuj podpisany zapis.

[Otwórz wersję demonstracyjną](https://phishdestroy.github.io/TgWitness/demo/?lang=pl)[Instrukcja konfiguracji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl)

W wersji demonstracyjnej wykorzystano dane fikcyjne. Nie jest wymagane logowanie do serwisu Telegram.

 [Zbieranie przez GitHub Actions (wersja wstępna)](https://phishdestroy.github.io/TgWitness/pl/docs/capture/) [Kopia zapasowa poza lokalizacją w usłudze S3: konfiguracja i odzyskiwanie](https://phishdestroy.github.io/TgWitness/pl/#s3)

WIADOMOŚĆ PRZEZ CZAS #0042

Northstar · BadaniaFikcyjne źródło / wiadomość nr 42

1. **Zaobserwowana wiadomość:**09:41:02

   Prezentacja rozpoczyna się od 14:00.
2. **Zachowano edycję**09:43:18

   Prezentacja rozpoczyna się od 15:00.

   Zachowano poprzednią wersję
3. **Powiadomienie o usunięciu**10:06:45

   Zarejestrowane treści pozostają w Państwa dzienniku.

Trzy obserwacje. Jedna historia. PRZYKŁAD

Wiadomość znika. Zachowana historia pozostaje.

## Każda zarejestrowana zmiana. Dokładnie tam, gdzie jest potrzebna.

Zapoznaj się z interfejsem, korzystając z fikcyjnych danych demonstracyjnych.

TgWitness / Zapisane rozmowyPANIE I PANI PRZESTRZEŃ ROBOCZA DO OBSERWACJI

![Zapisane rozmowy z Telegrama w ciemnym motywie, wraz z zarejestrowanymi zmianami i usuniętymi wiadomościami zachowanymi w kontekście](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Zapisane rozmowy – znany widok rozmowy, z zarejestrowanymi zmianami i powiadomieniami o usunięciu wyświetlanymi obok wiadomości.

TgWitness / DziennikLOKALNE ŚRODOWISKO PRACY

![Rejestr zawierający zaobserwowane wiadomości, zmiany, powiadomienia o usunięciu oraz zdarzenia objęte monitorowaniem](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Dziennik – Przeglądalna oś czasu zawierająca wszystkie zdarzenia zaobserwowane na Państwa koncie, w tym przerwy w działaniu.

TgWitness / Historia zmianLOKALNE ŚRODOWISKO PRACY

![Okienko szczegółów porównujące przechwyconą poprzednią wersję wiadomości z jej edytowaną wersją](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Historia zmian Porównaj zarejestrowane wersje bez nadpisywania wcześniejszych zapisów.

TgWitness / Podpisane eksportyLOKALNE ŚRODOWISKO PRACY

![Funkcja eksportu obszaru roboczego umożliwiająca uzyskanie podpisanego pliku ZIP, JSONL, CSV oraz raportu HTML w trybie offline](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Podpisane eksporty – proszę zabrać dziennik ze sobą, wraz z manifestem i niezależnym weryfikatorem.

01 / PRZECHWYTYWANIE

### To Państwo wybierają zakres.

Wybrane rozmowy, folder w aplikacji Telegram lub całe konto. Osobna przestrzeń robocza dla każdego konta.

[Porównaj tryby gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#scope)

02 / ZACHOWANIE

### Zmiany wzbogacają treść.

W dzienniku zachowywane są zarchiwizowane wersje, powiadomienia o usunięciu oraz luki w obserwacji.

[Zobacz matrycę zdarzeń](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#events)

03 / PRZEKAZANIE

### Rejestr, który podróżuje.

Podpisany plik ZIP, zachowane pliki oraz raport dostępny w trybie offline. Opcjonalna ochrona hasłem.

[Eksportuj i zweryfikuj](https://phishdestroy.github.io/TgWitness/pl/docs/exports/)

## Wystarczy zmienić jeden bajt. Łańcuch to wskaże.

Każde zdarzenie zawiera odnośnik do poprzedniego skrótu oraz podpis Ed25519.

![Zarejestrowane zdarzenia zawierają odnośniki do poprzednich skrótów, są opatrzone podpisami i przekazywane w formie weryfikowalnego pliku eksportowego.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Zmiana zarejestrowanego wpisu powoduje zmianę jego skrótu i uniemożliwia weryfikację powiązanego wpisu.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Oddzielnie przechowywany punkt kontrolny umożliwia odbiorcy porównanie wyeksportowanego dziennika z wcześniejszymi obserwacjami.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Proszę zapoznać się z tym, co zapewnia każdy mechanizm weryfikacji oraz gdzie leżą jego ograniczenia.

[Zapoznaj się z ośmioma poziomami dowodów](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#levels)

## Proszę o dodatkową weryfikację.

Przekażcie Państwo spostrzeżenia, pliki oraz raport HTML w trybie offline w jednym podpisanym pakiecie.

[Zapoznaj się z modelem dowodowym](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

tgwitness-evidence.zipPAKIET Z PODPISEM

- 01

  Oryginalne spostrzeżeniaPliki JSONL + tabela CSV
- 02

  Przejrzysty kontekstRaport HTML w trybie offline + zachowane pliki multimedialne
- 03

  Niezależna weryfikacjaPodpisany manifest + samodzielny weryfikator

Podpisy wykrywają manipulacje w odniesieniu do zaufanego klucza. Nie potwierdzają one pochodzenia z serwisu Telegram ani nie gwarantują kompletnego przechwycenia danych. Treść dziennika oraz pliki multimedialne wymagają szyfrowanego miejsca przechowywania zapewnionego przez Państwa.

## Kopie w usłudze S3. Kontrole zewnętrzne.

Należy przechowywać zaszyfrowane kopie i wprowadzać niezależne mechanizmy weryfikacyjne.

Domyślnie wyłączone

### Skopiuj wszystko do pamięci masowej zgodnej ze standardem S3

Dziennik, pliki, punkty kontrolne z sygnaturą czasową oraz eksporty czatów — szyfrowane przed przesłaniem do AWS S3 lub kompatybilnej pamięci masowej.

**Ustawienia przechowywania danych i odzyskiwanie**

Szyfrowanie po stronie klienta

`AES-256-GCM` szyfruje obiekty na tym komputerze. Dostawca otrzymuje zaszyfrowane obiekty.

Kopie tworzone automatycznie lub ręcznie

Proszę skopiować teraz lub wybrać przedział czasowy od 1 do 1 440 minut. Postęp można sprawdzić w panelu.

Object Lock

Proszę wybrać liczbę dni przechowywania oraz tryb działania, o ile obsługuje to magazyn danych. Panel informuje, czy potwierdzono przechowywanie przesłanego obiektu.

Zweryfikowane odzyskiwanie danych

Proszę pobrać klucz szyfrujący i przechowywać go oddzielnie. Proszę przywrócić dane na innym komputerze; pliki zostaną opublikowane dopiero po weryfikacji.

![Pełny panel ustawień kopii poza lokalizacją: punkt końcowy, region, zasób, klucze dostępu, harmonogram, blokada obiektów oraz opcje związane z kluczem odtwarzania](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Pełny panel z rozwijanymi opcjami zaawansowanymi. Nie są wyświetlane żadne dane uwierzytelniające dotyczące pamięci masowej.

Dziennik i media`AES-256-GCM`Pamięć masowa zgodna ze standardem S3

[Skonfiguruj S3 i przywróć kopię](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3)[Zapoznaj się ze szczegółami weryfikacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Nie umożliwia** przywracania danych bez wyeksportowanego klucza deszyfrującego ani nie zastępuje niezależnego świadka.

### Powiadomienia · Apprise

Powiadomienia o problemach, zmiany w czatach oraz codzienne podsumowania za pośrednictwem Apprise: komunikatory, poczta elektroniczna lub Państwa własny webhook JSON.

**Nie** wysyła treści wiadomości, chyba że włączą Państwo opcję wyświetlania fragmentów.

 [Konfiguracja miejsc docelowych powiadomień](https://phishdestroy.github.io/TgWitness/pl/docs/reference/operations/#notifications)

### Zewnętrzne znaczniki czasu

Skróty punktów kontrolnych z sygnaturą czasową zgodne z RFC 3161 i OpenTimestamps.

Nie traktuje oczekującego potwierdzenia w kalendarzu jako potwierdzonego znacznika czasu Bitcoin.

 [Proszę sprawdzić dowody z sygnaturami czasowymi:](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/)

### Niezależny świadek

Oddzielny serwer przechowuje podpisane obserwacje i może publikować punkty kontrolne `TGW1`.

**Nie powoduje** to, że dwa obszary robocze na jednym hoście kolektora stają się niezależnymi świadkami.

 [Skonfiguruj Witness](https://phishdestroy.github.io/TgWitness/pl/docs/witness/)

### Odtworzenie danych i widoczne luki

Wznowienie po ponownym uruchomieniu. Funkcje ponownej weryfikacji oraz `coverage.json` pokazują odzyskane wiadomości i luki w danych.

**Nie** odtwarza każdej pominiętej edycji ani znikniętej wiadomości.

 [Proszę sprawdzić ciągłość i ewentualne luki](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#continuity)

## Państwa pierwsze środowisko pracy zaczyna się właśnie tutaj.

Najpierw zapoznaj się z wersją demonstracyjną. Gdy będą Państwo gotowi, proszę podłączyć dedykowane konto. Systemy Windows, Linux, macOS lub Docker.

[Zapoznaj się z instrukcją konfiguracji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl)

**Jedna zaimportowana sesja, jeden uruchomiony klient.**

Nie należy uruchamiać zaimportowanego klucza TData/session jednocześnie w aplikacji Telegram Desktop i TgWitness. Telegram może unieważnić wspólną autoryzację (AUTH_KEY_DUPLICATED). W celu równoległego korzystania z obu aplikacji należy utworzyć oddzielne konto w TgWitness za pomocą numeru telefonu lub kodu QR.

[Proszę zapoznać się z ostrzeżeniem dotyczącym importowania sesji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl#session-warning)

**Proszę zapoznać się z nią przed nawiązaniem połączenia.**

Wypróbuj fikcyjne środowisko pracy bez konta w Telegramie.

[Otwórz wersję demonstracyjną online →](https://phishdestroy.github.io/TgWitness/demo/?lang=pl)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Polecenia dotyczące instalacji lokalnej**

KROK 01

### Pobierz kod źródłowy.

[Proszę pobrać plik ZIP ze źródłami](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) i rozpakować go lub sklonować repozytorium:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Uruchomienie aplikacji wymaga środowiska Python 3.11 lub nowszego. Program uruchamiający dla systemu Windows oferuje instalację, jeśli brakuje środowiska Python.

[Przeglądaj wersje](https://github.com/phishdestroy/TgWitness/releases)

Nie ma Pythona w systemie Windows? [Proszę pobrać pakiet przenośny](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), rozpakować go i kliknąć dwukrotnie plik „`TgWitness.cmd`”.

KROK 02

### Wybierz sposób uruchomienia.

Proszę dwukrotnie kliknąć plik `Start.cmd` lub uruchomić go w PowerShell:

```
.\Start.cmd
```

Chce Pan/Pani tylko zapoznać się z serwisem? Proszę dwukrotnie kliknąć `scripts\Demo.cmd`, aby uruchomić izolowaną wersję demonstracyjną. Nie jest wymagane logowanie do serwisu Telegram.

W przypadku dostępności języka Python 3.11+ oraz biblioteki `venv`:

```
sh start.sh
```

Aby zamiast tego otworzyć fikcyjny dziennik, proszę uruchomić polecenie `sh start.sh --demo`.

Przy uruchomionym Dockerze i zainstalowanym Compose w wersji 2.20 lub nowszej:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Drugie polecenie wyświetla token Państwa prywatnego panelu. Proszę zachować go na swoim komputerze.

Po uruchomieniu proszę otworzyć adres [127.0.0.1:8787](http://127.0.0.1:8787).

W przypadku instalacji ze źródeł token znajduje się w `data/live/panel-token.txt`. Do logowania w Telegramie można użyć wbudowanych ustawień API lub własnej pary kluczy z [my.telegram.org](https://my.telegram.org). [Pełny przewodnik konfiguracji ↗](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/)

**TgWitness 0.7.0** [Co nowego →](https://phishdestroy.github.io/TgWitness/pl/docs/reference/changelog/) · [Funkcje i znane ograniczenia →](https://phishdestroy.github.io/TgWitness/pl/docs/reference/features/)

## Jasne instrukcje. Przydatne wskazówki dotyczące dalszych działań.

[Zapoznaj się z przewodnikami ↗](https://phishdestroy.github.io/TgWitness/pl/docs/)

[### Tryby działania, scenariusze i poziomy wiarygodności dowodów Cztery tryby gromadzenia danych. Osiem poziomów weryfikacji. Znajdź schemat postępowania dostosowany do Państwa sprawy.](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html)

[01 ### Podłącz konto Obsługa importu danych z telefonów, kodów QR oraz obsługiwanych sesji.](https://phishdestroy.github.io/TgWitness/pl/docs/accounts/)[02 ### Proszę wybrać serwer proxy Publiczne listy serwerów MTProxy lub Państwa własna trasa.](https://phishdestroy.github.io/TgWitness/pl/docs/proxies/)[03 ### Skonfiguruj bota Witness Podpisane punkty kontrolne na Państwa kanale w Telegramie.](https://phishdestroy.github.io/TgWitness/pl/docs/witness/)[04 ### Eksportowanie i weryfikacja Udostępnij zarchiwizowaną historię i sprawdź jej integralność.](https://phishdestroy.github.io/TgWitness/pl/docs/exports/)

## Przeglądaj archiwum.

Wczytuj historię, przeglądaj źródła AI, podłącz klienta MCP, rozpoznawaj zapisane multimedia i wysyłaj podpisane webhooki.

Dostępne z aktualnego źródła. Przenośna wersja zapoznawcza 0.7.0 powstała przed wprowadzeniem tych narzędzi.

[Zapoznaj się z przebiegiem pracy](https://phishdestroy.github.io/TgWitness/pl/docs/archive/)

## Zanim zaczną Państwo.

**Czy ta strona jest powiązana z serwisem Telegram?**

Nie. Jest to statyczna strona projektu zawierająca fikcyjne przykłady i zrzuty ekranu. Rzeczywista aplikacja działa na Państwa komputerze lub serwerze; logowanie odbywa się właśnie tam.

**Czy narzędzie to pozwala odzyskać wiadomości usunięte przed ich przechwyceniem?**

Nie. TgWitness przechowuje treści, które pojawiły się na Państwa koncie w trakcie trwania procesu gromadzenia danych. Późniejsza migawka historii nie pozwala na odtworzenie pominiętych zmian ani usuniętych wiadomości.

**Czy cały mój dziennik jest zaszyfrowany?**

Dane uwierzytelniające konta oraz klucze podpisujące są przechowywane w zaszyfrowanym sejfie. Lokalne wiadomości i załączniki wymagają zaszyfrowanego dysku lub woluminu. Eksporty mogą opcjonalnie wykorzystywać plik ZIP z szyfrowaniem AES-256 chroniony hasłem.

**Czy serwis ten jest powiązany z Telegramem?**

Nie. TgWitness jest niezależnym projektem wykorzystującym oprogramowanie Telethon, rozpowszechnianym na licencji MIT. Użytkownik autoryzuje własne konta, korzystając z wbudowanych ustawień API lub własnej pary kluczy API.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Najpierw zapoznaj się z informacjami. Skonfiguruj narzędzie, gdy będzie Pan/Pani gotowy/gotowa.

[Otwórz wersję demonstracyjną](https://phishdestroy.github.io/TgWitness/demo/?lang=pl)[Instrukcja konfiguracji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl)
