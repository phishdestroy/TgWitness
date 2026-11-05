# Implementazione ad alta sicurezza

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/

Un server protetto attivo 24 ore su 24, 7 giorni su 7 su Hetzner o Phala Cloud, un DNS Gateway e controlli ripetibili da parte di terzi.

Un registro firmato dimostra che i dati non sono stati modificati **dopo** la firma. Per i casi più gravi, la domanda successiva è se qualcuno abbia potuto alterare i dati **prima** della firma: chi ha eseguito il collector, su quale macchina e se qualcuno vi abbia effettuato l’accesso. Questa modalità opzionale distribuisce il collector in modo che una terza parte possa verificarlo, utilizzando i dati conservati dal fornitore di servizi cloud e da Cloudflare anziché basarsi sulla parola dell’operatore.

L'utilizzo standard in locale e con Docker rimane invariato. Nulla qui funziona a meno che non si esegua la distribuzione con `python -m tgwitness.cloud`, e il collector legge il proprio host solo quando la distribuzione imposta `TGWITNESS_ASSURANCE`.

Diagramma di flusso · Operatore → Server, firewall senza regole in entrata (API del provider); Operatore → Tunnel e DNS (API di Cloudflare); Server, firewall senza regole in entrata → Tunnel e DNS (solo in uscita); Server, firewall senza regole in entrata → Chiave di firma generata sul server; Verifier, token di sola lettura → Log del provider e firewall; Verifier, token di sola lettura → Indirizzo del connettore Tunnel e ingresso; Verifier, token di sola lettura → Dichiarazione /api/assurance firmata; Verifier, token di sola lettura → File ZIP contenente le prove · Operatore · Verifier, token di solalettura · Server, firewall senzaregole in entrata · Log del provider efirewall · Indirizzo del connettoreTunnel e ingresso · Dichiarazione/api/assurance firmata · File ZIP contenente leprove · Tunnel e DNS · Chiave di firma generatasul server · API del provider · API di Cloudflare · solo in uscita

**Diagramma sotto forma di testo**

1. Operatore → Server, firewall senza regole in entrata (API del provider)
2. Operatore → Tunnel e DNS (API di Cloudflare)
3. Server, firewall senza regole in entrata → Tunnel e DNS (solo in uscita)
4. Server, firewall senza regole in entrata → Chiave di firma generata sul server
5. Verifier, token di sola lettura → Log del provider e firewall
6. Verifier, token di sola lettura → Indirizzo del connettore Tunnel e ingresso
7. Verifier, token di sola lettura → Dichiarazione /api/assurance firmata
8. Verifier, token di sola lettura → File ZIP contenente le prove

## Cosa può verificare un verificatore

| Affermazione | Come viene verificato | A cura di |
| --- | --- | --- |
| Il server è stato creato tramite l’API del provider in un momento ben preciso | Oggetto Server e la sua creazione nel log del provider stesso | Fornitore |
| Nessuno ha utilizzato i percorsi di accesso del provider | Registro delle richieste della console, operazioni di ripristino, reimpostazione della password, ricostruzione, ISO, immagini, backup | Fornitore |
| Non è possibile connettersi ad esso | Il firewall del provider non ha regole di ingresso; l’accesso SSH viene nascosto sin dal primo avvio | Provider (firewall), host (SSH) |
| È possibile accedere al pannello solo tramite il tunnel | L'ingresso del tunnel inoltra esclusivamente al pannello; il connettore parte dall'indirizzo del server | Cloudflare |
| Questo stesso software funziona | L’hash firmato dell’albero dei sorgenti del collector corrisponde a un checkout del commit distribuito | Collector, sincronizzato con Git |
| La chiave di firma è stata creata su quel server | La chiave firma una dichiarazione in cui vengono indicati l’ID del server del provider e l’hash del file cloud-init ricevuto | Collector, verificato dal provider |
| Il diario appartiene a quella chiave e a quel server | Ogni avvio di processo nella prova ZIP riporta la misurazione dell’host per quel server | Prove ZIP |

