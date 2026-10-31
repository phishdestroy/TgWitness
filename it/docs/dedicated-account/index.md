# Utilizzi un account separato. Mai quello principale.

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/dedicated-account/

Legga attentamente prima di collegare un account

Il nostro consiglio di non utilizzare il Suo account principale non è uno scherzo. È la realtà.

Account principale

- Hash della propria app: 99% disconnessi
- I blocchi dovuti esclusivamente a un basso livello di affidabilità sono frequenti
- Utilizzarlo è un’idea davvero stupida

Account aggiuntivo sulle coppie pubbliche

- Oltre un milione di account registrati tramite queste coppie
- Queste coppie sono attive da oltre 5 anni
- Nessuno può vedere nulla di ciò che Le appartiene attraverso di essi

01

## Perché non il Suo account principale?

Si tratta di informazioni accurate. Sappiamo esattamente dove si trovano le insidie di questi problemi.

1. ### Hash della propria app: 99% disconnessi

   Accedere a my.telegram.org da un account a cui non si ha accesso, per ottenere l’hash di un’app, e successivamente effettuare qualsiasi richiesta tramite tale hash comporta una probabilità del 99% che l’account venga disconnesso. È possibile verificarlo.
2. ### I blocchi dovuti esclusivamente a un basso livello di affidabilità sono frequenti

   Gli account vengono bloccati semplicemente perché Telegram non si fida di essi, e tali blocchi sono frequenti. Potete verificarlo anche voi. Utilizzare il proprio account è un’idea davvero stupida.
