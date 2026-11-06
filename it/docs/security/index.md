# Telegram · Garantite la sicurezza

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/security/

Cosa lascia la Sua macchina, cosa apre ogni segreto e cosa coprono le protezioni rispetto a ciò che spetta a Lei.

**127.0.0.1**Indirizzo del pannello predefinito

**256 bit**token casuale del pannello

**0**CDN, strumenti di analisi o font remoti

**Ed25519**firma su ogni registrazione

## Dove si trova tutto

Il collector, il pannello e ogni voce restano sulla Sua macchina. Di default si contatta solo Telegram; tutto il resto è un interruttore a parte.

06 / CIÒ CHE ESCE DALLA MACCHINALa vostra installazione

IL VOSTRO COMPUTER O SERVER

**Pannello**127.0.0.1:8787 · token bearer

**Collector**un client Telegram per ogni area di lavoro

DIRECTORY DEI DATI

**Registro**SQLite · concatenazione di hash · firmato

**Multimedia**file denominati in base all’SHA-256

**Vault**Fernet · sessione, coppia API, chiave di firma, proxy

- **Telegram**Sempre · seguendo il percorso da Lei scelto

  Connessione MTProto dell’account: diretta, SOCKS5, HTTP o MTProxy. La modalità «Nascondi IP» attende un proxy funzionante. Il fallback diretto richiede una modalità che lo consenta esplicitamente.
- **Testo esterno al sito**Opzionale · disattivato per impostazione predefinita

  Il registro, i file e i checkpoint vengono crittografati con AES-GCM prima del caricamento su un archivio compatibile con S3. La chiave rimane in vostro possesso; gli allegati vengono identificati tramite hash con chiave, non tramite l’hash del loro contenuto.
- **Notifiche**Opzionale · disattivato per impostazione predefinita

  Problemi e conteggio delle modifiche con i titoli delle chat. Gli estratti dei messaggi vengono inviati solo se si attiva questa opzione.
- **Autorità di marcatura temporale**Opzionale · disattivato per impostazione predefinita

  Solo l’SHA-256 di un checkpoint firmato e un nonce casuale. Nessun messaggio, nessun nome utente.
- **Testimone**Opzionale · disattivato per impostazione predefinita

  Estrae i checkpoint firmati e i contatori di acquisizione tramite un token di sola lettura. Non è in grado di leggere le conversazioni né di modificare le impostazioni.

Impostazione predefinita: solo la connessione a Telegram esce da questo dispositivo.

Le destinazioni opzionali vengono configurate per ogni area di lavoro. Il testo dei messaggi e i file multimediali vengono archiviati in chiaro nella directory dei dati: si raccomanda di proteggerla tramite crittografia del disco e permessi sui file.

## Cosa svela ogni segreto

| Segreto | Dove viene conservato | Cosa offre | In caso di fuga di notizie |
| --- | --- | --- | --- |
| **Token del pannello** | `panel-token.txt` nella cartella dati; il browser lo tiene per scheda | Tutto, in ogni spazio | Fermi TgWitness, elimini `panel-token.txt`, riavvii: ne riceve uno nuovo |
| **Sessione Telegram** | Archivio crittografato (`credentials.enc`) | L’account Telegram stesso | Chiuda la sessione su Telegram da *Impostazioni → Dispositivi* |
| **Chiave di firma** | Archivio crittografato (`signing.enc`) | Firmare voci con la Sua impronta | Punti di controllo conservati altrove, un testimone e le marche temporali mostrano comunque cosa esisteva prima |
| **Chiave di archiviazione** | `vault.key` accanto ai dati o una chiave master esterna | Il vault | Consideri trapelate anche la sessione e la chiave di firma |
| **Token Witness** | Sull’host di Witness | Sola lettura: punti di controllo e stato | Lo elimini nella pagina del testimone e ne crei uno nuovo |
| **Testo chiave per contenuti esterni** | Vault: scaricatelo una sola volta per il ripristino | La copia esterna | Chi ha anche il bucket può decifrarla: consideri la copia esposta |

## Cosa coprono le misure di protezione

### Trattato

- Una voce modificata, rimossa o riordinata: si rompe la catena di hash o una firma.
- Un diario accorciato o ricostruito dopo che ha conservato altrove un punto di controllo: il punto di controllo non corrisponde più.
- Indovinare il token: 256 bit casuali, confronto a tempo costante; 15 errori al minuto e l’indirizzo viene bloccato.
- Contenuti ostili nelle chat: il testo resta testo, mai HTML; gli allegati si scaricano come file; il pannello non carica nulla da altri siti.
- Una cartella dati rubata con chiave del vault esterna: sessioni e chiavi restano cifrate.

### A voi la scelta

- Il token principale può fare tutto. Dia agli altri un accesso limitato e tenga per sé quello principale.
- Chi è amministratore della macchina può leggere tutto e rifirmare il diario. Conservi impronta e punti di controllo altrove.
- TgWitness non cifra messaggi e media. Cifri il disco e restringa i permessi.
- L’HTTP semplice fuori da localhost espone il token. Usi HTTPS o un tunnel SSH.
- Le firme non Le dicono cosa è stato perso. Controlli la copertura e provi la consegna sui Suoi account e sulle Sue fonti.

[Condivida l’accesso a un caso](https://phishdestroy.github.io/TgWitness/it/docs/access/) con permessi, scadenza e limiti di sessione.

## Rafforzare la sicurezza di un’installazione

0 su 8 completato

1. **Usi un account Telegram dedicato**, mai quello principale.
2. **Tenga il pannello su 127.0.0.1.** Accesso remoto solo via HTTPS (Caddy incluso) o tunnel SSH.
3. **Cifri il disco** con la cartella dati: messaggi e media sono salvati così come arrivano.
4. **Limiti la cartella dati** all’account di servizio (0700 su Unix, permessi della cartella su Windows).
5. **Tenga la chiave del vault altrove** sui server: imposti `TGWITNESS_VAULT_KEY_FILE` prima del primo avvio.
6. **Salvi impronta e punti di controllo** su un altro sistema ed esegua un testimone su un altro host.
7. **Non carichi mai** le chiavi `data/`, di sessione, `panel-token.txt` o del vault su GitHub o in una chat.
8. **Non registrare** le intestazioni `Authorization` né i corpi delle richieste su un proxy inverso.

**È possibile modificare il token del pannello senza perdere i dati?**

Sì, apre solo il pannello. Fermi TgWitness, elimini `panel-token.txt`, riavvii. Diario, sessioni e chiavi restano. Se `TGWITNESS_TOKEN` è impostato, quel valore ha la precedenza sul file.

**Perché i messaggi non sono crittografati quando sono inattivi?**

Il collector deve leggerli per cercare, confrontare ed esportare. Una chiave sulla stessa macchina non fermerebbe chi può già leggere quella macchina. La cifratura del disco copre un disco rubato, i permessi uno in funzione.

## Segnalare una vulnerabilità

**Security → Report a vulnerability** su GitHub. Versione, impatto e una riproduzione minima con dati fittizi. Non invii mai credenziali, cartelle di account o prove reali. Se la segnalazione privata è disattivata, apra una issue chiedendo un canale privato, senza dettagli dell’exploit.
