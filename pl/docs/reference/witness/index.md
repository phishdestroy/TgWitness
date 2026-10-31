# Niezależny świadek

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/

Uruchom program Witness z własnym kluczem i botem, opublikuj podpisane punkty kontrolne na kanale i porównaj z nimi wyeksportowane dane.

[Konfiguracja bota i serwera proxy w języku rosyjskim](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Moduł zbierający podpisuje swój własny dziennik, więc każdy, kto kontroluje ten moduł oraz jego klucz, mógłby w zasadzie przeredagować lub skrócić dziennik, a następnie podpisać go ponownie. Świadek sprawia, że jest to wykrywalne. Jest to odrębny proces — inny kontener, a raczej serwer obsługiwany przez inną osobę — który co kilka minut pobiera podpisaną czołówkę dziennika kolektora, podpisuje to, co zauważył, własnym kluczem, przechowuje to we własnym dzienniku i publikuje na kanale Telegramu.

Schemat blokowy · Collector → Witness (podpisany punkt kontrolny: liczba zapisów + skrót nagłówka); Witness → Dziennik Witness, własny klucz; Witness → Kanał na Telegramie (podpisany wpis za pośrednictwem własnego bota); Plik ZIP z dowodami → verify.py; Dziennik Witness, własny klucz → verify.py; Kanał na Telegramie → verify.py (Eksport z aplikacji Telegram Desktop lub strona t.me/s) · Collector · Witness · Dziennik Witness, własnyklucz · Kanał na Telegramie · Plik ZIP z dowodami · verify.py · podpisany punkt kontrolny: · liczba zapisów + skrót · nagłówka · podpisany wpis za · pośrednictwem własnego bota · Eksport z aplikacji Telegram · Desktop lub strona t.me/s

**Schemat w formie tekstowej**

1. Collector → Witness (podpisany punkt kontrolny: liczba zapisów + skrót nagłówka)
2. Witness → Dziennik Witness, własny klucz
3. Witness → Kanał na Telegramie (podpisany wpis za pośrednictwem własnego bota)
4. Plik ZIP z dowodami → verify.py
5. Dziennik Witness, własny klucz → verify.py
6. Kanał na Telegramie → verify.py (Eksport z aplikacji Telegram Desktop lub strona t.me/s)

## Co oferuje TgWitness, a czego nie zapewnia

| Świadek posiada | Świadek nigdy nie ma |
| --- | --- |
| **Token świadka** z prawem tylko do odczytu dla jednego obszaru roboczego | Sesja Telegramu użytkownika korzystającego z narzędzia lub dane uwierzytelniające do interfejsu API |
| Własny klucz Ed25519 i dziennik | Skarbiec kolektora, klucz podpisujący lub token panelowy |
| Własny token bota w serwisie Telegram | Treść wiadomości: nagłówek zawiera liczbę zapisów oraz skrót |

Token jest generowany na stronie **„Witness”** w panelu, wyświetlany jednorazowo i przechowywany wyłącznie w postaci klucza SHA-256. Otwiera on dokładnie jeden punkt końcowy, `GET /api/witness/head`, który zwraca świeżo podpisany punkt kontrolny wraz z podpisanymi licznikami zbiorów bez treści oraz informacją o stanie operacyjnym. Nie może on otworzyć panelu, odczytać treści wiadomości ani zmienić ustawień, a token panelu nie jest tam akceptowany. Cofnięcie tokenu odbywa się na tej samej stronie. Kolektor rejestruje moment rozpoczęcia sprawdzania przez nowy klucz świadka (`witness.seen`) oraz pokazuje ostatnie sprawdzenie dla każdego tokenu; świadek, który nie przeprowadził sprawdzenia w ciągu 2,5 interwału, zostaje oznaczony jako przeterminowany.

Nowi świadkowie wysyłają losowe hasło weryfikacyjne przy każdej ankiecie; instrukcja przechwytywania powtarza je pod podpisem kolektora. Liczniki są powiązane z konkretnym punktem kontrolnym i są uwzględniane w podpisanych wpisach świadków. Starsze nagłówki są nadal akceptowane przez samodzielnego świadka. Sam wzrost objętości dziennika nigdy nie jest traktowany jako nowa wiadomość.

## Co narzędzie sprawdza i rejestruje

W każdym przedziale czasowym (domyślnie co 10 minut) narzędzie TgWitness:

1. samodzielnie pobiera nagłówek (moduł zbierający nie może go przesłać ani pominąć);
2. weryfikuje podpis kolektora, przypięty klucz kolektora (`--collector-fingerprint`, lub pierwszy widoczny klucz), niezmniejszającą się liczbę oraz niezmieniony nagłówek przy niezmienionej liczbie;
3. dodaje podpisany zapis do własnego dziennika: `witness.anchor` o statusie `ok`, `key_changed`, `rollback` (mniej zapisów niż poprzednio), `fork` (ta sama długość, inny nagłówek) lub `invalid` (odpowiedź nie przeszła weryfikacji), albo `witness.no_response`, gdy moduł zbierający nie udzielił odpowiedzi;
4. wynik jest publikowany na kanale wraz z podpisem, w tym komunikat „brak odpowiedzi”, o ile narzędzie TgWitness działa i ma dostęp do interfejsu API bota. Rejestrowany jest identyfikator publikacji (`witness.posted`), a także identyfikator nieudanej publikacji (`witness.post_failed`).

Wpis wygląda następująco; ostatnia linia zawiera podpisane oświadczenie:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Uruchom program Witness

Potrzebny jest Państwu bot w Telegramie (można go utworzyć za pomocą @BotFather), kanał, w którym bot ten pełni funkcję administratora, oraz adres kolektora dostępny dla świadka — za pośrednictwem protokołu HTTPS poza siecią prywatną (patrz profil HTTPS w [sekcji wdrożenia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/)).

Proszę otworzyć **menu „Dodatki” → „Bot w Państwa kanale” → „Skonfiguruj bota”** w panelu. Trzy kroki obejmują ustawienie dostępu tylko do odczytu, wybór kanału oraz określenie częstotliwości, a następnie uruchomienie bota. Polityka publikacji, opcjonalny serwer proxy HTTP/SOCKS5 oraz niestandardowy adres API bota znajdują się w **ustawieniach zaawansowanych** . Formularz pobiera plik `witness.json` z przypisanym kluczem kolektora dla tego obszaru roboczego. Proszę pobrać nowo utworzony token tylko do odczytu, **zapisując plik dostępu** jako `witness-token.txt` ; proszę umieścić go oraz plik `bot-token.txt` utworzony na hoście Witness obok tego pliku JSON. Kolektor nigdy nie otrzymuje tokenu bota. Pobieranie nie powoduje uruchomienia usługi ani opublikowania komunikatu. Żaden świadek projektu hostowanego nie jest domyślnie rejestrowany.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Pierwsze polecenie sprawdza pliki konfiguracyjne i pliki tajne bez wysyłania żądań sieciowych ani tworzenia kluczy. Ścieżki w formacie JSON są względne względem tego pliku; ścieżki CLI/środowiska są względne względem katalogu roboczego. Należy zachować odcisk palca świadka poza jego hostem. Wskaźnik ostatniego odczytu kolektora potwierdza jedynie żądanie; publikacja jest zgłaszana przez Proof lub sprawdzana w dzienniku świadka oraz na kanale.

Jeśli panel znajduje się za tunelem SSH, należy udostępnić wyłącznie wyznaczony punkt końcowy Witness na oddzielnej nazwie hosta HTTPS, korzystając z [poniższego przykładu wykorzystującego Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). Domyślny obszar roboczy korzysta wówczas z `https://witness.example.org`, pozostałe obszary robocze – z `https://witness.example.org/profiles/ID`. Tokeny są nadal wymagane; panel oraz jego inne trasy API nie są przekierowywane przez ten wirtualny host.

Proszę wybrać opcję `all`, aby uzyskać regularnie publikowane punkty kontrolne. Pięciominutowy interwał oznacza około 288 wpisów dziennie na każdy obszar roboczy. Opcje `changes` i `problems` celowo pomijają publikację niektórych punktów kontrolnych. MTProxy jest przeznaczony dla klienta Telegramu służącego do gromadzenia danych. Polling HTTP serwisu Witness oraz interfejs API botów Telegramu HTTPS korzystają z własnej trasy bezpośredniej/HTTP/SOCKS5 ([Bot API](https://core.telegram.org/bots/api)).

**Obok modułu zbierającego, z wykorzystaniem Docker** (ten sam host — niezależny proces i klucz, ale ten sam operator): należy wprowadzić wartości w polu „`.env`” i uruchomić profil.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

W przypadku publikacji obrazu prosimy o użycie kodu `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**Na serwerze innej osoby** (prawdziwy niezależny świadek): skopiuj tam repozytorium, ustaw `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` oraz trzy powyższe wartości w `.env`, a następnie

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

lub bez wykorzystania Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Opcje

| Opcja | Środowisko | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Czas między kolejnymi sprawdzeniami: 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | Czas oczekiwania na uruchomienie modułu zbierającego dane i interfejsu API bota: od 5 do 600 sekund |
| `--post` | `_POST` | `all` | `all`: wszystko w porządku; `changes`: nowa kwestia lub problem; `problems`: same problemy i brak odpowiedzi |
| `--title` | `_TITLE` | `TgWitness witness` | Pierwsze słowa każdego wpisu na kanale |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Należy zapisać klucz kolektora zamiast polegać na pierwszej odpowiedzi |
| `--proxy` | `_PROXY` | bezpośredni | `socks5://host:port` lub `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Adres interfejsu API bota, np. lokalny serwer interfejsu API bota |
| `--data-dir` | `_DATA` | `witness-data` | Klucz Witness i dziennik |
| `--config` | `_CONFIG` | – | Plik JSON zawierający dowolną z powyższych opcji |

Adres kolektora, tokeny oraz kanał pochodzą z `--collector`, `--token` lub `--token-file`, `--bot-token` lub `--bot-token-file` i `--channel`, albo `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` i `_CHANNEL`, co pozwala na utrzymanie poufności poza listą procesów.

Plik konfiguracyjny wykorzystuje nazwy opcji z podkreśleniami oraz symbol `texts`, który zastępuje słowa w postach kanału:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Klucze `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Wiersz pole wygrywa z środowiskiem, a środowisko z plikiem. Nieznane opcje lub klucze tekstowe powodują zatrzymanie działania narzędzia „witness” i wyświetlenie komunikatu zamiast ich ignorowania. Sformułowanie nigdy nie ma wpływu na weryfikację: skrypt verify.py sprawdza podpisany token na końcu każdego wpisu. W przypadku `--post changes` lub `problems` kontrole, które nie zostały opublikowane, nadal znajdują się w dzienniku świadków, a `verify.py` wymienia je jako nigdy nieopublikowane; rekord początkowy określa politykę. Każda kontrola nadal pojawia się w dzienniku, więc mniejsza liczba wpisów oznacza mniejszą liczbę niezależnych czasów w Telegramie, a nie mniejszą liczbę kontroli.

Nawet bez kanału aplikacja TgWitness nadal prowadzi swój dziennik. Proszę przechowywać odcisk klucza aplikacji TgWitness (`python -m tgwitness.witness fingerprint`) w innym miejscu.

## Zweryfikuj

Ze strony świadka należy wyeksportować ten dziennik:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Następnie, w dowolnym miejscu, korzystając z podpisanego pliku ZIP z narzędzia zbierającego oraz kanału wyeksportowanego z aplikacji Telegram Desktop (*opcja „Eksportuj historię czatu* ” → „JSON” generuje plik o nazwie „`result.json` ”) lub jego publicznej strony o nazwie „`https://t.me/s/…` ”:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` sprawdza dziennik świadka (łańcuch i podpisy), a następnie upewnia się, że **każdy nagłówek, który widział świadek, znajduje się w wyeksportowanym dzienniku**: zapis przy danym numerze musi posiadać dokładnie ten sam skrót. Nagłówek, który nie pasuje, nie przechodzi weryfikacji — dziennik został zmieniony po tym, jak widział go świadek. Zgłasza również nagłówki zaobserwowane po eksporcie, anomalie odnotowane przez świadka, odpowiedzi, które zakończyły się niepowodzeniem, okresy, dla których w niniejszym eksporcie występują pasujące punkty kontrolne („Poświadczone od X do Y”) oraz luki. Późniejsze punkty kontrolne nie przedłużają tych okresów. Wynik zawiera numer ostatniego dopasowanego zapisu oraz liczbę kolejnych zapisów bez pasującego punktu kontrolnego. Liczą się wyłącznie odpowiedzi podpisane kluczem należącym do danego eksportu: eksport podpisany kluczem, którego świadek nigdy nie widział, jest zgłaszany jako niepotwierdzony, a bez `--fingerprint` jego podpisujący pozostaje nieprzypisany. W przypadku `--channel` każdy podpisany wpis musi być zgodny z dziennikiem świadka wpis po wpisie: zmienione wpisy nie przechodzą weryfikacji, a brakujące wpisy są wymienione. Data w dostarczonym eksporcie JSON serwisu Telegram stanowi edytowalne metadane, pozostające poza zakresem podpisanego tokenu świadka. Zgodność tokenu nie potwierdza autentyczności daty publikacji; wynik wyraźnie informuje, że weryfikacja czasu publikacji nie została przeprowadzona.

### Wymagany jest eksport z potwierdzeniem

W przypadku przekazania, które musi obejmować poświadczony ostateczny zapis, proszę dodać `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Wymaga to niezależnie zachowanego odcisku palca świadka oraz pasującego punktu kontrolnego umieszczonego dokładnie na końcu tego eksportu. Punkt kontrolny obejmujący jedynie wcześniejszy prefiks jest niewystarczający. Należy wstrzymać gromadzenie danych, umożliwić świadkowi obserwację stanu końcowego, a następnie przeprowadzić eksport przed dalszym zapisywaniem w dzienniku; jeśli dziennik ulegnie zmianie, należy zachować kolejny punkt kontrolny i wyeksportować ten stan. Sam późniejszy punkt kontrolny nie pozwala zweryfikować końcowego skrótu krótszego eksportu. W przypadku podania również flagi „`--channel`” brakujące zgłoszone posty lub pusty zestaw dopasowań spowodują niepowodzenie tej rygorystycznej kontroli. Bez tej flagi zwykłe kontrole integralności nadal zgłaszają niepotwierdzone rekordy, nie odrzucając jednak archiwum, które poza tym jest nienaruszone.

Flaga ta zapewnia spójność z dostarczonymi, przypiętymi zapisami świadka. Operator musi jednak nadal potwierdzić niezależność świadka i przechowywać jego zapisy oddzielnie. Nie potwierdza ona prawdziwości wiadomości, kompletności zbioru ani niezależnie zmierzonego czasu działania.

Świadectwo pokazuje, co rejestrator zgłosił w danym momencie, oraz że późniejsze eksporty są z tym zgodne. Nie pokazuje ono, że rejestrator zarejestrował wszystko, co dostarczył Telegram, ani że treść wiadomości jest prawdziwa. Świadectwo wygenerowane przez tego samego operatora na tym samym urządzeniu ma mniejszą wagę niż świadectwo wygenerowane przez inną osobę.

Sam wzrost liczby wpisów nie wystarcza do ustalenia ciągłości danych w trybie „tylko dodawania” w sieci: porównanie w trybie offline musi polegać na zestawieniu każdego zachowanego skrótu prefiksu z pełnym eksportem z kolektora. Przerwy w działaniu serwisu Witness oraz nieudane publikacje powodują powstanie przedziałów czasowych bez zewnętrznych punktów odniesienia. Brakujące wpisy można zgłaszać na podstawie zachowanego dziennika Witness; ani kanał, ani serwer kontrolowany przez tego samego operatora nie stanowią niezmiennego archiwum strony trzeciej.
