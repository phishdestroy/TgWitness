# Scoprite cosa è andato storto

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/troubleshooting/

Si parta dal sintomo. Si verifichi un livello alla volta.

## Il pannello richiede un token

Utilizzi il token del pannello presente nel file locale visualizzato dal programma di avvio. Per Docker, esegua il comando `docker compose exec tgwitness cat /data/panel-token.txt`. Un codice di accesso a Telegram, un token BotFather e un token witness in sola lettura hanno finalità diverse.

## Telegram non si connette

Apra le impostazioni di connessione ed esegua il controllo della connessione. Se utilizza un proxy pubblico, provi un’altra voce e salvi esplicitamente il percorso. Verifichi il tipo di proxy e il formato del segreto supportato. L’aggiornamento di un elenco pubblico non modifica il percorso dell’account.

## Connesso, ma nessun nuovo messaggio

1. Verifichi che l’osservazione sia in esecuzione nell’area di lavoro corretta.
2. Si prega di verificare che la fonte sia selezionata e visibile a tale account.
3. Inviate un nuovo messaggio univoco in un gruppo controllato e cercate proprio quel testo.
4. Si prega di esaminare il registro operativo per individuare eventuali interruzioni, ritardi nell’elaborazione o errori di Telegram.

Le istantanee storiche e gli eventi relativi ai nuovi messaggi sono distinti. È possibile collegare una fonte inattiva senza generare nuovi messaggi. Si raccomanda di utilizzare un test di consegna controllata quando è fondamentale garantire la completezza dei dati.

## FloodWait o un intervallo dopo un riavvio

FloodWait indica che Telegram richiede una pausa. Attenda il periodo indicato e verifichi il carico di lavoro della raccolta; i tentativi ripetuti di riconnettersi non eliminano il limite. Lo stato degli aggiornamenti salvati consente di recuperare il ritardo dopo un riavvio, ma gli aggiornamenti scaduti e alcune finestre di interruzione rimangono dei limiti. Registri l’intervallo piuttosto che considerare il registro come completo.

## Il bot è configurato ma non pubblica nulla

Si assicuri che il processo di Witness sia effettivamente in esecuzione, che il bot possa pubblicare nel canale e che Witness possa raggiungere il collector e l’API del bot. Verifichi il registro per individuare eventuali pubblicazioni non andate a buon fine. Il solo esito positivo di un’interrogazione del collector non conferma la pubblicazione nel canale.

## Dove si trova l’integrazione del token GitHub?

**In fase di pianificazione.** La sezione «Extras» descrive il flusso di lavoro proposto per il fork e la verifica della compilazione. Attualmente non è disponibile alcun modulo per il token GitHub né alcuna attestazione automatica che confermi la corrispondenza tra un’installazione in esecuzione e un repository. Si prega di consultare lo [stato attuale delle funzionalità](https://phishdestroy.github.io/TgWitness/it/docs/reference/features/).

Quando si segnala un problema, si prega di indicare la versione, il sistema operativo, i passaggi seguiti e un messaggio di errore oscurato. Si prega di non menzionare sessioni, token, messaggi privati e la directory dei dati nelle segnalazioni pubbliche.
