# Bezpieczeństwo i przetwarzanie danych

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/security/

Model zagrożeń, model dostępu, dane poufne w stanie spoczynku, narażenie sieciowe, import sesji oraz sposób zgłaszania luk w zabezpieczeniach.

TgWitness działa na Państwa własnym komputerze lub serwerze. Połączenia z kontami, prowadzenie publicznej listy serwerów proxy oraz opcjonalne usługi zewnętrzne podlegają jasno określonym zasadom routingu. Powiadomienia, sygnatury czasowe, kopie poza serwerem oraz świadek są konfigurowane oddzielnie. Na tej stronie wymieniono, co jest chronione, w jaki sposób oraz co pozostaje w gestii operatora.

| Obszar | W skrócie |
| --- | --- |
| Dostęp | Klucz administratora oraz dostęp o ograniczonym zakresie do kont i czatów, siedem uprawnień oraz sesje z możliwością cofnięcia; domyślnie localhost |
| Sekrety w stanie spoczynku | Sesja, para API, klucz podpisujący oraz ustawienia serwera proxy są szyfrowane za pomocą algorytmu Fernet |
| Wiadomości i pliki multimedialne | Dane przechowywane są w postaci niezaszyfrowanej: zaleca się stosowanie szyfrowania dysku oraz rygorystycznych uprawnień dostępu |
| Rzetelność | Łańcuch skrótów SHA-256 oraz podpis Ed25519 na każdym wpisie |
| Nieobjęte zakresem | Administrator urządzenia, ujawniony token panelu, kompletność przechwytywania |

