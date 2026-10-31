# Format dowodów

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/

Zawartość podpisanego pliku ZIP, rodzaje zapisów, potwierdzenia przetwarzania, profile użytkowników, kopie zewnętrzne oraz weryfikacja w trybie offline.

Obserwacja nie jest wnioskiem. Identyfikator nadawcy nie jest tożsamą z tożsamością w świecie rzeczywistym. Źródłem informacji jest aktualizacja usługi widoczna na koncie; Telegram nie podpisuje kryptograficznie tych zapisanych danych na potrzeby zewnętrznego śledczego.

## Co jest podpisane

| Materiały | Ochrona | Co należy zachować |
| --- | --- | --- |
| Każdy wpis w dzienniku, w tym zdarzenia operacyjne | Łańcuch SHA-256 oraz podpis Ed25519 dla każdego zdarzenia | Oryginalny `events.jsonl`, odcisk klucza zaufanego oraz zachowany punkt kontrolny |
| Zawartość pliku ZIP z dowodami | `manifest.sig` podpisuje manifest kanoniczny, zawierający listę skrótów plików treści | Kompletny plik ZIP, zawierający manifest oraz podpis |
| Zachowane załączniki | SHA-256 i liczba bajtów w podpisanym zdarzeniu typu „`media.saved`”; skrót pliku w podpisanym manifeście ZIP | Oryginalne dane w zweryfikowanym pliku ZIP |
| Checkpoint | Podpis Ed25519 obejmujący długość dziennika, skrót nagłówka, klucz publiczny oraz czas utworzenia | Niezależna kopia zachowana przed wprowadzeniem spornej zmiany |
| Potwierdzenie wykonania | Oddzielnie podpisane pomiary kolektora; zawarte również w podpisanym zdarzeniu `process.started` | Potwierdzenie odbioru i powiązany dziennik; pomiary opierają się na danych podanych przez użytkowników |
| Samodzielny plik CSV lub HTML | Brak samodzielnego podpisu kryptograficznego; same skróty zdarzeń są niewystarczające | W celu sprawdzenia integralności prosimy o użycie dokładnie tej samej kopii, która znajduje się w zweryfikowanym pliku ZIP. |
| Zrzuty ekranu, wydruki lub pliki PDF wygenerowane przez przeglądarkę | Brak podpisu TgWitness na materiale pochodnym | Należy zachować oryginalny, zweryfikowany pakiet oraz udokumentować sposób powstania jego pochodnej wersji |

Narzędzie do gromadzenia danych weryfikuje podpisy dziennika przed wygenerowaniem każdego formatu eksportu. Ta weryfikacja źródła nie powoduje utworzenia podpisu w oddzielnie pobranym pliku CSV lub HTML. Prawidłowy podpis zdarzenia w formacie JSONL również nie zawiera bajtów załącznika ani nie potwierdza niezależnie, że dostarczono cały zaobserwowany dziennik.

## Przekazanie sprawy do dalszego dochodzenia

