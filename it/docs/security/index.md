# Garantite la sicurezza

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/security/

Scoprite i percorsi di Telegram, gli elenchi di proxy pubblici e i servizi esterni opzionali. Scoprite cosa sblocca ciascuna opzione segreta, cosa coprono le protezioni e cosa spetta a voi gestire.

**127.0.0.1**Indirizzo del pannello predefinito

**256 bit**token casuale del pannello

**0**CDN, strumenti di analisi o font remoti

**Ed25519**firma su ogni registrazione

## Dove si trova tutto

Il programma di raccolta, la relativa interfaccia e ogni registrazione salvata rimangono sul computer o sul server su cui lo si esegue. Telegram è l’unica destinazione predefinita; ogni altra destinazione è selezionabile tramite un’opzione separata.

06 / CIÒ CHE ESCE DALLA MACCHINALa vostra installazione

IL VOSTRO COMPUTER O SERVER

**Pannello**127.0.0.1:8787 · token bearer

**Collector**un client Telegram per ogni area di lavoro

DIRECTORY DEI DATI

**Registro**SQLite · concatenazione di hash · firmato

**Media**file denominati in base all’SHA-256

**Vault**Fernet · sessione, coppia API, chiave di firma, proxy

- **Telegram**Sempre · seguendo il percorso da Lei scelto

  Connessione MTProto dell’account: diretta, SOCKS5, HTTP o MTProxy. La modalità «Nascondi IP» attende un proxy funzionante. Il fallback diretto richiede una modalità che lo consenta esplicitamente.
- **Testo esterno al sito**Opzionale · disattivato per impostazione predefinita

  Il registro, i file e i checkpoint vengono crittografati con AES-GCM prima del caricamento su un archivio compatibile con S3. La chiave rimane in vostro possesso; gli allegati vengono identificati tramite hash con chiave, non tramite l’hash del loro contenuto.
- **Notifiche**Opzionale · disattivato per impostazione predefinita

  Problemi e conteggio delle modifiche con i titoli delle chat. Gli estratti dei messaggi vengono inviati solo se si attiva questa opzione.
- **Autorità di marcatura temporale**Opzionale · disattivato per impostazione predefinita

  Solo l’SHA-256 di un checkpoint firmato e un nonce casuale. Nessun messaggio, nessun nome utente.
- **Witness**Opzionale · disattivato per impostazione predefinita

  Estrae i checkpoint firmati e i contatori di acquisizione tramite un token di sola lettura. Non è in grado di leggere le conversazioni né di modificare le impostazioni.

Impostazione predefinita: solo la connessione a Telegram esce da questo dispositivo.

Le destinazioni opzionali vengono configurate per ogni area di lavoro. Il testo dei messaggi e i file multimediali vengono archiviati in chiaro nella directory dei dati: si raccomanda di proteggerla tramite crittografia del disco e permessi sui file.

## Cosa svela ogni segreto

| Segreto | Dove viene conservato | Cosa offre | In caso di fuga di notizie |
| --- | --- | --- | --- |
| **Token del pannello** | `panel-token.txt` nella directory dei dati; il browser lo conserva solo per quella scheda | Tutte le funzionalità in ogni area di lavoro: lettura ed esportazione, modifica dell’ambito, accesso agli account | Interrompa TgWitness, elimini `panel-token.txt`, poi riavvii il programma: verrà creato un nuovo token |
| **Sessione Telegram** | Archivio crittografato (`credentials.enc`) | L’account Telegram stesso | Chiuda la sessione su Telegram da *Impostazioni → Dispositivi* |
| **Chiave di firma** | Archivio crittografato (`signing.enc`) | Registrazioni firmate verificabili tramite la Sua impronta digitale | I checkpoint conservati altrove, un testimone e i timestamp mostrano ciò che esisteva in precedenza |
| **Chiave di archiviazione** | `vault.key` accanto ai dati, oppure una chiave master esterna per una nuova directory di dati | Decifrare il caveau | Si considerino come trapelate anche la chiave di sessione e quella di firma |
| **Token Witness** | Sull’host di Witness | Sola lettura: checkpoint firmati e stato di integrità | Si prega di eliminarlo dalla pagina Witness e di crearne uno nuovo |
| **Testo chiave per contenuti esterni** | Vault: scaricatelo una sola volta per il ripristino | Decifrare la copia fuori sede | Chiunque sia in possesso degli oggetti archiviati può decriptarli: consideri tale copia come esposta |

