# Telegram · Ricerca full-text

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/search/

Ricerca dei messaggi salvati in base a forme lessicali, frasi esatte, domini e @nomiutente, con i risultati più pertinenti in primo piano, grazie all’indice collegato al registro firmato.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Indagine](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/)

![Indagine](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Analisi dell'archivio](https://phishdestroy.github.io/TgWitness/it/docs/reference/analysis/) · [OCR locale e trascrizione](https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Anteprima.** In **"Journal**", selezionare **"Corrispondenza migliore · forme della parola"** accanto al campo di ricerca. I risultati sono ordinati con l'algoritmo BM25 e corrispondono ad altre forme della stessa parola: *"перевод"* trova *"переводом"* e *"переводы"*, *"transfer"* trova *"transfers"*, una frase in cinese viene trovata senza spazi. L'opzione "**Più recenti per primi · testo esatto"** mantiene la precedente ricerca di sottostringhe sull'intero record.

L’indice è un dato derivato. Viene ricostruito dal registro firmato, non è mai firmato di per sé e non viene mai esportato. I record originali non subiscono alcuna modifica.

**In questa pagina**

- [Sintassi di ricerca](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#search-syntax)
- [Lingue](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#languages)
- [Dove si trova l'indice](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#where-the-index-lives)
- [Risultati e il registro firmato](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#results-and-the-signed-journal)
- [Testo riconosciuto](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#recognized-text)
- [Access](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#access)
- [Chiedi all’archivio e MCP](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#ask-the-archive-and-mcp)
- [Dipendenze](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#dependencies)
- [Benchmark](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#benchmark)

## Sintassi di ricerca

| Scrivere | Risultati |
| --- | --- |
| `перевод карта` | Record contenenti entrambe le parole, in qualsiasi forma |
| `"переводом на карту"` | La frase esatta, in questo ordine |
| `бонус OR подарок` | Una delle due parole |
| `перевод -казино` | Registrazioni senza la parola esclusa |
| `example.com` | Il dominio e i suoi sottodomini, compresi quelli presenti nei link nascosti e negli URL dei pulsanti |
| `@username`, `t.me/username` | Menzioni e link relativi all’account, nonché i messaggi da esso inviati |
| `#tag` | L'hashtag |
| `+79991234567`, un indirizzo di wallet, un indirizzo e-mail | Lo stesso valore nel testo o nei link |
| `from:@username`, `from:123456` | Messaggi da quel mittente |
| `chat:-1001234567890` | Una sola chat; può limitare solo il proprio accesso |
| `id:42` | Versioni salvate del messaggio 42 |
| `since:2026-01-01 until:2026-01-31` | Periodo di osservazione: una data senza ora copre l’intera giornata |
| `kind:edited` | Solo modifiche (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Testo riconosciuto al posto dei messaggi o insieme a essi |

Le preposizioni e altre parole funzionali vengono ignorate quando sono presenti altre parole. Le lettere simili mescolate all’interno di una parola (ad esempio una *«a»* latina all’interno di una parola cirillica), le lettere Unicode a larghezza intera e decorative e i caratteri invisibili vengono normalizzati.

## Lingue

La lingua viene rilevata per ogni record in base allo script e alle lettere in esso contenute:

| Script | Corrispondenza |
| --- | --- |
| Cirillico | Lemmi russi e ucraini con [pymorphy3](https://github.com/no-plagiarism/pymorphy3). In assenza del dizionario ucraino opzionale, viene utilizzato uno stemmer ucraino leggero |
| Latino | Stemmer Snowball in inglese; i segni diacritici vengono ignorati |
| Cinese, giapponese, coreano, tailandese, laotiano, khmer, birmano | Coppie di caratteri sovrapposti: qualsiasi frase viene individuata senza spazi. Le query in cinese vengono suddivise in parole con jieba |
| Altri script | Parole esatte |

Il dizionario ucraino (`pymorphy3-dicts-uk`) è distribuito sotto licenza GPL-3.0, pertanto non è installato di default. Installarlo con `pip install "tgwitness[uk-dictionary]"`; l'indice rileva il nuovo analizzatore e si ricostruisce automaticamente.

## Dove si trova l'indice

| Modalità | Archiviazione | Utilizzo |
| --- | --- | --- |
| Su disco (impostazione predefinita) | `search/fulltext.sqlite3` nella directory dell'area di lavoro | Archivi di grandi dimensioni; resiste ai riavvii |
| Solo in memoria | Nulla viene salvato su disco; viene ricostruito ad ogni avvio | Nessuna copia derivata del testo dei messaggi su disco |
| Disattivato | Nessun indice; **i più recenti per primi · il testo esatto** rimane invariato | Installazioni minime |

L'amministratore principale sceglie la modalità in **Registro → Filtri → Indice di ricerca** per ogni area di lavoro. `TGWITNESS_FULLTEXT=disk|memory|off` Imposta il valore predefinito per gli spazi di lavoro che non hanno una propria impostazione. Passando alla modalità «memoria» o disattivando l’opzione, il file viene eliminato. Il file dell’indice ha la stessa protezione del registro: si trova nella directory dei dati privati . Non è crittografato e non fa parte dei backup né delle copie fuori sede.

I nuovi record vengono indicizzati in background in pochi secondi; una ricerca indicizza innanzitutto anche un breve arretrato, in modo da individuare un record salvato solo un attimo prima. Un registro esistente viene indicizzato dopo l’aggiornamento senza bloccare il pannello; fino a quel momento, i risultati coprono i record indicizzati e il registro mostra lo stato di avanzamento. **La ricostruzione dell’indice** ricomincia dal primo record.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` è necessario che il pannello sia arrestato (in caso contrario, codice di uscita 3). Con `--json`, l'output standard riporta solo il risultato; lo stato di avanzamento viene inviato all'output di errore standard.

## Risultati e registro firmato

L'indice memorizza il numero di sequenza e l'hash dell'ultimo record del registro che copre e li verifica confrontandoli con il registro all'apertura. Un registro sostituito, ripristinato o modificato comporta una ricostruzione. Ogni risposta riporta questa posizione e ogni risultato viene riletto dal registro firmato in base al suo numero di sequenza: l'indice decide quali record mostrare e in quale ordine, mai il loro contenuto. L'accesso alla chat viene applicato al campo chat del registro stesso, non al contenuto dell'indice.

## Testo riconosciuto

L’OCR e le trascrizioni rimangono nei rispettivi artefatti crittografati. Il loro indice esiste solo in memoria e viene ricostruito al completamento di un’operazione di riconoscimento. Un risultato viene visualizzato nel relativo `media.saved` record, etichettato come “riconoscimento automatico” con l’indicazione del motore, del modello e di un estratto; non viene mai presentato come testo inviato su Telegram. Lo stesso indice serve alla funzione **“Cerca testo riconosciuto**”, che continua a trovare corrispondenze anche con sottostringhe in formato semplice.

## Accesso

L'accesso limitato alle chat individua solo i record provenienti dalle proprie chat, compreso il testo riconosciuto dei relativi allegati. `chat:` e altri filtri possono solo restringere tale insieme. Lo stato dell’indice mostrato all’accesso limitato omette i totali del registro. Solo l’amministratore principale può modificare la modalità o ricostruire l’indice.

## Chiedi all’archivio e all’MCP

**Chiedere all’archivio** di recuperare le fonti da questo indice una volta completato: le migliori corrispondenze tra le chat selezionate, con ogni testo salvato conteggiato una sola volta. Vengono inviate fino a 24 fonti; i testi lunghi vengono troncati in corrispondenza della corrispondenza e contrassegnati come troncati. Le richieste relative alle modifiche recenti, alle versioni salvate di un messaggio e alle ricerche mentre l’indice è ancora in fase di creazione utilizzano il recupero cronologico precedente. L’anteprima mostra quale metodo è stato utilizzato.

I client MCP possono chiamare `search_messages` con `ranked=true` e inviare messaggi con `next_offset`. Le connessioni con ambito ricevono solo le proprie chat.

L'impaginazione ordinata copre al massimo i primi risultati 1,000, indipendentemente dalle dimensioni della pagina. Restringere la query, la chat o il periodo per esaminare ulteriori corrispondenze. Le ricerche più recenti per prime ordinano i messaggi, i risultati OCR e di trascrizione prima di selezionare ciascuna pagina.

## Dipendenze

| Pacchetto | Licenza | Perché |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Lemmi russi e ucraini; i dizionari vengono caricati localmente |
| snowballstemmer | BSD a 3 clausole | Radici in inglese, Python puro |
| jieba | MIT | Segmentazione delle query in cinese, Python puro (solo distribuzione del codice sorgente) |
| pymorphy3-dicts-uk (facoltativo) | GPL-3.0 | Dizionario completo dell'ucraino |

È richiesto SQLite FTS5 con il `unicode61` tokenizer; fa parte di SQLite nelle attuali build di Python. Senza di esso, la ricerca della corrispondenza migliore segnala che non è disponibile.

## Benchmark

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`Crea un registro firmato deterministico contenente messaggi misti in russo, ucraino, inglese, cinese e giapponese con link e handle in 200 chat, genera l’indice e misura i tempi delle ricerche tipiche (50 risultati, mediana di 7 esecuzioni).

Testato su Windows 11, Intel Core i9-13900K, 128 GB di RAM, Python 3.12.10, SQLite 3.49.1, dati su un'unità exFAT, analizzatore `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Misura | Risultato |
| --- | --- |
| Registro firmato | 1.000.000 di messaggi, 1,50 GiB, scritti in 19 minuti |
| Creazione dell'indice a partire dal registro | 71 s, circa 14.141 messaggi al secondo |
| File di indice | 58 MiB, pari al 3,8% del registro |
| Cerca subito dopo un nuovo record | Mediana di 8 ms, p95 di 9 ms |
| Ricerca della sottostringa precedente, stesso registro | `перевод` 3,2 s, `银行转账` 2,6 s, `verify-account.example` 2,6 s |

| Cerca | Record corrispondenti | Risultato migliore, mediana | p95 | Più recenti per primi, mediana |
| --- | --- | --- | --- | --- |
| Parole comuni, forme delle parole: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Due parole: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Parola rara: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Frase esatta: `"переказ коштів на картку"` | non conteggiato | 35 ms | 36 ms | 6 ms |
| Dominio con sottodomini: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @username: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Cinese senza spazi: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Giapponese: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Radice inglese: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| Oppure e esclusione: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Filtro chat: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Filtro per periodo: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Una frase esatta viene verificata alla lettera sui candidati in ordine di rilevanza fino a quando la pagina non è piena, quindi il suo totale non viene conteggiato. I tempi aumentano con il numero di record corrispondenti; restringere la chat o il periodo rende più veloci le ricerche generiche. Il corpus sintetico ripete un vocabolario limitato, quindi le parole comuni corrispondono a molti più record rispetto alle chat reali.
