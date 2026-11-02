# Configurazione iniziale e impostazioni

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/settings/

La procedura guidata di configurazione, gli obiettivi, i livelli dell’interfaccia, i percorsi di connessione e le impostazioni condivise da un gruppo di account.

[Account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/) · [Collegamento](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) · [Accesso](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/)

Si apre un nuovo spazio di lavoro `/first-run`: lingua e ora, livello dell’interfaccia, obiettivo, connessione, Telegram e chat. Ogni risposta viene salvata sul server non appena cambia, quindi ricaricando la pagina si riprende dallo stesso passaggio. L’ultima schermata elenca le risposte e consente di tornare a qualsiasi di esse.

La lingua, il fuso orario IANA, il tema e il livello vengono memorizzati per operatore e per area di lavoro. Le impostazioni predefinite sono la lingua del browser, il fuso orario del dispositivo, il tema di sistema e l’ interfaccia semplice. La modifica della lingua mantiene la sessione del pannello. Gli orari nel registro firmato non cambiano mai.

`/settings` Modifica gli stessi record della procedura guidata. La ricerca copre i campi principali, i parametri e i moduli estesi; un campo nascosto può essere aperto senza modificare il livello. I livelli modificano solo ciò che viene visualizzato: il server verifica autonomamente le autorizzazioni. Le impostazioni della raccolta e la prima connessione spettano all’amministratore dell’area di lavoro.

| Livello | Campi | Barra laterale |
| --- | --- | --- |
| Semplice | Solo l’essenziale | Home, Chat, Modifiche, Archivi, Impostazioni |
| Standard | Impostazioni comuni con spiegazioni | Aggiunge Case Board, Account e Accesso |
| Esperto | Tutti i campi, i limiti e i dettagli tecnici | Aggiunge Fonti, Extra, Chiedi all’archivio, Parametri, Account, Registro di sistema e Integrazioni |

[La guida ai pannelli](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/) descrive ciascuna sezione.

## Obiettivi

| Obiettivo | Raccolta | File | Servizi esterni | Indirizzo del server |
| --- | --- | --- | --- | --- |
| Copia d’archivio | Off; **Start** avvia un'esportazione | Foto fino a 20 MB | Off | Automatico |
| Segui le chat | Continuo | Foto e video fino a 60 secondi / 20 MB | Marcatori temporali e notifiche dei problemi | Automatico |
| Prove | Continuo | Tutti i file fino a 1 GB | Timestamp, drand, notifiche | No, nascondilo |

Per le prove si raccomandano la copia esterna, il bot testimone e il controllo del codice. Gli indirizzi di archiviazione e di notifica richiedono innanzitutto una destinazione. Una funzionalità che comunica con un servizio esterno richiede di consentire le richieste al di fuori di Telegram; disattivandola viene proposto di disattivare anche i timestamp, le notifiche e la copia esterna.

La modifica dell’obiettivo mostra innanzitutto la differenza, e le modifiche manuali possono essere mantenute. Un campo che differisce dall’obiettivo viene contrassegnato **come «Modificato da te»** e può essere ripristinato. La revisione delle impostazioni impedisce che una differenza revisionata venga applicata su una modifica effettuata in un’altra scheda.

## Collegamento

**Automatic** prova prima i server pubblici MTProxy, poi WARP, quindi una connessione diretta, quest'ultima solo quando l'indirizzo del server può essere mostrato. Automatic e WARP possono installare componenti con verifica dell'hash e registrare il server su Cloudflare. WARP utilizza il manager wgcf/wireproxy esistente e una porta SOCKS5 locale; la tabella di routing del sistema non viene modificata. Quando sono necessari servizi esterni, Automatic preferisce WARP a MTProxy.

Il tuo proxy accetta `tg://proxy`, `socks5://`, `http://` e `https://`. Il certificato di un proxy HTTPS viene verificato prima che le credenziali gli vengano inviate.

Un controllo della connessione è valido per cinque minuti ed è legato al percorso, alla politica e alle risposte della procedura guidata; la modifica di uno qualsiasi di questi elementi richiede un nuovo controllo. È disponibile l’opzione **“Continua senza controllo”**, che non sostituisce l’accesso a Telegram. Il percorso scelto viene ricontrollato in background e la funzione “Automatico” riesegue la propria catena dopo una perdita di connessione. Quando nessun proxy pubblico risponde, il contatore diventa rosso con le azioni WARP e di ricontrollo .

## Gruppi di account

Gli account di un gruppo condividono le impostazioni. Apri **Account → Gruppi e impostazioni condivise → Impostazioni condivise**, oppure **Impostazioni del gruppo** nella pagina Impostazioni di un account.

Il gruppo condivide l’obiettivo, i file salvati, i timestamp, il drand, le notifiche di problemi, la copia fuori sede, le richieste al di fuori di Telegram, la modalità IP, cosa registrare, la frequenza dei ricontrolli, le regole di notifica, le impostazioni dei report, i parametri e il percorso di connessione. Le destinazioni delle notifiche, le credenziali del proxy e l’accesso rimangono specifici per ogni account, così come l’avvio e la sospensione della raccolta.

- Ogni membro segue il gruppo. In “Impostazioni” si assegna un valore 🔗 **dal gruppo** oppure ✏️ **un valore personalizzato**; selezionando **“Torna al valore del gruppo”** si ripristina il valore predefinito.
- Una modifica elenca gli account interessati (**si applica a 2 account su 3**) e chiede conferma per ogni singolo account prima di sostituire un valore. Gli account non selezionati mantengono il proprio valore.
- Un parametro che il gruppo non condivide rimane su **«Non condiviso»: ogni account mantiene il proprio valore** finché non si preme **«Condividi questo valore**».
- **La copia delle impostazioni da un account** imposta i valori dell’account selezionato come quelli del gruppo.
- A un account spostato in un gruppo viene chiesto: **«Adottare i valori del gruppo?».** In caso contrario, mantiene i propri valori, contrassegnati con ✏️. Gli account aggiunti in seguito partono con i valori del gruppo.
- Un account di osservazione mantiene la modalità IP attiva finché non viene messo in pausa.

Ogni modifica viene registrata nel registro firmato dell’area di lavoro principale e di ogni membro a cui viene trasmessa. L’eliminazione di un gruppo mantiene i relativi account e i loro valori attuali.

La pagina del gruppo `/groups/<id>` mostra i membri, ciò che richiede attenzione e le chat visibili da diversi account. Vedi [gruppi di account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#bulk-import-and-account-groups).

## Spazi di lavoro esistenti

Un'area di lavoro con una sessione attiva o una configurazione completata in precedenza non visualizza la procedura guidata. I suoi valori non vengono sostituiti da un obiettivo al caricamento della pagina. Nascondere un campo non disattiva la funzionalità né ne elimina il valore.

La stima delle dimensioni e del tempo si basa sulla lettura di un massimo di tre chat selezionate e di un massimo di 20 messaggi da ciascuna. Si tratta di una stima: non tiene conto dei limiti di Telegram, della velocità di un determinato server né dei file presenti in ogni chat.

```
python tools/test_settings_hub.py
python tools/test_group_settings.py
python tools/check_group_settings_browser.py
python tools/check_first_run.py
```
