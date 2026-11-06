# Wiersz poleceń

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/cli/

Wyszukiwanie, odczytywanie kontekstu, zliczanie aktywności oraz eksportowanie zapisanych wiadomości ze skryptów i agentów, z wyjściem w formacie --json, stabilnymi kodami zakończenia oraz tokenami o ograniczonym zakresie dostępu, przeznaczonymi wyłącznie do odczytu.

[MCP tylko do odczytu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/) · [Wyszukiwanie pełnotekstowe](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Podgląd.** `tgwitness search`, `context`, `messages`, `stats` oraz `export` odczytuj zapisane obserwacje dla skryptów i agentów AI. Nie mogą one wysyłać niczego do Telegramu, zmieniać ustawień ani modyfikować podpisanego dziennika.

Przy `--json`, stdout przekazuje dokładnie jeden dokument JSON (`export` zapisuje wiersze JSON). Postęp, podpowiedzi i błędy są kierowane do stderr. Kody wyjścia są stałe:

| Kod | Znaczenie |
| --- | --- |
| `0` | Pomyślny wynik, w tym wynik pusty |
| `1` | Błąd: niedostępny panel, nieczytelne dane, przerwany eksport |
| `2` | Błąd użytkowania lub nieprawidłowe żądanie: nieprawidłowa data, nieznana opcja, indeks wyszukiwania wyłączony |
| `3` | Obecnie niedostępne: obszar roboczy jest otwarty w uruchomionym panelu lub panel prosi o ponowną próbę później (limit częstotliwości, przekroczenie limitu czasu) |
| `4` | Odmowa dostępu: brakujący, wygasły lub unieważniony token, czat poza zakresem działania narzędzia, narzędzie, które tego nie zezwala |

## Dwa sposoby czytania

**Za pośrednictwem panelu (`--url`).** Polecenie wykorzystuje ten sam API archiwum o ograniczonym zakresie, co MCP. Utwórz połączenie w sekcji **Integracje → MCP**: wybierz obszary robocze i czaty, narzędzia oraz okres ważności, a następnie skopiuj token jednorazowo. Połączenie ma charakter wyłącznie do odczytu, jest ograniczone do wybranych czatów, ma limit 60 żądań na minutę i może zostać cofnięte lub odnowione w dowolnym momencie. Tokeny logowania do panelu oraz dane uwierzytelniające do Telegrama nie działają w tym przypadku.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Panel zdalny wymaga protokołu HTTPS; zwykły protokół HTTP jest akceptowany wyłącznie w przypadku `127.0.0.1`, `localhost` oraz `::1`. Zmienne środowiskowe proxy są ignorowane, a przekierowania są odrzucane, dzięki czemu token dociera wyłącznie pod podany przez Ciebie adres.

**Bezpośrednio z zatrzymanego obszaru roboczego (`--data-dir`).** Odczytuje katalog danych z pełnym dostępem lokalnym, bez tokenu. Należy używać tej opcji na kopii katalogu danych lub gdy gromadzenie danych jest zatrzymane. Podpisane rekordy nigdy nie są modyfikowane; podobnie jak w przypadku panelu, otwarcie obszaru roboczego może spowodować aktualizację indeksów pochodnych. Gdy panel ma otwarty obszar roboczy, polecenie kończy działanie z kodem `3`; należy zamiast tego odczytywać dane za pośrednictwem panelu. W przypadku braku `--data-dir`, `TGWITNESS_DATA`, `./data/live` lub wykorzystywany jest katalog danych instalacji, w której uruchomiono polecenie.

`--workspace ID` wybiera obszar roboczy (domyślnie `default`). `tgwitness messages
--workspaces` wyświetla listę tych, do których masz dostęp.

## Polecenia

| Polecenie | Wynik |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Najlepsze wyniki na początku, uwzględniając formy słów, dokładne frazy w cudzysłowie, domeny oraz `@username` ([składnia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Dokładny tekst, najnowsze wpisy na początku, bez indeksu |
| `tgwitness context CHAT_ID MESSAGE_ID` | Zapisane wiadomości w zakresie dziesięciu identyfikatorów wiadomości po obu stronach |
| `tgwitness messages` | Czat, który można przeczytać |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Zapisane wiadomości z czatu, najnowsze na początku |
| `tgwitness messages CHAT_ID --message ID` | Każda zapisana wersja i zapis usunięcia jednej wiadomości |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Statystyki aktywności poniżej |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Zapisane obserwacje w formacie JSON Lines w kolejności zgodnej z dziennikiem |

Daty podaje się jako `2026-10-01` (północ czasu UTC) lub w formacie ISO z podaniem strefy czasowej `2026-10-01T09:00+03:00`. W przypadku `search`, `messages` i `export` wybierają czas obserwacji. Strony mieszczą do 50 rekordów: postępuj zgodnie z `next_offset` (`--offset`) w celu wyszukiwania według rankingu oraz `next_before` (`--before`) w innych miejscach.

Ranked search stops at 1，000 results．The final page may be shorter than `--limit`；narrow the query，chat or period when more matching observations exist．

Każdy wynik wiadomości zawiera `untrusted_content: true`, identyfikatory obszaru roboczego, czatu i wiadomości, numer sekwencyjny w dzienniku, skrót zapisanego rekordu oraz link do panelu. Edycje, powiadomienia o usunięciu oraz `missing_on_recheck` stanowią oddzielne zapisy. Brak zapisu nie dowodzi, że zdarzenie nigdy nie miało miejsca.

### Statystyki aktywności

`stats` zlicza zapisane obserwacje dla jednej rozmowy, jednego nadawcy lub wszystkich rozmów objętych zakresem:

- wiadomości według godziny UTC i dnia tygodnia (z poniedziałkiem na początku), godziny i dni o największym natężeniu ruchu;
- edytowane, usunięte i `missing_on_recheck` udostępnienia;
- nadawców wraz z liczbą wiadomości oraz czasem wysłania pierwszej i ostatniej wiadomości;
- najczęściej występujące domeny oraz `@handles`, zliczane raz na wiadomość we wszystkich jej zapisanych wersjach;
- zakres: `coverage.gap` zapisy oraz, w celu uzyskania dostępu do całego obszaru roboczego, okresy bez sygnału kontrolnego z podłączonego kolektora (`collector_liveness`).

Okres określa **czas wiadomości zgłoszony przez Telegram**. Liczba godzin i dni tygodnia może pomóc w oszacowaniu strefy czasowej nadawcy; nie pozwala jednak jej jednoznacznie ustalić. Dane liczbowe są obliczane na żądanie na podstawie dziennika i nie są przechowywane. Każdy wynik wskazuje nagłówek dziennika, który obejmuje, gdy dostęp obejmuje cały obszar roboczy. Odczyt zatrzymuje się po upływie pięciu sekund od przejścia przez panel lub `--timeout` sekund lokalnie (domyślnie 30); wówczas `complete` ma wartość false, a `partial` wskazuje pierwszy rekord, który nie został odczytany. W takim przypadku liczone są tylko najnowsze rekordy.

### Eksportuj

`export` tworzy jeden obiekt JSON na każdą zapisaną obserwację (nowe wiadomości, zrzuty ekranu, edycje, odzyskane wiadomości, powiadomienia o usunięciu, `missing_on_recheck` oraz zapisanych plików multimedialnych ) w kolejności z dziennika. Każdy wiersz zawiera te same pola co pozostałe wyniki, wraz z pełnym tekstem. W przypadku `--output`, plik jest zapisywany pod `.partial` nazwą i jest przemianowywany dopiero po zapisaniu zakończenia działania panelu; przerwany eksport nie pozostawia żadnego pliku i kończy działanie z kodem `1`. `--output` nigdy nie nadpisuje istniejącego pliku. Przy użyciu opcji `--output` i `--json`, stdout zawiera podsumowanie: liczbę rekordów, ostatnią sekwencję dziennika oraz, w przypadku dostępu do całego obszaru roboczego, nagłówek dziennika.

Eksport za pośrednictwem panelu wymaga połączenia umożliwiającego **eksport wiadomości (tylko z wiersza poleceń)**; opcja ta nie jest domyślnie zaznaczona. Niniejszy plik stanowi kopię roboczą, a nie dowód: w celu weryfikowalnego przekazania danych należy skorzystać z podpisanego eksportu w **sekcji** **„Eksporty”**, który `python -m tgwitness.verify`sprawdza poprawność.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Umiejętności agenta

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) informuje agenta, jak korzystać z tych poleceń, jak cytować zapisy oraz jak postępować z przechwyconym tekstem. Agenci, którzy `.agents/skills` pobierają go z repozytorium po wygenerowaniu kopii roboczej. W przypadku Claude Code należy skopiować `tgwitness-cli` folder do `.claude/skills/` w swoim projekcie lub `~/.claude/skills/`.

## MCP i wiersz poleceń

Oba korzystają z tych samych połączeń, kontroli zakresu i ograniczeń. Wyniki MCP są ograniczone do jednej strony o rozmiarze 64 KiB, więc MCP nie oferuje eksportu zbiorczego; wiersz poleceń przesyła dane strumieniowo. `get_activity_stats` jest dostępna dla obu.