W sprawie zgłoszeń luk w zabezpieczeniach prosimy zapoznać się z [polityką bezpieczeństwa](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Model dostępu

Token panelu głównego zapewnia pełną kontrolę. Inne osoby mogą otrzymać [dostęp o ograniczonym zakresie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/): wybrane obszary robocze i czaty, uprawnienia, termin ważności, ograniczenia adresów IP, limity logowań oraz sesje z możliwością cofnięcia. Użytkownik z dostępem ograniczonym do czatu nie może wykonywać operacji obejmujących cały obszar roboczy, nawet jeśli jego uprawnienie jest zaznaczone. Obszary robocze współdzielą proces i nie izolują danych od administratora serwera.

Panel domyślnie nasłuchuje na localhost. Logowanie w przeglądarce powoduje wymianę tokena dostępu na poświadczenie sesji; przeglądarka wysyła je jako token typu „bearer”. Jest ono przechowywane w pamięci sessionStorage, a nie w pliku cookie uwierzytelniającym. Zablokowanie lub wylogowanie powoduje wyczyszczenie sesji przeglądarki. Zamknięcie przeglądarki lub zakończenie sesji nie zatrzymuje gromadzenia danych.

Wydane tokeny i poświadczenia sesji są przechowywane w postaci skrótów w zaszyfrowanym skarbcu. Unieważnienie powoduje zakończenie powiązanych sesji; zmiany uprawnień mają wpływ na kolejne żądania. Pobranych plików nie można odzyskać. Administrator może również ograniczyć własne sesje przeglądarki, jednak skrypty wykorzystujące bezpośrednio token panelu głównego zachowują pełny dostęp i omijają te ograniczenia sesji przeglądarki.

Niepowodzenia uwierzytelniania podlegają ograniczeniom częstotliwości na podstawie adresu klienta. Ograniczenia adresów IP opierają się na adresie widocznym dla aplikacji; przed wykorzystaniem tej funkcji należy sprawdzić działanie serwera proxy odwrotnego. Dane uwierzytelniające Witness pozostają oddzielnymi danymi uwierzytelniającymi typu „read-only” służącymi do sprawdzania stanu i punktów kontrolnych.

### Dostęp do wersji demonstracyjnej

`/api/demo-access` to celowo nieautoryzowany bootstrap dla wyraźnie uruchomionego, izolowanego, syntetycznego środowiska demonstracyjnego. Generuje on oddzielną uprawnienie na czas trwania procesu, nigdy nie udostępnia prawdziwego tokenu panelu ani nie zastępuje tokenu TGWITNESS_TOKEN. Wydanie i wykorzystanie wymagają połączenia typu loopback oraz hosta, bez przekazywanych nagłówków i bez żądań międzydomenowych. Dodatkowe obszary robocze lub autoryzowana sesja uniemożliwiają tę ścieżkę. Aktywne obszary robocze nigdy nie wydają tego uprawnienia. Wersja demonstracyjna nie może łączyć kont ani zmieniać ustawień gromadzenia danych.

## Zawartość paneli i eksporty

Panel nie wykorzystuje żadnych zewnętrznych czcionek, narzędzi analitycznych, zasobów CDN ani osadzonych mediów zdalnych. Tekst pochodzący z Telegrama jest wstawiany jako zwykły tekst, a nie kod HTML. Pobrane załączniki są udostępniane jako załączniki binarne. Eksporty w formacie JSONL zachowują oryginalne ciągi znaków; kod HTML je zamienia; komórki plików CSV, które mogłyby stać się formułami, są poprzedzone apostrofem.

Eksportowane dane nie zawierają kluczy uwierzytelniających ani podpisujących, ale celowo zawierają zebrane metadane źródłowe, identyfikatory oraz ewentualnie treści osobiste lub wrażliwe. W surowych metadanych źródłowych mogą występować skróty dostępu do serwisu Telegram oraz odniesienia do plików.

## Sekrety w stanie spoczynku

Dane uwierzytelniające do API serwisu Telegram, obiekt StringSession oraz klucz prywatny Ed25519 są szyfrowane za pomocą biblioteki Fernet. Domyślnie klucz ten jest przechowywany w tym samym chronionym katalogu danych. Ogranicza to przypadkowe ujawnienie tekstu jawnego; nie stanowi to jednak zabezpieczenia przed atakującym, który może odczytać zawartość całego katalogu. Treść wiadomości i pliki multimedialne **nie** są **szyfrowane** przez TgWitness. Należy stosować szyfrowanie dysku oraz restrykcyjne uprawnienia systemu operacyjnego. Pliki klucza prywatnego w systemie Unix są tworzone z trybem dostępu 0600; nowo utworzone katalogi danych wykorzystują tryb 0700. Istniejące uprawnienia katalogów nie ulegają zmianie. System Windows dziedziczy listy kontroli dostępu (ACL) katalogów: należy je ograniczyć do konta usługi oraz upoważnionych administratorów.

### Zewnętrzny klucz główny

W przypadku nowego katalogu danych zmienna TGWITNESS_VAULT_KEY_FILE może dostarczyć zewnętrzny losowy klucz główny. HKDF-SHA256 oraz oddzielny losowy salt generują inny klucz Fernet dla każdego obszaru roboczego. Plik vault.external.json należy zachować na potrzeby odzyskiwania danych. Brakujące lub nieprawidłowe klucze główne powodują niepowodzenie operacji. Istniejące lokalne skarbce nie są migrowane w trybie cichym. Uruchomiony proces ma dostęp do klucza; nie jest to izolacja typu HSM. Panel informuje o wybranym trybie i wyraźnie zaznacza, że przechowywanie wiadomości/multimediów nie jest szyfrowane przez aplikację. Pełny model zagrożeń można znaleźć w sekcjach dotyczących [połączeń, serwerów proxy i ochrony danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) .

## Serwery proxy i trasy sieciowe

Konfiguracja serwera proxy jest szyfrowana w skarbcu. Hasła i klucze MTProxy nie są zwracane przez API ani zapisywane w rejestrach dowodowych. Każdy obszar roboczy wybiera własną trasę Telegramu oraz [tryb IP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes).

Tryb „Ukryj adres IP” blokuje bezpośrednie połączenie awaryjne z Telegramem i wymaga korzystania z serwera proxy dla zewnętrznych żądań HTTP. Wyraźnie wybrany tryb awaryjny umożliwia bezpośredni dostęp do Telegrama po upływie określonego opóźnienia; tryb tunelowy/VPN pozwala na bezpośrednie połączenia. Wybranie trybu tunelowego nie powoduje instalacji ani weryfikacji sieci VPN. Ustawienia te nie kontrolują całego ruchu urządzenia, przeglądarek, menedżerów pakietów ani lokalnego rozpoznawania nazw DNS przez serwer proxy.

MTProxy obsługuje wyłącznie ruch z aplikacji Telegram. Żądania zewnętrzne mogą korzystać z oddzielnego proxy SOCKS5/HTTP, trasy SOCKS5/HTTP obszaru roboczego lub dozwolonej trasy bezpośredniej; można je również wyłączyć. Niezależny moduł „witness” posiada własne ustawienia transportowe. Zwykłe uwierzytelnianie SOCKS5/HTTP CONNECT nie jest szyfrowane przez same protokoły proxy. Fałszywe klucze tajne TLS MTProxy nadal nie są obsługiwane.

## Logowanie i import sesji

Przekonwertowane pliki .tgwitness-session zawierają sekret autoryzacyjny w postaci zwykłego tekstu do momentu załadowania i zapisania w skarbcu. Interfejs CLI działający w trybie offline akceptuje zweryfikowane schematy Telethon. Import z panelu obsługuje dodatkowo formaty Pyrogram SQLite, nowoczesny plik ZIP TData dla pojedynczego konta oraz udokumentowane dane wejściowe w formacie JSON. Funkcja ta jest uwierzytelniana, ograniczona do czterech plików / 8 MiB, a przesyłane dane są przetwarzane w pamięci bez rozpakowywania archiwum ani zapisywania oryginalnych plików. Znormalizowane dane uwierzytelniające są zwracane wyłącznie do wysyłającej żądanie, uwierzytelnionej przeglądarki; są one zapisywane w zaszyfrowanym sejfie po pomyślnym uwierzytelnieniu w Telegramie. Należy chronić pliki oryginalne i przekonwertowane oraz unikać sytuacji, w której równoczesne klienty klonują dane uwierzytelniające.

Przetwarzanie danych obejmuje weryfikację sum kontrolnych kontenerów, lokalnych skrótów deszyfrujących oraz długości struktur. Podane lokalne hasło do aplikacji Desktop jest wykorzystywane tymczasowo i nie jest przechowywane. Ten ograniczony parser nie gwarantuje, że każda wersja aplikacji Desktop jest kompatybilna. Obrazy kodów QR są generowane lokalnie, zawierają krótkotrwałe tokeny logowania do aplikacji Telegram i nigdy nie są wysyłane do zewnętrznej usługi renderującej. Zablokowanie urządzenia, zmiana obszaru roboczego, nowe logowanie oraz zmiany trasy powodują anulowanie oczekujących prób skanowania kodów QR. Ponowne załadowanie lub zamknięcie karty może spowodować, że próba pozostanie w toku do momentu wygaśnięcia. Pomyślne zalogowanie za pomocą kodu QR nadal wymusza powiązanie konta. Zwykłe treści żądań API pozostają ograniczone do 16 KiB; uwierzytelniona ścieżka importu akceptuje do 12 MiB zakodowanego JSON, osobno egzekwując mniejszy limit rozmiaru zdekodowanego pliku.

Kody logowania oraz hasła do dwuetapowej weryfikacji w Telegramie nie są przechowywane. Stan numeru telefonu/skrótu kodu jest przechowywany w pamięci podczas autoryzacji. Sesje w Telegramie zapewniają dostęp do konta; nigdy nie należy przesyłać katalogu danych, sesji, tokenu, klucza do skarbca ani prywatnego klucza podpisującego na GitHub.

## Dzienniki i transport

Domyślna odpowiedź walidacyjna API została zastąpiona tak, aby nie powtarzała wartości danych uwierzytelniających. Rejestrowanie dostępu do aplikacji jest wyłączone. Proszę nie konfigurować serwera proxy odwrotnego w celu rejestrowania nagłówków autoryzacji ani treści żądań. Protokół HTTP przesyła tokeny i tajne dane logowania w postaci zwykłego tekstu: w przypadku opuszczania serwera localhost należy zawsze korzystać z protokołu HTTPS lub tunelu SSH.

## Ograniczenia dotyczące integralności

Łańcuch skrótów, wyzwalacze bazy danych oraz podpisy wykrywają określone modyfikacje; nie uniemożliwiają one jednak lokalnemu administratorowi przepisania i ponownego podpisania dziennika. Prosimy o przechowywanie podpisanych punktów kontrolnych oraz odcisku klucza publicznego w oddzielnym systemie. Tryb dowodowy oraz kopia zewnętrzna (oba domyślnie wyłączone) wysyłają skróty punktów kontrolnych do usług znaczników czasu oraz zaszyfrowane kopie do pamięci masowej zgodnej ze standardem S3; proszę zapoznać się z [formatem dowodowym](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/). Dzienniki przejrzystości, podpisywanie oparte na module HSM oraz formalna certyfikacja łańcucha dowodowego nie zostały wdrożone.

## Jeśli podejrzewają Państwo wystąpienie problemu

Należy zachować oryginalny katalog danych i wykorzystać do analizy oddzielną kopię. Nie należy umieszczać prywatnych danych z Telegrama ani danych uwierzytelniających w publicznych zgłoszeniach. Nie przedstawia się żadnych niezależnych certyfikatów bezpieczeństwa.
