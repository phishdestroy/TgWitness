# Scegliere un proxy

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/proxies/

Mantenere l’account connesso. Stabilire esplicitamente quando il suo percorso possa utilizzare l’indirizzo del server.

## Selezionare innanzitutto la modalità IP

01**Nascondi l’IP**

Utilizzi un proxy. Qualora nessuno funzionasse, attenda senza una connessione diretta a Telegram.

02**Consentire l’alternativa**

Consentire l’accesso diretto trascorso il ritardo configurato; tornare a un proxy funzionante quando uno di essi risponde.

03**Tunnel / VPN**

Consentire percorsi diretti attraverso la rete dell’host. Questa opzione non installa né verifica una VPN.

Il percorso determina il tipo di connessione. La modalità IP stabilisce se è consentita una connessione diretta.

## Lasciate che il pool gestisca il percorso

1. Aprire **l’account → Impostazioni → Impostazioni di connessione**.
2. Selezionare la modalità IP e **MTProxy automatico**, oppure inserire un percorso fisso.
3. Salvi ed esegua **il test di connessione a Telegram**. Funziona anche prima dell’accesso.
4. Dopo aver avviato la raccolta, si verifichi che un messaggio di controllo venga inserito nel registro.

I nuovi spazi di lavoro utilizzano MTProxy automatico con la funzione «Hide IP». Il pool combina quattro fonti pubbliche, verifica le voci, mantiene i percorsi funzionanti e sostituisce i proxy non funzionanti. I download non riusciti conservano le istantanee precedenti.

## Utilizzi il proprio proxy

Inserisca i dettagli SOCKS5 o HTTP CONNECT, incolli un link proxy Telegram supportato oppure fornisca un catalogo di operatori. Metta in pausa il monitoraggio prima di modificare un percorso attivo. I segreti TLS MTProxy falsi che iniziano con `ee` non sono ancora supportati.

**Impostazioni di rotazione, condivisione e riprova**

In **Parametri → MTProxy automatico**, impostare le soglie di errore, i tempi di attesa, la rotazione pianificata e il numero di account per proxy. Un limite di condivisione pari a uno comporta l’attesa da parte di un account qualora non sia disponibile alcun accesso esclusivo. Gli intervalli di aggiornamento dell’elenco e di sondaggio seguono i valori dell’area di lavoro principale. I proxy separati non garantiscono indirizzi IP di uscita distinti.

## Separare Telegram dalle richieste esterne

MTProxy gestisce esclusivamente il traffico di Telegram. I timestamp, le notifiche, le copie e le verifiche delle fonti utilizzano un proxy SOCKS5/HTTP separato, il percorso SOCKS5/HTTP dell’account oppure la modalità Direct, laddove la modalità IP lo consenta. Tali richieste esterne possono essere disattivate.

Un codice `TGWITNESS_PROXY_FEED_PROXY` esplicito configura il percorso del downloader del feed. Il [witness indipendente](https://phishdestroy.github.io/TgWitness/it/docs/witness/) mantiene le proprie impostazioni. Questi controlli non installano una VPN di sistema né reindirizzano il traffico del browser.

Visualizzi [tutte le modalità, le impostazioni predefinite e gli elenchi delle fonti](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes), oppure [scelga chi può modificare il percorso di un account](https://phishdestroy.github.io/TgWitness/it/docs/access/).