3. ### Le chiavi di sessione copiate possono essere revocate

   L’esecuzione simultanea di una chiave TData/sessione importata in Telegram Desktop e TgWitness può causare l’errore `AUTH_KEY_DUPLICATED`. Telegram invalida tale autorizzazione, pertanto entrambe le copie richiedono un nuovo accesso. Un account dedicato non impedisce che ciò accada.

   Chiuda completamente il client originale e lo mantenga chiuso mentre utilizza la sessione importata. Per un utilizzo in parallelo, effettui l’accesso a TgWitness tramite telefono o codice QR per creare un’autorizzazione separata; gli altri client autorizzati separatamente possono rimanere connessi.

   [Legga l’avviso relativo all’importazione della sessione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it#session-warning)

Documentazione di Telegram

- [Errori di disconnessione: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Creazione dell’hash della propria app: ottenimento dell’api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Perché TgWitness funziona tramite coppie pubbliche di hash dell’app e ID dell’app

Ecco perché abbiamo realizzato TgWitness basandoci su coppie pubbliche di hash dell’app e ID dell’app. Secondo la nostra logica, con queste coppie il rischio di ban è minore: oltre un milione di account Telegram sono stati registrati tramite queste coppie e molti programmi diversi funzionano grazie ad esse. Secondo la nostra logica, ciò è preferibile rispetto all’utilizzo diretto di un hash dell’app personale: queste coppie sono attive da oltre 5 anni, senza alcun dubbio.

### La vostra nuova coppia

Creato su my.telegram.org dall’account.

- Circa il 99% degli account è stato disconnesso
- Una nuova applicazione, un unico account

### Coppie pubbliche del pool

Le stesse coppie utilizzate da molti programmi.

- Oltre un milione di account registrati
- Molti programmi diversi
- Attivo da oltre 5 anni

### Perché nessuno può vedere nulla di ciò che Le appartiene attraverso queste coppie

- #### La coppia è un nome, non una chiave

  Telegram richiede l’ID API e l’hash API quando un programma si connette e quando richiede un codice di accesso. Essi identificano l’applicazione e non conferiscono alcun accesso ad alcun account; la documentazione di Telethon precisa che una coppia di questi dati funziona con qualsiasi numero di telefono.
- #### La vostra chiave di sessione non lascia mai il vostro server

  L’accesso crea una chiave di autorizzazione tramite uno scambio Diffie–Hellman tra il Suo TgWitness e Telegram; la chiave stessa non viene mai inviata. Documentazione di Telegram: dopo l’autorizzazione, la chiave viene associata all’utente e ogni chiamata effettuata con tale chiave viene eseguita a nome di quell’utente. Altri programmi con la stessa coppia dispongono delle proprie chiavi e non possono utilizzare la Sua.
- #### Il traffico è crittografato con la Sua chiave

  Ogni richiesta e risposta viene crittografata con la chiave di autorizzazione della sessione, non con l’hash dell’API. La conoscenza dell’hash dell’API non consente di decrittografare nulla.
- #### Il proprietario di una coppia non vede nulla

  Telegram non dispone di alcun metodo che elenchi account, sessioni o messaggi in base all’ID API. Il titolare di una coppia vede solo le impostazioni della propria app su my.telegram.org.
- #### Solo il Suo account può vedere di quale app si tratta

  La sezione Impostazioni → Dispositivi del proprio account elenca il nome dell’app e l’ID API, il dispositivo, l’indirizzo IP e le date di ciascuna sessione. Nessun altro ha accesso a questo elenco.

Documentazione di Telegram

- [Autorizzazione dell’utente: la chiave diventa l’utente](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Creazione di una chiave di autorizzazione](https://core.telegram.org/mtproto/auth_key)
- [Crittografia MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Cosa contiene un registro di sessione](https://core.telegram.org/constructor/authorization)
- [Ottenere l’api_id](https://core.telegram.org/api/obtaining_api_id)
- [Codice sorgente aperto delle app Telegram](https://telegram.org/apps#source-code)

Librerie e discussioni

- [Telethon: accesso](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: API dell’app ufficiale](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: l’api_hash dovrebbe essere mantenuto segreto?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Le stesse coppie in altri programmi 7

Le coppie di app ufficiali di Telegram sono pubbliche e integrate in numerosi programmi e librerie indipendenti:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Elenco sul forum delle coppie di app ufficiali, pubblicato per la registrazione degli account

03

## Modalità per creare un account aggiuntivo

Un account Telegram richiede un numero di telefono su cui ricevere il codice di accesso. Scegliete in base alla durata prevista dell’account.

- La scelta migliore

  ### SIM prepagata o eSIM

  ********

  Ultime modifiche

  A condizione che lo mantenga sempre rifornito

  Prestare attenzione

  La soluzione più affidabile: Telegram accetta al meglio i numeri di cellulare reali. Un numero ritirato dall’operatore viene assegnato a qualcun altro.
- ### App per numeri virtuali

  ********

  Ultime modifiche

  Sebbene l’app mantenga il numero

  Prestare attenzione

  Telegram potrebbe rifiutare un numero virtuale, non inviare il codice o limitare immediatamente il nuovo account; alcune app ritirano i numeri che non vengono utilizzati.
- ### Noleggio di numeri

  ********

  Ultime modifiche

  Il periodo di noleggio

  Prestare attenzione

  Al termine, il numero passa al cliente successivo.
- ### Attivazione una tantum

  ********

  Ultime modifiche

  Un unico codice

  Prestare attenzione

  Il numero torna immediatamente nel pool, spesso con una cronologia dei precedenti proprietari. Impostare la password del cloud prima di qualsiasi altra operazione.

Chiunque entri in possesso del numero in un secondo momento potrà richiedere un codice di accesso. Una password cloud (verifica in due passaggi) impedisce l’accesso; in sua assenza, l’account appartiene al successivo proprietario del numero.

Documentazione di Telegram

- [Domande frequenti sullo spam: numeri virtuali e precedenti proprietari](https://telegram.org/faq_spam)
- [Verifica in due passaggi](https://core.telegram.org/api/srp)

### Numeri +888 noleggiati (Fragment)

Alcuni marketplace e servizi offrono il noleggio temporaneo dei numeri ufficiali +888 di Telegram tramite Fragment.

Prezzo indicativo: 20 dollari USA al giorno.

- È possibile registrare un account direttamente su Telegram Web o Telegram Desktop.
- È possibile eliminare gli account associati al numero e crearne di nuovi.
- Questi account sono generalmente soggetti a un numero minore di controlli antifrode, ma non garantiscono alcuna immunità né privilegi speciali.

Il numero non è di Sua proprietà. Al termine del periodo di noleggio, il proprietario potrà rivendicarne la proprietà. Imposti immediatamente una «password cloud» e non consideri l’account come un servizio a lungo termine.

Possedere personalmente il numero +888 o utilizzare una SIM prepagata di cui si ha il controllo rimane la soluzione più affidabile.

### Account già pronti disponibili sui marketplace

Alcuni marketplace (ad esempio G2G o Z2U) vendono account Telegram già pronti: nuovi, con storia di utilizzo o con file di sessione.

- [G2G: Elenco degli account Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Elenco degli account Telegram](https://www.z2u.com/telegram/accounts-5-15140)

NON UTILIZZI MAI IL SUO ACCOUNT PRINCIPALE! Un account dedicato ottenuto in questo modo è comunque più sicuro rispetto all’inserimento del Suo account Telegram principale in TgWitness.

#### Avvertenze prima dell’acquisto

- Ciò costituisce una violazione dei Termini di servizio di Telegram.
- Molti account sono stati registrati in massa (registrazione automatica) o presentano una cronologia sconosciuta.
- Alcuni venditori potrebbero ancora disporre di un accesso di recupero.
- Gli account provenienti da tali mercati vengono spesso bloccati o soggetti a restrizioni in un secondo momento.
- Si eviti il ricorso a marketplace che vendono apertamente software di furto di credenziali, strumenti di phishing o account chiaramente rubati.
- L’acquisto di un account — anche se pubblicizzato come “auto-reg” — da piattaforme che vendono apertamente strumenti di phishing, software di furto di credenziali, sessioni rubate o account, viola non solo i Termini di servizio di Telegram, ma anche le leggi della maggior parte dei paesi. Ciò potrebbe in seguito invalidare le vostre prove. Scegliete con attenzione.

#### Se utilizza questa opzione

1. Considerare l’account come usa e getta.
2. Chiuda tutte le altre sessioni, imposti una «password cloud» e modifichi immediatamente i metodi di recupero.
3. Utilizzi 2–3 account di provider diversi o account da Lei stesso registrati.

**Premium, cancellazione e il ritardo di sette giorni**

Se l’account dispone della funzione Premium, chiunque abbia accesso al numero di telefono non potrà cancellare immediatamente l’account. Riceverà una notifica e avrà a disposizione sette giorni prima della cancellazione.

Ciò è importante poiché la Sua indagine dipende dall’account: ha tempo per predisporne uno sostitutivo.

**Account nuovi e credenziali API**

Se si ottengono e si utilizzano i propri api_id/api_hash da un account nuovo registrato personalmente utilizzando un numero proveniente da un servizio SMS, l’account verrà disconnesso alla prima richiesta API o all’autorizzazione della sessione. Si prega di tenerlo presente quando si pianifica un’indagine.

04

## Creazione dell’account

Da un numero alla prima chat registrata.

1. ### Ottenere un numero

   Una SIM prepagata o un’eSIM quando l’account deve rimanere attivo a lungo; un noleggio o un’attivazione una tantum per un incarico di breve durata. I servizi sono elencati di seguito.
2. ### Si registri separatamente dal Suo account principale

   Effettuare la registrazione nell’app ufficiale di Telegram su un dispositivo separato, un emulatore o un profilo telefonico, non accanto al proprio account principale.
3. ### Proteggetelo con una password cloud

   Impostare immediatamente una password per il cloud e un indirizzo e-mail di recupero non utilizzati altrove.
4. ### Chiuda le impostazioni sulla privacy

   Numero di telefono **Nessuno**, trovatemi tramite il mio numero **I miei contatti**, visto l’ultima volta, foto del profilo e biografia **Nessuno** o **I miei contatti**; disattivate la sincronizzazione dei contatti.
5. ### Evitare che si autodistrugga

   Impostare l’autodistruzione dell’account sul periodo più lungo, in modo che un’interruzione di TgWitness non comporti la perdita dell’account.
6. ### Conferitegli un profilo neutro

   Non inserite nomi, foto, nomi utente o biografie provenienti dai vostri altri account, né contatti personali.
7. ### Lasciatelo riscaldare

   All’inizio, partecipi a poche chat al giorno. Gli account nuovi che agiscono con troppa fretta vengono limitati per primi.
8. ### Non condividete nulla con i bot

   Non premetta mai «Condividi numero di telefono» o «Condividi posizione» per un bot. Apra i link e le Mini App tramite una VPN o un proxy su quel dispositivo.
9. ### Collegarlo a TgWitness

   Nel proprio spazio di lavoro, accedete a **Account → Codice QR**, quindi selezionate **Fonti → Modalità investigativa**. L’app è il luogo in cui agite, TgWitness è il registro.

Documentazione di Telegram

- [Verifica in due passaggi](https://core.telegram.org/api/srp)
- [Impostazioni sulla privacy](https://core.telegram.org/api/privacy)
- [Autodistruzione dell’account](https://core.telegram.org/method/account.setAccountTTL)

05

## Servizi numerici

Opzioni da cui partire. I paesi, i prezzi e l’accettazione da parte di Telegram di un determinato numero sono soggetti a frequenti variazioni; si raccomanda di verificare prima di effettuare il pagamento.

### SIM prepagate ed eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Prepagato

  Piano PayGo, molto conveniente
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Prepagato
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Prepagato
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Prepagato
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### App per numeri virtuali 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Solo per gli Stati Uniti; la registrazione richiede un numero di telefono statunitense
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Il numero viene ritirato se non lo utilizza
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Altri paesi
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - A pagamento

  Con un periodo di prova
- [Hushedhushed.com](https://hushed.com)

  - Molti paesi
  - A pagamento

  Economico
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Numeri di cellulare europei in un’app
- [Sonetelsonetel.com](https://sonetel.com)

  - Molti paesi
  - Numero gratuito
- [Zadarmazadarma.com](https://zadarma.com)

  - Molti paesi

  Numeri virtuali

### Numero di noleggi e attivazioni: 12

L’abbonamento mantiene un numero per settimane o mesi. Un’attivazione una tantum fornisce un codice unico: impostare la password del cloud subito dopo la registrazione.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Noleggio
  - Attivazioni
- [SMSPVAsmspva.com](https://smspva.com)

  - Noleggio
  - Attivazioni
- [5SIM5sim.net](https://5sim.net)

  - Noleggio
  - Attivazioni
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Noleggio
  - Una tantum
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Noleggio
  - Attivazioni
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Noleggio
  - Attivazioni
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Noleggio
  - Attivazioni
- [365SMS365sms.org](https://365sms.org)

  - Noleggio
  - Attivazioni
- [SIMSMSsimsms.org](https://simsms.org)

  - Noleggio
  - Attivazioni
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Una tantum
- [SMS-MANsms-man.com](https://sms-man.com)

  - Una tantum
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Una tantum