Le misurazioni dell’host (listener e processi SSH, sessioni attuali, accessi `wtmp`, l’avvio) vengono segnalate dal collettore stesso e vengono firmate ad ogni avvio del processo e nei `host.state` registrazioni ogni volta che subiscono modifiche. Un utente root sul server potrebbe falsificarle; esse supportano i registri del provider e di Cloudflare anziché sostituirli.

## Fornitori

| `--provider` | Credenziali | Accesso in sola lettura per il Verificatore | Log del provider per il verificatore | Conservato per |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Leggi il token dello stesso progetto | Azioni relative al server e al firewall | Finché le risorse sono disponibili |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Token di accesso personale in sola lettura | Azioni di Droplet | Finché il Droplet esiste |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` ambiti di sola lettura | Eventi relativi agli account, versioni delle regole del firewall | 90 giorni |
| `vultr` | `VULTR_API_KEY` | Utente con accesso in lettura e il `activity_logs` autorizzazione | Registro delle attività dell’account (metodo, percorso, autore) | 30 giorni, o più a lungo con un abbonamento al registro di audit |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Cronologia degli eventi di CloudTrail | 90 giorni |
| `phala` | `PHALA_CLOUD_API_KEY` | Una chiave API dello stesso spazio di lavoro | Revisioni dell’applicazione e operazioni CVM: modifiche alla configurazione e all’ambiente di Docker Compose, riavvii, aggiornamenti del sistema operativo | Sebbene l’applicazione esista |
| `generic` | nessuno | nessuno | nessuno: **autocertificato** | – |

Utilizzare un progetto, un team, un account o un sottoaccount dedicato per ogni caso: l’accesso in sola lettura del verificatore mostrerà quindi solo questa distribuzione. Le credenziali vengono lette dal `--provider-token-file` dalla variabile sopra indicata, mai dalla riga di comando. Per AWS il file contiene `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; la regione è `--location`.

Ciò che i registri di ciascun provider non possono mostrare è riportato in ogni rapporto. In breve: Hetzner registra le richieste alla console; la Recovery Console di DigitalOcean, Lish/Glish di Linode e la console web di Vultr non vengono registrate in quanto tali, quindi l’account root è bloccato al primo avvio e un accesso alla console richiederebbe una reimpostazione della password o una modifica delle impostazioni di avvio, operazioni che vengono registrate. Vultr restituisce l’indirizzo della console a qualsiasi chiave in grado di leggere l’istanza; né la registrazione né il rapporto lo memorizzano.

## VM riservata su Phala Cloud (Intel TDX)

