# Volltextsuche

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/search/

Suche nach gespeicherten Nachrichten anhand von Wortformen, genauen Phrasen, Domains und @Benutzernamen, wobei die besten Treffer zuerst angezeigt werden und der Index mit dem signierten Protokoll verknüpft ist.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Untersuchung](https://phishdestroy.github.io/TgWitness/de/docs/reference/investigation/)

![Untersuchung](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Analyse des Archivs](https://phishdestroy.github.io/TgWitness/de/docs/reference/analysis/) · [Lokale OCR und Transkription](https://phishdestroy.github.io/TgWitness/de/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Vorschau.** Wählen Sie im **Protokoll** neben dem Suchfeld **„Beste Übereinstimmung · Wortformen“** aus. Die Ergebnisse werden nach BM25 sortiert und umfassen auch andere Formen desselben Wortes: *„перевод“* findet *„переводом“* und *„переводы“*, *„transfer“* findet *„transfers“*, eine chinesische Phrase wird ohne Leerzeichen gefunden. **„Neueste zuerst · exakter Text“** behält die vorherige Teilstring-Suche über den gesamten Datensatz bei.

Der Index besteht aus abgeleiteten Daten. Er wird aus dem signierten Protokoll neu erstellt, ist selbst niemals signiert und wird niemals exportiert. Die ursprünglichen Datensätze bleiben unverändert.

**Auf dieser Seite**

- [Suchsyntax](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#search-syntax)
- [Sprachen](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#languages)
- [Speicherort des Index](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#where-the-index-lives)
- [Ergebnisse und das signierte Journal](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#results-and-the-signed-journal)
- [Erkannter Text](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#recognized-text)
- [Zugriff](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#access)
- [Das Archiv und MCP befragen](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#ask-the-archive-and-mcp)
- [Abhängigkeiten](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#dependencies)
- [Benchmark](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#benchmark)

## Suchsyntax

| Schreiben | Ergebnisse |
| --- | --- |
| `перевод карта` | Einträge, die beide Wörter in beliebiger Form enthalten |
| `"переводом на карту"` | Der genaue Wortlaut in dieser Reihenfolge |
| `бонус OR подарок` | Beliebiges Wort |
| `перевод -казино` | Einträge ohne das ausgeschlossene Wort |
| `example.com` | Die Domain und ihre Subdomains, auch in versteckten Links und Button-URLs |
| `@username`, `t.me/username` | Erwähnungen und Links des Kontos sowie die von ihm gesendeten Nachrichten |
| `#tag` | Der Hashtag |
| `+79991234567`, eine Wallet-Adresse, eine E-Mail-Adresse | Der gleiche Wert in Text oder Links |
| `from:@username`, `from:123456` | Nachrichten von diesem Absender |
| `chat:-1001234567890` | Ein Chat; er kann nur Ihren eigenen Zugriff einschränken |
| `id:42` | Gespeicherte Versionen von Nachricht 42 |
| `since:2026-01-01 until:2026-01-31` | Beobachtungszeitraum; ein Datum ohne Uhrzeit umfasst den gesamten Tag |
| `kind:edited` | Nur Bearbeitungen (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Erkannter Text anstelle von oder zusammen mit Nachrichten |

Präpositionen und andere Funktionswörter werden ignoriert, wenn andere Wörter vorhanden sind. Ähnlich aussehende Buchstaben, die in einem Wort gemischt vorkommen (z. B. ein lateinisches *„a“* in einem kyrillischen Wort), Unicode-Buchstaben in voller Breite sowie dekorative Unicode-Buchstaben und unsichtbare Zeichen werden normalisiert.

## Sprachen

Die Sprache wird für jeden Datensatz anhand des Skripts und der Buchstaben ermittelt:

| Skript | Übereinstimmung |
| --- | --- |
| Kyrillisch | Russische und ukrainische Lemmata mit [pymorphy3](https://github.com/no-plagiarism/pymorphy3). Ohne das optionale ukrainische Wörterbuch wird ein einfacher ukrainischer Stemmer verwendet. |
| Latein | Englischer Snowball-Stemmer; diakritische Zeichen werden ignoriert |
| Chinesisch, Japanisch, Koreanisch, Thailändisch, Laotisch, Khmer, Myanmarisch | Überlappende Zeichenpaare: Jede Phrase wird ohne Leerzeichen gefunden. Chinesische Suchanfragen werden mit Jieba in Wörter aufgeteilt. |
| Weitere Skripte | Wörtliche Übersetzung |

Das ukrainische Wörterbuch (`pymorphy3-dicts-uk`) wird unter der GPL-3.0 vertrieben und ist daher standardmäßig nicht installiert. Installieren Sie es mit `pip install "tgwitness[uk-dictionary]"`; der Index erkennt den neuen Analysator und erstellt sich neu.

## Wo sich der Index befindet

| Modus | Speicherung | Verwendung |
| --- | --- | --- |
| Auf Festplatte (Standard) | `search/fulltext.sqlite3` im Arbeitsverzeichnis | Große Archive; übersteht Neustarts |
| Nur im Arbeitsspeicher | Keine Daten auf der Festplatte; wird bei jedem Start neu erstellt | Keine abgeleitete Kopie des Nachrichtentextes auf der Festplatte |
| Aus | Kein Index; **Neueste zuerst · exakter Text** bleibt erhalten | Minimale Installationen |

Der Hauptadministrator wählt den Modus unter **„Journal“ → „Filter“ → „Suchindex“** für jeden Arbeitsbereich aus. `TGWITNESS_FULLTEXT=disk|memory|off` Er legt die Standardeinstellung für Arbeitsbereiche fest, die keine eigene Auswahl haben. Durch Umschalten auf „Speicher“ oder „Aus“ wird die Datei gelöscht. Die Indexdatei verfügt über denselben Schutz wie das Protokoll: Sie befindet sich im Verzeichnis für private Daten . Sie ist nicht verschlüsselt und wird nicht in Backups oder externen Kopien gespeichert.

Neue Einträge werden innerhalb von Sekunden im Hintergrund indiziert; bei einer Suche wird zudem zunächst ein kurzer Rückstand indiziert, sodass ein gerade erst gespeicherter Eintrag gefunden wird. Ein bestehendes Protokoll wird nach der Aktualisierung indiziert, ohne das Panel zu blockieren; bis dahin umfassen die Ergebnisse die indizierten Einträge, und das Protokoll zeigt den Fortschritt an. **Der Neuaufbau des Index** beginnt erneut ab dem ersten Eintrag.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` Das Panel muss beendet werden (ansonsten Exit-Code 3). Bei `--json`, enthält die Standardausgabe nur das Ergebnis; der Fortschritt wird an die Standardfehlerausgabe geleitet.

## Ergebnisse und das signierte Protokoll

Der Index speichert die Sequenznummer und den Hash des letzten Protokoll-Eintrags, den er abdeckt, und gleicht diese beim Öffnen mit dem Protokoll ab. Ein ersetztes, wiederhergestelltes oder bearbeitetes Protokoll führt zu einer Neuerstellung. Jede Antwort meldet diese Position, und jeder Treffer wird anhand seiner Sequenznummer aus dem signierten Protokoll zurückgelesen: Der Index entscheidet, welche Einträge in welcher Reihenfolge angezeigt werden, niemals jedoch über deren Inhalt. Der Chat-Zugriff gilt für das eigene Chat-Feld des Protokolls, nicht für den Inhalt des Index.

## Erkannter Text

OCR-Ergebnisse und Transkripte verbleiben in ihren verschlüsselten Artefakten. Ihr Index existiert nur im Arbeitsspeicher und wird nach Abschluss eines Erkennungsauftrags neu erstellt. Ein Treffer erscheint in seinem `media.saved` Datensatz, gekennzeichnet als maschinelle Erkennung mit Angabe der Engine, des Modells und eines Auszugs; er wird niemals als in Telegram gesendeter Text dargestellt. Derselbe Index dient der **Suche nach erkanntem Text**, die weiterhin auch einfache Teilzeichenfolgen abgleicht.

## Zugriff

Der Chat-bezogene Zugriff findet nur Datensätze aus den jeweiligen Chats, einschließlich des erkannten Textes ihrer Anhänge. `chat:` und andere Filter können diese Menge lediglich eingrenzen. Der Indexstatus, der beim zugriffsbegrenzten Zugriff angezeigt wird, lässt die Gesamtzahlen des Protokolls außer Acht. Nur der Hauptadministrator kann den Modus ändern oder den Index neu erstellen.

## Fragen Sie das Archiv und MCP

**„Ask the Archive“** bezieht seine Quellen aus diesem Index, sobald dieser fertiggestellt ist: die besten Übereinstimmungen aus den ausgewählten Chats, wobei ein gespeicherter Text nur einmal gezählt wird. Es werden bis zu 24 Quellen gesendet; lange Texte werden um die Übereinstimmung herum gekürzt und als abgeschnitten markiert. Anfragen zu den letzten Änderungen, gespeicherten Versionen einer Nachricht und Suchanfragen, während der Index noch erstellt wird, nutzen den vorherigen chronologischen Abruf. Die Vorschau zeigt an, welche Methode verwendet wurde.

MCP-Clients können `search_messages` mit `ranked=true` aufrufen und mit `next_offset`. Verbindungen mit eingeschränktem Zugriff erhalten nur ihre eigenen Chats.

Die nummerierte Paginierung umfasst unabhängig von der Seitengröße höchstens die ersten 1,000-Ergebnisse. Grenzen Sie die Suche, den Chat oder den Zeitraum ein, um weitere Treffer zu prüfen. Bei der Suche nach Neueste zuerst werden Nachrichten, OCR- und Transkriptionsergebnisse vor der Auswahl jeder Seite sortiert.

## Abhängigkeiten

| Paket | Lizenz | Warum |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Russische und ukrainische Lemmata; Wörterbücher werden lokal geladen |
| snowballstemmer | BSD-3-Klausel | Englische Wortstämme, reines Python |
| jieba | MIT | Segmentierung chinesischer Suchanfragen, reines Python (nur Quellcode-Verteilung) |
| pymorphy3-dicts-uk (optional) | GPL-3.0 | Vollständiges ukrainisches Wörterbuch |

SQLite FTS5 benötigt den `unicode61` Tokenizer ist erforderlich; dieser ist Teil von SQLite in aktuellen Python-Builds. Ohne ihn meldet die Best-Match-Suche, dass er nicht verfügbar ist.

## Benchmark

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`Erstellt ein deterministisches, signiertes Protokoll aus gemischten russischen, ukrainischen, englischen, chinesischen und japanischen Nachrichten mit Links und Handles in 200 Chats, erstellt den Index und misst die Dauer typischer Suchvorgänge (50 Ergebnisse, Median aus 7 Durchläufen).

Gemessen unter Windows 11, Intel Core i9-13900K, 128 GB RAM, Python 3.12.10, SQLite 3.49.1, Daten auf einem exFAT-Laufwerk, Analysator `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Maßnahme | Ergebnis |
| --- | --- |
| Signiertes Protokoll | 1.000.000 Nachrichten, 1,50 GiB, in 19 Minuten geschrieben |
| Erstellung eines Indexes aus dem Protokoll | 71 s, etwa 14.141 Nachrichten pro Sekunde |
| Indexdatei | 58 MiB, 3,8 % des Protokolls |
| Suche direkt nach einem neuen Eintrag | Median 8 ms, P95 9 ms |
| Vorherige Teilstringsuche, dasselbe Protokoll | `перевод` 3,2 s, `银行转账` 2,6 s, `verify-account.example` 2,6 s |

| Suche | Übereinstimmende Datensätze | Beste Übereinstimmung, Median | S. 95 | Neueste zuerst, Median |
| --- | --- | --- | --- | --- |
| Allgemeine Wörter, Wortformen: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Zwei Wörter: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Seltenes Wort: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Genauer Wortlaut: `"переказ коштів на картку"` | wird nicht gezählt | 35 ms | 36 ms | 6 ms |
| Domain mit Subdomains: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @Benutzername: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Chinesisch ohne Leerzeichen: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Japanisch: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Englischer Stamm: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| ODER und Ausschluss: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Chat-Filter: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Zeitraumfilter: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Eine exakte Phrase wird wörtlich bei Kandidaten in der Rangfolge überprüft, bis die Seite voll ist; daher wird deren Gesamtzahl nicht mitgezählt. Die Bearbeitungszeiten steigen mit der Anzahl der übereinstimmenden Datensätze; durch Eingrenzung des Chats oder des Zeitraums lassen sich umfassende Suchen beschleunigen. Das synthetische Korpus wiederholt einen kleinen Wortschatz, sodass häufige Wörter weitaus mehr Datensätze treffen als in echten Chats.
