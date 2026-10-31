# Condivida un caso

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/access/

Condivida il caso di cui qualcuno ha bisogno. Mantenga il controllo sul resto.

01**Scegliere le prove**

È possibile selezionare interi spazi di lavoro dell’account o singole chat registrate.

02**Selezionare le azioni**

Consentire la visualizzazione, l’esportazione o le autorizzazioni operative specifiche di cui la persona ha bisogno.

03**Stabilire i limiti**

Emittete un token personale con scadenza, limiti di sessione e restrizioni IP opzionali.

L’ambito di raccolta determina ciò che viene registrato. L’ambito di accesso determina ciò che una persona può vedere e fare.

## Concedere l’accesso a qualcuno

1. Acceda come amministratore e apra la sezione **«Accesso**».
2. Indicare l’accesso e selezionare gli spazi di lavoro e le chat.
3. Mantenere la voce **«Visualizza»** per il revisore. Aggiungere **«Esporta»** qualora fosse necessario scaricare i registri.
4. Impostare i limiti, quindi premere **«Crea accesso**».
5. Copi una volta il token visualizzato. Lo invii in privato insieme all’indirizzo del pannello.
6. Verifichi la visualizzazione consentita in una sessione separata del browser prima di consegnarlo.

## Si parta dal lavoro che devono svolgere

| Persona | Accesso | Risultato |
| --- | --- | --- |
| Revisore | Chat selezionate; solo visualizzazione | Legga la conversazione acquisita senza modificare la raccolta. |
| Analista | Chat selezionate; visualizzazione ed esportazione | Esaminare e scaricare i registri necessari per il caso. |
| Operatore | Spazi di lavoro interi selezionati; fonti e raccolta | Gestire ciò che viene monitorato e avviare o arrestare i collettori. |

Si tratta di configurazioni che potete scegliere, non di ruoli fissi. Le impostazioni a livello di account e le esportazioni complete del registro rimangono inaccessibili alle chat con accesso limitato anche quando è abilitata un’altra autorizzazione. L’accesso a tutti gli spazi di lavoro include gli account futuri.

## Potete cambiare idea in qualsiasi momento

Modifichi le impostazioni di accesso per determinare le operazioni consentite nelle richieste successive. Chiuda una singola sessione oppure revochi l’intero accesso per terminare tutte le sessioni in corso. I file già scaricati non possono essere recuperati. La chiusura di una sessione del pannello non interrompe la raccolta dei dati.

**Limiti relativi alle sessioni e agli indirizzi IP**

Limitare le sessioni parallele e gli accessi riusciti, impostare una data di scadenza assoluta, consentire indirizzi IP o sottoreti, oppure vincolare l’accesso all’indirizzo utilizzato per il primo accesso. La scadenza della sessione viene determinata in base all’inattività; il polling di un pannello aperto viene considerato come attività. Verificare l’indirizzo del client visualizzato dall’applicazione quando questa viene eseguita dietro un proxy o un tunnel.

**La chiave principale e il registro delle attività**

L’amministratore conserva il token del pannello principale. Gli utenti con autorizzazione di accesso non possono gestire l’accesso di altre persone né aprire la console di amministrazione. La console mostra l’attività dei processi in corso in tutti gli spazi di lavoro; i registri di accesso firmati conservano gli eventi relativi alle autorizzazioni e alle sessioni senza l’utilizzo di token. Gli spazi di lavoro condividono il processo host e non isolano i dati dall’amministratore del server.

Si prega di utilizzare il [riferimento completo alle autorizzazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/) per tutte e sette le autorizzazioni, le regole di sessione e i limiti dell’amministratore.
