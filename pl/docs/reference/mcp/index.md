# MCP tylko do odczytu

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/

Połącz klienta MCP z wybranymi obszarami roboczymi i czatami, korzystając z dostępu ograniczonego czasowo i podlegającego odwołaniu.

Podłącz klienta analitycznego do wybranych obszarów roboczych i czatów. TgWitness obsługuje **Streamable HTTP pod ścieżką `/mcp` w procesie panelu**. Każde połączenie ma własny token, termin ważności oraz dozwolone narzędzia. MCP nie może wysyłać wiadomości na Telegramie, zmieniać ustawień ani modyfikować podpisanego dziennika.

[Przewodnik po procesie pracy](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Instalacja i weryfikacja

Użyj środowiska Python, w którym działa panel. Z pobranego kodu źródłowego wykonaj:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Po instalacji uruchom ponownie panel ze standardowym katalogiem danych i argumentami startowymi. Sprawdzenie gotowości powinno zawierać `[PASS] mcp: streamable-http available`. Sekcja **Integrations → MCP** pokazuje status środowiska uruchomieniowego oraz polecenie instalacyjne używające rzeczywistego pliku wykonywalnego Pythona na tym serwerze. Przycisk **Re-check** odświeża ten status bez przeładowywania strony; nie instaluje pakietów ani nie restartuje serwera.

Dodatek MCP wykorzystuje oficjalny pakiet [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk). Plik `deploy/constraints-mcp.txt` przypina przetestowane wersje SDK i zależności. Funkcje te wymagają aktualnego kodu źródłowego; przenośna wersja poglądowa 0.7.0 powstała przed ich wprowadzeniem.

## Utworzenie połączenia

1. Wprowadź etykietę oraz wybierz obszary robocze i czaty, które klient może odczytywać.
2. Wybierz narzędzia pojedynczo lub użyj presetu. Dostępne są tylko zaimplementowane narzędzia.
3. Wybierz 1, 7, 30 lub 90 dni albo własny czas wygaśnięcia z przedziału od jednej minuty do 90 dni.
4. Naciśnij **Create connection**. Token wyświetli się jednorazowo obok konfiguracji klienta.
5. Skopiuj token i konfigurację, a następnie uruchom **Check connection**. Inicjalizuje to MCP i wyświetla listę dozwolonych narzędzi; **żadne wiadomości nie są odczytywane**. Wynik pokazuje wersję protokołu, nazwy narzędzi, ich liczbę oraz czas wykonania.
6. Naciśnij **Done** po zapisaniu poświadczeń. Odpytywanie w tle zachowuje formularz oraz kartę wyświetlaną jednorazowo. Zablokowanie panelu czyści wyświetlone sekrety.

Lista pokazuje ostatnie użycie, ostatnie narzędzie, adres oraz liczbę żądań w ciągu ostatniej minuty. **Revoke** kończy dostęp. **Rotate token** unieważnia stare poświadczenie i wydaje nowe z tym samym zakresem, zestawem narzędzi i czasem wygaśnięcia; skopiuj nowy token (wyświetlany jednorazowo). Tokeny logowania do panelu oraz poświadczenia Telegrama nie działają jako tokeny MCP.

## Podłączanie klienta

Wybierz klienta w panelu i skopiuj wygenerowaną dla niego konfigurację. Konfiguracje używają odwołań do sekretów lub jawnych symboli zastępczych (placeholderów); token jest kopiowany osobno.

| Klient | Konfiguracja | Połączenie |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, nagłówek bearer |
| Claude Desktop | `claude_desktop_config.json` | Lokalny mostek stdio |
| Cursor | `.cursor/mcp.json` | HTTP z nagłówkiem opartym na zmiennej środowiskowej |
| VS Code Local | `.vscode/mcp.json` | HTTP z wprowadzaniem hasła typu `promptString` |
| Windsurf | `mcp_config.json` | HTTP z symbolem zastępczym nagłówka bearer |
| Inni klienci | Adres URL i nagłówek Authorization | Streamable HTTP |

TgWitness używa tokenów bearer bez wykrywania OAuth. Użyj lokalnego mostka stdio dla klientów, których zdalny konektor wymaga OAuth. W przypadku VS Code zmienne wejściowe mają zastosowanie do środowiska **Local** i nie są przekazywane do sesji Copilot. Dokumentacja konfiguracji: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Kanoniczny punkt wejścia dla lokalnego mostka to:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Użyj lokalnego środowiska Python klienta z zainstalowanym dodatkiem MCP. Ustaw zmienną `TGWITNESS_MCP_TOKEN` w jego chronionym środowisku. Nie umieszczaj poświadczeń w argumentach poleceń ani w adresach URL. `tgwitness-mcp` to ten sam punkt wejścia. Stary moduł `tgwitness.mcp_bridge` oraz nazwa `TGWITNESS_ARCHIVE_TOKEN` pozostają ścieżkami zgodności z ostrzeżeniem; nowe konfiguracje używają `mcp_server` oraz `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Przekieruj ścieżkę `/mcp` panelu i zachowaj nagłówek bearer. Otwarcie ustawień MCP jako administrator rejestruje bieżący origin panelu dla danego uruchomienia. Aby uzyskać stabilny adres dostępny natychmiast po restarcie, skonfiguruj zmienną `TGWITNESS_PUBLIC_URL` z adresem origin HTTPS panelu przed jego uruchomieniem. Dowolne nagłówki Host i nagłówki przekazywane (forwarded) nie rejestrują zaufanego adresu. Weryfikacja nagłówków Host i Origin odrzuca niepowiązane adresy pochodzenia przeglądarki. Odpowiedzi używają `Cache-Control: no-store`; wartości autoryzacyjne nigdy nie są logowane.

Adres `*.trycloudflare.com` jest tymczasowy. Gdy restart tunelu zmieni nazwę hosta, zaktualizuj skonfigurowany publiczny adres URL oraz adres URL MCP u każdego klienta. Używaj stabilnej nazwy hosta dla zapisanych konfiguracji klientów.

## Narzędzia i ograniczenia

| Narzędzie | Odczytuje |
| --- | --- |
| `list_workspaces` | Przyznane obszary robocze |
| `list_chats` | Przyznane czaty |
| `search_messages` | Zapisany tekst wiadomości w wybranym okresie |
| `get_message_versions` | Przechwycone wersje i obserwacje usunięć |
| `get_message_context` | Identyfikatory pobliskich przechwyconych wiadomości |
| `get_journal_event` | Jeden oczyszczony rekord wraz z odwołaniem do źródła |
| `get_capture_status` | Stan gromadzenia danych i dozwolone rekordy pokrycia |

Wywołanie `tools/list` zwraca wyłącznie narzędzia przyznane dla danego połączenia. Wywołania innych narzędzi są odrzucane. Narzędzia dotyczące kontekstu grupowego, epizodów, terminologii oraz łańcuchów odpowiedzi nie są dostępne w tej kompilacji; ich oddzielny backend pakietów kontekstowych nie jest dołączony.

Każdy odczyt weryfikuje token, narzędzie oraz zakres obszaru roboczego/czatu, w tym również po zakończeniu pracy bazy danych. Limity wynoszą 60 żądań na minutę, 50 rekordów na stronę, 64 KiB na wynik oraz osiem sekund limitu czasu operacji w archiwum. Przekroczenie czasu wywołania MCP zwraca błąd narzędzia z prośbą o zawężenie okresu lub zmniejszenie limitu.

Wyniki wiadomości zawierają `untrusted_content: true`, identyfikatory obszaru roboczego/czatu/wiadomości, numer sekwencyjny zdarzenia, zapisany skrót (hash) oraz link do panelu. Surowe obiekty Telegrama, skróty dostępu (access hashes), sesje i klucze są pomijane. Obcięcie tekstu jest oznaczane. Edycje, powiadomienia o usunięciu oraz `missing_on_recheck` to odrębne obserwacje. Brakujące rekordy nie dowodzą, że zdarzenie nigdy nie miało miejsca.

Traktuj instrukcje zawarte w przechwyconych wiadomościach jako materiał dowodowy, a nigdy jako polecenia dla klienta. Dostęp tylko do odczytu uniemożliwia wprowadzanie zmian w archiwum; klient nadal może jednak zachować treści, do których odczytu ma uprawnienia. Skróty identyfikują zapisane rekordy i wspierają weryfikację integralności; nie dowodzą one autorstwa na Telegramie ani kompletności przechwycenia.
