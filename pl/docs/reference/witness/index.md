# Niezależny świadek

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/

Uruchom program Witness z własnym kluczem i botem, opublikuj podpisane punkty kontrolne na kanale i porównaj z nimi wyeksportowane dane.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[Eksportowanie i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/) · [Wysoki poziom bezpieczeństwa](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/) · [Przewodnik po panelach](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

Schemat blokowy · Collector → Witness (podpisany punkt kontrolny: liczba zapisów + skrót nagłówka); Witness → Dziennik Witness, własny klucz; Witness → Kanał na Telegramie (podpisany wpis za pośrednictwem własnego bota); Plik ZIP z dowodami → verify.py; Dziennik Witness, własny klucz → verify.py; Kanał na Telegramie → verify.py (Eksport z aplikacji Telegram Desktop lub strona t.me/s) · Collector · Witness · Dziennik Witness, własnyklucz · Kanał na Telegramie · Plik ZIP z dowodami · verify.py · podpisany punkt kontrolny: · liczba zapisów + skrót · nagłówka · podpisany wpis za · pośrednictwem własnego bota · Eksport z aplikacji Telegram · Desktop lub strona t.me/s

**Schemat w formie tekstowej**

1. Collector → Witness (podpisany punkt kontrolny: liczba zapisów + skrót nagłówka)
2. Witness → Dziennik Witness, własny klucz
3. Witness → Kanał na Telegramie (podpisany wpis za pośrednictwem własnego bota)
4. Plik ZIP z dowodami → verify.py
5. Dziennik Witness, własny klucz → verify.py
6. Kanał na Telegramie → verify.py (Eksport z aplikacji Telegram Desktop lub strona t.me/s)

**On this page**

- [What the witness gets, and what it does not](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [What it checks and records](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#what-it-checks-and-records)
- [Run a witness](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#run-a-witness)
- [Public proof page for several workspaces](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Verify](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#verify)

## Co oferuje TgWitness, a czego nie zapewnia

| Świadek posiada | Świadek nigdy nie ma |
| --- | --- |
| **Token świadka** z prawem tylko do odczytu dla jednego obszaru roboczego | Sesja Telegramu użytkownika korzystającego z narzędzia lub dane uwierzytelniające do interfejsu API |
| Własny klucz Ed25519 i dziennik | Skarbiec kolektora, klucz podpisujący lub token panelowy |
| Własny token bota w serwisie Telegram | Treść wiadomości: nagłówek zawiera liczbę zapisów oraz skrót |

Token jest tworzony w **sekcji „Extras” → „Independent witness”**, wyświetlany jednorazowo i przechowywany wyłącznie jako SHA-256. Otwiera dokładnie jeden punkt końcowy, `GET /api/witness/head`, który zwraca świeżo podpisany punkt kontrolny wraz z podpisanymi licznikami zbiorów bez treści oraz stanem operacyjnym. Nie może on otwierać panelu, odczytywać treści wiadomości ani zmieniać ustawień, a token panelu nie jest tam akceptowany. Token można unieważnić na tej samej stronie. Kolektor rejestruje moment, w którym nowy klucz świadka rozpoczyna sprawdzanie (`witness.seen`) oraz wyświetla ostatnią weryfikację dla każdego tokenu; świadek, który nie przeprowadził weryfikacji w ciągu 2,5 interwału, jest oznaczany jako zaległy.

Nowi świadkowie wysyłają losowe hasło weryfikacyjne przy każdej ankiecie; instrukcja przechwytywania powtarza je pod podpisem kolektora. Liczniki są powiązane z konkretnym punktem kontrolnym i są uwzględniane w podpisanych wpisach świadków. Starsze nagłówki są nadal akceptowane przez samodzielnego świadka. Sam wzrost objętości dziennika nigdy nie jest traktowany jako nowa wiadomość.

## Co narzędzie sprawdza i rejestruje

W każdym przedziale czasowym (domyślnie co 10 minut) narzędzie TgWitness:

1. samodzielnie pobiera nagłówek (moduł zbierający nie może go przesłać ani pominąć);
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
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

W panelu otwórz **opcję Dodatki → Niezależny świadek → Konfiguruj**. Trzy kroki obejmują dostęp tylko do odczytu, Twój kanał i interwał, a następnie uruchomienie świadka. Polityka publikacji, opcjonalny serwer proxy HTTP/SOCKS5 oraz niestandardowy adres API bota znajdują się w **ustawieniach zaawansowanych**. Formularz pobiera `witness.json` z przypiętym kluczem kolektora tego obszaru roboczego. Pobierz nowo utworzony token tylko do odczytu, wybierając opcję **„Zapisz plik dostępu** jako” `witness-token.txt`; umieść go wraz z `bot-token.txt`utworzony na hoście świadka obok tego pliku JSON. Kolektor nigdy nie otrzymuje tokenu bota. Pobieranie nie uruchamia usługi ani nie publikuje wiadomości. Żaden świadek projektu hostowanego nie jest domyślnie rejestrowany.

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

### Opublikuj na Discordzie

Świadek może publikować posty na kanale Discord zamiast w Telegramie. W Discordzie otwórz **Edytuj kanał → Integracje → Webhooki**, utwórz webhook i skopiuj jego adres URL. W panelu wybierz **Webhook Discorda · twój kanał** w kroku 2. Na serwerze świadka zapisz adres URL jako `discord-webhook.txt` obok `witness.json`; nigdy nie trafia do kolektora.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Każdy wpis ma jednego nadawcę: kanał w Telegramie lub webhook Discorda, ale nie oba jednocześnie. Wpisy zawierają tę samą podpisaną deklarację i nie mogą powiadamiać nikogo. Wpis dłuższy niż limit Discorda wynoszący 2 000 znaków jest zastępowany krótką linią z pełnym plikiem kontrolnym dołączonym jako `witness-check.txt`. Każdy identyfikator postu jest rejestrowany jako `witness.posted`. `verify.py --channel`odczytuje wyłącznie eksporty z kanałów Telegramu, więc w przypadku Discorda należy prowadzić dziennik świadka: zawiera on każdy check.

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

Adres kolektora, tokeny i kanał pochodzą z `--collector`, `--token` lub `--token-file`, `--bot-token` lub `--bot-token-file`, `--discord-webhook-file` oraz `--channel`, lub `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` oraz `_CHANNEL`, co sprawia, że sekrety nie pojawiają się na liście procesów.

Plik konfiguracyjny wykorzystuje nazwy opcji z podkreśleniami oraz symbol `texts`, który zastępuje słowa w postach kanału:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Klucze `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Wiersz pole wygrywa z środowiskiem, a środowisko z plikiem. Nieznane opcje lub klucze tekstowe powodują zatrzymanie działania narzędzia „witness” i wyświetlenie komunikatu zamiast ich ignorowania. Sformułowanie nigdy nie ma wpływu na weryfikację: skrypt verify.py sprawdza podpisany token na końcu każdego wpisu. W przypadku `--post changes` lub `problems` kontrole, które nie zostały opublikowane, nadal znajdują się w dzienniku świadków, a `verify.py` wymienia je jako nigdy nieopublikowane; rekord początkowy określa politykę. Każda kontrola nadal pojawia się w dzienniku, więc mniejsza liczba wpisów oznacza mniejszą liczbę niezależnych czasów w Telegramie, a nie mniejszą liczbę kontroli.

Nawet bez kanału aplikacja TgWitness nadal prowadzi swój dziennik. Proszę przechowywać odcisk klucza aplikacji TgWitness (`python -m tgwitness.witness fingerprint`) w innym miejscu.

## Publiczna strona z dowodami dla kilku obszarów roboczych

`python -m tgwitness.proof` Obsługuje do 32 obszarów roboczych jednocześnie i udostępnia stronę tylko do odczytu z najnowszym podpisanym raportem dla każdego z nich. Każdy obszar roboczy otrzymuje własny klucz świadka oraz dziennik w folderze danych, a także przypięty klucz kolektora; publikowanie na kanale Telegramu jest opcjonalne dla każdego obszaru roboczego. Zacznij od pliku [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Dziedzina | Znaczenie |
| --- | --- |
| `title` | Tytuł strony, 1–100 znaków |
| `data_dir` | Klucze i dzienniki Witness, powiązane z plikiem; domyślnie `proof-data` |
| `interval`, `timeout` | Czas w minutach między sprawdzaniami (1–1440, domyślnie 5); czas oczekiwania w sekundach (5–600, domyślnie 20) |
| `workspaces[].id`, `label` | Krótki alias pisany małymi literami oraz nazwa wyświetlana |
| `workspaces[].collector` | Adres kolektora; nazwy pozostałych obszarów roboczych kończą się na `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Wymagane, różne dla każdego obszaru roboczego |
| `workspaces[].token_file` | Plik zawierający token świadka tego obszaru roboczego z prawem tylko do odczytu |
| `workspaces[].channel`, `bot_token_file` | Opcjonalnie, łącznie: publikuj każdy wpis na kanale |
| `workspaces[].proxy`, `bot_api` | Opcjonalna trasa i adres API bota |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

Pierwsze polecenie weryfikuje plik oraz pliki tokenów bez nawiązywania połączenia. Strona obsługuje wyłącznie żądania GET i HEAD:

- `/` wyświetla wszystkie obszary robocze; obszar roboczy, który nie został zaznaczony przez 2,5 interwału, jest oznaczany jako nieaktualny.
- `/api/proof` zwraca to samo co JSON.
- `/api/proof/<id>` pobiera najnowsze podpisane oświadczenie (`tgwitness-public-proof-v1`): numer i skrót zapisu świadka, status, przypięty klucz zbierającego, punkt kontrolny, liczniki zbiorów oraz informacja, czy publikacja na kanale zakończyła się powodzeniem, podpisane kluczem świadka danego obszaru roboczego.
- `/healthz` zwraca kod 503, gdy monitor obszaru roboczego przestał działać.

Nadaj stronie własną nazwę hosta, np. [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). W celu weryfikacji wyeksportuj dziennik świadectw obszaru roboczego, `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` i wykorzystaj go zgodnie z poniższym opisem.

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

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
