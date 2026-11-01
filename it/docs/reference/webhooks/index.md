# Webhook in uscita

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/webhooks/

Invia eventi selezionati a destinatari HTTPS con firme HMAC, tentativi di reinvio e stato di consegna.

[Guida al flusso di lavoro](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Apri **Integrazioni → Webhook in uscita** nell’area di lavoro selezionata. Aggiungi un destinatario HTTPS, scegli gli eventi relativi a collector/media/export e, facoltativamente, seleziona le chat per nuove osservazioni e modifiche. Il testo dei messaggi è disattivato per impostazione predefinita. L’abilitazione degli estratti aggiunge al massimo 1.000 caratteri agli eventi relativi alle modifiche dei messaggi; i campi Telegram non elaborati e le credenziali non vengono mai inviati.

Copiare una sola volta la chiave segreta HMAC nella configurazione protetta del ricevitore. Essa è crittografata nel vault di TgWitness e non può essere recuperata dal pannello di controllo. Rimuovere e ricreare una destinazione per effettuare la rotazione. **Inviare** alle code **di test sintetiche** un test privo di contenuto di chat; aggiornare lo stato di consegna per verificarne l’esito.

La consegna amplia il ciclo di notifiche esistente insieme ad Apprise. Utilizza il percorso esterno dell’area di lavoro e le restrizioni esistenti relative alle destinazioni private. Non è previsto alcun fallback diretto né reindirizzamento successivo. Gli URL non devono contenere credenziali, stringhe di query o frammenti; gli indirizzi privati richiedono l’ opt-in a livello di rete del server, non un’impostazione che un utente del pannello possa aggirare.

## Payload e firma

Schema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Ogni payload contiene `event_id`, `timestamp`, `workspace`, `type`, `synthetic` e i contatori. Gli eventi basati sul registro includono la loro sequenza e l’hash. Il completamento dell’esportazione completa e i test sintetici sono eventi di consegna, senza alcun riferimento inventato al registro firmato. Le notifiche di cancellazione di Telegram e `missing_on_recheck` rimangono tipi distinti.

L'intestazione `X-TgWitness-Signature` è `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Calcola l'HMAC sui byte esatti `timestamp + "." + raw_request_body`, utilizzando il segreto visualizzato come byte UTF-8. Confronta le firme in tempo costante prima di analizzare o agire sul corpo del messaggio. Rifiuta i timestamp che differiscono di più di cinque minuti dal tuo orologio. Il timestamp viene aggiornato ad ogni tentativo di consegna.

Utilizzare `event_id` come chiave di idempotenza in un archivio permanente, con un vincolo atomico di unicità prima degli effetti collaterali. Una firma valida da sola non impedisce che una richiesta recente venga riprodotta. Conservare gli ID elaborati almeno per l’intera finestra di riprova; conservarli più a lungo se il destinatario può rielaborare gli eventi memorizzati.

## Nuovi tentativi

Le consegne vengono messe in coda in modo permanente prima delle richieste HTTP. Utilizzano la semantica «almeno una volta» : una conferma di ricezione persa o un riavvio potrebbero causare la consegna di un evento con lo stesso ID. Sono previsti otto tentativi con backoff esponenziale, a partire da 15 secondi e con un limite massimo di un’ora. Il successo richiede una risposta 2xx. I processi esauriti lasciano un errore visibile; la consegna non è garantita al termine dei tentativi.

La coda può contenere 1.000 consegne. Quando è piena, la scansione degli eventi del registro viene messa in pausa e ripresa non appena si libera spazio. Il completamento di un’esportazione completa che non può essere messa in coda genera un errore di coda visibile. Vengono tentate fino a cinque consegne per ogni ciclo di notifica e vengono conservati gli ultimi 100 record dei tentativi. La rimozione di una destinazione comporta anche la rimozione delle relative consegne in sospeso.

## Esempio n8n

Importa [il flusso di lavoro di esempio](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). È inattivo e non contiene informazioni riservate né azioni a valle. Imposta `TGWITNESS_WEBHOOK_SECRET` nell’ ambiente del worker n8n, consenti l’accesso a tale ambiente e abilita la funzione integrata `crypto` per il nodo Code. L’esempio utilizza l’opzione raw-body del nodo Webhook, verifica la firma e la validità temporale e conferma gli eventi convalidati. Ciò corrisponde all’[implementazione documentata](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) del nodo.

Prima di aggiungere scritture o notifiche SIEM, aggiungere un'archiviazione idempotente e duratura con chiave `event_id`. Limitare la modifica del flusso di lavoro n8n e la conservazione del registro di esecuzione in base ai dati che si è scelto di inviare. TgWitness non aggiunge comandi in entrata.
