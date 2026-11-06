# Instalacja, weryfikacja i aktualizacja

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/installation/

Zainstaluj za pomocą jednego polecenia, sprawdź podpisy i skróty, zaktualizuj lub usuń instalację.

[Projekt](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Szybki start](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/) · [Wdrożenie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/)

## Zainstaluj za pomocą jednego polecenia

Instalator z przewodnikiem zawiera prywatne środowisko uruchomieniowe języka Python. Użyj tego samego adresu do przyszłych instalacji: każda publikacja aktualizuje instalator, skróty, podpisy oraz informacje o kompilacji łącznie.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Na serwerze z systemem Ubuntu uruchom program jako root, aby zainstalować usługę działającą w tle. Na komputerze stacjonarnym uruchom program jako zwykły użytkownik.

**Windows (PowerShell lub wiersz poleceń):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

W systemie Windows nie jest wymagany administrator. Proces potomny PowerShell pozostawia terminal otwarty z wynikiem. Python i zależności pozostają w instalacji.

W systemie Ubuntu wybierz opcję **„Ten komputer**”, **„Tymczasowy link HTTPS**” lub **„Własna domena**”. Instalator wyświetli adres panelu oraz klucz dostępu. Aby uzyskać tymczasowy link, otwórz ten adres HTTPS w przeglądarce i wprowadź klucz. W przypadku dostępu lokalnego na serwerze zdalnym użyj przekierowania SSH z komputera (`ssh -L 8787:127.0.0.1:8787 user@server`) i otwórz `http://127.0.0.1:8787`. W systemach macOS i Windows lokalny panel otwiera się w przeglądarce; należy pozostawić terminal uruchomiony.

Zaloguj się do Telegrama w panelu i wybierz, co chcesz gromadzić. Sama instalacja nie uruchamia gromadzenia danych z Telegrama.

## Gdzie wszystko działa

`get.destroy.tools` jest to **Cloudflare Worker obsługujący statyczne pliki do pobrania**. Nie zawiera panelu TgWitness, sesji Telegramu ani bazy danych dowodów dotyczących użytkowników. Nie jest przekierowywany na serwer VPS projektu. Aplikacja działa na komputerze, na którym uruchamiasz polecenie.

| Instalacja | Program | Dane |
| --- | --- | --- |
| Ubuntu jako root | `/opt/tgwitness` | Usługa systemowa: `/var/lib/tgwitness-<installation ID>`; użyj `tgwitness paths` , aby uzyskać dokładną ścieżkę. |
| Użytkownik systemu Linux / macOS | `~/.local/share/tgwitness` | `data/live` w ramach tej instalacji. |
| Użytkownik systemu Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` w ramach tej instalacji. |

Ustaw `TGWITNESS_INSTALL_DIR` , aby wybrać inny folder. Zainstalowane wersje i dane są przechowywane oddzielnie. Instalator nie przesyła Twoich kont, wiadomości ani kluczy na stronę pobierania. Wybranie tunelu Cloudflare powoduje, że ruch panelu jest kierowany przez Cloudflare; użycie własnej domeny powoduje przekierowanie na Twój własny serwer.

Każda instalacja zawiera **pliki START-HERE.html** i **START-HERE.txt** z lokalnymi ścieżkami, poleceniami i linkami do repozytorium. Uruchom `tgwitness guide` , aby otworzyć przewodnik. W systemie Windows użyj `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` w PowerShellu.

## Ustawienia wyszukiwania pełnotekstowego

[Wyszukiwanie pełnotekstowe](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/) (wersja podglądowa) nie wymaga konfiguracji. Jego indeks jest tworzony w tle po aktualizacji.

| Zmienna lub polecenie | Efekt |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Domyślnie: indeks jest przechowywany w `search/fulltext.sqlite3` każdego obszaru roboczego |
| `TGWITNESS_FULLTEXT=memory` | Brak pliku indeksowego; indeks jest odbudowywany przy każdym uruchomieniu |
| `TGWITNESS_FULLTEXT=off` | Brak indeksu; wyszukiwanie wyłącznie po dokładnym tekście |
| `tgwitness index status` | Stan indeksu każdego obszaru roboczego |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Odbuduj wszystkie indeksy na podstawie podpisanego dziennika |

Wybór administratora w sekcji **Dziennik → Filtry → Indeks wyszukiwania** zastępuje zmienną dla danego obszaru roboczego. Polecenia wyszukują katalog danych instalacji, w której są uruchamiane; w pozostałych przypadkach należy dodać `--data-dir` ścieżkę z `tgwitness paths`. Aby uzyskać pełny słownik języka ukraińskiego (dane na licencji GPL-3.0), zainstaluj `pymorphy3-dicts-uk` w środowisku Python tej instalacji.

## Dostęp z wiersza poleceń

[Wiersz](https://phishdestroy.github.io/TgWitness/pl/docs/reference/cli/) [poleceń](https://phishdestroy.github.io/TgWitness/pl/docs/reference/cli/) (wersja podglądowa) odczytuje archiwum w poszukiwaniu skryptów i agentów.

| Zmienna | Efekt |
| --- | --- |
| `TGWITNESS_URL` | Adres panelu dla `tgwitness search`, `context`, `messages`, `stats` oraz `export`; domyślnie `http://127.0.0.1:8787` gdy ustawiono token |
| `TGWITNESS_MCP_TOKEN` | Zarchiwizuj token połączenia z **sekcji Integracje → MCP**, udostępniony klientom MCP; `--token-file` zamiast tego odczytuje go z pliku |
| `TGWITNESS_DATA` | Katalog danych odczytywany bezpośrednio, gdy nie podano `--data-dir`, adresu URL ani tokenu |

