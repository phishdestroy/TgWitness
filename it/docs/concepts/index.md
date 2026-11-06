# Telegram · Scoprite come funziona la raccolta delle prove

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/concepts/

I messaggi cambiano. La Sua traccia di ciò che ha visto non dovrebbe, e chiunque dovrebbe poterlo verificare.

Qui sotto due piccoli esperimenti. Messaggi fittizi, tutto gira nel browser, niente va a Telegram.

## Da un’esportazione della chat a un documento verificabile

Un’[esportazione di Telegram Desktop](https://telegram.org/blog/export-and-more) salva la cronologia visibile in quel momento come HTML o JSON. TgWitness aggiunge un diario continuo delle modifiche, firme su ogni voce e punti di controllo con cui altri possono confrontarsi.

| Compito | Esportazione da Telegram Desktop | TgWitness |
| --- | --- | --- |
| Leggi le conversazioni salvate | HTML o JSON con file multimediali selezionati | Chat salvate, registro ricercabile e report offline |
| Seguire l’evoluzione nel tempo | La cronologia disponibile al momento dell’esportazione | Versioni vecchie, modifiche successive ed eliminazioni, tutto conservato |
| Verificare i file dopo il passaggio di consegne | I file di esportazione standard in formato HTML/JSON non sono firmati | Manifest firmato, voci firmate e report sigillati, verificati con una chiave affidabile |
| Confronta con uno stato precedente conservato | Conservare una copia di riferimento separata o un hash | Checkpoint firmati, un testimone separato e timestamp esterni opzionali |

Il confronto si basa sul [codice di esportazione di Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) al 2 novembre 2026.

## Un messaggio, tre osservazioni

Un messaggio nuovo, una modifica e un’eliminazione diventano tre voci separate. La modifica non sovrascrive la prima e l’eliminazione non la cancella.

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

Telegram non dice chi ha eliminato un messaggio né quando esattamente. TgWitness lascia quei campi vuoti invece di tirare a indovinare.

## Modificare un record. Seguire l’hash.

Ogni voce contiene l’hash della precedente. Un punto di controllo conservato altrove fissa la lunghezza del diario e l’ultimo hash.

02 / SANDBOX HASH-CHAINSHA-256 reale · esempi di registrazioni

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

**C** sono i nove campi dell’evento come JSON UTF-8: chiavi ordinate, niente spazi in più, niente escape ASCII, niente NaN/infinito. `previous_hash` è hi−1, h0 sono 64 zeri e le firme coprono i 32 byte grezzi del digest.

I campi: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Specifica completa: [codifica degli eventi](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#event-canonicalization).

PUNTO DI CONTROLLO CONSERVATO

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Verifichi la firma del punto di controllo con la chiave fissata, poi lo confronti con il diario. Un’esportazione successiva può essere più lunga, ma deve coincidere al punto di controllo.

## Tre domande, tre diversi controlli

[01 / INTEGRITÀ**Questo registro è stato modificato?** Hash e firme contro una chiave di cui si fida.](https://phishdestroy.github.io/TgWitness/it/docs/exports/)[02 / CONTINUITÀ**Cosa era stato conservato in precedenza?** Confronti l’esportazione con i punti di controllo conservati da un testimone.](https://phishdestroy.github.io/TgWitness/it/docs/witness/)[03 / CONSEGNA**Sono pervenuti questi eventi di prova?** Invii, modifichi ed elimini messaggi di prova e veda cosa ha catturato ogni account.](https://phishdestroy.github.io/TgWitness/it/docs/cases/)

Le firme rispondono a «è stato modificato?», i punti di controllo a «corrisponde a ciò che c’era prima?», i messaggi di prova a «abbiamo catturato tutto?». [Cosa dimostra la verifica e cosa no.](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#verification-scope)

Avanti: un’[indagine su un intero account](https://phishdestroy.github.io/TgWitness/it/docs/cases/) dall’inizio al pacchetto del caso.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