Con `--provider phala` il collector viene eseguito in una macchina virtuale riservata Intel TDX su [Phala Cloud](https://phala.com/), gestita da dstack. L’host e il personale di Phala non possono leggere la sua memoria, e il processore firma un attestato relativo a ciò che la macchina ha avviato. Il verificatore non si limita a fidarsi della parola di Phala: `tgwitness.tdx` verifica personalmente ogni attestato, fino alla Root CA Intel SGX fissata, confrontandolo con gli elenchi di revoca di Intel e i dati della piattaforma firmati da Intel, e rifiuta le macchine che possono essere sottoposte a debug o migrate.

| Inserimento di una segnalazione | Cosa mostra |
| --- | --- |
| `tdx_binding` | L’attestato comprende la dichiarazione firmata del raccoglitore e il valore casuale di questa richiesta |
| `tdx_quote` | Intel garantisce la validità dell’attestazione; questa viene rilasciata solo quando Intel valuta la piattaforma come aggiornata |
| `tdx_compose_hash` | RTMR3, riprodotto dal log degli eventi di dstack, misura i dati di composizione dell’app riportati dal collector |
| `tdx_compose` | Quel codice è, byte per byte, quello generato dal commit distribuito: file sorgente identificati tramite hash, entrambe le immagini tramite digest, nessun altro codice |
| `tdx_identity` | L’attestazione proviene dall’applicazione e dall’istanza distribuite, con chiavi provenienti dal KMS di Phala e da un disco crittografato |
| `tdx_os` | MRTD e RTMR0-2 corrispondono ai valori che il verificatore calcola dall’immagine del sistema operativo dstack pubblicata da Dstack-TEE, individuata tramite l’hash dell’immagine del sistema operativo segnalato dalla CVM, e dalle tabelle ACPI che QEMU genera per la configurazione della VM: firmware, kernel, initrd, riga di comando con l’hash del filesystem root, memoria, vCPU e dispositivi. Un’immagine di sviluppo non supera il controllo |

L’immagine del sistema operativo (circa 180 MB, di cui 21 MB vengono conservati) viene scaricata una sola volta da [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) nella cartella `dstack-images` accanto al record; `--tdx-image FOLDER` utilizza un’altra cartella o un’immagine decompressa, `--tdx-image none` salta il confronto. La misurazione segue `dstack-mr` e il pacchetto Rust `qemu-acpi` da Dstack-TEE/dstack; `tools/check_dstack_image.py` la verifica rispetto all’output ACPI proprio di QEMU e rispetto a un record di attestazione hardware reale di Phala Cloud, mentre `--live` la verifica anche rispetto all’immagine pubblicata. `--tdx-measurements` continua a confrontare MRTD e RTMR0-2 forniti invece in formato JSON.

Ogni avvio del collettore registrato nel registro è accompagnato da tale attestato, pertanto `verify --evidence` verifica ogni avvio e l’immagine del sistema operativo da cui è stato avviato. Le revisioni dell’applicazione di Phala e le operazioni del CVM fungono da registro del provider: una configurazione di Docker Compose modificata dopo la distribuzione comporta il fallimento del rapporto, e i riavvii vengono elencati per la revisione.

Nel pannello, selezionare **«Macchina virtuale riservata · Phala Cloud»** in **«Extra** → **Server 24/7»** e incollare una chiave API di Phala Cloud; il tunnel rapido funziona come su Hetzner. Dalla riga di comando:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` Legge i certificati e gli elenchi di revoca di Intel da un file invece di scaricarli dal sito di Intel. Il DNS gateway non è disponibile in questo caso: Phala non dispone di un firewall del provider per il traffico in uscita.

### Certificato di attestazione

Per una distribuzione Phala, `verify --report certificate.md` scrive anche il certificato: un `certificate.html` autonomo e un `certificate.pdf` in formato A4 contenente il verdetto, la catena di fiducia dalla radice Intel alla chiave del collettore, un confronto tra server standard e ad alta sicurezza, le misurazioni accanto ai valori calcolati dall’immagine pubblicata, chi garantisce per ciascuna parte, la catena di certificati Intel, ogni controllo, il log del provider e le modalità per ripetere la verifica. Il rapporto JSON rimane il documento ufficiale; le pagine ne riportano il contenuto.

Il rapporto è sigillato digitalmente con firme e timbri temporali, nel file `certificate.seal.json` e nei file `.tsq`/`.tsr` ad esso associati:

| Seal | Cosa offre in più |
| --- | --- |
| Timbro temporale elettronico qualificato, `http://tsa.belgium.be/connect` | Timestamp RFC 3161 sui byte esatti di `certificate.json` proveniente dal fornitore di servizi di fiducia qualificato del governo federale belga (FPS Policy and Support, BOSA). Tale entità è elencata come servizio di marcatura temporale qualificato, con stato «concesso», nell’elenco di fiducia dell’UE del Belgio; la radice (Belgium Root CA6) e le voci dell’elenco, secondo l’elenco pubblicato il 20 ottobre 2026, sono fissate in `tgwitness/tsa_roots.py`. Ai sensi dell’articolo 41 del Regolamento (UE) n. 910/2014, tale marcatura temporale è ritenuta accurata per quanto riguarda la data e l’ora, nonché l’integrità dei dati in ogni Stato membro dell’UE |
| Timestamp RFC 3161, FreeTSA | Un secondo timestamp indipendente |
| Firma del verificatore | Ed25519 su un’istruzione che indica lo SHA-256 del rapporto e ogni timestamp, utilizzando la chiave del verificatore stesso (`--sign-with FOLDER`, predefinita `~/.tgwitness/verifier`); il PDF reca una firma generata con la stessa chiave |

`--timestamp URL` (ripetibile) sceglie altre autorità, `--timestamp none` nessuna, `--sign-with
none` lascia il sigillo non firmato. `check-report` verifica l’hash del rapporto, la firma del verificatore, ogni timestamp rispetto a una radice attendibile e il suo stato qualificato, nonché la firma del PDF. Il valore giuridico di un timbro temporale qualificato al di fuori dell’UE, nonché del rapporto nel suo complesso, spetta al tribunale o all’autorità che lo riceve; il sigillo attesta quando il rapporto è stato creato e che non ha subito modifiche.

Un'attestazione non può escludere la presenza di una vulnerabilità nel modulo TDX o nel microcodice di Intel, né l’accesso fisico al bus di memoria. Chiunque controlli l’applicazione nell’account di Phala può distribuire un altro “compose”; questo appare come una nuova revisione con un nuovo hash del “compose”. L’host controlla la fonte dell’ora della macchina e la rete.

L’implementazione, la verifica con `--evidence`, i riavvii, il confronto delle immagini del sistema operativo, il certificato sigillato digitalmente con firme e timbri temporali e la distruzione sono stati eseguiti su Phala Cloud stesso; si veda [, l’esecuzione del 4 novembre 2026,](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

## Prima di iniziare

1. Una zona Cloudflare, il relativo ID account e un token API con le autorizzazioni **Cloudflare Tunnel Edit**, **Zone Read** e **DNS Edit**, fornito con `--cloudflare-token-file` oppure `CLOUDFLARE_API_TOKEN`. Per il verificatore: **Cloudflare Tunnel Read**, **DNS Read** e, per il registro di audit, **Account Settings Read**. Senza un dominio, un [tunnel rapido](https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/#quick-tunnel-without-a-domain) non necessita di nulla di tutto ciò.
2. Credenziali del provider con accesso in scrittura a un progetto dedicato; `lock` utilizza lo stesso:

   - Hetzner: token API con autorizzazioni di lettura e scrittura;
   - DigitalOcean: token di accesso personale con diritti di scrittura;
   - Linode: token di accesso personale con `linodes`, `firewall` e `events` ambiti di lettura/scrittura;
   - Vultr: chiave API di un account dedicato o di un sottoaccount;
   - AWS: credenziali IAM consentite `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` e `ec2:RevokeSecurityGroupIngress`.
3. Il commit da eseguire. Un tag di rilascio viene risolto una sola volta nel suo commit con `git ls-remote`; il server riceve sempre e solo il commit di 40 caratteri.

## Dal pannello

Sul proprio computer, la voce **Extras → Server 24/7** esegue la stessa operazione `deploy` per Hetzner in tre passaggi: scegli Europa o Stati Uniti, incolla un token Hetzner (Lettura e Scrittura), quindi verifica il tipo di server, il prezzo mensile, l’indirizzo e la versione che il pannello ha individuato con quel token. Nulla viene creato prima della tua conferma. Il pannello mostra ogni passaggio come `deploy` viene segnalato, quindi l’ indirizzo, il token del pannello e l’impronta digitale della chiave di firma. Senza un dominio, il server ottiene un [tunnel rapido](https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **“I tuoi server” → “Trova l’indirizzo attuale”** lo ricerca nuovamente dopo un riavvio. Per un indirizzo fisso sotto il proprio dominio, apri **“Opzionale” · “Il tuo dominio”** e aggiungi un token Cloudflare (il link preparato seleziona “Lettura zona”, “Modifica DNS” e “Modifica tunnel Cloudflare”).

I token viaggiano con ogni richiesta dalla scheda del browser all’TgWitness sullo stesso computer e non vengono scritti da nessuna parte; il registro di distribuzione, il file cloud-init redatto, il token del pannello e, per un tunnel rapido, la chiave dell’indirizzo sono conservati `deployments/NAME` all’interno della directory dei dati. Il pannello offre questo servizio solo all’amministratore principale tramite una connessione loopback diretta (`127.0.0.1`, senza intestazioni proxy o tunnel); un pannello raggiungibile tramite rete mostra invece i comandi . La versione predefinita è il tag di rilascio del pannello in esecuzione, risolto tramite l’ API di GitHub. Posizione, tipo di server e prezzo provengono dall’API di Hetzner: `cpx22` laddove è disponibile, altrimenti il tipo x86 più economico con almeno 2 GB di memoria.

## Tunnel rapido senza dominio

`--quick-tunnel` sostituisce `--zone`, `--cloudflare-account` e `--panel-host`; non è coinvolto alcun account o token Cloudflare:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Sul server, cloudflared apre un [tunnel veloce](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) verso il pannello: un indirizzo casuale `https://….trycloudflare.com` che cambia ogni volta che cloudflared o il server si riavvia. Un piccolo servizio sul server pubblica ogni indirizzo in un argomento casuale di ntfy.sh , firmato (HMAC-SHA256) con una chiave presente solo nella directory di distribuzione (`address-key.txt`), e lo ripete ogni tre ore poiché ntfy.sh conserva i post per 12. `deploy` e **"Trova l’indirizzo attuale"** accettano solo post firmati, quindi un post contraffatto non può inviare te e il tuo token del pannello all’indirizzo di qualcun altro. L’argomento è presente nel registro e nel cloud-init pubblicato: chiunque ne disponga può leggere l’indirizzo corrente, che richiede comunque il token del pannello. Il server non mantiene alcuna porta in entrata in entrambi i casi.

Un verificatore non possiede una chiave di indirizzo e chiunque legga l’argomento può pubblicarvi un post. Pertanto, il collettore pubblica anche l’indirizzo stesso, firmato con la propria chiave Ed25519, e `verify` prende il post più recente firmato dalla chiave del collettore nel record di distribuzione; i post sono ordinati in base all’ora in cui ntfy.sh li ha ricevuti, non all’ora che essi dichiarano. Un collettore precedente a questa modifica non firma nulla, e `verify` prende quindi il messaggio più recente e lo indica nel controllo `statement`; un messaggio contraffatto può solo far fallire tale controllo, poiché l’indirizzo deve comunque rispondere con la chiave del collettore.

Costi: nessun account Cloudflare conserva registrazioni relative a un tunnel temporaneo, pertanto `verify` segnala il tunnel, il connettore e il controllo DNS come non disponibili e il risultato è, nella migliore delle ipotesi, `incomplete` (su Phala Cloud il controllo viene invece superato: il connettore viene eseguito all’interno della configurazione Docker Compose sottoposta a misurazione); i registri del provider, il firewall, la dichiarazione firmata, le misurazioni dell’host e il confronto con il programma di installazione vengono verificati come di consueto. Il confronto a livello di byte con il programma di installazione di riferimento richiede un commit distribuito che riconosca già `--quick-tunnel`; un checkout della versione 0.7.0 compila il programma di installazione del dominio e segnala la differenza. Cloudflare non garantisce l’uptime dei tunnel rapidi, consente 200 richieste in corso e non supporta i Server-Sent Events; pertanto, gli aggiornamenti in tempo reale del pannello (versioni successive alla 0.7.0) potrebbero non arrivare tramite un tunnel di questo tipo e potrebbe essere necessario ricaricare la pagina; tale aspetto non è stato ancora testato. Per un caso in cui sia necessario garantire la disponibilità, si raccomanda di utilizzare il proprio dominio.

## Distribuzione

Controlla prima tutto ciò che verrà inviato. `plan` Non effettua alcuna richiesta al provider né a Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Quindi eseguire il deploy con le stesse opzioni e le credenziali:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Tipi di server con cui iniziare: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` e `--image` per impostazione predefinita, Ubuntu 24.04 di ciascun provider in una regione europea.

`--repository` Prende il commit da un altro repository Git https, senza credenziali nell’ URL (per impostazione predefinita `https://github.com/phishdestroy/TgWitness.git`). `deploy` accetta anche `--out` per un’altra directory di distribuzione (per impostazione predefinita `deployments/NAME`; una directory che contiene già una distribuzione viene rifiutata) e `--wait`, i minuti di attesa per la dichiarazione firmata dal collector: da 1 a 240, predefinito 20, oppure 60 per `generic`.

Il comando:

1. crea un tunnel Cloudflare il cui ingresso inoltra il nome host del pannello al pannello stesso e, se specificato, il nome host del testimone a `/api/witness/head` e `/api/assurance` solo;
2. crea record CNAME proxy per quei nomi host, rifiutando quelli già esistenti;
3. crea un firewall provider senza regole in entrata e un server dietro di esso senza chiave SSH, senza backup, senza agente console e con cloud-init che maschera SSH, blocca l’accesso come root, installa `cloudflared`, recupera esattamente il commit, lo verifica e avvia TgWitness come servizio systemd rinforzato;
4. attende la dichiarazione firmata dal collettore e verifica che indichi questo server e l’ hash di questo cloud-init.

`deployments/case-2026-11/` contiene poi:

| File | Indice | Condividi? |
| --- | --- | --- |
| `deployment.json` | ID, hash, le chiamate API effettuate (metodo, percorso, stato) e la prima dichiarazione firmata | Sì, con il verificatore |
| `cloud-init.redacted.yaml` | Il comando esatto di cloud-init con i suoi due segreti sostituiti da `REDACTED` | Sì |
| `panel-token.txt` | Il token del pannello | No |

La password root del provider, il token del tunnel e il token del pannello non vengono mai scritti su `deployment.json`. Pubblicate l’impronta digitale del collettore riportata alla fine tramite un canale che non controllate da soli, ad esempio un canale testimone o un messaggio al destinatario.

Accedi a Telegram all’indirizzo `https://case.example.org` con il token del pannello, come indicato nella [guida all’account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/). Le azioni del pannello vengono registrate nel registro firmato; non si tratta di sessioni SSH. Un [testimone](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/) può interrogare `https://case-witness.example.org`.

Non è presente SSH: se il bootstrap fallisce, il collector non risponde mai. Eliminare il server e effettuare nuovamente la distribuzione, oppure utilizzare una distribuzione di debug per individuare la causa.

### Segreti nei dati degli utenti

Il cloud-init contiene due segreti: il token del pannello e il token del tunnel Cloudflare. La chiave di firma non è tra questi; viene creata sul server. Hetzner, DigitalOcean e Linode non restituiscono i dati degli utenti tramite le loro API. Vultr li restituisce a qualsiasi chiave in grado di leggere l’ istanza, mentre EC2 tramite `DescribeInstanceAttribute`. Per AWS, fornire al verificatore solo le tre azioni riportate nella tabella, mai `ec2:Describe*`. Per Vultr, si supponga che la chiave del verificatore possa leggere entrambi i token. Un token del tunnel consente a qualcuno di eseguire un secondo connettore: `verify` segnala qualsiasi connettore che non si trovi sul server, e le dichiarazioni del collettore non possono essere falsificate in questo modo poiché ciascuna di esse firma una nuova sfida. Con `--quick-tunnel` il secondo segreto è invece la chiave dell’indirizzo: chiunque la legga può pubblicare un indirizzo falso che il pannello accetterebbe.

La dichiarazione pubblica del responsabile della raccolta omette l’indirizzo del server e le fonti degli accessi; entrambi rimangono nel registro firmato.

## Debug, distribuzione e blocco

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` Conserva SSH per una chiave proveniente da un unico indirizzo o da una rete di piccole dimensioni, al massimo un /24 per IPv4 o un /48 per IPv6. `KEY` è già registrato presso il provider: il nome o l’ID di una chiave SSH nel progetto Hetzner, l’ID o l’impronta digitale di una chiave SSH nel team DigitalOcean, un nome utente Linode le cui chiavi SSH del profilo sono aggiunte a root, l’ID di una chiave SSH nell’account Vultr o il nome di una coppia di chiavi EC2 nella regione. Queste opzioni non si applicano a `generic`. Tale distribuzione viene registrata come `debug` e viene segnalata **mai** come ad alta sicurezza. Al termine, esegui `sudo tgwitness-lock` come ultimo comando dell’ultima sessione SSH, quindi:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Il firewall perde tutte le regole in entrata. I report mostrano quindi quando l’accesso SSH era consentito e quando era bloccato; quella finestra rimane visibile.

## Rimuovi una distribuzione

`destroy` Elimina il server e il relativo firewall, individuati tramite l’etichetta della distribuzione, in modo che venga rimossa anche una distribuzione che ha fallito a metà, quindi i record DNS che puntano al relativo tunnel e il tunnel stesso. Il registro del server e la chiave di firma vengono eliminati insieme ad essi: esportare prima le prove. Il registro rimane, contrassegnato `removed`, con le chiamate API relative alla rimozione.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

La rimozione tramite l’API è implementata per Hetzner. Per gli altri provider `destroy` si interrompe prima di eliminare qualsiasi cosa e indica l’etichetta da eliminare nella console del provider. Un server installato manualmente (`generic`) perde solo il proprio tunnel e i record DNS. Una distribuzione rapida del tunnel non richiede alcun token Cloudflare: il tunnel termina con il server e i relativi post scadono da ntfy.sh entro 12 ore.

## Qualsiasi server (autocertificato)

`--provider generic` È destinato a un server acquistato o installato manualmente. `deploy` crea il tunnel e il DNS, scrive `install.sh` (privato) e `install.redacted.sh` (per la pubblicazione), quindi rimane in attesa. Copiare `install.sh` su un server Ubuntu 24.04 appena installato ed eseguilo lì:

```
sudo bash install.sh
```

Registra l’host così com’era (accessi, account, `authorized_keys`, socket in ascolto, servizi, attività pianificate, pacchetti), installa il commit, abilita il firewall dell’host, si elimina da solo, maschera SSH e termina la sessione. Il report relativo a un server di questo tipo è, nella migliore delle ipotesi, **AUTOCERTIFICATO**: chiunque abbia eseguito il programma di installazione disponeva già dei privilegi di root, e non è disponibile alcuna registrazione del provider per il verificatore. È comunque meglio di un server di cui non si conosce l’origine: l’inventario, l’hash del programma di installazione e ogni accesso successivo sono firmati.

## Verificare

Il verificatore necessita `deployment.json`l'installer pubblicato, credenziali in sola lettura e, idealmente, un checkout del commit e una prova ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Ogni valore relativo al provider e a Cloudflare viene richiesto dal verificatore in quel momento; il record fornisce solo gli ID da richiedere. Il codice di uscita è 0 per **PASS**, 1 per **FAIL** e 2 per **REVIEW**, **INCOMPLETE** o **SELF-ATTESTED**. `--fingerprint` dovrebbe provenire da un canale indipendente ; in sua assenza, la chiave viene confrontata solo con il record dell’operatore. `python verify.py` verifica comunque la prova ZIP, come in [Evidence](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/).

Le azioni del provider vengono classificate: la creazione e l’avvio entro 30 minuti dalla creazione vengono approvate; console, ripristino, reimpostazione password, ricostruzione, ISO, immagini, snapshot, backup, Systems Manager, EC2 Instance Connect e aperture del firewall vengono rifiutate; le azioni relative all’alimentazione e qualsiasi evento imprevisto vengono contrassegnati per la revisione. Un’azione sconosciuta non viene mai ignorata.

## Rapporto per il trasferimento delle prove

`--report report.md` scrive il report in Markdown e `report.json` accanto ad esso:

1. risultato, impronta digitale della chiave del collector, distribuzione, provider, commit, server, firewall, tunnel;
2. ogni verifica con il relativo stato e la fonte (API del provider, API di Cloudflare, dichiarazione del collettore, registro delle prove);
3. il registro del fornitore con la valutazione di ciascuna azione e, laddove il fornitore lo registri, l’autore dell’azione;
4. gli endpoint Cloudflare che contengono le connessioni del tunnel, la configurazione e il registro di audit;
5. la dichiarazione firmata del collezionista;
6. ciò che il rapporto stabilisce e ciò che non stabilisce;
7. i comandi per riprodurlo e l’SHA-256 di ogni file che gli è stato fornito.

Consegnare il rapporto, `report.json`, `deployment.json`, il programma di installazione pubblicato e le prove ZIP. Preparate il rapporto tempestivamente: i log dei provider vengono conservati per periodi limitati.

## Cloudflare come testimone esterno

Tutto ciò che è riportato qui è facoltativo. Anche senza un account Cloudflare il server continua a funzionare, e due di questi sono attualmente operativi:

| Cosa | Cosa mostra | In TgWitness |
| --- | --- | --- |
| Tunnel rapido o tunnel del proprio dominio | È possibile accedere al pannello solo tramite il tunnel | la procedura guidata per il server, vedi sopra |
| drand relay `drand.cloudflare.com` | i registri successivi a un round di drand sono più recenti di esso: il diario è stato scritto man mano che si svolgeva | modalità prove, **Altri testimoni**, nessun account ([formato](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Notifiche sullo stato del tunnel | quando il tunnel era inattivo, tramite e-mail o webhook da Cloudflare | Configurali nella dashboard di Cloudflare |
| Gateway DNS (`--gateway-dns`, o **Cloudflare Gateway DNS** nella procedura guidata) | ogni nome cercato dal server, a cui Cloudflare ha risposto tramite TLS; il firewall di Hetzner impedisce al DNS di raggiungere qualsiasi altra risorsa; se una politica del Gateway potesse riscrivere le risposte | Hetzner, piano Zero Trust gratuito, senza dominio; `verify` controlla il firewall, la posizione, la registrazione dei log, le politiche, le query del server e il registro di audit; la modalità "evidence" copia il log nel registro |
| Gateway con il client Cloudflare One sul server, un firewall in uscita che consente l’accesso solo a Cloudflare | ogni connessione effettuata dal server, non solo quelle DNS | non ancora realizzato |
| Accesso davanti al pannello | chi ha effettuato l’accesso al pannello e quando | non implementato: richiede un dominio proprio |
| Registrazione dei comandi SSH | ogni comando in una sessione di debug | non ancora realizzato |

Logpush, che conserverebbe una copia di Cloudflare in R2, è una funzionalità Enterprise: nel piano gratuito Cloudflare risponde `logpush is not enabled for this account`. Il log del Gateway rimane lì per 24 ore, quindi la modalità "evidence" lo copia nel registro firmato (**il log di Cloudflare Gateway relativo alle query DNS di questo server**, un token di sola lettura con Account Analytics Read).

Senza un piano Zero Trust, un account ha un’unica posizione DNS. Quando Cloudflare ne rifiuta un’altra, il server condivide quella esistente e le sue query vengono distinte in base all’indirizzo; tale filtro richiede anche Zero Trust PII Read e `destroy` lascia un’ubicazione condivisa. Una query di log copre al massimo tre ore, quindi la copia e la `verify` leggere la giornata in finestre di tre ore.

Il DNS gateway gestisce il resolver di sistema. Il DNS over HTTPS sulla porta 443 verso un altro resolver e le connessioni a un indirizzo non presente in nessun elenco (come, ad esempio, i data center di Telegram) non vengono registrate nel suo log.

Cloudflare non può vedere all’interno della crittografia di Telegram, né gli altri dispositivi collegati all’account Telegram (l’elenco dei dispositivi in modalità “evidence” li registra dal lato di Telegram) né l’hypervisor del provider.

## Cosa questo non stabilisce

- Il provider e il suo personale gestiscono l’hypervisor, i dischi e la rete.
- Le misurazioni dell’host vengono comunicate autonomamente dal collettore.
- I contenuti delle regole del firewall precedenti non sono presenti in tutti i log dei provider; solo Linode conserva le versioni delle regole.
- Non aggiunge nulla di nuovo riguardo all’autenticità dei messaggi; si veda la sezione [“Prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)”.

Non ancora testato su account reali: un’implementazione sul proprio dominio (tunnel Cloudflare e DNS), gli altri provider, un’implementazione di debug e `lock`, un account Telegram su tale server, e gli aggiornamenti in tempo reale delle versioni successive tramite un tunnel veloce. Verifica la prima implementazione su ogni provider con `plan`, un'implementazione di debug e `verify` prima di utilizzarlo in un caso.