## Sprawdź przed uruchomieniem

Jednowierszowe polecenie polega na protokole HTTPS w przypadku skryptu początkowego. Skrypt ten sprawdza element SHA-256 oraz podpis RSA projektu w aplikacji i ograniczeniach przed instalacją. Można również najpierw pobrać i zweryfikować skrypt początkowy.

Publiczny klucz wydania to [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Jego SHA-256 to:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Zachowaj ten odcisk palca z wersji repozytorium, której ufasz. Suma kontrolna z tego samego serwera pobierania wykrywa niezgodność; niezależnie zaufany klucz publiczny służy do uwierzytelniania podpisu wydania.

Użyj nowego, pustego katalogu na poniższe pliki do weryfikacji.

**Linux / macOS — uruchom w nowym, pustym katalogu pobierania** (wymagane są curl i OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

Łańcuch `&&` łańcuch zatrzymuje się przed wykonaniem, jeśli pobieranie, sprawdzanie odcisku klucza lub podpisu zakończy się niepowodzeniem. Jeśli między pobraniem skryptu a jego podpisaniem nastąpiła publikacja, należy pobrać oba elementy ponownie. Stare instalatory zachowują swoje niezmienne adresy URL pakietów.

**Windows — przed uruchomieniem sprawdź element SHA-256:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Porównaj skrót z `install.ps1` wierszem. Aby przeprowadzić niezależną weryfikację podpisu, użyj OpenSSL (na przykład z poziomu Git Bash) i tego samego odcisku klucza publicznego, co powyżej:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Sam system Windows weryfikuje podpisy pakietów za pomocą .NET i nie wymaga OpenSSL. Są to oddzielne podpisy RSA-3072 / SHA-256, a nie Authenticode. [Manifest](https://get.destroy.tools/manifest.json) zawiera wersję oprogramowania, dokładny commit w Git, niezmienny identyfikator wydania oraz SHA-256 każdego artefaktu. Strona zawiera linki do odpowiednich źródeł. Manifest i lista sum kontrolnych również posiadają oddzielne podpisy (`manifest.json.sig` oraz `SHA256SUMS.txt.sig`).

## Aktualizacja istniejącej instalacji

**Nowa publikacja aktualizuje stronę pobierania; zainstalowane programy aktualizują się po ponownym uruchomieniu instalatora.** Nie ma funkcji automatycznej aktualizacji ani automatycznego restartu uruchomionej kolekcji. Obecny kanał instalatora to **wersja zapoznawcza**; opiera się on na opublikowanych, sprawdzonych kompilacjach z `main`, których commit może być nowszy niż ostatnia numerowana wersja na GitHubie. Wersja strony pochodzi z `pyproject.toml`; jej commit i identyfikator kompilacji pozwalają rozróżnić aktualizacje w ramach tej samej wersji podglądowej.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

Należy użyć tego samego folderu instalacyjnego i tego samego użytkownika systemu operacyjnego, co poprzednio. Należy wykonać kopię zapasową całego katalogu danych przy wyłączonej funkcji gromadzenia danych; `tgwitness paths` który go identyfikuje. Podpisany eksport nie stanowi pełnej kopii zapasowej instalacji.

**Instalacja w katalogu głównym systemu Ubuntu pod adresem `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Po pomyślnej instalacji:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

W przypadku instalacji przez użytkownika systemu Linux/macOS należy użyć oryginalnej `TGWITNESS_INSTALL_DIR` lub ustawienia domyślne i ponownie uruchom pierwsze polecenie instalacyjne. Przed aktualizacją zamknij panel działający w tle, a po jej zakończeniu uruchom go ponownie. W przypadku skonfigurowanej usługi w systemie Linux uruchom polecenie `tgwitness restart` polecenie.

**Windows:** zamknij uruchomiony panel, ponownie uruchom polecenie instalacyjne dla systemu Windows, a następnie otwórz `bin\tgwitness.cmd` w tej samej instalacji. Instalator zachowuje dane, sesje, ustawienia dostępu i klucze podpisujące. Przełącza program uruchamiający dopiero po pozytywnym przejściu testów przez nowe środowisko; nieudana instalacja pozostawia poprzedni program uruchamiający na swoim miejscu. Zachowaj kopię zapasową sprzed aktualizacji na wypadek zmian formatu przechowywania danych.

## Codzienne polecenia w systemie Ubuntu

| Polecenie | Wynik |
| --- | --- |
| `tgwitness open` | Aktualny adres URL panelu i klucz dostępu. |
| `tgwitness paths` | Dokładne ścieżki do programów, danych i instrukcji. |
| `tgwitness guide --print` | Instrukcja obsługi w trybie offline. |
| `tgwitness status` / `tgwitness logs` | Dostępność / dzienniki usług. |
| `tgwitness stop` / `tgwitness start` | Zatrzymaj / wznow usługę; zachowaj dane. |
| `tgwitness token rotate` | Wymień klucz administratora i zakończ sesje przeglądarki. |
| `tgwitness tunnel off` | Wyłącz publiczny szybki tunel; zachowaj panel lokalny. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Utwórz link do szybkiego tunelu / zmień jego adres. |

Zobacz [sekcję „Dostęp”](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/) , aby zapoznać się z tokenami współpracowników, sesjami i ograniczeniami adresów IP, a także sekcję [„Publikowanie instalatora”,](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) aby poznać proces wydawania wersji z GitHub do Cloudflare.

## Usuń TgWitness

Nie ma programu do odinstalowania: wystarczy zatrzymać panel i usunąć jego foldery. Usunięcie folderu danych powoduje nieodwracalne zniszczenie dzienników, kluczy podpisujących, sesji Telegrama oraz zapisanych plików. Zanim to zrobisz:

1. Wyeksportuj to, czego potrzebujesz (**Eksportuj → Pobierz podpisany plik ZIP**) i przechowuj odcisk palca klucza podpisu oraz punkty kontrolne poza tym komputerem. Aby zachować sam obszar roboczy, skopiuj cały folder danych po zatrzymaniu gromadzenia danych.
2. Usuń serwery utworzone w sekcji **„Dodatki” → „Serwer 24/7”** z **listy „Twoje serwery”** lub za pomocą `python -m tgwitness.cloud destroy`; dostawca nalicza opłaty za te serwery do momentu ich usunięcia.
3. Sesję każdego konta w Telegramie należy zakończyć w sekcji **Ustawienia → Urządzenia**. Usunięcie plików nie powoduje wylogowania sesji po stronie Telegrama.

**Instalacja w katalogu głównym systemu Ubuntu.** Zwróć uwagę na folder danych, zatrzymaj usługę, a następnie usuń usługę, foldery i skrót:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Instalacja dla użytkowników systemu Linux lub macOS.** Zamknij panel. Skonfigurowana usługa użytkownika w systemie Linux zostaje zatrzymana za pomocą `systemctl --user disable --now tgwitness-<ID>`; jego jednostka znajduje się w `~/.config/systemd/user/`. Następnie usuń plik `~/.local/share/tgwitness` (lub swoją `TGWITNESS_INSTALL_DIR`) oraz `~/.local/bin/tgwitness` skrót.

**Windows.** Zamknij panel i usuń `%LOCALAPPDATA%\TgWitness` (lub swój `TGWITNESS_INSTALL_DIR`). Instalator nie dodaje żadnej usługi, zaplanowanego zadania ani skrótu.
