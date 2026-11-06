# Chat segrete: implementazione e demo

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/secret-chats/

Comprendere l’implementazione separata delle chat segrete, provare l’interfaccia fittizia ed esaminare i difetti ancora da risolvere.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Stato verificato il 6 novembre 2026:** esiste un’implementazione separata delle Chat segrete in fase di sviluppo. Non è stata integrata nel ramo `main` pubblicato al commit `3d23e52b647b`. Il collettore standard e l’esportazione Takeout non raccolgono le Chat segrete. Lo scenario interattivo del sito web illustra l’interfaccia con dati fittizi; non consente la comunicazione tramite Telegram.

## Dove si trova l’implementazione

Il commit `0e60f88e` ha aggiunto **Sources → Pseudo-secret** nel ramo di sviluppo locale `fix/panel-routes-sessions`. Lo snapshot verificato è `bb8788fb685c`. La sua implementazione include `tgwitness/secret_chats.py`, percorsi dell'applicazione, `tgwitness/static/views/secret-chats.js` e test dedicati.

L'extra opzionale `secret-chats` in quel ramo utilizza [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), fissato a `d87bf037b90060383c7b704d8a06ebb98c621c6f`. La libreria implementa il protocollo di chat end-to-end di Telegram sull'autorizzazione Telethon esistente dell'account. L'installazione di quella libreria da sola non aggiunge l'integrazione mancante a `main`.

## Cosa fa l’interfaccia di sviluppo

| Azione | Comportamento registrato |
| --- | --- |
| Avvia una chat tramite nome utente o ID utente | Inviare una richiesta; l’altro partecipante deve accettarla. |
| Accettare una richiesta in arrivo | TgWitness diventa l'endpoint di ricezione per quella chat. L'accettazione automatica è un'impostazione separata, disattivata per impostazione predefinita. |
| Inviare o ricevere un messaggio | Aggiungere un record `secret_chat.message` in uscita o in entrata e visualizzarlo nella conversazione. |
| Ricevi un allegato | Decrittografarli, memorizzarne i byte in base a SHA-256 e registrare `secret_chat.file`. |
| Ricevi un avviso di scadenza o di cancellazione | Registrare l’avviso e conservare i contenuti acquisiti in precedenza. |
| Rivedere la conversazione | Mostrare messaggi, file, avvisi e la visualizzazione delle chiavi. La scheda aperta si aggiorna ogni quattro secondi. |

In una build di sviluppo contenente l’integrazione, l’operatore abilita il modulo per l’account selezionato e lo collega. L’avvio, l’accettazione e l’invio richiedono l’autorizzazione all’interazione e che la protezione in sola lettura dell’account sia disattivata. L’altro partecipante deve accettare una nuova chat in uscita. Questi controlli non sono presenti nell’ applicazione pubblicata nella revisione precedente.

Sono coperte solo le chat create o accettate da questa sessione TgWitness. Le chat segrete esistenti su un telefono rimangono su quel dispositivo. L’importazione di una sessione non fornisce le relative chiavi di crittografia separate. Il materiale delle chiavi delle chat segrete e i contatori sono archiviati nel vault dell’area di lavoro; i messaggi conservati e i file decrittografati seguono le normali misure di protezione dell’area di lavoro.

## Dimostrazione sul sito web

Lo scenario **Try Secret Chat** del sito web avvia una conversazione fittizia. Consente al lettore di avviare una richiesta, simularne l’accettazione, inviare un messaggio di esempio, ricevere una risposta e un file predefiniti, nonché esaminare un timer e un avviso di cancellazione. È inoltre possibile accettare una richiesta in arrivo. I controlli indicano esplicitamente le azioni simulate dei peer.

Questo scenario viene eseguito nella memoria del browser. Il reset o il ricaricamento lo cancellano. Non effettua l'accesso, non contatta Telegram, non crea chiavi di crittografia reali né altera i download dei campioni firmati. I messaggi visualizzati non costituiscono prove firmate. Lo scenario illustra l'interazione prevista; non certifica che l'implementazione dello sviluppo sia pronta.

## Controlli e difetti ancora da risolvere

I cinque test esistenti riguardano la persistenza delle chiavi crittografate, il ciclo di vita e i record dei messaggi, la politica di accettazione in entrata, l’invio in sola lettura e l’esportazione degli allegati. Hanno superato i test sulla libreria fissata durante la revisione del 6 novembre. Tre ulteriori controlli sintetici hanno riprodotto difetti nello stesso snapshot:

| Risultati | Conseguenza |
| --- | --- |
| La chiusura aggira l'`read_only` | Il percorso di chiusura può eseguire un'azione remota quando le interazioni devono essere bloccate. |
| La ricerca dei duplicati riguarda solo i record recenti di 500 | Una riproduzione precedente può creare un duplicato dopo il riavvio. |
| Il download fallito di un allegato comporta la rimozione della relativa voce in sospeso | Un errore transitorio comporta la perdita del processo di riprova. |

Si tratta di difetti noti, registrati anche nell’audit [pubblicato](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md). I cinque test superati non coprono questi errori. La revisione ha utilizzato spazi di lavoro sintetici e operazioni Telegram simulate; non ha ripetuto un handshake dal vivo né ha verificato l’implementazione in produzione.