1. Proszę odnotować w notatkach dotyczących sprawy numer referencyjny, operatora, numeryczny identyfikator konta w Telegramie, wybrane źródła, zasady gromadzenia danych oraz okres gromadzenia. TgWitness zapisuje obserwacje; przypisanie sprawy oraz dokumentacja przechowywania danych są zarządzane poza aplikacją. Proszę zweryfikować planowaną konfigurację gromadzenia danych w ramach [procedury akceptacji na żywo](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Należy niezależnie zachować odcisk klucza publicznego środowiska pracy przed oparciem się na jego eksportach. Podczas gromadzenia danych należy zapisywać podpisane punkty kontrolne poza kolektorem. Należy rejestrować przerwy w działaniu oraz ograniczenia widoczności konta.
3. Proszę wyeksportować **podpisany** plik **ZIP** i zachować podpisane potwierdzenie wykonania. Proszę użyć punktu kontrolnego na granicy eksportowanego dziennika lub przed nią. Późniejszy punkt kontrolny może prawidłowo odrzucić wcześniejszy eksport jako zbyt krótki. Eksporty obejmują pełny dziennik obszaru roboczego, niezależnie od filtrów panelowych; proszę przejrzeć materiał przed jego udostępnieniem.
4. Proszę poprosić odbiorcę o zweryfikowanie pliku ZIP za pomocą zaufanej kopii programu weryfikującego oraz niezależnie dostarczonego odcisku palca/punktu kontrolnego. Z poziomu zaufanego repozytorium z aktywnym środowiskiem języka Python:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Pomyślny wynik generuje raporty o kodach `key_pinned: true` i `checkpoint_checked: true` , gdy podano i zaakceptowano oba dane wejściowe. Należy zachować wynik weryfikacji.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Proszę odnotować w protokole przechowywania archiwum wartość SHA-256, granice eksportu, datę przekazania, nadawcę oraz odbiorcę. Proszę zachować oryginalny pakiet w nienaruszonym stanie i pracować na kopiach. Proszę udostępniać pliki dowodowe, a nie prywatny katalog danych aplikacji, który zawiera również sesje kont oraz klucze podpisywania. W celu przekazania eksport można umieścić w pliku ZIP zabezpieczonym hasłem przy użyciu algorytmu AES-256. Hasło służy wyłącznie do ochrony poufności i nie jest przechowywane; odbiorca rozpakowuje archiwum i weryfikuje znajdujący się w nim podpisany eksport, który pozostaje niezmieniony.
   2. Jeśli wymagane jest niezależne ustalenie punktu odniesienia czasowego, należy postępować zgodnie z [procedurą określoną w RFC 3161](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/) oraz zachować żądanie, punkt kontrolny, informacje o zaufanym urzędzie certyfikacji oraz zweryfikowaną odpowiedź organu certyfikującego. Samo przygotowanie żądania nie zapewnia uzyskania sygnatury czasowej.

Pomyślna weryfikacja potwierdza integralność w odniesieniu do zaufanego klucza zbierającego oraz zachowanych granic. Autentyczność źródła, pełna dostawa wiadomości w Telegramie, zaufany czas oraz dopuszczalność dowodowa w postępowaniu sądowym wymagają oddzielnych dowodów. Niniejsza wersja nie przeszła jeszcze kwalifikacji w środowisku produkcyjnym Telegramu ani niezależnej oceny kryminalistycznej/bezpieczeństwa.

Skopiowany klucz kolektora może podpisać sfałszowany dziennik zastępczy. Weryfikacja w oparciu o niezależnie przechowywany punkt kontrolny lub zapis świadka pozwala wykryć zmianę wcześniejszego prefiksu; sama weryfikacja podpisu nie jest w stanie tego wykryć. Świadek koryguje dane przedstawione przez moduł zbierający, więc nie potwierdza on samodzielnie prawdziwości zapisów sfałszowanych przed ich pierwszym zewnętrznym punktem kontrolnym. Raporty wdrożenia w chmurze sprawdzają konfigurację oraz pomiary zgłoszone przez moduł zbierający; nie potwierdzają one jednak, że klucz prywatny nie został skopiowany podczas fazy bootstrapu.

Powiadomienia wysyłane za pośrednictwem Apprise zawierają nazwy przestrzeni roboczych i czatów oraz liczbę wiadomości; krótkie fragmenty usuniętych i edytowanych wiadomości są dodawane wyłącznie wtedy, gdy operator włączy tę funkcję (domyślnie jest ona wyłączona). Stanowią one jedynie sygnał ułatwiający pracę, a nie dowód: nie gwarantuje się ich dostarczenia, a jedynie dziennik i jego podpisane eksporty rejestrują to, co zostało zaobserwowane. W przypadku serwera proxy przestrzeni roboczej powiadomienia przechodzą tą samą trasą; usługi, które nie mogą z niej korzystać, oraz trasy MTProxy są odrzucane.

## Kanonizacja zdarzeń

Dane wejściowe skrótu składają się dokładnie z następujących pól:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Serializacja przy użyciu formatu JSON zgodnego z Pythonem w kodowaniu UTF-8, z posortowanymi kluczami obiektów, bez escapingu znaków ASCII, bez zbędnych spacji oraz bez wartości NaN/nieskończoności:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

Suma kontrolna SHA-256 tych bajtów stanowi skrót zdarzenia. Podpis generowany jest algorytmem Ed25519 na podstawie 32 surowych bajtów skrótu, a następnie kodowany w base64. Pierwszy poprzedni skrót (previous_hash) składa się z 64 zer. Numery sekwencyjne zaczynają się od 1 i rosną o 1. Wszystkie zdarzenia, w tym zdarzenia operacyjne, są ujęte w jednym łańcuchu. Nie stosuje się eliminacji zduplikowanych dostarczeń: powtarzające się obserwacje stanowią odrębne potwierdzenia odbioru, a nie twierdzenie o odrębnych działaniach w Telegramie.

Surowe daty z Telegrama są ciągami znaków zgodnymi z normą ISO; pola binarne stają się obiektami zawierającymi bajty w formacie base64. Tekst wiadomości, encje, deskryptory multimediów, metadane odpowiedzi, reakcje oraz działania serwisowe są zachowywane w surowych metadanych wiadomości, o ile zostały dostarczone.

observed_at to czas z zegara systemowego kolektora w strefie czasowej UTC. source_at to podana data z serwisu Telegram, o ile jest dostępna. Powiadomienia o usunięciu nie podają dokładnego czasu usunięcia, dlatego source_at pozostaje wartością null. Kolejność odbioru danych nie musi odpowiadać kolejności zdarzeń źródłowych. W migawkach historii wykorzystywane są starsze daty źródłowe, ale aktualne czasy obserwacji.

## Semantyka podmiotów

Wartość `message.new actor_id` oznacza nadawcę wiadomości. W przypadku `message.edited` nie jest wyznaczany redaktor; `payload.sender_id` rejestruje nadawcę zaobserwowanej wiadomości. Usunięcie identyfikator actor_id pozostaje pusty. Wiadomości serwisu członkostwa zachowują nadawcę i typ działania, nie traktując każdego usunięcia jako dobrowolnego odejścia. Surowe aktualizacje dotyczące uczestników zachowują identyfikator actor_id w postaci podanej. Migawki reakcji nie tworzą fikcyjnego podmiotu wprowadzającego zmianę.

Powiadomienia o usunięciu wiadomości w czatach prywatnych i zwykłych grupach zawierają wyłącznie identyfikatory wiadomości. Czaty te korzystają z jednej sekwencji identyfikatorów obejmującej całe konto, więc dany identyfikator określa pojedynczą wiadomość na tym koncie. Jeżeli wiadomość o tym identyfikatorze została wcześniej zapisana w tym dzienniku, usunięcie jest rejestrowane w tej rozmowie jako message.deleted, przy czym nazwa metody to payload.chat_resolution. Identyfikatory, które nigdy nie zostały zapisane, są przechowywane jako deletion.unscoped bez chat_id; nie dokonuje się żadnych domysłów. Kanały i supergrupy numerują wiadomości w ramach poszczególnych czatów i nigdy nie są dopasowywane w ten sposób. Gdy usunięta wiadomość została wysłana przez obserwowane konto, payload.deleted_message_was_outgoing ma wartość true; nadal nie podano osoby, która dokonała usunięcia.

## Zakres: ciągłość, luki oraz niezauważone identyfikatory

Każdy podpisany plik ZIP zawiera `coverage.json`, raport HTML otwiera się z tym samym podsumowaniem, a `verify.py` ponownie oblicza je na podstawie `events.jsonl`, zamiast polegać na treści pliku:

- **Ciągła obserwacja od X do Y.** Okres rozpoczyna się od `observation.started` i kończy się w momencie pauzy, zatrzymania, utraty połączenia z Telegramem, wylogowania, uruchomienia procesu bez prawidłowego zakończenia lub upływu ponad trzech minut bez żadnego zapisu podczas obserwacji (sygnały kontrolne są zapisywane co minutę, więc cisza oznacza, że proces się zatrzymał, zawiesił lub komputer przeszedł w stan uśpienia). Gdy interwał sygnałów kontrolnych zostanie zmieniony w **sekcji „Parametry”**, każdy sygnał rejestruje tę zmianę, a dopuszczalny czas ciszy wynosi trzy interwały, nigdy mniej niż trzy minuty.
- W wykazie **luk** podano czas między okresami wraz z przyczyną. Luka, która w momencie ostatniego wpisu pozostawała nadal otwarta, została oznaczona jako `not_resumed_by_last_record`.
- **Nie odnotowano identyfikatorów wiadomości.** W przypadku kanałów i supergrup, w których liczba wiadomości jest przypisana do poszczególnych czatów, brakujące identyfikatory pomiędzy odnotowanymi są podawane w postaci przedziałów. Są one zgłaszane jako *nieodnotowane* — usunięte, nigdy niedostarczone lub znajdujące się poza zapisaną historią — nigdy jako usunięte. Czatach prywatnych i zwykłych grupach stosowana jest sekwencja wspólna dla całego konta, więc luki w tych przypadkach nie mają znaczenia i nie są wymieniane.
- Powiadomienia o lukach na poziomie czatu (na przykład prośba serwisu Telegram o odtworzenie różnic w jednym kanale) są traktowane jako notatki; nie przerywają one globalnego zasięgu monitorowania.

Zakres działania opisuje, co zarejestrował ten kolektor. Nie stanowi to dowodu na to, że serwis Telegram dostarczył każdą aktualizację w danym, nieprzerwanym okresie.

## Producent

Podpisany manifest plików ZIP zawierających dowody, eksporty czatów, dzienniki świadków oraz oświadczenia dotyczące plików profilowych osób zawiera `producer` : oprogramowanie, wersję, projekt (PhishDestroy), stronę główną oraz repozytorium źródłowe. Raport HTML zawiera ten sam wiersz, a `verify.py` wyświetla go jako część zweryfikowanych danych. Archiwa utworzone przed wprowadzeniem tego pola są weryfikowane tak jak dotychczas i zgłaszane jako nieokreślające twórcy.

## Profile osób

Plik profilu (`tgwitness-dossier-v1`, JSON) jest generowany na żądanie na podstawie zapisów już znajdujących się w dzienniku dla jednej rozmowy; żadne dane nie są pobierane z serwisu Telegram, a zawartość profilu nigdy nie jest zapisywana w dzienniku (włączanie i wyłączanie profili jest rejestrowane jako `dossier.changed`). Dla każdej osoby, której wiadomość została zapisana, podaje się imię i nazwisko oraz historię nazw użytkownika, oznaczenia Telegrama (bot, oszustwo, fałszywy, premium, zweryfikowany, z ograniczeniami, usunięty) widoczne w momencie zapisywania, identyfikatory zdjęć profilowych identyfikatory zdjęć profilowych, skrót SHA-256 oraz skrót percepcyjny (pHash, zgodny z `imagehash.phash`) awatara z lokalnej pamięci podręcznej awatarów wraz z podobnymi awatarami, aktywność (pierwsza i ostatnia wiadomość, liczby, edytowane i usunięte udostępnienia, wiadomości według godzin UTC), kto odpowiada komu, inne czaty w tym dzienniku, w których dana osoba pisała, oraz wymienione portfele (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; adresy Base58Check są weryfikowane pod kątem sum kontrolnych), numery telefonów, nazwy użytkowników oraz linki, w tym linki ukryte w tekście.

Każdy fakt zawiera odniesienie do wpisu w dzienniku (`seq`), z którego pochodzi, a `record_hashes` zawiera skrót każdego wpisu, do którego się odwołuje. Oświadczenie jest podpisane kluczem obszaru roboczego:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

Sprawdza podpis, weryfikuje sam eksport dowodów (podpis, łańcuch skrótów i pliki) oraz upewnia się, że każdy przywołany zapis istnieje w niezmienionej postaci w tym eksporcie tego samego obszaru roboczego. Skróty awatarów są oznaczone jako pochodzące z lokalnej pamięci podręcznej (a nie z zapisów dziennika). Wzmianki są dopasowaniami wzorców — stanowią wskazówki do sprawdzenia, a nie zweryfikowane fakty. Profile są włączane dla poszczególnych czatów, można je eksportować jako plik ZIP zaszyfrowany algorytmem AES-256 z hasłem oraz są usuwane po wyłączeniu lub gdy czat zostanie usunięty ze źródeł.

## Niezależny świadek

Dziennik świadka (`tgwitness-witness-v1`) oraz posty na jego kanale są porównywane z eksportem dowodów za pomocą `verify.py --witness … --channel …`; zob. [niezależny świadek](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/).

## Manifest i punkty kontrolne

Plik manifest.json zawiera format, czas eksportu, klucz publiczny, odcisk palca, długość dziennika, hash początku, zakres, producenta, ograniczenia oraz wartość SHA-256 każdego elementu treści innego niż same `manifest.json` i `manifest.sig`. Plik manifest.sig stanowi podpis Ed25519 w kodowaniu base64 nad kanonicznym plikiem manifestu JSON. Narzędzie weryfikujące odrzuca nieoczekiwane lub brakujące elementy, zduplikowane nazwy, uszkodzone pliki, złamane sekwencje lub łańcuchy, nieprawidłowe podpisy oraz niezgodności z podanym punktem kontrolnym. Nigdy nie wyodrębnia ścieżek archiwum. Ogranicza całkowity zadeklarowany rozmiar po rozpakowaniu do 4 GiB; format `--max-gib N` pozwala na tworzenie większych archiwów dzięki podwyższonemu limitowi **parametrów**.

Kod weryfikacyjny należy uzyskać z zaufanego źródła lub z niezależnej kopii poddanej weryfikacji. Weryfikator znajdujący się w niezaufanym archiwum stanowi materiał wykonywalny dostarczony przez autora tego archiwum; jego obecność ma na celu ułatwienie przenoszenia danych, a nie stanowi niezależnego punktu odniesienia.

Punkt kontrolny podpisuje oświadczenie zawierające klucz publiczny, długość dziennika, skrót początkowy oraz czas utworzenia. Weryfikator może sprawdzić, czy późniejsze archiwum zawiera ten sam prefiks. Należy zachować punkt kontrolny poza kolektorem przed wprowadzeniem spornej zmiany: osoba atakująca kontrolująca zarówno archiwum, jak i punkt kontrolny może zastąpić oba elementy.

Ważny podpis z klucza nieprzypiętego potwierdza jedynie wewnętrzną spójność. Nawet klucz przypięty nie może potwierdzić autentyczności treści źródłowej, jeśli urządzenie rejestrujące lub klucz zostały naruszone przed rozpoczęciem rejestracji. Zewnętrzne oznaczanie czasem oraz wiarygodne przechwytywanie danych to odrębne wymagania. TgWitness nie gwarantuje dopuszczalności dowodowej ani certyfikacji kryminalistycznej.

## Załączniki

Pliki są identyfikowane za pomocą skrótu SHA-256 w katalogu media/. Plik media.saved powiązuje skrót oraz długość w bajtach z konkretnym zdarzeniem wiadomości. Surowymi nazwami plików są metadane, nigdy lokalne ścieżki. Bajty multimediów są pobierane asynchronicznie, więc natychmiastowe usunięcie może uniemożliwić ich przechwycenie. Wyniki obejmują: wyłączone gromadzenie danych, pliki o zbyt dużym rozmiarze lub o nieznanym rozmiarze, niepowodzenia pobierania oraz przerwane pobieranie. Awaria procesu może pozostawić częściowe pliki bez odnośników; nie są one uwzględniane w eksportach.

Eksportator ZIP weryfikuje zapisane pliki multimedialne na podstawie ich nazw. Eksporty w formatach JSONL, CSV i HTML weryfikują sygnatury zdarzeń, ale nie zawierają danych multimedialnych. Raporty pochodne mają charakter pomocniczy; plik events.jsonl stanowi autorytatywny zapis zdarzeń.

## Trwałe gromadzenie i przetwarzanie potwierdzeń (0.2)

Operacja dotycząca pliku multimedialnego oraz zapis zdarzenia wiadomości odbywają się w ramach jednej transakcji. Zadanie przechowuje oryginalny deskryptor wiadomości z Telegramu; podpisana obserwacja wiąże się z jej skrótem SHA-256, kontem oraz zasadami dotyczącymi rozmiaru. Funkcja odzyskiwania weryfikuje tę powiązanie przed pobraniem. Nigdy nie pobiera aktualnej wiadomości i nie zastępuje w sposób niewidoczny nowszego załącznika. Przerwane zadania są ponawiane, natomiast trwała awaria pozostaje jednoznacznym wynikiem.

Każdy obszar roboczy posiada własny dziennik oraz tożsamość podpisującą. Zdarzenie „process.started” zawiera identyfikator uruchomienia, lokalne zegar, wersje zależności, skróty plików źródłowych, początkowe konto/zakres oraz ustawienia przechwytywania. Sygnały kontrolne zawierają identyfikator uruchomienia, czas monotoniczny oraz stan kolejki. Potwierdzenie przebiegu procesu można również pobrać jako oddzielnie podpisane oświadczenie. Pomiary plików są zgłaszane samodzielnie i nie stanowią wiarygodnego poświadczenia sprzętowego.

Automatyczne punkty kontrolne są przechowywane lokalnie podczas uruchamiania, co pięć minut w trakcie monitorowania (**Parametry → Podpisany punkt kontrolny co**) oraz przy prawidłowym zakończeniu działania. Weryfikacja przy uruchomieniu oraz eksport polegają na porównaniu dziennika z najnowszym zachowanym lokalnym punktem kontrolnym. Pozwala to wykryć cofnięcie zmian w bazie danych, o ile punkt kontrolny pozostał nienaruszony; operator kontrolujący oba elementy może jednak nadal zastąpić oba. Niezależne przechowywanie danych oraz zewnętrzne, wiarygodne znaczniki czasu pozostają odrębnymi wymaganiami.

Po ponownym uruchomieniu przywracana jest zapisana pozycja aktualizacji w Telegramie (`catch_up_from` w `observation.started`), a brakujące aktualizacje są pobierane. Okresowa ponowna weryfikacja rejestruje `message.recovered` dla brakujących wiadomości oraz `message.missing_on_recheck`, gdy Telegram nie zwraca już zapisanej wiadomości; ten ostatni wpis nie stanowi powiadomienia o usunięciu i nie podaje ani osoby, która dokonała usunięcia, ani czasu.

### Kopia zapasowa i przywracanie danych poza serwerem (S3)

Kopia zewnętrzna (opcja „Eksporty”, domyślnie wyłączona) przesyła segmenty dziennika, zachowane pliki, punkty kontrolne wraz z sygnaturami czasowymi oraz gotowe eksporty czatów do magazynu danych zgodnego ze standardem S3, zaszyfrowane algorytmem algorytmem AES-256-GCM przed przesłaniem przy użyciu klucza przechowywanego w skarbcu obszaru roboczego; stosowana jest retencja Object Lock, o ile obsługuje ją zasób. Bez pobranego klucza kopia nie może zostać odczytana. Przywrócenie i weryfikacja za pomocą `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Przywrócenie danych wymaga pustego, zwykłego katalogu. Pobrane i odszyfrowane obiekty pozostają w prywatnej pamięci tymczasowej do momentu zweryfikowania całego dziennika oraz każdego zachowanego punktu kontrolnego. Niebezpieczne ścieżki obiektów, niespójne zakresy segmentów oraz dzienniki krótsze niż punkt kontrolny są odrzucane; w przypadku niepowodzenia weryfikacji przywrócone pliki nie są publikowane. Kontrole retencji porównują zwrócony tryb blokady obiektu oraz datę z terminem wysłanym podczas przesyłania (z tolerancją zaokrąglenia wynoszącą jedną sekundę). Wygasły, nieważny lub skrócony termin nie jest uznawany za zweryfikowany. Status informuje o losowo wybranym obiekcie, którego retencja została odczytana dla danej operacji przesyłania.

Postęp kopiowania jest ograniczony do miejsca docelowego i klucza szyfrującego. Zmiana punktu końcowego, zasobnika lub prefiksu powoduje rozpoczęcie pełnego kopiowania lokalnie przechowywanego dziennika, plików multimedialnych i punktów kontrolnych do tego miejsca docelowego. Stary postęp nieobjęty zakresem zostaje zachowany, ale po aktualizacji jest odtwarzany jednokrotnie. Historyczne eksporty czatów, które zostały już usunięte z lokalnej skrzynki nadawczej, pozostają w poprzednim miejscu docelowym.

Brakujące lub uszkodzone pliki lokalne są zgłaszane jako błąd danego przebiegu i kursor pozostaje przed tym miejscem, dzięki czemu plik zostanie ponownie przetworzony podczas następnego przebiegu; pliki, punkty kontrolne i eksporty znajdujące się za nim są nadal kopiowane. Funkcja przywracania sprawdza wszystkie odniesienia do zachowanych plików pod kątem odszyfrowanych skrótów i zarejestrowanych rozmiarów. Identyczne, nakładające się segmenty dziennika pochodzące z przerwanych operacji przesyłania są deduplikowane; sprzeczne nakładania się są odrzucane. Punkty kontrolne utworzone podczas przesyłania są odkładane do momentu, aż objęte nimi zapisy dziennika zostaną skopiowane, dzięki czemu zakończony przebieg nie publikuje punktu kontrolnego przed odpowiadającym mu wpisem w dzienniku.

### Przesyłanie strumieniowe migawek eksportu

Eksporty strumieniowe wykorzystują stabilną migawkę odczytu bazy danych SQLite. Jej początek może być starszy niż aktualny dziennik na żywo w momencie zakończenia pobierania. Punkt kontrolny utworzony po tej migawce może prawidłowo wskazywać, że archiwum jest krótsze; należy porównać go z punktem kontrolnym znajdującym się w miejscu lub przed eksportowanym prefiksem, a nie z dowolnym późniejszym punktem kontrolnym.

## Przygotowanie RFC 3161 i weryfikacja odpowiedzi (0.2)

Tryb dowodowy (domyślnie wyłączony) wysyła wyłącznie skróty SHA-256 każdego podpisanego punktu kontrolnego do wymienionych instytucji zgodnych z RFC 3161 oraz kalendarzy OpenTimestamps, korzystając z trasy przestrzeni roboczej, a nigdy poprzez MTProxy. Odpowiedzi są przechowywane w `checkpoints/anchors/`, eksportowane i sprawdzane przez `verify.py` (`--tsa-ca` sprawdza podpis TSA; potwierdź dowody OpenTimestamps za pomocą `ots upgrade` i `ots verify`).

Panel przygotowuje archiwum żądań zawierające kanoniczne bajty pliku checkpoint.json, odcisk wiadomości SHA-256 oraz losowy nonce w pliku timestamp.tsq, sumy kontrolne oraz instrukcje. Nie są wysyłane żadne żądania sieciowe. Przygotowanie to nie stanowi zaufanego znacznika czasu.

`python -m tgwitness.anchor verify` wywołuje bibliotekę OpenSSL dwukrotnie: raz w odniesieniu do bajtów punktu kontrolnego i raz w odniesieniu do oryginalnego żądania. Wymagany jest wyraźnie wskazany plik zaufanego urzędu certyfikacji; załączone certyfikaty nie są automatycznie uznawane za zaufane. Sprawdzanie żądania jest opcjonalne w interfejsie CLI, dlatego należy zachować i podać opcję --request w celu sprawdzenia wartości nonce. Wynik wskazuje, czy sprawdzenie zostało przeprowadzone. Podpis punktu kontrolnego kolektora oraz dziennik muszą nadal zostać zweryfikowane osobno przy użyciu zaufanego odcisku palca kolektora.

Obecny weryfikator nie pobiera informacji o unieważnieniach ani nie zapewnia długoterminowej weryfikacji archiwalnej po wygaśnięciu certyfikatu. Nie należy utożsamiać pomyślnej weryfikacji podpisu z kwalifikowanym znacznikiem czasu ani dopuszczalnością dowodową w postępowaniu sądowym. W trakcie opracowywania narzędzia nie nawiązano kontaktu z prawdziwą, niezależną agencją TSA. Proszę zapoznać się z [procedurą](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/).
