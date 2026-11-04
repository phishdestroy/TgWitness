# Scegliere un proxy

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/proxies/

Tenga l’account online e decida Lei se potrà mai mostrare l’IP del Suo server.

## Selezionare innanzitutto la modalità IP

01**Nascondi l’indirizzo**

Solo proxy. Se nessuno funziona, aspetta.

02**Direct come ultima risorsa**

Passa al diretto dopo un ritardo e torna a un proxy appena uno funziona.

03**Server protetto da un tunnel o da una VPN**

Il diretto va bene. Non configura né verifica la VPN al posto Suo.

Il percorso determina il tipo di connessione. La modalità IP stabilisce se è consentita una connessione diretta.

## Lasciate che il pool gestisca il percorso

1. **Account → Impostazioni → Impostazioni di connessione**.
2. Scelga la modalità IP e **MTProxy automatico**, oppure un percorso fisso.
3. Salvi, poi **Testa connessione a Telegram** (funziona anche prima dell’accesso).
4. Avvii la raccolta e si invii un messaggio di prova.

I nuovi spazi partono con MTProxy automatico e **Nascondi l’indirizzo**. Il pool usa quattro elenchi pubblici, prova i server, tiene quelli buoni e sostituisce quelli caduti.

## Utilizzi il proprio proxy

SOCKS5, HTTP CONNECT, un link proxy di Telegram o un catalogo dell’operatore. Metta in pausa l’osservazione prima di cambiare. I segreti Fake TLS (`ee`…) non funzionano.

**Impostazioni di rotazione, condivisione e riprova**

**Parametri → MTProxy automatico**: soglie di errore, attese, rotazione, account per proxy. Limite 1 significa che un account aspetta invece di condividere. Proxy diversi possono comunque avere lo stesso IP di uscita.

## Separare Telegram dalle richieste esterne

MTProxy trasporta solo Telegram. Marche temporali, notifiche, copie e verifiche del codice passano da un proxy SOCKS5/HTTP separato, dal percorso SOCKS5/HTTP dell’account o in diretto se la modalità lo consente. Oppure le disattivi.

`TGWITNESS_PROXY_FEED_PROXY` imposta il percorso per scaricare gli elenchi. Il [testimone](https://phishdestroy.github.io/TgWitness/it/docs/witness/) ha impostazioni proprie. Niente di tutto questo tocca il Suo browser o la rete di sistema.

Altro: [modalità e valori predefiniti](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes), [chi può cambiare i percorsi](https://phishdestroy.github.io/TgWitness/it/docs/access/).
