# Come funziona la raccolta delle prove

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/how-it-works/

Spiegazione di catena di hash, firme, punti di controllo e testimoni con le formule esatte utilizzate dal verificatore.

TgWitness conserva ciò che un account di raccolta ha rilevato, collega tali osservazioni in un registro firmato e consente a un’altra persona di verificare un’esportazione confrontandola con una chiave affidabile e un punto di controllo precedentemente conservato.

Il [sito web di documentazione locale](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) aggiunge esempi interattivi all’indirizzo `/docs/concepts/` e un esploratore delle decisioni dei checkpoint all’indirizzo `/docs/witness/`. Tutti i messaggi di esempio, i conteggi e i ritardi sono fittizi. Gli hash nella sandbox della catena vengono calcolati con SHA-256 nel browser. Nulla viene inviato a Telegram.

## Un messaggio cambia; le osservazioni si accumulano

Diagramma di sequenza · Telegram → Collector: Nuovo messaggio: Ci vediamo alle 10:00; Collector → Registro firmato: Aggiungi messaggio.new; Telegram → Collector: Modifica: Appuntamento alle 11:00; Collector → Registro firmato: Aggiungere "message.edited"; Telegram → Collector: Avviso di cancellazione; Collector → Registro firmato: Aggiungere il messaggio.cancellato; Nota su Registro firmato: Vengono conservate le osservazioni relative all’originale, alle modifiche e alle cancellazioni · Telegram · Collector · Registro firmato · Nuovo messaggio: Ci vediamo alle 10:00 · Aggiungi messaggio.new · Modifica: Appuntamento alle 11:00 · Aggiungere "message.edited" · Avviso di cancellazione · Aggiungere il messaggio.cancellato · Vengono conservate le osservazioni relativeall’originale, alle modifiche e alle cancellazioni

**Diagramma sotto forma di testo**

1. Telegram → Collector: Nuovo messaggio: Ci vediamo alle 10:00
2. Collector → Registro firmato: Aggiungi messaggio.new
3. Telegram → Collector: Modifica: Appuntamento alle 11:00
4. Collector → Registro firmato: Aggiungere "message.edited"
5. Telegram → Collector: Avviso di cancellazione
6. Collector → Registro firmato: Aggiungere il messaggio.cancellato
7. Nota su Registro firmato: Vengono conservate le osservazioni relative all’originale, alle modifiche e alle cancellazioni

Questa sequenza semplificata presuppone che Telegram abbia consegnato ogni aggiornamento e che l’account selezionato potesse visualizzarlo. Anche gli eventi operativi vengono registrati nel registro. Una notifica di cancellazione non indica chi ha effettuato la cancellazione né l’ora esatta della stessa. Le consegne ripetute costituiscono osservazioni separate; non vi è alcuna eliminazione dei duplicati a livello di registro.

## Cosa comprende un hash

