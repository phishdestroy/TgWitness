# Format dowodów

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/

Zawartość podpisanego pliku ZIP, rodzaje zapisów, potwierdzenia przetwarzania, profile użytkowników, kopie zewnętrzne oraz weryfikacja w trybie offline.

TgWitness zabezpiecza widoczne na koncie obserwacje z Telegrama w podpisanym dzienniku. Odbiorcy mogą zweryfikować zapisane dane, załączniki i raporty przy użyciu zaufanego klucza kolektora, a następnie porównać dziennik z niezależnie przechowywanym punktem kontrolnym. Na tej stronie opisano formaty, kontrole oraz materiały, które należy zachować do celów przekazania.

Recipients can start with **VERIFY.cmd** on Windows: it asks for the original ZIP and independently obtained key fingerprint, displays an explained result, and saves a separate verification transcript. See [verification launchers and the portable runtime](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) for setup and trust limits.

## Co jest podpisane

| Materiały | Ochrona | Co należy zachować |
| --- | --- | --- |
| Każdy wpis w dzienniku, w tym zdarzenia operacyjne | Łańcuch SHA-256 oraz podpis Ed25519 dla każdego zdarzenia | Oryginalny `events.jsonl`, odcisk klucza zaufanego oraz zachowany punkt kontrolny |
| Zawartość pliku ZIP z dowodami | `manifest.sig` podpisuje manifest kanoniczny, zawierający listę skrótów plików treści | Kompletny plik ZIP, zawierający manifest oraz podpis |
| Zachowane załączniki | SHA-256 i liczba bajtów w podpisanym zdarzeniu typu „`media.saved`”; skrót pliku w podpisanym manifeście ZIP | Oryginalne dane w zweryfikowanym pliku ZIP |
| Checkpoint | Podpis Ed25519 obejmujący długość dziennika, skrót nagłówka, klucz publiczny oraz czas utworzenia | Niezależna kopia zachowana przed wprowadzeniem spornej zmiany |
| Potwierdzenie wykonania | Signed record of the collector version, source-file hashes and start settings, also included in `process.started` | The receipt, associated journal and the environment evidence for the selected verification mode |
| Czytelne raporty: `report.html` i jego części, `report.json`, `report.pdf`, `chat.pdf` | Pieczęć Ed25519 na każdym pliku potwierdzająca jego zawartość; plik PDF zawiera również standardowy podpis PDF (zobacz [Czytelne raporty](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#readable-reports)) | Otrzymany plik oraz odcisk klucza zaufanego; plik ZIP, którego dotyczy opis |
| Samodzielny plik CSV | Brak samodzielnego podpisu kryptograficznego; same skróty zdarzeń są niewystarczające | W celu sprawdzenia integralności prosimy o użycie dokładnie tej samej kopii, która znajduje się w zweryfikowanym pliku ZIP. |
| Zrzuty ekranu, wydruki lub pliki PDF wygenerowane przez przeglądarkę | Brak podpisu TgWitness na materiale pochodnym | Należy zachować oryginalny, zweryfikowany pakiet oraz udokumentować sposób powstania jego pochodnej wersji |

Kolektor weryfikuje podpisy dziennika przed wygenerowaniem każdego formatu eksportu. Czytelne raporty w formatach HTML i PDF posiadają własne pieczęcie; samodzielny plik CSV jest sprawdzany jako część podpisanego archiwum ZIP. Należy zachować archiwum ZIP, aby zachować bajty załączników i manifest, a także oddzielny punkt kontrolny w celu porównania dziennika z wcześniejszym punktem granicznym.

## Comparing chat exports

Verify and compare two signed chat-export ZIPs with independently retained signer fingerprints:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

When both archives record the same numeric account and chat IDs, records are paired by message ID. **Unchanged** means equality of the complete saved JSON record: full text, author, dates, reply target, nested metadata and unknown fields are all included. JSON object key order does not matter; absent fields, nulls, value types and array order do. The 300-character preview is only for display. Changed entries name the differing top-level `changed_fields`, including changes invisible in that preview. Duplicate message IDs are rejected instead of overwriting one another during matching.

A difference can be a changed display name, view count, collection annotation or other observation metadata. It does not by itself establish a Telegram edit, identify who made a change, or prove which contradictory archive is accurate. Unparsed records remain in the comparison; equality of their saved representation does not mean their Telegram payload was decoded.

For different or missing account/chat identities, the tool only finds possible correspondences using sender, complete text, file hash, media type and a five-second time tolerance. It reports **Matched**, not **Unchanged**. These candidates do not establish message identity or equality of all metadata. Unparsed records remain unmatched. Differences in paired records remain listed in `changed`, including in content mode; these differences do not prove edits of the same message. With `--json`, `matched` counts pairs and `unchanged` counts pairs whose complete saved records are equal. Neither count proves message identity in content mode. The existing `changed_fields` and integer `unchanged` output remain compatible with earlier comparison results. Archive format and signature verification are unchanged.

## Przekazanie sprawy do dalszego dochodzenia

1. W notatkach dotyczących sprawy należy odnotować numer referencyjny sprawy, operatora, numeryczny identyfikator konta Telegram, wybrane źródła, zasady gromadzenia danych oraz okres gromadzenia. TgWitness zapisuje obserwacje oraz obsługuje notatki powiązane ze źródłami i zbiory danych w [panelu Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-board/). Dokumentację dotyczącą przekazania i przechowywania należy przechowywać wraz z materiałami sprawy. Sprawdź planowaną konfigurację gromadzenia danych za pomocą [procedury akceptacji na żywo](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

Pomyślna weryfikacja potwierdza integralność w odniesieniu do zaufanego klucza kolektora i zachowanego zakresu. Zobacz [zakres weryfikacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope), aby zapoznać się z założeniami dotyczącymi zaufania oraz [wynikami walidacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/) przeprowadzonych kontroli.

## Fragment protokołu przekazania

Podpisany plik ZIP zawiera cały dziennik obszaru roboczego. Gdy sąd, prawnik lub biuro ds. nadużyć potrzebuje tylko niektórych czatów, określonego okresu lub konkretnych osób, **opcja Eksporty → Wyciąg do przekazania** przygotowuje zredukowaną kopię (`tgwitness-handover-v1`) zgodnie z wybranymi zasadami ujawniania. Operator określa cel i wybiera rozmowy, opcjonalny okres (UTC), osoby, których dotyczy wyciąg, co dzieje się z pozostałymi osobami (są wyświetlane, zastępowane pseudonimami P01, P02… lub pominięte ), które treści wiadomości pozostają, które załączniki i zdjęcia profilowe są uwzględnione oraz czy numery telefonów i adresy e-mail w tekstach są zamaskowane. Cel i te zasady znajdują się w podpisanym manifeście oraz w raporcie; dziennik rejestruje wpis „`handover.exported`” wraz z danymi dostępu, które go przygotowały, oraz skrótem SHA-256 pliku, a nie jego treścią.

Skrypt `verify.py` sprawdza wyodrębniony fragment na dwa sposoby. Zapis oznaczony jako niezmieniony jest weryfikowany w całości: jego treść jest porównywana z sumą kontrolną, podpisem Ed25519 oraz linkiem do dołączonego poprzednika. Z minimalizowanego zapisu zachowywane są oryginalny skrót i podpis, więc podpis nadal się zgadza, ale pominiętych pól nie da się na tej podstawie ponownie obliczyć; zapis określa, co zostało pominięte, a raport to zaznacza. Manifest podaje długość dziennika i nagłówek wraz z podpisem kolektora nad tym nagłówkiem oraz zlicza pominięte zapisy; plik `coverage.json` opisuje wybrane czaty. Nazwy występujące w nazwach plików nie są wykrywane. Przed udostępnieniem sprawdź ostateczne pliki: swobodny tekst, nazwy plików i wybrane załączniki nadal mogą umożliwiać identyfikację osób. Zachowaj pełny, podpisany plik ZIP: wyodrębniona zawartość stanowi ujawnienie, a nie zamiennik.

## Czytelne raporty

Podpisane dowody, pliki przekazywane oraz archiwa ZIP czatów zawierają czytelne raporty w formatach HTML i JSON, a także PDF, o ile dostępne są wymagane czcionki, w wybranym języku raportu. Każdy raport jest zabezpieczony kluczem Ed25519 obszaru roboczego i można go zweryfikować osobno: ` `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]``.

- `report.html` / `chat.html`: instrukcja plombowania (`tgwitness-report-seal-v1`) zamyka plik i podpisuje każdy poprzedzający go bajt (SHA-256). Długie dzienniki i czaty są dzielone na części o konfigurowalnej wielkości (Ustawienia raportu, od 500 do 100 000 rekordów; domyślnie 5 000): `records/records-0001.html` lub `messages/messages-0001.html`, z których każdy jest opatrzony numerem, zakresem i sumą oraz wymieniony wraz z plikiem SHA-256 w podpisanym manifeście. Serie sygnałów kontrolnych kolektora są wyświetlane jako jeden wiersz, chyba że w ustawieniach raportu wybrano wyświetlanie ich pojedynczo.
- `report.json` (`tgwitness-report-json-v1`, klucze `format`, `report`, `seal`): pieczęć podpisuje SHA-256 kanonicznego JSON z `report`, dzięki czemu fakty mogą być odczytywane przez systemy obsługi spraw i skrypty, a na ich podstawie można dokonać wyboru w celu ochrony danych, przy czym podpisany plik pozostaje nienaruszony.
- `report.pdf` / `chat.pdf`: formalny dokument przeznaczony do wydruku i archiwizacji, podpisany dwukrotnie na tych samych bajtach, obejmujący cały plik z wyjątkiem wartości podpisu (`/ByteRange`). Standardowy podpis PDF (`adbe.pkcs7.detached`, CMS wraz z SHA-256 i ECDSA P-256) wykorzystuje samodzielnie wygenerowany certyfikat do podpisywania dokumentów przechowywany w skarbcu obszaru roboczego; jego numer seryjny podmiotu stanowi odcisk klucza Ed25519 . Pieczęć Ed25519 znajduje się wewnątrz CMS jako niepodpisany atrybut `2.25.240684792623320047764573196045913242332` i określa certyfikat SHA-256 za pomocą `"content": "pdf-byte-range"`, więc klucz Ed25519 poświadcza certyfikat. Czytnik PDF pokazuje, czy plik uległ zmianie po podpisaniu i uznaje podpisującego za nieznanego, dopóki certyfikat nie zostanie uznany za zaufany; zamiast tego należy porównać odcisk palca Ed25519. Pliki PDF w języku chińskim, japońskim i koreańskim wymagają czcionki na serwerze (lub w `TGWITNESS_FONT_DIR`); w przypadku jej braku plik ZIP zawiera wyłącznie raporty HTML i JSON .

W kanale lub supergrupie Telegram numeruje wiadomości 1, 2, 3… w kolejności. Eksport czatu zawiera listę pierwszego i ostatniego numeru, liczbę obecnych wiadomości oraz każdy ciąg brakujących numerów w `message-ids.json` , manifeście i nagłówku `chat.json` , a także zaznacza każdą lukę w miejscu, w którym występuje ona w transkrypcji. `verify.py` ponownie je zlicza od `chat.json` . Brakujący numer to wiadomość, której Telegram nie zwrócił (usunięta przed eksportem lub niewidoczna dla konta); w czatach prywatnych i grupach podstawowych numery są wspólne dla wszystkich czatów danego konta, a luki nie są liczone.

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer records that the number is unavailable to this account at recheck time; it leaves the cause unspecified. A message returned on recheck is added to the export and marked `found_on_recheck`.

Każdy raport rozpoczyna się od **. W skrócie**: jeden akapit, a następnie to, co pokazuje materiał i czego nie pokazuje (kto stoi za kontem, kompletność dostarczonych danych, usunięcia przed obserwacją, czas zegarowy bez sygnatury czasowej). Własna pieczęć strony zmienia kolor na bursztynowy, gdy przeglądarka sprawdzi podpis pieczęci, a nie samą stronę: przeglądarka nie nadaje stronie własnych bajtów. Zmienia kolor na zielony tylko wtedy, gdy czytelnik przeciągnie plik do pola sprawdzania na końcu strony i każdy bajt się zgadza, oraz tylko wtedy, gdy wyświetlana strona jest tym plikiem; w przeciwnym razie zmienia kolor na czerwony.

Każdy raport podaje dokładną nazwę programu: commit w systemie Git, w którym kolektor uruchamia się po pobraniu kodu lub instalator ustawia `TGWITNESS_COMMIT`, oraz SHA-256 plików źródłowych (`source_tree_sha256`, kanoniczny JSON ścieżki → SHA-256 każdego pliku `.py`, `.js`, `.css`, `.html` i `.svg` w pakiecie), które odtwarza pobranie kodu z tego commitu, o ile pliki nie zostały zmienione. Klient Telegram jest nazywany na podstawie swojej biblioteki, warstwy API i centrum danych. W momencie rozpoczęcia obserwacji oraz rozpoczęcia i zakończenia eksportu czatu kolektor pyta Telegram o jego czas (`updates.getState`, w całych sekundach) i rejestruje czas Telegram pomniejszony o czas zegara kolektora, z uwzględnieniem niepewności wynikającej z czasu przesyłu w obie strony; raporty przedstawiają te pomiary w sekcji „Łańcuch dowodowy”. Eksport czatu rejestruje również moment odczytania historii, oprócz dat wiadomości.

### Przeglądarka raportów w trybie offline i przewodnik po archiwizacji

Przed otwarciem plików `chat.html` lub `report.html` należy rozpakować cały plik ZIP. Przeglądarka umożliwia wyszukiwanie, filtrowanie, przeglądanie uczestników, wskaźników, szczegółów zapisów oraz wybór plików JSON i CSV bez konieczności korzystania z serwera. Należy trzymać pliki `viewer/` i `media/` obok raportu. Wybrane elementy są pochodnymi: należy użyć pliku `verify.py SELECTION.json
--evidence ARCHIVE.zip`, aby porównać je z podpisanym archiwum. Narzędzie weryfikujące sprawdza identyfikator raportu, klucz podpisu, granice archiwum oraz każdą wybraną pozycję; pozycje edytowane, brakujące i zduplikowane nie przechodzą weryfikacji. Uwagi dotyczące wyboru oraz czas utworzenia pozostają niepodpisanymi metadanymi.

Luki w numeracji wiadomości są wyświetlane wyłącznie w przypadku kompletnego, niefiltrowanego strumienia czatu w porządku rosnącym. Ukrycie kategorii lub niepowodzenie w załadowaniu fragmentu danych nie może sprawić, że pominięty wiersz stanie się dowodem na brak wiadomości. Podświetlanie wyników wyszukiwania działa na tekście zwykłym przed zastosowaniem sekwencjiHTML, zachowując dosłowne znaczniki.

Przeglądarka sprawdza podpisy manifestu, identyfikator raportu i klucz oraz wszystkie wymienione skróty plików. Odrzuca niejednoznaczne lub nieprawidłowo sformowane struktury ZIP, zduplikowane nazwy i niebezpieczne ścieżki, a także ogranicza rozmiar plików do 256 MiB i deklarowaną całkowitą zawartość do 4 GiB. W przypadku większych archiwów należy użyć samodzielnego weryfikatora. Ta kontrola przeglądarkowa uzupełnia sprawdzanie łańcuchów dzienników i semantyki danych przeprowadzane przez weryfikator.

Plik `README.txt` zawiera przewodnik startowy, zsynchronizowany spis plików, instrukcje weryfikacji oraz uwagi dotyczące formatu danych w języku raportu, a po nim znajduje się kompletny przewodnik w języku angielskim. Plik `SHA256SUMS` obejmuje wymienione w nim pliki, z wyłączeniem samego siebie, plików `manifest.json` i `manifest.sig`; podpisany manifest obejmuje również plik `SHA256SUMS`. Należy pozostawić oryginalny plik ZIP bez zmian, a pliki robocze zapisać poza rozpakowanym folderem. Raporty PDF zawierają zakładki sekcji oraz identyfikatory sprawy/raportu na kolejnych stronach.

### Czat w momencie eksportu

Eksport czatu rejestruje informacje podane przez Telegram na temat czatu w momencie rozpoczęcia eksportu: własne etykiety Telegram (`scam`, `fake`, `restricted` wraz z uzasadnieniami, `verified`), nazwy użytkowników, opis, liczbę członków i administratorów, powiązaną dyskusję, ochronę treści, informację, czy nowi członkowie widzą wcześniejsze wiadomości oraz od której wiadomości na tym koncie widoczna jest historia (`available_min_id`), datę pierwszej wiadomości, jeśli jest to data utworzenia czatu, oraz SHA-256 zdjęcia czatu (zapisanego w `media/`). Rejestruje pozycję konta eksportującego w czacie: rolę, datę dołączenia, kto je zaprosił, a w przypadku administratora – jego uprawnienia. Zamiast tego podawana jest nazwa żądania, które Telegram odrzuciło.

Gdy konto eksportujące jest kontem administratora, eksport odczytuje dziennik administratora czatu (Telegram przechowuje dane przez około 48 godzin) do pliku `admin-log.json`: usunięcia i edycje wraz z treścią oraz kontem, które wykonało daną czynność. Jest to jedyny zapis usunięcia, który wskazuje, kto dokonał usunięcia.

### Wskaźniki

Lista raportów oraz archiwum zawierają oznaczenia `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) oraz `indicators.misp.json` (zdarzenie MISP ), na podstawie których dział ds. nadużyć może podjąć działania w odniesieniu do zarejestrowanych wiadomości: linki i domeny (również ukryte w tekście, przyciskach i podglądach linków), adresy kryptowalut, nazwy użytkowników i linki zaproszeniowe Telegram , numery telefonów, adresy e-mail oraz zapisane zdjęcia. Adresy Bitcoin, Litecoin, Dogecoin i TRON są uwzględniane tylko wtedy, gdy ich suma kontrolna base58 jest poprawna, adresy segwit – gdy ich suma kontrolna bech32 lub bech32m jest poprawna, a adresy TON – gdy ich suma CRC jest poprawna; adresy EVM i Solana są oznaczone jako niesprawdzone. Zdjęcia zawierają SHA-256 oraz percepcyjny hash (dHash, 64 bity), który pozostaje niemal niezmieniony w przypadku ponownej kompresji lub zmiany rozmiaru kopii. Raporty zapisują wskaźniki w taki sposób, aby nie otwierały się przypadkowo (`hxxps[://]example[.]com` ); pliki zachowują wartości w niezmienionej postaci. Każdy wskaźnik jest oznaczony jako nieznany i nieprzeznaczony do automatycznego wykrywania (STIX , `indicator_types: unknown` , MISP , `to_ids: false` , dystrybucja do własnej organizacji): umieszczenie na liście oznacza, że wiadomość go zawierała, a nie że jest złośliwy. Link, którego tekst wskazuje inny adres niż ten, który się otwiera, jest zaznaczony w raporcie.

Raporty typu „PDF” kończą się oświadczeniem biegłego, które należy podpisać odręcznie, listą kontrolną dla notariusza lub biegłego sądowego oraz kodem QR (znajdującym się również na pierwszej stronie) zawierającym identyfikator raportu, odcisk klucza oraz SHA-256 danych referencyjnych, dzięki czemu wydruk pozwala na powrót do archiwum.

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

An unscoped notice does not establish that a message was never saved: a matching chat may be outside the current observation scope, or a unique match may be unavailable. Recheck absence remains a separate observation from a deletion notification in report counts, filters and labels. A later recovery clears the current missing state while preserving the earlier unsuccessful check in the signed history; neither observation establishes a deletion notice.

Multiple IDs resolved to the same chat from one notification are grouped as `deletion.batch`, regardless of their count. The notification does not establish that the entire history was cleared, who performed the deletion, or whether it applied to all participants. Saved outgoing messages do not change these limits. Older journals may contain `history.cleared` events inferred from batches of ten or more IDs, with explanatory text attributing the deletion to the other participant. Those inferences are not supported by the update. Preserve those original signed records, but treat them as grouped deletion notifications; the current interface labels them accordingly.

## Zakres: ciągłość, luki oraz niezauważone identyfikatory

Każdy podpisany plik ZIP zawiera `coverage.json`, raport HTML otwiera się z tym samym podsumowaniem, a `verify.py` ponownie oblicza je na podstawie `events.jsonl`, zamiast polegać na treści pliku:

- **Ciągła obserwacja od X do Y.** Okres rozpoczyna się od `observation.started` i kończy się w momencie pauzy, zatrzymania, utraty połączenia z Telegramem, wylogowania, uruchomienia procesu bez prawidłowego zakończenia lub upływu ponad trzech minut bez żadnego zapisu podczas obserwacji (sygnały kontrolne są zapisywane co minutę, więc cisza oznacza, że proces się zatrzymał, zawiesił lub komputer przeszedł w stan uśpienia). Gdy interwał sygnałów kontrolnych zostanie zmieniony w **sekcji „Parametry”**, każdy sygnał rejestruje tę zmianę, a dopuszczalny czas ciszy wynosi trzy interwały, nigdy mniej niż trzy minuty.
- W wykazie **luk** podano czas między okresami wraz z przyczyną. Luka, która w momencie ostatniego wpisu pozostawała nadal otwarta, została oznaczona jako `not_resumed_by_last_record`.
- **Nie odnotowano identyfikatorów wiadomości.** W przypadku kanałów i supergrup, w których wiadomości są numerowane według czatu, brakujące identyfikatory pomiędzy odnotowanymi są wymienione jako przedziały. Są one zgłaszane jako *nieodnotowane* — usunięte, nigdy niedostarczone lub znajdujące się poza zapisaną historią — nigdy jako usunięte. Czaty prywatne i zwykłe grupy korzystają z tej samej sekwencji dla całego konta, więc luki w obrębie jednego takiego czatu nie mają znaczenia i nie są tam wymieniane.
- Powiadomienia o lukach na poziomie czatu (na przykład prośba serwisu Telegram o odtworzenie różnic w jednym kanale) są traktowane jako notatki; nie przerywają one globalnego zasięgu monitorowania.

### Brakujące numery wiadomości (`gap_summary`)

**Podgląd.** `coverage.json` → `gap_summary` mierzy numery przypisane przez Telegram, których ten kolektor nigdy nie zarejestrował. Telegram numeruje wiadomości raz na kanał lub supergrupę oraz raz na konto w ramach prywatnych czatów, botów i zwykłych grup. Liczba pomiędzy dwiema zaobserwowanymi wiadomościami oznacza, że wiadomość została zaobserwowana lub brakuje jej; ciągły zakres stanowi potwierdzenie, że każda wiadomość w nim oznaczona została zaobserwowana. Luka nie wskazuje żadnego podmiotu ani przyczyny.

| Dziedzina | Znaczenie |
| --- | --- |
| `status` | `on`lub `off` gdy jest wyłączone w sekcji **Parametry → Analiza luk** |
| `parameters` | Parametry, które doprowadziły do uzyskania wyniku, aby można było go powtórzyć |
| `chats[]` | Jeden wpis na kanał lub supergrupę, z których każdy jest osobno ponumerowany |
| `account` | Sekwencja prywatnych czatów, botów i zwykłych grup w ramach całego konta |
| `status` (dla każdej sekwencji) | `applicable`lub `not_applicable` z `reason` |
| `observed_from`, `observed_to`, `span` | Pierwszy i ostatni zaobserwowany numer oraz rozmiar zakresu |
| `observed`, `observed_without_content` | Liczby zaobserwowane; te znane wyłącznie na podstawie zapisu o usunięciu lub ponownej weryfikacji |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Liczby nigdy nie zaobserwowane, ich udział w zakresie, liczba przebiegów, najdłuższy przebieg |
| `clusters[]` | Wymienione braki: `low`, `high`, `missing`oraz sąsiednie zaobserwowane liczby `after` / `before` wraz z czasami ich odnotowania |
| `service_estimate` | Tylko po włączeniu: ile brakujących numerów stanowiłoby komunikaty serwisowe przy ich zaobserwowanym udziale. Nigdy nie odejmować od `missing` |

Ważność danych wynika z dziennika, nigdy nie jest zakładana:

- **Kanały i supergrupy** są mierzone na poziomie poszczególnych czatów, również w eksporcie wybranych czatów. Pomiar opiera się na wpisach wybranych przez nadawcę `not_applicable`.
- **Sekwencja obejmująca całe konto** jest mierzona wyłącznie od pierwszej do ostatniej wiadomości, która nadeszła w czasie, gdy aktywna była funkcja gromadzenia danych z całego konta, i obejmuje prywatne czaty, boty, zwykłe grupy oraz wiadomości własne konta, bez wykluczania żadnego z tych czatów (`scope.changed`). Liczby oznaczone jako `deletion.unscoped` są traktowane jako zaobserwowane bez treści. Eksport lub przekazanie wybranych czatów nie pozwala na jej pomiar. Jeśli funkcja gromadzenia danych z całego konta była wyłączana i włączana, pojawia się adnotacja informująca, że numery użyte w międzyczasie są wyświetlane jako luki.
- Komunikaty serwisowe to wpisy w dzienniku posiadające własne numery, więc same wypełniają luki ; opcjonalna wartość szacunkowa służy jedynie jako kontekst.

`verify.py` przelicza `gap_summary` na podstawie `events.jsonl` z parametrami zawartymi w podpisanym `coverage.json` (wartości domyślne dla starszych archiwów) oraz wyświetla w podsumowaniu zasięgu wiersz obejmujący całe konto. `get_capture_status`(MCP i wiersz poleceń) zwraca ten sam pomiar dla czatów, do których użytkownik może mieć dostęp; sekwencja obejmująca całe konto dotyczy wyłącznie dostępu obejmującego cały obszar roboczy.

Repeated observations of one service message count once, and the account service estimate uses only numbers inside the measured range. An applied scope must explicitly preserve the account's own messages before account-wide measurement is enabled; older records without that information cannot establish this condition. Stopped observation does not extend the measured range, and resuming it is noted. The live archive query has a time budget, including its database scan, and marks an unfinished measurement as partial.

Telegram documents the [separate message ID sequences](https://core.telegram.org/api/updates#message-id-sequences). These numbers describe observations; they do not identify a deletion actor or establish why a number is absent.

Gdy Telegram przestaje akceptować konto, rekord `coverage.gap` kończący obserwację zawiera `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` lub `not_authorized`) oraz błąd Telegram; `verify.py` określa przyczynę zakończenia okresu.

Coverage combines recorded observation periods, interruptions and message outcomes. Assess it together with the selected chats, period and attachment policy; continuous operation alone does not establish complete delivery of Telegram updates.

## Producent

Podpisany manifest plików ZIP zawierających dowody, eksporty czatów, dzienniki świadków oraz oświadczenia dotyczące plików profilowych osób zawiera `producer` : oprogramowanie, wersję, projekt (PhishDestroy), stronę główną oraz repozytorium źródłowe. Raport HTML zawiera ten sam wiersz, a `verify.py` wyświetla go jako część zweryfikowanych danych. Archiwa utworzone przed wprowadzeniem tego pola są weryfikowane tak jak dotychczas i zgłaszane jako nieokreślające twórcy.

Każdy rekord `observation.started` podaje również nazwę klienta Telegram, który dokonał obserwacji: jego `api_id` (nigdy skrót), niezależnie od tego, czy jest to wbudowana para publiczna, czy własna aplikacja operatora, opis klienta przesłany w żądaniu połączenia Telegram oraz rodzaj trasy połączenia wraz z trybem IP (bez adresu proxy ani klucza tajnego). Raport oraz plik `custody.json` zawierają listę wszystkich unikalnych klientów i tras wraz z datą ich zarejestrowania, a także liczbę przypadków, w których żaden z wymienionych serwerów proxy nie odpowiedział, oraz liczbę przypadków, w których plik Telegram wykrył adres serwera. Potwierdzają to dzienniki zarejestrowane wcześniej.

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

Run verification from your installed TgWitness version or a reviewed checkout. The copy included in an archive supports portable use; check that copy against your trusted installation before executing it.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain the checkpoint outside the collector, so later verification compares the archive with a reference held separately from it.

## Zakres weryfikacji

Verification checks the archive and the collection mode used to produce it. Choose the mode whose trust boundary matches the case, then retain its verification inputs.

| Tryb gromadzenia danych | Co sprawdza weryfikator | Dane wejściowe do weryfikacji i granica zaufania |
| --- | --- | --- |
| Lokalny obszar roboczy | Record signatures, hash chain, manifest and attachment bytes | Independently retained collector fingerprint; the host administrator controls the local signing key |
| Lokalny obszar roboczy z niezależnym świadkiem | Kontrola archiwum oraz zgodność z wcześniejszym prefiksem dziennika zachowanym przez świadka | Separately trusted witness key and records; the checkpoint binds the prefix already observed |
| [Przechwytywanie działań GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | GitHub attestation of the archive digest, approved workflow and collector commits, hosted runner, fresh session/key origin and internal archive integrity | Trusted verifier policy, caller repository and GitHub attestation bundle; collection runs under the pinned workflow |
| [Wdrożenie w chmurze](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/) | Provider lifecycle and access records, firewall and Cloudflare state, plus the collector's signed run record | Read-only queries to the provider and Cloudflare; availability of individual checks depends on the provider |
| [Poufna maszyna wirtualna Intel TDX](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Quote signature and platform status, binding to the collector statement, compose and OS measurements | Intel trust chain and expected deployment measurements; retain the results of every required TDX check |

In sealed acquisition, the approved collector receives data through an authenticated Telegram connection inside the verified environment. Attestation binds the archive to that execution, so verification covers acquisition as well as later file integrity. This relies on the approved code and the platform trust chain listed above. GitHub capture verification requires a session created inside the run and rejects imported-session captures.

The run receipt records the collector version, file hashes and startup settings. GitHub provenance and TDX measurements provide the environment checks; the [validation record](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/) identifies tested configurations.

TgWitness signs the observations it collects; Telegram and message authors do not issue these signatures. In a local workspace, material created before the first independent checkpoint still depends on the collector and its key holder. Coverage records describe the selected scope and collection outcomes, while verified external timestamps anchor the committed archive or journal boundary in time.

## Załączniki

Pliki są identyfikowane za pomocą skrótu SHA-256 w katalogu media/. Plik media.saved powiązuje skrót oraz długość w bajtach z konkretnym zdarzeniem wiadomości. Surowymi nazwami plików są metadane, nigdy lokalne ścieżki. Bajty multimediów są pobierane asynchronicznie, więc natychmiastowe usunięcie może uniemożliwić ich przechwycenie. Wyniki obejmują: wyłączone gromadzenie danych, pliki o zbyt dużym rozmiarze lub o nieznanym rozmiarze, niepowodzenia pobierania oraz przerwane pobieranie. Awaria procesu może pozostawić częściowe pliki bez odnośników; nie są one uwzględniane w eksportach.

Eksportator ZIP weryfikuje zapisane pliki multimedialne na podstawie ich nazw. Eksporty w formatach JSONL, CSV i HTML weryfikują sygnatury zdarzeń, ale nie zawierają danych multimedialnych. Raporty pochodne mają charakter pomocniczy; plik events.jsonl stanowi autorytatywny zapis zdarzeń.

Pełny eksport czatu zapisuje załączniki zgodnie z ustawieniami załączników w obszarze roboczym w katalogu media/, nadając im nazwy w formacie SHA-256. Każdy rekord wiadomości w pliku chat.json zawiera nazwę pliku (`file`, `file_sha256`) lub powód jego braku (`file_status`), wraz z informacją o tym, co widział czytelnik wokół tekstu: linki za tekstem, źródło przekazania, przyciski botów, podpis, wyświetlenia oraz licznik czasu automatycznego usunięcia. Plik `verify.py` sprawdza, czy każdy wymieniony plik znajduje się w podpisanym manifeście pod tym skrótem.

## Trwałe gromadzenie i przetwarzanie potwierdzeń (0.2)

Operacja dotycząca pliku multimedialnego oraz zapis zdarzenia wiadomości odbywają się w ramach jednej transakcji. Zadanie przechowuje oryginalny deskryptor wiadomości z Telegramu; podpisana obserwacja wiąże się z jej skrótem SHA-256, kontem oraz zasadami dotyczącymi rozmiaru. Funkcja odzyskiwania weryfikuje tę powiązanie przed pobraniem. Nigdy nie pobiera aktualnej wiadomości i nie zastępuje w sposób niewidoczny nowszego załącznika. Przerwane zadania są ponawiane, natomiast trwała awaria pozostaje jednoznacznym wynikiem.

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The run receipt can also be downloaded as a separately signed statement. For verification of the execution environment, pair it with the GitHub attestation or TDX checks described in [Verification scope](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope).

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives. Independent retention keeps that reference available outside the workspace; a verified external timestamp additionally anchors it in time.

Po ponownym uruchomieniu przywracana jest zapisana pozycja aktualizacji w Telegramie (`catch_up_from` w `observation.started`), a brakujące aktualizacje są pobierane. Okresowa ponowna weryfikacja rejestruje `message.recovered` dla brakujących wiadomości oraz `message.missing_on_recheck`, gdy Telegram nie zwraca już zapisanej wiadomości; ten ostatni wpis nie stanowi powiadomienia o usunięciu i nie podaje ani osoby, która dokonała usunięcia, ani czasu.

### Kopia zapasowa i przywracanie danych poza serwerem (S3)

Kopia zewnętrzna (opcja „Eksporty”, domyślnie wyłączona) przesyła segmenty dziennika, zachowane pliki, punkty kontrolne wraz z sygnaturami czasowymi oraz gotowe eksporty czatów do magazynu danych zgodnego ze standardem S3, zaszyfrowane algorytmem algorytmem AES-256-GCM przed przesłaniem przy użyciu klucza przechowywanego w skarbcu obszaru roboczego; stosowana jest retencja Object Lock, o ile obsługuje ją zasób. Bez pobranego klucza kopia nie może zostać odczytana. Przywrócenie i weryfikacja za pomocą `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Przywrócenie danych wymaga pustego, zwykłego katalogu. Pobrane i odszyfrowane obiekty pozostają w prywatnej pamięci tymczasowej do momentu zweryfikowania całego dziennika oraz każdego zachowanego punktu kontrolnego. Niebezpieczne ścieżki obiektów, niespójne zakresy segmentów oraz dzienniki krótsze niż punkt kontrolny są odrzucane; w przypadku niepowodzenia weryfikacji przywrócone pliki nie są publikowane. Kontrole retencji porównują zwrócony tryb blokady obiektu oraz datę z terminem wysłanym podczas przesyłania (z tolerancją zaokrąglenia wynoszącą jedną sekundę). Wygasły, nieważny lub skrócony termin nie jest uznawany za zweryfikowany. Status informuje o losowo wybranym obiekcie, którego retencja została odczytana dla danej operacji przesyłania.

Brakujące lub uszkodzone pliki lokalne są zgłaszane jako błąd danego przebiegu i kursor pozostaje przed tym miejscem, dzięki czemu plik zostanie ponownie przetworzony podczas następnego przebiegu; pliki, punkty kontrolne i eksporty znajdujące się za nim są nadal kopiowane. Funkcja przywracania sprawdza wszystkie odniesienia do zachowanych plików pod kątem odszyfrowanych skrótów i zarejestrowanych rozmiarów. Identyczne, nakładające się segmenty dziennika pochodzące z przerwanych operacji przesyłania są deduplikowane; sprzeczne nakładania się są odrzucane. Punkty kontrolne utworzone podczas przesyłania są odkładane do momentu, aż objęte nimi zapisy dziennika zostaną skopiowane, dzięki czemu zakończony przebieg nie publikuje punktu kontrolnego przed odpowiadającym mu wpisem w dzienniku.

### Przesyłanie strumieniowe migawek eksportu

Eksporty strumieniowe wykorzystują stabilną migawkę odczytu bazy danych SQLite. Jej początek może być starszy niż aktualny dziennik na żywo w momencie zakończenia pobierania. Punkt kontrolny utworzony po tej migawce może prawidłowo wskazywać, że archiwum jest krótsze; należy porównać go z punktem kontrolnym znajdującym się w miejscu lub przed eksportowanym prefiksem, a nie z dowolnym późniejszym punktem kontrolnym.

## Przygotowanie RFC 3161 i weryfikacja odpowiedzi (0.2)

Tryb dowodowy (domyślnie wyłączony) wysyła wyłącznie skróty SHA-256 każdego podpisanego punktu kontrolnego do wymienionych instytucji zgodnych z RFC 3161 oraz kalendarzy OpenTimestamps, korzystając z trasy przestrzeni roboczej, a nigdy poprzez MTProxy. Odpowiedzi są przechowywane w `checkpoints/anchors/`, eksportowane i sprawdzane przez `verify.py` (`--tsa-ca` sprawdza podpis TSA; potwierdź dowody OpenTimestamps za pomocą `ots upgrade` i `ots verify`).

Panel przygotowuje archiwum żądań zawierające kanoniczne bajty pliku checkpoint.json, odcisk wiadomości SHA-256 oraz losowy nonce w pliku timestamp.tsq, sumy kontrolne oraz instrukcje. Nie są wysyłane żadne żądania sieciowe. Przygotowanie to nie stanowi zaufanego znacznika czasu.

`python -m tgwitness.anchor verify` wywołuje bibliotekę OpenSSL dwukrotnie: raz w odniesieniu do bajtów punktu kontrolnego i raz w odniesieniu do oryginalnego żądania. Wymagany jest wyraźnie wskazany plik zaufanego urzędu certyfikacji; załączone certyfikaty nie są automatycznie uznawane za zaufane. Sprawdzanie żądania jest opcjonalne w interfejsie CLI, dlatego należy zachować i podać opcję --request w celu sprawdzenia wartości nonce. Wynik wskazuje, czy sprawdzenie zostało przeprowadzone. Podpis punktu kontrolnego kolektora oraz dziennik muszą nadal zostać zweryfikowane osobno przy użyciu zaufanego odcisku palca kolektora.

Weryfikacja sprawdza podpis odpowiedzi, bajty punktu kontrolnego oraz, jeśli zostały dostarczone, oryginalne żądanie w ramach określonego zaufania urzędu certyfikacji (CA). Sprawdzanie unieważnienia oraz długoterminowa walidacja archiwizacji po wygaśnięciu certyfikatu wykraczają poza zakres obecnego weryfikatora. Zobacz [procedurę](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/) i [wyniki walidacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/).

## Opcjonalne zapisy w trybie dowodowym: urządzenia typu drand i Telegram

Dwa dodatkowe zapisy mogą być generowane podczas tych samych operacji co znaczniki czasu. Oba są domyślnie wyłączone i działają tylko wtedy, gdy włączony jest tryb dowodowy: Dodatki → Dowody i kopie zapasowe → **Więcej świadków · opcjonalnie**, lub `"drand": true` oraz `"devices": true` w `POST /api/evidence`. Awaria jednego z nich nie zatrzymuje działania drugiego ani znaczników czasu; panel wyświetla najnowszy wynik każdego z nich pod formularzem.

**drand** (`beacon.drand` ). Każde przejście zapisuje najnowszą rundę drand quicknet, czyli publiczną losowość League of Entropy (runda co 3 sekundy), w dzienniku: `chain` , `round` , `randomness` , `signature` , `round_time` oraz `relay` , który udzielił odpowiedzi. Zweryfikowana nieprzewidywalna runda stanowi dolną granicę czasową dla kolejnych materiałów połączonych skrótami. Zweryfikowany znacznik czasu w późniejszym punkcie kontrolnym stanowi górny punkt odniesienia czasowego. Kontrole te ograniczają zakres połączonego materiału; zasięg zbioru jest oceniany oddzielnie. Kolektor wysyła zapytanie najpierw do `drand.cloudflare.com` , a następnie do przekaźników Protocol Labs, poprzez trasę obszaru roboczego, po jednym żądaniu na przejście.

`verify.py` sprawdza, czy każda wartość losowa jest zgodna z SHA-256 dla danego podpisu oraz czy czas rundy jest prawidłowy, a także zgłasza liczbę rund, najdłuższy okres bez rundy oraz to, jak bardzo zegar kolektora opóźniał się względem drand. Nie sprawdza podpisu BLS. `--check-drand` porównuje rundy z przekaźnikiem Cloudflare i przekaźnikiem Protocol Labs, ze wszystkimi z nich lub z losową próbką 100 z długiego dziennika; runda, która się różni, nie przechodzi weryfikacji.

Urządzenia **, Telegram,** (`account.devices`). Każdy przebieg odczytuje sesje konta o numerze `account.getAuthorizations`, a lista Telegram wyświetlana w Ustawieniach → Urządzenia, i rejestruje je: w całości, jeśli uległa zmianie od poprzedniego przebiegu, wraz z skrótami sesji `added` i `removed`, w przeciwnym razie tylko jej liczbę i SHA-256. Zachowywane są model urządzenia, platforma, aplikacja i wersja, data utworzenia i ostatniej aktywności, kraj oraz region; adresy IP nie są zachowywane, ponieważ eksportowane dowody opuszczają Twoje ręce. Własna sesja kolektora jest aktywna przez cały czas, więc tylko aktywność innych sesji liczy się jako zmiana. `verify.py` zgłasza, jak często lista została zarejestrowana, a także każdą nową i zakończoną sesję. Odczytuje listę tylko podczas trwania obserwacji.

Czego nie pokazują: drand potwierdza jedynie kolejność zapisów względem czasu publicznego, a lista urządzeń stanowi oświadczenie Telegram przekazane za pośrednictwem kolektora, podpisane przez kolektora tak jak każdy inny zapis.

**Dziennik Cloudflare Gateway** (`cloudflare.gateway_dns`). W przypadku serwera, który korzysta z bramy Cloudflare Gateway ([– Gateway DNS](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), każda kopia zawiera dane zarejestrowane przez bramę od momentu poprzedniej kopii: jeden wpis na okno trwające maksymalnie trzy godziny z `from`, `until`, `location_id`, `address` serwera (jeśli jest ustawiony) oraz `queries` jako `[at, name, type, rcode, decision, colo]`, również w przypadku braku wpisów. Należy to ustawić w **(dziennik Cloudflare Gateway)**: konto, lokalizacja, opcjonalny adres oraz token tylko do odczytu (odczyt danych analitycznych konta Analytics Read; Zero Trust PII Read, aby zachować jeden adres wspólnej lokalizacji). Panel sprawdza je za pomocą jednego żądania przed zapisaniem; token pozostaje zaszyfrowany i nigdy nie trafia do dziennika. `verify.py` zawiera listę okien, najczęściej wyszukiwanych nazw oraz wszelkich okresów, których nie obejmuje żadna kopia; rekord, którego liczba nie zgadza się z liczbą zapytań, kończy się niepowodzeniem. Okno, które zawiera więcej niż jedną stronę zapytań w ciągu jednej sekundy, zachowuje tę stronę i informuje, że reszta brakuje. Kopia jest odpowiedzią Cloudflare przesłaną przez kolektor, podpisaną przez kolektor; w ciągu 24 godzin każdy, kto posiada token tylko do odczytu, może porównać ją z danymi Cloudflare.
