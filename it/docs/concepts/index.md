# Scoprite come funziona la raccolta delle prove

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/concepts/

Un messaggio può cambiare. La registrazione di ciò che avete osservato deve rimanere verificabile.

Scoprite qui di seguito due piccoli esperimenti. Utilizzano messaggi fittizi, rimangono all’interno del vostro browser e non si connettono mai a Telegram.

## Da un’esportazione della chat a un documento verificabile

[Le esportazioni di Telegram Desktop](https://telegram.org/blog/export-and-more) salvano la cronologia delle chat e i contenuti multimediali disponibili in formato HTML o JSON per l’utilizzo offline. TgWitness aggiunge un registro continuo delle modifiche ricevute, delle firme sulle osservazioni e sulle esportazioni, nonché dei punti di controllo che i destinatari possono confrontare in modo indipendente.

| Compito | Esportazione da Telegram Desktop | TgWitness |
| --- | --- | --- |
| Leggi le conversazioni salvate | HTML o JSON con file multimediali selezionati | Chat salvate, registro ricercabile e report offline |
| Seguire l’evoluzione nel tempo | La cronologia disponibile al momento dell’esportazione | Le versioni acquisite in precedenza, le modifiche successive e le osservazioni relative alle cancellazioni vengono conservate insieme |
| Verificare i file dopo il passaggio di consegne | I file di esportazione standard in formato HTML/JSON non sono firmati | Manifesto firmato, firme per singolo record e report HTML/PDF/JSON sigillati, verificati rispetto a una chiave di raccolta attendibile |
| Confronta con uno stato precedente conservato | Conservare una copia di riferimento separata o un hash | Checkpoint firmati, un testimone separato e timestamp esterni opzionali |

Il confronto relativo alla firma dei file si basa sugli [strumenti di esportazione di](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) [Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) esaminati il 2 novembre 2026. TgWitness appone la firma con la chiave del collector; i controlli riportati di seguito mostrano come un destinatario la utilizza.

## Un messaggio, tre osservazioni

Quando Telegram invia un nuovo messaggio, una modifica o una notifica di cancellazione, il sistema di raccolta aggiunge tre osservazioni distinte. La modifica non sostituisce la prima registrazione. Una notifica di cancellazione non la cancella.

01 / PERCORSO DEL MESSAGGIOSequenza illustrativa

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Collector · Registro · aggiornamento → · aggiungi →

VISUALIZZAZIONE DELLA CHAT ATTUALE Messaggio n. 42

Messaggio cancellato

Il messaggio è scomparso dalla schermata della chat.

REGISTRO DI OSSERVAZIONE 3 record

1. 01

   `message.new`

   Appuntamento alle ore 10:00

   ✓
2. 02

   `message.edited`

   Appuntamento alle ore 11:00

   ✓
3. 03

   `message.deleted`

   Avviso di cancellazione per il n. 42

   ✓

Tutte e tre le osservazioni ricevute rimangono nel registro.

Percorso semplificato per una fonte già selezionata. Anche i registri operativi condividono il registro effettivo. L’acquisizione dipende da ciò che l’account può visualizzare e da ciò che Telegram fornisce.

Una notifica di cancellazione non fornisce né un’ora di cancellazione attendibile né l’identità della persona che ha cancellato il messaggio. Mantenere sconosciuti tali valori preserva la distinzione tra un’osservazione e una supposizione.

## Modificare un record. Seguire l’hash.

Ogni registrazione contiene l’hash della registrazione precedente. Il proprio hash copre i campi relativi all’evento, compreso tale collegamento. Un punto di controllo conservato esternamente fissa una lunghezza specifica del registro e l’hash iniziale.

02 / HASH-CHAIN SANDBOXSHA-256 reale · esempi di registrazioni

REGISTRAZIONE 01**Messaggio ricevuto**`h₁ = SHA-256(e₁)`Link a 64 zeri

REGISTRAZIONE 02**Appuntamento alle ore 11:00**`h₂ = SHA-256(e₂)`Include h₁

REGISTRAZIONE 03**Cancellazione rilevata**`h₃ = SHA-256(e₃)`Include h₂

CONSERVATO ALTROVE**3 record · intestazione `h₃`**Si confronti questo confine definito con il registro fornito.

La modifica di un evento ne altera l’hash. La ricostruzione della catena ne modifica l’intestazione. La rimozione della coda la rende più breve del punto di controllo conservato.

**Esaminare il record 2 e gli hash completi**

Questo è l’esatto JSON in formato UTF-8 sottoposto a hash in questo esempio. I valori sono fittizi; i nove campi e la serializzazione corrispondono al formato del registro.

```

```

Hash della registrazione salvata n. 2

``

Hash del record 2 ricalcolato

``

Questa sandbox calcola gli hash, non le firme. Il vero verificatore controlla anche la firma Ed25519, la sequenza e il link di ogni evento. La ricostruzione dei soli hash non è sufficiente a generare firme valide con la chiave fidata.

## Le regole effettive, in poche righe

HASH + FIRMA

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** serializza i nove campi dell’evento come JSON in formato UTF-8: chiavi ordinate, senza spazi bianchi aggiuntivi, senza escape ASCII e senza valori NaN/infinito. Il valore `previous_hash` dell’evento è hi−1. Il valore h0 visualizzato indica 64 caratteri zero; le firme coprono i 32 byte grezzi del digest.

I nove campi sono `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` e `previous_hash`. Si tratta [della codifica JSON documentata](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#event-canonicalization) di TgWitness; l’hash e la firma in sé non sono campi di immissione dell’hash.

PUNTO DI CONTROLLO CONSERVATO

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Verifichi la firma del checkpoint sotto la chiave del collettore fissata in primo piano, quindi confronti i suoi confini con quelli del registro verificato. Un’esportazione successiva potrebbe contenere più record; deve comunque corrispondere al checkpoint precedente.

## Tre domande, tre diversi controlli

[01 / INTEGRITÀ**Questo registro è stato modificato?** Verificare gli hash e le firme rispetto a una chiave affidabile separata.](https://phishdestroy.github.io/TgWitness/it/docs/exports/)[02 / CONTINUITÀ**Cosa era stato conservato in precedenza?** Si confronti un’esportazione firmata con i punti di controllo conservati da un testimone indipendente.](https://phishdestroy.github.io/TgWitness/it/docs/witness/)[03 / CONSEGNA**Sono pervenuti questi eventi di prova?** Confrontare le azioni controllate di invio, modifica ed eliminazione con il registro di ciascun account.](https://phishdestroy.github.io/TgWitness/it/docs/cases/)

Utilizzare le firme per verificare i record conservati, i checkpoint per confrontare un limite precedente e i test di consegna controllata per misurare la raccolta. Ciascuno di essi risponde a una domanda specifica. [Leggere l’ambito di verifica e i presupposti di affidabilità.](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#verification-scope)

Segua [l’intero processo investigativo,](https://phishdestroy.github.io/TgWitness/it/docs/cases/) dall’acquisizione fino alla compilazione del fascicolo.
