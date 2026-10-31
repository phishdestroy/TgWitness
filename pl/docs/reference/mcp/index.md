# MCP tylko do odczytu

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/

Połącz klienta MCP z wybranymi obszarami roboczymi i czatami, korzystając z dostępu ograniczonego czasowo i podlegającego odwołaniu.

**Aktualna wersja główna:** należy skorzystać z kopii źródłowej; przenośna wersja zapoznawcza 0.7.0 nie zawiera jeszcze tej funkcji.

[Przewodnik po procesie pracy](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Zainstaluj opcjonalny serwer z katalogu projektu TgWitness:

```
python -m pip install '.[mcp]'
```

W panelu otwórz **opcję Integracje → MCP**. Nadaj nazwę połączeniu, wybierz jego obszary robocze i czaty oraz określ okres ważności. Skopiuj token archiwum tylko raz; nie będzie można go później odzyskać. Unieważnij utracone tokeny i wygeneruj nowe. Tokeny panelu oraz dane logowania do Telegrama nie są danymi logowania do MCP.

## Podłącz klienta

Panel generuje `.vscode/mcp.json` dla środowiska **VS Code Local,** korzystając z [udokumentowanej konfiguracji](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Zapisz pobrany plik w tej lokalizacji, uruchom **MCP: List Servers** i uruchom TgWitness. VS Code wyświetli monit o podanie tokenu poprzez pole wprowadzania hasła. Pobrany plik JSON zawiera odniesienie do monitu, a nie sam token. Użyj pliku wykonywalnego w języku Python z środowiska, w którym zainstalowano dodatek MCP.

W przypadku innych klientów stdio należy uruchomić:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Ustaw `TGWITNESS_ARCHIVE_TOKEN` w chronionym środowisku klienta. Nie umieszczaj go w argumentach poleceń ani adresach URL. Most odczytuje dane poprzez autoryzowane API archiwum panelu; nie ma bezpośredniego dostępu do bazy danych. Stdout przekazuje wyłącznie wiadomości MCP.

W przypadku klientów zdalnych należy uruchomić usługę obok panelu:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Przekieruj `/mcp` przez odwrotny serwer proxy HTTPS do `127.0.0.1:8766/mcp`, zachowując nagłówek `Authorization: Bearer …`. Wyłącz rejestrowanie nagłówków autoryzacyjnych oraz treści żądań i odpowiedzi. Powiązaj poza pętlą zwrotną tylko w razie potrzeby, używając `--host` i `--public-url`. Punkt końcowy korzysta z Streamable HTTP z oficjalnego zestawu [SDK MCP dla języka Python](https://github.com/modelcontextprotocol/python-sdk). Obsługuje jawnie skonfigurowane poświadczenia typu „bearer”, a nie wykrywanie OAuth; klienci wymagający wyłącznie OAuth nie są obsługiwani.

**Sprawdzenie protokołu i uzyskanie dostępu** powoduje uruchomienie prawdziwego klienta MCP oraz wyświetlenie listy narzędzi. Nie pobiera ono wiadomości. W przypadku zdalnej weryfikacji wybrany serwer MCP otrzymuje token archiwum. Należy konfigurować wyłącznie serwer, który sam obsługujesz lub któremu ufasz w tym zakresie.

## Zakres i wyniki

Dostępne narzędzia: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` oraz `get_capture_status`. Nie ma funkcji związanych z działaniami w Telegramie, zmianami konfiguracji ani narzędzi do eksportu zbiorczego. Każde odczytanie powoduje ponowne sprawdzenie dostępu do obszaru roboczego/czatu; wygasłe i cofnięte poświadczenia przestają działać. Limity wynoszą 60 żądań API na minutę na jedno poświadczenie, 50 rekordów na stronę, odpowiedź o wielkości 64 KiB oraz ośmiosekundowy limit czasu API.

Wyniki wyszukiwania wiadomości obejmują obszar roboczy, identyfikatory czatów/wiadomości, sekwencję zdarzeń, zapisany skrót oraz link do panelu. Użytkownik otwierający link musi posiadać własną, autoryzowaną sesję w panelu. Nie uwzględniono surowych obiektów Telegramu, skrótów dostępu, odwołań do plików, materiałów sesji ani kluczy. Wyszukiwanie dotyczy treści wiadomości, a nie surowych pól. Tekst jest ograniczony, a miejsca skrócenia są zaznaczone. Edycje, powiadomienia o usunięciu z Telegrama oraz `missing_on_recheck` pozostają odrębnymi obserwacjami. Dostęp w zakresie czatu nie pozwala na przeglądanie zdarzeń operacyjnych dotyczących całego obszaru roboczego; status przechwytywania wyraźnie zaznacza to ograniczenie.

Tekst archiwum stanowi dane wejściowe o niepotwierdzonej wiarygodności. Instrukcje zawarte w wiadomościach nie nadają żadnych dodatkowych uprawnień i nie mogą być traktowane jako instrukcje klienta. Zewnętrzny model AI może otrzymywać dowolną treść, o którą poprosi jego klient MCP. Dostęp tylko do odczytu uniemożliwia wprowadzanie zmian w archiwum; nie uniemożliwia jednak klientowi zachowania odczytanych danych.

Skróty identyfikują zapisane rekordy i umożliwiają sprawdzanie ich integralności. Nie stanowią one jednak samodzielnego dowodu autorstwa w serwisie Telegram ani nie potwierdzają, że każda wiadomość została zarejestrowana.
