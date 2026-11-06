# Telegram · Condivida un caso

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/access/

Condivida il caso di cui qualcuno ha bisogno. Mantenga il controllo sul resto.

01**Scegliere le prove**

Spazi interi o singole chat.

02**Selezionare le azioni**

Vedere, esportare o solo le operazioni necessarie.

03**Stabilire i limiti**

Un token personale con scadenza, limiti di sessione e regole IP, se vuole.

L’ambito di raccolta determina ciò che viene registrato. L’ambito di accesso determina ciò che una persona può vedere e fare.

## Concedere l’accesso a qualcuno

1. Come amministratore apra **Accesso**.
2. Gli dia un nome, scelga spazi e chat.
3. A un revisore basta **Visualizza**. Per i download aggiunga **Esporta**.
4. Impostare i limiti, quindi premere **«Crea accesso**».
5. Copi il token (mostrato una sola volta) e lo invii in privato insieme all’indirizzo del pannello.
6. Controlli prima cosa vedrà la persona, in una sessione del browser separata.

## Si parta dal lavoro che devono svolgere

| Persona | Accesso | Risultato |
| --- | --- | --- |
| Revisore | Chat selezionate; solo visualizzazione | Legge la chat, non può cambiare nulla. |
| Analista | Chat selezionate; visualizzazione ed esportazione | Legge e scarica ciò che serve al caso. |
| Operatore | Spazi di lavoro interi selezionati; fonti e raccolta | Decide cosa osservare, avvia e ferma i collector. |

Sono solo esempi, non ruoli fissi. Un accesso limitato alle chat non ottiene mai impostazioni dell’account né esportazioni complete del diario. L’accesso a tutti gli spazi include gli account aggiunti dopo.

## Potete cambiare idea in qualsiasi momento

Modifichi l’accesso quando vuole, vale dalla richiesta successiva. Chiuda una sessione o revochi tutto. I file già scaricati non tornano indietro. La raccolta continua.

**Limiti relativi alle sessioni e agli indirizzi IP**

Limiti sessioni parallele e accessi, imposti una data di fine, consenta IP o sottoreti o leghi l’accesso all’IP del primo login. La scadenza conta l’inattività; un pannello aperto conta come attivo. Dietro un proxy controlli quale IP client vede l’app.

**La chiave principale e il registro delle attività**

Il token principale resta all’amministratore. Un accesso rilasciato non può gestire l’accesso altrui né aprire la console di amministrazione. Modifiche di accesso e sessioni vengono firmate nel diario, senza token. L’amministratore del server continua a vedere tutto.

I sette permessi e le regole di sessione: [riferimento accessi](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/).
