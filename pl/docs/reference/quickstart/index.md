# Szybki start

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/

Wszystkie sposoby instalacji i uruchomienia TgWitness: pakiet dla systemu Windows, Python, Docker oraz syntetyczna wersja demonstracyjna wraz z wstępnymi testami.

**Język angielski** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ukraiński](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Chiński uproszczony](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness to samodzielna aplikacja służąca do monitorowania grup i kanałów w serwisie Telegram, do których mają Państwo dostęp za pośrednictwem swoich kont. Działa ona lokalnie, korzystając z własnego katalogu danych.

**Pierwsza wizyta?** [Zapoznaj się z wersją demonstracyjną](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/#explore-the-interface) przed podłączeniem konta. [Wybierz przewodnik](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) dotyczący serwerów proxy, świadków, eksportu danych lub konfiguracji serwera.

## Zainstaluj i uruchom

[Zbieranie przez GitHub Actions (wersja wstępna)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Proszę wybrać jedną z metod. Pliki do pobrania w wersji przenośnej stają się dostępne po opublikowaniu kompilacji wydaniowej:

| Host | Nie wymaga instalacji | Źródło: Python 3.11+ | Docker: Engine/Desktop z Compose w wersji 2.20 lub nowszej |
| --- | --- | --- | --- |
| Windows | Proszę pobrać plik „`TgWitness-<version>-windows-amd64-portable.zip`” z sekcji „GitHub Releases”, a następnie kliknąć dwukrotnie plik „`TgWitness.cmd`” | Proszę dwukrotnie kliknąć `Start.cmd` | Proszę dwukrotnie kliknąć `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

W przypadku metod opartych na kodzie źródłowym [pobierz i rozpakuj bieżącą gałąź `main`](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) lub sklonuj repozytorium:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Bieżący kod źródłowy obejmuje zbiorczy import kont, panel MTProxy oraz wznawiane ładowanie historii. Wersja przenośna 0.7.0 preview oraz jej archiwum kodu źródłowego powstały przed wprowadzeniem tych funkcji. Zobacz [dziennik zmian](https://phishdestroy.github.io/TgWitness/pl/docs/reference/changelog/), aby sprawdzić granice wersji.

Skrypt `Start.cmd` proponuje instalację Pythona 3.12 dla użytkownika systemu Windows, jeśli nie zostanie znaleziony odpowiedni Python (przez winget lub podpisany instalator z python.org). Skrypt `start.sh` wypisuje dokładne polecenie instalacyjne dla danej dystrybucji systemu Linux lub systemu macOS, jeśli brakuje Pythona. Pierwsze uruchomienie ze źródeł automatycznie tworzy środowisko `.venv` i instaluje zależności.

Docker kompiluje aplikację i uruchamia ją w tle; nie jest wymagane środowisko Python na hostie. Polecenia ``scripts\Docker.cmd`` i ``scripts/docker-start.sh`` wyświetlają adres panelu oraz token, gdy kontener działa poprawnie. Odpowiednie polecenia Docker na każdym obsługiwanym hoście to:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Otwórz stronę **http://127.0.0.1:8787**. Proszę użyć tokenu wygenerowanego przez narzędzie pomocnicze Docker lub drugiego polecenia Docker, albo odczytać **plik data/live/panel-token.txt** w przypadku instalacji przenośnej lub źródłowej. Proszę przejść do sekcji **„Połącz z Telegramem**” poniżej. Instalacje natywne i w środowisku Docker korzystają z oddzielnych przestrzeni dyskowych; uruchomienie Docker nie powoduje zaimportowania istniejącego dziennika z instalacji natywnej.

W przypadku serwera [wdrożenie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/) obejmuje automatyczne włączenie protokołu HTTPS, restart, publikowane obrazy, aktualizacje oraz kopie zapasowe.

## Zapoznaj się z interfejsem

1. Należy uruchomić **plik „TgWitness-Demo.cmd”** w pakiecie przenośnym, **„scripts\Demo.cmd”** w folderze źródłowym systemu Windows lub „`sh start.sh --demo` ” w systemie Linux/macOS. Uruchomienie z folderu źródłowego powoduje najpierw utworzenie pliku „`.venv` ” oraz zainstalowanie zależności.
2. Otwórz stronę **http://127.0.0.1:8787**.
3. Lokalna wersja demonstracyjna automatycznie otwiera przykładowy dziennik. Do bezpośredniego dostępu lokalnego nie jest wymagana kopia tokenu.

Wiadomości demonstracyjne są fikcyjne. Tryb demonstracyjny nie umożliwia połączenia z prawdziwym kontem w Telegramie.

## Połącz się z Telegramem

> [!OSTRZEŻENIE] **Proszę nie korzystać z niczego, czego utraty nie mogą Państwo sobie pozwolić.** Zdecydowanie odradzamy podłączanie kont osobistych lub wartościowych oraz tworzenie identyfikatora API / skrótu na koncie, które jest dla Państwa cenne. Telegram blokuje konta w sposób nieprzewidywalny i często na stałe, niezależnie od używanego klienta. Płynny przebieg testu zależy od serwisu Telegram, a nie od TgWitness, i nie gwarantuje niczego na przyszłość.

1. Jeśli uruchomiona jest natywna wersja demonstracyjna, należy ją zatrzymać i uruchomić **plik Start.cmd** lub `sh start.sh`. W przeciwnym razie należy pozostawić uruchomioną instalację na żywo, o której mowa powyżej.
2. Aby otworzyć panel, należy użyć tokenu panelu odpowiadającego Państwa metodzie instalacji.
3. Jeśli potrzebują Państwo serwera proxy, proszę zapisać go w sekcji **Konto → Ustawienia → Ustawienia połączenia → Zmień trasę połączenia**.
4. W sekcji **„Konto**” proszę wprowadzić swój numer telefonu i nacisnąć **„Kontynuuj**”, wybrać opcję **„Kod QR” → „Pokaż kod QR**” lub wybrać pliki i nacisnąć **„Połącz konto**”. **Identyfikator API + skrót** są opcjonalne: obszar roboczy wykorzystuje zapisaną lub zaimportowaną parę, lub działającą parę z wbudowanej puli. Aby skorzystać z własnej aplikacji, proszę wkleić jedną parę `API ID:API Hash` w polu „Identyfikator API”. Aby uzyskać pełny klucz autoryzacyjny, wybierz **opcję „Klucz autoryzacyjny”**, wklej wszystkie 512 znaków szesnastkowych i wybierz podany identyfikator DC. Identyfikator użytkownika jest opcjonalny i zostanie zaznaczony, jeśli zostanie wprowadzony.
5. Proszę dokończyć wybraną metodę logowania: numer telefonu/kod/2FA, potwierdzenie z zalogowanej aplikacji Telegram w przypadku kodu QR lub import obsługiwanej, autoryzowanej sesji.
6. Proszę sprawdzić wyświetlony identyfikator konta. **Źródła** otwarte: Państwa czaty ładują się automatycznie; proszę dodać swoje grupy.
7. W sekcji **„Wybierz zmiany**, **które mają zostać zachowane**” proszę wybrać kategorie zdarzeń lub gotowy zestaw **„Wiadomości, edycje i usunięcia”**, a następnie zapisać ustawienia monitorowania.
8. Proszę wybrać ustawienia załączników osobno, a następnie nacisnąć przycisk **„Rozpocznij obserwację**”.

Dane uwierzytelniające API identyfikują Państwa aplikację; same w sobie nie uprawniają one do korzystania z konta. Grupy prywatne nie wymagają publicznej nazwy użytkownika, jednak Państwa konto musi posiadać do nich dostęp.

W przypadku istniejących kont zobacz [konta i formaty sesji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/): panel obsługuje Telethon StringSession, Telethon/Pyrogram SQLite, archiwa ZIP TData pojedynczych kont oraz obsługiwane pliki JSON kont. Wybierz jednocześnie plik sesji i towarzyszący mu plik JSON, a następnie naciśnij **Połącz konto**. Logowanie kodem QR jest również dostępne z tymi samymi opcjonalnymi ustawieniami API. Sesje TDLib, sesje botów oraz wykazy kont w formatach CSV/JSON nie są obsługiwane.

W przypadku kilku kont użyj opcji **Konta → Importowanie kont** i wybierz obsługiwane pliki sesji. Towarzyszące pliki JSON są parowane na podstawie nazwy bazowej; każde zaimportowane konto otrzymuje własny obszar roboczy. Zobacz [import zbiorczy i grupy kont](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#bulk-import-and-account-groups).

Aby dodać kolejne konto, proszę nacisnąć przycisk **+** obok selektora kont lub otworzyć **Konto → Ustawienia → Ustawienia połączenia → Obszary robocze**, albo skorzystać z **opcji Konta**. Obszary robocze mają oddzielne sesje, dzienniki, klucze, źródła i kolejki. Przełączanie widoków nie powoduje zatrzymania działania pozostałych modułów zbierających dane. W tej instalacji to samo konto Telegram nie może być przypisane do dwóch obszarów roboczych. Nie ma ustalonej liczby obszarów roboczych; współdzielą one jeden proces, więc ich wydajność zależy od komputera.

Token panelu na żywo zabezpiecza dostęp do Państwa uprawnień w Telegramie oraz zapisanych materiałów; jest on odrębny od danych uwierzytelniających do API serwisu Telegram. Tylko wyraźnie uruchomiona, bezpośrednio dostępna lokalna wersja demonstracyjna otrzymuje automatyczny wpis. Wersja demonstracyjna zdalna lub korzystająca z serwera proxy nadal wykorzystuje token `data/demo/panel-token.txt`.

## Przeglądanie i eksportowanie

- **Dziennik:** wyszukiwanie i filtrowanie obserwacji według źródła i typu zdarzenia.
- Proszę wybrać zdarzenie, aby sprawdzić jego oryginalny zapis, informacje o autorstwie oraz zapisane wersje.
- Szczegóły edycji pokazują treść przed i po zmianie. Szczegóły usunięcia pokazują ostatnią zarejestrowaną treść, o ile taka istnieje; tożsamość nieznanego podmiotu pozostaje nieznana.
- **Formaty eksportu:** podpisane pliki ZIP, JSONL, CSV oraz HTML do użytku offline.
- **Eksport pełnej**historii**czatu** (Źródła → Eksport pełnej historii czatu): pobierz całą widoczną historię jednego czatu w postaci podpisanego pakietu z `chat.json` (w formacie eksportu Telegramu) oraz czytelnego `chat.html`. Czat prywatny działa, gdy konto jest członkiem grupy. Jest to aktualna migawka, a nie rekonstrukcja usuniętych lub wcześniej edytowanych wiadomości. Proszę zweryfikować kopię za pomocą `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Punkt kontrolny:** należy zachować granicę podpisanego dziennika poza kolektorem.
- **Pobierz podpisane potwierdzenie uruchomienia:** zachowaj zapis dotyczący programu i wersji narzędzia zbierającego dane.
- **Przygotowanie żądania znaku czasu:** należy przygotować żądanie offline skierowane do serwisu generującego znaki czasu; należy postępować zgodnie z instrukcją zawartą w pliku [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/) w celu uzyskania i zweryfikowania odpowiedzi.
- **Weryfikacja dziennika:** sprawdzenie podpisów zdarzeń i ogniw łańcucha. Eksport do pliku ZIP obejmuje również pliki multimedialne.

Obsługiwane przeglądarki zapisują duże pliki eksportowe bezpośrednio do wybranego pliku. Inne przeglądarki buforują maksymalnie 128 MiB. Gdy serwer działa, interfejs CLI do strumieniowego przesyłania danych obsługuje większe pliki do pobrania bez konieczności buforowania całej odpowiedzi:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Aby dodać kolejne środowisko pracy, należy wprowadzić `--profile ID`, korzystając z **opcji Eksportuj → Identyfikator środowiska pracy**. W przypadku serwera zdalnego należy wprowadzić `--url https://your-server`. Domyślny limit transferu wynosi 5 GiB; opcja „`--max-mib`” pozwala go zmienić. Podpisana zawartość pliku ZIP ma domyślnie oddzielny limit weryfikacji w wysokości 4 GiB w postaci nieskompresowanych danych (**opcja „Parametry”** pozwala go zwiększyć; archiwa tego typu należy weryfikować za pomocą opcji „`verify.py --max-gib N`”). Proszę zweryfikować archiwum przy użyciu zaufanej kopii programu weryfikującego oraz niezależnie przechowywanego odcisku klucza/punktu kontrolnego.

## Sprawdź instrukcję instalacji

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` sprawdza lokalne zależności, obsługę podpisywania, pamięć masową, konfigurację kluczy oraz adres nasłuchujący. Nie instaluje żadnych elementów ani nie łączy się z Telegramem. Zajęty port może oznaczać, że działa inna instancja. Proszę użyć innego `--port` lub najpierw ją zatrzymać.

Program uruchamiający instaluje się w katalogu `.venv`. Polecenia pomocnicze `python -m tgwitness...` muszą korzystać z `.venv\Scripts\python.exe` w systemie Windows lub `.venv/bin/python` w systemach Linux/macOS, o ile dane środowisko nie zostało już aktywowane.

## Sesje, zabezpieczenia i działanie

Zamknięty, spójny plik Telethon SQLite `.session` można przekonwertować lokalnie za pomocą `python -m tgwitness.sessions account.session --out account.tgwitness-session`, a następnie załadować do konta. Dostępne są również bezpośredni import plików oraz logowanie za pomocą kodu QR. Informacje na temat formatów logowania, protokołów SOCKS5, HTTP CONNECT, MTProxy oraz zewnętrznych kluczy głównych można znaleźć [w pliku CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/).

**Wstrzymanie obserwacji** powoduje zatrzymanie gromadzenia danych. **Zablokowanie** ogranicza jedynie dostęp przez przeglądarkę. Zamknięcie karty nie powoduje zakończenia działania procesu gromadzenia danych. Zatrzymanie procesu przerywa gromadzenie danych; migawka historii nie pozwala na odtworzenie wszystkich pominiętych edycji lub usunięć. Zapoznaj się z [zasadami działania gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/) w odniesieniu do reguł zdarzeń, kolejek załączników, izolacji kont oraz zachowania przy ponownym uruchomieniu.

Sesje i dane poufne są szyfrowane. Treść wiadomości, pliki multimedialne oraz eksportowane dane wymagają szyfrowanego dysku lub woluminu. Podpisy potwierdzają integralność w odniesieniu do zaufanego klucza; nie potwierdzają one jednak pochodzenia z serwisu Telegram ani nie zapobiegają fałszowaniu danych przez operatora, który kontroluje narzędzie gromadzące dane oraz jego klucz.

Proszę zapoznać się z [plikiem OPERATIONS.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/operations/) w sprawie tworzenia kopii zapasowych i przywracania danych, z [plikiem DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/) w sprawie hostingu oraz z [katalogiem deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) zawierającym przykłady usług. Zainstalowany panel zawiera również przewodnik po konfiguracji w trybie offline dostępny pod adresem `/guide.html`.

Rzeczywisty stan weryfikacji oraz pozostałe ograniczenia zostały opisane w plik[ach VERIFICATION.md](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/) i [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
