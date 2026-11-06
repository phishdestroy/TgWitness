# Co zostało przetestowane

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/

Test na żywo w serwisie Telegram, automatyczne kontrole, kontrole w przeglądarce oraz elementy, które pozostają niezweryfikowane.

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Wdrożenie w chmurze Phala Cloud · 4 listopada 2026 r.

`--provider phala --quick-tunnel` uruchomiono na rzeczywistym **Phala Cloud** (`tdx.small`, region US-WEST-1) przy użyciu klucza API Phala Cloud dla pustego obszaru roboczego, rzeczywistego pliku ntfy.sh, serwisu GitHub oraz Intel PCS. W maszynie wirtualnej CVM zainstalowano commit `df7d860c` (wersja 0.8.1); operacje wdrożenia, weryfikacji i usunięcia przeprowadzono z wiersza poleceń z wykorzystaniem poniższych poprawek. Koszt siedmiu maszyn wirtualnych CVM wyniósł łącznie około 1,9 centa amerykańskiego.

Pierwsze dwa wdrożenia wykazały pięć różnic w stosunku do symulowanej chmury Phala. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) odtwarza obecnie każdą z nich i kończy się niepowodzeniem bez odpowiedniej poprawki:

| W Phala Cloud | Przed wprowadzeniem poprawki | Poprawka |
| --- | --- | --- |
| Wymagany jest `compose_file.name` | HTTP 422, nic nie zostało utworzone | Konfiguracja Docker Compose zawiera nazwę CVM |
| O ile nie podano pustej wartości, Phala dodaje własny skrypt przed uruchomieniem do mierzonego pliku app-compose (wersja 0.0.20: logowanie do Docker, `docker compose pull`, hasło użytkownika root, klucze SSH z `user_config`) | Błąd `tdx_compose`: kod wykracza poza opublikowaną konfigurację Docker Compose | Plik app-compose ustawia `pre_launch_script` na `""`; Phala następnie pomija tę wartość |
| W przypadku braku opcji `image` platforma Phala wybiera opcję `dstack-dev-0.5.12`, czyli wersję deweloperską, z włączonym dostępem SSH | `server_state` nie przeszedł testu. W przypadku tego obrazu pozytywnie przeszedł jedynie zapis poświadczenia sprzętowego; widać to wyłącznie w zapisie dostawcy oraz w `tdx_os` | Wdrożenie wymaga użycia wersji produkcyjnej aktualnego wydania platformy Phala, oznaczonej jako `dstack-0.5.12` |
| Przy wyłączonej bramie dstack w szczegółach CVM nigdy nie pojawia się kod `instance_id` | Wdrożenie czeka 30 minut i kończy się niepowodzeniem | Identyfikator instancji jest odczytywany ze stanu CVM |
| Ponowne uruchomienia, zatrzymania i uruchomienia są operacjami na maszynie CVM, a nie aktualizacjami aplikacji | W `provider_actions` nie odnotowano żadnych ponownych uruchomień | Operacje te są również odczytywane |

Trzecie wdrożenie:

