# Co zostało przetestowane

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/

Test na żywo w serwisie Telegram, automatyczne kontrole, kontrole w przeglądarce oraz elementy, które pozostają niezweryfikowane.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Liczba |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Sprawdź | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Test na żywo w serwisie Telegram, całe konto · 29 października 2026 r.

To samo konto nadal działało po przeprowadzeniu poniższego testu. 29 października o godz. 12:10 czasu UTC jego zakres został rozszerzony na całe konto (kanały, grupy, czaty prywatne i boty); panel poprosił o potwierdzenie, a podpisany dziennik to zarejestrował. O godz. 17:59 czasu UTC dziennik zawierał:

| Dane zarejestrowano w okresie od 27 października, godz. 21:36, do 29 października, godz. 17:59 czasu UTC | Liczba |
| --- | --- |
| Zapisy w dzienniku | 9,968 |
| Nowe wiadomości | 5,308 |
| z nich po przejściu na pełne konto | 3,878 |
| Usunięcia | 784 |
| z nich zostały usunięte po tym, jak TgWitness zapisało wiadomość | 596 |
| Edycje | 41 |
| Wiadomości dodane w wyniku ponownej weryfikacji | 2,273 |
| Wiadomości, których nie udało się odnaleźć podczas ponownej weryfikacji | 18 |
| Wiadomości zapisywane za pomocą migawek historii | 242 |
| Zapisane załączniki | 247 |
| Uruchomienie programu Collector | 19 |
| Funkcja „FloodWait” w Telegramie wstrzymuje działanie | 26 |

- W ramach kontroli **„Verify”** panelu potwierdzono podpisy oraz łańcuch skrótów wszystkich 9 968 rekordów.
- Wiadomości pochodziły z 2 grup lub kanałów oraz 3 prywatnych czatów i botów. Naciśnięto jeden przycisk wiadomości w **sekcji „Czaty”**; żądanie oraz odpowiedź serwisu Telegram znajdują się w dzienniku.
- Nowe czaty zostały dodane, gdy moduł zbierający ponownie przeskanował konto po ponownym uruchomieniu. Funkcja zapisywania wcześniejszych wiadomości z nowych czatów była wyłączona (`history = 0`), dlatego nie została tutaj uwzględniona.

Nie obejmuje: reakcji, zmian w składzie członków, profili użytkowników, wysyłania wiadomości, dołączania na zaproszenie, serwerów proxy, powiadomień, bota „witness” oraz korzystania z kilku kont jednocześnie. Pliki publiczne zawierają wyłącznie dane liczbowe.

## Plik eksportowy chroniony hasłem, otwierany za pomocą biblioteki libarchive · 29 października 2026 r.

Archiwum utworzone przy użyciu kodu szyfrowania eksportu (WinZip AES-256, format odczytywany przez programy 7-Zip i WinRAR ) zostało otwarte w systemie Windows za pomocą narzędzia `tar` (bsdtar 3.6.2, libarchive). Po wprowadzeniu prawidłowego hasła wyodrębniony plik wykazał zgodność z oryginalnym skrótem SHA-256; wprowadzenie nieprawidłowego hasła spowodowało komunikat „Nieprawidłowe hasło”. Same programy 7-Zip i WinRAR nie zostały uruchomione.

## Test na żywo w serwisie Telegram · 27–29 października 2026 r.

Jedno rzeczywiste konto w serwisie Telegram, zalogowane za pośrednictwem wbudowanej puli par API, rejestrowało dane z jednej supergrupy od **27 października, godz. 21:36 UTC do 29 października, godz. 05:15 UTC**. Moduł zbierający dane został uruchomiony 12 razy w tym okresie.

| Zarejestrowano | Liczba |
| --- | --- |
| Zapisy dziennika, w tym sygnały kontrolne i zapisy dotyczące działania usługi | 2,385 |
| Nowe wiadomości | 1,291 |
| Usunięcia | 472 |
| z nich zostały usunięte po tym, jak TgWitness zapisało treść | 347 |
| Edycje | 12 |
| Wiadomości pominięte w trakcie przerwy w działaniu, dodane podczas ponownej weryfikacji | 12 |
| Zapisane załączniki | 17 |
| Załączniki nie zostały pobrane (funkcja pobierania wyłączona lub brak pliku do pobrania) | 14 |
| Telegram FloodWait wstrzymuje działanie na 3 sekundy podczas ponownej weryfikacji | 8 |

