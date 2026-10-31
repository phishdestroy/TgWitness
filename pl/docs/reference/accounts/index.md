# Konta i formaty sesji

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/

Zaloguj się za pomocą telefonu, kodu QR lub klucza autoryzacyjnego, zaimportuj sesje z aplikacji Telethon, Pyrogram lub Telegram Desktop oraz korzystaj z wielu kont jednocześnie.

TgWitness loguje się jako **konto użytkownika Telegrama** (a nie jako bot) za pośrednictwem protokołu MTProto, korzystając z Telethon. Każde konto funkcjonuje we własnym **obszarze** roboczym (zwanym *„workspace”* w API i narzędziach wiersza poleceń) z własną sesją, źródłami, dziennikiem i kluczem podpisującym.

Pliki sesji, ciągi sesji oraz klucze autoryzacyjne stanowią **uprawnienia do konta**: każdy, kto je posiada, może działać w imieniu tego konta. Nie zawierają one historii wiadomości.

> [!OSTRZEŻENIE] **Proszę nie korzystać z niczego, czego utraty nie mogą Państwo sobie pozwolić.** Zdecydowanie odradzamy podłączanie kont osobistych lub w inny sposób wartościowych, a także tworzenie identyfikatora API / skrótu API na koncie, które jest dla Państwa cenne. Nie chodzi tu o to, że TgWitness nie zostało przetestowane: Telegram ogranicza dostęp i trwale blokuje konta w sposób nieprzewidywalny — w przypadku liczby żądań, którą uznaje za nadmierną, niezależnie od klienta lub celu, bez odpowiedniej dokumentacji. Wiele blokad jest nieodwracalnych. Prosimy korzystać z dedykowanych kont. Płynny przebieg testów zależy od serwisu Telegram, a nie od oprogramowania, i nie gwarantuje niczego na przyszłość.