- Maszyna wirtualna CVM uruchomiła instancję `dstack-0.5.12` z wyłączonym dostępem SSH. Moduł zbierający opublikował swój podpisany adres około 1,5 minuty po utworzeniu. Wdrożenie przeszło następnie instancje `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, rekord poświadczenia sprzętowego v4, FMSPC `20a06f000000`, bez trybu debugowania, bez możliwości migracji, obsługujący dane weryfikacji kryptograficznej pobrane z Intel), `tdx_compose_hash`, `tdx_compose` (bajt po bajcie) oraz `tdx_identity` (klucze KMS).
- Panel pod adresem trycloudflare.com zwracał kod 401 bez tokenu lub przy podaniu nieprawidłowego tokenu, a kod 200 przy podaniu tokenu panelu.
- `verify` z `--source` ustawionym na archiwum GitHubu dla danego commitu oraz odciskiem palca przekazanym osobno: serwer, `server_state`, zapora sieciowa (bez bramy, bez publicznego punktu końcowego), log dostawcy, wyciąg, odcisk palca, skrót źródła, uruchomienie oraz pięć testów `tdx_*` zakończyło się powodzeniem. Usługi Cloudflare oraz `tdx_os` były niedostępne, w związku z czym wynik był NIEKOMPLETNY.
- Dwa ponowne uruchomienia za pośrednictwem interfejsu API Phala: za każdym razem maszyna CVM wracała do działania w czasie krótszym niż dwie minuty z tym samym kluczem kolektora, nowym podpisanym adresem oraz starym adresem zwracającym kod 530. `verify` zgłosił nowe uruchomienie oraz oba ponowne uruchomienia jako REVIEW. W przypadku `--evidence` potwierdzono podpisy dziennika oraz trzy uruchomienia, z których każde posiadało własny rekord poświadczenia sprzętowego Intel TDX pochodzący z tego samego CVM.
- Komenda `destroy` usunęła wyłącznie tę instancję CVM. Obszar roboczy był wówczas pusty, a adres panelu przestał odpowiadać.
- W panelu kreatora cena wyświetlała się jako `tdx.small` za 0,058 USD za godzinę. W przypadku podania nieprawidłowego klucza pojawiał się prosty komunikat „nie zaakceptowano klucza API”.

Dwie dodatkowe nieprawidłowości, które zostały następnie usunięte:

- Bez klucza adresu `verify` kierował się najnowszym, poprawnie sformułowanym wpisem dotyczącym tematu adresu, który jest zamieszczony w opublikowanej konfiguracji Docker Compose. Jeden sfałszowany wpis skierował go do hosta, który nie istnieje, a `statement` zakończył się niepowodzeniem: fałszerz nie mógł podać się za kolektor, ale mógł zablokować weryfikację zewnętrzną na okres do 12 godzin za pomocą sfałszowanego znacznika czasu przyszłego. Kolektor obecnie publikuje również swój adres podpisany własnym kluczem; `verify` akceptuje wyłącznie takie wpisy, gdy pochodzą one od kolektora, a wpisy są porządkowane według czasu odbioru przez ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) odtwarza sfałszowane wpisy. CVM uruchamia to wyłącznie z poziomu commit’u, który je zawiera, więc kolektor tego uruchomienia nie podpisał jeszcze swojego adresu, o czym poinformował `verify`.
- `tdx_os` nie mógł działać bez `dstack-mr`, którego aktualna wersja to `measure-os`, a nie `measure --json`, jak podano w dokumentacji. Weryfikator oblicza teraz samodzielnie wartości MRTD i RTMR0-2 na podstawie opublikowanego obrazu oraz struktury maszyny wirtualnej, z uwzględnieniem tabel ACPI.

Czwarte wdrożenie, obejmujące następujące elementy:

- Deploy pobrał opublikowany plik `dstack-0.5.12` jednokrotnie, dopasował go do skrótu obrazu systemu operacyjnego zgłoszonego przez maszynę CVM , a plik `tdx_os` przeszedł test: wartości MRTD, RTMR0, RTMR1 i RTMR2 są równe wartościom obliczonym dla QEMU 8.2.2, 1 vCPU i 2 GiB. To samo obliczenie dało inną wartość RTMR0 w przypadku deklarowanych 4 GiB, 2 vCPU, QEMU 9.2.1 lub drugiej karty sieciowej, a także zakończyło się niepowodzeniem w przypadku zmienionego jądra, oprogramowania układowego lub wiersza poleceń oraz w przypadku obrazu deweloperskiego.
- `verify` przeszedł pomyślnie wszystkie 16 testów, w tym test złącza szybkiego tunelu, więc wynik brzmiał: ZALICZONO. System wygenerował certyfikat w formacie HTML i PDF, opatrzony pieczęciami cyfrowymi w postaci podpisów i znaczników czasu, w tym kwalifikowanym znacznikiem czasu eIDAS pochodzącym z rządowej jednostki znaczników czasu TSU 202301 (status przyznany na belgijskiej liście zaufanych podmiotów), znacznikiem czasu FreeTSA oraz podpisem weryfikatora; `check-report` potwierdził wszystkie te elementy oraz podpis pliku PDF.
- Po ponownym uruchomieniu `verify --evidence` potwierdził dwa uruchomienia, z których każdemu towarzyszyło poświadczenie sprzętowe wygenerowane wewnątrz CVM, a każde z nich zostało uruchomione z opublikowanego `dstack-0.5.12`; zarówno ponowne uruchomienie, jak i nowe uruchomienie miały status REVIEW.
- `destroy` pozostawił obszar roboczy pusty.

W ramach piątego wdrożenia uruchomiono kolektor z commitem `53a0f7e9`, który zawiera wszystkie powyższe elementy:

- Kolektor opublikował swój adres podpisany własnym kluczem obok wpisu operatora z kodem HMAC. Następnie do wątku dodano dwa sfałszowane wpisy: jeden z kodem HMAC o wartości zerowej, a drugi podpisany innym kluczem Ed25519; oba podawały datę z roku 2096. `verify` przejął adres podpisany kluczem kolektora i przeszedł wszystkie 16 testów; pieczęć ponownie zawierała kwalifikowany belgijski znacznik czasu, znacznik czasu FreeTSA oraz podpis weryfikatora, a `check-report` potwierdził ich autentyczność.
- Po ponownym uruchomieniu kolektor opublikował nowy adres z podpisem: `verify` od razu go wykrył, operator **„Znajdź aktualny adres”** 27 sekund później na podstawie wpisu HMAC, a obaj zignorowali sfałszowane wpisy. `verify --evidence` potwierdził dwa uruchomienia z `dstack-0.5.12`.
- Wdrożenie wyświetliło kwotę, jaką Phala nalicza za CVM, łącznie z dyskiem: 0,06078 USD za godzinę.

Kreator panelu został uruchomiony w usłudze Phala Cloud dwukrotnie: raz za pośrednictwem interfejsu API zadań, a raz za pośrednictwem przeglądarki opartej na prawdziwym silniku Chromium: sprawdzenie ceny, utworzenie z zatwierdzeniem pod nazwą **Advanced**, wszystkie sześć kontroli poświadczeń zakończyło się powodzeniem, lista serwerów wyświetlała cenę do rozliczenia (44,37 USD miesięcznie), **Find aktualny adres**, pobranie zmierzonej konfiguracji Docker Compose oraz usunięcie. W przeglądarce nie odnotowano żadnych błędów wyświetlania stron. Za każdym razem obszar roboczy pozostawał następnie pusty.

Nie uwzględniono: domeny Cloudflare w sieci Phala, konta Telegram na maszynie CVM oraz obrazu `dstack-0.6.1` . Cena podana przez kreatora przed utworzeniem obejmuje wyłącznie koszt obliczeniowy w sieci Phala, ponieważ API tej sieci podaje koszt dysku tylko dla istniejącej maszyny CVM; lista serwerów przedstawia cenę rozliczeniową po utworzeniu.

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

## Wyszukiwanie pełnotekstowe w milionie wiadomości · 5 listopada 2026 r.

Polecenie: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Deterministyczny, podpisany dziennik zawierający 1 000 000 syntetycznych wiadomości w 200 czatach (rosyjskie formy słów, ukraiński, angielski, chiński, japoński, linki i identyfikatory) został zindeksowany w 71 sekund; indeks zajął 58 MiB oprócz dziennika o wielkości 1,50 GiB. Wyszukiwanie najlepszego dopasowania trwało od 9 do 190 ms (mediana), w porównaniu z 2,4–3,2 sekundy w przypadku poprzedniego wyszukiwania podciągu . Pełne wyniki, sprzęt i ograniczenia: [Wyszukiwanie pełnotekstowe](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#benchmark). `tools/test_fulltext.py` weryfikuje również podpisane archiwum utworzone przed wyszukiwaniem pełnotekstowym (`tools/fixtures/evidence-before-fulltext.zip`) za pomocą aktualnego weryfikatora oraz aktualny archiwum przy użyciu własnego archiwum `verify.py`.

## Pozostałe informacje

Zachowany dziennik na żywo dokumentuje faktyczne zdarzenia związane z gromadzeniem danych, edycjami, powiadomieniami o usunięciu, załącznikami, ponownymi weryfikacjami oraz obsługą ograniczeń szybkości. Nie obejmuje on jednak wyczerpujących danych dotyczących dostarczenia ani kontrolowanej matrycy widoczności ról, podmiotów reagujących, przedłużonego czasu oczekiwania (FloodWait), blokad kont oraz przywracania działania po przerwach w sieci lub procesach. Wydawanie tokenów QR pozostaje odrębne od zakończonego procesu potwierdzenia za pomocą mobilnego kodu QR.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

Szczegółowe lokalne zrzuty ekranu i kopie wiadomości znajdują się w katalogu test-results/ (ignorowanym przez Git). Publiczny zrzut ekranu w katalogu docs/assets/ zawiera wyłącznie fikcyjne dane demonstracyjne.
