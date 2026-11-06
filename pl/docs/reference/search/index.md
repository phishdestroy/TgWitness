# Wyszukiwanie pełnotekstowe

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/

Wyszukuj zapisane wiadomości według form słów, dokładnych fraz, domen i nazw użytkowników z symbolem @, z najlepszymi wynikami na początku, przy czym indeks jest powiązany z podpisanym dziennikiem.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dochodzenie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/)

![Dochodzenie](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Analiza archiwum](https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/) · [Lokalne rozpoznawanie tekstu (OCR) i transkrypcja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Podgląd.** W sekcji **„Dziennik**” wybierz opcję **„Najlepsze dopasowanie · formy wyrazów”** obok pola wyszukiwania. Wyniki są sortowane według algorytmu BM25 i obejmują inne formy tego samego słowa: *wyszukiwanie „перевод”* znajdzie *„переводом”* i *„переводы”*, a *„transfer”* znajdzie *„transfers”*; chińskie frazy są wyszukiwane bez spacji. **Opcja „Najnowsze najpierw · dokładny tekst”** zachowuje poprzednie wyszukiwanie podciągu w całym zapisie.

Indeks jest danymi pochodnymi. Jest on odtwarzany na podstawie podpisanego dziennika, sam nigdy nie jest podpisywany i nigdy nie jest eksportowany. Oryginalne zapisy pozostają niezmienione.

**Na tej stronie**

- [Składnia wyszukiwania](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#search-syntax)
- [Języki](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#languages)
- [Gdzie znajduje się indeks](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#where-the-index-lives)
- [Wyniki i podpisany dziennik](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#results-and-the-signed-journal)
- [Rozpoznany tekst](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#recognized-text)
- [Dostęp](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#access)
- [Zapytaj archiwum i MCP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#ask-the-archive-and-mcp)
- [Zależności](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#dependencies)
- [Test porównawczy](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#benchmark)

## Składnia wyszukiwania

| Napisz | Wyniki wyszukiwania |
| --- | --- |
| `перевод карта` | Zapisy zawierające oba słowa, w dowolnej formie |
| `"переводом на карту"` | Dokładna fraza, w tej kolejności |
| `бонус OR подарок` | Którekolwiek z tych słów |
| `перевод -казино` | Zapisy bez wykluczonego słowa |
| `example.com` | Domena i jej subdomeny, również w ukrytych linkach i adresach URL przycisków |
| `@username`, `t.me/username` | Wzmianki i linki dotyczące konta oraz wysłane przez nie wiadomości |
| `#tag` | Hashtag |
| `+79991234567`, adres portfela, adres e-mail | Ta sama wartość w postaci tekstu lub linków |
| `from:@username`, `from:123456` | Wiadomości od tego nadawcy |
| `chat:-1001234567890` | Jedna rozmowa; może ona ograniczyć wyłącznie Twój własny dostęp |
| `id:42` | Zapisane wersje wiadomości nr 42 |
| `since:2026-01-01 until:2026-01-31` | Okres obserwacji; data bez godziny obejmuje cały dzień |
| `kind:edited` | Tylko zmiany (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Rozpoznany tekst zamiast wiadomości lub wraz z nimi |

Przyimki i inne słowa funkcyjne są ignorowane, gdy występują inne słowa. Litery podobne występujące w słowie (np. łacińskie *„a”* w słowie cyrylickim), znaki o pełnej szerokości oraz ozdobne znaki Unicode i znaki niewidoczne są normalizowane.

## Języki

Język jest wykrywany dla każdego wpisu na podstawie skryptu i liter:

| Skrypt | Dopasowanie |
| --- | --- |
| cyrylica | Lematy rosyjskie i ukraińskie z wykorzystaniem [biblioteki](https://github.com/no-plagiarism/pymorphy3) [pymorphy3](https://github.com/no-plagiarism/pymorphy3). W przypadku braku opcjonalnego słownika ukraińskiego stosowany jest uproszczony moduł rozdzielania wyrazów dla języka ukraińskiego. |
| Łacina | Angielski stemmer typu „Snowball”; znaki diakrytyczne są ignorowane |
| chiński, japoński, koreański, tajski, laotański, khmerski, birmański | Nakładające się pary znaków: wyszukiwane są dowolne frazy bez spacji. Chińskie zapytania są dzielone na słowa za pomocą ieba |
| Inne skrypty | Dokładne sformułowania |

Słownik ukraiński (`pymorphy3-dicts-uk`) jest rozpowszechniany na licencji GPL-3.0, więc nie jest instalowany domyślnie. Zainstaluj go za pomocą `pip install "tgwitness[uk-dictionary]"`; indeks wykrywa nowy moduł analizujący i sam się odbudowuje.

## Gdzie znajduje się indeks

| Tryb | Przechowywanie danych | Zastosowanie |
| --- | --- | --- |
| Na dysku (domyślnie) | `search/fulltext.sqlite3` w katalogu obszaru roboczego | Duże archiwa; zachowuje dane po ponownym uruchomieniu |
| Tylko w pamięci | Brak danych na dysku; odbudowywane przy każdym uruchomieniu | Na dysku nie ma żadnych kopii treści wiadomości |
| Wyłącz | Brak indeksu; **najnowsze na początku ·** zachowano **dokładny tekst** | Minimalne wymagania instalacyjne |

Główny administrator wybiera tryb w **sekcji** **Dziennik → Filtry → Indeks wyszukiwania** dla każdego obszaru roboczego. `TGWITNESS_FULLTEXT=disk|memory|off` Ustawia domyślną wartość dla obszarów roboczych, które nie mają własnego wyboru. Przełączenie na tryb pamięci lub wyłączenie powoduje usunięcie pliku. Plik indeksu ma takie samo zabezpieczenie jak dziennik: znajduje się w katalogu danych prywatnych . Nie jest szyfrowany i nie wchodzi w skład kopii zapasowych ani kopii poza siedzibą.

Nowe zapisy są indeksowane w tle w ciągu kilku sekund; wyszukiwanie indeksuje również najpierw krótki zaległy zestaw, dzięki czemu można znaleźć zapis zapisany przed chwilą. Istniejący dziennik jest indeksowany po aktualizacji bez blokowania panelu; do tego momentu wyniki obejmują zindeksowane zapisy, a dziennik pokazuje postęp. **Odbudowa indeksu** rozpoczyna się ponownie od pierwszego zapisu.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` wymaga zatrzymania panelu (w przeciwnym razie kod wyjścia wynosi 3). W przypadku `--json`, wyjście standardowe zawiera tylko wynik; informacje o postępie są kierowane do standardowego błędu.

## Wyniki i podpisany dziennik

Indeks przechowuje numer sekwencyjny i skrót ostatniego wpisu dziennika, który obejmuje, i porównuje je z dziennikiem podczas jego otwierania. Wymieniony, przywrócony lub edytowany dziennik powoduje przebudowę indeksu. Każda odpowiedź zgłasza tę pozycję, a każde trafienie jest odczytywane z podpisanego dziennika na podstawie jego numeru sekwencyjnego: indeks decyduje, które wpisy wyświetlić i w jakiej kolejności, ale nigdy nie decyduje o ich treści. Dostęp do czatu dotyczy własnego pola czatu dziennika, a nie treści indeksu.

## Rozpoznany tekst

Wyniki OCR i transkrypcje pozostają w swoich zaszyfrowanych plikach. Ich indeks istnieje wyłącznie w pamięci i jest odtwarzany po zakończeniu zadania rozpoznawania. Trafienie pojawia się w `media.saved` rekordzie, oznaczony jako rozpoznanie maszynowe wraz z silnikiem, modelem i fragmentem; nigdy nie jest prezentowany jako tekst wysłany w Telegramie. Ten sam indeks służy funkcji **„Wyszukaj rozpoznany tekst”**, która nadal dopasowuje również zwykłe podciągi.

## Dostęp

Dostęp ograniczony do czatu wyszukuje wyłącznie zapisy z tych czatów, w tym rozpoznany tekst załączników. `chat:` oraz inne filtry mogą jedynie zawęzić ten zbiór. Status indeksu wyświetlany w trybie dostępu ograniczonego do czatu pomija sumy dziennika. Tylko główny administrator może zmienić tryb lub odbudować indeks.

## Zapytaj archiwum i MCP

Po zakończeniu tworzenia indeksu**archiwum** pobiera z niego źródła: najlepsze dopasowania spośród wybranych czatów, przy czym zapisany tekst jest liczony tylko raz. Wysyłanych jest maksymalnie 24 źródeł; długie teksty są przycinane wokół dopasowania i oznaczane jako skrócone. Zapytania dotyczące ostatnich zmian, zapisanych wersji jednej wiadomości oraz wyszukiwania w czasie, gdy indeks jest nadal tworzony, wykorzystują poprzedni sposób pobierania danych w porządku chronologicznym. Podgląd pokazuje, która metoda została użyta.

Klienci MCP mogą wywołać `search_messages` z `ranked=true` oraz wyświetlać strony za pomocą `next_offset`. Połączenia z ograniczeniem zakresu odbierają wyłącznie swoje czaty.

Paginacja według rankingu obejmuje co najwyżej pierwsze wyniki 1,000, niezależnie od rozmiaru strony. Aby sprawdzić kolejne dopasowania, należy zawęzić zapytanie, czat lub okres. Wyszukiwanie według najnowszych wyników sortuje wiadomości, wyniki OCR i transkrypcji przed wybraniem każdej strony.

## Zależności

| Pakiet | Licencja | Dlaczego |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Lematy rosyjskie i ukraińskie; słowniki są ładowane lokalnie |
| snowballstemmer | Klauzula BSD-3 | Rdzenie angielskie, czysty Python |
| jieba | MIT | Segmentacja zapytań w języku chińskim, napisane wyłącznie w języku Python (tylko dystrybucja kodu źródłowego) |
| pymorphy3-dicts-uk (opcjonalnie) | GPL-3.0 | Pełny słownik języka ukraińskiego |

Wymagany jest moduł SQLite FTS5 z `unicode61` tokenizerem; jest on częścią biblioteki SQLite w aktualnych kompilacjach Pythona. Bez niego wyszukiwanie najlepszego dopasowania zgłasza, że funkcja jest niedostępna.

## Test porównawczy

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`tworzy deterministyczny, podpisany dziennik zawierający mieszankę wiadomości w językach rosyjskim, ukraińskim, angielskim, chińskim i japońskim wraz z linkami i identyfikatorami w 200 czatach, buduje indeks oraz mierzy czas typowych wyszukiwań (50 wyników, mediana z 7 przebiegów).

Testowano na systemie Windows 11, procesorze Intel Core i9-13900K, 128 GB pamięci RAM, w środowisku Python 3.12.10, SQLite 3.49.1, z danymi na dysku exFAT, analizator `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Miara | Wynik |
| --- | --- |
| Podpisany dziennik | 1 000 000 wiadomości, 1,50 GiB, zapisanych w ciągu 19 minut |
| Tworzenie indeksu na podstawie dziennika | 71 s, około 14 141 wiadomości na sekundę |
| Plik indeksowy | 58 MiB, 3,8% dziennika |
| Wyszukiwanie bezpośrednio po utworzeniu nowego wpisu | Mediana 8 ms, p95 9 ms |
| Poprzednie wyszukiwanie podciągu, ten sam dziennik | `перевод` 3,2 s, `银行转账` 2,6 s, `verify-account.example` 2,6 s |

| Wyszukiwanie | Dopasowywanie rekordów | Najlepsze dopasowanie, mediana | str. 95 | Najnowsze najpierw, mediana |
| --- | --- | --- | --- | --- |
| Powszechnie używane słowa i ich formy: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Dwa słowa: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Rzadko spotykane słowo: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Dokładne sformułowanie: `"переказ коштів на картку"` | nie wliczono | 35 ms | 36 ms | 6 ms |
| Domena wraz z subdomenami: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @nazwa_użytkownika: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Chiński bez spacji: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Japoński: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Rdzeń angielski: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| LUB i wykluczenia: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Filtr czatu: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Filtr czasowy: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Dokładna fraza jest sprawdzana dosłownie w wynikach w kolejności według rankingu, aż strona zostanie wypełniona, więc jej suma nie jest wliczana. Czas wyszukiwania rośnie wraz z liczbą pasujących rekordów; zawężenie czatu lub okresu przyspiesza szerokie wyszukiwania. Syntetyczny korpus powtarza niewielkie słownictwo, więc popularne słowa pasują do znacznie większej liczby rekordów niż w prawdziwych czatach.