- [W skrócie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#at-a-glance)
- [Zanim zaczną Państwo: identyfikator API i skrót API](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Numer telefonu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#phone-number) · [Kod QR](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#qr-code) · [Klucz autoryzacyjny + identyfikator DC](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#auth-key--dc-id)
- [Pliki kont](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#pyrogram-session) · [Para „sesja + JSON”](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#telethon-stringsession) · [Konto JSON](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#account-json)
- [Określ, czym dysponują Państwo](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#identify-what-you-have) · [Formaty nieobsługiwane](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#unsupported-formats)
- [Wiele kont](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#multiple-accounts) · [Zapewnienie bezpieczeństwa plików kont](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#keeping-account-files-safe) · [Rozwiązywanie problemów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#troubleshooting)

## W skrócie

| Co Państwo posiadają | Zakładka **„Dodaj konto**” | Będą Państwo również potrzebować |
| --- | --- | --- |
| Numer telefonu oraz dostęp do kodów logowania | **Telefon** | Hasło do uwierzytelniania dwuskładnikowego (2FA), o ile jest włączone |
| Aplikacja Telegram otwarta na innym urządzeniu | **Kod QR** | Hasło do uwierzytelniania dwuskładnikowego (2FA), o ile jest włączone |
| Plik `.session` (Telethon lub Pyrogram) | **Pliki** | Opcjonalny plik JSON zawierający ustawienia aplikacji |
| `.session` + `.json` o tej samej nazwie | **Pliki** (proszę wybrać oba) | Zazwyczaj nic więcej |
| Folder „`tdata`” w aplikacji Telegram Desktop | **Pliki** (w formacie ZIP) | Lokalny kod dostępu do aplikacji na komputerze, o ile został ustawiony |
| Sesja StringSession w ramach Telethonu (tekst, `.txt`, `.tgwitness-session`) | **Pliki** | Nie jest wymagana oddzielna para API |
| `.json` z sesją lub kluczem uwierzytelniającym | **Pliki** | Nie jest wymagana oddzielna para API |
| Klucz autoryzacyjny (512 znaków szesnastkowych) oraz jego numer DC | **Klucz autoryzacyjny** | Opcjonalny identyfikator użytkownika |

TgWitness rozpoznaje pliki na podstawie ich **zawartości**, a nie nazw. Zmiana nazwy pliku nigdy nie powoduje jego konwersji.

## Zanim zaczną Państwo: identyfikator API i skrót API

Można się zalogować bez konieczności tworzenia aplikacji API serwisu Telegram. Jeśli żadna para nie została wprowadzona, zaimportowana ani wcześniej zapisana w obszarze roboczym, TgWitness wybiera parę z wbudowanej puli 50 publicznych par API (`tgwitness/api_pool.py`) w losowej kolejności. Jeśli Telegram odrzuci parę (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), wypróbowana zostanie następna, maksymalnie osiem na jedno logowanie; odrzucone pary są pomijane do momentu ponownego uruchomienia. Para, która umożliwiła zalogowanie, jest zapisywana wraz z kontem i ponownie wykorzystywana dla tego konta. **Identyfikator API** oraz **skrót API** identyfikują aplikację w systemie Telegram; same w sobie nie uprawniają one do autoryzacji konta.

Aby zamiast tego korzystać z własnej aplikacji (ryzyko dotyczy konta, na którym została ona zarejestrowana; zob. [„Dlaczego wbudowana pula API?”](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. Proszę otworzyć [stronę my.telegram.org](https://my.telegram.org) i zalogować się przy użyciu dowolnego numeru telefonu, który Państwo posiadają. Kod zostanie wysłany do aplikacji Telegram, a nie w wiadomości SMS.
2. Proszę wybrać **narzędzia do tworzenia interfejsów API**.
3. Proszę utworzyć aplikację: dowolny tytuł i skrócona nazwa (5–32 liter), platforma: **komputer stacjonarny**. Pola adresu URL i opisu można pozostawić puste.
4. Skopiuj **identyfikator API aplikacji (api_id**) (liczba) oraz skrót **API aplikacji** (**api_hash)** (32 znaki szesnastkowe).

W panelu, pod formularzem logowania, znajdują się pola**„ID API” i „Hash**”. W polu**„ID API**” można wkleić pojedynczą parę `api_id:api_hash`, co spowoduje wypełnienie obu pól. Jedna para może być wykorzystana dla wszystkich Państwa kont. Po pomyślnym zalogowaniu dane te są zapisywane w postaci zaszyfrowanej wyłącznie w tym obszarze roboczym i nigdy nie są przesyłane z powrotem do przeglądarki.

W grę wchodzą trzy różne rodzaje danych uwierzytelniających:

| Tajne | Otwiera | Gdzie można to znaleźć |
| --- | --- | --- |
| Token panelu | Panel internetowy TgWitness | `panel-token.txt` w katalogu danych lub `TGWITNESS_TOKEN` |
| Identyfikator API + skrót | Nie zawiera żadnych dodatkowych informacji; służy wyłącznie do identyfikacji aplikacji | Wbudowana para, zaimportowane ustawienia lub Państwa własna aplikacja na stronie my.telegram.org |
| Autoryzacja konta | Konto w serwisie Telegram | Tworzone poprzez logowanie za pomocą telefonu lub kodu QR albo importowane jako sesja |

Jeśli dostęp do serwisu Telegram wymaga korzystania z serwera proxy, należy najpierw skonfigurować to w menu **Konto → Ustawienia → Ustawienia połączenia → Zmień trasę połączenia**.

## Numer telefonu

1. Proszę otworzyć **konto**, przejść do zakładki **„Telefon**” i wprowadzić numer w formacie międzynarodowym, na przykład `+44 7700 900123`. Spacje i myślniki są usuwane automatycznie.
2. Proszę kliknąć **„Kontynuuj**”. Pola „API ID” i „Hash” mogą pozostać puste.
3. Wprowadź kod wysłany przez Telegram (zazwyczaj do aplikacji Telegram; nie gwarantuje się otrzymania kodu SMS-em).
4. Jeśli konto posiada weryfikację dwuetapową, proszę wprowadzić to hasło. Nie jest to token panelu ani kod dostępu do urządzenia.
5. Proszę sprawdzić identyfikator konta wyświetlany po zalogowaniu, a następnie wybrać źródła.

Kody logowania oraz hasło do uwierzytelniania dwuskładnikowego (2FA) nigdy nie są zapisywane na dysku.

## Kod QR

Należy z tego skorzystać, gdy konto jest już zalogowane na telefonie lub innym komputerze.

1. Zakładka **„Kod QR”** → **Wyświetl kod QR**. Pola „ID API” i „Hash” mogą pozostać puste.
2. Na zalogowanym urządzeniu: **Ustawienia → Urządzenia → Połącz urządzenie stacjonarne**, zeskanuj kod i potwierdź.
3. Wprowadź hasło 2FA w TgWitness, jeśli Telegram o to poprosi.

Obraz kodu QR jest generowany lokalnie. Kody tracą ważność; proszę nacisnąć przycisk **„Wygeneruj kolejny kod QR”,** aby spróbować ponownie. Zablokowanie panelu, zmiana obszaru roboczego lub rozpoczęcie kolejnego logowania powoduje anulowanie kodów oczekujących na wykorzystanie.

## Klucz autoryzacyjny + identyfikator DC

Klucz autoryzacyjny to surowy 256-bajtowy klucz autoryzacyjny stanowiący podstawę każdej sesji w Telegramie, zapisany jako **512 znaków szesnastkowych** wraz z numerem centrum danych **DC 1–5**.

1. Zakładka **„Klucz autoryzacyjny**”. Proszę wkleić pełny klucz; skrócony klucz zawierający sekwencję „`…`” nie będzie działał.
2. Proszę wybrać identyfikator DC dostarczony wraz z kluczem.
3. Opcjonalnie można wprowadzić **identyfikator użytkownika**. W takim przypadku TgWitness odmówi nawiązania połączenia, jeśli Telegram zgłosi inne konto.
4. **Konto** Press **Connect**.

Klucz autoryzacyjny (512 znaków) nie jest skrótem API (32 znaki). Ten sam klucz można również zaimportować w formacie JSON – zob. [JSON konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#account-json).

## Pliki kont

Otwórz opcję **„Dodaj konto” → „Pliki”** i wybierz maksymalnie **cztery pliki należące do jednego konta**, o łącznej wielkości **8 MiB**, a następnie naciśnij przycisk **„Połącz konto**”.

- Pliki są konwertowane **w pamięci** na serwerze TgWitness. Przesłane dane nie są przechowywane, pliki ZIP nie są rozpakowywane na dysk, a także nie nawiązywane są połączenia z żadnymi usługami zewnętrznymi.
- Uzyskany zapis jest następnie weryfikowany w serwisie Telegram. Jeśli plik zawiera identyfikator użytkownika, musi on być zgodny z danymi konta podanymi przez serwis Telegram.
- Pliki opisujące różne konta lub różne dane uwierzytelniające API są odrzucane zamiast wybrania jednego z nich.
- Pole **„Kod dostępu lub tekst sesji”** zawiera lokalne pole kodu dostępu TData – pole służące do wklejenia obiektu StringSession oraz **odczytu plików bez konieczności logowania się** (wypełnia formularz bez nawiązywania połączenia z serwisem Telegram).

### Telethon `.session`

|  |  |
| --- | --- |
| Czym jest | Baza danych SQLite tworzona przez narzędzia oparte na Telethon, na przykład `my_account.session` |
| Uznane przez | Tabele `sessions` (wraz z `dc_id`, `server_address`, `port`, `auth_key`) oraz `version` = 7 lub 8 |
| Wymagania | Dokładnie jeden wiersz sesji autoryzowanej; zamknięta, kompletna baza danych |

Najpierw należy zamknąć program, który utworzył plik. Jeśli obok niego znajduje się plik `my_account.session-journal` lub `my_account.session-wal`, oznacza to, że baza danych nie została sfinalizowana: należy otworzyć i poprawnie zamknąć oryginalnego klienta. Usunięcie tych plików pomocniczych może spowodować powstanie uszkodzonej kopii.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Czym jest | Baza danych SQLite tworzona przez narzędzia oparte na Pyrogramie |
| Uznane przez | Tabela `sessions` wraz z `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 lub 3 |
| Wymagania | Jedna autoryzowana sesja **użytkownika** w sieci produkcyjnej. Sesje botów i serwerów testowych (test-DC) są odrzucane. |

Podczas logowania zapisany identyfikator użytkownika jest weryfikowany w serwisie Telegram.

### Para „sesja + JSON”

Zbiory danych są często udostępniane w postaci dwóch plików o tej samej nazwie, na przykład `447700900123.session` i `447700900123.json`. Proszę zaznaczyć **oba pliki** jednocześnie.

- Na podstawie danych JSON TgWitness korzysta z `app_id`/`api_id` oraz `app_hash`/`api_hash`, więc zazwyczaj nie ma potrzeby ręcznego wprowadzania danych uwierzytelniających API.
- Inne pola, takie jak `phone`, `device`, `sdk`, `app_version`, `lang_pack` lub zapisane hasło `twoFA`, są **ignorowane**. Jeśli konto posiada uwierzytelnianie dwuskładnikowe (2FA), TgWitness prosi o jego podanie.
- Sam plik JSON zawiera jedynie metadane. W przypadku braku pliku sesji proszę kontynuować, logując się za pomocą telefonu lub kodu QR.

### Telegram Desktop (TData)

TData to folder `tdata` aplikacji Telegram Desktop (aplikacja wieloplatformowa dostępna na stronie desktop.telegram.org).

| System | Domyślna lokalizacja: `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (przenośna wersja Telegrama: obok `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Aby je zaimportować:

> **Ostrzeżenie dotyczące sesji równoległych.** Importowanie danych TData powoduje ponowne wykorzystanie klucza autoryzacyjnego aplikacji Telegram Desktop; nie tworzy to niezależnego loginu. Proszę nie używać tego klucza jednocześnie w aplikacji Desktop i TgWitness. Telegram może unieważnić autoryzację za pomocą kodu `AUTH_KEY_DUPLICATED`, co spowoduje, że obie kopie staną się bezużyteczne do momentu wykonania nowego logowania.
>
>
>
> Proszę całkowicie zamknąć aplikację Desktop, w tym proces w zasobniku systemowym, i pozostawić tę kopię zamkniętą na czas, gdy TgWitness korzysta z zaimportowanej sesji. **Proszę zamknąć aplikację, nie wylogowywać się ani nie unieważniać sesji:** unieważnienie powoduje również unieważnienie zaimportowanej kopii. Jeśli konieczne jest uruchomienie obu klientów, proszę zalogować się do TgWitness za pomocą telefonu lub kodu QR, aby utworzyć własną autoryzację. Zaleca się utworzenie dedykowanego konta, jednak nie gwarantuje to bezpieczeństwa równoległego korzystania ze sklonowanych kluczy.
>
>
>
> Dotyczy to również zaimportowanych plików `.session`, tekstu StringSession oraz klucza autoryzacyjnego w formacie HEX. Inni klienci posiadający własne, niezależnie utworzone uprawnienia mogą pozostać zalogowani. Zobacz [dokumentację Telegramu dotyczącą AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Proszę całkowicie zamknąć aplikację Telegram Desktop.
2. Proszę utworzyć plik ZIP zawierający **wyłącznie** te dwa elementy z `tdata`:

   - `key_datas`
   - 16-znakowy plik zakończony na „`s`”, znajdujący się obok, zazwyczaj „`D877F783D5D3EF8Cs`”

   Skompresowanie całego folderu wraz z pamięcią podręczną multimediów zazwyczaj przekracza limity (512 wpisów, 32 MiB po rozpakowaniu). 3. Wybierz plik ZIP w sekcji **„Pliki**”. Jeśli aplikacja Telegram Desktop posiada **lokalny kod dostępu**, należy go najpierw wprowadzić w polu **„Kod dostępu” lub „Tekst sesji**”. Nie jest to hasło do uwierzytelniania dwuskładnikowego (2FA).

Obsługiwane: jedno konto na archiwum, nowoczesna pamięć masowa typu `key_datas`/`key_data0`/`key_data1`, lokalny kod dostępu. Nieobsługiwane: foldery zawierające konta z wieloma zalogowanymi użytkownikami, starsze wersje aplikacji na komputery stacjonarne, pliki ZIP chronione hasłem oraz oddzielna natywna aplikacja dla systemu macOS „Telegram dla macOS”.

### Telethon StringSession

Pojedynczy wiersz tekstu, zazwyczaj zaczynający się od `1` i zawierający około 350 znaków. Proszę wgrać go jako plik `.txt` lub `.tgwitness-session` (maksymalnie 4 KiB) lub wkleić w polu **„Kod dostępu” lub „Tekst sesji**”. Akceptowane są wyłącznie ciągi znaków w formacie Telethon; ciągi znaków w formatach Pyrogram i TDLib mają inne formaty.

### Konto JSON

Jeden obiekt JSON o rozmiarze maksymalnie **64 KiB**, umieszczony w pliku o rozszerzeniu **`.json`**.

| Pole (pseudonimy) | Znaczenie |
| --- | --- |
| `api_id` (`app_id`) | Identyfikator aplikacji – liczba dodatnia |
| `api_hash` (`app_hash`) | Skrót aplikacji, 32 znaki szesnastkowe |
| `string_session` (`session_string`, `session`) | Tekst „Telethon StringSession”, a nie nazwa pliku |
| `auth_key` (`auth_key_hex`) + `dc_id` | Pełny klucz autoryzacyjny o długości 512 znaków oraz DC 1–5 |
| `user_id` (`id`) | Opcjonalnie; weryfikacja w serwisie Telegram przed zapisaniem upoważnienia |

Jeśli podano zarówno pseudonim, jak i imię i nazwisko, muszą one być ze sobą zgodne. Przykłady:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

W pierwszym przykładzie należy jedynie wprowadzić dane uwierzytelniające API; należy zalogować się za pomocą telefonu lub kodu QR albo dodać plik sesji. Listy zbiorcze (tablica JSON zawierająca konta) nie są akceptowane.

## Określ, czym dysponują Państwo

| Jak widać | Jest to | Zastosowanie |
| --- | --- | --- |
| `*.session`; po otwarciu w edytorze tekstu na początku widoczny jest napis `SQLite format 3` | Telethon lub Pyrogram SQLite | **Pliki** (wykrywane automatycznie) |
| Folder „`tdata`” zawierający plik „`key_datas`” | Telegram Desktop TData | Spakuj dwa pliki do formatu ZIP, a następnie **Pliki** |
| Jeden wiersz tekstu zaczynający się od `1`, około 350 znaków | Telethon StringSession | **Pliki** |
| `*.json` wraz z `app_id`/`app_hash` | Metadane towarzyszące | **Pliki** wraz z danymi sesji |
| `*.json` wraz z `auth_key` lub `string_session` | Konto JSON | **Pliki** |
| 512 znaków `0-9a-f` | Klucz autoryzacyjny | **Klucz autoryzacyjny** |
| 32 znaki `0-9a-f` | Skrót API | **Identyfikator API + skrót** |
| `td.binlog` lub `db.sqlite` z aplikacji TDLib | Magazyn TDLib | Nieobsługiwane |
| `123456789:AA…` | Token bota | Nieobsługiwane |

## Formaty nieobsługiwane

| Format | Alternatywa |
| --- | --- |
| Magazyn TDLib (`td.binlog`) oraz eksporty z TDLib | Zaloguj się za pomocą telefonu lub kodu QR |
| **Ciągi** sesji programu Pyrogram | Proszę skorzystać z pliku Pyrogram o numerze `.session` lub skanować kod QR za pomocą telefonu. |
| TData z kilkoma zalogowanymi kontami | Wyloguj się z pozostałych kont w aplikacji Telegram Desktop lub skorzystaj z pliku sesji przypisanego do każdego konta |
| Tokeny botów | Nieobsługiwane: TgWitness obserwuje jako konto użytkownika |
| Listy wielu kont w formatach CSV/JSON | Należy dodać jeden obszar roboczy na każde konto |
| Sesje testowe DC lub sesje z wykorzystaniem botów | Należy korzystać z produkcyjnego konta użytkownika |

## Wiele kont

Naciśnij przycisk **+** obok selektora konta lub otwórz **Konto → Ustawienia → Ustawienia połączenia → Obszary robocze**, wprowadź nazwę i zaloguj się.

- Dowolna liczba obszarów roboczych, w tym obszar główny. Każdy z nich posiada własną sesję, trasę proxy, źródła, zasady przechwytywania, dziennik, klucz podpisujący, punkty kontrolne oraz opcje eksportu.
- Przełączenie wyświetlanego obszaru roboczego nie powoduje wstrzymania działania pozostałych.
- Dziennik pozostaje powiązany z kontem, które go utworzyło. Zalogowanie się przy użyciu innego konta wymaga utworzenia kolejnego obszaru roboczego, a jedno konto nie może być przypisane do dwóch obszarów roboczych.
- Główny token panelu kontroluje wszystkie obszary robocze. [Przyznany dostęp](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/) może ograniczać innym osobom dostęp do wybranych kont i czatów, z oddzielnymi uprawnieniami i limitami sesji.
- **Funkcja „Konta”** zmienia nazwę obszaru roboczego oraz usuwa dodany obszar wraz z jego sesją, dziennikiem, źródłami i kluczem podpisującym. Głównego obszaru roboczego nie można usunąć z panelu.

### Import zbiorczy i grupy kont

Otwórz **Konta → Importowanie kont**, aby dodać wiele kont, dopasować pliki według nazwy i sprawdzić wynik każdego logowania. Każde konto otrzymuje własny obszar roboczy. Grupy mogą kopiować wybrane ustawienia ze wzorca bez łączenia sesji, kluczy ani dowodów. Zobacz [przewodnik po imporcie i grupach](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) i [panel puli MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Wyloguj się

**Konto → Wyloguj się z Telegrama** (z wstrzymanym monitorowaniem) powoduje, że Telegram kończy sesję, w związku z czym znika ona również z sekcji **Ustawienia → Urządzenia** danego konta oraz jest usuwana z magazynu obszaru roboczego. Dziennik, źródła, ustawienia i klucz podpisujący pozostają, a dziennik rejestruje fakt wylogowania. Obszar roboczy nadal należy do danego konta: tylko to konto może ponownie nawiązać z nim połączenie. Jeśli aplikacja Telegram nie odpowiada, sesja i tak zostanie usunięta w tym miejscu, a panel wyświetli odpowiedni komunikat; należy ją zakończyć w aplikacji Telegram w sekcji **Ustawienia → Urządzenia**.

## Konwersja sesji Telethon w trybie offline

Panel importuje bezpośrednio pliki `.session`. Aby przeprowadzić konwersję w trybie offline do pliku StringSession, należy uruchomić z folderu projektu:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Konwerter odczytuje wyłącznie pliki Telethon SQLite (o rozmiarze do 64 MiB), nigdy nie modyfikuje danych wejściowych, nie wysyła żadnych żądań sieciowych i nie nadpisuje istniejących plików wyjściowych.

## Zapewnienie bezpieczeństwa plików kont

- Każdy plik `.session`, TData ZIP, StringSession, klucz autoryzacyjny oraz plik JSON konta należy traktować jak hasło. TgWitness przechowuje zaimportowane dane autoryzacyjne w zaszyfrowanym sejfie; po zakończeniu można usunąć oryginalne pliki.
- Nie należy uruchamiać tej samej autoryzacji w dwóch programach jednocześnie. Telegram może ją cofnąć (`AUTH_KEY_DUPLICATED`), co spowoduje, że obie kopie przestaną działać.
- Wygasłej lub unieważnionej sesji nie można przywrócić poprzez konwersję. Proszę zalogować się ponownie.

## Rozwiązywanie problemów

| Wiadomość lub symptom | Co należy zrobić |
| --- | --- |
| *Nie można odczytać tej sesji. Proszę zamknąć jej oryginalny klient…* | Plik SQLite jest otwarty lub niekompletny (plik pomocniczy `-journal`/`-wal`). Proszę poprawnie zamknąć oryginalny program i ponownie skopiować plik. |
| *Obsługiwane schematy bazy danych Telethon SQLite: 7 i 8* / *Pyrogram … 2 i 3* | Plik został utworzony przy użyciu bardzo starej lub nieznanej wersji biblioteki. Proszę zalogować się za pomocą telefonu lub kodu QR. |
| *Obsługiwane są wyłącznie sesje autoryzowanych użytkowników produkcyjnych* | Plik Pyrogram należy do bota lub sieci testowej. |
| *Archiwum TData przekracza 512 wpisów lub 32 MiB* | Proszę przesłać wyłącznie pliki ZIP o nazwach „`key_datas`” i „`D877F783D5D3EF8Cs`”, a nie cały folder. |
| *Nie można odszyfrować pliku TData. Proszę sprawdzić lokalne hasło dostępu na komputerze stacjonarnym.* | W polu **„Kod dostępu” lub „Tekst sesji**” należy wprowadzić lokalny kod dostępu do aplikacji Telegram Desktop. |
| *Importuj po jednym koncie TData na raz* | Aplikacja Telegram Desktop obsługiwała kilka kont; zob. sekcję [„Nieobsługiwane formaty](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#unsupported-formats)”. |
| *Wybrane pliki opisują różne konta lub dane uwierzytelniające API* | Proszę wybrać pliki wyłącznie z jednego konta. |
| *Plik JSON nie zawiera żadnych obsługiwanych danych uwierzytelniających ani uprawnień API* | Proszę sprawdzić nazwy pól w [pliku JSON konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#account-json). |
| *Wyłącznie metadane API* | Plik JSON nie zawiera sesji. Proszę dodać plik `.session` lub skorzystać z telefonu/kodu QR. |
| *Klucz autoryzacyjny w formacie HEX musi zawierać wszystkie 512 znaków szesnastkowych* | Klucz jest skrócony lub zawiera sekwencję „`…`”. |
| Identyfikator konta nie zgadza się z importowanym kontem | Identyfikator użytkownika podany w pliku różni się od tego, który podaje Telegram; plik dotyczy innego konta. |
| Konto należy już do innego obszaru roboczego | Proszę otworzyć ten obszar roboczy zamiast dodawać konto dwukrotnie. |
| Połączenie nawiązane, jednak na liście czatów w **sekcji „Źródła”** brakuje grupy prywatnej | Proszę sprawdzić członkostwo. Narzędzie analizuje pierwsze 1 000 rozmów; limit ten można zwiększyć w sekcji **„Parametry**”. |
| Błąd połączenia z serwerem proxy | Proszę sprawdzić tryb routingu i tryb IP. Automatyczny tryb MTProxy próbuje połączyć się z innym działającym węzłem. Tryb ukrywania adresu IP oczekuje; wyraźnie wybrany tryb awaryjny może nawiązać bezpośrednie połączenie po upływie skonfigurowanego opóźnienia. Zobacz [tryby routingu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes). |

Zobacz również: [połączenia i bezpieczeństwo](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) w odniesieniu do serwerów proxy i szyfrowania, oraz [sposób działania procesu gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/) dotyczących treści przechwyconych po zalogowaniu.