![Osservare, codificare, generare l’hash e firmare: ogni nuovo evento include l’hash precedente.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Legga la formula dall’interno verso l’esterno: **C** trasforma i nove campi in byte esatti; **SHA-256** ne produce il digest; **«hex»** indica il formato esadecimale in cui tale digest viene memorizzato. L’hash precedente è già contenuto nell’evento. **«unhex»** riconverte l’hash memorizzato nei 32 byte che Ed25519 firma.

[Diagramma statico della catena](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Sia C(ei) il JSON canonico in formato UTF-8 dei nove campi di evento. Il primo `previous_hash` è composto da 64 caratteri zero. Ogni record successivo include l’hash esadecimale del record precedente:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

La firma copre i 32 byte grezzi del digest. L’input dell’hash contiene esattamente `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` e `previous_hash`. Le chiavi degli oggetti sono ordinate; gli spazi bianchi e gli escape ASCII sono omessi; i valori NaN e infinito vengono scartati. Si veda la [codifica esatta](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#event-canonicalization).

Diagramma di flusso · 64 caratteri zero → Record 1 / hash h1; Record 1 / hash h1 → La registrazione 2 include h1 / hash h2; La registrazione 2 include h1 / hash h2 → Il record 3 include h2 / hash h3; Il record 3 include h2 / hash h3 → Punto di controllo firmato: conteggio 3, intestazione h3 (conservare altrove) · 64 caratteri zero · Record 1 / hash h1 · La registrazione 2include h1 / hash h2 · Il record 3 include h2/ hash h3 · Punto di controllofirmato: conteggio 3,intestazione h3 · conservare altrove

**Diagramma sotto forma di testo**

1. 64 caratteri zero → Record 1 / hash h1
2. Record 1 / hash h1 → La registrazione 2 include h1 / hash h2
3. La registrazione 2 include h1 / hash h2 → Il record 3 include h2 / hash h3
4. Il record 3 include h2 / hash h3 → Punto di controllo firmato: conteggio 3, intestazione h3 (conservare altrove)

| Modifica al registro fornito | Cosa lo rileva |
| --- | --- |
| Modificare il record 2 mantenendo il suo hash salvato | L’hash dell’evento ricalcolato risulta diverso; la sua firma non copre più l’evento modificato |
| Ricostruire il record modificato e ogni hash successivo | Le firme originali risultano non valide; anche un checkpoint conservato al confine interessato presenta discrepanze |
| Rimuovere la parte finale, ma mantenere intatto il prefisso rimanente | Un punto di controllo precedente, conservato oltre il prefisso fornito, rivela che l’esportazione è troppo breve |
| Rifirmare un registro sostitutivo con un’altra chiave | Un’impronta digitale della chiave, verificata separatamente, respinge l’identità sostitutiva |

![La modifica di un campo salvato ne altera il digest; il calcolo di nuovi hash non ripristina le firme originali.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Si provi ad applicare la logica al record 2:** si modifichi `Meet at 11:00` in `Meet at 12:00` nell’ evento salvato. Il suo hash ricalcolato non corrisponde più. Il ricalcolo della catena successiva può ripararne i collegamenti, ma non può far sì che le firme originali coprano i nuovi digest. Una modifica osservata su Telegram, al contrario, diventa un nuovo record del registro.

[Diagramma delle modifiche statiche](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

I soli link hash non impediscono a qualcuno di ricalcolare una catena sostitutiva. L’affidabilità deriva dalla verifica delle firme mediante una chiave considerata attendibile in modo indipendente e dal confronto con i riferimenti conservati al di fuori del collettore.

## Cosa aggiunge un punto di controllo precedente

![Mantenere il conteggio 3 e l’intestazione h3; un’esportazione successiva di 4 record viene verificata alla posizione 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Il riferimento rimane invariato mentre il registro cresce.** Se il punto di controllo indica «3 record, intestazione h3», un’esportazione di quattro record può essere accettata in quanto corrisponde a h3 nella posizione 3. La sua intestazione più recente è h4, che dovrebbe risultare diversa. Un’esportazione di soli due record non viene accettata.

[Diagramma statico dei punti di controllo](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Dopo aver verificato la firma del checkpoint, richiedere:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Un’esportazione può estendersi oltre un punto di controllo. Deve corrispondere al confine conservato. Il verificatore reale controlla inoltre la sequenza di ogni evento, il collegamento precedente, l’hash e la firma. Confrontando solo l’intestazione finale memorizzata si rischierebbe di trascurare un record interno alterato il cui hash salvato non è stato aggiornato.

## Il posto giusto per un testimone

Diagramma di flusso · Collector / sessione dell’account / chiave A → Endpoint di checkpoint in sola lettura; Witness / chiave di raccolta fissata / chiave propria B → Registro delle testimonianze separato e firmato; Witness / chiave di raccolta fissata / chiave propria B → Endpoint di checkpoint in sola lettura (Richiedere una verifica); Endpoint di checkpoint in sola lettura → Witness / chiave di raccolta fissata / chiave propria B (Risposta firmata); Witness / chiave di raccolta fissata / chiave propria B → Canale con post TGW1 firmati (API del bot / token proprio) · Host A · Host B · Collector / sessionedell’account / chiave A · Endpoint di checkpoint insola lettura · Witness / chiave diraccolta fissata / chiavepropria B · Registro delletestimonianze separato efirmato · Canale con post TGW1firmati · Richiedere una verifica · Risposta firmata · API del bot / token proprio

**Diagramma sotto forma di testo**

1. Collector / sessione dell’account / chiave A → Endpoint di checkpoint in sola lettura
2. Witness / chiave di raccolta fissata / chiave propria B → Registro delle testimonianze separato e firmato
3. Witness / chiave di raccolta fissata / chiave propria B → Endpoint di checkpoint in sola lettura (Richiedere una verifica)
4. Endpoint di checkpoint in sola lettura → Witness / chiave di raccolta fissata / chiave propria B (Risposta firmata)
5. Witness / chiave di raccolta fissata / chiave propria B → Canale con post TGW1 firmati (API del bot / token proprio)

Il witness registra i rollback, un conteggio diverso a parità di numero, chiavi modificate, risposte non valide e risposte mancanti. Un conteggio più elevato di per sé non garantisce che ogni registrazione precedente rimanga invariata; si confronti l’esportazione con i checkpoint conservati. Un witness su un altro host evita di subire le interruzioni di servizio dell’host del collettore; un operatore separato garantisce ulteriore indipendenza.

Il «witness» attesta lo stato del registro segnalato dal «collector». Esso non osserva in modo indipendente tutti i messaggi di Telegram. Si veda [la configurazione del «witness](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/)».

## Verifica del funzionamento rispetto ad azioni note

Si raccomanda di utilizzare un gruppo di controllo, account di raccolta distinti e un indicatore di novità. Si prega di inviare, modificare ed eliminare i messaggi in modo deliberato, verificando l’acquisizione dei dati tra una fase e l’altra. Si raccomanda di definire le azioni previste e un limite temporale prima di esaminare i risultati.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Conta solo l’azione prevista; le ricevute duplicate non aumentano il numeratore. Il denominatore deve essere diverso da zero. Una ricevuta mancante non presenta alcun ritardo misurato. Documentare l’incertezza dell’orologio; utilizzare il proprio tempo di azione di cancellazione controllato, poiché Telegram non fornisce l’ora esatta della cancellazione. Un risultato come 5/6 (83,3%) descrive le azioni di test, non la completezza dell’intero traffico di Telegram.

## Scegliete un flusso di lavoro

[La guida completa all’indagine](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/) segue lo svolgimento di un incidente attraverso un canale, un gruppo, un bot e una chat privata:

1. Attivare la modalità di indagine sull’intero account e catalogare tutte le chat accessibili.
2. Acquisisca istantanee del registro, la cronologia completa per ogni chat e gli allegati conservati.
3. Conservare le modifiche in tempo reale e qualsiasi interazione intenzionale con i pannelli, corredata delle relative ricevute.
4. Tracciate gli ID numerici dei mittenti, le relazioni di risposta, le destinazioni ricorrenti e gli hash dei file attraverso i record citati e i profili delle persone.
5. Ricostruite una cronologia delle conversazioni incrociate con indicazione sia dei timestamp che delle lacune esplicite.
6. Confrontare gli spazi di lavoro di altri account mantenendo separate le rispettive origini e chiavi.
7. Compilare e verificare i registri firmati, i profili e le esportazioni della cronologia insieme alle note relative al caso.

La guida «`/docs/cases/`» del sito web include una mappa interattiva dei casi e varianti per controversie relative ai bot, messaggi rimossi e partecipanti che cambiano nome. Le note sui casi e l’analisi incrociata tra spazi di lavoro sono esterne; l’applicazione non genera automaticamente un grafico investigativo globale né un archivio dei casi unificato.

[Convalida completata e lavoro residuo](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/) · [Esportare e verificare](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#investigation-handoff) · [Inizi con un solo account](https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/)