## Cosa coprono le misure di protezione

### Trattato

- Un record modificato, rimosso o riorganizzato in un’esportazione: la catena di hash o una firma non risultano più valide.
- Un registro ridotto o ricostruito dopo che un punto di controllo è stato conservato altrove: il punto di controllo conservato non corrisponde più.
- Indovinare il token del pannello: 256 bit casuali, confrontati in tempo costante; dopo 15 tentativi falliti al minuto, l’indirizzo viene rifiutato.
- Contenuti ostili delle chat: il testo viene inserito come testo, mai come HTML; gli allegati vengono scaricati come file; il pannello non carica nulla da altri siti.
- Una directory di dati copiati con una chiave di archiviazione esterna: le sessioni e le chiavi di firma rimangono crittografate senza la chiave principale.

### A voi la scelta

- Il titolare del token del pannello principale detiene il pieno controllo. Conceda ad altre persone un accesso limitato agli account, alle chat e alle azioni di cui hanno bisogno; mantenga riservata la chiave principale.
- Un amministratore del sistema può leggere tutto, nonché riscrivere e rifirmare il registro. Si raccomanda di conservare l’impronta digitale e i punti di controllo su un altro sistema.
- Il testo dei messaggi e i file multimediali non vengono crittografati da TgWitness. Si raccomanda di utilizzare la crittografia del disco e di impostare autorizzazioni rigorose.
- L’uso del protocollo HTTP standard al di fuori di localhost espone il token sulla rete. Si raccomanda di utilizzare HTTPS o un tunnel SSH.
- Le firme dimostrano che quanto registrato non è stato modificato, non che ogni evento su Telegram sia stato registrato.

[Condivida l’accesso a un caso](https://phishdestroy.github.io/TgWitness/it/docs/access/) con autorizzazioni, scadenza e limiti di sessione. Il token di Testimone rimane una credenziale separata.

## Rafforzare la sicurezza di un’installazione

0 su 8 completato

1. **Utilizzi un account Telegram dedicato** — mai quello principale. Il token del pannello e la sessione le garantiscono il pieno controllo dello stesso.
2. **Mantenete il pannello all’indirizzo 127.0.0.1.** Accedetevi da remoto esclusivamente tramite HTTPS (la configurazione Caddy inclusa) o un tunnel SSH.
3. **Crittografare il disco** che contiene la directory dei dati: il testo dei messaggi e i file multimediali vengono archiviati così come sono stati ricevuti.
4. **Limitare la directory dei dati** all’account di servizio. Le nuove directory assumono la modalità 0700 su Unix; su Windows, impostare i permessi della cartella.
5. **Conservare la chiave principale dell’archivio** su un **altro** server: impostare `TGWITNESS_VAULT_KEY_FILE` prima di creare la directory dei dati.
6. **Salvi l’impronta digitale della chiave di firma e i checkpoint** su un altro sistema e aggiunga un testimone su un altro host.
7. **Non carichi mai** le chiavi `data/`, di sessione, `panel-token.txt` o del vault su GitHub o in una chat.
8. **Non registrare** le intestazioni `Authorization` né i corpi delle richieste su un proxy inverso.

**È possibile modificare il token del pannello senza perdere i dati?**

Sì. Il token serve solo ad aprire il pannello. Arresti TgWitness, elimini `panel-token.txt` dalla directory dei dati e lo riavvii; il registro, le sessioni e le chiavi rimangono inalterati. Se `TGWITNESS_TOKEN` è impostato, viene utilizzato il valore dell’ambiente anziché il file.

**Perché i messaggi non sono crittografati quando sono inattivi?**

Il responsabile della raccolta deve leggerli per effettuare ricerche, confrontare le versioni ed esportarli. Crittografarli con una chiave sulla stessa macchina sarebbe di scarsa utilità contro chi è in grado di accedere a tale macchina. La crittografia del disco protegge un disco fuori uso o rubato; permessi rigorosi proteggono invece un disco in funzione.

## Segnalare una vulnerabilità

Utilizzi **la sezione Sicurezza → Segnala una vulnerabilità** nel repository GitHub. Indichi la versione, l’impatto e una riproduzione sintetica minima. Non invii mai credenziali, directory degli account o archivi di prove reali. Qualora la segnalazione privata non fosse disponibile, apra un ticket richiedendo un canale privato senza fornire dettagli sull’exploit.