- Podpisy oraz łańcuch skrótów wszystkich 2 385 wpisów można zweryfikować przy użyciu klucza publicznego dziennika.
- Po ponownym uruchomieniu moduł zbierający wznawia działanie od zapisanego stanu aktualizacji (`pts`), a Telethon nadrabia zaległości; następnie podczas ponownej weryfikacji dodawane są wiadomości, których wciąż brakuje.
- Przy każdym zdarzeniu typu „FloodWait” moduł zbierający dane odczekał żądany czas, a następnie kontynuował działanie.
- Konto pozostało zalogowane, a ta sama sesja została ponownie nawiązana 29 października.

Niniejszy test nie obejmuje następujących kwestii: obsługi wielu kont jednocześnie, ról administratora, serwerów proxy, przerw w działaniu trwających dłużej niż kilka godzin oraz pełnej [procedury akceptacji na żywo](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Pliki publiczne zawierają wyłącznie następujące dane: brak identyfikatorów kont lub czatów, wiadomości ani danych uwierzytelniających.

## Syntetyczny pomiar lokalnych możliwości

Polecenie: `python tools/check_capacity.py --events 10000 --chats 100`

| Metryka | Zaobserwowano |
| --- | --- |
| Dane wejściowe | 10 000 syntetycznych zdarzeń związanych z wiadomościami z 100 wybranych syntetycznych źródeł |
| Treść wiadomości | 400 znaków; bez multimediów ani odniesień do sieci |
| Przetwarzanie danych | 53,273 sekundy; 187,7 zdarzeń na sekundę |
| Opóźnienie obsługi | p50 4,162 ms; p95 7,784 ms; maksymalnie 129,118 ms |
| Eksport do pliku ZIP | 19,868 sekundy przy włączonej funkcji tracemalloc |
| Szczytowe wartości przydziałów eksportu w języku Python | 0,51 MiB; brak obsługi RSS |
| Rozmiar pliku ZIP | 4 610 962 bajtów |
| Niezależna weryfikacja | Wszystkie 10 000 zdarzeń zostało zweryfikowanych |

Niniejszy pomiar dotyczy lokalnej ścieżki zapisu/eksportu na tym hoście z systemem Windows. Nie obejmuje on dostarczania wiadomości za pośrednictwem protokołu MTProto, kont działających jednocześnie, ograniczeń przepustowości w serwisie Telegram, plików multimedialnych, długotrwałego obciążenia ani gwarantowanej liczby rzeczywistych czatów. Pomiar ten został przeprowadzony przed wprowadzeniem ostatecznej wersji narzędzia do generowania znaczników czasu w trybie offline, które nie zmienia mierzonej ścieżki wiadomości.

## Pozostałe informacje

Zachowany dziennik na żywo dokumentuje faktyczne zdarzenia związane z gromadzeniem danych, edycjami, powiadomieniami o usunięciu, załącznikami, ponownymi weryfikacjami oraz obsługą ograniczeń szybkości. Nie obejmuje on jednak wyczerpujących danych dotyczących dostarczenia ani kontrolowanej matrycy widoczności ról, podmiotów reagujących, przedłużonego czasu oczekiwania (FloodWait), blokad kont oraz przywracania działania po przerwach w sieci lub procesach. Wydawanie tokenów QR pozostaje odrębne od zakończonego procesu potwierdzenia za pomocą mobilnego kodu QR.

Kompilacja i uruchamianie w Dockerze, instalacja w systemach Linux/macOS, obsługa długotrwałego wysokiego obciążenia, niezależny przegląd bezpieczeństwa, rzeczywista niezależna reakcja TSA, weryfikacja unieważnienia certyfikatów i archiwizacji oraz certyfikacja kryminalistyczna pozostają poza zakresem niniejszej kwalifikacji. Zaimplementowano zapis stanu MTProto oraz funkcję nadrabiania zaległości; nie ustalono jeszcze możliwości atomowego, trwałego odtwarzania. Gromadzenie logów administracyjnych, dodatkowe listy reaktorów oraz priorytetowe krótkie odpytywanie pozostają odrębnymi funkcjami. Proszę zapoznać się z [aktualną wersją](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) matrycy kwalifikacji kontrolowanych.

Szczegółowe lokalne zrzuty ekranu i kopie wiadomości znajdują się w katalogu test-results/ (ignorowanym przez Git). Publiczny zrzut ekranu w katalogu docs/assets/ zawiera wyłącznie fikcyjne dane demonstracyjne.
