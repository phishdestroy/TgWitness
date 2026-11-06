# Co zostało przetestowane

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/

Test na żywo w serwisie Telegram, automatyczne kontrole, kontrole w przeglądarce oraz elementy, które pozostają niezweryfikowane.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dowody i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

![Dowody i weryfikacja](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Zaktualizowano 6 listopada 2026 r.** Wyniki są powiązane z wersją, środowiskiem i obciążeniem zarejestrowanym dla każdego uruchomienia. Sekcja [Aktualne możliwości](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) opisuje dostępne przepływy pracy; na tej stronie odnotowano, co faktycznie zostało sprawdzone.

[Wykresy wydajności](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Audyt języka angielskiego z podpisem](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Pomiary do pobrania](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Najnowsze dowody | Wynik | Zakres |
| --- | --- | --- |
| Audyt wydania · 6, listopad | Testy rdzenia 1,461 zakończone sukcesem; pominięto testy platformy 37 | Źródło `92e539af40d8`; zachowano otwarte ustalenia |
| Najnowsze eksporty · 6 listopada | 127.713 i 141.781 rekordów na sekundę, pełny cykl | Dwa konta na serwer; tekst i metadane przesyłane przez WARP |
| Zachowane archiwa · 6 listopada | Archiwa 48; rekordy 3,598,381 zweryfikowane | Istniejące archiwa zostały zweryfikowane względem przypiętych kluczy obszaru roboczego |
| Trusted Live · 5 listopada | Zabezpieczone rejestrowanie aktywności procesora i kontrole WARP | Oficjalne logowanie w wersji desktopowej oraz natywny eksport pozostają bez zastrzeżeń |
| Phala / Intel TDX · 4 listopada | Wszystkie testy weryfikatora 16 zostały zaliczone w późniejszych przebiegach | Wdrożenie historyczne; brak konta Telegram na CVM |

**Na tej stronie**

- [Audyt wydania i nowe eksporty · 6 listopada 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Zaufane środowisko Live CPU Ubuntu i WARP · 5 listopada 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Wdrożenie Phala Cloud na żywo · 4 listopada 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Aktualny spis dzienników serwerów · 1 listopada 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Ostatnie kontrole w trybie offline i z symulacją błędów · 1 listopada 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Test Telegrama na żywo, całe konto · 29 października 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Eksport chroniony hasłem, otwierany za pomocą libarchive · 29 października 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Test Telegramu na żywo · 27–29 października 2026 r.](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Syntetyczny pomiar pojemności lokalnej](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Wyszukiwanie pełnotekstowe w milionie wiadomości · 5 listopada 2026](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Pozostałe wymagania](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/#remaining-qualification)

## Audyt wydania i nowe eksporty · 6 listopada 2026

W audycie wykorzystano wersję v0.9.1 w źródle `92e539af40d8368d198ff5e040f1d876f2c1310e`, wydanie `92e539af40d8-83e41104669e`. Testy sprawdzające zainstalowane pakiety zakończyły się powodzeniem na trzech serwerach. Podpisany raport odzwierciedla stan zaobserwowany w tym czasie.

[![Wskaźniki pozyskiwania i pełnego eksportu dla dwóch nowych obciążeń roboczych](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Zakres prac | Rejestruje | Pozyskiwanie | Pełny cykl | Współczynnik pełnego cyklu |
| --- | --- | --- | --- | --- |
| Serwer A · dwa konta | 27,030 | 189.043 s | 211.647 s | 127.713 zapisów/s |
| Serwer B · dwa konta | 29,299 | 182.513 s | 206.650 s | 141.781 zapisów/s |

Oba eksporty rozpoczęły się bez wznowienia, z wyłączeniem załączników i awatarów, a zakończyły się brakiem zduplikowanych lub ponownie wykorzystanych rekordów. Pełny cykl obejmuje przygotowanie, pozyskiwanie, selekcję, pakowanie i weryfikację archiwum. Serwer A przeprowadził również kontrolę odczytu chronionych czatów. Cztery zdarzenia typu FloodWait na serwerze A i trzy na serwerze B zostały uwzględnione. Obserwacje te nie stanowią ogólnej gwarancji przepustowości.

| Sprawdź | Wynik | Kwalifikacje |
| --- | --- | --- |
| Podstawowy pytest | 1,461: test zakończony sukcesem | Pominięcia na platformie 37 |
| Przeglądarka / doświadczenie użytkownika w przeglądarce / dowody / strona internetowa | 102 / 66 / 15 / 9 zaliczone | Programy te pokrywają się z innymi testami; wyniki nie sumują się |
| Dodatek Capture | 124: test zakończony sukcesem | Trzy oficjalne kontrole internetowe zablokowane przez wymaganą piaskownicę Chromium |
| Autoryzacja API | Trasy 269; żądania 538 przekazane | Brakujące dane uwierzytelniające i cofnięty dostęp |
| Zachowane archiwa | 48 z 48 zweryfikowano | Rekordy 3,598,381; przypięte klucze obszaru roboczego |
| Sprawdzanie odczytów floty na żywo | Zdał profil 24 z 40 | Trasy WARP 16 nie przeszły kwalifikacji; profile te nie zostały połączone |

Raport [z podpisem](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) rejestruje wszystkie otwarte ustalenia, w tym trzy usterki w nieopublikowanej migawce z tajnej rozmowy, której nie ma w skontrolowanej głównej kompilacji. Wcześniejsza [kwalifikacja historii publicznej](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) wykorzystywała inną wersję i obciążenie; jej wskaźników nie wolno łączyć z niniejszym porównaniem.

Zweryfikuj oryginalny raport przy użyciu klucza [pinned oraz weryfikatora](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Jego podpis chroni raport operatora przed zmianami. Nie stanowi to niezależnego poświadczenia, dowodu autorstwa w Telegramie ani certyfikacji zgodności z RODO.

## Zaufane środowisko Live CPU Ubuntu i WARP · 5 listopada 2026

W zachowanym przebiegu integracji wykorzystano gościa Ubuntu 24.04.5 działającego wyłącznie na procesorze (4 vCPU, 8 GiB) w środowisku QEMU wewnątrz hosta RunPod CPU. Kolektor korzystał z `14e642a5`; weryfikacja z `02072461`. Ostateczne poprawki zostały scalone w [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) jako `755f78f6`, którego drzewo kodu odpowiadało testowanej główce PR. Nie było to środowisko TEE.

- Prawdziwy moduł WARP Connector zgłosił prawidłowe działanie; proxy HTTPS zgłosiło, że WARP i Gateway są włączone. Trzy sondy wykryły ten sam adres wyjściowy, co nie gwarantuje stałego adresu IP.
- Odłączenie WARP spowodowało niepowodzenie żądania przesyłanego przez serwer proxy. Bezpośrednie połączenie HTTPS z usługą bramy zostało odrzucone. W przestrzeni nazw rejestratora zablokowano bezpośrednie adresy IPv4/IPv6, zewnętrzny DNS oraz wbudowany resolver UDP platformy Docker.
- Token dostawcy z ograniczonym zakresem dostępu, przeznaczony wyłącznie do odczytu, mógł odczytywać informacje o stanie i połączeniach, ale nie mógł odczytać tokenu rejestracji łącznika. Podpisane obserwacje dostawcy zawierały wyraźnie zaznaczone niedostępne próbki. Świadek działał na hoście operatora, co świadczy o rejestrowaniu i przechowywaniu danych, a nie o niezależnym przechowywaniu przez stronę trzecią.
- Program Official Desktop wyświetlił ekran powitalny bez uwierzytelnienia. Chronione dane wprowadzane z klawiatury zostały odrzucone podczas przechwytywania. Zdekodowano trzy segmenty wyświetlacza H.264 i sprawdzono nakładkę zegara. Archiwum wstępnej weryfikacji zdarzenia 18 zostało zweryfikowane w oparciu o przypięty klucz rejestratora i zachowany punkt kontrolny.
- Końcowe testy przechwytywania przeszły pomyślnie przypadki 114 w środowisku CI na systemach Windows i Linux, z wykorzystaniem rzeczywistych bibliotek Chromium/FFmpeg. Pięć testów kotwicowych oraz kontrole zaleceń dotyczących zależności zakończyły się powodzeniem.

Wstępny uruchomienie w trybie 2 vCPU/4 GiB zakończyło się przekroczeniem limitu czasu przy równoczesnym obciążeniu związanym z tworzeniem obrazu i zostało zatrzymane przez mechanizm zabezpieczający; nie jest to uznawane za sukces. Ręczne logowanie na konto testowe, eksport natywnego czatu, rzeczywiste porównanie hybrydowe oraz wylogowanie po stronie Telegrama pozostają w toku. Nie zaimportowano żadnej dostarczonej sesji Telethon. Załączniki, automatyczne OCR, lokalna weryfikacja drand BLS oraz poświadczenie Trusted Live TDX nie zostały zakwalifikowane.

## Wdrożenie w chmurze Phala Cloud · 4 listopada 2026 r.

**Wynik historyczny: późniejsze wdrożenia** przeszły wszystkie kontrole weryfikatora 16, w tym Intel TDX i szybki tunel. Dowody ponownego uruchomienia, wykrywanie podpisanych adresów oraz sygnatury czasowe raportów zostały sprawdzone oddzielnie. Każdy testowy moduł CVM był usuwany po zakończeniu działania.

| Konfiguracja | Zarejestrowana wartość |
| --- | --- |
| Dostawca | Phala Cloud · `tdx.small` · US-WEST-1 |
| Wdrożenie | `--provider phala --quick-tunnel`; początkowo pusty obszar roboczy |
| Początkowy moduł zbierający dane | `df7d860c` · v0.8.1 |
| Kolekcja zawierająca wszystkie poprawki | `53a0f7e9` |
| Gość produkcyjny | `dstack-0.5.12`; dostęp przez SSH wyłączony |
| Usługi zewnętrzne | ntfy.sh, GitHub i Intel PCS |
| Zaobserwowany koszt | Siedem CVM o łącznej wartości około 1.9 centów amerykańskich; historyczne ceny testowe |

Poniższa sekwencja rozróżnia początkowe błędy, poprawki i zakończone kontrole. Żadne konto Telegram nie było połączone z tymi modułami CVM.

**Wdrożenia 1–2 · różnice między dostawcami i testy regresji**

Pierwsze dwa wdrożenia wykazały pięć różnic w stosunku do symulowanej chmury Phala. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) odtwarza obecnie każdą z nich i kończy się niepowodzeniem bez odpowiedniej poprawki:

| W Phala Cloud | Przed wprowadzeniem poprawki | Poprawka |
| --- | --- | --- |
| Wymagany jest `compose_file.name` | HTTP 422, nic nie zostało utworzone | Konfiguracja Docker Compose zawiera nazwę CVM |
| O ile nie podano pustej wartości, Phala dodaje własny skrypt przed uruchomieniem do mierzonego pliku app-compose (wersja 0.0.20: logowanie do Docker, `docker compose pull`, hasło użytkownika root, klucze SSH z `user_config`) | Błąd `tdx_compose`: kod wykracza poza opublikowaną konfigurację Docker Compose | Plik app-compose ustawia `pre_launch_script` na `""`; Phala następnie pomija tę wartość |
| W przypadku braku opcji `image` platforma Phala wybiera opcję `dstack-dev-0.5.12`, czyli wersję deweloperską, z włączonym dostępem SSH | `server_state` nie przeszedł testu. W przypadku tego obrazu pozytywnie przeszedł jedynie zapis poświadczenia sprzętowego; widać to wyłącznie w zapisie dostawcy oraz w `tdx_os` | Wdrożenie wymaga użycia wersji produkcyjnej aktualnego wydania platformy Phala, oznaczonej jako `dstack-0.5.12` |
| Przy wyłączonej bramie dstack w szczegółach CVM nigdy nie pojawia się kod `instance_id` | Wdrożenie czeka 30 minut i kończy się niepowodzeniem | Identyfikator instancji jest odczytywany ze stanu CVM |
| Ponowne uruchomienia, zatrzymania i uruchomienia są operacjami na maszynie CVM, a nie aktualizacjami aplikacji | W `provider_actions` nie odnotowano żadnych ponownych uruchomień | Operacje te są również odczytywane |

**Wdrożenie 3 · poświadczenie, kontrole dostępu i dowody ponownego uruchomienia**

- Maszyna wirtualna CVM uruchomiła instancję `dstack-0.5.12` z wyłączonym dostępem SSH. Moduł zbierający opublikował swój podpisany adres około 1,5 minuty po utworzeniu. Wdrożenie przeszło następnie instancje `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, rekord poświadczenia sprzętowego v4, FMSPC `20a06f000000`, bez trybu debugowania, bez możliwości migracji, obsługujący dane weryfikacji kryptograficznej pobrane z Intel), `tdx_compose_hash`, `tdx_compose` (bajt po bajcie) oraz `tdx_identity` (klucze KMS).
- Panel pod adresem trycloudflare.com zwracał kod 401 bez tokenu lub przy podaniu nieprawidłowego tokenu, a kod 200 przy podaniu tokenu panelu.
- `verify` z `--source` ustawionym na archiwum GitHubu dla danego commitu oraz odciskiem palca przekazanym osobno: serwer, `server_state`, zapora sieciowa (bez bramy, bez publicznego punktu końcowego), log dostawcy, wyciąg, odcisk palca, skrót źródła, uruchomienie oraz pięć testów `tdx_*` zakończyło się powodzeniem. Usługi Cloudflare oraz `tdx_os` były niedostępne, w związku z czym wynik był NIEKOMPLETNY.
- Dwa ponowne uruchomienia za pośrednictwem interfejsu API Phala: za każdym razem maszyna CVM wracała do działania w czasie krótszym niż dwie minuty z tym samym kluczem kolektora, nowym podpisanym adresem oraz starym adresem zwracającym kod 530. `verify` zgłosił nowe uruchomienie oraz oba ponowne uruchomienia jako REVIEW. W przypadku `--evidence` potwierdzono podpisy dziennika oraz trzy uruchomienia, z których każde posiadało własny rekord poświadczenia sprzętowego Intel TDX pochodzący z tego samego CVM.
- Komenda `destroy` usunęła wyłącznie tę instancję CVM. Obszar roboczy był wówczas pusty, a adres panelu przestał odpowiadać.
- W panelu kreatora cena wyświetlała się jako `tdx.small` za 0,058 USD za godzinę. W przypadku podania nieprawidłowego klucza pojawiał się prosty komunikat „nie zaakceptowano klucza API”.

**Kolejne poprawki · wykrywanie adresów podpisanych oraz pomiary systemu operacyjnego**

- Bez klucza adresu `verify` kierował się najnowszym, poprawnie sformułowanym wpisem dotyczącym tematu adresu, który jest zamieszczony w opublikowanej konfiguracji Docker Compose. Jeden sfałszowany wpis skierował go do hosta, który nie istnieje, a `statement` zakończył się niepowodzeniem: fałszerz nie mógł podać się za kolektor, ale mógł zablokować weryfikację zewnętrzną na okres do 12 godzin za pomocą sfałszowanego znacznika czasu przyszłego. Kolektor obecnie publikuje również swój adres podpisany własnym kluczem; `verify` akceptuje wyłącznie takie wpisy, gdy pochodzą one od kolektora, a wpisy są porządkowane według czasu odbioru przez ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) odtwarza sfałszowane wpisy. CVM uruchamia to wyłącznie z poziomu commit’u, który je zawiera, więc kolektor tego uruchomienia nie podpisał jeszcze swojego adresu, o czym poinformował `verify`.
- `tdx_os` nie mógł działać bez `dstack-mr`, którego aktualna wersja to `measure-os`, a nie `measure --json`, jak podano w dokumentacji. Weryfikator oblicza teraz samodzielnie wartości MRTD i RTMR0-2 na podstawie opublikowanego obrazu oraz struktury maszyny wirtualnej, z uwzględnieniem tabel ACPI.

**Wdrożenie 4 · wszystkie kontrole 16, pieczęcie raportów i weryfikacja ponownego uruchomienia**

- Deploy pobrał opublikowany plik `dstack-0.5.12` jednokrotnie, dopasował go do skrótu obrazu systemu operacyjnego zgłoszonego przez maszynę CVM , a plik `tdx_os` przeszedł test: wartości MRTD, RTMR0, RTMR1 i RTMR2 są równe wartościom obliczonym dla QEMU 8.2.2, 1 vCPU i 2 GiB. To samo obliczenie dało inną wartość RTMR0 w przypadku deklarowanych 4 GiB, 2 vCPU, QEMU 9.2.1 lub drugiej karty sieciowej, a także zakończyło się niepowodzeniem w przypadku zmienionego jądra, oprogramowania układowego lub wiersza poleceń oraz w przypadku obrazu deweloperskiego.
- `verify` przeszedł pomyślnie wszystkie 16 testów, w tym test złącza szybkiego tunelu, więc wynik brzmiał: ZALICZONO. System wygenerował certyfikat w formacie HTML i PDF, opatrzony pieczęciami cyfrowymi w postaci podpisów i znaczników czasu, w tym kwalifikowanym znacznikiem czasu eIDAS pochodzącym z rządowej jednostki znaczników czasu TSU 202301 (status przyznany na belgijskiej liście zaufanych podmiotów), znacznikiem czasu FreeTSA oraz podpisem weryfikatora; `check-report` potwierdził wszystkie te elementy oraz podpis pliku PDF.
- Po ponownym uruchomieniu `verify --evidence` potwierdził dwa uruchomienia, z których każdemu towarzyszyło poświadczenie sprzętowe wygenerowane wewnątrz CVM, a każde z nich zostało uruchomione z opublikowanego `dstack-0.5.12`; zarówno ponowne uruchomienie, jak i nowe uruchomienie miały status REVIEW.
- `destroy` pozostawił obszar roboczy pusty.

**Wdrożenie 5 · wykrywanie podpisanych przez kolektora i odrzucanie sfałszowanych wpisów**

Kolektor działał od wersji `53a0f7e9`, która zawiera powyższe poprawki.

- Kolektor opublikował swój adres podpisany własnym kluczem obok wpisu operatora z kodem HMAC. Następnie do wątku dodano dwa sfałszowane wpisy: jeden z kodem HMAC o wartości zerowej, a drugi podpisany innym kluczem Ed25519; oba podawały datę z roku 2096. `verify` przejął adres podpisany kluczem kolektora i przeszedł wszystkie 16 testów; pieczęć ponownie zawierała kwalifikowany belgijski znacznik czasu, znacznik czasu FreeTSA oraz podpis weryfikatora, a `check-report` potwierdził ich autentyczność.
- Po ponownym uruchomieniu kolektor opublikował nowy adres z podpisem: `verify` od razu go wykrył, operator **„Znajdź aktualny adres”** 27 sekund później na podstawie wpisu HMAC, a obaj zignorowali sfałszowane wpisy. `verify --evidence` potwierdził dwa uruchomienia z `dstack-0.5.12`.
- Wdrożenie wyświetliło kwotę, jaką Phala nalicza za CVM, łącznie z dyskiem: 0,06078 USD za godzinę.

### Kreator paneli i pozostały zakres

Kreator panelu został uruchomiony w usłudze Phala Cloud dwukrotnie: raz za pośrednictwem interfejsu API zadań, a raz za pośrednictwem przeglądarki opartej na prawdziwym silniku Chromium: sprawdzenie ceny, utworzenie z zatwierdzeniem pod nazwą **Advanced**, wszystkie sześć kontroli poświadczeń zakończyło się powodzeniem, lista serwerów wyświetlała cenę do rozliczenia (44,37 USD miesięcznie), **Find aktualny adres**, pobranie zmierzonej konfiguracji Docker Compose oraz usunięcie. W przeglądarce nie odnotowano żadnych błędów wyświetlania stron. Za każdym razem obszar roboczy pozostawał następnie pusty.

Nie uwzględniono: domeny Cloudflare na platformie Phala, konta Telegram na CVM oraz obrazu `dstack-0.6.1`. Cena kreatora przed utworzeniem obejmuje wyłącznie koszt obliczeniowy platformy Phala, ponieważ jej API podaje cenę dysku tylko dla istniejącego CVM; lista serwerów pokazuje cenę rozliczeniową po utworzeniu. Wszystkie ceny w tej sekcji zostały odnotowane 4 listopada 2026 r.

## Aktualny spis dzienników serwerów · 1 listopada 2026

Około godziny 19:15 UTC sekwencyjne zapytania SQLite typu `query_only` (tylko do odczytu) zliczyły zdarzenia w dziesięciu bazach danych obszarów roboczych na działającym serwerze. Gromadzenie danych trwało podczas wykonywania zapytań, więc nie jest to atomowa migawka obejmująca wszystkie obszary robocze.

| Zaobserwowano w dziesięciu bazach danych obszarów roboczych | Liczba |
| --- | --- |
| Obszary robocze zawierające co najmniej jedno zdarzenie typu `message.new` | 8 |
| Zapisy dziennika, w tym zdarzenia operacyjne | 1,610,818 |
| Zdarzenia `message.new` | 900,232 |
| Zdarzenia `message.edited` | 80,683 |
| Zdarzenia `message.deleted` | 400,536 |
| Zdarzenia `message.recovered` | 53,403 |
| Zdarzenia `message.snapshot` | 2,183 |
| Zdarzenia `media.saved` | 50,418 |
| Zdarzenia `media.failed` | 5,575 |
| Zdarzenia `coverage.gap` | 11 |
| Bajty bazy danych, z wyłączeniem plików WAL i multimediów | 7,909,003,264 |

Są to **liczby zdarzeń**, a nie unikalne wiadomości, osoby ani pliki multimedialne. Ta sama wiadomość może pojawić się w więcej niż jednym obszarze roboczym, a edycja lub usunięcie może spowodować powstanie kolejnego zdarzenia w dzienniku. `media.failed` zlicza historyczne zdarzenia niepowodzeń, a nie bieżącą kolejkę multimediów. Zapytania **nie** obejmowały ponownej weryfikacji podpisów ani pełnego łańcucha skrótów wszystkich 1,610,818 rekordów, nie mierzyły dostarczalności ani przepustowości, ani nie potwierdzały, że każde zdarzenie z Telegrama zostało zarejestrowane. Nie publikuje się tutaj treści wiadomości, identyfikatorów kont ani czatów, etykiet obszarów roboczych, danych uwierzytelniających ani plików prywatnych.

W trakcie niniejszej analizy oddzielnie skonfigurowany monitor publiczny obejmował trzy źródła: jedna odpowiedź przechwytywania była w porządku, a dwie zgłaszały `no_response`. Monitor ten nie stanowi podsumowania stanu dziesięciu obszarów roboczych. `no_response` oznacza, że obserwator nie mógł uzyskać odpowiedzi podczas tej kontroli; nie oznacza to utraty wiadomości. Poniższy, mniejszy test z 29 października posiada własny wyraźny podpis oraz weryfikację łańcucha skrótów.

## Ostatnie kontrole w trybie offline i z symulacją błędów · 1 listopada 2026

Te testy wykorzystują fikcyjne dane i pliki lokalne; dostarczają one dowodów regresji dla bieżącego źródła, a nie dla innego rzeczywistego pomiaru dostarczalności w Telegramie:

| Sprawdź | Co zostało przetestowane |
| --- | --- |
| [Archiwum źródłowe](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Dwie kompilacje o identycznych bajtach źródłowych, ale ze zmienionymi datami plików, dały ten sam plik ZIP i tę samą sumę kontrolną. Dokładna liczba bajtów w archiwum i skróty plików były zgodne; prywatne pliki testowe pozostały poza archiwum. Symulowana awaria zapisu pozostawiła poprzednie archiwum i sumę kontrolną nienaruszone. |
| [Odzyskiwanie eksportu konta](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Symulowany błąd dysku na drugim elemencie archiwum ZIP spowodował brak opublikowanego lub częściowego archiwum ZIP. Funkcja wznowienia zachowała każdy podpisany potwierdzenie jako identyczny bajt po bajcie, wygenerowała niezależnie weryfikowalne archiwum przy użyciu oczekiwanego odcisku palca podpisu oraz zachowała syntetyczną lukę w pokryciu jako wynik częściowy. Twierdzenia dotyczące skali chronią przed powtarzającym się skanowaniem zadań i potwierdzeń w miarę powiększania się historii. |
| [Ochrona prywatności poprzez minimalizację ujawniania informacji](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Syntetyczne nazwy i aliasy Unicode, zagnieżdżone metadane, nieznani nadawcy oraz pola multimedialne zostały sprawdzone we wszystkich trzech trybach tożsamości oraz przy pominięciu tekstu. Niepowodzenie związane z limitem maskowania nie osłabiło w sposób niezauważalny redakcji; oryginalny, podpisany eksport konta pozostał niezmieniony. |
| [Dekoder multimediów dla systemu Linux i OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | [Sprawdzenie CI w środowisku Docker na systemie Linux](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) przy commitcie `5a9e0814` zakończyło się powodzeniem dla generowanych plików wejściowych w formatach Ogg/Opus, MP3, M4A, MP4 z wideo, WAV i FLAC; kontroli dotyczących sfałszowanego czasu trwania i odwołań do plików pomocniczych; oraz 48 zmodyfikowanych zestawów testowych parsera (34 odrzuconych, 14 zdekodowanych w granicach). Prawdziwe OCR Tesseract działało bez zmian w oryginalnych bajtach. Dekoder i OCR działały w kontenerach odizolowanych sieciowo bez modelu Whisper. |

Sprawdzanie odbywa się w ramach procesów [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) oraz [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml). Sprawdzają one te granice awarii, a nie każdą możliwą awarię pamięci masowej ani to, czy ujawnienie danych jest automatycznie bezpieczne do opublikowania. Sprawdzanie multimediów nie mierzy dokładności rozpoznawania mowy ani dostarczalności wiadomości w Telegramie. Przed udostępnieniem należy przejrzeć każdą pochodną.

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

Sprawdzenia Docker/Compose oraz instalacji są rejestrowane w CI; rzeczywiste wdrożenie Phala oraz weryfikacja zewnętrznych znaczników czasu zostały opisane powyżej. Nie zapewniają one trwałego wysokiego obciążenia, kompletnej macierzy platform/ról na żywo, niezależnego przeglądu bezpieczeństwa, długoterminowej walidacji archiwalnej ani certyfikacji kryminalistycznej. Zaimplementowano zapis stanu MTProto i nadrabianie zaległości; atomowe, bezstratne odtwarzanie na żywo pozostaje niewykonalne. Nowsza funkcja uzupełniania danych (backfill) zatwierdza komunikaty i kursory atomowo oraz zachowuje dostępne ostatnie działania, ale jej syntetyczny zasięg różni się od kwalifikacji na żywo. Zobacz [akceptacja na żywo](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md), aby zapoznać się z matrycą kwalifikacji kontrolowanej.

Katalog audytu publicznego  zawiera wyłącznie podpisany raport i zbiorcze pomiary. Szczegółowe potwierdzenia operacji, surowe zrzuty ekranu oraz materiały dotyczące kont pozostają prywatne. Zrzuty ekranu aplikacji w `docs/assets/` wykorzystują fikcyjne dane demonstracyjne.
