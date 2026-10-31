# Wdrożenie

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/

Proszę uruchomić TgWitness jako usługę w systemach Windows, Linux, macOS lub Docker, za protokołem HTTPS, z kopiami zapasowymi i aktualizacjami.

**Język angielski** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ukraiński](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Chiński uproszczony](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Proszę wybrać opcję instalacji

W przypadku pakietu przenośnego należy rozpakować plik `TgWitness-<version>-windows-amd64-portable.zip` z sekcji „GitHub Releases”. W przypadku pozostałych metod należy pobrać i rozpakować plik ZIP ze źródłami lub sklonować repozytorium, a następnie uruchomić następujące polecenie z katalogu projektu:

| Instalacja | Rozpocznij | Czy działa w tle? |
| --- | --- | --- |
| Pakiet przenośny dla systemu Windows | `TgWitness.cmd` | Nie; proszę pozostawić okno otwarte. |
| Wersja natywna dla systemu Windows | `Start.cmd` | Nie; w przypadku działania w tle należy skorzystać z opcjonalnego zadania logowania. |
| Wersja natywna dla systemów Linux/macOS | `sh start.sh` | Nie; w celu działania w tle należy używać systemd/launchd. |
| Docker na dowolnym obsługiwanym serwerze | `docker compose up -d --build --wait` | Tak, o ile działa demon Docker. |
| Narzędzie pomocnicze Docker w systemie Windows | `scripts\Docker.cmd` | Tak; moduł pomocniczy oczekuje na informacje o stanie serwera internetowego. |
| Narzędzie pomocnicze Docker na systemach Linux/macOS | `sh scripts/docker-start.sh` | Tak; moduł pomocniczy oczekuje na informacje o stanie serwera internetowego. |

W przypadku serwera w chmurze, który powinien być dostępny do weryfikacji przez stronę trzecią — utworzonego za pośrednictwem interfejsu API dostawcy, bez korzystania z SSH, dostępnego wyłącznie poprzez tunel Cloudflare — proszę zapoznać się z opisem [wdrożenia o wysokim poziomie bezpieczeństwa](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md).

Podczas uruchomienia natywnego programu tworzony jest prywatny plik `.venv` oraz instalowane są przypisane zależności. Docker kompiluje je wewnątrz obrazu, bez konieczności korzystania z środowiska Python na hoście. Pierwsza konfiguracja wymaga dostępu do Internetu. W przypadku braku Pythona w wersji 3.11 lub nowszej, `Start.cmd` wyświetla zapytanie przed zainstalowaniem Pythona 3.12 dla bieżącego użytkownika systemu Windows (za pomocą winget, w przeciwnym razie za pomocą instalatora z python.org po sprawdzeniu podpisu Python Software Foundation); nigdy nie wymaga uprawnień administratora. Docker i usługi systemu operacyjnego pozostają wymaganiami wstępnymi.

Instalacje natywne i przenośne wykorzystują wolumin o nazwie „`data/live`” w obrębie swojego folderu. Docker korzysta z woluminu o nazwie „`tgwitness-data`” w lokalizacji „`/data`”. Są to odrębne instalacje do momentu celowej migracji całego katalogu danych. Nie należy oczekiwać, że nowy kontener Docker automatycznie wykryje natywne konta.

## Wymagania instalacyjne

Instalacja natywna wymaga środowiska Python 3.11 lub nowszego wraz z modułami `venv` i `ensurepip`, dostępu do Internetu w celu zainstalowania pierwszej zależności oraz katalogu projektu z uprawnieniami do zapisu dla modułu `.venv`. Dołączony panel nie wymaga środowiska Node.js ani kompilacji interfejsu użytkownika. Proszę uruchomić program uruchamiający z zwykłego konta użytkownika systemu operacyjnego; narzędzie TgWitness nie wymaga uprawnień administratora ani root.

- **System Windows:** `Start.cmd` sprawdza lokalizację `py -3`, następnie `python`, a następnie domyślne foldery instalacyjne dla poszczególnych użytkowników oraz folder „Program Files” i wymaga wersji 3.11 lub nowszej. Jeśli żadna z tych opcji nie zadziała, narzędzie proponuje automatyczną instalację dla poszczególnych użytkowników, opisaną powyżej. Działa również `py -3 start.py`. Pakiet przenośny nie wymaga w ogóle środowiska Python.
- **Linux:** `start.sh` próbuje `python3.13`, `python3.12`, `python3.11`, `python3` oraz `python` i wyświetla polecenie instalacyjne dla apt, dnf, pacman, zypper, apk lub Homebrew, gdy żadna z opcji nie jest odpowiednia. Instalacje w systemach Debian/Ubuntu mogą wymagać pakietu `python3-venv` odpowiadającego wybranemu interpreterowi. Starszą domyślną wersję języka Python w danej dystrybucji należy zastąpić lub uzupełnić o Python 3.11+.
- **macOS:** zainstaluj aktualną dystrybucję języka Python 3.11 lub nowszą; nie należy zakładać, że interpreter dostarczony wraz z systemem operacyjnym spełnia wymagania. Należy użyć pliku `python3 start.py` z katalogu projektu.
- **Docker:** należy korzystać z Docker Engine/Desktop wraz z Compose w wersji 2.20 lub nowszej. W systemie Windows program Docker Desktop musi korzystać z kontenerów Linux. Kontener instaluje swoje własne zależności języka Python; na komputerze hosta nie jest wymagana oddzielna instalacja języka Python.

Proszę wykorzystać trwałą pamięć lokalną jako katalog danych. Należy zaplanować pojemność, uwzględniając liczbę wiadomości, pliki multimedialne, wzrost rozmiaru pliku WAL, eksporty oraz kopie zapasowe; nie istnieje oparta na dowodach, uniwersalna minimalna specyfikacja dotycząca dysku lub pamięci RAM dla każdego obciążenia. Architektury procesorów oraz wersje języka Python bez kompatybilnych zestawów zależności mogą wymagać dodatkowych narzędzi kompilacyjnych oraz ich własnej kwalifikacji. Termin „przenośny” nie oznacza uniwersalnej obsługi wszystkich systemów operacyjnych ani sprzętu.

Działanie na systemie Windows 11 z Pythonem 3.12 zostało zweryfikowane lokalnie. Definicje dla systemów Linux, macOS oraz kontenerów, a także środowisko CI zostały dostarczone, ale nie zostały uruchomione na tym serwerze deweloperskim. Dokładny zakres weryfikacji znajduje się w [pliku VERIFICATION.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/).

## Komputer lokalny

W systemie Windows należy użyć kodu `Start.cmd`, a w systemach Linux/macOS – `sh start.sh`. Kod `scripts\Setup.cmd` lub `sh start.sh --setup-only` służy do przygotowania środowiska. Program uruchamiający instaluje zależności przy pierwszym uruchomieniu; kolejne uruchomienia wykorzystują już przygotowane środowisko. Dostęp do Internetu jest wymagany podczas konfiguracji oraz gromadzenia danych z Telegrama, jednak przeglądanie istniejących zapisów i tworzenie eksportów odbywa się w trybie offline.

Po zakończeniu konfiguracji proszę uruchomić polecenie „`python start.py --check`”, aby sprawdzić lokalne zależności, algorytm Ed25519, pamięć masową, konfigurację kluczy oraz adres nasłuchowy bez uruchamiania modułu zbierającego dane. Proszę użyć polecenia `--json`, aby uzyskać uporządkowany wynik. Proszę przekazać zamierzone polecenia `--data-dir`, `--host` oraz `--port`. Sprawdzanie to nie powoduje instalacji pakietów, nie tworzy dziennika ani nie łączy się z aplikacją Telegram; nie stanowi ono kwalifikacji pod kątem integralności ani zakresu. Podczas uruchamiania następuje oddzielna weryfikacja istniejących dzienników. Polecenie `python start.py --help` również pozwala uniknąć instalacji.

Opcje:

Po uruchomieniu pliku start.py należy wykonać polecenia pomocnicze za pomocą `.venv\Scripts\python.exe` w systemie Windows lub `.venv/bin/python` w systemach Linux/macOS, albo najpierw aktywować to środowisko. Poniższe przykłady dotyczące `python -m ...` zakładają, że środowisko jest aktywne.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Zmienne środowiskowe: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE wybiera tryb klucza zewnętrznego dla nowej instalacji; patrz poniżej. TGWITNESS_TOKEN, o ile zostanie podany, musi zawierać co najmniej 24 znaki; należy użyć wartości losowej wygenerowanej kryptograficznie. W przypadku braku tego parametru aplikacja generuje losowy token 256-bitowy w pliku panel-token.txt. Nadpisanie zmiennej środowiskowej nie powoduje ponownego zapisania tego pliku. Należy ponownie uruchomić aplikację, aby zmienić dane uwierzytelniające.

Katalog danych może być zarządzany wyłącznie przez jeden proces. Międzyplatformowa blokada plików systemu operacyjnego zapobiega przypadkowym równoczesnym zapisom. Należy używać jednego procesa roboczego Uvicorn. Panel może zarządzać dowolną liczbą obszarów roboczych, przy czym dodatkowe katalogi obszarów roboczych znajdują się w ścieżce profiles/<id>/. W przypadku oddzielnych instancji usługi należy stosować oddzielne katalogi i porty. Pliki WAL bazy SQLite powinny znajdować się w lokalnej pamięci trwałej, a nie w sieciowym systemie plików. Nie należy współdzielić jednego woluminu między replikami.

## Pakiet przenośny dla systemu Windows

Każda wersja opublikowana na GitHubie zawiera plik `TgWitness-<version>-windows-amd64-portable.zip` oraz jego odpowiednik `.sha256`. Zawiera ona oficjalne środowisko uruchomieniowe Python 3.12 z serwisu python.org, które można osadzić w innych aplikacjach (suma kontrolna zapisana w pliku `tools/build_portable.py`), program TgWitness wraz z jego stałymi zależnościami, oraz trzy programy uruchamiające:

| Plik | Cel |
| --- | --- |
| `TgWitness.cmd` | Uruchom panel; dodatkowe opcje są przekazywane dalej, np. `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Uruchom demonstrację syntetyczną pod adresem `data\demo` |
| `TgWitness-Check.cmd` | Proszę uruchomić sprawdzanie gotowości bez uruchamiania |

Rozpakuj całe archiwum do folderu z uprawnieniami do zapisu, np. `Documents\TgWitness`; nie uruchamiaj programu z poziomu pliku ZIP ani z folderu Program Files. Środowisko uruchomieniowe korzysta z izolowanej ścieżki modułów, więc inne instalacje języka Python oraz folder `PYTHONPATH` nie mają na nie wpływu. Dane pozostają w folderze `data` pakietu. Aby zaktualizować oprogramowanie, należy zatrzymać TgWitness, rozpakować nową wersję do nowego folderu, a następnie skopiować do niego folder `data`.

Zainstaluj samodzielnie na 64-bitowym systemie Windows z wykorzystaniem języka Python 3.12:

```
python tools/build_portable.py
```

Kompilator weryfikuje sumę kontrolną środowiska uruchomieniowego, instaluje ograniczone zależności w pakiecie, przeprowadza kontrolę gotowości za pomocą wbudowanego interpretera oraz zapisuje plik ZIP wraz z sumą kontrolną w pliku `dist/`.

## Kontener

```
docker compose up -d --build --wait
```

Powoduje to utworzenie nazwanego woluminu trwałego dla katalogu /data. Port sieciowy jest mapowany na adres 127.0.0.1:8787. Proces działa pod identyfikatorem UID 10001 z ograniczonymi uprawnieniami, z systemem plików root tylko do odczytu oraz katalogami /data i /tmp z prawem do zapisu. `--wait` sprawdza stan serwera internetowego przed zakończeniem działania; nie nawiązuje połączenia w celu autoryzacji ani dostarczenia wiadomości w Telegramie. Dostarczone narzędzia pomocnicze stosują 180-sekundowy limit czasu gotowości po zakończeniu kompilacji. Początkowe pobieranie zależności może trwać dłużej.

Oba podstawowe pliki Compose wykorzystują nazwę projektu `tgwitness`, więc rozpakowanie nowej wersji do innego katalogu nie powoduje automatycznego wyboru nowego woluminu danych. Należy utrzymywać tylko jedno aktywne wdrożenie dla danego projektu. W przypadku niezależnych instalacji należy użyć unikalnej nazwy `docker compose -p NAME ...` oraz innego portu hosta, a podczas aktualizacji zachować oba wdrożenia. W przypadku starszego wdrożenia wykorzystującego inną nazwę projektu należy nadal używać jego pierwotnej nazwy wraz z `-p`; `docker compose ls` wyświetla listę istniejących projektów.

Skopiuj `deploy/env.example` do `.env` i zmień `TGWITNESS_PORT`, aby używać innego portu pętli zwrotnej. Na przykład `TGWITNESS_PORT=8788` udostępnia panel pod adresem `http://127.0.0.1:8788`; kontener nadal nasłuchuje na porcie 8787. `.env` jest pomijany przez Git.

Pobierz token początkowy:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Przydatne polecenia:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` uruchamia ponownie moduł zbierający dane po awarii lub ponownym uruchomieniu demona Docker. Na serwerze z systemem Linux należy włączyć uruchamianie Docker przy starcie systemu za pomocą menedżera usług danej dystrybucji, zwykle `sudo systemctl enable --now docker`. W systemach Windows/macOS należy włączyć ustawienie „uruchom przy logowaniu” w programie Docker Desktop. Wylogowanie z komputera, przejście w stan uśpienia lub zatrzymanie demona Docker mogą przerwać gromadzenie danych. Wyraźnie zatrzymany kontener pozostaje w stanie zatrzymania do momentu jego ponownego uruchomienia.

W przykładowej konfiguracji rozmiar woluminu /tmp jest ograniczony do 512 MiB. Konstrukcja eksportu wykorzystuje zamiast tego identyfikator `temporary-exports/` każdego obszaru roboczego w trwałym katalogu /data. Należy zarezerwować tam miejsce na równoczesne eksporty, wzrost rozmiaru dziennika/WAL, pliki multimedialne oraz kopie zapasowe. Program uruchamiający wykorzystuje plik deploy/constraints.txt do ustalenia kwalifikowanych wersji zależności środowiska uruchomieniowego. Serwery Docker oraz serwery o wysokim poziomie bezpieczeństwa są instalowane na podstawie plików deploy/requirements.lock oraz deploy/build.lock przy użyciu polecenia pip --require-hashes: każdy plik pakietu musi odpowiadać wartości SHA-256 zarejestrowanej w commitcie, w związku z czym plik zastąpiony w serwisie PyPI lub na serwerze lustrzanym zostanie odrzucony. Obraz bazowy języka Python oraz pakiety systemu operacyjnego nadal wymagają niezależnej kwalifikacji wydania.

Nie należy używać polecenia `docker compose down -v`, chyba że zamierza się zniszczyć dziennik i klucze. Raporty o stanie kontenera informują o dostępności serwera internetowego, a nie o pomyślnym przechwyceniu wiadomości z Telegrama. Należy sprawdzić stan kolektora panelu, sygnał kontrolny, błędy oraz zdarzenia związane z zasięgiem.

### Profil niezależnego świadka

Opcjonalna usługa `witness` uruchamia [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/) we własnym kontenerze, z własnym kluczem i dziennikiem w woluminie `witness-data` oraz wyłącznie tokenem świadka tylko do odczytu dla kolektora. Należy utworzyć token na stronie **„Witness”** w panelu, dodać go wraz z tokenem bota i kanałem do `.env`, a następnie uruchomić profil:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Usługa łączy się z modułem zbierającym w sieci Compose pod adresem `http://tgwitness:8787` (adres `TGWITNESS_WITNESS_COLLECTOR` ma pierwszeństwo, na przykład `/profiles/<workspace ID>` dla innego obszaru roboczego). W przypadku modułu świadczącego na oddzielnym serwerze, zarządzanym przez inną osobę, należy użyć tam adresu `deploy/compose/compose.witness.yaml` , ustawiając `TGWITNESS_WITNESS_COLLECTOR` na adres HTTPS modułu zbierającego; plik ten zawiera wyłącznie moduł świadczący.

## Zainstaluj opublikowany obraz

Zostanie to udostępnione po pomyślnym zakończeniu [procesu wydania](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/#automated-github-releases) oraz publicznej konfiguracji pakietu GHCR. Nazwa lub właściciel repozytorium nie są na stałe zakodowane w tym drzewie źródłowym. Proszę skorzystać z obrazka przedstawionego w podsumowaniu procesu wydania.

Skopiuj `deploy/env.example` do `.env`. Ustaw `TGWITNESS_IMAGE` na opublikowaną wersję, używając ścieżki do repozytorium **zapisanej małymi literami**, na przykład:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

Proszę uruchomić ten plik samodzielnie, zamiast pliku `compose.yaml`:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Na serwerze nie jest wymagana kompilacja kodu źródłowego, język Python ani kompilator. Proces wydawania aktualizacji jest przeznaczony dla kontenerów Linux AMD64 i ARM64, w tym dla maszyny wirtualnej Linux w programie Docker Desktop. Należy użyć tagu wersji lub oznaczenia „`ghcr.io/owner/repository@sha256:...`” z podsumowania procesu. Nie skonfigurowano przenoszenia tagu „`latest`” ani automatycznej aktualizacji aplikacji. Obraz i warianty źródłowe korzystają z tego samego woluminu danych, o ile nazwa projektu jest identyczna.

## Automatyczne włączenie protokołu HTTPS na serwerze

Należy skorzystać z serwera z oprogramowaniem Docker, domeny, nad którą sprawują Państwo kontrolę, oraz trwałej pamięci lokalnej. Proszę skierować rekordy A/AAAA domeny na serwer; opublikuj rekord AAAA tylko wtedy, gdy serwer jest dostępny w sieci IPv6. Proszę zezwolić na ruch przychodzący na portach TCP 80 i 443 oraz ruch wychodzący przez DNS/HTTPS w celu wydania certyfikatu. Porty te nie mogą być już zajęte przez inne usługi.

Skopiuj `deploy/env.example` do `.env` i ustaw nazwę hosta, bez schematu ani ścieżki:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Rozpocznij kompilację kodu źródłowego z nakładką HTTPS:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

W przypadku opublikowanego obrazu należy zamiast tego użyć pliku `deploy/compose/compose.image.yaml` jako pierwszego. Należy zachować oba argumenty `-f` na potrzeby późniejszych poleceń dotyczących statusu, logów, aktualizacji oraz zatrzymania.

Caddy pobiera i odnawia certyfikat, przekierowuje połączenia HTTP na HTTPS oraz przekazuje żądania do kolektora w prywatnej sieci Compose. Stan certyfikatu jest przechowywany na osobnym woluminie trwałym. Port hosta kolektora pozostaje przeznaczony wyłącznie do pętli zwrotnej. Dostarczona konfiguracja Caddy nie włącza rejestrowania dostępu.

Proszę otworzyć `https://watch.your-domain.org` i wprowadzić token panelu. Gotowość do tworzenia nie potwierdza wydania certyfikatu ani dostępności zewnętrznej. Jeśli protokół HTTPS nie jest gotowy, proszę sprawdzić DNS, reguły zapory sieciowej oraz:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Dostarczony obraz Caddy jest oznaczony tagiem `2-alpine`. Wykonanie polecenia „pull” powoduje odświeżenie tego obrazu; w razie potrzeby zastosowania stałych wersji infrastruktury proszę przypiąć sprawdzony skrót do Państwa wdrożenia.

## Aktualizacje i kopie zapasowe

Należy zachować nazwę projektu Compose oraz objętość danych podczas aktualizacji. Najpierw należy zatrzymać moduł zbierający dane i wykonać pełną kopię zapasową. W przypadku domyślnego wdrożenia opartego na źródłach:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Za każdym razem należy korzystać z nowej lokalizacji kopii zapasowej, znajdującej się poza repozytorium, i chronić ją jako materiał wymagający dostępu do konta. Podana ścieżka ma charakter poglądowy; należy skorzystać z własnej prywatnej lokalizacji kopii zapasowej. Należy skopiować cały katalog, w tym pliki ukryte, wszystkie obszary robocze, klucze, dzienniki oraz pliki multimedialne. Jeśli został skonfigurowany, należy osobno wykonać kopię zapasową zewnętrznego klucza głównego skarbca. Plik ZIP z dowodami nie jest kopią zapasową aplikacji umożliwiającą przywrócenie danych. W przypadku protokołu HTTPS należy również zachować woluminy Caddy, jeśli konieczne jest zachowanie stanu certyfikatu/konta.

Aby przeprowadzić wdrożenie z kodu źródłowego, należy pobrać pliki nowej wersji i uruchomić:

```
docker compose up -d --build --wait
```

W przypadku wdrożenia obrazu należy zmienić `TGWITNESS_IMAGE` na żądaną wersję, a następnie uruchomić:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

W przypadku powyższych poleceń stop/copy należy również skorzystać z plików Compose swojej instalacji. Zachowaj plik `.env`, niestandardową konfigurację oraz tę samą nazwę projektu. Plik `down` zachowuje nazwane woluminy; plik **`down -v` je usuwa**. Nie należy kopiować pliku `.venv` między systemami operacyjnymi ani wersjami języka Python. W przypadku aktualizacji natywnych należy zatrzymać działanie TgWitness, wykonać kopię zapasową całego katalogu danych , zastąpić pliki źródłowe, a przed uruchomieniem wykonać polecenie `python start.py --setup-only`.

Proszę sprawdzić dostęp do panelu, tożsamość konta, stan obserwacji oraz zakres działania po aktualizacji. Ponowne uruchomienie nie odtwarza pominiętych aktualizacji serwisu Telegram. Cofnięcie zmian może wymagać kopii zapasowej sprzed aktualizacji, jeśli przyszła wersja zmieni formaty przechowywania danych.

## Zautomatyzowane wydania na GitHubie

[Proces wydawania](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) jest gotowy do użycia po umieszczeniu tego projektu w repozytorium GitHub z włączoną funkcją Actions. Uruchamia się on w momencie **opublikowania** wydania na GitHubie, w tym również wersji przedpremierowej. Same wersje robocze i operacje dodawania tagów nie powodują publikacji pakietów.

1. Należy ustawić wersję pakietu oraz dziennik zmian, a następnie opublikować wydanie oznaczone tagiem „`v`” wraz z dokładną wersją „`pyproject.toml`”, np. „`v0.7.0`”.
2. Proces ten weryfikuje tag i uruchamia wspólne dla systemów Windows/Linux/macOS sprawdzanie środowiska Python, ogólne/import konta/QR w przeglądarce, pakietu źródłowego oraz Docker. Przeprowadzana jest również nowa instalacja natywna na wszystkich trzech systemach operacyjnych z wykorzystaniem języka Python 3.12.
3. Po pomyślnym przejściu tych kontroli przeprowadzane są testy wstępne obrazu ARM64 w środowisku QEMU, publikowane są obrazy AMD64/ARM64 na serwerze `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, a do wydania dołączany jest plik ZIP ze źródłami, suma kontrolna oraz pakiet Python wheel. Oddzielne zadanie w systemie Windows kompiluje i dołącza przenośny plik ZIP wraz z jego sumą kontrolną.
4. Po pierwszej publikacji należy otworzyć ustawienia pakietu GHCR i ustawić widoczność na **„Publiczna”**, jeśli planowane jest anonimowe pobieranie obrazów. Samo publiczne repozytorium źródłowe nie gwarantuje, że pakiet kontenerowy będzie publiczny. Polityka organizacji musi zezwalać na publikację pakietów. W procesie tym wykorzystywany jest `GITHUB_TOKEN`; w repozytorium nie należy umieszczać hasła do rejestru ani danych uwierzytelniających do serwera VPS.

Powyższe przygotowania lokalne nie gwarantują powodzenia pracy zdalnej. Emulacja ARM64 stanowi jedynie test wstępny, a nie kwalifikację na sprzęcie natywnym ani w rzeczywistym środowisku Telegramu. Funkcja ta automatyzuje pakowanie wydania; uruchomienie serwera nadal wymaga polecenia Compose oraz spełnienia związanych z nim wymagań dotyczących domeny i hosta. Istniejące serwery nie są automatycznie aktualizowane ani restartowane po opublikowaniu nowego wydania.

## Serwer zdalny

Należy ograniczyć działanie usługi do pętli zwrotnej i korzystać z tunelu SSH lub zakończyć połączenie HTTPS na proksie odwrotnym. Podstawowy plik Compose jest przeznaczony wyłącznie do użytku lokalnego; opcjonalna nakładka `deploy/compose/compose.https.yaml` udostępnia serwer Caddy dla skonfigurowanej domeny. Należy unikać umieszczania tokenu bearer w adresach URL i logach serwera proxy. Serwer proxy odwrotny powinien ograniczać rozmiar żądań oraz częstotliwość połączeń. Nie należy udostępniać zwykłego protokołu HTTP w Internecie.

Przykłady dotyczące systemu systemd, zadania logowania w systemie Windows, agenta użytkownika w systemie macOS oraz serwera Caddy znajdują się w [katalogu deploy/.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Prosimy o sprawdzenie i dostosowanie ścieżek dostępu przed instalacją. Są to dostarczone szablony, a nie lokalnie wykonywane konfiguracje platformowe. Żadna usługa działająca w tle ani żadne zadanie nie są rejestrowane przez standardowy program uruchamiający.

W systemie Windows uruchomienie `pythonw.exe` bez okna powoduje zapisywanie diagnostyki uruchomienia/serwera w pliku `logs/server.log` w katalogu danych (5 MiB na plik, dwie rotowane kopie zapasowe). Uruchomienia z konsoli zachowują logi konsoli. Rejestrowanie dostępu HTTP jest wyłączone w obu trybach. Należy zabezpieczyć logi wraz z katalogiem danych i przejrzeć je przed udostępnieniem.

## Ponowne uruchomienie i luki

Ostatni żądany stan obserwacji jest zachowywany. Jeśli obserwacja była aktywna, program podczas uruchamiania podejmuje próbę ponownego połączenia się i wznowienia wybranych źródeł. Ręczne wstrzymanie usuwa ten zamiar. Nieudane ponowne uruchomienie jest rejestrowane i wyświetlane w panelu.

StringSession zachowuje autoryzację, ale nie przechowuje trwałego stanu aktualizacji/entności z Telethon. Okna dialogowe są ponownie ładowane przy uruchomieniu. Telegram/Telethon może odtworzyć niektóre przerwy w transmisji podczas działania, jednak TgWitness nie gwarantuje trwałego odtworzenia danych po ponownym uruchomieniu procesu. Przy każdym uruchomieniu rejestrowany jest poprzedni początek dziennika oraz granica trybu offline. Monitor sprawdza łączność co 10 sekund i dodaje sygnał kontrolny co minutę (**Parametry → Częstotliwość rejestrowania aktywności**). Krótkie przerwy mogą zostać pominięte; połączenie transportowe nie gwarantuje pełnego dostarczenia aktualizacji. Migawki są wyraźnymi obserwacjami bieżącej historii, a nie uzupełnianiem luk.

Kolejka multimediów jest przechowywana w bazie danych SQLite każdego obszaru roboczego. Wiadomość i związane z nią zadanie są zatwierdzane atomowo. Przerwane zadania są odzyskiwane w celu ponownej próby po uruchomieniu. Każde pobieranie ma podstawowy limit czasu wynoszący 120 sekund plus czas obliczony przy prędkości 256 KiB/s w zależności od rozmiaru pliku oraz limit 1–2 000 MiB na typ załącznika; limit czasu, prędkość i liczba ponownych prób są konfigurowane w **sekcji „Parametry**”. Moduł zbierający pomija pliki o nieznanym rozmiarze. Wstrzymanie zachowuje zadania w kolejce. Ponowna próba wykorzystuje oryginalny zarejestrowany deskryptor pliku, a nie najnowszą wersję wiadomości edytowanej później. W przypadku tymczasowych awarii liczba ponownych prób jest ograniczona; wstrzymania typu „FloodWait” dotyczą plików multimedialnych są zachowywane po ponownym uruchomieniu. Odzyskiwanie plików multimedialnych jest odrębne od odzyskiwania aktualizacji Telegramu i nie pozwala na odtworzenie utraconych plików.

## Tworzenie kopii zapasowych, przywracanie danych i pojemność

Należy zatrzymać proces przed skopiowaniem **całego katalogu danych**, w tym plików vault.key, signing.enc, credentials.enc, bazy danych SQLite/plików WAL, multimediów, tokenu, punktów kontrolnych oraz wszystkich profili i podkatalogów. Przywróć kompletną kopię, gdy usługa docelowa jest zatrzymana. Brakujące klucze do skarbca lub niezgodność kluczy podpisujących powodują niepowodzenie uruchomienia; nie należy regenerować kluczy w celu wymuszenia dostępu.

Tajne kopie zapasowe należy przechowywać w postaci zaszyfrowanej i z kontrolowanym dostępem. Pliki ZIP z dowodami są przenośnymi artefaktami do przeglądu, a nie kopiami zapasowymi aplikacji ani sesji Telegramu. Nie ma automatycznego usuwania danych po upływie okresu przechowywania. Należy zaplanować miejsce na dysku na wszystkie wiadomości, surowe metadane, pliki multimedialne, tymczasowe eksporty oraz kopie zapasowe.

Weryfikacja uruchomienia oraz eksport rekordów strumienia zamiast ładowania całego dziennika. Eksport utrwala odczytany migawkę, podczas gdy nowe zapisy do dziennika WAL mogą być kontynuowane; długotrwałe eksporty mogą zachowywać strony dziennika WAL, dlatego pojemność dysku nadal ma znaczenie. Pliki ZIP są ograniczone do 4 GiB po rozpakowaniu, aby odpowiadały domyślnym ustawieniom niezależnego weryfikatora; **Parametry → Największy podpisany plik ZIP** zwiększa ten limit, a archiwa tego typu są weryfikowane za pomocą `verify.py --max-gib N`. Inne formaty nie mają ograniczeń dotyczących liczby zdarzeń. Obsługiwane przeglądarki przesyłają strumieniowo fragmenty odpowiedzi do pliku wybranego przez użytkownika. Inne przeglądarki buforują maksymalnie 128 MiB, a większe transfery kierują do uwierzytelnionego interfejsu CLI:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Proszę użyć `--profile ID` z **menu Eksportuj → Identyfikator obszaru roboczego** dla innego obszaru roboczego, `--format zip|jsonl|csv|html`, `--url https://your-server` dla serwera zdalnego lub `--max-mib`, aby zmienić limit transferu wynoszący 5 GiB. Zwykły protokół HTTP jest dozwolony wyłącznie w przypadku pętli zwrotnej. Tokeny są przesyłane w nagłówkach, przekierowania są odrzucane, istniejące pliki nie są nadpisywane, a niekompletne pliki do pobrania nie są publikowane jako pliki ukończone. Jeśli zmienna TGWITNESS_TOKEN zastępuje wygenerowany token, należy użyć oddzielnie zabezpieczonego pliku zawierającego tę aktywną wartość: plik panel-token.txt nie jest nadpisywany przez tę zmianę. Wartość SHA-256 polecenia stanowi jedynie sumę kontrolną transferu; należy niezależnie zweryfikować podpisany plik ZIP.

Pliki eksportowe serwera pozostają w prywatnym katalogu `temporary-exports/` każdego obszaru roboczego. Pomyślnie zakończone operacje usuwają swoje pliki. Przerwane eksporty są usuwane przy następnym uruchomieniu obszaru roboczego, gdy utrzymywana jest jego wyłączna blokada instancji. Katalog ten stanowi część modelu zagrożeń związanych z pamięcią masową oraz jej pojemnością; należy stosować zaszyfrowany wolumin danych. Transfery na skalę produkcyjną, o wielkości wielu gigabajtów, nadal wymagają weryfikacji w systemie docelowym.

Panel wyświetla multimedia oczekujące w kolejce lub, których przesłanie nie powiodło się, najstarsze multimedia oczekujące, wolne miejsce na dysku, przerwy w żądaniach serwisu Telegram oraz źródła, do których dostęp nie został potwierdzony. Te dane diagnostyczne nie stanowią kompletnego monitoringu dostarczania danych od początku do końca. Obszary robocze współdzielą ten sam proces; konto generujące nadmierną aktywność może nadal wpływać na pozostałe. Nadal obowiązują oddzielne procesy robocze, zasady przechowywania i rotacji danych, trwałe odzyskiwanie aktualizacji oraz pełna kwalifikacja wdrożenia. Dostęp do panelu w określonym zakresie jest udokumentowany w [sekcji „Dostęp i uprawnienia”](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/); niezależne punkty kontrolne są omówione w [przewodniku dla świadków](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/).

## Opcje połączeń i zabezpieczeń

Trasy połączeń są przypisane do poszczególnych obszarów roboczych i należy je skonfigurować przed autoryzacją. Protokół SOCKS5/HTTP CONNECT wykorzystuje przypisaną zależność python-socks. MTProxy korzysta z eksperymentalnego, losowego transportu pośredniego firmy Telethon; fałszywe sekrety TLS ee nie są obsługiwane. Bezpośrednie przełączanie awaryjne zależy od wybranego [trybu IP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes): tryb „Ukryj adres IP” odrzuca tę opcję; tryb jawnego przełączania awaryjnego zezwala na to po upływie określonego opóźnienia. Tryb tunelu/VPN zezwala na bezpośrednie trasy, ale nie tworzy sieci VPN. Nie jest to polityka sieciowa obowiązująca w całym systemie.

W przypadku nowych instalacji zmienna TGWITNESS_VAULT_KEY_FILE wskazuje na oddzielnie zabezpieczony plik zawierający losowy klucz główny. Należy zamontować go w trybie tylko do odczytu poza katalogiem /data w kontenerze. Należy zachować publiczne metadane salt z pliku vault.external.json osobno dla każdego obszaru roboczego oraz dla klucza głównego. Istniejące lokalne skarbce wymagają zaplanowanej migracji; ustawienie tej zmiennej nie powoduje ich automatycznej konwersji. Przechowywanie wiadomości i multimediów oraz ich eksport nie są szyfrowane na poziomie aplikacji. W razie potrzeby należy stosować zaszyfrowane woluminy oraz zapewnić wystarczającą ilość prywatnej pamięci tymczasowej.

Szczegółowe procedury: [połączenie/bezpieczeństwo](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) oraz [tryby działania](https://phishdestroy.github.io/TgWitness/pl/docs/reference/operations/).
