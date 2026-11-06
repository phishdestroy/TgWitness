# Telegram · Gestisci l’archivio

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/archive/

Trova il messaggio. Verifica la fonte. Costruisci il caso.

01**Inserire la cronologia**

Porti nello spazio i messaggi passati delle Sue fonti attive.

02**Segui le fonti**

Cerchi, poi apra il messaggio salvato dietro ogni risultato.

03**Mantenere chiara la transizione**

La Sua analisi in un file, la prova firmata accanto.

I dati acquisiti, il testo riconosciuto e le conclusioni degli analisti rimangono ben distinti.

## Carica i messaggi precedenti

1. **Fonti → Chat incluse**: controlli le chat attive e avvii l’osservazione.
2. **Carica cronologia completa**. Usa l’elenco delle fonti così com’è in quel momento.
3. **Metti in pausa la cronologia** / **Riprendi la cronologia** quando vuole. Dopo un riavvio riprenda a mano.
4. Controlli il risultato per fonte e la coda dei download, e conservi il report di avanzamento firmato con l’esportazione.

Così si riempie lo spazio. L’esportazione di una singola chat in HTML/JSON è un’altra cosa. [Dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/).

## Prima cerca, poi decidi in merito all’IA

1. **Diario** cerca in locale, con filtri per fonte e data.
2. Cerchi una frase o un dominio e apra la voce e le sue versioni.
3. Per l’IA l’amministratore configura un provider in **Integrazioni**. Poi **Chiedi all’archivio**: scelga chat e periodo, guardi **Dati inviati al modello** e tolga la spunta a ciò che non deve uscire.
4. Controlli le citazioni, salvi la risposta come report e aggiunga le Sue note.

La ricerca non ha bisogno dell’IA. I report conservano fonti e revisioni, separati dal diario firmato. [Configurare il provider](https://phishdestroy.github.io/TgWitness/it/docs/reference/analysis/).

## Scegli la connessione che ti serve

| Compito | Apri | Configurazione |
| --- | --- | --- |
| Far leggere a un client IA le chat scelte | **Integrazioni → MCP** | [Installare MCP, creare un token limitato, collegarsi](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/) |
| Riconoscimento del testo nei file multimediali salvati | Un record `media.saved` → **Riconoscere l'allegato** | [Configurare il worker Docker locale](https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/) |
| Invia gli eventi a n8n o a un SIEM | **Integrazioni → Webhook in uscita** | [Aggiungere un ricevitore, verificare l’HMAC, scartare ID duplicati](https://phishdestroy.github.io/TgWitness/it/docs/reference/webhooks/) |

**Quale token di accesso va dove?**

L’accesso al pannello è per le persone. MCP ha i propri token di sola lettura, i webhook il proprio segreto HMAC. Nessuno ha bisogno di una sessione Telegram.

[Condividi l'accesso al pannello di controllo](https://phishdestroy.github.io/TgWitness/it/docs/access/) o [configura un client MCP](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/).

## Fornire fonti e conclusioni

Metta il report accanto allo ZIP firmato. Il report è la Sua lettura delle fonti; lo ZIP è ciò che il destinatario verifica.

[Esportare e verificare](https://phishdestroy.github.io/TgWitness/it/docs/exports/) · [Svolgimento di un'indagine completa](https://phishdestroy.github.io/TgWitness/it/docs/cases/)
